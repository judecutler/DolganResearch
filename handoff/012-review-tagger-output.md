# 012: Calibrate, then review the tagger's uncertain words

- **From:** Claude
- **To:** Jude, Dustan
- **Status:** todo
- **Created:** 2026-11-07
- **Depends on:** D-042; `docs/TAGGER_NOTES.md`; `reports/tagger_eval.md`

## Why
The tagger (`shared/igt_tagger/`) adds subject, object and predicate tags to the 86 Dolgan texts INEL did not tag. That gives B2, B3, C and D1 more speakers within each genre: the B2 and Study D nulls showed this is what the corpus lacks. The model cannot be trusted alone on the hard cases (unmarked objects, subordinate clauses), so you decide those.

## Steps
1. **Calibration (about 1 hour each).**
   - Open `shared/review_ui/review.html` in a browser and choose your coder letter.
   - Open `data/derived/dolgan/review_calibration/queue.csv`. These are texts INEL already tagged; the model's guesses are hidden.
   - Decide every orange word, then press **Export decisions**.
   - Put both export files in that folder and ask Claude to run `merge_review.py` on it. `calibration.md` then shows your agreement with INEL's annotators and with each other.
   - If agreement with INEL is low (kappa below about 0.7), we read the disagreements together and adjust the coding guide before step 2.
2. **Main review.**
   - Open `data/derived/dolgan/review/queue.csv`.
   - Items marked for both of you give the kappa; the rest are split between you.
   - Export at the end of every session (the browser keeps your progress, but the export file is the record).
3. **Merge.**
   - Claude runs `merge_review.py`, which writes `final_roles.csv` and `agreement.md`.
   - You discuss the disputed and unsure words, and write the agreed labels into `resolved.csv`.
   - Claude runs the merge again.
4. **Before any analysis of the expanded corpus,** Claude writes a pre-specified plan (as for Study D), and you confirm it.

Speaker, date and text are hidden in both queues on purpose. Do not look them up while coding, and do not open the `review_key` and `review_calibration_key` folders: they hold the key and, for calibration, INEL's answers.

**Files on Jude's computer, under `data/derived/dolgan/`:**
- `review_calibration/` holds the calibration queue (112 utterances, 298 words) and a copy of `review.html`.
- `review/` holds the main queue (6,085 utterances, 11,051 flagged words; batch 1 of 3,756 utterances comes first). Each of you sees about 3,000 utterances.

## Results
*(fill in: date, items done by each coder, kappa, notes)*
