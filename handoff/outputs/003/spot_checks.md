# Spot checks (handoff 003, step 4)

Checker: `scripts/spot_checks.py` (stdlib only, seed 20261105). It does not import `shared/`; it re-reads the .exb and .coma files and compares them with `data/derived/`. Token ids only; no corpus text and no names.

How an utterance is matched: the pipeline numbers utterances by their order in the file (`<text_id>#NNN`), which is not the number inside the ref label. The checker finds the utterance by its `ref` string from `utterances.csv`, then re-derives the words from the .exb.

Two checker bugs found and fixed during this step (my script, not the pipeline): (1) first version read the utterance number from the ref label; (2) the `evenki_PRF` check looked only at the first gloss component and `next_verb` check accepted lexical verbs. Results below are from the final script. The one remaining FAIL is a real finding.

Summary: 39 of 40 pass. 1 fail (objects, predicate is not a verb).


| Group | Checked | Pass | Fail |
|---|---|---|---|
| objects | 10 | 9 | 1 |
| evid tier 1 (Dolgan) | 5 | 5 | 0 |
| evid tier 2 (Dolgan) | 5 | 5 | 0 |
| evid (Evenki) | 3 | 3 | 0 |
| b1 | 5 | 5 | 0 |
| multi-speaker utterances | 5 | 5 | 0 |
| speakers | 5 | 5 | 0 |

| Group | Id | Result | Note |
|---|---|---|---|
| objects | `KiPP_KuNS_200211_LifeChildren_conv#241.w02` | pass | pred ps=v |
| objects | `LaVN_KuNS_1999_FateOfANortherner_conv#165.w01` | pass | pred ps=v |
| objects | `SuAA_2004_Birth_nar#002.w10` | pass | pred ps=v |
| objects | `ElBK_KuNS_2004_Storytellers_conv#135.w03` | FAIL | pred ps='adv' is not a verb |
| objects | `PoXN_19701118_Chopochuka_flk#029.w03` | pass | pred ps=v |
| objects | `SuAA_2004_Birth_nar#052.w07` | pass | pred ps=v |
| objects | `PoNA_19940110_LastSupper_transl#016.w07` | pass | pred ps=v |
| objects | `AkEE_19900810_GirlAnys_flk#011.w03` | pass | pred ps=v |
| objects | `PoXN_19701118_Chopochuka_flk#102.w01` | pass | pred ps=v |
| objects | `ChPK_1970_ThreeBoys_flk#073.w10` | pass | pred ps=v |
| evid tier 1 (Dolgan) | `UkET_AkEE_19940424_SongsTales_conv#116.w03` | pass | rules: ge_EVID |
| evid tier 1 (Dolgan) | `KuSM_2008_Pear_nar#011.w10` | pass | rules: ge_INFER |
| evid tier 1 (Dolgan) | `SaSS_1964_NganasanBraveBoy_flk#059.w02` | pass | rules: ge_INFER |
| evid tier 1 (Dolgan) | `ChAPa_NN1_2009_Taboo_nar#095.w09` | pass | rules: ge_EVID |
| evid tier 1 (Dolgan) | `KiMN_19900417_Milkmaid_flk#150.w07` | pass | rules: ge_EVID |
| evid tier 2 (Dolgan) | `BaRD_1931_OldManHaresPolarFoxes_flk#008.w04` | pass | rules: IST_quot |
| evid tier 2 (Dolgan) | `BaRD_1930_DaughterOfNganasan_flk#045.w07` | pass | rules: mp_TAK_not_INFER |
| evid tier 2 (Dolgan) | `ChGS_UoPP_20170724_SocCogDesc_conv#359.w09` | pass | rules: mp_BIT |
| evid tier 2 (Dolgan) | `ErSV_1964_WarBirdsAnimals_flk#550.w03` | pass | rules: mp_BIT |
| evid tier 2 (Dolgan) | `ErSV_1964_OldManHares_flk#041.w08` | pass | rules: IST_quot |
| evid (Evenki) | `UV_192X_UpperWorld_flk#044.w04` | pass | rules: IST_quot |
| evid (Evenki) | `Be_19120710_HirogirKundogir_flk#039.w02` | pass | rules: evenki_PRF |
| evid (Evenki) | `NNR4_191X_Bandits_nar#056.w02` | pass | rules: evenki_PRF |
| b1 | `SoLK_2008_Life_nar#223.w04` | pass | rules: copula_next; next_verb = next cop/aux word, 2 word(s) after the target, 1 lexical verb(s) in between |
| b1 | `LaVN_KuNS_1999_FateOfANortherner_conv#057.w07` | pass | rules: copula_next; next_verb = next cop/aux word, 2 word(s) after the target, 0 lexical verb(s) in between |
| b1 | `BeES_1997_HistoryOfKatyryk_nar#079.w06` | pass | rules: ins_nominal; next_verb empty |
| b1 | `ChNM_2009_Vika_nar#083.w06` | pass | rules: ins_nominal; next_verb empty |
| b1 | `UkOA_KuNS_20XX_LifeNovorybnaya_conv#021.w05` | pass | rules: ins_nominal; next_verb empty |
| multi-speaker utterances | `KiPP_KuNS_2002_LegendOfBegichev_nar#021` | pass | 7 words, speaker KiPP |
| multi-speaker utterances | `KiPP_KuNS_2002_LegendOfBegichev_nar#072` | pass | 4 words, speaker KiPP |
| multi-speaker utterances | `KiPP_KuNS_2002_LegendOfBegichev_nar#049` | pass | 8 words, speaker KiPP |
| multi-speaker utterances | `KiPP_KuNS_2002_LegendOfBegichev_nar#015` | pass | 12 words, speaker KiPP |
| multi-speaker utterances | `KiPP_KuNS_2002_LegendOfBegichev_nar#064` | pass | 11 words, speaker KiPP |
| speakers | `KaVS` | pass | coma format '...'; pipeline -..-; mine -..- |
| speakers | `UkET` | pass | coma format 'DDDD.DD.DD.'; pipeline 1938..1938; mine 1938..1938 |
| speakers | `PoNA` | pass | coma format 'DDDD.DD.DD.'; pipeline 1929..1929; mine 1929..1929 |
| speakers | `AnMS` | pass | coma format 'DDDDs (?)'; pipeline 1910..1919; mine 1910..1919 |
| speakers | `SuKN` | pass | coma format 'DDDD/DDDD'; pipeline 1889..1890; mine 1889..1890 |

## The failure

`ElBK_KuNS_2004_Storytellers_conv#135.w03` (object `pro:O`, ps `que`): `pred_token_id` is `#135.w08`, a word with ps `adv` and SyF `adj:pred`, followed by a copula (`#135.w09`). The utterance also has a lexical verb before the object (`#135.w02`, SyF `v:pred`, `n_preds_in_utt` = 2). The pipeline picks the SyF `:pred` word nearest after the object, regardless of part of speech.

Over all 1,307 Dolgan objects, `pred_token_id` is set for 1,212. Part of speech of the predicate: v 1,112; aux 81; adj 5; n 5; empty 3; ptcl 3; cop 2; adv 1. So 19 of 1,212 are not a verb, auxiliary or copula (`diag_findings.py`).

## Notes on the passes (for web Claude)

- `copula_next` B1 rule: of 267 rows where a copula/aux follows the target in the utterance, 139 have at least one lexical verb between the target and that copula/aux (example `SoLK_2008_Life_nar#223.w04`: noun, then participle, then aux). "Neighbouring" does not mean adjacent. In such rows the copula probably belongs to the participle, not to the noun.
- `evenki_PRF` fires on the gloss `PTCP.PRF` (e.g. `NNR4_191X_Bandits_nar#056.w02`), i.e. the perfect participle, as well as finite perfects. Whether a participle counts as an evidential perfect is a question for the linguists.
- Speakers table: all 5 sampled rows match the .coma birth value, including a decade ("(?)") entry and a `YYYY/YYYY` range.
