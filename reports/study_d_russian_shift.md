# Study D results: possible Russian-driven shifts by birth year

Built by `case_change/russian_shift.py` from the plan in `case_change/STUDY_D_PLAN.md`, committed before this run. Estimates are percentage points per decade of birth year; p from 9999 wild-cluster-bootstrap draws by speaker (999 for leave-one-out), seed 20261106. Holm correction over D1-D3; PC is a positive control, not corrected.

## Primary tests

| Hypothesis | Adjusted for | Speakers | Units | Change per decade (points) | p | Holm p | Verdict |
|---|---|---|---|---|---|---|---|
| D1: overt personal-pronoun subject (vs zero subject); predicted up | genre and source | 25 | 2454 | -2.07 | 0.1025 | 0.3075 | not supported (Holm p >= 0.05) |
| D2: PST2 among finite pasts (vs PST1); predicted down | genre and source | 59 | 7653 | +0.28 | 0.8183 | 0.8183 | not supported (Holm p >= 0.05) |
| D3: converb among lexical verbs; predicted down | genre and source | 60 | 20743 | +0.93 | 0.1052 | 0.3075 | not supported (Holm p >= 0.05) |
| PC: Russian-origin word among glossed words (positive control); predicted up | genre and source | 60 | 84766 | +0.11 | 0.7053 | n/a | no difference detected |

Decision rule (share of birth-year variance explained): D1 genre + source 0.55; D2 genre + source 0.47; D3 genre + source 0.53; PC genre + source 0.52.

## Secondary rows (not corrected)

| Row | Speakers | Units | Change per decade (points) | p | |
|---|---|---|---|---|---|
| D1, unadjusted | 25 | 2454 | -1.66 | 0.0887 |  |
| D1, recording year, adjusted | 24 | 2294 | -5.04 | 0.2916 |  |
| D2, unadjusted | 59 | 7653 | -3.55 | 0.0060 |  |
| D2, recording year, adjusted | 58 | 7433 | +2.98 | 0.3434 |  |
| D3, unadjusted | 60 | 20743 | -0.86 | 0.0216 |  |
| D3, recording year, adjusted | 59 | 20216 | -0.08 | 0.9129 |  |
| PC, unadjusted | 60 | 84766 | +1.36 | 0.0004 |  |
| PC, recording year, adjusted | 59 | 82676 | -0.80 | 0.2582 |  |

## Descriptive: D1, overt personal-pronoun subject (vs zero subject); predicted up

| Birth bin | Units | Outcome 1 | Share |
|---|---|---|---|
| -1919 | 580 | 70 | 12.1% |
| 1920-1939 | 1274 | 174 | 13.7% |
| 1940-1959 | 228 | 2 | 0.9% |
| 1960- | 372 | 22 | 5.9% |

| Speaker | Birth year | Units | Share |
|---|---|---|---|
| ChPK | 1900 | 57 | 17.5% |
| ErSV | 1900 | 113 | 23.9% |
| PoMA | 1914 | 40 | 5.0% |
| AnMS | 1914 | 44 | 20.5% |
| KiMN | 1915 | 326 | 6.7% |
| MiXS | 1920 | 34 | 47.1% |
| ChVD | 1923 | 133 | 3.8% |
| LaVN | 1924 | 151 | 19.9% |
| PoNA | 1929 | 164 | 20.1% |
| KiPP | 1932 | 146 | 16.4% |
| ChSA | 1934 | 68 | 5.9% |
| BeES | 1935 | 112 | 7.1% |
| AkEE | 1936 | 213 | 8.5% |
| AkNN | 1937 | 133 | 10.5% |
| NaLE | 1938 | 50 | 16.0% |
| ElBK | 1939 | 70 | 20.0% |
| SuAA | 1940 | 67 | 0.0% |
| PoS | 1948 | 62 | 1.6% |
| UoPP | 1954 | 99 | 1.0% |
| AnIM | 1960 | 28 | 0.0% |
| KuNS | 1965 | 141 | 5.7% |
| ChGS | 1967 | 156 | 3.8% |
| ZhNA | 1979 | 28 | 17.9% |
| AnKA | 1998 | 7 | 0.0% |
| KuDP | 2000 | 12 | 25.0% |

## Descriptive: D2, PST2 among finite pasts (vs PST1); predicted down

| Birth bin | Units | Outcome 1 | Share |
|---|---|---|---|
| -1919 | 2228 | 1632 | 73.2% |
| 1920-1939 | 3310 | 1963 | 59.3% |
| 1940-1959 | 1174 | 783 | 66.7% |
| 1960- | 941 | 410 | 43.6% |

| Speaker | Birth year | Units | Share |
|---|---|---|---|
| BoND | 1884 | 52 | 63.5% |
| SuKN | 1890 | 254 | 67.7% |
| ChPK | 1900 | 170 | 95.9% |
| ErSV | 1900 | 378 | 77.0% |
| ChuAE | 1904 | 23 | 82.6% |
| BeAM | 1913 | 382 | 60.2% |
| PoKK | 1914 | 230 | 83.5% |
| PoMA | 1914 | 132 | 43.2% |
| AnMS | 1914 | 53 | 24.5% |
| KiMN | 1915 | 234 | 85.5% |
| SaSS | 1916 | 75 | 80.0% |
| MiPP | 1919 | 78 | 65.4% |
| BeVP | 1920 | 167 | 90.4% |
| MiXS | 1920 | 63 | 63.5% |
| ChVD | 1923 | 79 | 34.2% |
| LaVN | 1924 | 175 | 47.4% |
| PoNA | 1929 | 801 | 83.1% |
| ErTS | 1931 | 65 | 40.0% |
| KiPP | 1932 | 311 | 65.9% |
| BeEI | 1933 | 148 | 22.3% |
| ChMI | 1934 | 199 | 57.3% |
| ChSA | 1934 | 31 | 58.1% |
| SuON | 1934 | 234 | 33.3% |
| BeES | 1935 | 132 | 68.2% |
| AkEE | 1936 | 264 | 65.2% |
| KiES | 1936 | 86 | 55.8% |
| AkNN | 1937 | 93 | 30.1% |
| BeSN | 1938 | 45 | 84.4% |
| NaLE | 1938 | 37 | 27.0% |
| UkET | 1938 | 133 | 69.9% |
| ElBK | 1939 | 95 | 26.3% |
| FeAP | 1939 | 41 | 34.1% |
| PoIP | 1940 | 278 | 55.8% |
| SuAA | 1940 | 13 | 84.6% |
| MiAI | 1940 | 260 | 93.8% |
| PoPD | 1942 | 129 | 48.8% |
| ChAP | 1946 | 41 | 51.2% |
| SoLK | 1946 | 273 | 33.0% |
| ChAPa | 1946 | 33 | 36.4% |
| PoS | 1948 | 151 | 87.4% |
| PrG | 1950 | 22 | 100.0% |
| ErAI | 1952 | 26 | 57.7% |
| UoPP | 1954 | 112 | 85.7% |
| KiLS | 1956 | 43 | 69.8% |
| AnSP | 1957 | 4 | 0.0% |
| ChNM | 1959 | 67 | 70.1% |
| AnIM | 1960 | 104 | 44.2% |
| KuNS | 1965 | 294 | 28.6% |
| ChGS | 1967 | 73 | 87.7% |
| PoTY | 1967 | 184 | 34.8% |
| UkOA | 1969 | 57 | 50.9% |
| KuSM | 1973 | 30 | 83.3% |
| ZhNA | 1979 | 25 | 60.0% |
| KuSE | 1994 | 43 | 62.8% |
| PoVV | 1997 | 2 | 0.0% |
| AnKA | 1998 | 24 | 29.2% |
| KuDP | 2000 | 70 | 42.9% |
| AnMSp | 2001 | 18 | 61.1% |
| PoKI | 2009 | 17 | 47.1% |

## Descriptive: D3, converb among lexical verbs; predicted down

| Birth bin | Units | Outcome 1 | Share |
|---|---|---|---|
| -1919 | 6473 | 1837 | 28.4% |
| 1920-1939 | 8531 | 2120 | 24.9% |
| 1940-1959 | 3235 | 850 | 26.3% |
| 1960- | 2504 | 550 | 22.0% |

| Speaker | Birth year | Units | Share |
|---|---|---|---|
| BoND | 1884 | 304 | 26.3% |
| SuKN | 1890 | 689 | 30.2% |
| ChPK | 1900 | 322 | 34.8% |
| ErSV | 1900 | 1203 | 23.4% |
| ChuAE | 1904 | 135 | 30.4% |
| BeAM | 1913 | 924 | 28.9% |
| PoKK | 1914 | 562 | 35.8% |
| PoMA | 1914 | 609 | 32.7% |
| AnMS | 1914 | 103 | 39.8% |
| KiMN | 1915 | 821 | 24.2% |
| SaSS | 1916 | 261 | 22.2% |
| MiPP | 1919 | 249 | 25.7% |
| BeVP | 1920 | 291 | 29.6% |
| MiXS | 1920 | 168 | 40.5% |
| ChVD | 1923 | 234 | 19.2% |
| LaVN | 1924 | 297 | 16.8% |
| PoNA | 1929 | 2151 | 28.1% |
| ErTS | 1931 | 228 | 25.9% |
| KiPP | 1932 | 1110 | 27.3% |
| BeEI | 1933 | 233 | 14.2% |
| ChMI | 1934 | 471 | 23.1% |
| ChSA | 1934 | 118 | 22.0% |
| SuON | 1934 | 395 | 12.2% |
| BeES | 1935 | 498 | 27.9% |
| AkEE | 1936 | 605 | 24.5% |
| KiES | 1936 | 235 | 24.3% |
| UKN | 1936 | 11 | 72.7% |
| AkNN | 1937 | 189 | 25.4% |
| BeSN | 1938 | 115 | 15.7% |
| NaLE | 1938 | 102 | 21.6% |
| UkET | 1938 | 495 | 36.2% |
| ElBK | 1939 | 126 | 11.1% |
| FeAP | 1939 | 127 | 17.3% |
| PoIP | 1940 | 623 | 19.3% |
| SuAA | 1940 | 296 | 29.7% |
| MiAI | 1940 | 587 | 39.7% |
| PoPD | 1942 | 151 | 13.2% |
| ChAP | 1946 | 411 | 25.8% |
| SoLK | 1946 | 638 | 14.4% |
| ChAPa | 1946 | 225 | 14.7% |
| PoS | 1948 | 273 | 39.9% |
| PrG | 1950 | 37 | 35.1% |
| ErAI | 1952 | 78 | 20.5% |
| UoPP | 1954 | 308 | 24.4% |
| KiLS | 1956 | 69 | 15.9% |
| AnSP | 1957 | 33 | 27.3% |
| ChNM | 1959 | 129 | 34.9% |
| AnIM | 1960 | 449 | 21.6% |
| KuNS | 1965 | 623 | 22.6% |
| ChGS | 1967 | 302 | 20.5% |
| PoTY | 1967 | 564 | 23.8% |
| UkOA | 1969 | 199 | 23.6% |
| KuSM | 1973 | 59 | 0.0% |
| ZhNA | 1979 | 49 | 24.5% |
| KuSE | 1994 | 88 | 20.5% |
| PoVV | 1997 | 17 | 47.1% |
| AnKA | 1998 | 36 | 13.9% |
| KuDP | 2000 | 66 | 13.6% |
| AnMSp | 2001 | 31 | 29.0% |
| PoKI | 2009 | 21 | 38.1% |

## Descriptive: PC, Russian-origin word among glossed words (positive control); predicted up

| Birth bin | Units | Outcome 1 | Share |
|---|---|---|---|
| -1919 | 22374 | 631 | 2.8% |
| 1920-1939 | 37824 | 3885 | 10.3% |
| 1940-1959 | 13027 | 1316 | 10.1% |
| 1960- | 11541 | 1336 | 11.6% |

| Speaker | Birth year | Units | Share |
|---|---|---|---|
| BoND | 1884 | 1029 | 0.0% |
| SuKN | 1890 | 2143 | 4.4% |
| ChPK | 1900 | 1124 | 1.3% |
| ErSV | 1900 | 3878 | 0.0% |
| ChuAE | 1904 | 477 | 0.0% |
| BeAM | 1913 | 4008 | 4.4% |
| PoKK | 1914 | 1730 | 0.0% |
| PoMA | 1914 | 2006 | 0.3% |
| AnMS | 1914 | 599 | 15.7% |
| KiMN | 1915 | 2801 | 6.4% |
| SaSS | 1916 | 848 | 0.9% |
| MiPP | 1919 | 745 | 2.8% |
| BeVP | 1920 | 986 | 3.8% |
| MiXS | 1920 | 941 | 12.9% |
| ChVD | 1923 | 898 | 14.1% |
| LaVN | 1924 | 1719 | 15.2% |
| PoNA | 1929 | 8298 | 9.1% |
| ErTS | 1931 | 1119 | 14.0% |
| KiPP | 1932 | 4732 | 9.4% |
| BeEI | 1933 | 1366 | 17.9% |
| ChMI | 1934 | 2030 | 12.3% |
| ChSA | 1934 | 510 | 8.0% |
| SuON | 1934 | 2078 | 15.6% |
| BeES | 1935 | 2360 | 7.2% |
| AkEE | 1936 | 2109 | 3.1% |
| KiES | 1936 | 1170 | 7.1% |
| UKN | 1936 | 30 | 10.0% |
| AkNN | 1937 | 900 | 12.8% |
| BeSN | 1938 | 488 | 24.6% |
| NaLE | 1938 | 451 | 3.8% |
| UkET | 1938 | 1877 | 5.2% |
| ElBK | 1939 | 864 | 12.7% |
| FeAP | 1939 | 480 | 19.2% |
| PoIP | 1940 | 3404 | 8.4% |
| SuAA | 1940 | 1112 | 4.0% |
| MiAI | 1940 | 1649 | 0.0% |
| PoPD | 1942 | 1014 | 20.8% |
| ChAP | 1946 | 1756 | 12.1% |
| SoLK | 1946 | 2666 | 20.0% |
| ChAPa | 1946 | 1191 | 6.5% |
| PoS | 1948 | 803 | 1.1% |
| PrG | 1950 | 168 | 1.8% |
| ErAI | 1952 | 399 | 6.0% |
| UoPP | 1954 | 1050 | 8.6% |
| KiLS | 1956 | 434 | 12.9% |
| AnSP | 1957 | 133 | 6.8% |
| ChNM | 1959 | 652 | 7.1% |
| AnIM | 1960 | 2042 | 10.7% |
| KuNS | 1965 | 3469 | 12.3% |
| ChGS | 1967 | 1228 | 9.9% |
| PoTY | 1967 | 2017 | 8.1% |
| UkOA | 1969 | 1158 | 14.2% |
| KuSM | 1973 | 200 | 7.5% |
| ZhNA | 1979 | 285 | 15.1% |
| KuSE | 1994 | 319 | 13.2% |
| PoVV | 1997 | 42 | 0.0% |
| AnKA | 1998 | 143 | 10.5% |
| KuDP | 2000 | 412 | 22.3% |
| AnMSp | 2001 | 110 | 20.0% |
| PoKI | 2009 | 116 | 11.2% |
