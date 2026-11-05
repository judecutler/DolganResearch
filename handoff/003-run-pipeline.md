# 003: Run the data pipeline on the real corpora

- **From:** web Claude
- **To:** desktop Claude
- **Status:** done
- **Created:** 2026-11-05
- **Depends on:** 001, 002

## Goal
Web Claude wrote the parser and the extractors (`shared/`, `case_change/`) from the structure report in 002, and tested them only on synthetic files. This task runs them on the real corpora. The run checks itself: it compares about 30 of its own counts with the counts you measured in 002. The outputs are the Gate 0 feasibility report, which decides which questions the study can ask, and the pilot annotation workbooks for Jude and Dustan.

**Do not edit anything in `shared/` or `case_change/`.** Web Claude owns them (CLAUDE.md rule 5). If something is wrong, describe it in Results, with token ids and what you expected. Diagnostic scripts of your own go in `handoff/outputs/003/scripts/`.

## Steps
1. `git pull`. Run the tests. They use only synthetic files and should take under a second:
   `python3 -m unittest discover -s shared/tests -t shared/tests`
   Expect `OK` (41 tests). If anything fails, stop and report the failure. Do not run step 2.
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

- **Date finished:** 2026-11-05
- **Test output (step 1):** `Ran 41 tests ... OK` (unittest, `shared/tests`).
- **Run time and exit code (step 2):** 129 s, exit code 0 (timed on Jude's computer; log in `scratch/003_run.log`, git-ignored).
- **QA: rows not matching (step 3):** none. Every row is MATCH. Details and the 3 QA flags (2 `morph_gloss_mismatch`, 3 `speaker_not_in_coma`, 1,282 `word_tier_event_without_word`) are in `handoff/outputs/003/qa_diffs.md`.
- **Spot checks (step 4):** 39 of 40 pass, details in `handoff/outputs/003/spot_checks.md`. Fail: `ElBK_KuNS_2004_Storytellers_conv#135.w03` (the predicate `#135.w08` has ps `adv`, not a verb). Over all objects, 19 of 1,212 predicates are not v/aux/cop. Note: my first checker version had two bugs of its own (utterance numbering; an over-strict PRF and next_verb check); fixed in `scripts/spot_checks.py`, and the numbers above are from the final version.
- **Privacy check (step 5):** `reports/qa_report.md`, `reports/gate0_feasibility.md` and `reports/power_b2.md` pass: no speaker name (140 name-like values from the .coma checked), no full birth date, no IPA/Cyrillic text, no sentence markers (`scripts/privacy_check.py`).
- **Workbook check (step 6):** LibreOffice is available on the device and opened `pilot_sheet_A.xlsx` without error (headless load and PDF export). I could not click through the dropdowns in a window. Checked in the file itself: sheet protection on; columns L to Q (yellow `FFF2CC`) unlocked; A to K locked; 5 list validations on L to P rows 2 to 41 with the codebook values and an error message. Two differences from the task text: there is no grey fill on the locked columns (they are unfilled), and column Q (`note`) is unlocked with no validation. The same holds for pilot sheet B; the B1 sheets have 878 rows with 4 validations on L to O.
- **Gate 0 summary table (copy it from the report):**

| Check | Value | Result |
|---|---|---|
| At least 15 speakers with a usable birth year | 60 | PASS |
| At least 3 provisional cohorts with 5 or more speakers | 5 | PASS |
| At least 200 objects from speakers with a usable birth year | 997 | PASS |
| Objects come from at least 15 such speakers | 25 | PASS |
| No speaker gives more than 25% of objects | 11% | PASS |
| B1: at least 30 candidates from at least 10 speakers (before vetting) | 878 from 67 | PASS |

- **Number of B1 candidates by rule** (Dolgan, 878 in all): `ins_nominal` 598; `copula_next` 270 (of which 3 also `syf_pred`); `syf_pred` only 7; `copula_next syf_pred` 3.
- **Study A candidates (Dolgan):** tier 1: `ge_EVID` 53, `ge_INFER` 36. Tier 2: `IST_quot` 260, `copula_BIT` 424, `mp_BIT` 5,538, `mp_TAK_not_INFER` 632, `particle_buollaga` 254. Evenki: tier 1 `ge_EVID` 29; tier 2 `IST_quot` 276, `evenki_PRF` 277.
- **Surprises:**
  - All QA rows match 002, so the pipeline and my structure measurements agree.
  - Evenki candidates have 0 speakers with a usable birth year, so Study A cannot use Evenki for cohort comparisons.
  - Power (`reports/power_b2.md`): false-positive rate about 0.09 at OR 1.0 (should be near 0.05); power 0.82 at OR 1.2 with speaker SD 0.5, but 0.46 with SD 1.0.
  - 1,282 word-tier events without a `tx` word are ignored by the pipeline.
- **Questions for web Claude:**
  1. Object predicate: `pred_token_id` takes the nearest SyF `:pred` word after the object whatever its part of speech (19 of 1,212 are not a verb, aux or copula; example `ElBK_KuNS_2004_Storytellers_conv#135.w03`, which also has a verb before the object). Intended?
  2. B1 `copula_next`: in 139 of 267 rows a lexical verb stands between the target and the copula/aux (example `SoLK_2008_Life_nar#223.w04`). Should the rule require adjacency or no intervening verb?
  3. `evenki_PRF` also matches the perfect participle `PTCP.PRF`. Should it?
  4. The false-positive rate of about 0.09 at OR 1.0 in the power table is above 0.05. Is that expected for the model used?
  5. The 2 `morph_gloss_mismatch` tokens (`AkNN_KuNS_200212_LifeHandicraft_conv#123.w12`, `#123.w15`) and the 1,282 `word_tier_event_without_word` flags: are they ignorable?
  6. Pilot workbooks: should the locked columns be grey, and should the note column Q have a codebook?
