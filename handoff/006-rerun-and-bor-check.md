# 006: Rerun the pipeline after the 003 fixes, and check the BOR events

- **From:** web Claude
- **To:** desktop Claude
- **Status:** done
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

- **Date finished:** 2026-11-06
- **Test output (step 1):** `Ran 44 tests ... OK`.
- **Backup made (step 2):** no. All yellow cells in the four workbooks were empty (checked every row), so nothing could be lost.
- **Run time and exit code (step 3):** 131 s, exit code 0. Run as `python3 shared/run_all.py --derived <local disk> --reports <local disk>`, then copied into `data/derived/` and `reports/` and checked with `diff -r` (identical). Reason: run straight into the repo folder, the table build writes thousands of CSV rows to the mounted Windows folder and did not finish within the 180 s limit of one shell call (twice; a faulthandler dump showed it was still in `build_tables.write_csv` for Dolgan). No code was changed. Log in `scratch/006_run.log` (git-ignored). QA: 0 checks differ from 002. Gate 0: all six PASS (60 speakers; 5 cohorts; 997 objects from 25 speakers; max share 11%; B1 767 from 67 speakers).
- **New power table (copy from `reports/power_b2.md`):**

| Odds ratio per decade | Power, speaker SD 0.5 | Power, speaker SD 1.0 |
|---|---|---|
| 1.0 | 0.04 | 0.04 |
| 1.2 | 0.65 | 0.27 |
| 1.35 | 0.92 | 0.64 |
| 1.5 | 0.99 | 0.82 |
| 1.75 | 1.00 | 0.94 |
| 2.0 | 1.00 | 0.99 |

- **B1 candidates by rule (from the Gate 0 report):** 767 in all: `ins_nominal` 625, `copula_next` 135, `syf_pred` 7 (003: 598, 270, 7 + 3 both).
- **Evenki tier-2 counts, `evenki_PRF` vs `evenki_PTCP_PRF`:** 186 vs 91 (sum 277 = the old `evenki_PRF`). Both from 0 speakers with a usable birth year.
- **Objects with no predicate found (from the Gate 0 report):** 106 of 1,307.
- **BOR check summary (step 4):** details in `handoff/outputs/006/bor_check.md`. Dolgan 1,282 flags: 1,259 `ExLocPoss`, 20 `BOR`, 3 `BOR-Morph`. 1,280 are class (a) multi-word events, 1 is (b) inside one word (`PoTY_2009_Aku_nar`, BOR (426, 427), value marks a borrowed suffix, probably meant for BOR-Morph), 1 is (b) crossing a word boundary (ExLocPoss), 0 are (c). Evenki 526 flags, all `ExLocPoss`, all class (a). The 22 class-(a) BOR/BOR-Morph events cover 54 tokens whose `BOR`/`BOR_Morph` field is empty in `tokens.csv`, so the loan label is lost at token level. **Objects inside a class-(a) BOR event with empty `bor`: 0** (BOR-Morph: 0). So B2 is not affected now, but would be for any future object inside such an event. The multi-word `ExLocPoss` annotations are also absent from tokens.
- **Spot checks (step 5):** seed 20261106, all 12 pass (`handoff/outputs/006/spot_checks.md`). `ElBK_KuNS_2004_Storytellers_conv#135.w03` now has predicate `#135.w02` (ps `v`); over all objects 0 predicates have ps other than v/aux/cop. 5 `copula_next` rows: copula 1 or 2 words after the noun, no verb between. 3 `evenki_PTCP_PRF` rows have `PTCP.PRF`; 3 `evenki_PRF` rows have a bare `PRF`.
- **Privacy check (step 6):** the three regenerated reports and both 006 outputs pass (no names, no full dates, no IPA/Cyrillic text, no sentence markers; no local paths).
- **Note for web Claude from Jude:** please keep desktop Claude's share to what needs Jude's computer: downloads, running code on the real data, permissions, commits. Write the diagnostic scripts yourself (in the handoff or `shared/`) so desktop Claude only runs them. Here, the BOR classifier and spot-check scripts had to be written on this side.
- **Questions for web Claude:**
  1. `run_all.py` no longer fits in one 3-minute shell call on Jude's computer when it writes to the repo folder. Could the default `--derived` go to local scratch, or the CSV writing be buffered, so the documented command works as written?
  2. Should multi-word `BOR`/`BOR-Morph` and `ExLocPoss` events be carried onto the tokens they cover (like the SPAN_TIERS `*_cover` columns)? No object is affected today.
  3. The one BOR event inside a single word (`PoTY_2009_Aku_nar`, (426, 427)): treat it as BOR-Morph?
