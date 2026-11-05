"""Study B2 power analysis from the real design, without looking at the outcome.

    python3 case_change/power.py data/derived/dolgan/objects.csv reports/power_b2.md

Reads only speaker_id and birth_mid from the object table (how many objects each
speaker with a usable birth year contributes, and when they were born). The case
column is never read, so this can run before Gate 3. Simulates the speaker-level
permutation test in speaker_test.py over a grid of effect sizes and between-speaker
spreads, and reports the power of each.

The baseline accusative share is an input, not a measurement. The default 0.8 is
close to the pooled share in handoff 002 (1,056 of 1,307 objects). That figure is
pooled over all speakers, so it says nothing about cohorts.
"""
import argparse
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from speaker_test import power  # noqa: E402

PRECISE = 10


def design_from(objects_csv, min_tokens=1):
    """[(birth_mid, n_objects)] for speakers with a usable birth year. Reads no outcome column."""
    counts, birth = {}, {}
    with open(objects_csv, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            lo, hi = r["birth_lo"], r["birth_hi"]
            if not lo or float(hi) - float(lo) > PRECISE:
                continue
            counts[r["speaker_id"]] = counts.get(r["speaker_id"], 0) + 1
            birth[r["speaker_id"]] = float(r["birth_mid"])
    return [(birth[s], n) for s, n in sorted(counts.items()) if n >= min_tokens]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("objects")
    p.add_argument("out")
    p.add_argument("--base", type=float, default=0.8)
    p.add_argument("--sims", type=int, default=200)
    p.add_argument("--min-tokens", type=int, default=3)
    a = p.parse_args(argv)
    design = design_from(a.objects, a.min_tokens)
    if len(design) < 4:
        sys.exit(f"only {len(design)} speakers with a usable birth year and {a.min_tokens}+ objects: no power analysis possible")
    births = [b for b, _ in design]
    lines = ["# Study B2: power of the speaker-level trend test", "",
             "Built by `case_change/power.py` from the design alone: speakers with a usable birth year "
             f"and at least {a.min_tokens} objects, and their object counts. The outcome was not read.", "",
             f"Speakers: {len(design)}. Objects: {sum(n for _, n in design)}. Birth years "
             f"{min(births):.0f} to {max(births):.0f}. Baseline accusative share (input): {a.base}. "
             f"Simulations per cell: {a.sims}, alpha 0.05, two-sided permutation test.", "",
             "Effect sizes are odds ratios per decade of birth year. For orientation, an odds ratio of "
             "1.5 per decade over 50 years moves a share of 0.80 to about 0.97 or 0.35, depending on direction.", "",
             "| Odds ratio per decade | Power, speaker SD 0.5 | Power, speaker SD 1.0 |", "|---|---|---|"]
    for orat in (1.0, 1.2, 1.35, 1.5, 1.75, 2.0):
        b = math.log(orat)
        cells = [power(design, a.base, b, sd, n_sim=a.sims, seed=7) for sd in (0.5, 1.0)]
        lines.append(f"| {orat} | {cells[0]:.2f} | {cells[1]:.2f} |")
    lines += ["", "Row 1.0 is the false-positive rate and should be near 0.05. Speaker SD is the "
              "between-speaker spread on the log-odds scale. It is unknown until the outcome is seen, so "
              "both values are shown. Report the smallest odds ratio with power of 0.8 or more in the paper."]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[-12:]))


if __name__ == "__main__":
    main()
