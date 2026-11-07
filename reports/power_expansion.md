# Study B: would the expansion add power? (design only)

Built by `case_change/power_expansion.py`. Expected new objects per speaker and text = sum of the tagger's P(object) over nominals in the untagged texts (the model is calibrated). No case value was read. Test: birth year adjusted for genre and source (source only within one genre); baseline accusative share 0.8 (an input); 200 simulations per cell; wild cluster bootstrap by speaker.

| Design | Speakers with a birth year | Objects | Birth-year variance explained by controls | Power OR 1.5, SD 0.5 | OR 1.5, SD 1.0 | OR 2.0, SD 0.5 | OR 2.0, SD 1.0 |
|---|---|---|---|---|---|---|---|
| current, all genres | 25 | 997 | 0.60 | 0.83 | 0.42 | 0.98 | 0.80 |
| current + expanded, all genres | 59 | 3569 | 0.57 | 1.00 | 0.88 | 1.00 | 0.99 |
| current + expanded, narrative only | 33 | 1497 | 0.41 | 0.95 | 0.58 | 1.00 | 0.91 |
| current + expanded, conversation only | 19 | 741 | 0.18 | 0.68 | 0.34 | 0.94 | 0.64 |
| current, narrative only | 10 | 294 | 0.71 | 0.28 | 0.17 | 0.51 | 0.27 |

Within one genre the controls are source only. Speakers with a birth-year range over 10 years are left out, as in B2.
