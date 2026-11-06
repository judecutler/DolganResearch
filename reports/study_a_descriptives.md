# Study A, exploratory: evidential and past forms in the corpus glosses

Built by `shared/evid_descriptives.py`. **Exploratory.** These counts use the INEL annotators' glosses (only glosses without `%`), not Jude and Dustan's coding, and no hypothesis was fixed in advance. Tense forms are counted only on finite verbs (no `PTCP`).

## 1. Forms per 1,000 glossed words, by genre

### Dolgan

| Genre | Glossed words | EVID per 1,000 (n; speakers) | INFER per 1,000 (n; speakers) | PST2 per 1,000 (n; speakers) | PST1 per 1,000 (n; speakers) | COND1 per 1,000 (n; speakers) |
|---|---|---|---|---|---|---|
| conv | 19671 | 0.97 (19; 10) | 0.20 (4; 4) | 37.97 (747; 20) | 50.07 (985; 20) | 2.95 (58; 13) |
| flk | 31609 | 0.41 (13; 10) | 0.89 (28; 9) | 87.19 (2756; 26) | 24.68 (780; 25) | 7.85 (248; 25) |
| misc | 111 | 0.00 (0; 0) | 0.00 (0; 0) | 0.00 (0; 0) | 0.00 (0; 0) | 0.00 (0; 0) |
| nar | 41174 | 0.51 (21; 10) | 0.10 (4; 2) | 43.23 (1780; 38) | 30.80 (1268; 39) | 6.00 (247; 28) |
| sng | 98 | 0.00 (0; 0) | 0.00 (0; 0) | 0.00 (0; 0) | 20.41 (2; 1) | 0.00 (0; 0) |
| transl | 746 | 0.00 (0; 0) | 0.00 (0; 0) | 80.43 (60; 1) | 16.09 (12; 1) | 2.68 (2; 1) |

### Evenki

| Genre | Glossed words | EVID per 1,000 (n; speakers) | PST per 1,000 (n; speakers) | PRF per 1,000 (n; speakers) | AOR per 1,000 (n; speakers) |
|---|---|---|---|---|---|
| conv | 211 | 0.00 (0; 0) | 90.05 (19; 3) | 0.00 (0; 0) | 90.05 (19; 2) |
| flk | 43649 | 0.09 (4; 3) | 80.90 (3531; 39) | 1.53 (67; 18) | 175.45 (7658; 39) |
| misc | 1941 | 0.00 (0; 0) | 51.00 (99; 4) | 1.03 (2; 2) | 130.35 (253; 6) |
| nar | 45837 | 0.52 (24; 5) | 51.88 (2378; 18) | 2.55 (117; 9) | 233.33 (10695; 18) |
| song | 696 | 0.00 (0; 0) | 44.54 (31; 4) | 0.00 (0; 0) | 102.01 (71; 4) |

## 2. Dolgan finite past verbs: PST2 (indirect) versus PST1 (direct)

| Genre | Finite past verbs | PST2 | PST2 share |
|---|---|---|---|
| conv | 1732 | 747 | 43.1% |
| flk | 3536 | 2756 | 77.9% |
| nar | 3046 | 1779 | 58.4% |
| sng | 2 | 0 | 0.0% |
| transl | 72 | 60 | 83.3% |

| Subject person | Finite past verbs | PST2 | PST2 share |
|---|---|---|---|
| 1 | 1359 | 639 | 47.0% |
| 2 | 323 | 124 | 38.4% |
| 3 | 6683 | 4565 | 68.3% |
| none | 23 | 14 | 60.9% |

| Genre and person | Finite past verbs | PST2 | PST2 share |
|---|---|---|---|
| conv, person 1 | 454 | 235 | 51.8% |
| conv, person 2 | 133 | 49 | 36.8% |
| conv, person 3 | 1136 | 457 | 40.2% |
| conv, person none | 9 | 6 | 66.7% |
| flk, person 1 | 219 | 51 | 23.3% |
| flk, person 2 | 124 | 43 | 34.7% |
| flk, person 3 | 3193 | 2662 | 83.4% |
| nar, person 1 | 680 | 351 | 51.6% |
| nar, person 2 | 62 | 31 | 50.0% |
| nar, person 3 | 2290 | 1389 | 60.7% |
| nar, person none | 14 | 8 | 57.1% |

## 2b. Dolgan finite PST2 verbs by person agreement (from `mc`)

Pakendorf and Stapert (2020) describe possessive agreement as the witnessed and predicative agreement as the unwitnessed form of this past. Counts by genre; the share column is the predicative share among PST2 verbs with either agreement.

| Genre | Possessive | Predicative | Unmarked | Predicative share |
|---|---|---|---|---|
| conv | 395 | 344 | 8 | 46.5% |
| flk | 482 | 2274 | 0 | 82.5% |
| nar | 730 | 1032 | 17 | 58.6% |
| transl | 10 | 50 | 0 | 83.3% |

## 3. Speaker-clustered tests (exploratory)

Estimates are differences in PST2 share in percentage points; p from 9999 wild-cluster-bootstrap draws by speaker.

| Comparison | Speakers | Verbs | Difference (points) | p |
|---|---|---|---|---|
| Folklore minus personal narrative (flk vs nar) | 62 | 6582 | +19.5 | 0.002 |
| The same, adjusted for source | 62 | 6582 | +10.2 | 0.181 |
| First minus third person subject, nar and conv only | 52 | 4560 | -2.2 | 0.769 |
| The same, adjusted for genre | 52 | 4560 | -1.2 | 0.861 |

Among PST2 verbs with possessive or predicative agreement, the predicative share:

| Comparison | Speakers | Verbs | Difference (points) | p |
|---|---|---|---|---|
| Folklore minus personal narrative (flk vs nar) | 61 | 4518 | +23.9 | 0.000 |
| The same, adjusted for source | 61 | 4518 | +17.6 | 0.009 |
