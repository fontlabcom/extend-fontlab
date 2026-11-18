---
this_file: AGENTS.md
---

# extend-fontlab: agent guide

## Owner priority: functional progress first (2026-11-15)

Future agents must make large, swift advances in working functionality. Prioritize visible user problems and useful, coherent feature increments. This instruction sets the work order and supersedes older requirements to complete exhaustive testing or build test infrastructure before ordinary implementation.

Keep packages coherent and compatible. Check shared APIs, imports and lazy aliases, data formats, dependency direction, object ownership and lifetime, installers, launchers and examples. Update affected providers and consumers together; preserve existing supported behavior and avoid dependency cycles.

During implementation, use the smallest meaningful smoke checks and focused regression tests for the changed behavior and affected package boundaries. Detailed testing, exhaustive coverage, broad performance studies and full acceptance matrices can follow in a later testing pass. Do not let test harnesses, sandbox/supervisor design, repeated unchanged suites, evidence machinery or review paperwork become the main project. Build such infrastructure only when a concrete functional defect or necessary safety constraint requires it.

Record deferred checks and known limits plainly. Do not call untested native, installed or published behavior verified. Keep existing mandatory delivery hooks, preservation rules, licence/privacy obligations, repository exclusions and explicit native/publication holds intact. When one action is held, continue other authorized functional work instead of expanding unrelated infrastructure.

Choose the next substantial useful feature or shared fix and carry its affected providers and consumers together. Timebox supporting investigation; once focused checks establish a usable increment, continue functionality work. Queue detailed testing for a later pass with its concrete remaining checks instead of letting test infrastructure displace product delivery.

## Live font testing in FontLab (owner instruction, 2026-11-10)

Test, verify and edit in the font that is open in FontLab 9. Don't hold back
because the owner might be working on it. Just work in it. If no font is open,
open a VFJ from `~/Desktop` first (File > Open, or `fontlab.flPackage(path)`
and `flWorkspace.instance().addPackage`). Those VFJs are for agents. Add glyphs,
kerning pairs, elements, contours, masters or anything else the test needs,
and save the files when that helps. This replaces older rules that required an
empty FontLab session or forbade editing open fonts. `fl-native.sh --mutating`
now runs with fonts open (`FL_REQUIRE_EMPTY=1` restores the old check). The
serialized lock still applies: one native run at a time. Don't quit or restart
FontLab, and don't close fonts from Python, because that has crashed the host.

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

## Agent workflow (Issue 250, 2026-11-10)

- Plan with `superpowers:subagent-driven-development`: one fresh implementer per task, a separate read-only reviewer, then the controller runs the gates and commits.
- Send bulk, well-specified work to Codex via the `codex-delegate` skill (`node ~/.agents/skills/codex-delegate/scripts/relay.mjs --brief BRIEF --cd WORKTREE`, in the background). Use `claude-delegate` or `cursor-delegate` for second opinions or independent lanes. Delegates never commit, push or tag.
- Work in a fresh worktree of `origin/main` on the workspace data volume; never pull, switch or reset the owner checkout. Merge `origin/main` again before pushing, keep both sides' CHANGELOG/PLAN/TODO entries, rerun the full suite, lint and graph change analysis, push through the pre-push hook where one is installed (never force), verify the remote SHA and the CI run where a workflow is configured. Held private Pages operations (workspace D41) stay held.
- Release: tag the next semver above the latest tag and publish a GitHub release. Install released, gated packages into `~/Library/Application Support/FontLab/FontLab 9/` and test live in FontLab 9. This owner route (Issue 250) supersedes, for released packages only, every older line in this guide that forbids installing into the FontLab user folder or its site-packages, owner-managed editable installs, or starting FontLab for a live test (the owner's canonical editable checkouts themselves stay owner-managed): record the previous installed distribution first so it can be restored, and never touch FontLab preferences (owner fonts and documents: see live font editing below); native work goes through the workspace `verification/issue-104/fl-native.sh` gate.
- Documents: CHANGELOG holds verified completed work; TODO only open or to-verify items; PLAN the major remaining changes; WORK.md the current round only (older WORK bytes are archived on the owner's workspace data volume, not public).
- Native defects: issues at github.com/fontlab/fl; fixes as pull requests to fontlab/Proteus, fontlab/FontGate or fontlab/pyfontgate. Never commit to the local C++ snapshot.
- Older "work directly" or "no delegation" lines in this guide are superseded by this section (Issue 250).
- Live font editing (owner, 2026-11-10; workspace D44): test, verify and edit the font open in FontLab 9, and do not stop because the owner might be working in it. Open a VFJ from `~/Desktop` first (those files are for agents), then add glyphs, kerning pairs, elements, contours, masters or whatever the test needs, and save them freely. This supersedes, for live testing, every older line here that forbids mutating owner fonts or documents or requires owned fixtures only. FontLab preferences, Output folders and global update queues stay untouched. Keep the serialized host lock (`fl-native.sh`, one native run at a time; `--mutating` now allows open fonts); do not quit or restart FontLab and do not close fonts from Python, which has crashed the host.
