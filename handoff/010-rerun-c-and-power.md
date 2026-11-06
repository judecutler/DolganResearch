# 010: Rerun Study C and the design report with the fixed code

- **From:** web Claude
- **To:** desktop Claude
- **Status:** todo
- **Created:** 2026-11-06
- **Depends on:** 007, 008, 009

## Goal
007 to 009 ran on code from before commit 4b39c22 (you saw 59 tests; there are now 62). Three fixes matter:
- **Study C's H4** now compares the two languages on the odds scale (ratio of odds ratios), as changed in `case_change/STUDY_C_PLAN.md` before any Study C output existed. The 008 report's H4 row is the superseded version.
- **The design report** no longer depends on `PYTHONHASHSEED` (the per-speaker random effects were drawn by iterating a set; now sorted). Thank you for catching it.
- **Coding sheets** no longer show `source_collection` either (its values name the period).

You only run commands and report. Do not edit `shared/` or `case_change/`.

## Answers to your questions
- **007 Q1 (hash seed):** fixed as above, with a test that compares simulated data under three hash seeds.
- **007 Q2 (long jobs):** `run_all.py` no longer runs the power simulation unless given `--power`. For the simulation, use the new design export (step 4) and run it in your cloud workspace. The export holds only speaker IDs, years, genre, source and predicate counts: no case, no text.
- **008 Q1 (Kazama, Siegl):** Study C now cites both, and the ledger grades it PARTIAL with a stated gap: Siegl (2021: 375) says a dedicated study is needed, and his counts are not from INEL. H3's premise (from Sheifer and Bolshakova) is contradicted by Kazama and by your counts; that is a finding, not a reason to change the plan.
- **008 Q2 (excerpts):** your summary with four short quotes is enough. Thank you for not committing the unlicensed excerpts.
- **009 Q (source-adjusted folklore effect, p = 0.18):** expected. Most folklore comes from one source (`published_folklore`), so adjusting for source leaves only the folklore inside the archive to compare with narratives, a few speakers. The estimate stays positive (+10 points); the paper reports both.

## Steps
1. `git pull`. Run the tests: `python3 -m unittest discover -s shared/tests -t shared/tests`. Expect `OK` (62 tests). Stop if it says 59: the pull did not work.
2. Rebuild the coding sheets (all yellow cells must still be empty; if not, stop and ask Jude):
   `python3 shared/workbook.py build pilot data/derived/workbooks data/derived/dolgan/evid_candidates.csv --n 40`
   `python3 shared/workbook.py build pilot data/derived/workbooks data/derived/dolgan/b1_candidates.csv --n 100000 --prefix b1 --codebook shared/config/b1_codebook.json`
   Check that `pilot_sheet_A.xlsx` has no `source_collection` column and `pilot_key.csv` does.
3. Rerun Study C in the foreground (about 30 s):
   `python3 case_change/clause_dom.py data/derived/dolgan/objects.csv data/derived/evenki/objects.csv reports/study_c_clause_dom.md`
4. Design report:
   - On Jude's computer: `python3 case_change/power.py --export-design data/derived/dolgan/objects.csv scratch/design_b2.csv`
   - Copy `scratch/design_b2.csv` and the repo's `case_change/` folder to your cloud workspace. There: `python3 case_change/power.py design_b2.csv power_b2.md` (about 9 minutes), then copy `power_b2.md` back to `reports/power_b2.md`.
   - Reproducibility check there: `PYTHONHASHSEED=1 python3 case_change/power.py design_b2.csv a.md --sims 20` and the same with `PYTHONHASHSEED=2` into `b.md`; `diff a.md b.md` should print nothing.
5. Privacy check both reports as in 003, step 5.
6. Commit `reports/study_c_clause_dom.md`, `reports/power_b2.md`, this file and `PLAN.md` (one log line). Nothing under `data/` or `scratch/`.

## Results
*(desktop Claude fills in)*

- **Date finished:**
- **Tests:**
- **Sheets rebuilt, no `source_collection` (step 2):**
- **Study C run time; H4 table (copy it):**
- **Design report run time; hash-seed diff empty? (step 4):**
- **Collinearity table and the genre + source power column (copy them):**
- **Privacy check:**
- **Questions for web Claude:**
