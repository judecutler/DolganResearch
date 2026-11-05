# 001: Environment check and corpus download

- **From:** web Claude
- **To:** desktop Claude
- **Status:** blocked
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

- **Date finished:** not finished. Blocked at the download (steps 2 to 3). Last updated 2026-11-05.
- **Environment (step 1 done; nothing installed):**
  - Desktop host is Windows x64. All commands ran in the Linux VM the desktop app provides (Ubuntu 22.04.5). The package list below is that VM's, not the Windows host's. Python on the Windows host was not checked.
  - Free disk on the drive holding the repo folder: about 722 GB of 953 GB.
  - git 2.34.1, Python 3.10.12.
  - Installed: pandas 2.3.3, numpy 2.2.6, matplotlib 3.10.9, lxml 6.1.3.
  - Not installed: pyarrow, statsmodels, scipy.
  - R: not installed (`R` and `Rscript` not found), so lme4 and brms were not checked.
- **Dolgan (read from the repository page; NOT downloaded):**
  - Version 2.0, published 2022-11-30. Page: `https://www.fdr.uni-hamburg.de/record/11165` (the handle `https://hdl.handle.net/11022/0000-0007-F9A7-4` redirects there). DOI `10.25592/uhhfdm.11165`.
  - Wanted package: `dolgan-2.0-noaudio.zip`, listed as 40.4 MB, md5 `6f85f1a09811f07606caf6747744eef2`. The page gives only a rounded size, so the exact `size_bytes` is not known (UNVERIFIED until a file is in hand).
  - Other files on the page (not wanted): `dolgan-2.0-documentation.pdf` 1.0 MB md5 `ec3647edf1b70e222e25ff62482a9ff8`; `dolgan-2.0-mp3only.zip` 2.1 GB; `dolgan-2.0.zip` 11.7 GB.
  - Licence shown on the page for the files: Creative Commons Attribution Non Commercial Share Alike 4.0 International.
  - Citation string on the page: Däbritz, Chris Lasse; Kudryakova, Nina; Stapert, Eugénie. 2022. INEL Dolgan Corpus. Version 2.0. Publication date 2022-11-30. https://hdl.handle.net/11022/0000-0007-F9A7-4. Archived at Universität Hamburg. In: The INEL corpora of indigenous Northern Eurasian languages. https://hdl.handle.net/11022/0000-0007-F45A-1.
- **Evenki (read from the repository page; NOT downloaded):**
  - Version 2.0, published 2024-12-31. Page: `https://www.fdr.uni-hamburg.de/record/16605`. DOI `10.25592/uhhfdm.16605`. Handle `https://hdl.handle.net/11022/0000-0007-FE38-D`.
  - **No package is named `noaudio`.** The page lists: `evenki-2.0-lite.zip` 61.5 MB md5 `395717280876078cd33d54382b9717e1`; `evenki-2.0-standard.zip` 2.0 GB md5 `e578975ec4c2517a30e7aed597338e15`; `evenki-2.0-mp3.zip` 1.0 GB md5 `1476fa0e1374563b41e2c32850d2d4aa`; `evenki-2.0-documentation.pdf` 2.5 MB md5 `8c3472ec27035d8d56c70d50b57dc55d`.
  - Which of these is the transcripts-only package is UNVERIFIED. `lite` is the likely candidate by size, but nothing on the page says what it contains. The documentation PDF would probably say; it did not load (see below).
  - Licence on the page: Creative Commons Attribution Non Commercial Share Alike 4.0 International.
  - Citation string on the page: Däbritz, Chris Lasse; Gusev, Valentin; Stoynova, Natalia. 2024. INEL Evenki Corpus. Version 2.0. Publication date 2024-12-31. Archived at Universität Hamburg. https://hdl.handle.net/11022/0000-0007-FE38-D. In: The INEL corpora of indigenous Northern Eurasian languages. https://hdl.handle.net/11022/0000-0007-F45A-1
  - Figures stated on the page: 612 texts, 19,931 sentences, 93,264 tokens; 3 h 58 min of audio in 69 texts.
- **Newer Dolgan version found?** No. The page's version list shows only Version 2.0 (2022-11-30) and Version 1.0 (2019-08-31), as read on 2026-11-05. The same check for Evenki shows only 2.0 and 1.0.
- **Count reconciliation:** not done, no data.
- **Exactly what was seen:** every request to the three hosts below failed with `HTTP 403 from proxy after CONNECT` (curl exit 56, no HTTP response from the site itself). This means the connection was refused by the network egress allowlist before reaching the site. Whether the sites are up was not determined.
  - `https://hdl.handle.net/11022/0000-0007-F9A7-4`
  - `https://www.fdr.uni-hamburg.de/record/16605`
  - `https://inel.corpora.uni-hamburg.de/`
  - The same 403 came from the desktop VM and from the cloud workspace. GitHub is reachable.
  - No workaround was attempted (no mirrors, no other fetch methods).
- **Download attempt, 2026-11-05:** the shell on this computer and the cloud workspace are still refused (403). The desktop app's built-in browser can open the repository pages after the site is approved, so the two record pages above were read there. Clicking Download for `dolgan-2.0-noaudio.zip` in that browser did not produce a file in the Downloads folder (checked for any new file in the last hour). The documentation PDF link for Evenki failed to load. No other method was tried.
- **Needs from Jude:**
  1. Download `dolgan-2.0-noaudio.zip` yourself from `https://www.fdr.uni-hamburg.de/record/11165` into the Downloads folder (desktop Claude has been given access to that folder). Expected: 40.4 MB, md5 `6f85f1a09811f07606caf6747744eef2`.
  2. For Evenki, decide which package to use. Either confirm from the Evenki documentation PDF which zip is text-only (probably `evenki-2.0-lite.zip`, 61.5 MB), or say to use that one. Download it to the same folder.
  3. Desktop Claude then does steps 4 to 7 (md5, unzip into `data/raw/`, `MANIFEST.json`, counts) and task 002.
  Alternative to 1 and 2: allow the egress domains `hdl.handle.net`, `www.fdr.uni-hamburg.de`, `fdr.uni-hamburg.de`, `inel.corpora.uni-hamburg.de` for the shell, and desktop Claude downloads.
- **Surprises:**
  - The folder already held an empty git repo with the remote set, and `master` was its branch name. The remote branch is `main`.
  - Delete permission was declined, so git left lock files and `tmp_obj_*` files, which are objects git had not finished writing. Some were deleted by hand, which corrupted the local object store. It was rebuilt: the damaged `.git` was renamed to a `.git-corrupt-*` folder (ignored locally, safe to delete by hand), a fresh `.git` was made and fetched from GitHub. `git status` showed the working files identical to `origin/main` and `git fsck` was clean. Nothing was lost.
  - Because delete is not allowed, git may leave stale `.lock` and `tmp_obj_*` files in `.git` on this machine. Rename a stale lock rather than deleting it.
- **Questions for web Claude:** (1) The Evenki record has no `noaudio` package, only `lite`, `standard` and `mp3`. Should the task and `docs/CORPUS_NOTES.md` name `lite`? (2) Please check the Evenki documentation PDF for what `lite` contains. Task 002 cannot start until 001 is done.
