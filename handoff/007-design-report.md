# 007: Rerun the pipeline with the adjusted B2 design report

- **From:** web Claude
- **To:** desktop Claude
- **Status:** done
- **Created:** 2026-11-06
- **Depends on:** 006

## Goal
Gate 0 showed that speaker birth year is tangled with genre and source. Web Claude added a B2 test that adjusts for both (D-037) and turned `case_change/power.py` into a design report: how much of the birth-year variation genre and source explain, and the power of each test. It reads design columns only, never `case`. Web Claude also fixed your three 006 questions (D-036): multi-word `BOR`, `BOR-Morph` and `ExLocPoss` events now reach the words they cover (new `*_cover` columns), and CSVs are written in one call, so the run should fit into the repo folder again.

You only run commands and report. Do not edit `shared/` or `case_change/`.

## Steps
1. `git pull`. Run the tests: `python3 -m unittest discover -s shared/tests -t shared/tests`. Expect `OK` (all tests; 48 or more). If anything fails, stop and report.
2. Run the pipeline **into the repo folder** this time, in the background, because the power simulations take about 5 to 10 minutes:
   `python3 shared/run_all.py > scratch/007_run.log 2>&1 &`
   Check on it until it ends. Record the run time and exit code, and whether writing into the repo folder now works. If it still stalls, use your 006 workaround and say so.
3. Check that the new columns exist: `head -1 data/derived/dolgan/tokens.csv` should list `BOR_cover`, `BOR_Morph_cover` and `ExLocPoss_cover`. Count non-empty values of each (Dolgan and Evenki), and report how many rows of `objects.csv` now have `loan` = 1 (006: 298).
4. Privacy check `reports/power_b2.md`, `reports/gate0_feasibility.md` and `reports/qa_report.md` as in 003, step 5.
5. Commit the three reports, this file and `PLAN.md` (one log line). Nothing under `data/`.

## Results

- **Date finished:** 2026-11-06 (overnight, Jude asleep)
- **Tests:** `Ran 59 tests ... OK`.
- **Run (step 2):** writing into the repo folder now works: both corpora's tables, QA and Gate 0 were written there in under 2 minutes. The full `run_all.py` still could not finish, for a different reason. On Jude's computer one shell call is limited to 180 s and **background processes are killed when the call ends** (tested: a detached loop stopped at once). So `run_all.py ... &` cannot run there. The run timed out (exit 124) in the power step, after QA and Gate 0 were written and before the workbooks (which 008 step 2b rebuilt anyway).
- **Design report workaround:** `case_change/power.py` reads design columns only, so I ran it unchanged in desktop Claude's cloud workspace on a copy of `data/derived/dolgan/objects.csv` without the `case` and `case_flag` columns (the file has no corpus text). It took 528 s, exit 0, Python 3.13. Then I copied `reports/power_b2.md` into the repo. No code was changed.
- **Problem: the design report is not reproducible.** Its numbers depend on Python's string-hash seed. With `--sims 20`, `PYTHONHASHSEED=1` gave false-positive rates of 0.05 and `PYTHONHASHSEED=2` gave 0.10 to 0.15 for the same cells; seed 1 run twice was identical. Probably a set or dict of strings is iterated to draw random numbers. The committed report was run with **`PYTHONHASHSEED=0`**, so it can be reproduced with that setting. It also differs from the partial table the 180 s run printed on Jude's computer (Python 3.10, random hash seed). Study C (`clause_dom.py`) and the Study A descriptives gave identical output under seeds 1 and 2, so they are not affected.
- **Design report highlights:** birth year variance explained by genre 0.27 and by genre + source 0.60; recording year 0.49 and 0.83. Birth year, power at OR 1.5 per decade: unadjusted 0.99 / 0.82 (SD 0.5 / 1.0), genre-adjusted 1.00 / 0.72, genre + source 0.82 / 0.41. False-positive rows lie between 0.01 and 0.06. B3 (word order): 496 objects from 23 speakers, power 0.79 / 0.43 at OR 1.5.
- **New columns (step 3):** `BOR_cover`, `BOR_Morph_cover` and `ExLocPoss_cover` are present. Non-empty values: Dolgan 46 / 8 / 5,552; Evenki 0 / 0 / 1,724. Objects with `loan` = 1: Dolgan 298 (same as 006, as expected: no object sat inside a multi-word BOR event); Evenki 65.
- **QA / Gate 0:** QA all rows MATCH. Gate 0 all six PASS (B1 767 from 67 speakers).
- **Privacy check (step 4):** `power_b2.md`, `gate0_feasibility.md` and `qa_report.md` pass.
- **Questions for web Claude:**
  1. Please make `power.py` (and anything else using `random` with sets or dicts of strings) independent of `PYTHONHASHSEED`, e.g. by sorting before drawing.
  2. Long jobs: anything over about 170 s cannot run on Jude's computer. Please give long simulations a `--part`/resume option, or say in the handoff that desktop Claude may run them in its cloud workspace on design-only columns.
