# Study B analysis plan: case change across speaker generations

Status: **draft, ready to freeze.** To freeze it, Jude and Dustan read it, change what they disagree with, and replace this line with `Status: **frozen YYYY-MM-DD by Jude and Dustan**`, then commit. `case_change/b2_test.py` refuses to read the outcome until that line exists. After freezing, every change needs a dated entry under "Changes after freezing" and in `docs/DECISIONS.md`.

Owner: web Claude wrote it (2026-11-06); Jude and Dustan decide.

## Before freezing: checklist
1. Handoff 007 is done. Copy its collinearity table into "Design facts" below, and apply the decision rule in "Primary test".
2. D-034 and D-037 (the test) and D-013 (the descriptive bins below) are confirmed or changed in `docs/DECISIONS.md`.
3. Nobody has looked at object case by birth year or recording year. Gate 0 and the power report show design counts only (D-026). Study C reads case by clause type, not by time (D-038).

Artem'ev (1999) is still unread (handoff 004, item 3b). It does not block the freeze. It blocks the novelty claim in the paper.

## What is new, and what the paper must not claim
Details and links in `docs/LITERATURE_LEDGER.md`.
- Siegl (2015) asserts that Dolgan secondary predicates moved from dative to instrumental marking in the 20th century. He gives two examples, no counts and no criteria.
- Däbritz (2022, 2023), Sheifer and Bolshakova (2023, slides) and Siegl (on the partitive) describe three-way object marking (nominative, accusative, partitive). None reports variation between speakers or over time.
- Stapert (2013) checks speaker age only for stem variants of relational nouns (pp. 187-188, no counts by age) and for OV/VO word order (Table 7.3). Neither is case marking (handoff 005).

So the contribution is the **first test of whether Dolgan case marking differs by speaker birth year (apparent time) and by recording year (real time)**, in a corpus, with the speaker as the unit. It is not a description of the case system.

## Questions
- **B2, objects (confirmatory).** Does the share of accusative-marked objects change with speaker birth year, once genre and source are held constant?
- **B3, word order (secondary study).** Does the share of verb-before-object order change with birth year? See B3 below.
- **B1, secondary predicates.** Among nominal secondary predicates, does the share marked instrumental (versus dative) change with birth year or recording year? Confirmatory only if the vetting yields enough items (see B1 below). Otherwise descriptive.

No direction is predicted for B2. The literature gives no prediction, and Russian contact could push either way. All tests are two-sided.

## Data
- **Corpus.** INEL Dolgan Corpus 2.0, objects from the 50 texts with `SyF` annotation (`case_change/extract_objects.py`; D-025). 1,307 objects; 997 from 25 speakers with a usable birth year (range of 10 years or less), 2026-11-05 run.
- **Analysis set (B2).** Objects whose case is `NOM`, `ACC` or `PART`, from speakers with a usable birth year. Other cases and the reflexive-possessive objects without a case label are left out.
- **Evenki** has no usable birth years and is not used in B. The cross-language question is Study C (`case_change/STUDY_C_PLAN.md`).

## Design facts (from Gate 0 and the power report; counts only)
- Birth years of speakers with objects run from the 1890s to the 2000s. The speakers born after 1970 give 4 to 8 objects each, one speaker per decade.
- Birth year is tangled with source and genre. Speakers born before 1920 appear almost only in `published_folklore` and genre `flk`. Speakers born after 1950 appear only in fieldwork and the archive, mostly `nar` and `conv`.
- `SyF` exists in 50 of 136 texts: 27 `TDNT_archive`, 18 `published_folklore`, 3 `fieldwork_2007_2010`, 2 `fieldwork_2017`.
- Collinearity (share of the object-weighted variance of birth year explained by the controls), from `reports/power_b2.md` after handoff 007: genre ___ ; genre + source ___ . Recording year: genre ___ ; genre + source ___ .
- Power of the primary test at odds ratio 1.5 per decade, speaker SD 0.5 / 1.0: ___ / ___ (from the same report).

## Primary test (B2)
- **Outcome.** 1 if the object is `ACC`, 0 if `NOM` or `PART`.
- **Model.** Linear probability model at the object level: outcome on birth year (decades) plus genre and source dummies. Standard errors are clustered by speaker. The p-value comes from a wild cluster bootstrap with the null imposed and Webb weights, 9,999 draws, seed 20261105 (`speaker_test.adjusted_test`, D-034, D-037). A control level that adds nothing is dropped automatically.
- **Estimate.** Change in accusative share, in percentage points per decade of birth year.
- **Why adjusted.** In a simulated design with the same tangle, an unadjusted test reported a birth-year trend 50 to 70% of the time when only genre had an effect. The adjusted test stayed at 4 to 5% (D-037).
- **Decision rule, fixed now, applied by `b2_test.py` itself.** The script computes, on the analysis set and from the design only, the share of birth-year variance explained by genre + source. If it is 0.90 or more (1.0 when a control duplicates birth year), the primary test adjusts for genre only. If that is also 0.90 or more, B2 has no confirmatory test: the script labels the row "NOT CONFIRMATORY" and the paper reports the descriptive tables and says the corpus cannot separate generation from genre. The same rule applies to B3. The power report (`power_b2.md`, `--min-tokens 1`) shows the same numbers in advance.
- **What counts as support for change.** The primary p is below 0.05, **and** the estimate has the same sign in every robustness check that can be run (rows with "too few speakers" do not count), **and** the leave-one-speaker-out estimates keep that sign. If p is below 0.05 but a robustness check reverses the sign, the paper reports a fragile result, not change.
- **What a null result means.** Report the estimate and the smallest odds ratio with power 0.8 from `reports/power_b2.md`, and say that effects smaller than that cannot be ruled out.

## Secondary tests (B2), reported with their p-values, no correction, labelled secondary
All in `case_change/b2_test.py`, in this order:
1. Unadjusted birth-year test (to show what the adjustment does).
2. Adjusted for genre only.
3. Real time: recording year instead of birth year, adjusted for genre and source. Apparent and real time are never combined into one variable.
4. Partitive: outcome `PART` versus `NOM` or `ACC`. Dolgan has few partitive objects, so this may be uninformative; report counts.
5. Adjusted for genre, source and clause TAM group (`config.TAM_GROUPS`, D-032), because Däbritz (2023) and Sheifer and Bolshakova tie the partitive to clause type.

## Robustness checks (primary model, fixed in advance)
1. Native nouns only (no `BOR` tag, including multi-word `BOR` events, D-036).
2. No pronoun objects.
3. Well-aligned glosses only, without `%` or `%%` glosses.
4. Exact birth years only (precision `year` or `date`).
5. Without Anabar texts (D-019).
6. Each source on its own, adjusted for genre (sources with fewer than 5 speakers are skipped).
7. Leave one speaker out, for every speaker (999 bootstrap draws each).

## B3, word order (added 2026-11-06, before any word-order output)
- **Question.** Does the share of objects that follow their verb (VO) change with birth year? Stapert (2013: 257-258, Table 7.3) compared OV and VO across three age groups of one or two speakers each and found no age pattern. Pakendorf and Stapert (2020) attribute Dolgan's looser word order to Russian. Udmurt shows a generational shift toward VO under Russian contact (Asztalos, Benjamins IMPACT 50; Belova and Khomchenkova 2026). Ledger: B3.
- **Data.** Objects in utterances with exactly one `SyF` predicate (`n_preds_in_utt` = 1), from speakers with a usable birth year, any case. With more than one predicate, the object table's nearest-predicate rule cannot say which verb the object belongs to.
- **Outcome.** 1 if the predicate comes before the object (`pred_position` = `before`), else 0.
- **Primary test.** The B2 model: birth year, adjusted for genre and source, wild cluster bootstrap by speaker; the same decision rule on collinearity. Two-sided.
- **Secondary rows.** Unadjusted; recording year adjusted for genre and source; no pronoun objects.
- **Caveat.** `SyF` is tagged in main clauses only, and published folklore may have been edited toward a written norm. The source-adjusted model takes part of this into account; the paper must state the rest.

## B1, secondary predicates
- **Candidates.** `case_change/extract_b1.py`, rules from Siegl (2015)'s examples (D-033, D-035): 767 candidates from 67 speakers (handoff 006).
- **Vetting comes first.** Jude and Dustan code every candidate separately in the B1 sheets. The sheets show the sentence and translation, **not** the speaker's birth year or the recording year, and coders do not look them up. Agreement (kappa) is reported. Only items both accept as a nominal secondary predicate enter the analysis, and disagreements are resolved by discussion before any outcome is computed.
- **Outcome.** 1 if instrumental, 0 if dative/locative, among accepted items.
- **Tests.** The same model as B2: birth year, adjusted for genre (source too if it is not redundant); and recording year, adjusted for genre. Both two-sided.
- **Script.** `case_change/b1_test.py`, on the merged vetting file. A `resolved` column, added while discussing disagreements, overrides the two codes.
- **Minimum.** At least 30 accepted items from at least 10 speakers with a usable birth year. Below that, B1 is descriptive only: counts by decade of birth and by recording period, with exact binomial intervals, and the statement that the corpus cannot test Siegl's claim.

## Descriptive tables (not tests)
- **Birth bins (D-013 proposal), chosen from the speaker distribution before any outcome.** Before 1920; 1920 to 1939; 1940 to 1959; 1960 and later. From the Gate 0 object table, these hold roughly 185, 568, 88 and 156 objects.
- **Recording bins.** Before 1980; 1980 to 1999; 2000 and later.
- Counts of `NOM`, `ACC` and `PART` by bin, and by bin and genre.
- Each speaker's accusative share against birth year, with the number of objects, so readers see the variation behind the model.

## Interpreting age
- **Apparent time.** It assumes older speakers keep an earlier state of the language. It cannot separate generational change from changes in a person's speech over their life (age grading). Recording year is the only real-time check we have.
- **Genre and source.** Even after adjustment, folklore by old speakers and conversation by young speakers differ in ways the dummies may not capture (register, editing of published texts). The source-only checks show how much this matters.
- **Bilingualism and Russian schooling.** These differ by generation. The metadata have L1 and L2, but they are too sparse to control for. Discuss them; do not claim them as causes.
- **Siegl's 20th-century dating.** A birth-year effect in the corpus is consistent with change. It does not date it.

## Software
Python standard library only (D-005 settled for the confirmatory tests by D-034/D-037). If R becomes available, a mixed logistic model with a speaker random intercept may be added as a sensitivity analysis, labelled as added after freezing.

## Competitors to watch
Sheifer (Dartmouth; object marking and modality in Dolgan) and the INEL team. Check again before submission, and contact them before submitting.

## Changes after freezing
(none)
