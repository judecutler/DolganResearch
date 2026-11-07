# The IGT argument tagger: design, results and how to scale it

Written by Claude, 2026-11-07 (overnight). Code in `shared/igt_tagger/` and `shared/review_ui/`. Evaluation numbers come from `reports/tagger_eval.md`. No corpus text is in this file or in the report.

## What it does
Input is interlinear glossed text (IGT) in the form INEL uses: one row per word with a transcription, a morpheme gloss line in Leipzig style (`fish-ACC`, `man.[NOM]`, `go-PST-3SG`) and a part of speech. Output is, for every word:
- the probability that it heads a **predicate** (verbal, nominal, adjectival or particle predicate);
- the probability that it sits inside a **subordinate clause**;
- its **argument role**: subject (S), direct object (O) or neither, following INEL's GRAID-based scheme (Haig and Schnell 2014; INEL Dolgan Corpus documentation, section 2.10.3.8): roles are tagged on phrase heads, and only in main clauses;
- for predicates, a **zero subject** and its person (0.1, 0.2, 0.3).

These are the layers our studies need:
- B2 needs object case.
- B3 needs object position.
- C needs objects and clause type.
- D1 needs overt versus zero subjects.

Today these layers exist only in the 50 of 136 Dolgan texts that INEL tagged by hand.

## Design choices, and why

| Choice | Why | Precedent |
|---|---|---|
| Features from the gloss line, not from the words | Glosses use shared Leipzig labels across languages, so the same features work for any glossed corpus | IGT as a cross-lingual bridge: Xia and Lewis; Georgi, Xia and Lewis (projection of structure via IGT) |
| English gloss lemmas as lexical features | INEL glosses every language into English, so "the verb glossed *take* usually has an object" can transfer between languages | as above |
| Two stages: predicates and subordinate clauses first, then roles | Roles are defined relative to the main-clause predicate. Stage 2 is trained on out-of-fold stage-1 guesses, so it learns from the same noise it will meet | Stacked generalisation (Wolpert 1992); pipeline taggers |
| Regularised logistic regression, rare features dropped, C chosen by nested cross-validation | Small data: about 30,000 tagged Dolgan words. Gives calibrated probabilities, which the review queue needs | Standard for small-data tagging |
| Language profiles and feature augmentation | Each feature has a shared copy, a copy for the language's type (word order, affix position, alignment) and a copy for the language. Related languages pool evidence; unrelated ones do not inherit wrong position rules | Daumé III 2007 ("Frustratingly easy domain adaptation") |
| Profile values declared and also estimated from the language's own text | A new language arrives with a profile even if nobody has described it; the estimate checks the declared value | — |
| Context features tuned to the language's grammar | Clause type of the governing verb (object marking depends on it in Dolgan, Study C); predicative zero agreement on nominals (Turkic `[3SG]`); converb versus finite governing verb; noun-phrase shape (only heads are tagged) | — |
| Human review of uncertain words, not full automation | The model is least sure exactly where it matters (unmarked objects). Routing by confidence cuts the work while keeping the hard cases human | Baldridge and Palmer (2009): machine suggestions save annotation time in language documentation, but the best strategy depends on the annotator |
| Unmarked-object rule in the review queue | Every unmarked nominal with P(O) at or above a floor goes to a human, even when the model is confident. Missing unmarked objects more for some speakers than others would fake a change in case marking | Lesson of B2/D: errors that correlate with speaker age create false trends |
| Blind review screen | No speaker, date or text shown, as in the Study A sheets | D-039 |
| Export to JSON, prediction in pure Python | Runs on any computer with Python 3, no installs; training needs scikit-learn once | — |

**What did not help (measured on development texts, Dolgan role macro-F1):**

| Change | Score | Baseline |
|---|---|---|
| Unsupervised verb-transitivity estimates from untagged text | 0.742 | 0.743 |
| Pooling Evenki training data | 0.749 | 0.743 |
| Pooling with augmentation | 0.739 | 0.743 |
| Gradient-boosted trees | 0.751 | 0.743 |

None of these changes is clearly better. The trees are less portable and less well calibrated, so the linear model stays. Pooling and augmentation should matter most when a language has little tagged text; the learning curve in the report tests that.

## Results
Full tables are in `reports/tagger_eval.md`. All numbers are on texts not used for training. "Held-out" means 20% of each language's tagged texts (10 Dolgan, 26 Evenki), set aside before development started.

**Role tagging** (macro-F1 over S and O):
- **Dolgan:** 75.3 on held-out texts, 74.3 on speakers never seen in training, against 57.2 for a rule from case alone.
- **Evenki:** 83.1 held-out, 81.4 for unseen speakers, against 64.2 for the rule.
- **Other layers, Dolgan:** predicates 87.5, zero subjects 77.4, subordinate-clause membership 67.7 (the hardest layer).

**Objects by case (Dolgan, held-out):**
- Accusative objects: 87% found.
- Partitive: 4 of 5.
- **Unmarked objects: 31% found** (dev CV: 36%). The model alone misses most of them, which is why every unmarked nominal with P(O) ≥ 0.05 goes to a human.

**No age bias found.** For speakers never seen in training, recall of unmarked objects is similar across birth groups: 44% (before 1920), 39% (1920–1939), 45% (1940–1959), 48% (1960 and later). O F1 is 76–84% in every group. Small groups, so this rules out large bias only.

**Calibration.** The probabilities mean what they say: in every 0.1-wide bin of P(O), the observed share of objects is within about 0.05 of the predicted one.

**Routing.** With threshold 0.9 and floor 0.05, a human checks:
- 37% of nominals, in about 60% of utterances;
- after correction, S F1 is about 95–96 and O F1 about 96;
- 91% (development) to 100% (held-out) of unmarked objects are found.

Lower thresholds halve the work but leave 10–30% of unmarked objects unfound, which is too risky for B2.

**Transfer with no target data:**
- Evenki → Dolgan: 62.9.
- Dolgan → Evenki: 69.9.
- Both beat the case rule in the target language (57.2 and 64.2): the shared-gloss features carry real information across a Turkic–Tungusic boundary.

**Pooling helps when data is scarce:**
- With 10% of the texts (4 Dolgan texts), adding the other language raises Dolgan from 63.9 to 66.5–66.7 and Evenki from 72.2 to 73.3–74.6.
- With 25% or more, it adds nothing.
- With full data, augmented pooling gives Dolgan 75.5, against 75.3 alone and 74.2 for plain pooling.

These comparisons were all scored on the same held-out texts, so differences under about 1.5 points are noise. The final Dolgan model is Dolgan-only.

**Workload for the 86 untagged Dolgan texts** (67,073 words):
- 11,051 flagged words in 6,085 utterances.
- Batch 1 (narrative and conversation from speakers with a birth year, the texts that matter for comparing generations) is 3,756 utterances with 7,015 flagged words, and comes first in the queue.
- Each coder sees about 3,000 utterances, including the 10% both do.
- The time per item will be known after calibration (the screen stores timestamps).

## How to use it (Jude and Dustan)
1. Open `shared/review_ui/review.html` in a browser (double-click it).
2. Choose your coder letter (A or B).
3. Open `data/derived/dolgan/review/queue.csv`. Do not open the `review_key` folder: it holds the speaker key and the model's full output.
4. For each utterance, decide the orange words with the keys S (subject), O (object), N (neither) or U (unsure), then press Enter.
   - Read the "Coding guide" at the bottom first.
   - Decide by meaning, not by the ending.
   - Words inside subordinate clauses are N.
5. Progress is saved in the browser. Press **Export decisions** at the end of each session and keep the file.
6. When both of you are done, run `python3 shared/igt_tagger/merge_review.py data/derived/dolgan/review review_A.csv review_B.csv` (any Claude session can do this). It writes `final_roles.csv` and `agreement.md`, with kappa between the two of you and each coder's agreement with the model.
7. Discuss the disputed and unsure words. Write the agreed labels into `resolved.csv`, then run the merge again.

About 10% of items go to both of you (marked "both"); that overlap gives the kappa. Before starting, each of you should code 2 or 3 of INEL's already-tagged texts the same way, so we can report your agreement with INEL's annotators. I can build that queue in a minute.

## Glossing new texts
`shared/igt_tagger/glosser.py` is a memory-based glosser trained on INEL's glossed words.
- **Word forms seen in training** get their most frequent analysis, re-weighted by what was seen next to the same neighbours.
- **Unseen forms** get the suffix analysis of the longest matching word ending seen in training.

These texts were also used while tuning the glosser, so treat the figures as slightly optimistic. Results on 20% of texts kept out of training (Dolgan; Evenki in brackets):

| Words | Share of words | Exact gloss | Part of speech | Case |
|---|---|---|---|---|
| All | — | 71.5% (66.0%) | 87.1% (84.5%) | 82.0% (80.0%) |
| Unambiguous forms seen in training | 44% | 93.8% (95.3%) | | 97.3% (98.0%) |
| Ambiguous forms seen in training | 35% | 75.3% (73.8%) | | |
| Unseen forms | 20% (34%) | 16.5% (17.1%) | | 54.8% (47.3%) |

**From raw transcription to tags** (`eval_pipeline.py`, held-out texts, glosses produced automatically):

| | Dolgan, hand glosses | Dolgan, automatic glosses | Evenki, hand glosses | Evenki, automatic glosses |
|---|---|---|---|---|
| Role macro-F1 | 74.9 | 62.7 | 83.1 | 68.1 |
| Unmarked objects found | 10 of 32 | 5 of 32 | | |

- **Retraining doesn't close the gap.** A tagger trained on automatic glosses (each training text glossed by a glosser that never saw it) gets 62.9; a character-based part-of-speech guesser for unseen words gets 63.2.
- **The bottleneck is the glosses.** Automatic part of speech agrees with the hand glosses on 85% of words, case on 91.5%.
- **So, for brand-new texts:** the glosses need human correction (at least every word not marked "known") before tagging, or a better glosser (PolyGloss fine-tuned on INEL) has to close the gap first. `pipeline.py` produces the draft glosses and a review queue, but the role review alone is not enough for new texts.

Most exact-match errors on ambiguous forms are particles (*da*: "and", EMPH or INDEF) and near-synonym lemma glosses (*house* or *tent*), not grammar. **PolyGloss** (Ginn et al. 2026), a pretrained multilingual glossing model with open weights, is the obvious next step for unseen words. It could not be downloaded tonight: neither the cloud workspace nor the shell on Jude's computer can reach HuggingFace. To use it, run it on Colab, fine-tuned (LoRA) on INEL Dolgan, and compare its unseen-word accuracy with the numbers above. INEL's licence terms for model training must be checked first (D-004).

## Scaling this to a general fieldwork parser
What would turn this into a tool for any documented language:
1. **More training languages with the same scheme.**
   - **Multi-CAST** (Haig, Schnell and Schiborr): 11 spoken corpora, about 20,000 clauses, all annotated with GRAID (the scheme INEL's tags follow), with zero arguments, under a Creative Commons licence.
   - **The other INEL corpora** (Selkup, Kamas, Nganasan and others) use the same tiers.
   - Adding these gives the type copies something to learn from: verb-initial and ergative languages, prefixing languages.
   - Then test leave-one-language-out: train on all others, tag a new language with zero tagged text, and compare with the learning curve.
2. **Profiles from typological databases.** Fill profiles from Grambank or WALS automatically (word order, case alignment, pro-drop, DOM) and keep the estimate-from-text check. More profile keys (head marking versus dependent marking, verb agreement type) can be added as type copies without code changes.
3. **A gloss-label normaliser.** Each project glosses a little differently (`INS`/`INSTR`, `COM1`, `ACC.INDF`). `igt.ALIASES` holds the mapping. A shared table built from the Leipzig rules and UniMorph would let any corpus plug in.
4. **Active learning.** The review queue already sends the most uncertain words to humans. Retraining after each batch and re-ranking the rest is the standard loop. Baldridge and Palmer (2009) show it pays off only if it is measured in annotator time, so log time per item (the screen already stores timestamps).
5. **Model choice.** A linear model is the right size for one language with 30,000 words. With 15 or more languages pooled, a small multilingual neural tagger over gloss tokens, or PolyGloss-style byte models with a role head, becomes worth trying. The JSON export and the review loop would stay the same.
6. **The bias check is a feature, not an afterthought.** For any sociolinguistic use, report the tagger's accuracy per speaker group, and route the error-prone class (here unmarked objects) to humans regardless of confidence. This is what makes automatic annotation usable for variation studies, and it is a contribution worth writing up on its own.

## Open questions
- **INEL's own inter-annotator agreement for SyF is unknown.** Our ceiling may be its agreement, not the model. Ask INEL in the email (handoff 004).
- **The held-out set is small:** 10 Dolgan texts and 12 speakers. Treat its scores as accurate to about ±0.03.
- **Unmarked objects are rare in training:** 216 in Dolgan. Their recall is the number to watch.
