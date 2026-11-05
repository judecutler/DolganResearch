# PLAN: living status page

Update this at the end of every work session. Last updated: 2026-11-05 by web Claude (overnight run).

## Current phase
**Pipeline built, waiting for its first real run.** Handoffs 001 and 002 are `done`. Web Claude answered 002's questions (D-016 to D-022) and built the parser, the extractors for both studies, the QA and Gate 0 reports and the annotation workbooks (`shared/README.md`). All are tested on synthetic files only. Next: desktop Claude runs handoff 003 on the real corpora. In parallel, Jude and Dustan do handoff 004.

## Next actions
| # | Who | Action | Where |
|---|---|---|---|
| 1 | Jude | Add Dustan as a collaborator on the GitHub repo | GitHub, Settings, Collaborators |
| 2 | Jude + desktop Claude | Tell desktop Claude: "pull and run handoff 003" | `handoff/003-run-pipeline.md` |
| 3 | Jude, Dustan | Confirm decisions, update the evidentiality plan, read Däbritz §6.6 and Siegl 2015, send the INEL email | `handoff/004-for-jude-and-dustan.md` |
| 4 | Jude, Dustan | After 003: code the 40-item pilot separately (Gate 2) | `handoff/004`, item 5 |
| 5 | web Claude | After 003: read `reports/qa_report.md` and `reports/gate0_feasibility.md`, fix any mismatches, then design the main annotation round and the Study B analysis | `docs/ROADMAP_CLAUDE_WEB.md` |

## Gates
| Gate | Question | Status |
|---|---|---|
| G0 | Is there enough data of the right kind for each design? (speakers by birth year, SyF coverage, counts) | not started |
| G1 | Has the literature been re-checked and the closest authors contacted before we commit? | not started |
| G2 | Is the evidentiality codebook stable (pilot agreement acceptable)? | not started |
| G3 | Is the analysis plan frozen before outcomes are examined? | not started |

Criteria for each gate are in `docs/ROADMAP_CLAUDE_WEB.md` and `docs/ROADMAP_HUMAN.md`.

## Open decisions
See `docs/DECISIONS.md`. Currently open: D-004 licensing, D-005 stats stack, D-006 evidentiality codebook, D-007 Evenki comparison design, D-008 which Study B sub-questions survive G0, D-009 target venues, D-013 cohort bins, D-014 one paper or two, D-015 authorship. Waiting for Jude's confirmation: D-016 to D-023.

## Log (newest first)
- 2026-11-05: Web Claude (overnight): docs corrected from 002; decisions D-016 to D-027; parser and pipeline in `shared/` and `case_change/` (27 tests, synthetic files); handoff 003 (real run) and 004 (humans) written. Decision trail: `.audit/overnight.tsv`.
- 2026-11-05: Handoff 002 done. Structure report, tier coverage and gloss census written to `handoff/outputs/002/`. Main surprises: Dolgan token and utterance totals do not match the documentation under any rule; Anabar texts exist despite the documentation; `-BIt`/`-DAK` are `BIT`/`TAK` in `mp`; `St` is stimulus.
- 2026-11-05: Handoff 001 done. Dolgan 2.0 (noaudio) and Evenki 2.0 (lite) downloaded, md5s match the pages. 136 Dolgan and 612 Evenki `.exb` files, matching the documented counts. Evenki has no `noaudio` package; `lite` is the text-only one per the documentation. Handoff 002 started.
- 2026-11-05: Desktop Claude read both repository pages in the built-in browser and recorded versions, md5s, licence and citations in handoff 001 Results. Nothing downloaded (browser download produced no file). Evenki has no `noaudio` package (`lite`, `standard`, `mp3` only). 001 still blocked, 002 waiting.
- 2026-11-04: Desktop Claude set up the repo on Jude's computer. Handoff 001 step 1 done (environment report). Step 2 blocked: HTTP 403 from proxy for hdl.handle.net, www.fdr.uni-hamburg.de and inel.corpora.uni-hamburg.de. No corpus downloaded. 002 not started.
- 2026-11-04: Repo scaffolded. Plans written. Handoff 001 and 002 created.
