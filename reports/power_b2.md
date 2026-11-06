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
| 1.0 | 0.04 | 0.01 | 0.06 | 0.04 | 0.06 | 0.03 |
| 1.2 | 0.66 | 0.29 | 0.62 | 0.26 | 0.34 | 0.18 |
| 1.35 | 0.95 | 0.62 | 0.91 | 0.59 | 0.60 | 0.30 |
| 1.5 | 0.99 | 0.81 | 0.97 | 0.79 | 0.83 | 0.42 |
| 2.0 | 1.00 | 0.99 | 1.00 | 0.97 | 0.98 | 0.80 |

## Power, time = recording year

| Odds ratio per decade | none, SD 0.5 | none, SD 1.0 | genre, SD 0.5 | genre, SD 1.0 | genre + source, SD 0.5 | genre + source, SD 1.0 |
|---|---|---|---|---|---|---|
| 1.0 | 0.07 | 0.05 | 0.07 | 0.06 | 0.06 | 0.04 |
| 1.2 | 0.41 | 0.17 | 0.27 | 0.16 | 0.12 | 0.07 |
| 1.35 | 0.86 | 0.40 | 0.64 | 0.31 | 0.24 | 0.12 |
| 1.5 | 0.98 | 0.66 | 0.83 | 0.45 | 0.38 | 0.17 |
| 2.0 | 1.00 | 0.98 | 1.00 | 0.84 | 0.78 | 0.38 |

## B3 (word order): design and power, birth year adjusted for genre and source

Objects in utterances with one predicate: 497 from 24 speakers; birth-year variance explained by genre and source: 0.58. Assumed VO share (input): 0.2.

| Odds ratio per decade | SD 0.5 | SD 1.0 |
|---|---|---|
| 1.0 | 0.06 | 0.06 |
| 1.2 | 0.23 | 0.10 |
| 1.35 | 0.55 | 0.25 |
| 1.5 | 0.77 | 0.44 |
| 2.0 | 0.98 | 0.82 |

Report in the paper the smallest odds ratio with power 0.8 or more for the test the frozen plan names as primary.
