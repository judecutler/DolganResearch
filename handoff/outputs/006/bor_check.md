# 006 step 4: `word_tier_event_without_word` check

Script: `handoff/outputs/006/scripts/bor_check.py`, seed 20261106. Spans are timeline indices. Examples are random (fixed seed), ids and tier values only.

Classes (same speaker's `tx` words): **a** = starts at one word's start and ends at a later word's end; **b** = partial overlap (b-inside-one-word: lies within one word; b-crosses-boundary: overlaps a word boundary); **c** = overlaps no word of that speaker (c-other-speaker: overlaps another speaker's word; c-none: no word at all).

## Dolgan: 1282 flags

| Tier | a | b-inside-one-word | b-crosses-boundary | c-other-speaker | c-none | Total |
|---|---|---|---|---|---|---|
| BOR | 19 | 1 | 0 | 0 | 0 | 20 |
| BOR-Morph | 3 | 0 | 0 | 0 | 0 | 3 |
| ExLocPoss | 1258 | 0 | 1 | 0 | 0 | 1259 |
| **All** | 1280 | 1 | 1 | 0 | 0 | 1282 |

Examples, class a (5 of 1280):

| text_id | speaker | tier | span | tx words inside | tier value |
|---|---|---|---|---|---|
| ChSA_KuNS_2004_ReindeerHerding_conv | ChSA | ExLocPoss | (139, 141) | 2 | `Poss:Zero.Aff` |
| LaVN_KuNS_1999_FateOfANortherner_conv | KuNS | ExLocPoss | (812, 818) | 5 | `Ex:Cop.Aff` |
| SuON_KuNS_19990303_HardLife_conv | KuNS | ExLocPoss | (183, 190) | 7 | `Ex:PosV.Aff` |
| BoND_1964_ThreeBrothers_flk | BoND | ExLocPoss | (331, 337) | 6 | `Ex:PosV.Aff` |
| AkNN_KuNS_200212_LifeHandicraft_conv | AkNN | ExLocPoss | (50, 53) | 3 | `Poss:Zero.Aff` |

Examples, class b-inside-one-word (1 of 1):

| text_id | speaker | tier | span | tx words inside | tier value |
|---|---|---|---|---|---|
| PoTY_2009_Aku_nar | PoTY | BOR | (426, 427) | 0 | `MONG:gram (NMLZ)` |

Examples, class b-crosses-boundary (1 of 1):

| text_id | speaker | tier | span | tx words inside | tier value |
|---|---|---|---|---|---|
| BeVP_1970_BaldheadedOrphanBoy_flk | BeVP | ExLocPoss | (302, 306) | 3 | `Loc:Ex.Aff` |

Examples, class a, BOR and BOR-Morph only (5 of 22):

| text_id | speaker | tier | span | tx words inside | tier value |
|---|---|---|---|---|---|
| AkNN_KuNS_200212_LifeHandicraft_conv | AkNN | BOR | (329, 332) | 3 | `RUS:cult` |
| KuDP_2009_Hare_nar | KuDP | BOR | (53, 55) | 2 | `RUS:gram` |
| AkNN_KuNS_200212_LifeHandicraft_conv | KuNS | BOR | (556, 558) | 2 | `RUS:cult` |
| KuDP_2009_Hare_nar | KuDP | BOR | (48, 50) | 2 | `RUS:core` |
| AkNN_KuNS_200212_LifeHandicraft_conv | KuNS | BOR | (941, 943) | 2 | `RUS:cult` |

Class-a events by tier: {'BOR': 19, 'ExLocPoss': 1258, 'BOR-Morph': 3}. Words covered per class-a event: {2: 182, 3: 305, 4: 302, 5: 201, 6: 134, 7: 64, 8: 43, 9: 22, 10: 10, 11: 5, 12: 3, 13: 7, 15: 1, 20: 1}.

## Evenki: 526 flags

| Tier | a | b-inside-one-word | b-crosses-boundary | c-other-speaker | c-none | Total |
|---|---|---|---|---|---|---|
| ExLocPoss | 526 | 0 | 0 | 0 | 0 | 526 |
| **All** | 526 | 0 | 0 | 0 | 0 | 526 |

Examples, class a (5 of 526):

| text_id | speaker | tier | span | tx words inside | tier value |
|---|---|---|---|---|---|
| NNR3_1913_FlyingSquirrel_flk | NNR3 | ExLocPoss | (50, 52) | 2 | `Poss:Zero.Aff` |
| NNR_190X_FireFeather_flk | NNR | ExLocPoss | (62, 65) | 3 | `Ex:Cop.Neg` |
| KI_1931_Charchikan_flk | KI | ExLocPoss | (264, 266) | 2 | `Ex:Ex.Neg` |
| KSh_1930_Nara_flk | KSh | ExLocPoss | (75, 77) | 2 | `Ex:Ex.Neg` |
| NNR_190X_NelheKokora_flk | NNR | ExLocPoss | (1154, 1156) | 2 | `Loc:Zero.Aff` |

Class-a events by tier: {'ExLocPoss': 526}. Words covered per class-a event: {2: 157, 3: 187, 4: 105, 5: 52, 6: 14, 7: 8, 8: 1, 9: 1, 12: 1}.

## Dolgan: objects inside class-a BOR / BOR-Morph events

Class-a BOR/BOR-Morph events: 22 in 4 texts. Utterances in those texts not resolvable to one ref event: 0.

| Tier | Objects inside a class-a event | of which `bor` / `bor_morph` empty | Tokens (tokens.csv) inside | of which `BOR` / `BOR_Morph` empty |
|---|---|---|---|---|
| BOR | 0 | 0 | 46 | 46 |
| BOR-Morph | 0 | 0 | 8 | 8 |

## Is information lost?

Yes at the token level, no at the object level. Every flagged event except 2 in Dolgan is a multi-word (class a) event, so the pipeline, which only copies word-tier values onto a token whose tx span matches the event exactly, drops them. For BOR this means 19 class-a BOR and 3 class-a BOR-Morph events lose their loan label: 46 + 8 tokens in tokens.csv that lie inside these events have an empty BOR / BOR_Morph field. None of these tokens is an object (0 objects affected), so the B2 object table and its `bor` / `bor_morph` / loan confounder are not affected in the current data. The ExLocPoss events (1258 Dolgan, 526 Evenki) are construction-level annotations over several words and are also absent from the token-level ExLocPoss column; whether that matters depends on whether any analysis uses ExLocPoss. No event lies outside the speaker's words or on another speaker's words.

