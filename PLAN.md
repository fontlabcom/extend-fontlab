---
this_file: PLAN.md
---

# extend-fontlab: remaining plan

The website catalogue for FontLab extensions, scripts, plugins and templates.

1. Retain THEME.md ownership rules and verify generated desktop/mobile routes, search and downloads before publication.
2. Compare public paths and downloadable asset hashes after any rebuild; record deployment and actual live verification separately.

Python 3.12+ and uv are required. The project pins ProperDocs 1.6.7 and MaterialX 10.1.5. A separately authorized isolated build uses `bash build.sh`; it writes docs/ and docs/.nojekyll. This is a build, not a runtime test or proof of a live site. The docs boundary suite runs with `uv run python -B -m unittest discover -s tests_docs -v`.

Keep shared browser behavior in the shared theme project. Preserve existing downloads, public URLs, licence terms and authorship. Never hand-edit generated CSS as the source fix.

Keep implementation, offline verification, native acceptance and delivery as
separate milestones. Record verified scope in CHANGELOG and current checks in WORK.

3. Qualify remaining strict public entity-byte/not-found scope while preserving
   the recorded Cloudflare failure, consent continuation and unmet highlight-URL
   literals. Retain the independently accepted narrower canonical/light/focus/mobile
   observations; do not infer a source/provider cause or add a normalizer/security
   workaround. Keep all-site routes/search/download/live acceptance open. Deliver
   the factual Markdown successor through review, fresh graph/main guards and
   applicable normal CI, referencing the qualified code milestone rather than a
   recursive own-SHA note. For later affected publication retain source/output
   lineage/epoch/parity, the conditional Pages route and its latest-default race.
