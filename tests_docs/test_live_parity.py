# this_file: tests_docs/test_live_parity.py
"""Compare the deployed site and public download with the committed bytes.

The synthetic tests inject a fake fetcher and never touch the network. The
live check runs only when EXTEND_FONTLAB_LIVE=1; record its output in WORK.md
as a separate deployment record (TODO.md row on public paths and hashes).
"""
import email.message
import hashlib
import io
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

import live_parity
from live_parity import DOWNLOADS, compare_live, url_fetch

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index.html', 'scripts/index.html', 'typerig/index.html', 'varia/fixes/index.html', 'frontend-notices/index.html']
SITE_URL = 'https://extend.fontlab.com/'


def sha(data):
    return hashlib.sha256(data).hexdigest()


class FakeFetch:
    """Serve URL -> (status, bytes); unknown URLs return 404."""

    def __init__(self, table):
        self.table = table
        self.calls = []

    def __call__(self, url):
        self.calls.append(url)
        return self.table.get(url, (404, b''))


class Fixture:
    def __init__(self, tmp):
        self.root = Path(tmp)
        self.docs = self.root / 'docs'
        self.pages = ['index.html', 'a/index.html']
        for route in self.pages + ['404.html']:
            path = self.docs / route
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(f'<p>{route}</p>'.encode())
        self.asset = self.root / 'download/x.vfpy'
        self.asset.parent.mkdir(parents=True)
        self.asset.write_bytes(b'payload')
        self.downloads = {'download/x.vfpy': 'https://cdn.example/x.vfpy'}

    def table(self):
        table = {SITE_URL + route.removesuffix('index.html'): (200, (self.docs / route).read_bytes()) for route in self.pages}
        table['https://cdn.example/x.vfpy'] = (200, b'payload')
        return table

    def run(self, fetch):
        return compare_live(fetch, self.root, self.pages, self.downloads, SITE_URL)


class LiveParityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.fx = Fixture(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_compare_live_when_all_bytes_match_then_no_findings(self):
        fetch = FakeFetch(self.fx.table())
        report = self.fx.run(fetch)
        self.assertEqual(report['findings'], [], report)
        self.assertEqual(len(report['results']), 3)
        self.assertEqual(len(fetch.calls), 3, 'exactly the pinned routes plus downloads are fetched')
        self.assertTrue(all(r['status'] == 200 and r['match'] for r in report['results']))
        self.assertRegex(report['checked_utc'], r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$')

    def test_compare_live_when_route_missing_then_status_finding(self):
        table = self.fx.table()
        del table[SITE_URL + 'a/']
        report = self.fx.run(FakeFetch(table))
        self.assertEqual(report['findings'], ['a/index.html: HTTP 404'])

    def test_compare_live_when_html_bytes_differ_then_hash_finding(self):
        table = self.fx.table()
        table[SITE_URL] = (200, b'<p>rewritten by proxy</p>')
        report = self.fx.run(FakeFetch(table))
        self.assertEqual(len(report['findings']), 1, report)
        self.assertTrue(report['findings'][0].startswith('index.html: sha256 '), report)
        row = report['results'][0]
        self.assertEqual(row['expected'], sha((self.fx.docs / 'index.html').read_bytes()))
        self.assertEqual(row['actual'], sha(b'<p>rewritten by proxy</p>'))

    def test_compare_live_when_download_hash_differs_then_finding(self):
        table = self.fx.table()
        table['https://cdn.example/x.vfpy'] = (200, b'stale')
        report = self.fx.run(FakeFetch(table))
        self.assertEqual(len(report['findings']), 1)
        self.assertTrue(report['findings'][0].startswith('download/x.vfpy: sha256 '))

    def test_compare_live_when_docs_has_unpinned_route_then_finding(self):
        extra = self.fx.docs / 'b/index.html'
        extra.parent.mkdir()
        extra.write_bytes(b'new')
        report = self.fx.run(FakeFetch(self.fx.table()))
        self.assertEqual(report['findings'], ['b/index.html: generated route is not pinned'])

    def test_compare_live_when_fetch_blocked_then_error_recorded(self):
        def blocked(url):
            raise OSError('HTTP Error 403: Forbidden')

        report = self.fx.run(blocked)
        self.assertEqual(len(report['findings']), 3)
        self.assertTrue(all(r['status'] is None and 'Forbidden' in r['error'] for r in report['results']))

    def test_url_fetch_when_scheme_not_https_then_rejected(self):
        with self.assertRaises(ValueError):
            url_fetch('file:///etc/hosts')

    def test_url_fetch_when_http_error_then_status_returned_without_retry(self):
        calls = []

        def raise_404(request, timeout):
            calls.append((request.full_url, request.get_header('User-agent'), timeout))
            raise urllib.error.HTTPError(request.full_url, 404, 'Not Found', email.message.Message(), io.BytesIO(b'gone'))

        with mock.patch.object(live_parity.urllib.request, 'urlopen', raise_404):
            self.assertEqual(url_fetch('https://example.invalid/a/'), (404, b'gone'))
        self.assertEqual(calls, [('https://example.invalid/a/', live_parity.USER_AGENT, live_parity.TIMEOUT_S)])

    def test_url_fetch_when_connection_fails_twice_then_raises_after_one_retry(self):
        calls = []

        def refuse(request, timeout):
            calls.append(request.full_url)
            raise urllib.error.URLError('refused')

        with mock.patch.object(live_parity.urllib.request, 'urlopen', refuse), mock.patch.object(live_parity.time, 'sleep'), self.assertRaises(urllib.error.URLError):
            url_fetch('https://example.invalid/')
        self.assertEqual(len(calls), 2)

    def test_pinned_downloads_match_site_pages(self):
        self.assertEqual(sorted(DOWNLOADS), ['download/fontlab-8/fixes/fix_fontlab_8_for_macos_10_13.vfpy'])
        for path, url in DOWNLOADS.items():
            self.assertTrue((ROOT / path).is_file(), path)
            self.assertEqual(url, 'https://cdn.jsdelivr.net/gh/fontlabcom/extend-fontlab/' + path)
            self.assertIn(url, (ROOT / 'src_docs/md/varia/fixes.md').read_text())

    @unittest.skipUnless(os.environ.get('EXTEND_FONTLAB_LIVE') == '1', 'live check runs only with EXTEND_FONTLAB_LIVE=1')
    def test_live_site_when_enabled_then_matches_committed_bytes(self):
        report = compare_live(url_fetch, ROOT, PAGES, DOWNLOADS, SITE_URL)
        print(report)
        self.assertEqual(report['findings'], [], report)


if __name__ == '__main__':
    unittest.main()
