# PLAN: living status page

Update this at the end of every work session. Last updated: 2026-11-05 by web Claude (after handoff 003).

## Current phase
**Pipeline run on the real corpora; Gate 0 passes.** Handoffs 001, 002 and 003 are `done`. All QA counts match 002 and all six Gate 0 checks pass. Web Claude answered desktop's questions from 003: the B2 test was miscalibrated and is replaced (D-034), and three extractor rules are tightened (D-035). Next: desktop Claude reruns the pipeline (handoff 006) and checks Stapert (005). In parallel, Jude and Dustan do handoff 004.

## Next actions
| # | Who | Action | Where |
|---|---|---|---|
| 1 | Jude | Add Dustan as a collaborator on the GitHub repo | GitHub, Settings, Collaborators |
| 2 | Jude + desktop Claude | Tell desktop Claude: "pull and run handoff 006", then "handoff 005" | `handoff/006-rerun-and-bor-check.md` |
| 3 | Jude, Dustan | Confirm decisions, update the evidentiality plan, read Däbritz §6.6 and Siegl 2015, send the INEL email | `handoff/004-for-jude-and-dustan.md` |
| 4 | Jude, Dustan | After 006: code the 40-item pilot separately (Gate 2). If you already started on the 003 sheets, keep them; 006 backs them up first | `handoff/004`, item 5 |
| 5 | web Claude | After 006: read the new power report and the BOR check; then design the main annotation round, propose cohort bins (D-013) and draft the Gate 3 freeze | `docs/ROADMAP_CLAUDE_WEB.md` |

## Gates
| Gate | Question | Status |
|---|---|---|
| G0 | Is there enough data of the right kind for each design? (speakers by birth year, SyF coverage, counts) | passed on counts (003); D-008 still needs a human call, see below |
| G1 | Has the literature been re-checked and the closest authors contacted before we commit? | not started |
| G2 | Is the evidentiality codebook stable (pilot agreement acceptable)? | not started |
| G3 | Is the analysis plan frozen before outcomes are examined? | not started |

Criteria for each gate are in `docs/ROADMAP_CLAUDE_WEB.md` and `docs/ROADMAP_HUMAN.md`.

## Open decisions
See `docs/DECISIONS.md`. Currently open: D-004 licensing, D-005 stats stack, D-006 evidentiality codebook, D-007 Evenki comparison design, D-008 which Study B sub-questions survive G0, D-009 target venues, D-013 cohort bins, D-014 one paper or two, D-015 authorship. Waiting for Jude's confirmation: D-016 to D-035.

**D-008 caveat from the Gate 0 crosstabs (counts only, no outcome seen).** The counts pass, but birth cohort is tangled with source and genre. Speakers born before 1920 appear almost only in `published_folklore` and genre `flk`. Speakers born after 1950 appear only in fieldwork and the archive, mostly `nar` and `conv`. For B2, the speakers born after 1970 give 4 to 8 objects each, one speaker per decade, so B2 in practice compares births from the 1890s to the 1960s. Genre and source must be in the model or the robustness checks, and the paper must say this.

## Log (newest first)
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
