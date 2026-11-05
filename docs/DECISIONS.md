# Decision log

Newest decisions at the bottom of each list. Record the date and who decided.

## Decided

| ID | Date | Decision | Why | By |
|---|---|---|---|---|
| D-001 | 2026-11-04 | Primary data: INEL Dolgan Corpus 2.0 and INEL Evenki Corpus 2.0. DoReCo Dolgan is optional validation. | Open, glossed, matching tier design. See `CORPUS_NOTES.md`. | Jude |
| D-002 | 2026-11-04 | Two studies on one data layer. Study A (evidentiality) is led by Jude and Dustan. Study B (case change) is built by Claude and reviewed by humans. | Splits hand analysis from computational work. | Jude |
| D-003 | 2026-11-04 | Two Claude sessions (web and desktop) coordinate through `handoff/` in this repo. | The accounts cannot message each other. | Jude |
| D-010 | 2026-11-04 | Stdlib-first parsing. Raw corpora are never committed. Small derived tables may be. | Licence and size; portability without installs. | web Claude, to confirm |
| D-011 | 2026-11-04 | Derived tables keep speaker ID, birth year, L1/L2 and region only. No names, family details or coordinates. | Minimise personal data about speakers. | web Claude, to confirm |
| D-012 | 2026-11-04 | Gap claims need a ledger record. "Open" means no falsifier found in the searches run. | Avoid building on a gap that is already filled. | Jude |

## Open

| ID | Decision | Options and a recommendation | Needed by |
|---|---|---|---|
| D-004 | Licences | Code: MIT or similar. Derived tables containing corpus text: CC BY-NC-SA 4.0, since INEL requires share-alike and non-commercial use. Paper: CC BY. **Confirm with the INEL team** what they expect for derived annotation sheets. We are not lawyers. | before any public release |
| D-005 | Stats stack | Python for extraction; R (`lme4`, `brms`) for mixed models, which are better supported there. Alternative: all Python with `statsmodels` or `bambi`. Depends on what is installed on Jude's machine (handoff 001 reports it). | before WP9 |
| D-006 | Evidentiality codebook | Strawman in `evidentiality/PLAN.md`. Jude and Dustan decide after the pilot. | Gate 2 |
| D-007 | What counts as an evidential in Evenki, and which forms to compare | Needs the Evenki and Sakha literature (WP10) and the Evenki gloss census (handoff 002). | before the main annotation round |
| D-008 | Which Study B sub-questions survive Gate 0 | Decide from the counts in `reports/gate0_feasibility.md`. | Gate 0 |
| D-009 | Target venues | Ideas to check for scope and policies, not recommendations: *Turkic Languages*, *Journal of Language Contact*, *Studies in Language*, *Journal of Endangered Languages*. Choose after the results are in. | before writing |
| D-013 | Cohort bins for speaker birth year | Chosen after the speaker distribution is known and before any outcome is seen. | before Gate 3 |
| D-014 | Whether the two studies become one paper or two | Depends on what survives Gate 0 and how well the results fit together. | before writing |
| D-015 | Authorship and acknowledgements | Include the INEL team's contribution in the acknowledgements. Discuss authorship between the two of you early, in writing. | before writing |
