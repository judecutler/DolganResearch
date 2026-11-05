# Gate 0: feasibility

Built by `shared/gate0.py`. Design counts only; outcomes by cohort stay hidden until Gate 3. Decades are a provisional binning for counting (D-013 sets the real bins).

## Summary

| Check | Value | Result |
|---|---|---|
| At least 15 speakers with a usable birth year | 60 | PASS |
| At least 3 provisional cohorts with 5 or more speakers | 5 | PASS |
| At least 200 objects from speakers with a usable birth year | 997 | PASS |
| Objects come from at least 15 such speakers | 25 | PASS |
| No speaker gives more than 25% of objects | 11% | PASS |
| B1: at least 30 candidates from at least 10 speakers (before vetting) | 878 from 67 | PASS |

## Dolgan

### Speakers and birth years

77 speakers appear in transcripts. Birth-year precision: date 16, decade 2, range 15, unknown 17, year 27. Usable (range of 10 years or less): **60**, of which 2 are decades or marked uncertain (a robustness check drops them).

| Birth decade (provisional) | Speakers | Tokens |
|---|---|---|
| 1880s | 2 | 3176 |
| 1890s | 2 | 5012 |
| 1900s | 1 | 478 |
| 1910s | 8 | 13816 |
| 1920s | 4 | 12260 |
| 1930s | 17 | 27437 |
| 1940s | 8 | 10719 |
| 1950s | 5 | 3062 |
| 1960s | 5 | 10861 |
| 1970s | 2 | 494 |
| 1990s | 3 | 551 |
| 2000s | 3 | 664 |

### Are birth cohort, source, genre and recording date tangled?

Counts are (speaker, text) pairs. If each cohort sits in one source or genre, a cohort effect cannot be told apart from a source or genre effect.

| birth \ source (inferred) | TDNT_archive | fieldwork_2007_2010 | fieldwork_2017 | published_folklore | total |
|---|---|---|---|---|---|
| 1880s | . | . | . | 2 | 2 |
| 1890s | . | . | . | 6 | 6 |
| 1900s | . | . | . | 1 | 1 |
| 1910s | 6 | . | . | 7 | 13 |
| 1920s | 18 | . | . | . | 18 |
| 1930s | 20 | 18 | . | . | 38 |
| 1940s | 4 | 3 | . | 4 | 11 |
| 1950s | . | 8 | 4 | . | 12 |
| 1960s | 14 | 12 | 4 | . | 30 |
| 1970s | 1 | 1 | . | . | 2 |
| 1990s | . | 5 | . | . | 5 |
| 2000s | . | 4 | . | . | 4 |

| birth \ genre | conv | flk | misc | nar | sng | transl | total |
|---|---|---|---|---|---|---|---|
| 1880s | . | 2 | . | . | . | . | 2 |
| 1890s | . | 6 | . | . | . | . | 6 |
| 1900s | . | 1 | . | . | . | . | 1 |
| 1910s | . | 10 | . | 3 | . | . | 13 |
| 1920s | 2 | 2 | . | 10 | . | 4 | 18 |
| 1930s | 9 | 7 | 1 | 21 | . | . | 38 |
| 1940s | 1 | 4 | 1 | 5 | . | . | 11 |
| 1950s | 3 | . | . | 9 | . | . | 12 |
| 1960s | 16 | . | . | 13 | 1 | . | 30 |
| 1970s | 1 | . | . | 1 | . | . | 2 |
| 1990s | . | . | . | 4 | 1 | . | 5 |
| 2000s | 1 | . | . | 3 | . | . | 4 |

| birth \ recording decade | 1930s | 1960s | 1970s | 1980s | 1990s | 2000s | 2010s | imprecise | total |
|---|---|---|---|---|---|---|---|---|---|
| 1880s | 1 | 1 | . | . | . | . | . | . | 2 |
| 1890s | . | 4 | 2 | . | . | . | . | . | 6 |
| 1900s | . | 1 | . | . | . | . | . | . | 1 |
| 1910s | . | 5 | 4 | . | 4 | . | . | . | 13 |
| 1920s | . | 1 | 1 | 1 | 12 | 3 | . | . | 18 |
| 1930s | . | . | . | 1 | 10 | 25 | 1 | 1 | 38 |
| 1940s | . | 4 | . | . | . | 7 | . | . | 11 |
| 1950s | . | . | . | . | . | 8 | 4 | . | 12 |
| 1960s | . | . | . | . | 4 | 18 | 5 | 3 | 30 |
| 1970s | . | . | . | . | . | 1 | . | 1 | 2 |
| 1990s | . | . | . | . | . | 5 | . | . | 5 |
| 2000s | . | . | . | . | . | 4 | . | . | 4 |

### `SyF` coverage (Study B needs it to find objects)

`SyF` is non-empty in 50 of 136 texts. Speakers in those texts: 34, of whom 25 have a usable birth year.

| source \ genre (texts with SyF) | conv | flk | nar | transl | total |
|---|---|---|---|---|---|
| TDNT_archive | 6 | 9 | 8 | 4 | 27 |
| fieldwork_2007_2010 | . | . | 3 | . | 3 |
| fieldwork_2017 | 2 | . | . | . | 2 |
| published_folklore | . | 18 | . | . | 18 |

### Study B objects (counts only, no case by cohort)

1307 objects in total; 997 from 25 speakers with a usable birth year. Largest single-speaker share: 11%. Speakers with 20 or more objects: 20.

| Birth decade (provisional) | Speakers with objects | Objects |
|---|---|---|
| 1880s | 0 | 0 |
| 1890s | 2 | 89 |
| 1900s | 0 | 0 |
| 1910s | 3 | 96 |
| 1920s | 4 | 216 |
| 1930s | 7 | 352 |
| 1940s | 2 | 55 |
| 1950s | 1 | 33 |
| 1960s | 3 | 136 |
| 1970s | 1 | 8 |
| 1990s | 1 | 4 |
| 2000s | 1 | 8 |

Objects by source (all speakers): TDNT_archive 887, published_folklore 292, fieldwork_2017 87, fieldwork_2007_2010 41.
Objects by clause TAM group (draft grouping in `config.TAM_GROUPS`): past 524, present_habitual 493, no predicate 99, prospective 84, imperative 81, other 23, inferential 3.
Objects with a `BOR` value (possible loans, a confounder for zero marking): 298. With no predicate found in the utterance: 95.

### Study B1 (secondary predicates): candidates for human vetting

No tag marks secondary predicates (D-021). `case_change/extract_b1.py` applies rules built from Siegl (2015)'s examples. Counts are by rule, source and recording decade only, not by case, because case is the B1 outcome. Candidates: 878, from 67 speakers (55 with a usable birth year).

| rule \ source | TDNT_archive | fieldwork_2007_2010 | fieldwork_2017 | published_folklore | total |
|---|---|---|---|---|---|
| copula_next | 154 | 79 | 1 | 39 | 273 |
| ins_nominal | 294 | 154 | 2 | 148 | 598 |
| syf_pred | 4 | . | 2 | 1 | 7 |

| rule \ recording decade | 1930s | 1960s | 1970s | 1980s | 1990s | 2000s | 2010s | imprecise | total |
|---|---|---|---|---|---|---|---|---|---|
| copula_next | 14 | 24 | 11 | 3 | 85 | 122 | 3 | 11 | 273 |
| ins_nominal | 33 | 100 | 34 | . | 201 | 185 | 23 | 22 | 598 |
| syf_pred | . | 1 | . | . | 3 | 1 | 2 | . | 7 |

### Study A candidates

| Rule (first rule that found it) | Tier | Words | Speakers | From speakers with usable birth year |
|---|---|---|---|---|
| `ge_EVID` | 1 | 53 | 25 | 50 |
| `ge_INFER` | 1 | 36 | 15 | 29 |
| `IST_quot` | 2 | 260 | 21 | 138 |
| `copula_BIT` | 2 | 424 | 53 | 381 |
| `mp_BIT` | 2 | 5538 | 73 | 4960 |
| `mp_TAK_not_INFER` | 2 | 632 | 60 | 553 |
| `particle_buollaga` | 2 | 254 | 32 | 233 |

By genre: `IST_quot` conv 32; `IST_quot` flk 169; `IST_quot` nar 55; `IST_quot` transl 4; `copula_BIT` conv 51; `copula_BIT` flk 217; `copula_BIT` nar 149; `copula_BIT` transl 7; `ge_EVID` conv 19; `ge_EVID` flk 13; `ge_EVID` nar 21; `ge_INFER` conv 4; `ge_INFER` flk 28; `ge_INFER` nar 4; `mp_BIT` conv 801; `mp_BIT` flk 2753; `mp_BIT` misc 1; `mp_BIT` nar 1916; `mp_BIT` sng 2; `mp_BIT` transl 65; `mp_TAK_not_INFER` conv 78; `mp_TAK_not_INFER` flk 262; `mp_TAK_not_INFER` misc 1; `mp_TAK_not_INFER` nar 289; `mp_TAK_not_INFER` transl 2; `particle_buollaga` conv 39; `particle_buollaga` flk 58; `particle_buollaga` nar 155; `particle_buollaga` transl 2.

Corpus-glossed evidentials (tier 1) per 1,000 glossed words, by genre. These are descriptive, and they count the annotators' glosses, not our coding:

| Genre | Glossed words | Tier-1 words | Per 1,000 |
|---|---|---|---|
| conv | 19671 | 23 | 1.17 |
| flk | 31609 | 41 | 1.30 |
| misc | 111 | 0 | 0.00 |
| nar | 41174 | 25 | 0.61 |
| sng | 98 | 0 | 0.00 |
| transl | 746 | 0 | 0.00 |

## Evenki (baseline; no cohort analysis)

612 texts, 53 speakers, 19 with a usable birth year. 1691 objects. Texts by dialect and source:

| dialect \ source | INEL collection: audio | archive: audio | archive: written | published: written | total |
|---|---|---|---|---|---|
| Barhahan | . | . | 200 | . | 200 |
| Ilimpi | . | . | 10 | 14 | 24 |
| Khantayskoye Ozero | 39 | 30 | . | 11 | 80 |
| Nepa (?) | . | . | . | 1 | 1 |
| Stony Tunguska | . | . | . | 10 | 10 |
| Sym | . | . | 203 | 22 | 225 |
| Taimyr | . | . | 37 | . | 37 |
| Yerbogachyon | . | . | . | 35 | 35 |

Objects by source: published: written 873, INEL collection: audio 491, archive: written 224, archive: audio 103.

### Study A candidates

| Rule (first rule that found it) | Tier | Words | Speakers | From speakers with usable birth year |
|---|---|---|---|---|
| `ge_EVID` | 1 | 29 | 7 | 0 |
| `IST_quot` | 2 | 276 | 23 | 0 |
| `evenki_PRF` | 2 | 277 | 32 | 0 |

By genre: `IST_quot` flk 266; `IST_quot` nar 10; `evenki_PRF` flk 118; `evenki_PRF` misc 2; `evenki_PRF` nar 157; `ge_EVID` flk 5; `ge_EVID` nar 24.

Corpus-glossed evidentials (tier 1) per 1,000 glossed words, by genre. These are descriptive, and they count the annotators' glosses, not our coding:

| Genre | Glossed words | Tier-1 words | Per 1,000 |
|---|---|---|---|
| conv | 211 | 0 | 0.00 |
| flk | 43649 | 5 | 0.11 |
| misc | 1941 | 0 | 0.00 |
| nar | 45837 | 24 | 0.52 |
| song | 696 | 0 | 0.00 |
