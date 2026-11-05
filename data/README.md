# data/

Local copies of the corpora live here. **Everything except `MANIFEST.json` and this file is git-ignored.**

```
data/
  MANIFEST.json        committed: corpus versions, DOIs/handles, download dates, file sizes, md5, licence, citation strings
  raw/
    dolgan-2.0/        unzipped INEL Dolgan Corpus (no-audio package), never edited
    evenki-2.0/        unzipped INEL Evenki Corpus (no-audio package), never edited
  derived/             tables built by shared/ (tokens, morphemes, speakers, ...), rebuildable
  audio/               optional: audio packages, only if needed for listening
```

Rules:
- `raw/` is read-only. If something looks wrong, record it in a QA report. Do not fix it in place.
- `derived/` can always be rebuilt from `raw/` plus the code at a given commit. Do not hand-edit it.
- Human work (annotations) lives in `annotations/`, not here.

`MANIFEST.json` is created by handoff task 001. Expected fields per corpus: `corpus`, `version`, `doi_or_handle`, `source_url`, `download_date`, `package_filename`, `size_bytes`, `md5`, `licence`, `citation`.
