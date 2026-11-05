# 001: Environment check and corpus download

- **From:** web Claude
- **To:** desktop Claude
- **Status:** done
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

- **Date finished:** 2026-11-05
- **Environment (step 1; nothing installed):**
  - Desktop host is Windows x64. All commands ran in the Linux VM the desktop app provides (Ubuntu 22.04.5). The package list below is that VM's, not the Windows host's. Python on the Windows host was not checked.
  - Free disk on the drive holding the repo folder: about 722 GB of 953 GB.
  - git 2.34.1, Python 3.10.12.
  - Installed: pandas 2.3.3, numpy 2.2.6, matplotlib 3.10.9, lxml 6.1.3.
  - Not installed: pyarrow, statsmodels, scipy.
  - R: not installed (`R` and `Rscript` not found), so lme4 and brms were not checked.
- **Dolgan:** INEL Dolgan Corpus **version 2.0**, published 2022-11-30. Source `https://www.fdr.uni-hamburg.de/record/11165` (handle `https://hdl.handle.net/11022/0000-0007-F9A7-4` redirects there). Package `dolgan-2.0-noaudio.zip`, 40,432,276 bytes (page: 40.4 MB), md5 `6f85f1a09811f07606caf6747744eef2`. **md5 matches the page.** Licence and citation are in `data/MANIFEST.json`, copied from the page.
- **Evenki:** INEL Evenki Corpus **version 2.0**, published 2024-12-31. Source `https://www.fdr.uni-hamburg.de/record/16605`. Package `evenki-2.0-lite.zip`, 61,537,332 bytes (page: 61.5 MB), md5 `395717280876078cd33d54382b9717e1`. **md5 matches the page.**
  - **Naming discrepancy:** the record has no package named `noaudio`. The files are `lite` (61.5 MB), `standard` (2.0 GB), `mp3` (1.0 GB) and the documentation PDF. The Evenki documentation PDF says: the "lite" package does not include any sound, video or PDF files; "standard" has WAV and PDF; "mp3" has MP3 and PDF. So `lite` is the transcripts-only package. I used it. Please confirm this is what you intended.
  - The Evenki documentation PDF itself was also downloaded (md5 `8c3472ec27035d8d56c70d50b57dc55d`, matches the page) and kept locally in `data/raw/docs/`. It is not committed.
- **Newer version found?** No. The Dolgan page's version list shows only 2.0 (2022-11-30) and 1.0 (2019-08-31). The Evenki page shows only 2.0 (2024-12-31) and 1.0 (2021-12-31). Checked 2026-11-05.
- **File counts (counted in the unzipped folders):**

| | `.exb` | `.exs` | `.coma` | other |
|---|---|---|---|---|
| Dolgan | 136 | 136 | 1 | 136 `_tei.xml`, 3 `.eaf`, 1 documentation PDF |
| Evenki | 612 | 612 | 1 | 614 `.xml`, 612 `.eaf`, 1 `coma-overview.html`, 1 documentation PDF |

  - Dolgan communication folders per genre folder (folders / `.exb` files): `conv` 17 / 17, `flk` 51 / 51, `misc` 1 / 1, `nar` 64 / 61, `sng` 2 / 2, `transl` 4 / 4. That is 139 folders and 136 `.exb`.
  - The 3 extra `nar` folders each contain only one `.eaf` file and no `.exb`. I did not look inside them (task 002 may). They are not counted as transcripts.
  - Evenki top-level folders (subfolders / `.exb`): `conv` 9 / 9, `flk` 198 / 198, `misc` 40 / 40, `nar` 347 / 347, `song` 18 / 18 (Dolgan calls its song folder `sng`, Evenki calls it `song`). Plus `corpus-utilities` and `documentation`, with no texts. That is 612 texts.
- **Count reconciliation:**
  - Dolgan: 136 `.exb` files against the documentation's 136 glossed transcripts. Same. (I counted files, not the contents of the files. Whether each `.exb` is a glossed transcript is for task 002.)
  - Evenki: 612 `.exb` files against the website's 612 texts. Same.
- **Where the files are (local only, git-ignored):** `data/raw/dolgan-2.0/`, `data/raw/evenki-2.0/`, the two zips in `data/raw/_packages/`, the Evenki documentation PDF in `data/raw/docs/`. The unzipped folders were compared file by file (md5 of every file) with a fresh extraction of each verified zip: no differences. `git status` shows only `data/MANIFEST.json` and the task, README and PLAN files as changes.
- **How the download worked (for next time):** the shell on this computer and the cloud workspace are refused by the network allowlist (HTTP 403 from the proxy for `hdl.handle.net`, `www.fdr.uni-hamburg.de`, `inel.corpora.uni-hamburg.de`). The desktop app's built-in browser can open those sites after the person approves them, and a file link opened there is saved into the connected repo folder. That is how both zips came in. Nothing else was used to get around the block.
- **Surprises:**
  - The Evenki record has no `noaudio` package (see above).
  - The three Dolgan `nar` folders with only a `.eaf`.
  - The repo folder already held an empty git repo with the remote set, and `master` was its branch name. The remote branch is `main`.
  - Delete permission was first declined, so git left lock files and `tmp_obj_*` files, which were objects git had not finished writing. Deleting them by hand corrupted the local object store. It was rebuilt by fetching from GitHub (`git fsck` clean, working files identical to `origin/main`). The damaged `.git` was renamed `.git-corrupt-*` (ignored locally).
  - Writing thousands of small files to the connected folder is slow, and an unzip straight into it timed out and left a partial copy. The fix was to extract on local disk and `rsync` into the folder. Worth knowing before task 002 writes many small outputs.
- **Questions for web Claude:** (1) The task and `docs/CORPUS_NOTES.md` say "no-audio package" for Evenki. The package is called `lite`. Please update the wording. (2) Do the 3 Dolgan `.eaf`-only folders matter for the 136-transcript count?
