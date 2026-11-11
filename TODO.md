---
this_file: TODO.md
---

# extend-fontlab: pending work

- [ ] Retain THEME.md ownership rules and verify generated desktop/mobile routes, search and downloads before publication.
- [ ] Live page bytes differ from docs/: Cloudflare Rocket Loader and the Web Analytics beacon rewrite all 5 pages (download matches). Decide whether to turn both off for extend.fontlab.com or accept the injection, then rerun `EXTEND_FONTLAB_LIVE=1` `tests_docs/test_live_parity.py` to zero findings after each rebuild.
- [ ] Make `tests_docs/live_parity.py` `url_fetch` refuse redirects that leave https (urllib follows an https→http redirect today) and add an offline test with a patched redirect.

- [ ] Verify actual remote main and both exact-source CI jobs, source epoch, generated lineage/parity, the applicable conditional Pages request and deployed/live bytes.
