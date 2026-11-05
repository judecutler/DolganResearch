# shared/

Code for both studies. It reads the raw INEL files and writes the tables described in [`docs/DATA_PREP_PLAN.md`](../docs/DATA_PREP_PLAN.md). Owner: web Claude. Standard library only (Python 3.10 or later). Nothing needs installing.

## One command
```
python3 shared/run_all.py
```
This reads `data/raw/dolgan-2.0/` and `data/raw/evenki-2.0/`. It writes:
- `data/derived/<corpus>/`, local only (it contains corpus text): `texts.csv`, `speakers.csv`, `utterances.csv`, `tokens.csv`, `morphemes.csv`, `qa_flags.csv`, `counts.json`, `objects.csv` (Study B) and `evid_candidates.csv` (Study A)
- `reports/qa_report.md`: counts compared with handoff 002
- `reports/gate0_feasibility.md`: is there enough data? Design counts only.
- `data/derived/workbooks/pilot_sheet_A.xlsx`, `pilot_sheet_B.xlsx` and `pilot_key.csv`: the Study A pilot

Tests (synthetic files only): `python3 -m unittest discover -s shared/tests -t shared/tests`

## Layout
| Path | What it does |
|---|---|
| `inel/config.py` | What the files contain: tier names, case labels per corpus, `.coma` keys, and the real counts from handoff 002 that the QA report checks against. Change a value only with evidence. |
| `inel/exb.py` | Reads one `.exb` into utterances and words. Tiers are aligned by timeline span. The speaker comes from the tier's `speaker` attribute, so single-speaker files work. |
| `inel/coma.py` | Reads the `.coma`, keeping only whitelisted fields. Parses birth and recording dates (`1935`, `1930/1935`, `1948.04.12.`, `1920s`, `199X`, `...`). Infers the Dolgan source collection. |
| `inel/gloss.py` | Gloss conventions: `-` and `=` boundaries, `.[NOM]` zeros, `%` marks, case per word, `SyF`/`SeR` items. |
| `inel/tables.py` | Row builders and column lists for the tables. |
| `inel/xlsx.py` | Writes and reads `.xlsx` with dropdowns and locked columns. |
| `build_tables.py` | Builds the tables for one corpus. |
| `evid_candidates.py` | Study A: every word a rule flags as possibly evidential, with its context and the rule that found it. |
| `workbook.py` | Study A: builds pilot and main annotation sheets. Merges coded sheets, checks values against the codebook, computes Cohen's kappa. |
| `qa_report.py`, `gate0.py` | The two reports. |
| `config/evid_codebook.json` | Dropdown values. A copy of the codebook in `evidentiality/PLAN.md`. |
| `../case_change/extract_objects.py` | Study B: one row per object, with speaker, cohort, source and clause context. |

## Things to know
- **Every number from the real data has been measured by desktop Claude, not by web Claude.** Web Claude tests on synthetic files (`tests/fixtures.py`). Those files copy real word forms from the 002 excerpts, and the file marks every made-up form `SYNTH`.
- A word whose `mb`, `mp` and `ge` have different morph counts is kept, with `align_ok = false` and a QA flag. Words with no analysis have `align_ok` empty.
- Assumptions not yet checked on real data. The QA report lists the values so a human can check them:
  - Any non-empty `BOR` value means a loan.
  - The `IST` quotative tags contain the string `quot`.
