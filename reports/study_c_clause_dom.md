# Study C: object marking by clause type, Dolgan and Evenki

Built by `case_change/clause_dom.py` from the plan in `case_change/STUDY_C_PLAN.md`. Counts are objects (SyF function O) whose case is the marker or NOM/ACC. Estimates are the irrealis-minus-realis difference in the marker's share, in percentage points, from speaker-clustered regressions; p is from 9999 wild-cluster-bootstrap draws by speaker.

## Counts by clause type

### Dolgan (marker PART)

| Clause type | PART | NOM | ACC | PART share | Speakers using PART |
|---|---|---|---|---|---|
| irrealis | 20 | 19 | 127 | 12.0% | 13 |
| realis | 3 | 175 | 832 | 0.3% | 3 |
| other | 0 | 1 | 14 | 0.0% | 0 |
| no predicate | 0 | 21 | 83 | 0.0% | 0 |

### Evenki (marker ACC.INDF)

| Clause type | ACC.INDF | NOM | ACC | ACC.INDF share | Speakers using ACC.INDF |
|---|---|---|---|---|---|
| irrealis | 45 | 16 | 141 | 22.3% | 16 |
| realis | 99 | 130 | 961 | 8.3% | 15 |
| other | 1 | 1 | 11 | 7.7% | 1 |
| no predicate | 4 | 1 | 17 | 18.2% | 3 |

## Tests

| Test | Speakers | Objects | Irrealis minus realis (points) | p |
|---|---|---|---|---|
| H1 Dolgan PART, adjusted for genre | 32 | 1176 | +11.5 | 0.000 |
| H3 Evenki ACC.INDF, adjusted for genre | 32 | 1392 | +14.1 | 0.016 |

## Robustness

| Test | Speakers | Objects | Irrealis minus realis (points) | p |
|---|---|---|---|---|
| H1 extended irrealis (adds INTNS, PROB) | 32 | 1179 | +11.3 | 0.000 |
| H3 extended irrealis | 32 | 1392 | +14.1 | 0.014 |
| H1 no pronoun objects | 32 | 964 | +14.3 | 0.000 |
| H3 no pronoun objects | 32 | 1127 | +20.3 | 0.004 |
| H1 unadjusted | 32 | 1176 | +11.8 | 0.000 |
| H3 unadjusted | 32 | 1392 | +14.0 | 0.015 |

## H4: Dolgan versus Evenki on the odds scale

Irrealis-versus-realis odds ratio of the marker in each corpus, and their ratio. A ratio above 1 means the clause effect is stronger in Dolgan. 95% interval from 2,000 draws resampling speakers within each corpus. Unadjusted for genre.

| Analysis | OR Dolgan | OR Evenki | Ratio | 95% interval |
|---|---|---|---|---|
| H4 core irrealis | 40.28 | 3.17 | 12.71 | 3.23 to 81.00 |
| H4 extended irrealis | 39.47 | 3.17 | 12.46 | 3.67 to 65.54 |
| H4 no pronoun objects | 42.33 | 4.64 | 9.12 | 2.70 to 55.77 |
