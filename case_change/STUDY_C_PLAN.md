# Study C (proposed): is Dolgan's three-way object marking clause-driven, unlike Evenki's?

Status: **pre-specified by web Claude on 2026-11-06, before any Study C output was produced.** The git history of this file is the record of that order. Jude and Dustan can still change it; any change after `reports/study_c_clause_dom.md` exists must be listed under "Changes after data" below, with the reason.

## Why
Sheifer and Bolshakova (2023, workshop slides, no counts; ledger) describe Dolgan object marking as follows. Dolgan chooses by **clause type**. Future, imperative, conditional and modal clauses (capacitive, necessitative, desiderative, hortative, jussive, distant imperative) use a three-way system: accusative for definite objects, partitive for specific indefinites, bare nominative for non-specific ones. Past, present and habitual clauses use a two-way system with no partitive. Evenki, by contrast, chooses by **object** semantics alone (accusative vs indefinite accusative, `ACC.INDF`). They read Dolgan's wide use of the three-way system as Evenki influence. Däbritz (2023: 196) also links Dolgan partitive objects to imperative and prospective clauses, and Matić and Nikolaeva (2024: fn. 1) list partitive or ablative imperative objects as a regional feature of north-east Siberia. Pakendorf and Stapert (2020: Oxford Guide, ch. on Sakha and Dolgan; read 2026-11-06, before any Study C output) disagree in part: the partitive marks "partially affected or indefinite direct objects in the imperative mood", but in Dolgan it is "more widespread" and "can occur with indicative verbs". H2 below therefore decides between two published descriptions. Nobody has counted any of this. The INEL Dolgan and Evenki corpora carry the same object annotation (`SyF` function `O`), so the claims can be tested on two corpora with one method.

Gap status: OPEN, provisional. See `docs/LITERATURE_LEDGER.md`, Study C. Siegl's article on the Dolgan partitive and one *Language Documentation and Description* article could not be read here (handoff 008).

## Data
`objects.csv` for each corpus (built by `case_change/extract_objects.py`). Objects with a predicate found in the utterance (`pred_labels` not empty).

- **Dolgan outcome:** `PART` (1) versus `NOM` or `ACC` (0). Other cases are left out.
- **Evenki outcome:** `ACC.INDF` (1) versus `NOM` or `ACC` (0).

## Clause type, from the predicate's gloss components
Digits are stripped from each component first (`COND1` becomes `COND`, `PST2` becomes `PST`). The first rule that matches wins.

| Clause type | Components |
|---|---|
| irrealis (core) | IMP, FUT, COND, NEC, DEB, SBJV, DESID, POT, CAP, HORT, JUSS |
| realis | PST, PRS, HAB, AOR, NFUT |
| other | anything else (participles without the above, converbs, INFER) |

The extended definition adds INTNS and PROB to irrealis. Their meaning in the INEL glosses is not checked (UNVERIFIED), so they are a sensitivity check only.

## Hypotheses (two-sided, alpha 0.05)
- **H1, Dolgan.** The partitive share is higher in irrealis clauses than in realis clauses.
- **H2, Dolgan, descriptive.** In realis clauses the partitive is rare. Reported as counts, and as the number of speakers who use it there at all. No test.
- **H3, Evenki.** The `ACC.INDF` share does not differ between irrealis and realis clauses. A non-significant result does not show equality, so the estimate is reported next to the Dolgan one.
- **H4, both.** The irrealis-minus-realis difference is larger in Dolgan than in Evenki (the interaction term in a pooled model).

## Test
The same speaker-clustered wild bootstrap as Study B (`speaker_test.adjusted_test`, D-034, D-037), with a 0/1 clause predictor instead of birth year (`scale=1`). The estimate is the difference in percentage points. Each test is adjusted for genre. H4 pools the two corpora, with language, clause type and genre as controls, and tests the term "irrealis and Dolgan". 9,999 bootstrap draws. Speakers are the clusters; Evenki speakers have no usable birth years, but they have IDs.

## Robustness (fixed in advance)
1. Extended irrealis definition.
2. No pronoun objects.
3. Unadjusted (no genre control).

## Limits, stated in advance
- The corpus glosses are the annotators' analyses, not ours. A clause type with almost no partitive could reflect glossing practice.
- Specificity, which drives the choice in both descriptions, is not annotated. Clause type is only its proxy here, as in Sheifer and Bolshakova's account.
- The Dolgan partitive is rare (111 `PART` tokens in the whole corpus, handoff 002), so H1 may have low power. The script reports the counts so this is visible.

## Changes after data
(none)
