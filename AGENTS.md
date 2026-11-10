---
this_file: AGENTS.md
---

# extend-fontlab: agent guide

The website catalogue for FontLab extensions, scripts, plugins and templates.

Edit Markdown in `src_docs/md/` and configuration in `src_docs/mkdocs.yml`. `docs/` is generated output; `download/` contains downloads. Read THEME.md for shared theme ownership.

## Workflow

Work in an isolated successor and preserve concurrent owner edits and branch state.
Read README, PLAN, TODO, WORK and CHANGELOG first. Choose one small useful MVP
milestone; inspect callers and imports before source changes and use graph impact
where indexed. Keep the exact applicable tests and the unchanged complete-module
80% coverage gate for changed production modules. Documentation-only changes need
links, fences, headers, privacy and diff checks, not a new product test run.

After independent review and the applicable checks, commit and push each milestone
and verify the remote result. Integrate qualified branches into main (or this
repository’s existing primary branch) without discarding owner work. Before deleting
obsolete branches, files or folders, prove recovery, current integration and absence
of unique or attached owner work. Update TODO and CHANGELOG with each milestone;
remove only scoped verified tasks and retain unmet native, delivery and release gates.
Issue 123 stays paused. Do not access owner fonts, preferences or the FontLab user
folder. Source tests, artifacts, native acceptance and publication are separate.

## Verification

Python 3.12+ and uv are required. The project pins ProperDocs 1.6.7 and MaterialX 10.1.5. A separately authorized isolated build uses `bash build.sh`; it writes docs/ and docs/.nojekyll. This is a build, not a runtime test or proof of a live site. The docs boundary suite runs with `uv run python -B -m unittest discover -s tests_docs -v`.

## Boundaries

Keep shared browser behavior in the shared theme project. Preserve existing downloads, public URLs, licence terms and authorship. Never hand-edit generated CSS as the source fix.

## Retained local guidance

Keep the project-specific rules and examples below. The current workflow and
verification limits above govern this documentation milestone.

<!-- this_file: AGENTS.md -->

# extend-fontlab: agent guidance

<!-- shared-theme-integration:start -->
## Shared theme maintenance

Read [THEME.md](THEME.md) before changing shared chrome, MaterialX configuration
or component assets. This repository’s role is: extension catalogue.
Shared browser behavior belongs in `fontlab-www-docstheme`; FontLab global menu
source belongs in `img/docs/menu/fontlab.js`, Vexy menu source in
`i.vexy.art/docs/menu/vexy.js`. Keep per-site content, branding and native builds here.
Preserve one menu and one search control, documented ownership defaults, scoped
`.fltheme-components` styles and `du-` component prefixes. Verify final generated
HTML after overlays; a source-only change is not proof of a live deployment.
Do not commit unrelated local edits or hand-edit generated CSS as the source fix.
Work directly unless the current user explicitly requests delegation.
<!-- shared-theme-integration:end -->

## Integration rounds

After each important round, independently verify the result, refresh the actual upstream main (or existing default branch), and reconcile concurrent team work in an isolated successor. Integrate qualified changes upstream through normal gates without force-pushing. Move only verified solved TODO items to cumulative CHANGELOG, update PLAN for remaining work, and continue the authorized backlog. Existing preservation rules, exclusions, pauses, native/install restrictions, private P/L holds and capability gates remain in force.
