# Scripts for handoff 002

Throwaway inspection scripts, kept so the numbers in `structure_report.md` can be re-checked. They are not a parser and not part of the pipeline. Standard library only; run with `python3 -I`.

Order: `parse_all.py CORPUS_DIR OUT.pkl` (one pickle per corpus), then the `q_*.py` scripts, which read the pickles and the `.coma` files. They expect the unzipped corpora at `~/scratch/x/d` (Dolgan) and `~/scratch/x/e` (Evenki) and the pickles in `~/scratch/002/`. Change the paths at the top if you run them elsewhere. `wordlib.py` aligns tiers by (start, end) timeline position within a speaker. `coma_lib.py` reads the `.coma` metadata.

Some scripts print speaker or text details to the screen. Their output was filtered by hand before anything went into the report. Do not paste their raw output into committed files.
