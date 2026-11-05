"""Study B2: the pre-specified birth-year test of accusative object marking.

    python3 case_change/b2_test.py data/derived/dolgan/objects.csv reports/b2_results.md

This reads the outcome, so it refuses to run until case_change/ANALYSIS_PLAN.md
has a line starting "Status: **frozen" (Gate 3). Running it earlier would let the result
shape the plan.

Outcome per object: ACC versus not ACC, among NOM, ACC and PART objects.
Unit: the speaker (empirical logit of their ACC share, weighted by their object
count), regressed on birth year, with a permutation p-value (speaker_test.py).
Pre-specified robustness checks from ANALYSIS_PLAN.md that this script can run:
native nouns only (no BOR tag), leave one speaker out, each source on its own,
precise birth years only, and well-aligned glosses only.
"""
import argparse
import csv
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from speaker_test import trend_test  # noqa: E402

PLAN = os.path.join(HERE, "ANALYSIS_PLAN.md")
PRECISE = 10
OUTCOMES = ("NOM", "ACC", "PART")


def plan_is_frozen(path=PLAN):
    """True only if a line of the plan starts with "Status: **frozen" (prose mentioning it does not count)."""
    with open(path, encoding="utf-8") as f:
        return any(line.startswith("Status: **frozen") for line in f)


def by_speaker(rows):
    d = {}
    for r in rows:
        k, n = d.get(r["speaker_id"], (0, 0))
        d[r["speaker_id"]] = (k + (r["case"] == "ACC"), n + 1)
    birth = {r["speaker_id"]: float(r["birth_mid"]) for r in rows}
    return [(birth[s], k, n) for s, (k, n) in sorted(d.items())]


def run(rows, label, n_perm, rng, min_speakers=5):
    data = by_speaker(rows)
    if len(data) < min_speakers:
        return f"| {label} | {len(data)} | {sum(n for *_, n in data)} | too few speakers | |"
    slope, p = trend_test(data, n_perm, rng)
    return (f"| {label} | {len(data)} | {sum(n for *_, n in data)} | {math.exp(slope):.2f} | {p:.3f} |")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("objects")
    ap.add_argument("out")
    ap.add_argument("--perm", type=int, default=9999)
    ap.add_argument("--plan", default=PLAN)
    a = ap.parse_args(argv)
    if not plan_is_frozen(a.plan):
        sys.exit("ANALYSIS_PLAN.md is not frozen (Gate 3). Freeze the plan before looking at outcomes.")
    with open(a.objects, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["case"] in OUTCOMES and r["birth_lo"]
                and float(r["birth_hi"]) - float(r["birth_lo"]) <= PRECISE]
    rng = random.Random(20261105)
    lines = ["# Study B2 results: accusative share by speaker birth year", "",
             "Built by `case_change/b2_test.py` after the analysis plan was frozen. The odds ratio is per "
             "decade of birth year, from a speaker-level weighted regression of the empirical logit; the "
             f"p-value is from {a.perm} permutations of birth year across speakers.", "",
             "| Analysis | Speakers | Objects | Odds ratio per decade | p |", "|---|---|---|---|---|"]
    lines.append(run(rows, "Main: all objects", a.perm, rng))
    lines.append(run([r for r in rows if r["loan"] == "0"], "Native nouns only", a.perm, rng))
    lines.append(run([r for r in rows if r["align_ok"] == "true" and r["unsure_gloss"] == "0"],
                     "Aligned, no % glosses", a.perm, rng))
    lines.append(run([r for r in rows if r["birth_precision"] in ("year", "date")],
                     "Exact birth years only", a.perm, rng))
    for src in sorted({r["source_collection"] for r in rows}):
        lines.append(run([r for r in rows if r["source_collection"] == src], f"Source: {src}", a.perm, rng))
    lines += ["", "## Leave one speaker out", "", "| Speaker left out | Odds ratio per decade | p |", "|---|---|---|"]
    for s in sorted({r["speaker_id"] for r in rows}):
        data = by_speaker([r for r in rows if r["speaker_id"] != s])
        slope, p = trend_test(data, min(a.perm, 999), rng)
        lines.append(f"| {s} | {math.exp(slope):.2f} | {p:.3f} |")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[:12]))


if __name__ == "__main__":
    main()
