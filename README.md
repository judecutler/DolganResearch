# DolganResearch

Corpus-based studies of morphology in Dolgan (Turkic, Taymyr Peninsula, Siberia), built on the open INEL corpora from Universität Hamburg. Dolgan has about 1,000 speakers and one modern reference grammar (Däbritz 2022), so most corpus-quantitative questions are still open.

## The two studies

| | Study A: evidentiality | Study B: case change |
|---|---|---|
| Draft question | How are evidential and indirective forms distributed in Dolgan by genre and speaker generation? Does Dolgan pattern with Evenki (contact) or with Sakha (relatives)? | Is there apparent-time change in Dolgan case use? Two sub-questions: dative vs instrumental on secondary predicates, and accusative / partitive / unmarked objects. |
| Led by | Jude and Dustan (hand annotation) | Claude builds the pipeline; Jude and Dustan review |
| Folder | `evidentiality/` | `case_change/` |
| Data | INEL Dolgan 2.0, compared with INEL Evenki 2.0 | Same |

Both studies read the same cleaned tables, produced by the code in `shared/`.

Every "this is unstudied" claim in this repo has a verification record in [`docs/LITERATURE_LEDGER.md`](docs/LITERATURE_LEDGER.md). "Open" means "no falsifier found in the searches we ran", not "proven unstudied".

## Where things are

| Path | What |
|---|---|
| [`PLAN.md`](PLAN.md) | Living status page: current phase, next actions, gates. Read this first. |
| [`CLAUDE.md`](CLAUDE.md) | Rules for any Claude session working here. |
| [`docs/ROADMAP_HUMAN.md`](docs/ROADMAP_HUMAN.md) | Plain-language roadmap for Jude and Dustan. |
| [`docs/ROADMAP_CLAUDE_WEB.md`](docs/ROADMAP_CLAUDE_WEB.md) | Work packages, acceptance tests and risks for the Claude that writes code. |
| [`docs/DATA_PREP_PLAN.md`](docs/DATA_PREP_PLAN.md) | How raw corpus files become analysis-ready tables and annotation sheets. |
| [`docs/CORPUS_NOTES.md`](docs/CORPUS_NOTES.md) | Facts about the INEL corpora (tiers, tags, metadata, caveats). |
| [`docs/LITERATURE_LEDGER.md`](docs/LITERATURE_LEDGER.md) | Verified gaps, closest existing work, must-cite list, manual checks still owed. |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Decision log, including open decisions. |
| [`docs/background/`](docs/background) | The research notes behind the plan. |
| [`handoff/`](handoff) | Task files that pass work between the two Claude sessions. |
| `shared/`, `case_change/`, `evidentiality/` | Code and study plans. |
| `annotations/` | Human annotation files (small CSVs). |
| `reports/` | Generated reports (feasibility, QA). |
| `data/` | Local corpus copies. Contents are git-ignored except `MANIFEST.json`. |

## How we work

Two Claude sessions share this repo and cannot see each other's chats:
- **Web Claude** (claude.ai): planning, writing code, analysis design, literature checks. No network downloads, no package installs.
- **Desktop Claude** (Claude desktop app on Jude's computer): downloads, running code on the real corpus, installing packages, committing results.

They pass work through `handoff/`. See [`handoff/README.md`](handoff/README.md).

## Data and licensing

- Corpora are **not** committed. Download them using the instructions in `handoff/001-environment-and-download.md`; versions and checksums go in `data/MANIFEST.json`.
- INEL corpora are CC BY-NC-SA 4.0. Derived tables that contain corpus text inherit those terms if released. DoReCo Dolgan: annotations CC BY 4.0, audio CC BY-NC 4.0, and each dataset must be cited individually.
- No license has been chosen for this repo's own code yet (decision D-004).
- Derived tables use speaker IDs, not names.

## Citing the data

Cite the corpus creators for every use. Required citations are listed in `data/MANIFEST.json` once the corpora are downloaded. Questions about the corpora go to the INEL team (inel@uni-hamburg.de).
