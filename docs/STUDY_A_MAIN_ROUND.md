# Study A: proposal for the main annotation round

Status: **proposal by web Claude, 2026-11-06.** Jude and Dustan own Study A (`evidentiality/`). Accept, change or reject this after the pilot (Gate 2). Nothing here runs until you say so.

## What the paper can claim
Skribnik and Aikhenvald (2024: 1016-1022) describe Dolgan, Sakha and Evenki evidentials qualitatively. No quantitative, corpus-based study of Dolgan evidentials was found (ledger, narrowed-claim queries, 2026-11-06). So the contribution is **how often** each form is used evidentially, **in which genres**, and **how Dolgan compares with Evenki**. Greed (2018) gives a tested path for the *-BIt* past: perfect, then inferential, then mirative with first-person subjects, then a non-witnessed narrative tense. Handoff 009 shows how the corpus glosses alone line up with that path. Your coding adds what the glosses cannot: which uses are evidential.

## Questions
1. For each ambiguous form (`TAK` glossed `COND1`, `-BIt`/`PST2`, copula *e-bit*, *buollaga*, quotative `IST`), what share of tokens carry an evidential reading?
2. Does that share differ by genre (folklore, personal narrative, conversation)?
3. Combined with the gloss counts: how many evidential uses per 1,000 words does each genre have?
4. How do these rates compare with Evenki?

Speaker age and recording period are left out of the confirmatory questions. Evenki has no usable birth years, and the sample per speaker is small. Report them descriptively.

## Sample
The builder already exists (`python3 shared/workbook.py build main ...`). It keeps every tier-1 item, samples tier-2 items per rule spread over speakers, excludes the pilot items, and gives 15% of items to both coders without saying which. Coders see no speaker, birth year or recording year (D-039).

| Part | Items |
|---|---|
| Dolgan tier 1 (`EVID` 53, `INFER` 36) | 89, all |
| Dolgan tier 2, 5 rules × 60 | 300 |
| Evenki tier 1 (`EVID`) | 29, all |
| Evenki tier 2, 3 rules × 60 (`IST_quot`, `evenki_PRF`, `evenki_PTCP_PRF`) | 180 |
| **Total** | **598**, of which about 90 double-coded; about 340 per coder |

Precision for one rule's evidential share with 60 items: about ±13 percentage points (95%, share near one half), ±10 near 0.2. These widths ignore clustering by speaker, so the real intervals will be somewhat wider. With 120 items: ±9 and ±7.

**Proposed change, needs your decision:** for `mp_BIT` (5,538 Dolgan tokens), sample 120 items split evenly between folklore and the other genres, so question 2 can be answered for the most frequent form. This needs a small change to the builder (stratify by genre within one rule). Web Claude makes it if you agree.

**Evenki:** you code from the glosses and the free translation. If that is not enough to judge evidential use, drop Evenki tier 2 and compare only the corpus-glossed `EVID` rates (handoff 009 has them).

## Coding
The codebook is the one you settle at the pilot (`shared/config/evid_codebook.json`). One minute per item is a rough guess. If it holds, that is about six hours per coder.

## Analysis (to fix after the pilot, before the main round is merged)
- Per rule: the share coded evidential, with a speaker-cluster bootstrap interval.
- Per genre: the same, where a rule has at least 20 items in the genre.
- Evidential uses per 1,000 words: gloss rate (handoff 009) × coded share, with the interval carried through.
- Agreement: Cohen's kappa per codebook column on the double-coded items, reported in the paper.
- Dolgan versus Evenki: rates side by side, by genre where both corpora have the genre.

## Timeline
1. Pilot (40 items), merge, revise the codebook: Gate 2.
2. Decide on this proposal; web Claude builds the main sheets; desktop Claude generates them.
3. Code; merge; web Claude writes the analysis script against the merged file.
