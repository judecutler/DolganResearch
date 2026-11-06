# 009: Run the Study A gloss descriptives

- **From:** web Claude
- **To:** desktop Claude
- **Status:** todo
- **Created:** 2026-11-06
- **Depends on:** 007

## Goal
Before Jude and Dustan code anything, the corpus glosses can already show two things: how often each evidential and past form occurs per genre in Dolgan and Evenki, and whether the indirect past `PST2` is the usual past of folklore and rarer with first-person subjects. The script labels all of it exploratory. You only run it and report.

## Steps
1. `git pull`. Run the tests: `python3 -m unittest discover -s shared/tests -t shared/tests`. Expect `OK`.
2. Run in the background (a few minutes):
   `python3 shared/evid_descriptives.py data/derived/dolgan data/derived/evenki reports/study_a_descriptives.md > scratch/009.log 2>&1 &`
   Record the run time and exit code.
3. Privacy check `reports/study_a_descriptives.md` as in 003, step 5 (counts only).
4. Commit the report, this file and `PLAN.md` (one log line). Nothing under `data/`.

## Results
*(desktop Claude fills in)*

- **Date finished:**
- **Run time and exit code:**
- **Section 3 table (copy from the report):**
- **Privacy check:**
- **Questions for web Claude:**
