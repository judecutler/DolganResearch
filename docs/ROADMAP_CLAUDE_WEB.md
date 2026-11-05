# Roadmap for web Claude

Exact work packages for the Claude that writes code and designs the analysis. Each has inputs, outputs, an acceptance test, and the handoff it needs. Jude and Dustan's version is `ROADMAP_HUMAN.md`.

## Status (2026-11-05, after the overnight run)
| WP | State |
|---|---|
| WP0 to WP2 | done (handoffs 001, 002) |
| WP3 parser, WP4 QA, WP5 enrich | built and tested on synthetic files; first real run is handoff 003 |
| WP6 gloss map | case labels done in `shared/inel/config.py`; TAM grouping for B2 still to draft (needs human sign-off) |
| WP7a Study B | objects (`case_change/extract_objects.py`) and B1 candidates (`extract_b1.py`, rules from Siegl 2015) built |
| WP7b Study A | candidate generator built (`shared/evid_candidates.py`) |
| WP8 | `.xlsx` workbooks with dropdowns, merge, kappa built (`shared/workbook.py`) |
| WP9 | primary B2 test, power analysis and the Gate 3 lock built (`case_change/speaker_test.py`, `power.py`, `b2_test.py`) |
| WP10 | Evenki and Sakha literature mapped; Study A re-graded to PARTIAL (Skribnik and Aikhenvald 2024) |
| WP11, WP12 | not started |

## Working conditions
- This session has no network downloads and no package installs. It can use Python 3.13 with the standard library, and pandas is present here, but parsers must still run on stdlib alone.
- It has never seen a real INEL file. Until handoff 002 returns, it writes only plans and synthetic fixtures. Fixtures use made-up content with the real structure. They never contain invented Dolgan sentences presented as data.
- All real-data runs happen on desktop Claude. Web Claude writes the script, desktop Claude runs it and commits the report, and web Claude reads the report.
- Do not claim a result that was not produced by code on the real corpus.

## Dependency map

```
WP0 scaffold (done)
  |
WP1 acquire (desktop) --> WP2 inspect (desktop)
                              |
                         WP3 parser --> WP4 QA --> WP5 enrich ---> GATE 0
                                                        |
                                    WP6 gloss map <-----+
                                        |
                  +---------------------+----------------------+
                  |                                            |
            WP7a Study B extractors                   WP7b Study A candidate generator
                  |                                            |
            WP9 analysis (after G3)                    WP8 workbook + merge + kappa
                                                               |
                                                      (humans annotate; G2)
WP10 literature upkeep   (runs alongside; feeds G1)
WP11 reproducibility and archive
WP12 paper support
```

## Work packages

### WP0: Scaffold. Done
Repo, rules, handoff protocol, plans, tasks 001 and 002.

### WP1: Acquire. Handoff 001. Desktop
Output: corpora in `data/raw/`, `data/MANIFEST.json`.

### WP2: Inspect. Handoff 002. Desktop
Output: `handoff/outputs/002/`. This decides the parser's design. If the real structure contradicts `CORPUS_NOTES.md`, update that file first.

### WP3: Parser. Web
- **Inputs:** WP2 report, real structure.
- **Outputs:** `shared/inel/` (stdlib only), `shared/config/tiers.yaml`, `shared/tests/` with synthetic fixtures, `shared/build_tables.py`.
- **Produces:** the tables in `DATA_PREP_PLAN.md` stage 3.
- **Acceptance:**
  - unit tests pass on the fixtures
  - on the real corpus (desktop run), counts of transcripts, speakers, utterances and tokens equal the documentation figures or the difference is explained in QA
  - two runs give identical output
  - unknown tiers warn and do not crash; `BOR-Phon` and `BORphon` both work
  - words with unequal morph and gloss counts are flagged, never dropped
- **Handoff:** task 003 (desktop runs `build_tables.py`, commits the console summary and the QA stub).

### WP4: QA reports. Web writes, desktop runs
- **Outputs:** `reports/qa_dolgan.md`, `reports/qa_evenki.md` as listed in `DATA_PREP_PLAN.md` stage 4.
- **Acceptance:** every optional tier has a coverage figure by source and genre; every discrepancy with the documentation is stated.

### WP5: Enrich and speaker coverage. Web writes, desktop runs
- **Outputs:** `speakers` and `texts` tables with `birth_year`, `source_collection`, `age_at_recording`; `reports/speaker_coverage.md`.
- **Acceptance:** no imputed birth years; precision recorded; the crosstab (birth decade by source by genre) exists and is readable.

### GATE 0: Feasibility
Run after WP5 and the counts half of WP7a. Output: `reports/gate0_feasibility.md`. It looks at **counts and distributions, not at the relationship between age and any outcome**, so the decision does not depend on the result.

Proposed defaults, to revisit once real numbers exist (they are not derived from power calculations):

| Check | Proposed threshold for GO |
|---|---|
| Dolgan speakers with known birth year and recorded in TDNT or Stapert texts | at least 15 |
| Birth cohorts (bins chosen after seeing the distribution) with at least 5 such speakers | at least 3 |
| Object tokens (`SyF :O`, main clause) overall | at least 200, from at least 15 speakers, with no single speaker supplying more than about a quarter |
| Secondary-predicate candidates, after vetting | at least 30 across at least 10 speakers |
| Study A candidates after rule-based generation | enough that sampling is possible; decide after seeing the number |
| Correlation of birth year with source and genre | reported; if near-total confounding, the apparent-time design fails and we say so |

Note: every number in this table is a placeholder for "enough distinct speakers that no one speaker dominates". Replace them with figures from the simulation in WP9 once real counts exist, or drop the row.

Outcomes: GO, GO with a narrower question, or STOP and switch to the backup angle in the ledger. Jude and Dustan make the call; web Claude states the evidence.

### WP6: Gloss map. Web drafts, humans approve
- **Input:** gloss census from WP2.
- **Output:** `shared/config/gloss_map.yaml` with a comment per row stating the reason.
- **Acceptance:** every label in either census is mapped or explicitly marked `ignore`; Jude and Dustan sign off in `DECISIONS.md`.

### WP7a: Study B extractors. Web
Specification in `case_change/ANALYSIS_PLAN.md`. Outputs `data/derived/objects.csv`, `data/derived/secpred_candidates.csv`, and the counts for Gate 0. Candidate lists for secondary predicates are small enough that one human reads them all.

### WP7b: Study A candidate generator. Web
Specification in `evidentiality/PLAN.md`. Output `data/derived/evid_candidates.csv` with a `rule_hit` column. High recall by design.

### WP8: Workbook, merge, agreement. Web
- **Outputs:** workbook builder, merge script, kappa script.
- **Acceptance:**
  - the sheet's ID columns survive a round trip through Excel and Google Sheets (test with a CSV opened and saved by desktop Claude)
  - the merge rejects values outside the codebook and any edited ID
  - kappa is reproduced on a hand-made example with a known answer
  - the overlap items are chosen reproducibly from a recorded seed

### GATE 2: Codebook stable
After the pilot round, humans and web Claude look at agreement and at disagreements. Move on only when the codebook categories are stable, not when a kappa number crosses a line. Web Claude reports kappa per category, not only overall.

### WP9: Study B analysis. Web, after Gate 3
- Freeze `case_change/ANALYSIS_PLAN.md` in a commit **before** any outcome is examined (Gate 3). Variable coding, exclusions, models and robustness checks are fixed there.
- Simulation-based power or sensitivity analysis using the real cohort sizes and speaker counts, to say what effect size the data could detect. Report what could not be detected.
- Models, robustness checks, figures: see the plan. Run on desktop; commit result tables and figures to `reports/`.
- **Acceptance:** results regenerate from frozen data with one command; every number in the paper traces to a file in `reports/`.

### WP10: Literature upkeep. Web
Web Claude has search tools that desktop Claude may lack, so this stays here.
1. **Map Evenki and Sakha evidentiality.** Not done. The Study A verification covered the Dolgan side. The Evenki and Sakha evidential literature was never mapped. Do this before saying anything about a "comparison gap". Add the results to the ledger.
2. **Read Siegl (2015) in full** (full text link in the ledger) and write down exactly what he claims about the dative-to-instrumental shift and what data he used. Study B's first sub-question depends on it.
3. **Check whether Däbritz (2022) is open access** (a Zenodo record exists; see ledger). If it is, read §6.6 (evidentiality) and §4.2 (case) and record what they already say.
4. **Monitor competitors every few weeks until submission:** Sheifer (object marking; epistemic modality), Riaposov-type projects in the INEL group, any new Dolgan paper citing Däbritz (2022). Record each check, with its date, in the ledger.
5. **Close the loose ends** the ledger lists (Stapert 2013 chapter titles, and others).

### WP11: Reproducibility and archive. Web
- A `Makefile` or shell script that runs stages 3 to 9 from `data/raw/`.
- A pinned environment file (Python and R) written after desktop Claude reports the real versions.
- Licensing decision D-004. Zenodo or OSF deposit at submission, with a DOI.
- A short `REPRODUCE.md`.

### WP12: Paper support. Web
- Export of numbered, glossed examples from the tables to LaTeX (`expex` or `gb4e`), each with its text ID and source line so every example can be traced to the corpus.
- Table and figure generators that read from `reports/`.
- Methods paragraph that states corpus versions, exclusions and software.
- **Acceptance:** an example exported from the table matches the corpus line character for character.

## Handoffs web Claude expects to write
| Task | Content | When |
|---|---|---|
| 003 | Run `build_tables.py`; commit console summary | after WP3 |
| 004 | Run QA and enrichment; commit reports | after WP4, WP5 |
| 005 | Gate 0 counts | after WP7a |
| 006 | Build pilot workbook; test round trip through a spreadsheet | after WP8 |
| 007 | Install analysis packages; report versions | before WP9 |
| 008 | Run models; commit results | after Gate 3 |

## Things web Claude will not do
- Decide linguistic categories for the humans. It proposes, with reasons.
- Call a gap open without a record in the ledger.
- Run an analysis whose outcome would change the design after it has been seen.
- Edit raw data, or silently drop or repair a malformed record.
- Pick up the evidentiality annotation work, apart from tooling.

## Risk register
| Risk | Effect | Mitigation |
|---|---|---|
| Birth year, source and genre are tangled | Apparent-time design is unsound | Gate 0 crosstab; source covariate; stop rule |
| Secondary predicates too rare | Sub-question 1 cannot be tested | Count first; report descriptively or drop |
| SyF coverage thin or biased by source | Object counts unrepresentative | Per-text coverage; use only annotated texts and say so |
| Sheifer and Bolshakova publish first | Object-marking question loses novelty | Frame around the age comparison; check before submitting |
| Riaposov or others cover our topic | Overlap | Monitor; contact early |
| Parser mistakes pass tests on fixtures but fail on real data | Wrong counts | Reconciliation against documentation; desktop spot checks |
| Evenki 2.0 documentation differs from 1.0 | Wrong label assumptions | Gloss census on real files (002) |
| Long chain of handoffs stalls | Slow progress | Keep tasks small; Jude triggers promptly |
