# Corpus notes: INEL Dolgan 2.0 and INEL Evenki

Facts taken from the corpus documentation PDFs and repository pages, as read on 2026-11-04. Nothing here comes from inspecting real files yet. Handoff 002 will confirm or correct it.

**Important:** the Evenki details below come from the **1.0** documentation (the 2.0 documentation PDF was not reachable). Label inventories may differ in 2.0.

## Sources
- Dolgan 2.0 documentation: https://s3-uhh.lzs.uni-hamburg.de/gwiss-inel-corpora/remote/dolgan-2.0/documentation/INEL_Dolgan_Corpus.pdf
- Dolgan 2.0 handle: https://hdl.handle.net/11022/0000-0007-F9A7-4 (published 2022-11-30; Däbritz, Kudryakova, Stapert)
- Evenki 1.0 documentation: https://s3-uhh.lzs.uni-hamburg.de/gwiss-inel-corpora/remote/evenki-1.0/documentation/INEL_Evenki_Corpus.pdf
- Evenki 2.0 record: https://www.fdr.uni-hamburg.de/record/16605 (DOI 10.25592/uhhfdm.16605; published 2024-12-31; Däbritz, Gusev, Stoynova)
- Project page: https://inel.corpora.uni-hamburg.de/ ; contact inel@uni-hamburg.de
- Licence: CC BY-NC-SA 4.0 for INEL corpora

## Size

| | Dolgan 2.0 | Evenki 2.0 | Evenki 1.0 |
|---|---|---|---|
| Transcripts | 136 glossed | 612 | 251 |
| Speakers | 74 | not stated | 41 |
| Utterances | 14,193 | 19,931 | 9,765 |
| Tokens | 97,625 | 93,264 | 47,778 |
| Linked audio | 100 transcripts, 14:15:28 | 69 transcripts, 3:58 | same |

Dolgan genres: 61 narrative, 51 folklore, 17 conversation, 4 translation, 2 songs, 1 miscellaneous.
Dolgan also has 37 **unglossed** audio files (10:00:36 total: 28 TDNT, 9 Stapert). They are not part of the glossed counts and are of no use without transcription.
Evenki 2.0 by dialect: Northern 34,931 tokens (176 texts); Southern sh-dialects 55,674 tokens; Southern s-dialects 2,659 tokens (11 texts).

## Dolgan sources (what the texts are)
1. Published folklore, "Fol'klor Dolgan" (Efremov 2000), abbreviated [FD 2000]: no audio, and the BOR tier is **not** filled for these texts.
2. Recordings from the Taymyr House of Folk Art (TDNT), Dudinka, 1970s to 2000s, transcribed by native speakers.
3. Eugénie Stapert's fieldwork, 2007 to 2010.
4. Recordings from a 2017 social-cognition experiment (Stapert and Däbritz).

Some Stapert texts were glossed in Toolbox and re-imported, so glossing workflow differs by source.

## File layout (Dolgan, per the documentation)
- Folder `DolganCorpus/` with genre folders `conv`, `flk`, `misc`, `nar`, `sng`, `transl`, plus `documentation/` and one metadata file `dolgan.coma`.
- Each genre folder has one subfolder per communication with `*.exb` (transcript), `*.exs` (segmented transcript, used for search and counts) and `*.wav` if audio exists.
- Format: EXMARaLDA XML. Audio: WAV mono 44.1 kHz 16-bit; MP3 also supplied.
- Download packages: complete, mp3-only, no-audio.

## Tiers (Dolgan 2.0, Table 2)

| Tier | Content |
|---|---|
| ref | communication code and sentence number |
| st / stl | source transcription (Cyrillic / Latin) |
| ts | main transcription, sentence level |
| tx | main transcription, word level |
| mb | morpheme breaks (surface forms) |
| mp | underlying morphophonemes |
| ge / gg / gr | glosses in English / German / Russian |
| mc | morphological category |
| ps | part of speech |
| SeR, SyF | semantic roles, syntactic functions (optional) |
| IST, Top, Foc | information status, topic, focus (optional) |
| BOR, BOR-Phon, BOR-Morph | borrowing source and type, phonological and morphological adaptation (optional) |
| CS | code-switching (optional) |
| ExLocPoss | existential, locative, possessive predication (optional) |
| fe / fg / fr | free translation in English / German / Russian |
| ltr | literal Russian translation |
| nt | notes |

The Evenki 1.0 documentation lists the same tier names. Its annotation principles derive from the Nganasan Spoken Language Corpus.

## Tag inventories (Dolgan 2.0)
- **SeR and SyF** use `<form.animacy:role>`. Forms: `0.1.`, `0.2.`, `0.3.`, `adv`, `np`, `pp`, `pro`. Animacy: `h` for human. SeR roles: A, B, Cau, Com, E, G, Ins, L, Path, P, Poss, R, So, St, Th, Time.
- **SyF subjects and objects:** `pro.h:S`, `pro:S`, `np.h:S`, `np:S`, `0.1.h:S`, `0.2.h:S`, `0.3.h:S`, `0.3:S`, and the same with `:O`. Predicates: `v:pred`, `n:pred`, `adj:pred`, `pro:pred`, `ptcl:pred`, `cop`. Subordinate clauses: `s:comp`, `s:rel`, `s:temp`, `s:cond`, `s:adv`, `s:purp`.
- **IST:** `giv-active`, `giv-inactive`, `accs-sit`, `accs-aggr`, `accs-inf`, `accs-gen`, `new`; zero referents prefixed `0.`; direct speech adds `-Q`; utterance predicates `quot-sp`, `quot-th`.
- **Top:** `top.ext`, `top.int.concr`, `top.int.concr.contr`, `top.int.abstr`. **Foc:** `foc.wid`, `foc.int`, `foc.nar`, `foc.contr`, `foc.ver`.
- **BOR:** `<LANG>:<type>`; languages RUS, EV, MONG, NGAN; types `:cult`, `:core`, `:gram`, `:mod`, `:disc`.
- **ExLocPoss:** `Domain:Strategy.Polarity`; domains Ex, Loc, Poss; strategies Zero, Cop, Ex, PosV; polarity Aff or Neg.

## Gloss labels

**Dolgan 2.0, Appendix 1**
- Case: NOM, ACC, DAT/LOC, ABL, GEN, COMP (comparative), INSTR, PART (partitive). No separate comitative label is listed.
- Evidentiality: EVID (evidential particle), INFER (inferential). No label for the postterminal is listed. Which label it carries is a question for handoff 002.
- TAM and mood: PRS, PST1, PST2, FUT, HAB, ITER, FREQ, INCH, PFV, MOM, INTL, IMP, ADM, POT, PROB, NEC, COND1, COND2, plus several converbs and participles.

**Evenki 1.0, Appendix 1**
- Case: ABL, ACC, ACC.INDEF, ALL, COM, DAT, DAT/LOC, INSTR, LAT, LOC, NOM, PROL.
- Evidentiality and TAM: EVID, ASP, AOR, FUT, FUT.DIST, FUT.IMM, PST, PST.DIST, HAB, IPFV, PROB, IRREAL, COND, DUR, ITER, INCEP, NEG, NEG.EX.
- The documentation is internally inconsistent (examples use `CVB.COND1` and `IMP.2SG`, which Appendix 1 does not list). Appendix 2 is truncated.

The two corpora therefore do **not** share a case or TAM label set. Comparison needs a mapping (`shared/config/gloss_map.yaml`, decision needed).

## Speaker metadata (Dolgan `.coma`)
Name fields, education, occupation, ethnicity, parents and spouse, place of birth (with coordinates), region, date of birth, date of death, residences, **L1 and L2 with dialect** (codes dlg, evn, nio, rus, sah). A sex field is not listed. Derived tables must keep only: speaker ID, birth year, L1/L2, region (decision D-011).

## Communication metadata
Name (`speaker_year_title_genre`), genre, title (English, Russian), recorded by, **year of recording (year only)**, dialect, speakers, who transcribed, translated, glossed, checked and annotated, location (country always Russia), languages, archive reference (TDNT disc and track), start and end time, links.

Evenki: speaker date of birth; recording year (year only); dialect group (Northern or Southern) plus subdialect; archive field (folder and page numbers for Rychkov) and "Published in".

## Caveats the documentation states
**Both corpora**
- Optional tiers are optional. The documents do not say which transcripts carry SyF or SeR. Coverage must be measured.
- Glosses with unsure meaning carry `%`; fully unknown morphemes carry `%%`.
- SyF is tagged **only in main clauses**.

**Dolgan**
- Tier label mismatch: Table 2 writes `BORphon` and `BORmorph`; the text writes `BOR-Phon` and `BOR-Morph`. The parser must accept both.
- BOR is not filled for [FD 2000] texts.
- Information status in direct speech is tagged for the whole communication, not within the quoted speech.
- TDNT literal translations (`ltr`) reflect Dolgan structure and are not standard Russian.
- Glossing workflow differs by source (FLEx vs Toolbox re-import).
- Stoynova (2024) reports inconsistent glossing of Russian items across INEL corpora.

**Evenki**
- Speaker identity is often unknown for the Anisimov (1936) and Rychkov texts, so "41 speakers" is misleading.
- Rychkov metadata are sparse or missing; some dates are guesses.
- Rychkov's diacritics are kept only in the `st` tier, not in the INEL transcription.
- Vasilevich's [±ATR] distinctions are retained.

## What this means for the studies
- **Apparent time works only for Dolgan,** and only for texts with speaker birth years. The folklore texts [FD 2000] have no audio and unclear speaker metadata, so they probably cannot take part. Evenki cannot be analysed by age; it serves as a baseline by dialect and source.
- **Source, genre and age are tangled.** Older speakers probably appear mostly in folklore and TDNT recordings; younger ones in Stapert's conversations and narratives. Handoff 002 and Gate 0 measure how tangled.
- **Annotation consistency differs by source.** Tagging conventions that vary by source look exactly like an age effect if sources differ in age. Analyses must control for source.
- Gopal, Nichols, Károly and Iosad's vowel study used 42 Dolgan speakers born 1912 to 2009 from INEL, so birth years exist for at least that many.

## Open questions for handoff 002
Which label does the postterminal carry? Do `SeR` role `St` and `SyF` tags cover secondary predicates? How many texts have SyF? What formats do birth dates use? Are there Anabar texts? Do Evenki 2.0 labels match 1.0?
