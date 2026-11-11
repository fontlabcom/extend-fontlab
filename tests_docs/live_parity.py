# this_file: tests_docs/live_parity.py
"""Compare deployed public routes and download bytes with committed bytes.

Used by tests_docs/test_live_parity.py. `compare_live` takes an injected
fetcher, so tests run offline; `url_fetch` is the stdlib live fetcher (plain
GET, generic User-Agent, no cookies or credentials, one retry at most).
Differences are reported as findings; nothing is rewritten to match.
"""
import hashlib
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

DOWNLOADS = {
    'download/fontlab-8/fixes/fix_fontlab_8_for_macos_10_13.vfpy':
        'https://cdn.jsdelivr.net/gh/fontlabcom/extend-fontlab/download/fontlab-8/fixes/fix_fontlab_8_for_macos_10_13.vfpy',
}
USER_AGENT = 'Mozilla/5.0 (compatible; site-parity-check)'
TIMEOUT_S = 20
ATTEMPTS = 2
NOT_ROUTES = {'404.html'}


def url_fetch(url):
    """GET an https URL; return (status, body). HTTP errors return their status."""
    if not url.startswith('https://'):
        raise ValueError(f'refusing non-https URL: {url}')
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    for attempt in range(ATTEMPTS):
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as error:
            return error.code, error.read()
        except OSError:
            if attempt == ATTEMPTS - 1:
                raise
            time.sleep(2)


def check(name, url, expected_bytes, fetch):
    """Fetch one URL and compare its sha256 with the committed bytes."""
    row = {'path': name, 'url': url, 'status': None, 'expected': hashlib.sha256(expected_bytes).hexdigest()}
    try:
        row['status'], body = fetch(url)
    except OSError as error:
        row.update(error=str(error), match=False)
        return row, f'{name}: fetch failed: {error}'
    row['actual'] = hashlib.sha256(body).hexdigest()
    row['match'] = row['status'] == 200 and row['actual'] == row['expected']
    if row['status'] != 200:
        return row, f'{name}: HTTP {row["status"]}'
    if not row['match']:
        return row, f'{name}: sha256 {row["actual"]} != committed {row["expected"]}'
    return row, None


def compare_live(fetch, root, pages, downloads, site_url):
    """Return {'checked_utc', 'results', 'findings'} for pinned pages and downloads."""
    root = Path(root)
    docs = root / 'docs'
    results, findings = [], []
    targets = [(route, site_url + route.removesuffix('index.html'), docs / route) for route in pages]
    targets += [(path, url, root / path) for path, url in downloads.items()]
    for name, url, local in targets:
        row, finding = check(name, url, local.read_bytes(), fetch)
        results.append(row)
        if finding:
            findings.append(finding)
    generated = sorted(p.relative_to(docs).as_posix() for p in docs.rglob('*.html'))
    findings += [f'{route}: generated route is not pinned' for route in generated if route not in pages and route not in NOT_ROUTES]
    checked = datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    return {'checked_utc': checked, 'results': results, 'findings': findings}
