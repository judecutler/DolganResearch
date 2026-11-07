# Study B2 results: object case by time

Built by `case_change/b2_test.py` after the analysis plan was frozen. Each row is a speaker-clustered regression of the outcome on time; the estimate is the change in the outcome share in percentage points per decade; p is from 9999 wild-cluster-bootstrap draws by speaker (999 for leave-one-out rows) (D-034, D-037).

Decision rule (B2): birth-year variance explained by genre + source 0.59. Primary test adjusts for genre and source.

Decision rule (B3): birth-year variance explained by genre + source 0.58. Primary test adjusts for genre and source.

## Primary and secondary tests

| Analysis | Speakers | Objects | Change per decade (points) | p |
|---|---|---|---|---|
| PRIMARY: ACC, birth year, adjusted for genre and source | 25 | 985 | +0.7 | 0.800 |
| ACC, birth year, unadjusted | 25 | 985 | -1.3 | 0.171 |
| ACC, birth year, adjusted for genre only | 25 | 985 | +0.4 | 0.688 |
| ACC, recording year (real time), adjusted for genre and source | 24 | 915 | -4.8 | 0.394 |
| PART, birth year, adjusted for genre and source | 25 | 985 | -0.1 | 0.834 |
| ACC, birth year, adjusted for genre, source and clause TAM group | 25 | 985 | +0.6 | 0.822 |

## Robustness checks (primary model, adjusted for genre and source)

| Analysis | Speakers | Objects | Change per decade (points) | p |
|---|---|---|---|---|
| Native nouns only (no BOR tag) | 25 | 759 | +1.3 | 0.465 |
| No pronoun objects | 25 | 805 | +1.6 | 0.584 |
| Aligned, no % glosses | 25 | 985 | +0.7 | 0.797 |
| Exact birth years only | 20 | 813 | +0.9 | 0.812 |
| Without Anabar | 24 | 981 | +1.2 | 0.657 |
| Source TDNT_archive only | 16 | 729 | +2.3 | 0.549 |
| Source fieldwork_2007_2010 only | 3 | 41 | too few speakers | |
| Source fieldwork_2017 only | 2 | 85 | too few speakers | |
| Source published_folklore only | 4 | 130 | too few speakers | |

## B3: word order (verb before object), utterances with one predicate

| Analysis | Speakers | Objects | Change per decade (points) | p |
|---|---|---|---|---|
| B3 PRIMARY: VO, birth year, adjusted for genre and source | 24 | 497 | -1.3 | 0.434 |
| B3: VO, birth year, unadjusted | 24 | 497 | -2.1 | 0.192 |
| B3: VO, recording year, adjusted for genre and source | 23 | 458 | -0.9 | 0.694 |
| B3: VO, no pronoun objects | 24 | 410 | -0.8 | 0.599 |

## Leave one speaker out (primary model, adjusted for genre and source)

| Speaker left out | Speakers | Objects | Change per decade (points) | p |
|---|---|---|---|---|
| AkEE | 24 | 881 | +0.6 | 0.827 |
| AkNN | 24 | 941 | +0.8 | 0.793 |
| AnIM | 24 | 956 | +1.5 | 0.573 |
| AnKA | 24 | 981 | +1.2 | 0.665 |
| AnMS | 24 | 973 | +1.0 | 0.723 |
| BeES | 24 | 910 | +1.5 | 0.513 |
| ChGS | 24 | 931 | +0.8 | 0.752 |
| ChPK | 24 | 942 | +0.5 | 0.855 |
| ChSA | 24 | 966 | +0.6 | 0.815 |
| ChVD | 24 | 960 | +0.7 | 0.792 |
| ElBK | 24 | 955 | +0.7 | 0.804 |
| ErSV | 24 | 941 | +0.9 | 0.765 |
| KiMN | 24 | 924 | +0.6 | 0.871 |
| KiPP | 24 | 937 | +0.3 | 0.895 |
| KuDP | 24 | 977 | +0.8 | 0.767 |
| KuNS | 24 | 932 | -1.4 | 0.385 |
| LaVN | 24 | 933 | +0.3 | 0.891 |
| MiXS | 24 | 960 | +1.1 | 0.683 |
| NaLE | 24 | 958 | +0.7 | 0.822 |
| PoMA | 24 | 963 | +0.7 | 0.797 |
| PoNA | 24 | 873 | +0.8 | 0.770 |
| PoS | 24 | 964 | +0.9 | 0.792 |
| SuAA | 24 | 951 | +0.4 | 0.880 |
| UoPP | 24 | 954 | +0.8 | 0.757 |
| ZhNA | 24 | 977 | +0.7 | 0.824 |

## Real-time panel: speakers with objects in two or more recording years (descriptive)

| Speaker | Recording year | NOM | ACC | PART |
|---|---|---|---|---|
| PoNA | 1991 | 10 | 50 | 0 |
| PoNA | 1994 | 0 | 35 | 0 |
| PoNA | 2004 | 0 | 17 | 0 |

## Descriptive tables (not tests)


| Birth bin | NOM | ACC | PART | ACC share |
|---|---|---|---|---|
| -1919 | 18 | 157 | 7 | 86.3% |
| 1920-1939 | 119 | 439 | 3 | 78.3% |
| 1940-1959 | 11 | 73 | 2 | 84.9% |
| 1960- | 29 | 124 | 3 | 79.5% |

| Recording bin | NOM | ACC | PART | ACC share |
|---|---|---|---|---|
| -1979 | 14 | 148 | 5 | 88.6% |
| 1980-1999 | 73 | 287 | 3 | 79.1% |
| 2000- | 82 | 298 | 5 | 77.4% |
| imprecise | 8 | 60 | 2 | 85.7% |

| Birth bin, genre | NOM | ACC | PART | ACC share |
|---|---|---|---|---|
| -1919, flk | 18 | 145 | 7 | 85.3% |
| -1919, nar | 0 | 12 | 0 | 100.0% |
| 1920-1939, conv | 61 | 132 | 0 | 68.4% |
| 1920-1939, flk | 13 | 115 | 2 | 88.5% |
| 1920-1939, nar | 45 | 157 | 1 | 77.3% |
| 1920-1939, transl | 0 | 35 | 0 | 100.0% |
| 1940-1959, conv | 7 | 23 | 1 | 74.2% |
| 1940-1959, flk | 3 | 18 | 0 | 85.7% |
| 1940-1959, nar | 1 | 32 | 1 | 94.1% |
| 1960-, conv | 21 | 91 | 3 | 79.1% |
| 1960-, nar | 8 | 33 | 0 | 80.5% |

Per-speaker accusative shares are plotted in `b2_results_speakers.svg` (circle area = objects).

| Speaker | Birth year | Objects | ACC share |
|---|---|---|---|
| ChPK | 1900 | 43 | 81.4% |
| ErSV | 1900 | 44 | 88.6% |
| PoMA | 1914 | 22 | 86.4% |
| AnMS | 1914 | 12 | 100.0% |
| KiMN | 1915 | 61 | 85.2% |
| MiXS | 1920 | 25 | 100.0% |
| ChVD | 1923 | 25 | 84.0% |
| LaVN | 1924 | 52 | 67.3% |
| PoNA | 1929 | 112 | 91.1% |
| KiPP | 1932 | 48 | 60.4% |
| ChSA | 1934 | 19 | 57.9% |
| BeES | 1935 | 75 | 57.3% |
| AkEE | 1936 | 104 | 88.5% |
| AkNN | 1937 | 44 | 79.5% |
| NaLE | 1938 | 27 | 88.9% |
| ElBK | 1939 | 30 | 73.3% |
| SuAA | 1940 | 34 | 94.1% |
| PoS | 1948 | 21 | 85.7% |
| UoPP | 1954 | 31 | 74.2% |
| AnIM | 1960 | 29 | 89.7% |
| KuNS | 1965 | 53 | 88.7% |
| ChGS | 1967 | 54 | 70.4% |
| ZhNA | 1979 | 8 | 75.0% |
| AnKA | 1998 | 4 | 25.0% |
| KuDP | 2000 | 8 | 75.0% |
