# Study B analysis plan: case change across speaker generations (draft)

Status: **draft, not frozen.** It is frozen at Gate 3, before any outcome is examined. Until then everything here can change. After that, changes need a dated entry in `docs/DECISIONS.md`.

Owner: web Claude writes; Jude and Dustan review.

## Why this design, and what it must not claim

Existing work (details and links in `docs/LITERATURE_LEDGER.md`):
- Siegl (2015) states that Dolgan secondary predication shifted from dative to instrumental marking in the 20th century, under Russian influence. No test of that claim was found.
- Sheifer and Bolshakova (2023, workshop slides, unpublished as far as we found) describe Dolgan object marking as ternary, and say that it spreads to more TAM contexts than in Sakha. Sheifer's profile lists related work in progress.
- Däbritz (2022, 2023) describes three-way object marking in Dolgan (nominative, accusative, partitive) and reports no variation between speakers.

So the contribution is **not** "object marking in Dolgan". It is an **apparent-time test**: does case use differ by speaker birth cohort? The gap is verified as PARTIAL overall and open only for that sub-question.

## Questions

**B1. Secondary predicates.** Among nominal secondary predicates, is the share marked instrumental (versus dative) higher in younger speakers?

**B2. Object marking.** Among objects, does the share of nominative / accusative / partitive marking differ by speaker cohort, after accounting for clause TAM and referent properties? Does the Dolgan system look more like Evenki's (binary) or more like what Sheifer and Bolshakova report for Sakha?

Gate 0 may drop B1 or B2. A dropped question is reported as dropped, with the counts.

## Data

- **Dolgan:** INEL 2.0, only texts with a recorded speaker whose birth year is known. Folklore texts from the published volume [FD 2000] are expected to be out (no audio, unclear speakers, no BOR tier). Confirm in handoff 002.
- **Evenki:** INEL 2.0. No usable age information. Used as a **baseline by dialect and source** for B2 only.
- **Sakha:** not in INEL. Comparison to Sakha comes from the literature only.

## Variables

**Outcome B1:** case on the secondary-predicate nominal: instrumental, dative/locative, other.
**Outcome B2:** object marking: nominative (unmarked), accusative, partitive. Evenki: nominative, accusative, indefinite accusative (`ACC.INDF`). Case labels per corpus are in `shared/inel/config.py`. Dolgan has only 23 partitive objects (handoff 002), so a three-way model may not be estimable. Plan for accusative versus not, and report partitive descriptively.

**Predictor of interest:** speaker cohort (birth-year bins fixed after looking at the speaker distribution, before any outcome). Also try birth year as a continuous variable.

**Covariates (B2):** borrowing (`BOR` tag on the object: several zero-marked objects in 002 are Russian loans, so loan status must be controlled or the analysis restricted to native nouns); clause TAM context (from `pred_labels` in the object table, grouped to match Sheifer and Bolshakova's contrasts; the grouping needs human sign-off); referent properties from tags (`IST` information status, possession, demonstrative, animacy from `SyF`/`SeR`); source collection; genre; dialect.
**Covariates (B1):** source, genre, dialect.

**Grouping variables (random effects):** speaker; text.

## Extraction

**B2 objects:** words with an overt `SyF` item of function `O` (D-025). Built by `case_change/extract_objects.py`. Dolgan has about 1,307, all in the 50 texts with `SyF`. The verb's TAM comes from the clause predicate in the same utterance. SyF is tagged only in main clauses and is optional, so coverage is measured per text and per source before anything else. If many speakers or sources lack SyF, the object sample is biased and we say so.

**B1 candidates:** nominals marked INSTR or DAT/LOC that are not arguments by `SeR` and `SyF`. Handoff 002 showed that `SeR` role `St` is the stimulus of perception verbs, not a secondary predicate, so there is no tag to start from (D-021). The filter will be designed from Siegl (2015)'s criteria, and humans vet every hit. Because the candidate list is small, a human reads every item and codes whether it is a secondary predicate (depictive or resultative). The vetting sheet lists the reading and the free translation.

Both extractors write a `rule_hit` column so that every row can be traced.

## Models (outline)

Tokens from one speaker are not independent, so every model has speaker structure.

- **B2:** a mixed-effects model with a speaker random intercept (and a text intercept if it converges), outcome the object marking category. Binary version first (accusative vs not), then multinomial. If counts are small or categories separate, use a penalised or Bayesian fit instead of dropping terms to make it converge.
- **B1:** if there are enough tokens, a binary mixed model (instrumental vs dative). If not, **do not model**. Report counts by cohort, with exact confidence intervals, and say that the data cannot test the claim.
- **Software:** Python for extraction. R (`lme4`, `brms`) for models (decision D-005, open).

## Robustness checks (fixed in advance)
0. Native nouns only (objects with no `BOR` tag).
1. Leave one speaker out, repeated for every speaker. Does the result survive losing the most prolific speaker?
2. Restrict to one source (for example Stapert fieldwork only) and to one genre.
3. Restrict to texts with complete SyF coverage.
4. Birth year continuous instead of binned.
5. Drop words flagged `align_ok = false`.
6. Compare results with and without the `%` / `%%` uncertain glosses.

## Interpreting age

Apparent time assumes older speakers reflect an earlier state of the language. Reasons for care, all to be discussed in the paper:
- Source, genre and age may be correlated. A result that disappears within a single source is not an age effect.
- Speakers change with age. Without recordings of the same speakers at several times, apparent time cannot separate generational change from age grading.
- Some recordings come from decades apart (TDNT 1970s to 2000s, Stapert 2007 to 2017). Include recording year, not only birth year, and look at what it does to the cohort effect.
- Bilingualism and schooling in Russian differ across generations. The metadata include education and L2. They are candidate covariates, not controls we can trust.
- Siegl's claim concerns the 20th century. A cohort effect in the corpus does not establish that change occurred, only that it is consistent.

## Power
Before examining outcomes, simulate data with the real number of speakers per cohort and tokens per speaker to find what effect size the design could detect. State it in the paper. A null result with no power statement is uninformative.

## Reporting
- Counts by cohort and source, as a table.
- Per-speaker proportions, plotted, so readers see the variation behind any model.
- Model tables with intervals.
- Every example sentence with its text ID.
- A limitations section built from the checks above.

## Decisions needed
- Cohort bins (after Gate 0).
- Whether B1 survives (Gate 0).
- Stats stack (D-005).
- TAM groupings for B2 (gloss map).

## Competitors to watch
Sheifer (object marking in Dolgan; epistemic modality), Dartmouth. The INEL team (Hamburg). Check at each milestone and before submission. Contact before submitting.
