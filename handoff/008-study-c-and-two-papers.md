# 008: Run Study C, and fetch two papers web Claude cannot open

- **From:** web Claude
- **To:** desktop Claude
- **Status:** done
- **Created:** 2026-11-06
- **Depends on:** 007 (run it first; this uses the `objects.csv` files that 007 regenerates)

## Goal
Study C is new (`case_change/STUDY_C_PLAN.md`, committed before this script existed). It tests, with counts, a claim that Sheifer and Bolshakova (2023) made only qualitatively. Dolgan is said to use the partitive for objects only in future, imperative, conditional and modal clauses, while Evenki's indefinite accusative is said not to depend on clause type. Two papers could show that someone has already counted this. Both block automated readers, so web Claude cannot open them.

You only run commands, download the two files and report. Do not edit `shared/` or `case_change/`.

## Steps
1. `git pull`. Run the tests: `python3 -m unittest discover -s shared/tests -t shared/tests`. Expect `OK` (all tests pass; 54 or more).
2. Run Study C in the background (a few minutes):
   `python3 case_change/clause_dom.py data/derived/dolgan/objects.csv data/derived/evenki/objects.csv reports/study_c_clause_dom.md > scratch/008_c.log 2>&1 &`
   Record the run time and exit code. Do not change the plan or rerun with other settings.
2b. Rebuild the coding sheets. Web Claude moved `speaker_id`, `birth_year` and `recording_year` out of the sheets into the key files, so coders cannot see them (D-039). Nobody has coded yet (006). Run:
   `python3 shared/workbook.py build pilot data/derived/workbooks data/derived/dolgan/evid_candidates.csv --n 40`
   `python3 shared/workbook.py build pilot data/derived/workbooks data/derived/dolgan/b1_candidates.csv --n 100000 --prefix b1 --codebook shared/config/b1_codebook.json`
   Check that the header row of `pilot_sheet_A.xlsx` and `b1_sheet_A.xlsx` has none of those three columns, and that `pilot_key.csv` and `b1_key.csv` do. If any yellow cell in the old sheets has a value, stop and ask Jude before overwriting.
3. In the built-in browser, download these two PDFs to `scratch/008/` (git-ignored):
   - Siegl, "Der Partitiv im Taimyr Dolganischen", *Journal de la Société Finno-Ougrienne*: https://journal.fi/susa/article/view/87180
   - The *Language Documentation and Description* article https://lddjournal.org/article/id/1188 (title unknown to web Claude).
   If one cannot be downloaded, say what you saw and go on.
4. For each PDF, run the excerpt tool. It needs `pdftotext`, which you used for Stapert.
   - Siegl: `python3 shared/pdf_excerpts.py scratch/008/<file>.pdf handoff/outputs/008/siegl_partitive.md --terms Imperativ Futur Konditional Ewenk Evenk Akkusativ Generation Alter jünger Belege Prozent Tabelle Korpus`
   - LDD: `python3 shared/pdf_excerpts.py scratch/008/<file>.pdf handoff/outputs/008/ldd_1188.md --terms partitive Dolgan object accusative Evenki corpus INEL imperative generation`
   Add the full reference (authors, year, title, journal, volume, pages) at the top of each output file, from the PDF's first page.
5. Privacy check `reports/study_c_clause_dom.md` as in 003, step 5. It should hold only counts and test results.
6. Commit `reports/study_c_clause_dom.md`, `handoff/outputs/008/`, this file and `PLAN.md` (one log line). Nothing under `data/` or `scratch/`.

## Results

- **Date finished:** 2026-11-06 (overnight)
- **Tests:** `Ran 59 tests ... OK`.
- **Study C (step 2):** 24 s, exit 0, run in the foreground (background jobs are killed on Jude's computer, see 007). Output is identical under `PYTHONHASHSEED` 1 and 2. Headline: Dolgan PART share irrealis 12.0% vs realis 0.3% (H1 +11.5 points, p < 0.001). Evenki ACC.INDF irrealis 22.3% vs realis 8.3% (H3 +14.1, p = 0.016). Dolgan minus Evenki difference H4 −2.2, p = 0.70. So in these data Evenki also depends on clause type. See also Siegl's citation of Kazama below.
- **Workbooks (step 2b):** all yellow cells in the old sheets were empty, so I rebuilt them. Pilot 40 items and B1 767 items, both double-coded. The `speaker_id`, `birth_year` and `recording_year` columns are absent from all four sheets and present in `pilot_key.csv` and `b1_key.csv`. Locked columns are grey (`E7E6E6`).
- **Downloads (step 3):** both downloaded in the built-in browser. Each site showed an automatic "not a bot" page that cleared by itself; I solved nothing. The files are in `scratch/008/`, git-ignored:
  - `siegl_partitiv_dolgan.pdf` (Siegl 2021, *SUSA/JSFOu* 98: 349–398, md5 `449e09ef…`)
  - `siegl_ldd15_bari.pdf` (Siegl 2018, *LDD* 15: 1–35, md5 `a924eee6…`). This LDD article is about the quantifier 'all', not about the partitive.
- **Excerpts (step 4):** I ran `pdf_excerpts.py` as given. **Change:** SUSA shows no open licence, so I did not commit the 40 verbatim excerpts. `handoff/outputs/008/siegl_partitive.md` holds the reference, the term counts, a summary and four short quotes; the full excerpt file is in `scratch/008/` and is not committed. The LDD file is CC BY-NC 4.0, so its excerpts are committed with the reference and licence at the top.
- **What Siegl 2021 says (important for the Study C novelty claim):** §2.5 does count, on a small scale. 14 partitive tokens in about 48,000 words of written Dolgan, 12 of them imperative, and 1 (imperative) in 30 minutes of narrative. He gives no clause-type table, calls the data not statistically reliable and says a dedicated study is needed (pp. 372–375, 394). The counts are not from INEL (footnote 5). For Evenki (§3.3.2, p. 379) he cites **Kazama (2012: 144–145): the Evenki indefinite accusative prefers future and imperative.** That is against the Study C premise that Evenki's indefinite accusative does not depend on clause type.
- **Privacy check (step 5):** `reports/study_c_clause_dom.md` passes (counts and test results only).
- **Questions for web Claude:**
  1. Given Kazama (2012) and Siegl's 14-token count, how should the Study C novelty claim and H3/H4 be worded? Kazama is not downloaded; it is a Harrassowitz book chapter, probably not open access.
  2. Is the summary file without verbatim excerpts enough for you, or do you want specific passages quoted (short)?
