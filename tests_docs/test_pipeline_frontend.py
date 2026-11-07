# this_file: tests_docs/test_pipeline_frontend.py
"""Verify the actual English browser notices, source maps and output boundary."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FrontendPayloadTests(unittest.TestCase):
    def test_every_current_notice_is_exact_in_source_and_generated_payload(self):
        record = json.loads((ROOT / 'src_docs/md/assets/current-frontend-notices.json').read_text())
        self.assertEqual(record['scope'], 'Current English browser payload and exact retained notices; build dependencies and external services have separate provenance.')
        names = {row['name'] for row in record['components']}
        self.assertTrue({'clipboard', 'tiny-emitter', 'select', 'good-listener', 'delegate', 'escape-html', 'focus-visible', 'rxjs', 'tslib', 'lunr', 'material-design-color', '@mdi/svg', '@fortawesome/fontawesome-free', '@primer/octicons', 'lucide-static'} <= names)
        page = (ROOT / 'src_docs/md/frontend-notices.md').read_text()
        count = 0
        for row in record['components']:
            self.assertTrue(row['source_url'].startswith('https://'))
            for notice in row['notices']:
                count += 1
                data = (ROOT / 'src_docs/md' / notice['path']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), notice['sha256'])
                self.assertEqual((ROOT / 'docs' / notice['path']).read_bytes(), data)
                self.assertIn(notice['path'], page)
                if row['name'] in ('select', 'good-listener', 'delegate'):
                    self.assertEqual(data.decode().strip(), '## License\n\n[MIT License](http://zenorocha.mit-license.org/) © Zeno Rocha')
        self.assertEqual(count, 25)

    def test_current_source_map_identities_and_exact_embedded_sources_are_retained(self):
        record = json.loads((ROOT / 'src_docs/md/assets/current-frontend-notices.json').read_text())
        for row in record['source_maps']:
            data = (ROOT / 'docs' / row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), row['sha256'])
            source_map = json.loads(data)
            self.assertEqual(source_map['sources'], [s['source'] for s in row['sources']])
            if 'sourcesContent' in source_map:
                self.assertEqual(len(source_map['sourcesContent']), row['sources_count'])
                for body, source in zip(source_map['sourcesContent'], row['sources']):
                    self.assertEqual(hashlib.sha256(body.encode()).hexdigest(), source['sha256'])
                    if 'package' in source:
                        self.assertTrue(source['byte_exact'])
            else:
                self.assertTrue(all(source['sha256'] is None for source in row['sources']))
        self.assertEqual([row['sources_count'] for row in record['source_maps']], [211, 13, 51, 5])

    def test_complete_current_output_contains_no_omitted_helper_or_font_binary(self):
        policy = json.loads((ROOT / 'src_docs/md/assets/english-search-omissions.json').read_text())
        self.assertEqual(len(policy['omitted']), 34)
        for row in policy['omitted']:
            self.assertFalse((ROOT / 'docs' / row['path']).exists())
        for row in policy['retained']:
            self.assertEqual(hashlib.sha256((ROOT / 'docs' / row['path']).read_bytes()).hexdigest(), row['sha256'])
        self.assertFalse([p for p in (ROOT / 'docs').rglob('*') if p.suffix.lower() in ('.woff', '.woff2', '.ttf', '.otf')])
