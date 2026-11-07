# this_file: tests_docs/test_pipeline_english.py
"""English-only output must reject configuration, reference and vendor drift."""
import importlib.metadata
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from src_docs import english_search

ROOT = Path(__file__).resolve().parents[1]


class EnglishSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        policy = json.loads((ROOT / 'src_docs/md/assets/english-search-omissions.json').read_text())
        self.inventory = {'generated_vendor_assets': policy['omitted'] + policy['retained']}
        for row in self.inventory['generated_vendor_assets']:
            source = row['installed_distribution_sources'][0]
            data = importlib.metadata.distribution(source['distribution']).locate_file(source['path']).read_bytes()
            target = self.site / row['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (self.site / 'search').mkdir()
        self.index = {'config': {'lang': ['en']}, 'docs': [{'location': 'index.html', 'title': 'Glyph tools', 'text': 'Meaningful complete search fixture'}]}
        (self.site / 'search/search_index.json').write_text(json.dumps(self.index))
        (self.site / 'index.html').write_text('<html><script src="assets/javascripts/bundle.1a8646e9.min.js"></script></html>')
        self.config = {'theme': {'language': 'en'}, 'plugins': {'materialx/search': SimpleNamespace(config={'lang': ['en']})}, 'docs_dir': str(ROOT / 'src_docs/md'), 'site_dir': str(self.site)}

    def test_exact_english_payload_omits_only_all_34_unused_helpers(self):
        self.assertIs(english_search.on_config(self.config), self.config)
        before = {p.relative_to(self.site).as_posix(): p.read_bytes() for p in self.site.rglob('*') if p.is_file()}
        english_search.on_post_build(self.config)
        after = {p.relative_to(self.site).as_posix(): p.read_bytes() for p in self.site.rglob('*') if p.is_file()}
        removed = set(before) - set(after)
        self.assertEqual(len(removed), 34)
        self.assertEqual(removed, {row['path'] for row in self.inventory['generated_vendor_assets'] if '/lunr/' in row['path']})
        self.assertEqual(after, {name: data for name, data in before.items() if name not in removed})

    def test_non_english_theme_or_search_configuration_is_rejected(self):
        for languages, theme in [(['fr'], 'en'), (['en', 'fr'], 'en'), (['en'], 'fr'), ([], 'en')]:
            with self.subTest(languages=languages, theme=theme):
                self.config['plugins']['materialx/search'].config['lang'] = languages
                self.config['theme']['language'] = theme
                with self.assertRaisesRegex(ValueError, 'English'):
                    english_search.on_config(self.config)

    def test_search_index_language_drift_is_rejected(self):
        self.index['config']['lang'] = ['ja']
        (self.site / 'search/search_index.json').write_text(json.dumps(self.index))
        with self.assertRaisesRegex(ValueError, 'search index'):
            english_search.on_post_build(self.config)

    def test_empty_search_corpus_is_rejected(self):
        self.index['docs'] = []
        (self.site / 'search/search_index.json').write_text(json.dumps(self.index))
        with self.assertRaisesRegex(ValueError, 'search index'):
            english_search.on_post_build(self.config)

    def test_changed_helper_or_retained_vendor_bytes_are_rejected_before_deletion(self):
        for path in ['assets/javascripts/lunr/wordcut.js', 'assets/javascripts/bundle.1a8646e9.min.js']:
            with self.subTest(path=path):
                target = self.site / path
                before = target.read_bytes()
                target.write_bytes(before + b'changed')
                with self.assertRaisesRegex(ValueError, 'hash'):
                    english_search.on_post_build(self.config)
                self.assertTrue((self.site / 'assets/javascripts/lunr/wordcut.js').is_file())
                target.write_bytes(before)

    def test_missing_helper_is_rejected_before_deletion(self):
        (self.site / 'assets/javascripts/lunr/wordcut.js').unlink()
        with self.assertRaisesRegex(ValueError, 'asset set'):
            english_search.on_post_build(self.config)
        self.assertTrue((self.site / 'assets/javascripts/lunr/tinyseg.js').is_file())

    def test_unexpected_new_browser_asset_is_rejected(self):
        (self.site / 'assets/javascripts/lunr/unreviewed.js').write_text('new dependency')
        with self.assertRaisesRegex(ValueError, 'asset set'):
            english_search.on_post_build(self.config)

    def test_internal_html_helper_reference_is_rejected_even_when_encoded(self):
        (self.site / 'index.html').write_text('<script src="assets/javascripts/%6cunr/wordcut.js"></script>')
        with self.assertRaisesRegex(ValueError, 'reference'):
            english_search.on_post_build(self.config)
        self.assertTrue((self.site / 'assets/javascripts/lunr/wordcut.js').is_file())

    def test_external_source_notice_link_does_not_load_a_local_helper(self):
        (self.site / 'index.html').write_text('<a href="https://registry.npmjs.org/lunr-languages/-/lunr-languages-1.14.0.tgz">Original source</a><a href="assets/current-frontend/lunr/LICENSE.txt">Lunr notice</a>')
        english_search.on_post_build(self.config)
        self.assertFalse((self.site / 'assets/javascripts/lunr/wordcut.js').exists())

    def test_real_properdocs_materialx_configuration_uses_the_expected_search_plugin(self):
        import properdocs.replacement
        from properdocs.config import load_config
        config = load_config(str(ROOT / 'src_docs/mkdocs.yml'))
        self.assertIs(english_search.on_config(config), config)
        self.assertEqual(config['plugins']['materialx/search'].config['lang'], ['en'])

    def test_manifest_count_or_helper_boundary_drift_is_rejected(self):
        policy = json.loads((ROOT / 'src_docs/md/assets/english-search-omissions.json').read_text())
        policy['omitted'].pop()
        with self.assertRaisesRegex(ValueError, 'manifest'):
            english_search.verify_assets(self.site, policy)
        policy = json.loads((ROOT / 'src_docs/md/assets/english-search-omissions.json').read_text())
        policy['omitted'][0], policy['retained'][0] = policy['retained'][0], policy['omitted'][0]
        with self.assertRaisesRegex(ValueError, 'boundary'):
            english_search.verify_assets(self.site, policy)
