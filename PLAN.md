# PLAN: living status page

Update this at the end of every work session. Last updated: 2026-11-06 by web Claude (overnight run 2).

## Current phase
**Analysis code ready; first results in; waiting on the 010 rerun and human decisions.** Handoffs 007 to 009 are done: design report (birth year 0.60 explained by genre + source, so the adjusted test stays primary; power 0.82 / 0.41 at OR 1.5), Study C (Dolgan partitive 12.0% irrealis vs 0.3% realis; Evenki indefinite accusative 22.3% vs 8.3%), Study A gloss descriptives (PST2 78% of pasts in folklore, 43% in conversation). Handoffs 001 to 006 are `done`; Stapert (2013) does not count case by age (005). Overnight, web Claude added a genre- and source-adjusted B2 test (D-037), a design report, a freeze-ready analysis plan (B1, B2 and new B3 word order, D-040), blind coding sheets (D-039), Study C on clause-driven object marking in Dolgan vs Evenki (D-038, pre-specified), Study A gloss descriptives and a main-round proposal, and analysis scripts for B1 and Study A that wait for coding. Desktop runs 007, 008 and 009 next.

## Next actions
| # | Who | Action | Where |
|---|---|---|---|
| 1 | desktop Claude | Run 010: rebuild sheets, rerun Study C (H4 on the odds scale) and the design report (hash-seed fix) | `handoff/010-rerun-c-and-power.md` |
| 2 | Jude, Dustan | Read `case_change/ANALYSIS_PLAN.md` (blanks now filled from 007) and freeze it (Gate 3). Confirm or change D-016 to D-040 | `case_change/ANALYSIS_PLAN.md`, `docs/DECISIONS.md` |
| 3 | Jude, Dustan | Handoff 004: read Skribnik and Aikhenvald, send the INEL email (add the in-word BOR event, D-036), request Artem'ev (1999) pp. 81-82 and 102-103 | `handoff/004-for-jude-and-dustan.md` |
| 4 | Jude, Dustan | After 008 rebuilds the sheets: code the 40-item pilot separately (Gate 2); then decide on `docs/STUDY_A_MAIN_ROUND.md` | `handoff/004`, item 5 |
| 5 | Jude, Dustan | Vet the B1 sheets (no birth year shown, D-039) | `data/derived/workbooks/b1_sheet_*.xlsx` |
| 6 | Jude | Add Dustan as a collaborator on the GitHub repo | GitHub, Settings, Collaborators |
| 7 | web Claude | Read 007, 008, 009; check the Siegl and LDD excerpts for Study C; fix anything the runs show | `reports/`, `handoff/outputs/` |

## Gates
| Gate | Question | Status |
|---|---|---|
| G0 | Is there enough data of the right kind for each design? (speakers by birth year, SyF coverage, counts) | passed on counts (003); D-008 still needs a human call, see below |
| G1 | Has the literature been re-checked and the closest authors contacted before we commit? | re-checked for A, B, B3, C (ledger); Artem'ev 1999, Siegl's partitive article and LDD 1188 unread; no authors contacted |
| G2 | Is the evidentiality codebook stable (pilot agreement acceptable)? | not started |
| G3 | Is the analysis plan frozen before outcomes are examined? | plan ready to freeze, blanks wait for 007 |

Criteria for each gate are in `docs/ROADMAP_CLAUDE_WEB.md` and `docs/ROADMAP_HUMAN.md`.

## Open decisions
See `docs/DECISIONS.md`. Currently open: D-004 licensing, D-005 stats stack, D-006 evidentiality codebook, D-007 Evenki comparison design, D-008 which Study B sub-questions survive G0, D-009 target venues, D-013 cohort bins, D-014 one paper or two, D-015 authorship. Waiting for Jude's confirmation: D-016 to D-040.

**D-008 caveat from the Gate 0 crosstabs (counts only, no outcome seen).** The counts pass, but birth cohort is tangled with source and genre. Speakers born before 1920 appear almost only in `published_folklore` and genre `flk`. Speakers born after 1950 appear only in fieldwork and the archive, mostly `nar` and `conv`. For B2, the speakers born after 1970 give 4 to 8 objects each, one speaker per decade, so B2 in practice compares births from the 1890s to the 1960s. Genre and source must be in the model or the robustness checks, and the paper must say this.

## Log (newest first)
- 2026-11-06: Desktop ran 007-009 (on code before the review fixes). Web Claude: plan blanks filled; hash-seed bug fixed (sorted speakers, test under three seeds); power simulation made opt-in and exportable on design columns only (Jude's computer kills jobs over 180 s); Study C graded PARTIAL with a stated gap (Siegl 2021 counted 14 tokens and calls for a dedicated study; Kazama 2012 on Evenki, unread); H3 premise contradicted; real-time panel table added to the B2 script; handoff 010 written.
- 2026-11-06 (overnight): Handoffs 007, 008, 009 done by desktop Claude. 007: design report run in the cloud workspace on design-only columns (background jobs die on Jude's computer); it depends on PYTHONHASHSEED (committed with seed 0), a fix is needed. 008: Study C H1 +11.5 points (p<0.001), H3 Evenki +14.1 (p=0.016), H4 p=0.70; Siegl 2021 counts 14 partitives (12 imperative) and cites Kazama 2012 for an Evenki future/imperative preference, so the Study C claim needs checking. Coding sheets rebuilt without speaker/year columns. 009: PST2 share folklore 77.9% vs narrative 58.4%.
- 2026-11-06: Web Claude (overnight run 2): adjusted B2 test (genre-only effects read as birth trends 50-70% of the time unadjusted; 4-5% adjusted, D-037); design report with collinearity and power; freeze-ready plan with B3 word order (D-040); blind sheets (D-039); Study C pre-specified and scripted (D-038); Study A descriptives incl. PST2 agreement split, main-round proposal and analysis script; B1 analysis script; Gate 0 real-time panel; ledger: Stapert cleared, narrowed Study A claim open-verified, Pakendorf and Stapert (2020) read, B3 and C records. Handoffs 007-009 queued. Trail: `.audit/night2.tsv`.
- 2026-11-05: Web Claude answered handoff 003. The B2 permutation test gave 0.09 false positives on the real design because the speakers with fewest objects are all born last; replaced by a wild cluster bootstrap (D-034, about 0.055 in simulation). Object predicates must be verbal, B1 `copula_next` stops at an intervening verb, Evenki `PTCP.PRF` has its own rule, locked workbook columns are grey (D-035). 44 tests OK, each new test fails on the old code. Handoff 006 written.
- 2026-11-05: Web Claude (overnight): docs corrected from 002; decisions D-016 to D-027; parser and pipeline in `shared/` and `case_change/` (tests on synthetic files); handoff 003 (real run) and 004 (humans) written. Decision trail: `.audit/overnight.tsv`.
- 2026-11-05: Web Claude (overnight, later): an independent review found 10 problems, all fixed with regression tests (41 tests at the end of the night). Read Siegl (2015) and Däbritz (2023) in full and built Study B1 candidate rules from Siegl's examples. Mapped the Evenki and Sakha evidential literature: no comparison found, but Skribnik and Aikhenvald must be read, and Hagel (2022) is a method precedent. Added the speaker-level B2 test, a power analysis and the freeze gate. Proposed D-028 to D-030.
- 2026-11-05: Literature: Study A re-graded to PARTIAL after reading Skribnik and Aikhenvald (2024), and re-scoped as a quantitative test (D-031). Study B falsification pass (29 queries): B1 and B2 OPEN-VERIFIED, pending Stapert (2013) chapters (handoff 005) and Artem'ev (1999) pp. 81-82, 102-103 (library request in 004).
- 2026-11-06: Handoff 005 done. Stapert (2013) full text searched: no passage counts case by speaker age. The closest is Ch 5 pp. 187-188 (stem variants of case-inflected relational nouns show no age effect, no figures given). Ch 7 Table 7.3 counts OV/VO by age group. Web Claude to decide on the Study B claim.
- 2026-11-06: Handoff 006 done. 44 tests OK; rerun exit 0 (131 s, written to local disk then copied: the repo folder is too slow for one shell call). QA all MATCH; Gate 0 all PASS; B1 767; power false-positive rate now 0.04. BOR check: 22 multi-word BOR events lose their label on 54 tokens, 0 objects affected. Jude asks web Claude to write diagnostic scripts on its side and leave desktop Claude only the runs that need his computer.
- 2026-11-05: Handoff 003 done. 41 tests OK; pipeline ran in 129 s on the real corpora, all QA rows MATCH, all six Gate 0 checks PASS (60 speakers with usable birth year, 997 objects from 25 speakers, 878 B1 candidates). 39 of 40 spot checks pass; open questions for web Claude in 003 Results (object predicate choice, B1 copula_next, Evenki PRF). Reports in `reports/`, details in `handoff/outputs/003/`.
- 2026-11-05: Handoff 002 done. Structure report, tier coverage and gloss census written to `handoff/outputs/002/`. Main surprises: Dolgan token and utterance totals do not match the documentation under any rule; Anabar texts exist despite the documentation; `-BIt`/`-DAK` are `BIT`/`TAK` in `mp`; `St` is stimulus.
- 2026-11-05: Handoff 001 done. Dolgan 2.0 (noaudio) and Evenki 2.0 (lite) downloaded, md5s match the pages. 136 Dolgan and 612 Evenki `.exb` files, matching the documented counts. Evenki has no `noaudio` package; `lite` is the text-only one per the documentation. Handoff 002 started.
- 2026-11-05: Desktop Claude read both repository pages in the built-in browser and recorded versions, md5s, licence and citations in handoff 001 Results. Nothing downloaded (browser download produced no file). Evenki has no `noaudio` package (`lite`, `standard`, `mp3` only). 001 still blocked, 002 waiting.
- 2026-11-04: Desktop Claude set up the repo on Jude's computer. Handoff 001 step 1 done (environment report). Step 2 blocked: HTTP 403 from proxy for hdl.handle.net, www.fdr.uni-hamburg.de and inel.corpora.uni-hamburg.de. No corpus downloaded. 002 not started.
- 2026-11-04: Repo scaffolded. Plans written. Handoff 001 and 002 created.
