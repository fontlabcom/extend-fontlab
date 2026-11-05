---
this_file: README.md
---

# extend-fontlab

The website catalogue for FontLab extensions, scripts, plugins and templates.

Edit Markdown in `src_docs/md/` and configuration in `src_docs/mkdocs.yml`. `docs/` is generated output; `download/` contains downloads. Read THEME.md for shared theme ownership.

## Development

Python 3.12+ and uv are required. The project pins ProperDocs 1.6.7 and MaterialX 10.1.5. A separately authorized isolated build uses `bash build.sh`; it writes docs/ and docs/.nojekyll. This is a build, not a runtime test or proof of a live site. No automated test suite is established.

Keep shared browser behavior in the shared theme project. Preserve existing downloads, public URLs, licence terms and authorship. Never hand-edit generated CSS as the source fix.

Use an isolated checkout. Read [AGENTS.md](AGENTS.md) for workflow and
[TODO.md](TODO.md) for pending work. The Issue 230 documentation reconciliation
does not establish a new runtime, native or release result.

## Existing usage and reference

# extend-fontlab
Extensions, scripts, plugins, templates for the FontLab font editor

## Build the website

Run `./build.sh` with uv installed. ProperDocs and MaterialX build the Markdown
in `src_docs/md/` into `docs/`, which GitHub Pages publishes. The shared theme
loads from `https://i.fontlab.com/fltheme26/1.0.0/`. Edit source files, then
rebuild; generated HTML in `docs/` is not the authoring source.

The migration preserves public page paths and downloadable assets. The
`fontlab-www-docstheme` sibling repository records source and output asset
hashes and browser verification.

<!-- shared-theme-integration:start -->
## Shared FontLab theme integration

This repository is part of the FontLab theme 2026 rollout: extension catalogue.
[THEME.md](THEME.md) documents its source/output boundaries, configuration,
publication route, control ownership, shared visual changes and verification.
Use the [public setup guide](https://i.fontlab.com/fltheme26/) and
[MaterialX starter](https://i.fontlab.com/fltheme26/starter.zip) for new sites.
<!-- shared-theme-integration:end -->
