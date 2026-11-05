# Data preparation plan

Goal: turn the raw INEL files into tables and annotation sheets so that Jude's and Dustan's limited time goes into reading sentences and making judgment calls, not into cleaning data.

Status: plan only. Nothing is built. The parser design is provisional until handoff 002 returns the real file structure.

## Pipeline

```
 raw INEL files (.exb, .coma)              data/raw/            [never edited]
        |
 1. ACQUIRE      download, checksum, manifest                   desktop Claude, handoff 001
 2. INSPECT      learn the real structure                       desktop Claude, handoff 002
        |
 3. PARSE        .exb + .coma  ->  tables                        shared/inel/
        |
 4. QA           alignment, coverage, anomalies                 reports/qa_*.md
        |
 5. ENRICH       speaker birth year, source, genre, age         speakers, texts tables
        |
 6. NORMALISE    gloss labels -> analysis categories            shared/config/gloss_map.yaml
        |                                                          (needs human sign-off)
        +----------------------+--------------------------+
        |                                                 |
 7a. EXTRACT (Study B)                          7b. EXTRACT (Study A)
     object marking, secondary                      evidential candidates,
     predicate candidates                           with context windows
        |                                                 |
 8a. VET small candidate sets                   8b. ANNOTATION WORKBOOK
     (spot-check by a human)                        humans code each item
        |                                                 |
 9. FREEZE       tag the data version, then analysis reads only frozen tables
```

Each stage writes to `data/derived/` and can be re-run from `data/raw/` plus a commit hash. Humans never hand-edit derived tables.

## Stage 1 to 2: acquire and inspect
See `handoff/001` and `handoff/002`. Output: `data/MANIFEST.json`, `handoff/outputs/002/*`.

## Status (2026-11-05)
Stages 3 to 8 are built (`shared/README.md`) and tested on synthetic files. They have not yet run on the real corpora: that is handoff 003. Parquet is dropped; everything is CSV (stdlib).

## Stage 3: parse

Reads `.exb` (transcripts) and `dolgan.coma` (metadata) with the standard library only (`xml.etree`, `csv`).

Canonical tables (CSV for anything small or committed, Parquet optional for large local files):

| Table | One row per | Key columns |
|---|---|---|
| `texts` | communication | `corpus`, `text_id`, `genre`, `source_collection`, `title_en`, `recording_year`, `dialect`, `has_audio`, `audio_file`, `n_utterances`, `n_tokens`, `tiers_present` |
| `speakers` | speaker | `corpus`, `speaker_id`, `birth_year`, `birth_year_precision`, `region`, `l1`, `l2` |
| `utterances` | utterance | `utt_id`, `text_id`, `speaker_id`, `t_start`, `t_end`, `ts`, `fe`, `fr`, `fg`, `ltr`, `nt` |
| `tokens` | word | `token_id`, `utt_id`, `idx`, `tx`, `ps`, `mc`, `mb`, `mp`, `ge`, `gr`, `SyF`, `SeR`, `IST`, `Top`, `Foc`, `BOR`, `BOR_Phon`, `BOR_Morph`, `CS`, `ExLocPoss`, `n_morphs`, `align_ok` |
| `morphemes` | morpheme in a word | `token_id`, `m_idx`, `form_surface`, `form_underlying`, `gloss_en`, `kind` (stem, suffix, clitic), `gloss_norm` |
| `qa_flags` | problem found | `token_id` or `text_id`, `flag`, `detail` |

ID scheme: `text_id` is the communication name; `utt_id = <text_id>#<nnn>`; `token_id = <utt_id>.w<nn>`. IDs are stable across rebuilds because they come from the source files, not from row order.

Design points:
- **Alignment.** Word-level tiers are joined by timeline events. Morphemes inside a word are split on the separators found in handoff 002 and matched one-to-one against glosses. A word whose morph count and gloss count differ is kept and flagged `align_ok = false`. It is never silently dropped or repaired.
- **Tier aliases** (`BOR-Phon` / `BORphon`, `BOR-Morph` / `BORmorph`) live in `shared/config/tiers.yaml`.
- **Unknown tiers** produce a warning and are carried through as extra columns.
- **Encoding.** Latin and Cyrillic are both present. Read and write UTF-8 and normalise Unicode (NFC) in one place.
- **Determinism.** Same input and same commit give byte-identical output.

## Stage 4: QA
Report per corpus (`reports/qa_dolgan.md`, `reports/qa_evenki.md`):
- counts of texts, speakers, utterances, tokens, reconciled with the documentation figures in `CORPUS_NOTES.md`
- per-text coverage of each optional tier (SyF, SeR, IST, BOR, CS, ExLocPoss), summarised by source and genre
- share of words with `align_ok = false`, by source
- count of `%` and `%%` glosses, by source
- gloss labels that appear in the data but not in the documentation, and the reverse
- parse failures and odd files

A parser that cannot reproduce the documented counts, or explain the difference, is not finished.

## Stage 5: enrich
The step that Study B depends on.
- **Birth year.** Parse every format found in handoff 002. Record `birth_year_precision` (exact, year-only, approximate, missing). Never impute.
- **Source collection.** From the communication name or metadata: published folklore, TDNT, Stapert 2007 to 2010, 2017 experiment (Dolgan); Rychkov, Vasilevich, Anisimov, Bolina, TDNT, other (Evenki).
- **Age at recording** = `recording_year - birth_year`, only where both are known.
- **Cohort bins** are chosen after looking at the speaker-by-year distribution and **before** looking at any outcome. Record the choice in `DECISIONS.md`.
- **Crosstab report** `reports/speaker_coverage.md`: speakers by birth decade, source, genre, dialect, number of tokens. This is the first half of Gate 0.

## Stage 6: normalise gloss labels
A human-edited file `shared/config/gloss_map.yaml` maps each corpus's gloss label to an analysis category. It is separate from the parser so that linguistic decisions are visible, reviewable and reversible.

Examples of what it must settle:
- Case: Dolgan has `DAT/LOC` (merged), `PART`, `INSTR`; Evenki has `DAT`, `LOC`, `COM`, `ACC.INDEF`, `LAT`, `PROL`. Which Dolgan and Evenki labels count as "accusative-type", "unmarked object", "instrumental/comitative"?
- Evidentiality: which labels and which forms count as candidates in each corpus.
- Clause TAM context for Study B: group Dolgan `FUT`, `IMP`, `COND1/2`, `POT`, `NEC`, `INTL` and so on into the contexts that Sheifer and Bolshakova (2023, slides) contrast. Evenki has different labels.

Web Claude drafts the map from the gloss census (handoff 002). Jude and Dustan approve every row.

## Stage 7: extract candidates

### 7a. Study B
Details in `case_change/ANALYSIS_PLAN.md`. In short:
- **Objects:** tokens with `SyF` ending `:O` in main clauses, with their case morphology (NOM, ACC, PART in Dolgan; NOM, ACC, ACC.INDEF in Evenki), the clause verb's TAM, possessive marking, demonstrative, information status.
- **Secondary-predicate candidates:** nominals marked INSTR or DAT/LOC in the predicate's neighbourhood that are not arguments by `SeR`/`SyF`. `SeR` role `St` turned out to be perception stimulus (D-021); the filter waits for Siegl (2015).
- Counts only, at first (Gate 0).

### 7b. Study A
A **high-recall** candidate generator, because humans can discard false hits but never see missed ones.
- Rule 1, by label: any morpheme glossed `EVID` or `INFER`.
- Rule 2, by form: the forms Däbritz (2023) describes: the inferential `-DA4K` + possessive agreement, the postterminal `-BI4T`, and the copula's 3SG postterminal *äbit*, which has become an evidential particle. Match on `mp` and `mb` forms. Which gloss labels these carry is unknown until handoff 002.
- Rule 3, by neighbourhood: quotative frames (`IST` tags `quot-sp`, `quot-th`).
- Rules are listed in `evidentiality/PLAN.md` and logged in each output so that every candidate says which rule found it.
- For Evenki: labels `EVID`, `AOR`, `PROB` plus whatever Däbritz or the Evenki literature says. The Evenki evidential literature has **not yet been mapped** (see ledger, Study A).

## Stage 8b: annotation workbook (Study A)
One CSV per round, built by code. Opens in Excel or Google Sheets.

| Column group | Columns |
|---|---|
| IDs (never edit) | `item_id`, `token_id`, `text_id`, `utt_id`, `rule_hit` |
| Pre-filled context | `corpus`, `genre`, `source_collection`, `speaker_id`, `birth_year`, `recording_year`, `t_start`, `t_end` |
| The sentence | `prev_utt_tx`, `utt_tx`, `utt_mb`, `utt_ge`, `utt_fe` (English), `utt_fr` (Russian), `next_utt_tx`, and the target word marked |
| To fill in | coding columns from the codebook (see `evidentiality/PLAN.md`), `confidence`, `note` |

Practicalities:
- Dropdown lists (data validation) on every coding column, built from the codebook.
- Sorted randomly, not by text, so that fatigue and drift are not confounded with text or speaker. The sheet records the seed.
- A pilot round (about 30 to 50 items) first. The codebook is revised after the pilot.
- **Overlap sample**: a fixed 15 percent of items coded by both annotators, hidden among the rest. Agreement is computed with Cohen's kappa. If it is low, the codebook is wrong, not the annotators.
- The merge script **rejects** values outside the codebook and any edited ID column.
- Items where the glossing looks broken (`align_ok = false`, `%` marks) are flagged, not removed.
- Audio is optional. Where the texts have audio and the audio package is downloaded, `t_start` and `t_end` give the segment to listen to. The folklore texts have no audio.

## Stage 9: freeze
- Tag the repo `data-v1` once the annotations are adjudicated and QA is clean.
- Record the corpus versions and md5 values, the commit hash, and the seed in `reports/freeze_v1.md`.
- Analysis code reads only frozen tables. Any later change creates `data-v2`. It is never an in-place edit.

## What the humans do not have to do
- Download, unzip, parse, align, count, clean, merge or format anything.
- Choose which sentences to look at (the generator does, recall-first).
- Keep track of IDs, versions or seeds.

## What only the humans can do
- Approve the gloss map.
- Decide the coding scheme and the cohort bins.
- Code every Study A item.
- Judge the sentences Claude cannot (what a form means in context).

## Time budget (guess; revise after Gate 0)
- Gloss map review: 1 to 2 hours together.
- Pilot coding: about 2 hours each.
- Main coding: about 1 to 2 minutes an item. 300 items is about 5 to 10 hours per annotator, including the overlap. If Gate 0 shows many more candidates, we sample, we do not annotate everything.

## Risks specific to data
| Risk | How we catch it |
|---|---|
| Parser misaligns morphs and glosses | `align_ok` flag; per-source mismatch rate in QA; counts reconcile with documentation |
| Source differences masquerade as age effects | Source is a covariate; restrict to the best-glossed source as a robustness check |
| Birth years missing or ambiguous for many speakers | Speaker coverage report; Gate 0 |
| SyF coverage too thin for object counts | Per-text SyF coverage; Gate 0; fallback in `case_change/ANALYSIS_PLAN.md` |
| Evenki and Dolgan labels not comparable | `gloss_map.yaml` with human sign-off; compare categories, not raw labels |
| Corpus updated while we work | Pinned versions in `MANIFEST.json` |
