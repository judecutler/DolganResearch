# 006 step 5: spot checks

Script: `handoff/outputs/006/scripts/spot_checks_006.py`, seed **20261106** (one `random.Random`, used in order: 5 copula_next rows, 3 evenki_PTCP_PRF, 3 evenki_PRF). Words re-derived from the .exb files.

| Check | Token id | Result | Note |
|---|---|---|---|
| object predicate | `ElBK_KuNS_2004_Storytellers_conv#135.w03` | pass | pred `ElBK_KuNS_2004_Storytellers_conv#135.w02`: tokens.csv ps='v', .exb ps='v' |
| b1 copula_next | `KiPP_KuNS_200211_LifeChildren_conv#273.w07` | pass | copula at +1 (ps=cop, stem gloss 'be'), ps=v between: 0 |
| b1 copula_next | `LaVN_KuNS_1999_FateOfANortherner_conv#308.w04` | pass | copula at +1 (ps=cop, stem gloss 'be'), ps=v between: 0 |
| b1 copula_next | `SuON_KuNS_19990303_HardLife_conv#146.w15` | pass | copula at +1 (ps=cop, stem gloss 'be'), ps=v between: 0 |
| b1 copula_next | `PoMA_1964_IronCapBonyBelt_flk#076.w02` | pass | copula at +2 (ps=cop, stem gloss 'be'), ps=v between: 0 |
| b1 copula_next | `BeEI_KuNS_1998_Teacher_conv#134.w02` | pass | copula at +2 (ps=cop, stem gloss 'become'), ps=v between: 0 |
| evenki_PTCP_PRF | `NNR4_191X_ChopOffLeg_nar#093.w04` | pass | PRF morph gloss: `PTCP.PRF.[NOM]` |
| evenki_PTCP_PRF | `UA_1965_OldDevilWoman_flk#031.w01` | pass | PRF morph gloss: `PTCP.PRF` |
| evenki_PTCP_PRF | `BTV_20190822_ReindeerEvenks_nar#012.w04` | pass | PRF morph gloss: `PTCP.PRF` |
| evenki_PRF | `Kalk_191X_AnganchaWent_nar#035.w02` | pass | PRF morph gloss: `PRF.[3SG]` |
| evenki_PRF | `NNR4_191X_StoriesAboutMedicines_nar#036.w10` | pass | PRF morph gloss: `PRF` |
| evenki_PRF | `BTV_20190815_HowokoTorganej_flk#053.w06` | pass | PRF morph gloss: `PRF` |

Dolgan objects: 1307; with pred_token_id 1201, empty 106. pred_token_ids whose tokens.csv ps is not v/aux/cop: **0**.

Summary: object predicate: 1 pass, 0 fail; b1 copula_next: 5 pass, 0 fail; evenki_PTCP_PRF: 3 pass, 0 fail; evenki_PRF: 3 pass, 0 fail.
