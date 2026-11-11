---
this_file: WORK.md
---

# Work in progress

Earlier WORK.md (11,695 bytes, SHA256 `5019b2897329d626bcede07c39843511cf9c4ef5fe1c0a7571d0cfa4a4d2eff2`) is archived on the owner's workspace data volume (not public) under `issue250/work-archives/` (Issue 250). Completed work is in CHANGELOG.md; open work is in TODO.md and PLAN.md.

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
