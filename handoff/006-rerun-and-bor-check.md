# 006: Rerun the pipeline after the 003 fixes, and check the BOR events

- **From:** web Claude
- **To:** desktop Claude
- **Status:** todo
- **Created:** 2026-11-05
- **Depends on:** 003

## Goal
Web Claude answered your six questions from 003 (answers below) and changed code in `shared/` and `case_change/`. This task reruns the pipeline so the reports match the new code, and checks one QA flag that could hide information: the 1,282 `word_tier_event_without_word` events.

**Do not edit `shared/` or `case_change/`.** Diagnostic scripts go in `handoff/outputs/006/scripts/`.

## Answers to your questions in 003
1. **Object predicate.** Not intended. A predicate must now have ps `v`, `aux` or `cop` (D-035). Objects with no verbal predicate get an empty `pred_token_id`.
2. **B1 `copula_next`.** Yes: the rule now stops at the first verb within the window. If that verb is not "be"/"become" (or SyF `cop`), there is no hit (D-035).
3. **`evenki_PRF` and `PTCP.PRF`.** Both stay in the pool, but the participle is now the rule `evenki_PTCP_PRF`. Which Evenki forms are compared is D-007, a human decision.
4. **False-positive rate 0.09.** Not expected. It was a real flaw. The speakers with 4 to 8 objects are all born last, and permuting birth years moves their noisy shares into the middle. The test is now a wild cluster bootstrap (D-034). In web Claude's simulations of a similar design it gives about 0.055, and the old test gives 0.15. A regression test covers it.
5. **QA flags.** The 2 `morph_gloss_mismatch` tokens are ignorable (2 postposition tokens). The 1,282 BOR-tier events are **not** ignorable until checked: if a `BOR` event spans two words, the loan flag is lost, and loans are a confounder in B2. Step 4 checks this.
6. **Workbooks.** Locked columns are now grey. Column Q (`note`) is free text on purpose: no codebook.

## Steps
1. `git pull`. Run the tests: `python3 -m unittest discover -s shared/tests -t shared/tests`. Expect `OK` (44 tests). If anything fails, stop and report.
2. **Protect any coding already done.** `run_all.py` overwrites the workbooks. If any yellow cell in `data/derived/workbooks/pilot_sheet_A.xlsx`, `pilot_sheet_B.xlsx`, `b1_sheet_A.xlsx` or `b1_sheet_B.xlsx` holds a value, copy the whole `data/derived/workbooks/` folder to `data/derived/workbooks_003_backup/` first, and say so in Results. Ask Jude if you can't tell.
3. Rerun: `python3 shared/run_all.py 2>&1 | tee scratch/006_run.log`. Record the run time and exit code.
4. **BOR check.** Classify the `word_tier_event_without_word` events by tier and by how the event's span relates to the same speaker's `tx` words:
   - (a) it starts at one `tx` word's start and ends at a later `tx` word's end (a multi-word event);
   - (b) it overlaps a `tx` word only partly;
   - (c) it overlaps no `tx` word of that speaker (check whether it matches another speaker's word).
   Give the counts by tier and class, 5 example token spans per class (ids and tier values only, no sentences), and the number of **objects** in `objects.csv` that fall inside a class-(a) `BOR` event but have an empty `bor`. Write this to `handoff/outputs/006/bor_check.md`.
5. Spot checks, with a fixed seed written down:
   - `ElBK_KuNS_2004_Storytellers_conv#135.w03` now has a verbal predicate, or none;
   - 5 random `copula_next` rows in `b1_candidates.csv` have no verb between the noun and the copula;
   - 3 random `evenki_PTCP_PRF` rows and 3 `evenki_PRF` rows have the gloss the rule name says.
6. Privacy check the regenerated reports as in 003, step 5.
7. Commit `reports/`, `handoff/outputs/006/`, this file and `PLAN.md`. Nothing under `data/`.

## Results
*(desktop Claude fills in)*

- **Date finished:**
- **Test output (step 1):**
- **Backup made (step 2):** yes / no, and why
- **Run time and exit code (step 3):**
- **New power table (copy from `reports/power_b2.md`):**
- **B1 candidates by rule (from the Gate 0 report):**
- **Evenki tier-2 counts, `evenki_PRF` vs `evenki_PTCP_PRF`:**
- **Objects with no predicate found (from the Gate 0 report):**
- **BOR check summary (step 4):**
- **Spot checks (step 5):**
- **Privacy check (step 6):**
- **Questions for web Claude:**
