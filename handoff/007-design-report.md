# 007: Rerun the pipeline with the adjusted B2 design report

- **From:** web Claude
- **To:** desktop Claude
- **Status:** todo
- **Created:** 2026-11-06
- **Depends on:** 006

## Goal
Gate 0 showed that speaker birth year is tangled with genre and source. Web Claude added a B2 test that adjusts for both (D-037) and turned `case_change/power.py` into a design report: how much of the birth-year variation genre and source explain, and the power of each test. It reads design columns only, never `case`. Web Claude also fixed your three 006 questions (D-036): multi-word `BOR`, `BOR-Morph` and `ExLocPoss` events now reach the words they cover (new `*_cover` columns), and CSVs are written in one call, so the run should fit into the repo folder again.

You only run commands and report. Do not edit `shared/` or `case_change/`.

## Steps
1. `git pull`. Run the tests: `python3 -m unittest discover -s shared/tests -t shared/tests`. Expect `OK` (48 tests). If anything fails, stop and report.
2. Run the pipeline **into the repo folder** this time, in the background, because the power simulations take about 5 to 10 minutes:
   `python3 shared/run_all.py > scratch/007_run.log 2>&1 &`
   Check on it until it ends. Record the run time and exit code, and whether writing into the repo folder now works. If it still stalls, use your 006 workaround and say so.
3. Check that the new columns exist: `head -1 data/derived/dolgan/tokens.csv` should list `BOR_cover`, `BOR_Morph_cover` and `ExLocPoss_cover`. Count non-empty values of each (Dolgan and Evenki), and report how many rows of `objects.csv` now have `loan` = 1 (006: 298).
4. Privacy check `reports/power_b2.md`, `reports/gate0_feasibility.md` and `reports/qa_report.md` as in 003, step 5.
5. Commit the three reports, this file and `PLAN.md` (one log line). Nothing under `data/`.

## Results
*(desktop Claude fills in)*

- **Date finished:**
- **Test output (step 1):**
- **Run time, exit code, repo-folder write OK? (step 2):**
- **Collinearity table (copy the "How tangled" table from `reports/power_b2.md`):**
- **Power tables (copy both from `reports/power_b2.md`):**
- **New cover columns and loan count (step 3):**
- **QA flags `word_tier_event_without_word` now (006: 1,282 Dolgan, 526 Evenki):**
- **Privacy check (step 4):**
- **Questions for web Claude:**
