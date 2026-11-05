# 001: Environment check and corpus download

- **From:** web Claude
- **To:** desktop Claude
- **Status:** todo
- **Created:** 2026-11-04
- **Depends on:** none

## Goal
Get both corpora onto Jude's computer, verified and untouched, and record exactly which versions we have. Web Claude cannot download from the web, so nothing else can start until this is done.

## Steps
1. **Environment check.** Report:
   - OS and free disk space
   - `git --version`, `python3 --version`
   - which of these Python packages are installed: pandas, pyarrow, statsmodels, scipy, numpy, matplotlib, lxml
   - whether R is installed (`R --version`) and, if so, whether `lme4` and `brms` are installed
   - Do **not** install anything yet. Just report.
2. **Find the Dolgan corpus.** Start from the handle `https://hdl.handle.net/11022/0000-0007-F9A7-4` (INEL Dolgan Corpus 2.0, published 2022-11-30) or from `https://inel.corpora.uni-hamburg.de/`. Confirm that it is version 2.0, and check whether a newer version exists. Download the **no-audio** package (transcripts only; the file name should contain `noaudio`). Note the size and the md5 shown on the page.
3. **Find the Evenki corpus.** `https://www.fdr.uni-hamburg.de/record/16605` (INEL Evenki Corpus 2.0, DOI `10.25592/uhhfdm.16605`, published 2024-12-31). Download the no-audio package. Note size and md5.
4. **Verify checksums.** Compute md5 of each downloaded file and compare with the page. If they differ, stop and set Status to `blocked`.
5. **Unzip** into `data/raw/dolgan-2.0/` and `data/raw/evenki-2.0/`. Do not modify, rename or delete anything inside. These folders are git-ignored.
6. **Write `data/MANIFEST.json`** (this file is committed). One entry per corpus with: `corpus`, `version`, `doi_or_handle`, `source_url`, `download_date`, `package_filename`, `size_bytes`, `md5`, `licence`, `citation`. Take the licence and the citation string from the repository page or the documentation PDF. Do not write them from memory.
7. **Count files.** For each corpus, report the number of `.exb`, `.exs` and `.coma` files, and for Dolgan the number of communication folders per genre folder (`conv`, `flk`, `misc`, `nar`, `sng`, `transl`).

## Expected outputs
- `data/raw/dolgan-2.0/`, `data/raw/evenki-2.0/` (local only)
- `data/MANIFEST.json` (committed)
- Results section below (committed)

## Acceptance checks
- [ ] Both md5 values match the repository pages.
- [ ] `git status` shows no corpus files staged. Only `data/MANIFEST.json` and this task file changed.
- [ ] The Dolgan package's communication count is reported next to the documentation's figure: 136 glossed transcripts. Any difference is stated.
- [ ] The Evenki count is reported next to the website's figure: 612 texts. Any difference is stated.

## How to report
Fill in Results below. Then update the table in `handoff/README.md` and `PLAN.md`, commit and push.

---

## Results
*(desktop Claude fills in)*

- **Date finished:**
- **Environment:**
- **Dolgan:** version, source URL, size, md5, file counts
- **Evenki:** version, source URL, size, md5, file counts
- **Newer Dolgan version found?**
- **Count reconciliation:**
- **Surprises:**
- **Questions for web Claude:**
