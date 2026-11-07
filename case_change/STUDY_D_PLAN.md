# Study D: three possible Russian-driven shifts in Dolgan, by speaker birth year

Status: **pre-specified 2026-11-06 ~19:20 Pacific by Claude at Jude's request, before any Study D output existed.** The git history of this file is the record of that order. The script `case_change/russian_shift.py` was committed together with this plan and run once afterwards. Every change after `reports/study_d_russian_shift.md` exists goes under "Changes after data", with the reason.

## Honest context
- This plan was written **after** the B2/B3 result (no change in object case or word order, handoff 011) was known. B2 and B3 are not changed, rerun or redefined. Study D asks three different questions about different variables. None of their outcomes had been looked at by birth year or recording year before this plan was committed.
- What had been seen before: corpus-wide label counts (how many tokens carry `CVB`, `PST1`, `PST2`, `BOR`, zero subjects; no split by speaker or time), and the Study A gloss descriptives (PST2 share by **genre** and **person**, handoff 009, not by birth year or recording year).
- Three hypotheses are tested, so the p-values are corrected (Holm). The positive control is reported separately and not counted.
- Jude and Dustan had no time to review this before the run (11:59 pm deadline, 2026-11-06). They may reject it afterwards; the paper must then say so.

## Why these three
Russian is dominant for Dolgan speakers born after about 1970 (Stapert 2013: 263-264, Table 7.4). Each hypothesis is a place where Russian and Dolgan differ, so shift could show up as change across birth years.

| | Question | Russian | Dolgan | Link to our studies | Literature |
|---|---|---|---|---|---|
| **D1** | Do younger speakers use more overt personal-pronoun subjects instead of dropping them? | Overt pronoun subjects are the norm in most clauses | Pro-drop; the verb's person ending identifies the subject | Argument realisation, like B2 and B3; same `SyF` texts | Nobody has counted it by age (ledger, Study D). Stapert (2013: 310) only notes that Sakha is pro-drop |
| **D2** | Do younger speakers use the indirect past PST2 (*-BIt*) less, relative to the direct past PST1 (*-TI*)? | No evidential or indirective past | PST2 vs PST1 marks indirectivity (Skribnik and Aikhenvald 2024: 1018) | Study A (evidentiality) | Not counted by age anywhere we found |
| **D3 (long shot)** | Do younger speakers use fewer converbs (clause chaining), on the Russian model of finite clauses joined by conjunctions? | Finite clauses and conjunctions | Converbs chain clauses (Turkic type) | Stapert (2013: 317, ch. 8) | Stapert (2013: 317) says Dolgan has fewer converbal clauses than Sakha "on the surface", and offers two explanations: ongoing shift, or an older lingua-franca style. She has no counts by age. D3 decides between the two: shift predicts a decline with birth year; the older explanation predicts none |
| **PC** (positive control, not a hypothesis) | Do younger speakers use more Russian-origin words? | | | Shows whether this corpus and design can detect a Russian-driven difference at all. If PC is null too, nulls in D1 to D3 mean little | Stapert (2013: 293) says Russian coordinators are used "by all age groups"; no counts by age |

Directions are predicted (D1 up, D2 down, D3 down, PC up), but all tests are **two-sided**.

## Data
Dolgan only, INEL Dolgan Corpus 2.0, tables built by `shared/build_tables.py` (`tokens.csv`, `texts.csv`, `speakers.csv`). Speakers with a usable birth year (range of 10 years or less), as in B2.

## Units and outcomes (exact rules, in `case_change/russian_shift.py`)
- **D1, subjects.** Texts with `SyF` annotation. Each `SyF` item is `form:function`. A subject is an item with function `S`.
  - Outcome 1: an overt subject whose form starts with `pro` on a token with part of speech `pers` (personal pronoun).
  - Outcome 0: a zero subject (form starts with `0`).
  - Left out: lexical noun-phrase subjects and demonstrative-pronoun subjects.
- **D2, past tense.** All glossed texts. Finite past verbs as in Study A (`shared/evid_descriptives.finite_pasts`): a certain `PST1` or `PST2` component, not both, no `PTCP`. Outcome 1 if `PST2`.
- **D3, converbs.** All glossed texts. Tokens with part of speech `v` and a gloss. Outcome 1 if the gloss has a `CVB` component.
- **PC, Russian words.** All glossed tokens. Outcome 1 if the `BOR` value starts with `RUS` or `%RUS`, or the `CS` value starts with `RUS`.

## Test
The B2 test, unchanged:
- Speaker-clustered linear probability model of the outcome on birth year (per decade), adjusted for genre and source. Wild cluster bootstrap with the null imposed, Webb weights, 9,999 draws, seed 20261106 (`speaker_test.adjusted_test`, D-034, D-037).
- The same decision rule on collinearity: genre + source if they explain under 0.90 of birth-year variance; else genre only; else "NOT CONFIRMATORY".
- Rows with fewer than 5 speakers are not tested.

**Multiplicity.** Holm correction over the three primary p-values (D1, D2, D3). PC is not included.

**What counts as support.** For each of D1 to D3:
1. The Holm-adjusted p is below 0.05.
2. Every leave-one-speaker-out estimate (999 draws each) has the same sign as the primary estimate.

A significant result in the opposite direction from the prediction is reported as such, not as support for Russian influence.

**Secondary rows (reported, not corrected, labelled secondary):** unadjusted; recording year instead of birth year, adjusted for genre and source.

## Descriptive output
Share and count by birth bin (the B2 bins); per-speaker share against birth year.

## Limits, stated in advance
- **Apparent time** cannot separate change from age grading.
- **The glosses and `SyF` tags are INEL's analyses.** D1 depends on how annotators tagged zero subjects; D3 on how they glossed converbs.
- **Genre and register.** Conversation and narrative may differ in pronoun use and clause chaining beyond what the genre dummies capture.
- **Publication.** Published folklore may have been edited toward a written norm.
- **The positive control is not a hypothesis.** A Russian-word increase is expected and is not a discovery by itself, but its size is useful context.

## Changes after data
(none)
