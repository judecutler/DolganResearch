# 003: Run the data pipeline on the real corpora

- **From:** web Claude
- **To:** desktop Claude
- **Status:** todo
- **Created:** 2026-11-05
- **Depends on:** 001, 002

## Goal
Web Claude wrote the parser and the extractors (`shared/`, `case_change/`) from the structure report in 002, and tested them only on synthetic files. This task runs them on the real corpora. The run checks itself: it compares about 30 of its own counts with the counts you measured in 002. The outputs are the Gate 0 feasibility report, which decides which questions the study can ask, and the pilot annotation workbooks for Jude and Dustan.

**Do not edit anything in `shared/` or `case_change/`.** Web Claude owns them (CLAUDE.md rule 5). If something is wrong, describe it in Results, with token ids and what you expected. Diagnostic scripts of your own go in `handoff/outputs/003/scripts/`.

## Steps
1. `git pull`. Run the tests. They use only synthetic files and should take under a second:
   `python3 -m unittest discover -s shared/tests -t shared/tests`
   Expect `OK` (38 tests). If anything fails, stop and report the failure. Do not run step 2.
2. Run the pipeline from the repo root (stdlib only, no installs). It reads `data/raw/dolgan-2.0/` and `data/raw/evenki-2.0/`:
   `mkdir -p scratch && python3 shared/run_all.py 2>&1 | tee scratch/003_run.log`
   It writes `data/derived/<corpus>/*.csv` (local, git-ignored), `reports/qa_report.md`, `reports/gate0_feasibility.md`, `reports/power_b2.md` (about 10 to 60 seconds of simulation; it reads no outcome), and in `data/derived/workbooks/` (local, git-ignored) the Study A pilot (`pilot_sheet_A.xlsx`, `pilot_sheet_B.xlsx`, `pilot_key.csv`) and the Study B1 vetting sheets (`b1_sheet_A.xlsx`, `b1_sheet_B.xlsx`, `b1_key.csv`). Exit code 1 means some QA checks did not match 002. That is a finding to report, not a reason to stop. Record the run time.
3. Read `reports/qa_report.md`. For every row whose status is not `MATCH`:
   - give the two numbers and the difference;
   - find up to 5 example words that explain it (token ids from `data/derived/<corpus>/tokens.csv`), and show their `tx | mb | mp | ge | SyF` values;
   - say which side you think is right, the 002 count or the pipeline, and why.
   Write this to `handoff/outputs/003/qa_diffs.md`. Excerpts at most 30 lines each, no speaker names.
4. **Spot checks against the `.exb` files** (CLAUDE.md rule 7). Pick at random, with a fixed seed, and write the seed down:
   - 10 rows of `data/derived/dolgan/objects.csv`. For each, open the `.exb` and confirm `tx`, `ge`, `SyF`, `case`, the `speaker_id`, and that `pred_token_id` is a verb in the same utterance.
   - 10 rows of `data/derived/dolgan/evid_candidates.csv` (5 from tier 1 and 5 from tier 2), and 3 from Evenki. Confirm the word, its gloss, the rule, and that the `context` sentence is the right utterance.
   - 5 rows of `data/derived/dolgan/b1_candidates.csv`. Confirm the case and the neighbouring copula (`next_verb`).
   - 5 utterances from a **multi-speaker** Dolgan text. Confirm that each word is assigned to the right speaker.
   - 5 rows of `data/derived/dolgan/speakers.csv`. Confirm `birth_lo`/`birth_hi` against the `.coma` value.
   Record each check as pass or fail in `handoff/outputs/003/spot_checks.md`. Use token ids only, no names.
5. Check the reports for private data before committing: `reports/qa_report.md` and `reports/gate0_feasibility.md` must contain no speaker names, no full birth dates, and no corpus sentences. They hold counts, labels and the values of the `BOR` and `IST` tags. If anything else got in, do not commit that file; say what you found.
6. Open `data/derived/workbooks/pilot_sheet_A.xlsx` in whatever spreadsheet program is available (LibreOffice, or tell Jude to open it in Excel or Numbers). Check that the dropdowns work in the yellow columns and that the grey columns are locked. If nothing can open it, say so.
7. Commit `reports/qa_report.md`, `reports/gate0_feasibility.md`, `reports/power_b2.md`, `handoff/outputs/003/`, this file and `PLAN.md`. Do **not** commit anything under `data/derived/`: it contains corpus text.

## Expected outputs
- `reports/qa_report.md`, `reports/gate0_feasibility.md` (committed)
- `handoff/outputs/003/qa_diffs.md`, `handoff/outputs/003/spot_checks.md` (committed)
- `data/derived/...` and `data/derived/workbooks/...` (local only)
- Results below, and a line in `PLAN.md`

## Acceptance checks
- [ ] Tests pass (step 1), with the output pasted in Results.
- [ ] `run_all.py` finished. Run time recorded.
- [ ] Every QA row that does not `MATCH` is explained in `qa_diffs.md`, or marked "could not explain".
- [ ] All spot checks done and recorded. Any failure is described with token ids.
- [ ] Privacy check of the two reports done (step 5).
- [ ] Nothing under `data/derived/` and no corpus file is staged (`git status` before committing).

## How to report
Fill in Results. If the run crashes, set Status `blocked` and paste the last 30 lines of the traceback. Do not patch the code.

---

## Results
*(desktop Claude fills in)*

- **Date finished:**
- **Test output (step 1):**
- **Run time and exit code (step 2):**
- **QA: rows not matching (step 3):**
- **Spot checks (step 4):** passed / failed, with the token ids of any failures
- **Privacy check (step 5):**
- **Workbook check (step 6):**
- **Gate 0 summary table (copy it from the report):**
- **Number of B1 candidates by rule** (from the Gate 0 report; web Claude tightens the rules if there are too many to vet):
- **Surprises:**
- **Questions for web Claude:**
