# Study B, second round: generations compared within one genre, on the expanded corpus

Status: **draft by Claude, 2026-11-07, before any reviewed label exists.** To freeze it, Jude and Dustan read it, change what they disagree with, and replace this line with `Status: **frozen YYYY-MM-DD by Jude and Dustan**`. Freeze before `merge_review.py` is run on the main review queue (handoff 012, step 3). The git history is the record of that order.

## Why a second round
- **B2 and B3 (frozen plan, handoff 011) found no change in object case or word order across birth years.**
- **Study D showed the corpus could not have found change in Russian borrowing either.** Unadjusted, Russian words rise by 1.4 points per decade (p = 0.0004). Adjusted for genre and source, the difference disappears (p = 0.71), because the oldest speakers are recorded almost only in published folklore.
- **So the first round could not separate generation from genre.** The way out is to compare generations **within one genre**, which needs more tagged text per genre. The tagger (D-042) and the review (handoff 012) supply it.
- **This is a new test, not a re-analysis of B2.** B2 stays as reported.

## Data
- **INEL-tagged objects:** the current `objects.csv`, 50 texts.
- **Reviewed objects from the 86 untagged texts:**
  - `to_syf.py` writes labels back as SyF tags, and `extract_objects.py` then builds the expanded object table with no changes to the study code.
  - Words flagged by the model carry the coders' decision.
  - The remaining words carry the model's label: confident non-objects, and confident accusative objects.
  - Disputed or unsure words stay unlabelled until resolved.
- **Label source:** every object has `syf_source` = inel, human or model.
- **Only speakers with a usable birth year,** as in B2.

## Preconditions, checked before the outcome is read
1. Calibration (handoff 012, step 1): each coder's kappa with INEL on S/O/neither is at least 0.70. If not, revise the coding guide and recalibrate.
2. Batch 1 of the review queue is complete: narrative and conversation from speakers with a birth year.
3. The two coders' kappa on the overlap items is reported, whatever its value.

## Questions and tests
All use the B2 test unchanged: a speaker-clustered linear probability model, a wild cluster bootstrap with the null imposed, Webb weights, 9,999 draws, two-sided (D-034, D-037).

- **B2x, primary.** Within **narrative** texts, does the share of accusative objects (versus NOM or PART) change with birth year? Adjusted for source and label source (inel vs reviewed).
- **B3x, primary.** Within narrative texts, does the share of verb-before-object order change with birth year? Same adjustment. Objects in utterances with one predicate, as in B3.
- Holm correction over B2x and B3x.
- **Secondary, uncorrected:**
  - the same two tests within **conversation**;
  - all genres, adjusted for genre, source and label source;
  - recording year instead of birth year (narrative).
- **Robustness, fixed now:**
  - INEL-tagged texts only;
  - reviewed texts only;
  - human-decided objects only (drop words that carry a model label);
  - leave one speaker out (999 draws);
  - without Anabar texts.
- **Support for change** is defined as in B2: Holm p < 0.05, the same sign in every robustness row that can be run, and the same sign in every leave-one-out run.
- **The decision rule on collinearity** is as in B2, applied within the genre to source and label source.

## Not tested here
- **D1 (overt pronoun subjects) waits.** It needs zero subjects, which the review does not check: the model finds them with macro-F1 0.77, which is too noisy for a confirmatory test. A D1 round needs its own review of zero subjects first.
- **B1 is unchanged.** It depends on the vetting of secondary-predicate candidates.

## Power (design only)
Filled from `reports/power_expansion.md` (expected objects from the tagger's calibrated probabilities; no case read). See the "Design facts" section added after that run.

## Limits, stated now
- **The coders see case endings while they review.** They decide by meaning, and they cannot see speaker or date, but their judgement of unmarked objects is the hardest part. The label-source control and the human-only robustness row are there for this.
- **The model labels remain for confident words.** On held-out texts, after review at threshold 0.9, object F1 is about 96 and 91–100% of unmarked objects are found. The residual errors are not shown to differ by birth group (`reports/tagger_eval.md`), but the groups are small.
- **Apparent time still cannot separate change from age grading.**

## Changes after freezing
(none)
