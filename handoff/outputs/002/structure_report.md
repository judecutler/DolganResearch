# Handoff 002: structure report

Written by desktop Claude, 2026-11-05. Corpora: INEL Dolgan Corpus 2.0 (`dolgan-2.0-noaudio.zip`) and INEL Evenki Corpus 2.0 (`evenki-2.0-lite.zip`), as recorded in `data/MANIFEST.json`. Answers are keyed by the question numbers in `002-inspect-structure.md`. Everything below was read from the real files unless marked **UNVERIFIED**. Excerpts are at most 30 lines and name their source file. No speaker names are included; speaker IDs (sigles) appear only inside excerpts and file names.

**How things were counted.** All 136 Dolgan and 612 Evenki `.exb` files parsed without error with `xml.etree`. Words were aligned across tiers by exact `(start, end)` timeline position within one speaker. A "morph" is a piece of an `mb`, `mp` or `ge` string after splitting on `-` and `=`. Scripts are in `handoff/outputs/002/scripts/`.

## Short version for web Claude

- Per-word alignment is exact: every word that has both `mb` and `ge` has the same number of morphs in each (0 mismatches in 93,409 Dolgan and 92,334 Evenki words). `mp` also aligns. The `mc` tier does **not** align one-to-one in Dolgan (about 17% of words with `mc` and `mp` have different slot counts); it does in Evenki.
- Zero nominative is written `.[NOM]` on the last gloss, e.g. `PL.[NOM]`, in both corpora; no plain `NOM` label exists. Dolgan has `DAT/LOC` as one label (no separate DAT or LOC); Evenki has `LAT`, `ALL`, `COM1` to `COM4`, `ACC.INDF` (not `ACC.INDEF`) and `INS` (not `INSTR`).
- There is no `-BIt` or `-DAK` in the tiers as the task spelled them. In Dolgan `mp` the morph `BIT` is glossed `PST2`, `BIt` is `1PL`, and `TAK` is `COND1` (555) or `INFER` (36). `EVID` in Dolgan is the particle `eːt` (53 tokens). Evenki has `EVID` on `rkə` (29 tokens) and no `INFER` at all.
- Role `St` is not secondary predicates. The documentation defines it as stimulus of perception verbs, and the examples agree. The hypothesis in Q10 is not supported.
- Counts reconcile for Evenki exactly (612 texts, 19,931 utterances, 93,264 tokens when tokens are counted as `# INEL:w` in the `.coma`). For Dolgan, 136 texts and 74 speakers reconcile, but utterances (14,078 or 14,076) and tokens (97,757 or 97,652) do not equal the documented 14,193 and 97,625.
- The Dolgan documentation says Anabar Dolgan is not in the corpus, but the `.coma` marks 3 texts and 2 speakers as `Anabar`.
- Birth dates are mostly missing or imprecise. Dolgan: 60 of 74 speakers who appear in a transcript have a value, only 16 as full dates. Evenki: 34 of 53 speakers are unknown.

## A. File layout

**Q1. Tiers.** Each transcript is one folder holding `<id>.exb`, `<id>_s.exs`, `<id>_tei.xml`. In every tier, `display-name` equals the tier `id`, `category` is the tier name, and `speaker` is set (no tier lacks it). Type is `t` for `tx` only; every other tier is `a`. The `.exb` tiers (per speaker) in Dolgan, in file order, are: `ref`, `st`, `ts`, `tx`(t), `mb`, `mp`, `ge`, `gg`, `gr`, `mc`, `ps`, `SeR`, `SyF`, `IST`, `Top`, `Foc`, `BOR`, `BOR-Phon`, `BOR-Morph`, `CS`, `ExLocPoss`, `fe`, `fg`, `fr`, `ltr`, `nt`. What I could confirm from content: `ref` holds the utterance reference ID, `st` the Cyrillic source text, `ts` a Latin transliteration of the whole utterance, `tx` the Latin transcription per word, `mb`/`mp` morph strings, `ge`/`gg`/`gr` English/German/Russian glosses, `mc` morph categories, `ps` part of speech, `fe`/`fg`/`fr` English/German/Russian free translations per utterance, `ltr` a Russian literal translation. Meanings of `IST`, `Top`, `Foc`, `BOR*`, `CS`, `ExLocPoss`, `nt` are from the tier names and the documentation only (not checked in the data beyond the value patterns below).

Differences between files and corpora (file counts of 136 Dolgan, 612 Evenki):

| Tier | Dolgan files | Evenki files |
|---|---|---|
| `st` | 106 | 531 |
| `stl` | 5 | 612 |
| `Top`, `Foc` | 136 each | **0** (absent) |
| `ExLocPoss` | 120 | 154 |
| `nto` | 0 | 359 |
| `lte` | 0 | 164 |
| `ltg` | 0 | 80 |
| all other tiers above | 136 | 612 |

`stl`, `nto`, `lte`, `ltg` appear in only one corpus or a subset; I did not look at what they hold (**UNVERIFIED**; Evenki-only tiers are listed in the Evenki documentation).

**Q2. Speakers.** One set of tiers per speaker. In files with more than one speaker the tier id is `<category>-<SIGLE>` (e.g. `tx-KuNS`); in single-speaker files the id is just the category (e.g. `tx`) and the speaker is only in the `speaker` attribute. Speakers per transcript: Dolgan 94 files with 1, 33 with 2, 8 with 3, 1 with 4; Evenki 605 with 1, 6 with 2, 1 with 3. Sigles are 2 to 5 mixed-case letters (e.g. `AkNN`, `KuNS`, `ChI`).

**Q3. `.exb` vs `.exs`.** The `.exb` is the basic transcription: tiers of events on a shared timeline. The `.exs` is EXMARaLDA's segmented version of the same transcript. Its tiers are `segmented-tier` elements with `annotation` children that refer to segments, plus two `segmentation` layers per speaker (`SpeakerContribution_Utterance_Word` and `SpeakerContribution_Event`) made of `ts` elements of type `sc` (speaker contribution), `HIAT:u` (utterance) and `HIAT:w` (word). So the `.exs` is the file that lists utterance and word segmentation; the `.exb` has no such layer. Whether the annotation text itself is identical in both files I did not check (**UNVERIFIED**). In Dolgan the counts of `HIAT:u`, `HIAT:w` and `sc` in the `.exs` files add up to the `# HIAT:u`, `# HIAT:w`, `# sc` values in the `.coma` (14,078, 97,757, 8,052). The Evenki `.coma` has `# INEL:w`, `# INEL:u`, `# sc` instead; `sc` matches (2,788).

## B. Alignment

**Q4.** Each word is one event in `tx`, with the morphemes of that word separated by `-` inside the `mb`, `mp`, `ge`, `mc` strings of the event with the same start and end. Events at word level in `ps` and the other word tiers share the same start and end ids. Utterance tiers (`ref`, `fe`, `st`, ...) span many words. Ten consecutive fully annotated events, one per corpus (chosen to avoid names):

```
start end   tx | mb | mp | ge | mc | ps
 T104  T105  ɨj | ɨj | ɨj | moon.[NOM] | n.[n:case] | n
 T105  T106  külüːge | külüːg-e | külük-tA | shadow-3SG.[NOM] | n-n:(poss).[n:case] | n
 T106  T107  bert | bert | bert | very | adv | adv
 T107  T108  hugaskaːn | hugas-kaːn | čugas-kAːN | close-INTNS.[NOM] | adj-adj>adj.[n:case] | adj
 T108  T109  köstör, | köst-ör | köhün-Ar | be.visible-PRS.[3SG] | v-v:tense.[v:pred.pn] | v
 T109  T110  ojbonu | ojbon-u | ojbon-nI | icehole-ACC | n-n:case | n
 T110  T111  toloru | toloru | toloru | full | adj | adj
 T111  T112  bu͡olla, | bu͡olla | bu͡olla | MOD | ptcl | ptcl
 T112  T113  kihi | kihi | kihi | human.being.[NOM] | n.[n:case] | n
 T113  T114  da | da | da | EMPH | ptcl | ptcl
```
*Source: Dolgan corpus, `AkEE_19900810_GirlAnys_flk.exb` (flk), events T104 to T114*

```
start end   tx | mb | mp | ge | mc | ps
  T44   T45  hurukəl, | huru-kəl | suru-kəl | leave-IMP.2SG | v-v:imp.pn | v
  T45   T46  tadu | ta-du | tar-duː | that-DAT/LOC | dem-n:case | dem
  T46   T47  higindulo | higin-dulo | higin-ləː | wind-LAT | n-n:case | n
  T47   T48  hogdʼoji | hogdʼo-ji | hogdʼo-wiː | tail-RFL.SG | n-n:rfl.poss | n
  T48   T49  əjiːkəl, | əjiː-kəl | əjiː-kəl | put.in.water-IMP.2SG | v-v:imp.pn | v
  T49   T50  gorojoː | goro-joː | goro-jə | long/distant-ACC.INDF | adj-n:case | adv
  T50   T51  təgətkəl, | təgət-kəl | təgət-kəl | sit-IMP.2SG | v-v:imp.pn | v
  T51   T52  imuːrə | imuːrə | imuːrəː | tallow.[NOM] | n.[n:case] | n
  T52   T53  oːdʼan", | oː-dʼa-n | oː-dʼəː-n | become-FUT.IMM-3SG | v-v:tense1-v:pn2 | cop
  T53   T54  hulakiː | hulakiː | sulakiː | fox.[NOM] | n.[n:case] | n
```
*Source: Evenki corpus, `BTV_20190814_FoxAndBear_flk.exb` (flk), events T44 to T54*

Note that `mc` in Dolgan has a slot for case even when `mb` has no case morph (e.g. `n-n:case` for a one-morph noun, with `.[NOM]` in `ge`).

**Q5. Separators.** Counts of non-alphanumeric characters:

| Character | Dolgan `mb` | Dolgan `mp` | Dolgan `ge` | Evenki `mb` | Evenki `mp` | Evenki `ge` |
|---|---|---|---|---|---|---|
| `-` morph boundary | 79,416 | 79,416 | 79,421 | 121,454 | 121,454 | 121,454 |
| `=` clitic boundary | 651 | 651 | 646 | **0** | 0 | 0 |
| `.` | 1 | 367 | 52,706 | 0 | 0 | 73,695 |
| `[` `]` | 0 | 367 | 28,044 | 0 | 0 | 38,381 |
| `/` | 0 | 0 | 5,700 | 0 | 0 | 5,315 |
| `%` | 0 | 0 | 197 | 2 | 8 | 3,033 |
| `:` | 953 | 0 | 0 | 0 | 5 | 0 |
| `_` | 23 | 23 | 253 | 6 | 6 | 6 |
| `~` | 0 | 0 | 0 | 0 | 0 | 0 |

Reading these against the files and the Dolgan documentation (which says the same): `-` separates morphs; `=` marks a clitic in Dolgan only (e.g. `woman-2PL=Q`, `be-PST1-2PL=Q`); in Evenki clitics are not marked by a special character. `.` joins several semantic components in one gloss (`IMP.2SG`, `PTCP.PRS`, `human.being`); `/` separates alternative analyses (`DAT/LOC`, `RECP/COLL`); `_` joins words in one gloss (`black_and_white`); `:` in Dolgan `mb` is a vowel-length mark (e.g. `ülel-i:r`; in `mp` the length mark is `ː`). **Zero morphs** are written in square brackets after a dot on the last gloss (`FUT.[3SG]`, `PL.[NOM]`, `PRS.[3SG]`); they do not appear in `mb`, and in Dolgan `mp` only 367 words show a bracketed zero (e.g. `IAK.[tA]`). **Portmanteau** glosses are single labels with dots (e.g. `PST2.NEG`, `PRO.1SG.ACC` in Evenki). **Unsure/unknown analyses:** a `%` prefix marks a morpheme of unsure meaning and `%%` one of unknown meaning (the Dolgan documentation says so; Evenki uses the same signs, 3,033 `%` in `ge`).

**Q6. `mb` vs `ge` morph counts.** Counted over all words that have both tiers non-empty: Dolgan 93,409 words, 93,409 equal, **0 differ**; Evenki 92,334 words, 92,334 equal, **0 differ**. For one text (the largest): 2,910 of 2,910 equal in Dolgan, 3,312 of 3,312 in Evenki. So there are no mismatches to show. The caveat is that these are only words that have both tiers: 4,243 Dolgan and 1,066 Evenki `tx` words have no `mb` event (see Q21).

## C. Optional tiers

**Q7.** Per-text table in `tier_coverage_dolgan.csv` and `tier_coverage_evenki.csv` (columns `<tier>_present`, `<tier>_nonempty_events`). Totals:

| Tier | Dolgan texts with tier | Dolgan texts non-empty (events) | Evenki texts with tier | Evenki texts non-empty (events) |
|---|---|---|---|---|
| SyF | 136 | 50 (11,710) | 612 | 131 (12,251) |
| SeR | 136 | 50 (11,694) | 612 | 130 (10,879) |
| IST | 136 | 36 (8,465) | 612 | 69 (4,343) |
| Top | 136 | 30 (2,937) | 0 | 0 |
| Foc | 136 | 30 (3,710) | 0 | 0 |
| BOR | 136 | 136 (15,864) | 612 | 481 (6,359) |
| BOR-Phon | 136 | 36 (573) | 612 | 60 (240) |
| BOR-Morph | 136 | 39 (1,427) | 612 | 82 (608) |
| CS | 136 | 17 (374) | 612 | 18 (89) |
| ExLocPoss | 120 | 120 (1,287) | 154 | 154 (534) |

**Q8.** The files use `BOR-Phon` (and `BOR-Morph`) in every tier; the spelling `BORphon` occurs nowhere in either corpus.

**Q9. SyF.** In the `SyF` tier a value is `<form>:<function>` (sometimes followed by ` cop`). Counting the last part of each non-empty `SyF` event: Dolgan `pred` 5,656, `S` 2,507, `O` 1,308, `adv` 657, `temp` 609, `cop` 268, `rel` 181, `comp` 174, `purp` 152, `S cop` 129, `cond` 69; Evenki `pred` 6,105, `S` 3,286, `O` 1,691, `temp` 307, `cop` 305, `adv` 132, `S cop` 100, `rel` 96, `compl` 95, `purp` 82, `cond` 52. Five values ending in `:O` and five in `:S`, per corpus (single-word events, names avoided):

Ending in `:O`

```
np:O       | taŋastargɨtɨn, | taŋas-tar-gɨtɨ-n | clothes-PL-2PL-ACC
np:O       | ataktargɨtɨn | atak-tar-gɨtɨ-n | shoes-PL-2PL-ACC
np:O       | kajgalɨn | kajgal-ɨ-n | award-3SG-ACC
np:O       | vɨstavkalar | vɨstavka-lar | exhibition-PL.[NOM]
np.h:O     | kihileri | kihi-ler-i | human.being-PL-ACC
```
*Source: Dolgan corpus, files: `AkNN_KuNS_200212_LifeHandicraft_conv.exb` (SyF value | tx | mb | ge)*

```
pro.h:O    | nuŋarwatin | nuŋa-r-wa-tin | PRO.3-PL-ACC-3PL
np:O       | hulukukoːnə | hulu-ku-koːn-ə | small-AUG-DIM1-ACC.INDF
np.h:O     | bəjəwə | bəjə-wə | human-ACC
np:O       | uldəwə | uldə-wə | meat-ACC
np:O       | bərwə | bər-wə | bow-ACC
```
*Source: Evenki corpus, files: `BTV_20180827_SmallPeople_flk.exb` (SyF value | tx | mb | ge)*

Ending in `:S`

```
np.h:S     | kihiler | kihi-ler | human.being-PL.[NOM]
np.h:S     | kihiler, | kihi-ler | human.being-PL.[NOM]
pro.h:S    | min | min | 1SG.[NOM]
pro.h:S    | bejegit | beje-git | self-2PL.[NOM]
pro.h:S    | min, | min | 1SG.[NOM]
```
*Source: Dolgan corpus, files: `AkNN_KuNS_200212_LifeHandicraft_conv.exb` (SyF value | tx | mb | ge)*

```
np.h:S     | bəjətkoːr | bəjə-tkoː-r | human-DIM3-PL.[NOM]
pro.h:S    | nuŋartin | nuŋa-r-tin | PRO.3-PL.[NOM]-3PL
np.h:S     | bəjəl | bəjə-l | human-PL.[NOM]
np.h:S     | mata | mata | guest.[NOM]
np.h:S     | bəjə | bəjə | human.[NOM]
```
*Source: Evenki corpus, files: `BTV_20180827_SmallPeople_flk.exb` (SyF value | tx | mb | ge)*

Note: `SyF` can also sit on a span of several words (e.g. clause-level values such as `s:comp`), not only on single words.

**SeR.** A value is `<form>:<role>`. Distinct roles with counts. Dolgan (19 values): A 3,951; Th 2,853; Poss 748; L 716; Time 682; P 675; G 616; E 592; So 194; R 150; Com 112; Ins 112; St 102; Cau 86; Path 63; B 39; and three singletons that look like annotation slips (**UNVERIFIED**): `Ben` 1, `poss` 1, one value with no colon. Evenki (16 values): A 4,412; Th 2,080; P 826; G 643; E 503; L 500; Time 489; Poss 386; St 242; B 175; R 150; Com 141; So 117; Path 105; Ins 74; Cau 36. Five most common `SeR` forms: Dolgan `np` 3,066, `0.3.h` 2,264, `np.h` 1,874, `pro.h` 857, `0.1.h` 782; Evenki `np` 2,718, `np.h` 2,560, `0.3.h` 2,092, `pro.h` 1,007, `pro` 511.

**Q10. Role `St`.** It occurs: 102 times in Dolgan, 242 in Evenki. It is **not** a marker of secondary predicates. The Dolgan documentation defines it as the stimulus of physical perception, the second actant of verbs like "see", "hear", "feel" (but not "look for", "listen"). The examples agree: the `St` word is the thing seen or recognised. The hypothesis in the task is not supported.

```
np:St              | otu | flower-ACC | “It spotted a strange, a strange flower; a flower, though, you see, a flower.”
pro:St             | tugu | what-ACC | “– The little child has spotted something, the child.”
0.3.h:Poss np.h:St | dʼaktarɨn | woman-3SG-ACC | “He is remembering his child, he is remembering his wife.”
np:St              | ülegitin, | work-2PL-ACC | “– The heads of the rayon saw your work apparently, right?”
np:St              | tɨl | word.[NOM] | “There I said in vain "raise them", now one listens to the words, our workers are bad nowadays.”
```
*Source: Dolgan corpus, files: `ChGS_UoPP_20170724_SocCogDesc_conv.exb`, `ChSA_KuNS_2004_ReindeerHerding_conv.exb` (SeR value | tx | ge | free translation en)*

```
np.h:St            | amakaːsiwə, | bear-ACC | “It saw a bear, stopped and started to chew something.”
np.h:St            | hulakiːtki | fox-ALL | “The bear was angry with the fox.”
pro:St             | ərgəsinmə | this-SIMIL-ACC | “"I didn't see such thing yet", the girl's father said.”
np:St              | monoptunma | %necklace-ACC | “The hunter recognised his daughter's necklace.”
np:St              | oːranma | waterfall-ACC | “They ran to the mountains, the saw how the snow sheep are jumping, they saw the waterfall.”
```
*Source: Evenki corpus, files: `BTV_20190814_FoxAndBear_flk.exb`, `BTV_20190815_BearWasGirl_flk.exb`, `BTV_20190815_ChompoBear_flk.exb` (SeR value | tx | ge | free translation en)*

## D. Metadata (`.coma`)

Both `.coma` files have `Speaker` and `Communication` records with `Key` fields. The Dolgan `.coma` lists 91 speakers and 173 communications: 136 have transcripts, 37 are audio-only (matching the corpus page). The Evenki `.coma` lists 53 speakers and 612 communications, all with transcripts. **Privacy:** the speaker records contain names, parents' names, family, birthplace and residence (some with coordinates). None of that is repeated here, and it must stay out of derived tables.

**Q11. Dolgan speaker fields** (key names, 91 speaker records): 1 First language; 2 Dialect; 3 Second dialect (1 record); 1 Second language; 1 Third language (3); 1a Place of birth; 1b Place of birth (RU); 1c Place of birth (LngLat) (62, plus 2 as `1c Place of Birth (LngLat)`); 2 Region; 3 Country; 4 Date of birth; 5 Date of death; 6a/6b Former residences; 7a/7b Domicile; 7c Domicile (LngLat) (83); 8a/8b Other information; 1a/1b Education; 2a/2b Higher education; 3a/3b Occupation; 1 Ethnicity; 2a/2b mother; 3a/3b father; 4a/4b husband/wife; 5a/5b grandparents; 6a/6b Family; Informant of; 1a/1b Family name; 2a/2b Given name; 3a/3b Patronymic; 4 Vulgo (Dolgan name); 5a/5b Alternate names (and 4a/4b once). Each record also has Sigle, Pseudo, KnownHuman and Sex (50 female, 41 male).

`4 Date of birth` is filled in for all 91 (the unknown value is the literal `...`). With a real value: 66; unknown: 25. Formats found (D = digit): `DDDD` 32; `...` (unknown) 25; `DDDD/DDDD` (range) 15; `DDDD.DD.DD.` 12; `DDDD.DD.DD` 5 (full dates, 17); `DDDDs` 1 (`1920s`); `DDDDs (?)` 1 (`1910s (?)`). Restricting to the 74 speakers who appear in a transcript and are in the `.coma`: 60 have a value (27 year, 15 range, 16 full date, 2 decade), 14 unknown. The documentation's 74 speakers equals this set; 77 distinct speaker ids occur in the `.exb` files, 3 of them are not in the `.coma`.

**Q12. Communication fields** (Dolgan): 1a Archive (sound); 1b Start-end time; 2 Published in; 2b Published in (bibtex); 0a/0b Title; 1 Genre; 2a Recorded by; 2b Date of recording; 3 Dialect; 4 Speakers; 5a Transcribed by; 5b Date of transcribing; 5d Time-aligned by; 6a Processed by; 6b Date of processing; 7a/7b/7c Translation into Russian/English/German; 8a Glossed by; 8b Glosses checked; 9a Annotation SeR; 9b SyF; 9c IST; 9d BOR/CS; 9e Top; 9f Foc; 9g ExLocPoss; Country; Region; Settlement; Settlement (LngLat). Over the 136 transcripts:

- `2b Date of recording` has a value for all 136: 126 full years, 10 partial (formats `DDXX`, 6 texts, and `DDDX`, 4 texts, with a literal `X`). By year: 1930 13, 1931 3, 1936 1, 1964 14, 1967 1, 1968 1, 1970 6, 1972 1, 1975 1, 1982 1, 1990 8, 1991 1, 1994 8, 1996 1, 1997 1, 1998 1, 1999 3, 2002 5, 2004 8, 2008 3, 2009 39, 2010 2, 2017 4. (This list covers the 126 full years only; the 10 partial dates are not in it.)
- `1 Genre`: nar 61, flk 51, conv 17, transl 4, sng 2, misc 1 (equals the folder counts).
- `3 Dialect`: 131 have a value, 5 are unknown (`...`). Values: Upper 61; Lower 42; Upper (?) 15; Upper, Lower 6; Anabar 3; Lower (?) 2; Lower, Upper 1; `..., Lower` 1; unknown 5. `Region` is filled for all (Taymyr-area spellings, 5 variants) and does not separate dialects.

**Q13. Source collection.** There is no field that names it. It can be inferred from three fields together, over the 136 transcripts: *Published in* has a value (37 texts; the values I looked at name the Efremov 2000 folklore volume, I did not read all 37) / the sound archive contains `TDNT` (52 texts) / recording year. Combinations: published value, not TDNT, year up to 1999: 36; no published value, TDNT, year up to 1999: 29; TDNT, 2000 to 2006: 12; TDNT with partial year: 10; published value and TDNT, 2000 to 2006: 1; neither, recorded 2007 to 2010: 44 (consistent with the Stapert fieldwork); neither, recorded 2017: 4 (consistent with the 2017 trip; the corpus page calls it a fieldwork trip, the task calls it an experiment). The mapping from these combinations to the four collections is my inference (**UNVERIFIED**). The text id also encodes speaker sigles and a date, but no collection code.

**Q14. Anabar.** Yes in the metadata: 2 speakers have `2 Dialect` = `Anabar` (both appear in transcripts) and 3 texts have `3 Dialect` = `Anabar`: `AnKA_2009_Games_nar`, `AnKA_2009_Story_nar`, `ChAPa_NN1_2009_Taboo_nar`. The region fields do not mention Anabar (all Taymyr-area spellings); three ancestry fields (father or mother) mention Anabar (not used here). **This contradicts the Dolgan documentation, which says the corpus contains only the "core" area and that Anabar Dolgan is not included.** One of them (metadata or documentation) is wrong or the label means something else.

**Q15. Evenki.** 53 speakers, all in transcripts. `4 Date of birth`: 34 unknown (`...`), 19 with a value (14 year, 4 range `YYYY/YYYY`, 1 full date). Sex is marked `unknown` for 12 speakers. `2b Date of recording` is filled for all 612 texts: `DDDD` 335, `DDDX` 237 (decade, literal `X`), `DDDD/DDDD` 30, `DDDD-DDDD` 10. By first four characters, for the 335 full years and 40 ranges (the 237 decade values are not in this list): 1912 10, 1913 203, 1928 29, 1929 10, 1930 22, 1931 21, 1965 11, 2007 22, 2018 8, 2019 39. Evenki texts also carry `3a Dialectal group` and `3b Dialect` (Sym 225, Barhahan 200, Khantayskoye Ozero 80, Taimyr 37, Yerbogachyon 35, Ilimpi 24, Stony Tunguska 10, Nepa (?) 1) and `2 Source type` (archive: written 450, published: written 93, INEL collection: audio 39, archive: audio 30) plus `6 Has audio` (yes 69).

## E. Labels

**Q16. Gloss census.** `gloss_census_dolgan.csv` and `gloss_census_evenki.csv` list every distinct morph-level gloss string exactly as written (after splitting `ge` on `-` and `=`), with its token count and the number of texts it occurs in. Rule used to split them: a label with any lowercase letter is `stem_or_word`; otherwise `grammatical`. Dolgan: 4,703 distinct labels, 176 grammatical, 4,527 stem/word, 173,476 label tokens. Evenki: 5,944 distinct, 636 grammatical, 5,308 stem/word, 213,788 tokens. The rule is crude: all-capital stems (e.g. an acronym) are counted as grammatical, and a stem that is only a number or symbol would be too. Combined labels such as `PL.[NOM]` are one entry. **Withheld:** capitalised stem glosses (people, places, peoples; Dolgan 713 labels with 2,764 tokens, Evenki 1,133 labels with 5,365 tokens) are replaced in the committed CSVs by one summary row each, because some are personal names. The counts above include them. The full lists are local only, in `data/derived/002/`.

**Q17. Case labels** (token counts of the exact morph-level label):

| Label | Dolgan | Evenki |
|---|---|---|
| `NOM` (explicit) | 0 | 0 |
| any label ending `.[NOM]` (zero nominative) | 21,167 | 28,291 |
| `ACC` | 6,608 | 5,483 |
| `ACC.INDEF` | 0 | 0 |
| `ACC.INDF` | 0 | 1,595 |
| `ACC` inside a longer label (e.g. `PRO.1SG.ACC`) | 0 | 2,131 |
| `PART` (partitive) | 111 | 0 |
| `DAT/LOC` (one label) | 5,216 | 4,395 |
| `DAT`, `LOC` alone | 0 | 0 |
| `ABL` | 1,058 | 1,644 (plus `ABL2` 49) |
| `ALL` | 0 | 512 |
| `LAT` | 0 | 2,147 (plus `LAT2` 34, `LAT.ADV` 386) |
| `INSTR` | 928 | 0 |
| `INS` | 0 | 1,341 |
| `COM` | 0 | 0 (`COM1` 458, `COM2` 14, `COM3` 35, `COM4` 4) |
| `PROL` | 0 | 885 |
| `GEN` | 603 | 0 |
| `COMP` (comparative per both documentations) | 40 | 56 |
| `VOC` | 0 | 61 |

Other case-like or case-bearing labels: Dolgan `PROPR` (proprietive, 733 alone and 547 with `.[NOM]`); Evenki `PRO.<person>.[NOM]` and `PRO.<person>.ACC` pronoun labels, `NMLZ.LOC1`, `NMLZ.INS3`, `VBLZ.INS1`, `VBLZ.LOC`. Dolgan has no `ALL`, `LAT`, `COM`, `PROL` labels in `ge`.

**Q18. Evidentiality.** Tokens whose `ge` contains `EVID` or `INFER`:

| | Dolgan | Evenki |
|---|---|---|
| tokens | 89 | 29 |
| `EVID` | 53, all the particle `mp` `eːt` (part of speech `ptcl`) | 28: `rkə` as `EVID.[3SG]` 17, `EVID` 10, `EVID.[PN]` 1 |
| `%EVID` (unsure) | 0 | 1 (`kčə`) |
| `INFER` | 36, all `mp` `TAK`, in the mood slot `v:mood` | **0** |

Full token lists (with `mb`, `mp`, `mc`, free translation) are in `data/derived/002/evid_infer_tokens_<corpus>.csv`, which is local only and git-ignored, because it would exceed the 30-line excerpt limit. Excerpt, 10 lines per corpus:

```
eːt | mb eːt | mp eːt | ge EVID | mc ptcl | “And that's a big award, though.”
bɨraktaga | mb bɨrak-tag-a | mp bɨrak-TAK-tA | ge throw-INFER-3SG | mc v-v:mood-v:poss.pn | “– He has thrown away something, apparently, maybe the alcohol is leaking.”
kaːllakpɨt | mb kaːl-lak-pɨt | mp kaːl-TAK-BIt | ge stay-INFER-1PL | mc v-v:mood-v:poss.pn | “Then by learning we apparently also gained experience.”
et – | mb et | mp eːt | ge EVID | mc ptcl | “That was the only way to have fun – with tales.”
eːt. | mb eːt | mp eːt | ge EVID | mc ptcl | “At ours as well, I know that my parents have put children's clothes there.”
eːt, | mb eːt | mp eːt | ge EVID | mc ptcl | “Now he goes to kindergarten, I stopped bothering.”
eːt." | mb eːt | mp eːt | ge EVID | mc ptcl | “I do know that, though."”
terinnegiŋ | mb terin-neg-i-ŋ | mp terin-TAK-I-ŋ | ge prepare-INFER-EP-2SG | mc v-v:mood-v:(ins)-v:poss.pn | “Then you should do it yourself."”
kellegej? | mb kel-leg-e=j | mp kel-TAK-tA=Ij | ge come-INFER-3SG=Q | mc v-v:mood-v:poss.pn-ptcl | “"How does a shaman of the lower world dare to come here without an order?!”
oŋordogo. | mb oŋor-dog-o | mp oŋor-TAK-tA | ge make-INFER-3SG | mc v-v:mood-v:poss.pn | “He brought trouble to his own people.”
```
*Source: Dolgan corpus, files: `AkEE_19900810_PearlBeard_flk.exb`, `BaRD_1930_ChildOfMasterOfMountain_flk.exb`, `BaRD_1930_DaughterOfUrungAjyy_flk.exb`, `BeEI_KuNS_1998_Teacher_conv.exb`, `ChGS_UoPP_20170724_SocCogDesc_conv.exb`, `ChSA_KuNS_2004_ReindeerHerding_conv.exb`, `ElBK_KuNS_2004_Storytellers_conv.exb`, `PoIP_ErAI_2009_LifeNomadize_conv.exb`, `PoPD_KuNS_2004_Life_conv.exb` (tx | mb | mp | ge | mc | free translation en)*

```
birkə. | mb bi-rkə | mp bi-rkə | ge be-EVID.[3SG] | mc v-v:mood2.[v:pn2] | “It was evidently (…).”
juːrkəl", | mb juː-rkə-l | mp juː-rkə-l | ge go.out-EVID-PL | mc v-v:mood2-v:(num) | “"Where did they come out", they said, "how did they lock them up?"”
juːrkəl. | mb juː-rkə-l | mp juː-rkə-l | ge go.out-EVID-PL | mc v-v:mood2-v:(num) | “There they went out apparently.”
dəɣilisirkəl | mb dəɣ-i-l-i-si-rkə-l | mp dəg-i-l-i-sin-rkə-l | ge fly-EP-INCH-EP-INCEP1-EVID-PL | mc v-v:(ep)-v>v-v:(ep)-v>v-v:mood2-v:(num) | “There the devils flew up apparently, who knows.”
birkə | mb bi-rkə | mp bi-rkə | ge be-EVID.[3SG] | mc v-v:mood2.[v:pn2] | “Then the human (forgot(?)), how many years it was I don't know, there with that one.”
```
*Source: Evenki corpus, files: `BTV_20190819_Father_nar.exb`, `YUK_2007_CrazyMan_nar.exb`, `YUK_2007_Ngamundu1_nar.exb` (tx | mb | mp | ge | mc | free translation en)*

**The two forms named in the task.** (a) `-BIt` / postterminal: in the Dolgan `mp` tier the morph spelled `BIT` (capital T) is glossed `PST2` in the tense slot (2,415 words) and `PTCP.PST` in the participle slot (714 words); the morph spelled `BIt` (lowercase t) is `1PL` (the possessive or predicate person ending). The corpus calls `BIT` "past tense 2" in its abbreviation list; the word "postterminal" does not occur in the Dolgan documentation (**so I cannot confirm that `PST2` is the label web Claude means**). (b) `-DAK` / inferential: no `DAK` morph exists in `mp`. The archiphonemic spelling is `TAK`, and the same `mp` morph `TAK` carries three different glosses: `COND1` (555 tokens), `INFER` (36), and `PTCP.COND` per the documentation's affix list. So `INFER` cannot be found by form alone; it must be selected by the `ge` label.

**Most common tense and mood labels.** Found through the `mc` slot names (`v:tense`, `v:mood` in Dolgan; `v:tense1`, `v:tense2`, `v:mood1`, `v:mood2` in Evenki), only for words where `mc`, `mp` and `ge` have the same number of pieces (Dolgan 77,093 of 93,404 words with `mc`, `mp`, `ge`; Evenki all). Forms shown as `mb form / mp form`. Counts are tokens; labels with `.[...]` carry a zero person ending.

Dolgan, slot `v:tense` (11,037 tokens): `PST1` 3,009 (`t / TI`, `ti / TI`), `PRS` 2,563 (`el / Ar`, `a / A`), `PST2` 2,415 (`bit / BIT`, `bɨk / BIT`, `bik / BIT`), `FUT` 1,047 (`ɨ͡ak / IAK`, `u͡ok / IAK`, `i͡ek / IAK`), `PRS.[3SG]` 926 (`er / Ar`, `ü:r / Iːr`). Slot `v:mood` (1,631 tokens): `COND1` 555 (`dek / TAK`), `HAB` 349 (`čči / AːččI`, `aːččɨ / AːččI`), `IMP.2PL` 268 (`ŋ / ŋ`), `HAB.[3SG]` 102 (`aːččɨ / AːččI`), `IMP.3SG` 87 (`lin / TIn`, `lun / TIn`). Imperative singular is a zero morph on the verb (`see.[IMP.2SG]`).

Evenki, slot `v:tense1` (17,442 tokens): `AOR` 11,559 (`ča / rə`, `rə / rə`, `i / rə`), `AOR.[3PL]` 3,938 (`rə / rə`, `tə / rə`), `FUT.IMM` 1,492 (`dʼa / dʼəː`), `AOR.[PN]` 374 (`da / rə`, `a / rə`), `FUT.IMM.[3PL]` 54 (`čurə / dʼəː`). Slot `v:tense2` (6,331): `PST` 2,966 (`ča / čəː`), `PST.[3SG]` 2,559 (`soː / čəː`, `ča / čəː`), `PST.DIST` 483 (`ŋki / ŋkiː`), `PRF` 110 (`nə / nə`), `FUT` 78 (`dʼəŋo / dʼəŋəː`). Slot `v:mood2` (1,017): `HAB` 821 (`pki / wkiː`), `SBJV.[3SG]` 81 (`mčə / mčə`), `SBJV` 66 (`čo / mčə`), `EVID.[3SG]` 17 (`rkə / rkə`), `EVID` 10 (`rka / rkə`). Slot `v:mood1`: `PROB` 56 (`nəː / nəː`).

**Q19. Objects.** In both corpora the `ge` tier marks a nominative-marked (zero-case) object with `.[NOM]` on the last gloss. The `mc` tier is not consistent for this: it shows a case slot as `n.[n:case]` (bracketed, for zero), or as `n-n:case` / `n-n:(num)-n:case` even when `mb` has no case morph (that is why Dolgan `mc` does not align one-to-one). Words with a `SyF` value ending `:O`: Dolgan 1,307 (accusative 1,056; zero nominative `.[NOM]` 216; partitive 23; ablative 1; genitive 1; no case label 8; no gloss 2); Evenki 1,691 (accusative incl. `ACC.INDF` and `PRO.*.ACC` 1,284; reflexive-possessive suffix with no case label 228; zero nominative 119; no case label otherwise 57; `INS` 2; `DAT/LOC` 1). Five examples per corpus of `:O` words with no case suffix, i.e. zero-marked (names avoided):

```
vɨstavkalar | vɨstavka-lar | exhibition-PL.[NOM] | mc n-n:(num)-n:case | np:O
napravlʼenije | napravlʼenije | relocation.[NOM] | mc n.[n:case] | np:O
prikaz | prikaz | order.[NOM] | mc n-n:case | np:O
untajkalar | untajka-lar | fur.boots-PL.[NOM] | mc n-n:(num)-n:case | np:O
zakaːz | zakaːz | order.[NOM] | mc n-n:case | np:O
```
*Source: Dolgan corpus, files: `AkNN_KuNS_200212_LifeHandicraft_conv.exb` (tx | mb | ge | mc | SyF)*

```
hiŋərəkoːr | hiŋərə-koː-r | mouse-DIM1-PL.[NOM] | mc n-n:(eval)-n:(num).[n:case] | np:O
təmu | təmu | raft.[NOM] | mc n.[n:case] | np:O
omoːlgil-əŋəːsil | omoːlgi-l-əŋəːsi-l | boy-PL.[NOM]-strong.man-PL.[NOM] | mc n-n:(num).[n:case]-n-n:(num).[n:case] | np.h:O
oron | oron | reindeer.[NOM] | mc n.[n:case] | np:O
əkun | əkun | what.[NOM] | mc interrog.[n:case] | pro:O
```
*Source: Evenki corpus, files: `BTV_20190815_BoyGoldenNape_flk.exb`, `BTV_20190815_CuckooFox_flk.exb`, `BTV_20190815_Holondyok_flk.exb`, `BTV_20190815_HowokoTorganej_flk.exb`, `BTV_20190821_CreationWorld_flk.exb` (tx | mb | ge | mc | SyF)*

## F. Reconciliation and oddities

**Q20. Counts.** A token is counted in several ways because none of them reproduces the documentation for Dolgan:

| | Dolgan | Documentation | Evenki | Documentation |
|---|---|---|---|---|
| transcripts / texts (`.exb`) | 136 | 136 | 612 | 612 |
| speakers (distinct ids in `.exb` that are also in the `.coma`) | 74 | 74 | 53 | not stated |
| speaker ids in `.exb` speaker tables | 77 | | 53 | |
| utterances: `ref` events | 14,076 | 14,193 | 19,931 | 19,931 |
| utterances: `HIAT:u` in `.exs` / `# HIAT:u` in `.coma` | 14,078 | | (`# INEL:u`) 19,931 | |
| utterances: `fe` events | 14,033 | | 16,947 | |
| tokens: `tx` events (= `# e` in `.coma`) | 97,652 | 97,625 | 93,411 | 93,264 |
| tokens: `tx` events that are not punctuation only | 97,497 | | 93,303 | |
| tokens: `HIAT:w` in `.exs` (= `# HIAT:w` in `.coma`) | 97,757 | | | |
| tokens: `# INEL:w` summed from `.coma` | | | 93,264 | 93,264 |
| tokens: whitespace-split `tx` | 99,318 | | 97,059 | |
| words with an `mb` event | 93,409 | | 92,345 | |

Evenki reconciles exactly when "token" means the `# INEL:w` value in the `.coma` (summed over texts) and "sentence" means a `ref` event. Dolgan does not: the closest values are 97,652 tokens against 97,625 (27 more) or 97,757 against 97,625 (132 more), and 14,076 or 14,078 utterances against 14,193 (115 to 117 fewer). I do not know how the documentation counted; **web Claude should treat the documentation figures as not reproducible from the files** and state which rule it uses. Speakers: the 74 matches only when counting speakers who appear in an `.exb` and in the `.coma`.

**Q21. Oddities.**

- **Parsing and ids.** All 748 `.exb` files parse. No duplicate tier ids, no repeated spans within `tx`, `mb`, `mp` or `ge` tiers, no duplicate timeline ids. No replacement characters or control characters.
- **Texts with no glosses:** none (every text has non-empty `ge` events).
- **Empty tiers.** Many tiers exist but hold no events or only blanks. Dolgan (tier instances): `CS` 163, `Top` 151, `Foc` 151, `BOR-Phon` 146, `IST` 145, `BOR-Morph` 139, `SeR` 128, `SyF` 128, `nt` 95, `ltr` 12, `ExLocPoss` 9, `BOR` 4, `fr` 3, and one speaker with an empty `mb`, `mp`, `ge`, `gg`, `gr`, `mc`, `ps`, `st`, `stl` set. Evenki: `CS` 602, `BOR-Phon` 560, `IST` 549, `BOR-Morph` 538, `SeR` 489, `SyF` 488, `nto` 194, `fe` 156, `fg` 242, `nt` 101, `BOR` 137, `ltr` 16, `fr` 18, `st` 5, `stl` 4. An empty tier does not mean "no such phenomenon" (see Q7: the tiers exist in all 136 Dolgan texts but only some are annotated).
- **`tx` words with no `mb` event:** Dolgan 4,243, Evenki 1,066. By kind (Dolgan / Evenki): punctuation only 155 / 108; non-speech `((…))` 88 / 38; truncated or parenthesised `(xx-)` 476 / 135; other 3,524 / 785. The "other" words are spread over 82 texts in each corpus; in Dolgan 302 utterances have no glossed word at all and 818 have some. From examples they appear to be Russian words inside the speech and parenthesised repairs (e.g. `kvartʼiːru`, `vsʼo`, `(ha-)`), which is my reading, **UNVERIFIED**.
- **Mixed scripts.** Dolgan: 102 `tx` events contain Cyrillic (101 mix Cyrillic and Latin), 52 `mb` and 59 `mp` events contain Cyrillic. Evenki: 26 `tx` events (all mixed), 26 `mb`, 17 `mp`.
- **`%` and `%%`.** Dolgan `ge`: 23 events exactly `%%`, 77 contain `%%`, 19 have a single-`%` prefix. Evenki `ge`: 122 exactly `%%`, 562 contain `%%`, 1,898 have a single-`%` prefix; also `%` in 4 `mp` and 1 `mb` events. The `%` signs are defined in the Dolgan documentation (Q5).
- **Evenki words without an utterance:** 11 `tx` words are not inside any `ref` span.
- **Three Dolgan `nar` folders contain only a `.eaf` file and no `.exb`.** They are not among the 136 transcripts. Their role (for example whether they are among the 37 audio-only texts) was not checked.
- **Single-speaker files** drop the `-SIGLE` suffix from tier ids (Q2); a parser that expects the suffix will fail on 94 Dolgan and 605 Evenki files.
- **Names inside text.** Personal names appear in the transcript text itself (for example in introductions), not only in the metadata, so free text must not be copied into committed tables.
- **Gloss spelling differs between corpora** (`INSTR` vs `INS`, `ACC.INDEF`/`ACC.INDF`, `DAT/LOC` as one label in both, `COND1`/`COND` and numbered variants such as `DIM1` to `DIM4`, `EMPH3`, `EMPH5` in Evenki). Any shared label list needs a mapping.
- **`SeR` singletons** `Ben`, `poss` and a value without colon in Dolgan look like slips (**UNVERIFIED**).

## What I did not do

- I did not compare annotation content between `.exb` and `.exs`, or check the `_tei.xml` files. - I did not inspect the three `.eaf`-only Dolgan folders. - I did not check `stl`, `nto`, `lte`, `ltg`. - I did not read the Evenki documentation beyond its package description and gloss list, or the Dolgan documentation beyond the passages cited above. - The `mc` slot analysis (Q18) covers only words where `mc`, `mp`, `ge` align.
