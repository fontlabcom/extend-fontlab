# this_file: src_docs/english_search.py
"""Omit only the hash-bound unused language helpers from English documentation."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


def on_config(config):
    """Fail before building if either search or presentation stops being English."""
    if config['theme']['language'] != 'en' or config['plugins']['materialx/search'].config['lang'] != ['en']:
        raise ValueError('English-only asset policy requires English theme and search')
    return config


def verify_assets(site: Path, policy: dict) -> None:
    """Bind both the omitted and retained payload before removing any files."""
    if len(policy['omitted']) != 34 or len(policy['retained']) != 9:
        raise ValueError('English omission manifest must bind 34 helpers and 9 core assets')
    if any('/lunr/' not in row['path'] for row in policy['omitted']) or any('/lunr/' in row['path'] for row in policy['retained']):
        raise ValueError('English omission manifest changed its helper boundary')
    rows = policy['omitted'] + policy['retained']
    expected = {row['path'] for row in rows}
    actual = {p.relative_to(site).as_posix() for folder in ('assets/javascripts', 'assets/images')
              for p in (site / folder).rglob('*') if p.is_file()}
    actual.update(p.relative_to(site).as_posix() for p in (site / 'assets/stylesheets').glob('*') if p.is_file())
    if actual != expected:
        raise ValueError('Generated vendor asset set changed; review before omission')
    for row in rows:
        if hashlib.sha256((site / row['path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Generated vendor hash changed: ' + row['path'])


def on_post_build(config) -> None:
    """Require current corpus/configuration and references, then omit exact helpers."""
    on_config(config)
    site = Path(config['site_dir'])
    policy = json.loads((Path(config['docs_dir']) / 'assets/english-search-omissions.json').read_text())
    verify_assets(site, policy)
    search = json.loads((site / 'search/search_index.json').read_text())
    if search['config']['lang'] != ['en'] or not search['docs']:
        raise ValueError('English nonempty search index required before omission')
    for page in site.rglob('*.html'):
        for reference in re.findall(r"(?:src|href)=[\"']([^\"']+)[\"']", page.read_text()):
            url = urlsplit(reference)
            if not url.scheme and not url.netloc and '/assets/javascripts/lunr/' in '/' + unquote(url.path):
                raise ValueError('HTML reference to omitted language helper: ' + reference)
    for row in policy['omitted']:
        (site / row['path']).unlink()
