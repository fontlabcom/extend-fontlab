# this_file: tests_docs/test_build.py
"""Rebuild the actual shell entrypoint across midnight and a generated commit."""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReproducibleBuildTests(unittest.TestCase):
    def test_cross_date_generated_commit_reuses_source_epoch_for_all_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / 'src_docs', root / 'src_docs')
            env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
            env.pop('SOURCE_DATE_EPOCH', None)
            env.pop('GIT_INDEX_FILE', None)
            env.update(GIT_AUTHOR_DATE='2026-11-05T12:00:00Z', GIT_COMMITTER_DATE='2026-11-05T12:00:00Z')
            git = [shutil.which('git'), '-C', str(root)]
            for args in (['init', '-b', 'main'], ['config', 'user.name', 'Fixture'], ['config', 'user.email', 'fixture@example.invalid'], ['add', 'src_docs'], ['commit', '-m', 'source']):
                subprocess.run(git + args, env=env, check=True, capture_output=True)
            epoch = subprocess.check_output(git + ['show', '-s', '--format=%ct', 'HEAD'], env=env, text=True).strip()
            bindir = root / 'bin'
            bindir.mkdir()
            shim = bindir / 'properdocs'
            shim.write_text(f'#!{sys.executable}\n' + '''import os
from datetime import datetime, timezone
import properdocs.utils
from properdocs.__main__ import cli
class Clock(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 11, 6, 23, 59, 59, tzinfo=timezone.utc) if os.environ['BUILD_TEST_CLOCK'] == 'before' else datetime(2026, 11, 7, 0, 0, 1, tzinfo=timezone.utc)
properdocs.utils.datetime = Clock
cli()
''')
            shim.chmod(0o755)
            env['PATH'] = str(bindir) + os.pathsep + env['PATH']
            env['BUILD_TEST_CLOCK'] = 'before'
            result = subprocess.run(['sh', str(root / 'src_docs/build.sh')], env=env, text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            first = {str(p.relative_to(root / 'docs')): hashlib.sha256(p.read_bytes()).hexdigest() for p in (root / 'docs').rglob('*') if p.is_file()}
            self.assertEqual(len(first), 50)
            self.assertIn(datetime.fromtimestamp(int(epoch), UTC).strftime('%Y-%m-%d'), (root / 'docs/sitemap.xml').read_text())
            env.update(GIT_AUTHOR_DATE='2026-11-07T00:00:01Z', GIT_COMMITTER_DATE='2026-11-07T00:00:01Z')
            subprocess.run(git + ['add', 'docs'], env=env, check=True, capture_output=True)
            subprocess.run(git + ['commit', '-m', 'generated output'], env=env, check=True, capture_output=True)
            generated_epoch = subprocess.check_output(git + ['show', '-s', '--format=%ct', 'HEAD'], env=env, text=True).strip()
            self.assertNotEqual(generated_epoch, epoch)
            env.update(SOURCE_DATE_EPOCH=epoch, BUILD_TEST_CLOCK='after')
            result = subprocess.run(['sh', str(root / 'src_docs/build.sh')], env=env, text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            second = {str(p.relative_to(root / 'docs')): hashlib.sha256(p.read_bytes()).hexdigest() for p in (root / 'docs').rglob('*') if p.is_file()}
            self.assertEqual(first, second, 'Every file, including sitemap.xml and its gzip, must match')
            self.assertEqual(subprocess.check_output(git + ['diff', '--name-only', '--', 'docs'], env=env, text=True), '')
