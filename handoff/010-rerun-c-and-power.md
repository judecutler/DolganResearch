# 010: Rerun Study C and the design report with the fixed code

- **From:** web Claude
- **To:** desktop Claude
- **Status:** done
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

- **Date finished:** 2026-11-06 (overnight)
- **Tests:** `Ran 62 tests ... OK`.
- **Coding sheets (step 2):** all yellow cells were still empty, so I rebuilt them (pilot 40, B1 767). No sheet has `source_collection`, `speaker_id`, `birth_year` or `recording_year`; both key files have `source_collection`.
- **Study C (step 3):** 34 s, exit 0, in the foreground. The output is identical under `PYTHONHASHSEED` 1 and 2. The new H4 (odds scale) gives: core irrealis OR Dolgan 40.28, OR Evenki 3.17, ratio 12.71 (95% interval 3.23 to 81.00); extended irrealis ratio 12.46 (3.67 to 65.54); no pronoun objects ratio 9.12 (2.70 to 55.77). H1 and H3 are unchanged from 008 (e.g. unadjusted +11.8 and +14.0 points).
- **Design report (step 4):** the export (0 s) has 1,307 rows with only `speaker_id`, birth and recording years, `genre`, `source_collection` and `n_preds_in_utt`. In the cloud workspace, `power.py design_b2.csv power_b2.md` took 530 s, exit 0 (Python 3.13); the report was copied to `reports/power_b2.md`. Reproducibility: `--sims 20` under `PYTHONHASHSEED=1` and `2` gave identical files (`diff` empty). Highlights: variance explained is unchanged (birth year 0.27 / 0.60; recording year 0.49 / 0.83). Birth year power at OR 1.5: unadjusted 0.99 / 0.81, genre 0.97 / 0.79, genre + source 0.83 / 0.42 (SD 0.5 / 1.0). False-positive rows are 0.01 to 0.07. B3 power at OR 1.5: 0.77 / 0.44.
- **Privacy check (step 5):** both reports pass.
- **Questions for web Claude:** none.
