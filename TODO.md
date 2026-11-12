---
this_file: TODO.md
---

# extend-fontlab: pending work

- [ ] Retain THEME.md ownership rules and verify generated desktop/mobile routes, search and downloads before publication.
- [ ] Live page bytes differ from docs/: Cloudflare Rocket Loader and the Web Analytics beacon rewrite all 5 pages (download matches). Decide whether to turn both off for extend.fontlab.com or accept the injection, then rerun `EXTEND_FONTLAB_LIVE=1` `tests_docs/test_live_parity.py` to zero findings after each rebuild.

- [ ] Verify actual remote main and both exact-source CI jobs, source epoch, generated lineage/parity, the applicable conditional Pages request and deployed/live bytes.

- [ ] Optional: add an Apache-2.0 `license` field to pyproject metadata if one is introduced (LICENSE is already Apache text; licence inventory).
