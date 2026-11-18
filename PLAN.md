---
this_file: PLAN.md
---

# extend-fontlab: remaining plan

> HELD (owner, 2026-11-12; root TODO.md owner-hold row): do not edit extend-fontlab or extend.fontlab.com until the owner lifts this. Rows below are not actionable now. Annotated 2026-11-17 (issue 258).

## Functional work order — 2026-11-14

Prioritize useful catalogue navigation, search and downloads while preserving existing URLs and shared-theme ownership. Keep package names and download targets consistent with their maintained providers; retain the unresolved Cloudflare live-byte decision.

[Test-infrastructure guidance; deprioritised by the owner functional-first rule 2026-11-15] Use small smoke checks and focused regressions for changed behavior and package boundaries. Keep the existing detailed acceptance tasks for a later testing pass; mandatory delivery hooks and current holds remain in force.

The website catalogue for FontLab extensions, scripts, plugins and templates.

1. Retain THEME.md ownership rules and verify generated desktop/mobile routes, search and downloads before publication.
2. [HELD, owner hold 2026-11-12] Resolve the Cloudflare rewriting of live pages (Rocket Loader, Web Analytics beacon) or accept it, then rerun the live parity check (`EXTEND_FONTLAB_LIVE=1`, `tests_docs/test_live_parity.py`) after each rebuild; record deployment and live verification separately.

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
