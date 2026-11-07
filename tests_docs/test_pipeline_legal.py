# this_file: tests_docs/test_pipeline_legal.py
"""Exact licence and generated asset bytes must survive real Git distribution."""
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LegalDistributionTests(unittest.TestCase):
    def test_current_licences_and_generated_assets_survive_index_checkout_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            names = subprocess.check_output(['git', 'rev-parse', '--local-env-vars'], cwd=root, text=True).splitlines()
            env = {k: v for k, v in os.environ.items() if k not in names}
            command = ['git', '-c', 'core.autocrlf=input', '-C', str(root)]
            subprocess.run(command + ['init', '--quiet'], env=env, check=True)
            shutil.copyfile(ROOT / '.gitattributes', root / '.gitattributes')
            paths = {}
            policy = json.loads((ROOT / 'src_docs/md/assets/english-search-omissions.json').read_text())
            self.assertEqual(len(policy['omitted']), 34)
            self.assertEqual(len(policy['retained']), 9)
            for row in policy['omitted']:
                self.assertFalse((ROOT / 'docs' / row['path']).exists(), row['path'])
            paths.update({Path('docs') / row['path']: row['sha256'] for row in policy['retained']})
            frontend = json.loads((ROOT / 'src_docs/md/assets/current-frontend-notices.json').read_text())
            for component in frontend['components']:
                for notice in component['notices']:
                    paths[Path('src_docs/md') / notice['path']] = notice['sha256']
                    paths[Path('docs') / notice['path']] = notice['sha256']
            payloads = {}
            for relative, digest in paths.items():
                data = (ROOT / relative).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), digest, str(relative))
                payloads[relative] = data
            # Exercise CRLF even when the actual upstream payload happens to be LF.
            payloads[Path('docs/owned-line-ending-probe.txt')] = b'owned\r\nbytes\r\n'
            payloads[Path('src_docs/md/assets/owned-probe.txt')] = b'# retained\r\nguide\r\n'
            for relative, data in payloads.items():
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            subprocess.run(command + ['add', '.'], env=env, check=True, capture_output=True)
            tree = subprocess.check_output(command + ['write-tree'], env=env, text=True).strip()
            archive_bytes = subprocess.check_output(command + ['archive', tree], env=env)
            with tarfile.open(fileobj=io.BytesIO(archive_bytes)) as archive:
                for relative, expected in payloads.items():
                    self.assertEqual(subprocess.check_output(command + ['show', ':' + relative.as_posix()], env=env), expected, str(relative))
                    self.assertEqual(archive.extractfile(relative.as_posix()).read(), expected, str(relative))
            checkout = root / 'checkout'
            checkout.mkdir()
            subprocess.run(command + ['checkout-index', '--all', '--prefix=' + str(checkout) + '/'], env=env, check=True)
            for relative, expected in payloads.items():
                self.assertEqual((checkout / relative).read_bytes(), expected, str(relative))
