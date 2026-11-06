# Study B2: design and power

Built by `case_change/power.py` from design columns only (speaker, birth and recording years, genre, source). The outcome was not read. Every simulated effect is an odds ratio per decade; baseline accusative share 0.8 (an input); 200 simulations per cell; alpha 0.05; wild cluster bootstrap by speaker (D-034). Row 1.0 is the false-positive rate: within about 0.03 of 0.05 is consistent with a correct test. Speaker SD is the between-speaker spread on the log-odds scale, unknown until the outcome is seen. The simulations give genre and source no effect of their own; with such an effect, only the adjusted tests keep their false-positive rate (D-037).

## How tangled is time with genre and source?

Share of the object-weighted variance of the time variable explained by the controls. 0 means independent, 1 means time cannot be told apart from them. Above about 0.8 an adjusted test has little information left.

| Time variable | Controls | Speakers | Objects | Explained |
|---|---|---|---|---|
| birth year | genre | 25 | 997 | 0.27 |
| birth year | genre + source | 25 | 997 | 0.60 |
| recording year | genre | 24 | 927 | 0.49 |
| recording year | genre + source | 24 | 927 | 0.83 |

## Power, time = birth year

| Odds ratio per decade | none, SD 0.5 | none, SD 1.0 | genre, SD 0.5 | genre, SD 1.0 | genre + source, SD 0.5 | genre + source, SD 1.0 |
|---|---|---|---|---|---|---|
| 1.0 | 0.05 | 0.06 | 0.05 | 0.04 | 0.03 | 0.03 |
| 1.2 | 0.67 | 0.26 | 0.56 | 0.21 | 0.30 | 0.11 |
| 1.35 | 0.96 | 0.51 | 0.92 | 0.48 | 0.66 | 0.29 |
| 1.5 | 0.99 | 0.82 | 1.00 | 0.72 | 0.82 | 0.41 |
| 2.0 | 1.00 | 0.99 | 1.00 | 0.98 | 0.98 | 0.78 |

## Power, time = recording year

| Odds ratio per decade | none, SD 0.5 | none, SD 1.0 | genre, SD 0.5 | genre, SD 1.0 | genre + source, SD 0.5 | genre + source, SD 1.0 |
|---|---|---|---|---|---|---|
| 1.0 | 0.05 | 0.04 | 0.04 | 0.04 | 0.01 | 0.02 |
| 1.2 | 0.45 | 0.20 | 0.28 | 0.12 | 0.12 | 0.05 |
| 1.35 | 0.85 | 0.45 | 0.66 | 0.30 | 0.24 | 0.10 |
| 1.5 | 0.97 | 0.68 | 0.86 | 0.50 | 0.41 | 0.20 |
| 2.0 | 1.00 | 0.97 | 1.00 | 0.88 | 0.78 | 0.47 |

## B3 (word order): design and power, birth year adjusted for genre and source

Objects in utterances with one predicate: 496 from 23 speakers; birth-year variance explained by genre and source: 0.57. Assumed VO share (input): 0.2.

| Odds ratio per decade | SD 0.5 | SD 1.0 |
|---|---|---|
| 1.0 | 0.03 | 0.05 |
| 1.2 | 0.20 | 0.11 |
| 1.35 | 0.49 | 0.27 |
| 1.5 | 0.79 | 0.43 |
| 2.0 | 0.98 | 0.79 |

Report in the paper the smallest odds ratio with power 0.8 or more for the test the frozen plan names as primary.
