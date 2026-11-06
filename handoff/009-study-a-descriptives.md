# 009: Run the Study A gloss descriptives

- **From:** web Claude
- **To:** desktop Claude
- **Status:** done
- **Created:** 2026-11-06
- **Depends on:** 007

## Goal
Before Jude and Dustan code anything, the corpus glosses can already show two things: how often each evidential and past form occurs per genre in Dolgan and Evenki, and whether the indirect past `PST2` is the usual past of folklore and rarer with first-person subjects. The script labels all of it exploratory. You only run it and report.

## Steps
1. `git pull`. Run the tests: `python3 -m unittest discover -s shared/tests -t shared/tests`. Expect `OK`.
2. Run in the background (a few minutes):
   `python3 shared/evid_descriptives.py data/derived/dolgan data/derived/evenki reports/study_a_descriptives.md > scratch/009.log 2>&1 &`
   Record the run time and exit code.
2b. Regenerate the Gate 0 report, which has a new section on speakers recorded at times 10 or more years apart (design counts only):
   `python3 shared/gate0.py reports/gate0_feasibility.md data/derived/dolgan data/derived/evenki`
3. Privacy check `reports/study_a_descriptives.md` and `reports/gate0_feasibility.md` as in 003, step 5. Speaker IDs and birth decades are allowed; names and full dates are not.
4. Commit both reports, this file and `PLAN.md` (one log line). Nothing under `data/`.

## Results

- **Date finished:** 2026-11-06 (overnight)
- **Tests:** `Ran 59 tests ... OK`.
- **Run (step 2):** `evid_descriptives.py` took 16 s, exit 0, in the foreground (background jobs are killed on Jude's computer). Output is identical under `PYTHONHASHSEED` 1 and 2.
- **Highlights (exploratory):** Dolgan PST2 share of finite past verbs is 77.9% in folklore, 58.4% in personal narrative and 43.1% in conversation. By subject person it is 1st 47.0%, 2nd 38.4%, 3rd 68.3%. In folklore the 1st person drops to 23.3% (3rd person 83.4%). Speaker-clustered test, folklore minus narrative: +19.5 points, p = 0.002; adjusted for source +10.2, p = 0.18. Predicative-agreement share of PST2 (2b) is 82.5% in folklore, 58.6% in narrative and 46.5% in conversation. Evenki EVID is rare: 0.09 per 1,000 words in folklore, 0.52 in narrative.
- **Gate 0 (step 2b):** regenerated in under 1 s, exit 0. New real-time panel: 4 speakers recorded 10 or more years apart (AkEE 1982–1994, BeES 1997–2010, KiMN 1975–1990, PoNA 1970–2004). Only PoNA has objects in more than one recording year (62, 35, 17).
- **Privacy check (step 3):** `study_a_descriptives.md` and `gate0_feasibility.md` pass (speaker IDs and birth decades only).
- **Questions for web Claude:** the source-adjusted folklore effect is not significant (p = 0.18). Is that expected, given how genre and source overlap?
