# PLAN: living status page

Update this at the end of every work session. Last updated: 2026-11-04 by desktop Claude.

## Current phase
**Phase 0 complete (scaffold pushed). Data acquisition is blocked.** Handoff 001 is `blocked`: the corpus hosts are refused by the network egress allowlist. Handoff 002 waits on 001. Nothing can be tested on real data yet.

## Next actions
| # | Who | Action | Where |
|---|---|---|---|
| 1 | Jude | Add Dustan as a collaborator on the GitHub repo | GitHub, Settings, Collaborators |
| 2 | Jude + desktop Claude | **BLOCKED.** Allow the Hamburg domains in egress settings, or download the two no-audio zips by hand (see handoff 001 Results), then re-run 001 | `handoff/001-environment-and-download.md` |
| 3 | Jude + desktop Claude | Run handoff 002 (inspect real structure) | `handoff/002-inspect-structure.md` |
| 4 | Jude, Dustan | Start the reading list (it does not need data) | `docs/ROADMAP_HUMAN.md`, Phase 2 |
| 5 | web Claude | After 002 returns: write the parser and tests (WP3) | `docs/ROADMAP_CLAUDE_WEB.md` |

## Gates
| Gate | Question | Status |
|---|---|---|
| G0 | Is there enough data of the right kind for each design? (speakers by birth year, SyF coverage, counts) | not started |
| G1 | Has the literature been re-checked and the closest authors contacted before we commit? | not started |
| G2 | Is the evidentiality codebook stable (pilot agreement acceptable)? | not started |
| G3 | Is the analysis plan frozen before outcomes are examined? | not started |

Criteria for each gate are in `docs/ROADMAP_CLAUDE_WEB.md` and `docs/ROADMAP_HUMAN.md`.

## Open decisions
See `docs/DECISIONS.md`. Currently open: D-004 licensing, D-005 stats stack, D-006 evidentiality codebook, D-007 Evenki comparison design, D-008 which Study B sub-questions survive G0, D-009 target venues.

## Log (newest first)
- 2026-11-04: Desktop Claude set up the repo on Jude's computer. Handoff 001 step 1 done (environment report). Step 2 blocked: HTTP 403 from proxy for hdl.handle.net, www.fdr.uni-hamburg.de and inel.corpora.uni-hamburg.de. No corpus downloaded. 002 not started.
- 2026-11-04: Repo scaffolded. Plans written. Handoff 001 and 002 created.
