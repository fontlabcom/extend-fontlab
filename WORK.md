---
this_file: WORK.md
---

## 2026-11-05 — approved documentation applied

Task 3 received independent SPEC PASS / QUALITY APPROVED review. Its 52 guides
were applied on 2026-11-05 at 12:48 UTC. The review and application receipts are
`verification/issue-230/task-3-review.md` and `task-3-apply.json` in the workspace.
Both receipts retain their original identities. The application preserved all 21
repository heads, branches, indexes and non-selected diffs.

This entry corrects the current documentation state. The proposal statements below
record the earlier authoring stage. Issue 230 has no milestone commit or push.
Integration, product/native acceptance, installation and publication remain separate.

## 2026-11-05 — Issue 230 documentation proposal

Inspected the six guide slots and current layout/configuration. Python 3.12+ and uv are required. The project pins ProperDocs 1.6.7 and MaterialX 10.1.5. A separately authorized isolated build uses `bash build.sh`; it writes docs/ and docs/.nojekyll. This is a build, not a runtime test or proof of a live site. No automated test suite is established.

Keep shared browser behavior in the shared theme project. Preserve existing downloads, public URLs, licence terms and authorship. Never hand-edit generated CSS as the source fix.

No runtime suite, native action, installation, Git change or publication was run
for this documentation pass. Review and canonical application are still pending.

# Work

## 2026-09-23: task422

Migrating Jekyll sources to ProperDocs + MaterialX and the shared fltheme26
assets. Original Markdown and public assets copied to src_docs/md before any
build replaces docs/. URLs and downloads must be verified before deployment.
Git objects recovered with git fetch --refetch; no working content discarded.

## Verification

ProperDocs build succeeded on 2026-09-23. SHA-256 comparison verified all 2
original font/image assets in both src_docs/md and built docs. Chromium checked
desktop/mobile rendering, no horizontal overflow, images and download targets.
GetGo's editable GG Pixa specimen and search passed. Extend's TypeRig screenshot
carousel passed. build.sh writes docs/.nojekyll after a successful build.
Deployment/live verification is tracked by fontlab-www-docstheme/consumers.json.
