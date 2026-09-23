---
this_file: README.md
---
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
