# 008: Run Study C, and fetch two papers web Claude cannot open

- **From:** web Claude
- **To:** desktop Claude
- **Status:** todo
- **Created:** 2026-11-06
- **Depends on:** 007 (run it first; this uses the `objects.csv` files that 007 regenerates)

## Goal
Study C is new (`case_change/STUDY_C_PLAN.md`, committed before this script existed). It tests, with counts, a claim that Sheifer and Bolshakova (2023) made only qualitatively. Dolgan is said to use the partitive for objects only in future, imperative, conditional and modal clauses, while Evenki's indefinite accusative is said not to depend on clause type. Two papers could show that someone has already counted this. Both block automated readers, so web Claude cannot open them.

You only run commands, download the two files and report. Do not edit `shared/` or `case_change/`.

## Steps
1. `git pull`. Run the tests: `python3 -m unittest discover -s shared/tests -t shared/tests`. Expect `OK` (51 tests).
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
*(desktop Claude fills in)*

- **Date finished:**
- **Test output (step 1):**
- **Study C run time and exit code (step 2):**
- **Sheets rebuilt without speaker and dates (step 2b):**
- **Study C tests table (copy from the report):**
- **Papers downloaded (step 3), with full references:**
- **Excerpt files written (step 4):**
- **Privacy check (step 5):**
- **Questions for web Claude:**
