# Argument tagger: evaluation

Built by `shared/igt_tagger/train_eval.py`; design and caveats in `docs/TAGGER_NOTES.md`. P / R / F1 are precision, recall and F1 in percent. Everything is scored on texts the model did not train on. 'Held-out' texts (20% of each language's tagged texts) were set aside before development and used once.

## Data

| Language | Split | Texts | Speakers | Words | S | O |
|---|---|---|---|---|---|---|
| dolgan | dev | 40 | 31 | 24281 | 2019 | 1052 |
| dolgan | test | 10 | 12 | 6298 | 476 | 256 |
| evenki | dev | 105 | 28 | 14814 | 2382 | 1229 |
| evenki | test | 26 | 15 | 5506 | 892 | 462 |

## Language profiles (declared vs estimated from the language's own glossed text)

- **dolgan**: declared OV, suffix, acc; estimated OV (share of accusative nominals before their verb 0.884), suffix, acc (ACC labels 6566, ERG labels 0).
- **evenki**: declared OV, suffix, acc; estimated OV (share of accusative nominals before their verb 0.769), suffix, acc (ACC labels 7593, ERG labels 0).

## Dolgan

| Evaluation | S (P/R/F1) | O (P/R/F1) | Role macro-F1 | Predicate F1 | Subordinate F1 | Zero-subject macro-F1 |
|---|---|---|---|---|---|---|
| dev, 5-fold nested CV | 72.4 / 68.3 / 70.3 | 80.9 / 75.6 / 78.1 | 74.2 | 86.0 | 66.5 | 75.6 |
| ... case-only rule baseline | 49.1 / 51.0 / 50.0 | 57.0 / 81.4 / 67.1 | 58.5 | | | |
| held-out texts | 69.7 / 70.0 / 69.8 | 82.8 / 78.9 / 80.8 | 75.3 | 87.5 | 67.7 | 77.4 |
| ... case-only rule baseline | 41.7 / 44.7 / 43.2 | 61.2 / 85.5 / 71.3 | 57.2 | | | |

Regularisation chosen in the nested folds: [0.3, 0.3, 0.1, 0.3, 0.3].

**Objects found, by case (dev CV):** ACC 717/839 (85.5%); NOM 66/184 (35.9%); PART 12/18 (66.7%); other 0/11 (0.0%)

**By speaker birth group (dev CV):** does the model work equally well for old and young speakers?

| Birth group | Speakers | S F1 | O F1 | Unmarked objects found |
|---|---|---|---|---|
| -1919 | 4 | 76.8 | 78.8 | 6/11 |
| 1920-1939 | 10 | 66.1 | 77.1 | 39/109 |
| 1940-1959 | 3 | 70.3 | 76.6 | 0/10 |
| 1960- | 6 | 63.5 | 81.3 | 10/26 |
| unknown | 8 | 77.5 | 78.8 | 11/28 |

**Objects found, by case (held-out):** ACC 188/217 (86.6%); NOM 10/32 (31.2%); PART 4/5 (80.0%); other 0/2 (0.0%)

**By speaker birth group (held-out):** does the model work equally well for old and young speakers?

| Birth group | Speakers | S F1 | O F1 | Unmarked objects found |
|---|---|---|---|---|
| -1919 | 1 | 60.2 | 84.8 | 3/7 |
| 1920-1939 | 3 | 71.1 | 78.1 | 2/10 |
| 1940-1959 | 1 | 82.4 | 100.0 | 1/1 |
| 1960- | 2 | 65.0 | 84.4 | 2/3 |
| unknown | 5 | 77.1 | 78.9 | 2/11 |

**Calibration of P(object)** on nominals (dev CV): mean predicted vs observed share of objects.

| P(O) bin | Words | Mean predicted | Observed |
|---|---|---|---|
| 0.0 | 9702 | 0.01 | 0.01 |
| 0.1 | 275 | 0.14 | 0.16 |
| 0.2 | 195 | 0.25 | 0.28 |
| 0.3 | 109 | 0.35 | 0.37 |
| 0.4 | 89 | 0.45 | 0.45 |
| 0.5 | 109 | 0.55 | 0.52 |
| 0.6 | 114 | 0.65 | 0.68 |
| 0.7 | 116 | 0.75 | 0.70 |
| 0.8 | 225 | 0.86 | 0.88 |
| 0.9 | 389 | 0.95 | 0.94 |

**Review routing (dev CV).** A nominal is flagged if the model's top probability is below the threshold, or if it is unmarked and P(O) is at least the floor. Scores assume a human corrects every flagged word.

| Threshold | Unmarked-object floor | Flagged words | Share of nominals | Utterances to review | S F1 after review | O F1 after review | Unmarked objects found |
|---|---|---|---|---|---|---|---|
| 0.7 | none | 1853 | 16.4 | 1413 of 3571 | 86.3 | 89.2 | 72.8 |
| 0.7 | 0.05 | 2136 | 18.9 | 1559 of 3571 | 87.2 | 90.4 | 83.2 |
| 0.7 | 0.1 | 1958 | 17.3 | 1469 of 3571 | 86.6 | 89.9 | 77.7 |
| 0.7 | 0.2 | 1894 | 16.7 | 1428 of 3571 | 86.4 | 89.5 | 73.4 |
| 0.8 | none | 2852 | 25.2 | 1907 of 3571 | 91.6 | 93.2 | 82.6 |
| 0.8 | 0.05 | 2983 | 26.3 | 1943 of 3571 | 91.7 | 93.5 | 85.3 |
| 0.8 | 0.1 | 2891 | 25.5 | 1917 of 3571 | 91.6 | 93.4 | 84.2 |
| 0.8 | 0.2 | 2872 | 25.4 | 1912 of 3571 | 91.6 | 93.3 | 82.6 |
| 0.9 | none | 4228 | 37.3 | 2365 of 3571 | 96.2 | 96.2 | 90.2 |
| 0.9 | 0.05 | 4255 | 37.6 | 2369 of 3571 | 96.2 | 96.3 | 90.8 |
| 0.9 | 0.1 | 4233 | 37.4 | 2365 of 3571 | 96.2 | 96.2 | 90.2 |
| 0.9 | 0.2 | 4233 | 37.4 | 2365 of 3571 | 96.2 | 96.2 | 90.2 |
| 0.95 | none | 5222 | 46.1 | 2638 of 3571 | 98.2 | 97.8 | 94.6 |
| 0.95 | 0.05 | 5222 | 46.1 | 2638 of 3571 | 98.2 | 97.8 | 94.6 |
| 0.95 | 0.1 | 5222 | 46.1 | 2638 of 3571 | 98.2 | 97.8 | 94.6 |
| 0.95 | 0.2 | 5222 | 46.1 | 2638 of 3571 | 98.2 | 97.8 | 94.6 |

**Review routing (held-out texts).** A nominal is flagged if the model's top probability is below the threshold, or if it is unmarked and P(O) is at least the floor. Scores assume a human corrects every flagged word.

| Threshold | Unmarked-object floor | Flagged words | Share of nominals | Utterances to review | S F1 after review | O F1 after review | Unmarked objects found |
|---|---|---|---|---|---|---|---|
| 0.7 | none | 425 | 15.5 | 336 of 960 | 85.0 | 88.8 | 68.8 |
| 0.7 | 0.05 | 471 | 17.2 | 363 of 960 | 85.4 | 90.3 | 90.6 |
| 0.7 | 0.1 | 439 | 16.0 | 343 of 960 | 85.1 | 89.2 | 75.0 |
| 0.7 | 0.2 | 430 | 15.7 | 338 of 960 | 85.0 | 89.0 | 71.9 |
| 0.8 | none | 657 | 24.0 | 448 of 960 | 90.3 | 92.2 | 84.4 |
| 0.8 | 0.05 | 677 | 24.7 | 461 of 960 | 90.4 | 92.6 | 90.6 |
| 0.8 | 0.1 | 658 | 24.0 | 449 of 960 | 90.3 | 92.2 | 84.4 |
| 0.8 | 0.2 | 658 | 24.0 | 449 of 960 | 90.3 | 92.2 | 84.4 |
| 0.9 | none | 1021 | 37.3 | 578 of 960 | 95.3 | 96.3 | 100.0 |
| 0.9 | 0.05 | 1023 | 37.4 | 580 of 960 | 95.3 | 96.3 | 100.0 |
| 0.9 | 0.1 | 1021 | 37.3 | 578 of 960 | 95.3 | 96.3 | 100.0 |
| 0.9 | 0.2 | 1021 | 37.3 | 578 of 960 | 95.3 | 96.3 | 100.0 |
| 0.95 | none | 1288 | 47.0 | 665 of 960 | 97.2 | 98.2 | 100.0 |
| 0.95 | 0.05 | 1288 | 47.0 | 665 of 960 | 97.2 | 98.2 | 100.0 |
| 0.95 | 0.1 | 1288 | 47.0 | 665 of 960 | 97.2 | 98.2 | 100.0 |
| 0.95 | 0.2 | 1288 | 47.0 | 665 of 960 | 97.2 | 98.2 | 100.0 |

## Evenki

| Evaluation | S (P/R/F1) | O (P/R/F1) | Role macro-F1 | Predicate F1 | Subordinate F1 | Zero-subject macro-F1 |
|---|---|---|---|---|---|---|
| dev, 5-fold nested CV | 81.8 / 85.5 / 83.6 | 83.3 / 79.8 / 81.5 | 82.5 | 93.7 | 64.1 | 84.7 |
| ... case-only rule baseline | 70.6 / 54.6 / 61.6 | 72.7 / 69.2 / 70.9 | 66.2 | | | |
| held-out texts | 83.0 / 85.2 / 84.1 | 82.4 / 81.8 / 82.1 | 83.1 | 93.5 | 62.8 | 82.5 |
| ... case-only rule baseline | 68.0 / 49.3 / 57.2 | 75.2 / 67.5 / 71.2 | 64.2 | | | |

Regularisation chosen in the nested folds: [0.3, 0.1, 0.3, 0.3, 0.1].

**Objects found, by case (dev CV):** ACC 851/935 (91.0%); NOM 4/113 (3.5%); other 126/181 (69.6%)

**Objects found, by case (held-out):** ACC 315/349 (90.3%); NOM 1/35 (2.9%); other 62/78 (79.5%)

**Calibration of P(object)** on nominals (dev CV): mean predicted vs observed share of objects.

| P(O) bin | Words | Mean predicted | Observed |
|---|---|---|---|
| 0.0 | 4847 | 0.01 | 0.02 |
| 0.1 | 264 | 0.14 | 0.14 |
| 0.2 | 104 | 0.25 | 0.28 |
| 0.3 | 77 | 0.35 | 0.35 |
| 0.4 | 51 | 0.45 | 0.41 |
| 0.5 | 80 | 0.55 | 0.65 |
| 0.6 | 117 | 0.65 | 0.67 |
| 0.7 | 146 | 0.76 | 0.79 |
| 0.8 | 275 | 0.86 | 0.90 |
| 0.9 | 467 | 0.95 | 0.91 |

**Review routing (dev CV).** A nominal is flagged if the model's top probability is below the threshold, or if it is unmarked and P(O) is at least the floor. Scores assume a human corrects every flagged word.

| Threshold | Unmarked-object floor | Flagged words | Share of nominals | Utterances to review | S F1 after review | O F1 after review | Unmarked objects found |
|---|---|---|---|---|---|---|---|
| 0.7 | none | 1125 | 17.5 | 901 of 3012 | 90.4 | 88.7 | 47.8 |
| 0.7 | 0.05 | 1363 | 21.2 | 1054 of 3012 | 91.3 | 90.0 | 74.3 |
| 0.7 | 0.1 | 1191 | 18.5 | 942 of 3012 | 90.7 | 89.1 | 55.8 |
| 0.7 | 0.2 | 1127 | 17.5 | 902 of 3012 | 90.4 | 88.7 | 48.7 |
| 0.8 | none | 1797 | 28.0 | 1289 of 3012 | 92.8 | 91.5 | 67.3 |
| 0.8 | 0.05 | 1908 | 29.7 | 1352 of 3012 | 93.2 | 92.1 | 77.9 |
| 0.8 | 0.1 | 1816 | 28.3 | 1298 of 3012 | 92.9 | 91.5 | 67.3 |
| 0.8 | 0.2 | 1797 | 28.0 | 1289 of 3012 | 92.8 | 91.5 | 67.3 |
| 0.9 | none | 2845 | 44.3 | 1779 of 3012 | 94.9 | 93.8 | 80.5 |
| 0.9 | 0.05 | 2864 | 44.6 | 1788 of 3012 | 95.0 | 94.0 | 83.2 |
| 0.9 | 0.1 | 2845 | 44.3 | 1779 of 3012 | 94.9 | 93.8 | 80.5 |
| 0.9 | 0.2 | 2845 | 44.3 | 1779 of 3012 | 94.9 | 93.8 | 80.5 |
| 0.95 | none | 3792 | 59.0 | 2175 of 3012 | 96.1 | 95.6 | 90.3 |
| 0.95 | 0.05 | 3792 | 59.0 | 2175 of 3012 | 96.1 | 95.6 | 90.3 |
| 0.95 | 0.1 | 3792 | 59.0 | 2175 of 3012 | 96.1 | 95.6 | 90.3 |
| 0.95 | 0.2 | 3792 | 59.0 | 2175 of 3012 | 96.1 | 95.6 | 90.3 |

**Review routing (held-out texts).** A nominal is flagged if the model's top probability is below the threshold, or if it is unmarked and P(O) is at least the floor. Scores assume a human corrects every flagged word.

| Threshold | Unmarked-object floor | Flagged words | Share of nominals | Utterances to review | S F1 after review | O F1 after review | Unmarked objects found |
|---|---|---|---|---|---|---|---|
| 0.7 | none | 405 | 17.2 | 332 of 1071 | 90.5 | 89.2 | 42.9 |
| 0.7 | 0.05 | 489 | 20.8 | 386 of 1071 | 91.2 | 89.9 | 60.0 |
| 0.7 | 0.1 | 431 | 18.3 | 347 of 1071 | 90.7 | 89.7 | 54.3 |
| 0.7 | 0.2 | 406 | 17.2 | 333 of 1071 | 90.5 | 89.2 | 42.9 |
| 0.8 | none | 617 | 26.2 | 449 of 1071 | 92.9 | 91.3 | 54.3 |
| 0.8 | 0.05 | 665 | 28.2 | 477 of 1071 | 93.0 | 91.6 | 60.0 |
| 0.8 | 0.1 | 623 | 26.5 | 451 of 1071 | 92.9 | 91.4 | 57.1 |
| 0.8 | 0.2 | 617 | 26.2 | 449 of 1071 | 92.9 | 91.3 | 54.3 |
| 0.9 | none | 1005 | 42.7 | 634 of 1071 | 95.0 | 94.1 | 68.6 |
| 0.9 | 0.05 | 1015 | 43.1 | 639 of 1071 | 95.0 | 94.1 | 68.6 |
| 0.9 | 0.1 | 1005 | 42.7 | 634 of 1071 | 95.0 | 94.1 | 68.6 |
| 0.9 | 0.2 | 1005 | 42.7 | 634 of 1071 | 95.0 | 94.1 | 68.6 |
| 0.95 | none | 1361 | 57.8 | 776 of 1071 | 95.8 | 95.1 | 77.1 |
| 0.95 | 0.05 | 1361 | 57.8 | 776 of 1071 | 95.8 | 95.1 | 77.1 |
| 0.95 | 0.1 | 1361 | 57.8 | 776 of 1071 | 95.8 | 95.1 | 77.1 |
| 0.95 | 0.2 | 1361 | 57.8 | 776 of 1071 | 95.8 | 95.1 | 77.1 |

## Transfer between languages (scored on the target's held-out texts)

| Training data | Role macro-F1 | S F1 | O F1 | Predicate F1 | Zero-subject macro-F1 |
|---|---|---|---|---|---|
| dolgan only -> evenki | 69.9 | 68.7 | 71.0 | 87.9 | 71.8 |
| evenki + dolgan plain -> evenki | 81.7 | 82.2 | 81.2 | 92.8 | 82.1 |
| evenki + dolgan augmented -> evenki | 81.8 | 83.2 | 80.4 | 93.4 | 81.6 |
| evenki only -> dolgan | 62.9 | 58.4 | 67.4 | 77.9 | 74.0 |
| dolgan + evenki plain -> dolgan | 74.2 | 69.2 | 79.3 | 86.7 | 77.0 |
| dolgan + evenki augmented -> dolgan | 75.5 | 70.2 | 80.8 | 87.3 | 77.1 |

## How much tagged text does a language need? (held-out role macro-F1; mean of 3 random draws below 100%)

| Language | Share of dev texts | Texts | Alone | + other language | + other language, augmented |
|---|---|---|---|---|---|
| dolgan | 0.1 | 4 | 63.9 | 66.5 | 66.7 |
| dolgan | 0.25 | 10 | 70.0 | 69.6 | 69.5 |
| dolgan | 0.5 | 20 | 73.3 | 73.2 | 72.7 |
| dolgan | 1.0 | 40 | 75.3 | n/a | n/a |
| evenki | 0.1 | 10 | 72.2 | 74.6 | 73.3 |
| evenki | 0.25 | 26 | 78.9 | 78.2 | 78.5 |
| evenki | 0.5 | 52 | 82.1 | 80.4 | 81.1 |
| evenki | 1.0 | 105 | 83.1 | n/a | n/a |

## Unseen speakers (speaker-disjoint 5-fold CV on all tagged texts, C = 0.3)

No speaker is in both training and test. The held-out texts above share speakers with training.

| Language | S (P/R/F1) | O (P/R/F1) | Role macro-F1 | Predicate F1 | Zero-subject macro-F1 |
|---|---|---|---|---|---|
| dolgan | 73.2 / 67.1 / 70.0 | 80.6 / 76.6 / 78.5 | 74.3 | 86.9 | 76.9 |
| evenki | 81.9 / 83.6 / 82.8 | 82.2 / 78.0 / 80.1 | 81.4 | 93.7 | 84.3 |

**Dolgan, unseen speakers, by birth group:**

| Birth group | Speakers | S F1 | O F1 | Unmarked objects found |
|---|---|---|---|---|
| -1919 | 5 | 71.0 | 81.9 | 8/18 |
| 1920-1939 | 11 | 66.2 | 76.4 | 46/119 |
| 1940-1959 | 3 | 69.0 | 80.7 | 5/11 |
| 1960- | 6 | 67.0 | 83.8 | 14/29 |
| unknown | 9 | 77.5 | 77.3 | 9/39 |

## Glosser (held-out texts)

| Language | Words | Kind | Share | Exact gloss | Part of speech | Case |
|---|---|---|---|---|---|---|
| dolgan | 17871 | all | 100.0 | 71.5 | 87.1 | 82.0 |
| dolgan | 7937 | known | 44.4 | 93.8 | 98.1 | 97.3 |
| dolgan | 6285 | ambiguous | 35.2 | 75.3 | 88.4 | 81.4 |
| dolgan | 3649 | ending | 20.4 | 16.5 | 60.9 | 54.8 |
| evenki | 25120 | all | 100.0 | 66.0 | 84.5 | 80.0 |
| evenki | 13168 | known | 52.4 | 95.3 | 98.5 | 98.0 |
| evenki | 3507 | ambiguous | 14.0 | 73.8 | 89.1 | 86.1 |
| evenki | 8442 | ending | 33.6 | 17.1 | 60.7 | 47.3 |
| evenki | 3 | none | 0.0 | 0.0 | 0.0 | 0.0 |
