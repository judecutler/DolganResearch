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

## Added after handoff 002 (2026-11-05)

| ID | Date | Decision | Why | By |
|---|---|---|---|---|
| D-016 | 2026-11-05 | The primary token count for Dolgan is the number of `tx` events (97,652), and utterances are `ref` events (14,076). Evenki uses the `# INEL:w` sum (93,264) and `ref` events (19,931). Discrepancies with the documentation are reported in QA and are not parser errors. | Dolgan documentation figures (97,625 tokens, 14,193 utterances) cannot be reproduced from the files under any rule tried. | web Claude, to confirm after the INEL team replies |
| D-017 | 2026-11-05 | The repo stays **private** while it contains corpus sentences. No public release before D-004 is settled and a names check has been run on any released text. Committed derived tables hold IDs and labels, not free text. Annotation sheets contain sentences and stay in the private repo or local. | Personal names appear inside the transcript text; speaker records contain private family and residence data. | web Claude, to confirm with Jude |
| D-018 | 2026-11-05 | The parser ignores the `mc` slot structure (it does not align with `mb` in Dolgan) and carries `mc` as a raw string. Slots are read from `mp` and `ge`. | `mb`, `mp`, `ge` align exactly; `mc` does not. | web Claude |
| D-019 | 2026-11-05 | `Anabar` texts and speakers are kept, flagged by a `dialect` column, and excluded in one robustness check. | The documentation says Anabar is not in the corpus, but the `.coma` says otherwise. Unresolved. | web Claude, to confirm after the INEL team replies |
| D-020 | 2026-11-05 | The Study A candidate pool has two tiers: **Tier 1** is every token labelled `EVID` or `INFER` (Dolgan 89, Evenki 29). **Tier 2** is the polyfunctional forms an annotator would have to judge: `TAK` glossed `COND1`, `PST2` and `PTCP.PST` (`BIT`). Tier 2 is sampled, not exhaustive. | `TAK` is glossed `COND1` 555 times and `INFER` 36 times, and `PST2` has 2,415 tokens, so exhaustive coding is not feasible. | Jude and Dustan to confirm |
| D-021 | 2026-11-05 | Study B sub-question B1 (secondary predicates) has no tag to find candidates by. Candidates come from `INSTR` and `DAT/LOC` nominals read by a human against Siegl (2015). B1 is a descriptive check unless Gate 0 shows enough tokens. | `SeR` role `St` is perception stimulus. | web Claude, to confirm after reading Siegl (2015) |
| D-022 | 2026-11-05 | The documented postterminal is provisionally `PST2` (`BIT`). Unconfirmed until Däbritz (2022) is read. | The Dolgan documentation never uses the word postterminal. | Jude and Dustan to confirm |
| D-023 | 2026-11-05 | `speakers.csv` keeps `sex`, `dialect`, `l1`, `l2` with the birth-year columns. Full birth dates never leave the `.coma` (only `birth_lo`, `birth_hi` and precision). | Sex is a standard covariate. CLAUDE.md rule 9 names only ID and birth year, so this needs a yes from Jude. | web Claude, to confirm with Jude |
| D-024 | 2026-11-05 | Tier names, case labels and the 002 reference counts live in `shared/inel/config.py`, not in YAML files. The Study A codebook is `shared/config/evid_codebook.json`. | The standard library has no YAML parser (rule 6). One place for each fact. | web Claude |
| D-025 | 2026-11-05 | An object is a word with an overt `SyF` item of function `O`. Handoff 002 used "the last part of the SyF value is `O`". The QA report gives both counts. | One `SyF` event can hold zero-argument items (`0.3.h:S`) as well as the word's own item. | web Claude |
| D-026 | 2026-11-05 | Gate 0 reports design counts only (speakers, cohorts, sources, totals). Object case by cohort stays hidden until Gate 3. | Seeing the outcome first would let us choose bins that fit it. | web Claude |
| D-027 | 2026-11-05 | Annotation workbooks are `.xlsx` with codebook dropdowns and locked ID columns. The rule that found an item is in the key, not the sheet. | Fewer invalid values, and the rule would steer the coding. | web Claude |
| D-028 | 2026-11-05 | **Proposed** (decide at Gate 3): the primary Study B2 test is the speaker-level permutation test in `case_change/speaker_test.py`. Mixed models are secondary, if R becomes available. This mostly settles D-005. | No R, statsmodels or scipy on Jude's machine. With few speakers, a speaker-level test is easier to defend. | web Claude, Jude and Dustan to confirm |
| D-029 | 2026-11-05 | **Proposed**: add recording period (real time, 1930 to 2017) as a second time axis, especially for B1. Report it next to birth cohort, never merged with it. | Siegl (2015) dates the shift within the 20th century, which the recordings span. | web Claude, Jude and Dustan to confirm |
| D-030 | 2026-11-05 | The Evenki perfect (`PRF`) is a tier-2 Study A candidate. | Malchukov (1999, 2000) treat the Tungusic perfect as the indirect-evidential form (ledger). | web Claude, to confirm in D-007 |
