# Study B2: power of the speaker-level trend test

Built by `case_change/power.py` from the design alone: speakers with a usable birth year and at least 3 objects, and their object counts. The outcome was not read.

Speakers: 25. Objects: 997. Birth years 1900 to 2000. Baseline accusative share (input): 0.8. Simulations per cell: 200, alpha 0.05, two-sided permutation test.

Effect sizes are odds ratios per decade of birth year. For orientation, an odds ratio of 1.5 per decade over 50 years moves a share of 0.80 to about 0.97 or 0.35, depending on direction.

| Odds ratio per decade | Power, speaker SD 0.5 | Power, speaker SD 1.0 |
|---|---|---|
| 1.0 | 0.09 | 0.09 |
| 1.2 | 0.82 | 0.46 |
| 1.35 | 0.99 | 0.79 |
| 1.5 | 1.00 | 0.93 |
| 1.75 | 1.00 | 0.99 |
| 2.0 | 1.00 | 1.00 |

Row 1.0 is the false-positive rate and should be near 0.05. Speaker SD is the between-speaker spread on the log-odds scale. It is unknown until the outcome is seen, so both values are shown. Report the smallest odds ratio with power of 0.8 or more in the paper.
