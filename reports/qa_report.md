# QA report

Built by `shared/qa_report.py`. Compares the derived tables with the counts desktop Claude measured in handoff 002 (`handoff/outputs/002/structure_report.md`). No corpus text in this file.

## Dolgan

**Verdict: all checks MATCH.**

| Count | Handoff 002 | This build | Status |
|---|---|---|---|
| `transcripts` | 136 | 136 | MATCH |
| `speakers_in_exb_and_coma` | 74 | 74 | MATCH |
| `speaker_ids_in_exb` | 77 | 77 | MATCH |
| `tx_events` | 97652 | 97652 | MATCH |
| `ref_events` | 14076 | 14076 | MATCH |
| `words_with_mb` | 93409 | 93409 | MATCH |
| `words_mb_ge_mismatch` | 0 | 0 | MATCH |
| `words_syf_ends_O` | 1307 | 1307 | MATCH |
| `syf_ends_O_ACC` | 1056 | 1056 | MATCH |
| `syf_ends_O_NOM` | 216 | 216 | MATCH |
| `syf_ends_O_PART` | 23 | 23 | MATCH |
| `ge_EVID` | 53 | 53 | MATCH |
| `ge_INFER` | 36 | 36 | MATCH |
| `mp_TAK_ge_COND1` | >= 555 | 555 | MATCH |
| `ge_PST2` | >= 2415 | 5343 | MATCH |
| `ge_zero_NOM_morphs` | 21167 | 21167 | MATCH |
| `ge_ACC_morphs` | 6608 | 6608 | MATCH |
| `texts_with_SyF` | 50 | 50 | MATCH |

Documentation figures (D-016; reported, not checked): transcripts 136, speakers 74, utterances 14193, tokens 97625. This build: transcripts 136, utterances (`ref`) 14076, tokens (`tx`) 97652.

### QA flags

| Flag | Count |
|---|---|
| `morph_gloss_mismatch` | 2 |
| `speaker_not_in_coma` | 3 |
| `word_tier_event_without_word` | 1 |

### Values that later steps rely on

- Objects: 1307 words by 002's rule (last `SyF` part is `O`), 1307 by this pipeline's rule (any overt `form:O` item). The object table uses the second.
- `SyF` overt functions: `pred` 5104, `S` 2495, `O` 1307, `adv` 232, `temp` 69, `purp` 37, `comp` 34, `rel` 34, `cond` 6.
- `SyF` zero-argument items: `S` 2669, `S cop` 124, `O` 1.
- `BOR` values (the object table treats any non-empty value as a loan; **check this**): `RUS:cult` 4864, `MONG:cult` 2000, `MONG:core` 1338, `%MONG:core` 1070, `RUS:gram` 856, `RUS:mod` 763, `RUS:core` 717, `%MONG:cult` 649, `MONG:mod` 587, `MONG:gram (HAB)` 525, `MONG:gram (PTCP.HAB)` 455, `MONG:gram` 424, `RUS:disc` 345, `EV:core` 277, `EV:cult` 266.
- `IST` values (the Study A rule `IST_quot` looks for `quot`; **check the spelling**): `giv-active` 1389, `0.giv-active` 1354, `giv-inactive` 1353, `accs-inf` 808, `new` 638, `0.giv-active-Q` 511, `giv-active-Q` 412, `giv-inactive-Q` 364, `0.quot-sp` 340, `0.giv-inactive` 267, `accs-gen` 191, `accs-inf-Q` 155, `quot-sp` 137, `new-Q` 122, `accs-sit` 114, `0.giv-inactive-Q` 112, `accs-gen-Q` 65, `accs-sit-Q` 34, `0.quot-th` 29, `0.accs-aggr` 25.
- Case labels on all words: `NOM` 21113, `ACC` 6567, `DAT/LOC` 5204, `ABL` 1055, `INS` 926, `GEN` 604, `PART` 111, `COMP` 40.
- Source collection per text (inferred for Dolgan, D-013 note): `TDNT_archive` 52, `fieldwork_2007_2010` 44, `published_folklore` 36, `fieldwork_2017` 4.
- Dialect per text: `Upper` 61, `Lower` 42, `Upper (?)` 15, `Upper, Lower` 6, `(empty)` 5, `Anabar` 3, `Lower (?)` 2, `..., Lower` 1, `Lower, Upper` 1.
- Part-of-speech (`ps`) values: `v` 23238, `n` 23138, `ptcl` 9742, `adv` 6670, `dempro` 5881, `adj` 4360, `(empty)` 4247, `que` 2963, `aux` 2932, `post` 2426, `pers` 2322, `propr` 2223, `cop` 2093, `cardnum` 1486, `interj` 1400, `conj` 951, `quant` 705, `emphpro` 424, `ordnum` 131, `posspr` 111, `indfpro` 89, `collnum` 52, `distrnum` 34, `%%` 13, `prep` 10, `pro` 6, `postp` 3, `rel` 1, `ad` 1.
- Words with more than one case label: 2.

## Evenki

**Verdict: all checks MATCH.**

| Count | Handoff 002 | This build | Status |
|---|---|---|---|
| `transcripts` | 612 | 612 | MATCH |
| `speakers_in_exb_and_coma` | 53 | 53 | MATCH |
| `speaker_ids_in_exb` | 53 | 53 | MATCH |
| `tx_events` | 93411 | 93411 | MATCH |
| `ref_events` | 19931 | 19931 | MATCH |
| `words_with_mb` | 92345 | 92345 | MATCH |
| `words_mb_ge_mismatch` | 0 | 0 | MATCH |
| `words_syf_ends_O` | 1691 | 1691 | MATCH |
| `ge_EVID` | 28 | 28 | MATCH |
| `ge_zero_NOM_morphs` | 28291 | 28291 | MATCH |
| `ge_ACC_morphs` | 5483 | 5483 | MATCH |
| `texts_with_SyF` | 131 | 131 | MATCH |

Documentation figures (D-016; reported, not checked): transcripts 612, utterances 19931, tokens 93264. This build: transcripts 612, utterances (`ref`) 19931, tokens (`tx`) 93411.

### QA flags

| Flag | Count |
|---|---|
| `morph_gloss_mismatch` | 11 |
| `word_outside_utterance` | 11 |

### Values that later steps rely on

- Objects: 1691 words by 002's rule (last `SyF` part is `O`), 1691 by this pipeline's rule (any overt `form:O` item). The object table uses the second.
- `SyF` overt functions: `pred` 6087, `S` 3274, `O` 1691, `temp` 140, `adv` 60, `purp` 46, `rel` 36, `cond` 11, `compl` 6.
- `SyF` zero-argument items: `S` 2762, `S cop` 100.
- `BOR` values (the object table treats any non-empty value as a loan; **check this**): `RUS:cult` 3604, `RUS:gram` 1114, `RUS:core` 639, `RUS:mod` 386, `DOLG/YAK:cult` 224, `RUS:disc` 75, `YAK:mod` 60, `DOLG/YAK:core` 56, `%RUS:cult` 39, `%SELK:cult` 28, `RUS:gram(PTCL)` 22, `YAK:cult` 15, `DOLG/YAK:mod` 15, `SELK:cult` 14, `NEN:cult` 12.
- `IST` values (the Study A rule `IST_quot` looks for `quot`; **check the spelling**): `giv-active` 895, `0.giv-active` 836, `giv-inactive` 530, `new` 405, `giv-active-Q` 336, `accs-inf` 298, `0.giv-active-Q` 289, `quot-sp` 251, `giv-inactive-Q` 166, `new-Q` 66, `accs-sit` 64, `0.giv-inactive-Q` 62, `0.giv-inactive` 56, `accs-inf-Q` 53, `accs-gen` 50, `0.accs-aggr` 23, `accs-gen-Q` 17, `quot-th` 17, `accs-sit-Q` 13, `accs-aggr` 11.
- Case labels on all words: `NOM` 28251, `ACC` 5903, `DAT/LOC` 4389, `LAT` 2176, `ABL` 1699, `ACC.INDF` 1591, `INS` 1332, `PROL` 878, `ALL` 509, `COM` 498, `VOC` 68, `COMP` 37.
- Source collection per text (inferred for Dolgan, D-013 note): `archive: written` 450, `published: written` 93, `INEL collection: audio` 39, `archive: audio` 30.
- Dialect per text: `Sym` 225, `Barhahan` 200, `Khantayskoye Ozero` 80, `Taimyr` 37, `Yerbogachyon` 35, `Ilimpi` 24, `Stony Tunguska` 10, `Nepa (?)` 1.
- Part-of-speech (`ps`) values: `v` 30694, `n` 26799, `adv` 4878, `dem` 4466, `nprop` 4404, `pers` 4085, `adj` 3423, `interrog` 2070, `aux` 2046, `cardnum` 1809, `cop` 1373, `conj` 1255, `(empty)` 1121, `ptcl` 1001, `locn` 837, `quant` 785, `ptcp` 693, `posspro` 583, `interj` 545, `emphpro` 349, `%%` 93, `onom` 52, `pp` 44, `recpro` 6.
- Words with more than one case label: 182.
