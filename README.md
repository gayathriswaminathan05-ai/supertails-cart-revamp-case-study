# Supertails cart revamp — case study

A product design case study on revamping the Supertails app cart: grouping products by delivery, making savings and prescription checks legible, and showing the next valid checkout action for each shopper state.

- `index.html` — the case study
- `process.html` — appendix: proto-personas, competitive learnings, validation plan and draft explorations

## Structure

- `source/` — the canvas exports each page is built from
- `images/` — screens, crops and photos used by the pages
- `tools/build.py` — rebuilds `index.html` and `process.html` from `source/`

## Updating

Replace the files in `source/` with fresh exports (add any new images to `images/` as `<id>.jpg`), then:

```sh
python3 tools/build.py
```

The site is static and deploys from the repository root on `main` with GitHub Pages.

## Notes

Prices and savings in the screens are mock design content. Lifestyle photos are AI-generated.
