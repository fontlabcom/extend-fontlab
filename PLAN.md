---
this_file: PLAN.md
---

# extend-fontlab: remaining plan

The website catalogue for FontLab extensions, scripts, plugins and templates.

1. Retain THEME.md ownership rules and verify generated desktop/mobile routes, search and downloads before publication.
2. Compare public paths and downloadable asset hashes after any rebuild; record deployment and actual live verification separately.

Python 3.12+ and uv are required. The project pins ProperDocs 1.6.7 and MaterialX 10.1.5. A separately authorized isolated build uses `bash build.sh`; it writes docs/ and docs/.nojekyll. This is a build, not a runtime test or proof of a live site. No automated test suite is established.

Keep shared browser behavior in the shared theme project. Preserve existing downloads, public URLs, licence terms and authorship. Never hand-edit generated CSS as the source fix.

Keep implementation, offline verification, native acceptance and delivery as
separate milestones. Record verified scope in CHANGELOG and current checks in WORK.
