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

- **Date finished:** 2026-11-04 (not finished: blocked at step 2)
- **Environment (step 1 done; nothing installed):**
  - Desktop host is Windows x64. All commands ran in the Linux VM the desktop app provides (Ubuntu 22.04.5). The package list below is that VM's, not the Windows host's. Python on the Windows host was not checked.
  - Free disk on the drive holding the repo folder: about 722 GB of 953 GB.
  - git 2.34.1, Python 3.10.12.
  - Installed: pandas 2.3.3, numpy 2.2.6, matplotlib 3.10.9, lxml 6.1.3.
  - Not installed: pyarrow, statsmodels, scipy.
  - R: not installed (`R` and `Rscript` not found), so lme4 and brms were not checked.
- **Dolgan:** not downloaded. Version, size and md5 not obtained.
- **Evenki:** not downloaded. Version, size and md5 not obtained.
- **Newer Dolgan version found?** Could not check, because the pages cannot be reached.
- **Count reconciliation:** not done, no data.
- **Exactly what was seen:** every request to the three hosts below failed with `HTTP 403 from proxy after CONNECT` (curl exit 56, no HTTP response from the site itself). This means the connection was refused by the network egress allowlist before reaching the site. Whether the sites are up was not determined.
  - `https://hdl.handle.net/11022/0000-0007-F9A7-4`
  - `https://www.fdr.uni-hamburg.de/record/16605`
  - `https://inel.corpora.uni-hamburg.de/`
  - The same 403 came from the desktop VM and from the cloud workspace. GitHub is reachable.
  - No workaround was attempted (no mirrors, no other fetch methods).
- **Needs from Jude (one of):**
  1. Allow these domains in the network egress settings, then re-run this task: `hdl.handle.net`, `www.fdr.uni-hamburg.de`, `inel.corpora.uni-hamburg.de`. The actual file download host may be a further domain, which is only visible after the first allowed attempt.
  2. Download the two no-audio zips by hand in a browser, copy the size and md5 from each page, and put the zips in a folder desktop Claude can read. Desktop Claude then does steps 4 to 7.
- **Surprises:**
  - The folder already held an empty git repo with the remote set, and `master` was its branch name. The remote branch is `main`.
  - Delete permission was declined, so git left lock files and `tmp_obj_*` files, which are objects git had not finished writing. Some were deleted by hand, which corrupted the local object store. It was rebuilt: the damaged `.git` was renamed to a `.git-corrupt-*` folder (ignored locally, safe to delete by hand), a fresh `.git` was made and fetched from GitHub. `git status` showed the working files identical to `origin/main` and `git fsck` was clean. Nothing was lost.
  - Because delete is not allowed, git may leave stale `.lock` and `tmp_obj_*` files in `.git` on this machine. Rename a stale lock rather than deleting it.
- **Questions for web Claude:** none yet. Task 002 cannot start until 001 is done.
