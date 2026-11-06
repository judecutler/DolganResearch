# Study B2: power of the speaker-level trend test

Built by `case_change/power.py` from the design alone: speakers with a usable birth year and at least 3 objects, and their object counts. The outcome was not read.

Speakers: 25. Objects: 997. Birth years 1900 to 2000. Baseline accusative share (input): 0.8. Simulations per cell: 200, alpha 0.05, two-sided wild cluster bootstrap (D-034).

Effect sizes are odds ratios per decade of birth year. For orientation, an odds ratio of 1.5 per decade over 50 years moves a share of 0.80 to about 0.97 or 0.35, depending on direction.

| Odds ratio per decade | Power, speaker SD 0.5 | Power, speaker SD 1.0 |
|---|---|---|
| 1.0 | 0.04 | 0.04 |
| 1.2 | 0.65 | 0.27 |
| 1.35 | 0.92 | 0.64 |
| 1.5 | 0.99 | 0.82 |
| 1.75 | 1.00 | 0.94 |
| 2.0 | 1.00 | 0.99 |

Row 1.0 is the false-positive rate and should be near 0.05. With 200 simulations per cell, a rate within about 0.03 of 0.05 is consistent with a correct test. Speaker SD is the between-speaker spread on the log-odds scale. It is unknown until the outcome is seen, so both values are shown. Report the smallest odds ratio with power of 0.8 or more in the paper.
