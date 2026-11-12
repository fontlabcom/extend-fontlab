---
this_file: WORK.md
---

# Work in progress (2026-11-12, D46 status note)

- State: main `a42086e`; Documentation CI success on `564df25`, pages deployment success on `a42086e`. Live parity check (`c1519e5`, https-only redirects `95869b7`) is on main.
- Open: decide Cloudflare Rocket Loader / Web Analytics for extend.fontlab.com, then rerun the live parity check (TODO).
- Earlier WORK.md (1,546 bytes, SHA256 `1603205a36023b0ac4c47b54ab0ecf3f3c537dbb30b7e0a7b39bdc9d4686df72`) is archived on the owner's workspace data volume (not public) under `issue250/review/d46-work-archive/`; the first archive is under `issue250/work-archives/`. The latest parity table follows unchanged.

## Live parity check, 2026-11-11T22:44:16Z (source main 4cb4e46, docs from edbedd8)

`tests_docs/live_parity.py` fetched the 5 pinned routes and the jsDelivr download with plain GETs (generic User-Agent, no cookies, 20 s timeout, one retry). The site does not expose a deployed commit SHA.

| Path | HTTP | sha256 live | sha256 committed | Match |
| --- | --- | --- | --- | --- |
| index.html | 200 | ac0b6010… | cd27f2fe… | no |
| scripts/index.html | 200 | 8a777cf8… | 89207ca1… | no |
| typerig/index.html | 200 | c4b22da7… | a28bdca5… | no |
| varia/fixes/index.html | 200 | 149bfff2… | 02ecdb1c… | no |
| frontend-notices/index.html | 200 | f8a93ebc… | 4dfec4ee… | no |
| download/fontlab-8/fixes/fix_fontlab_8_for_macos_10_13.vfpy | 200 | 1b473e7e… | 1b473e7e… | yes |

Finding: Cloudflare in front of GitHub Pages rewrites every page. Rocket Loader adds a `type="<id>-text/javascript"` attribute to each script and appends `rocket-loader.min.js`; Web Analytics appends the `beacon.min.js` script. Removing exactly those changes gives the committed bytes for varia/fixes (checked by hand; the repository has no normalizer). docs/ was not changed. Live parity stays open in TODO.md.
