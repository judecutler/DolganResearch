"""Study B2: the pre-specified time test of object case marking.

    python3 case_change/b2_test.py data/derived/dolgan/objects.csv reports/b2_results.md

This reads the outcome, so it refuses to run until case_change/ANALYSIS_PLAN.md
has a line starting "Status: **frozen" (Gate 3). Running it earlier would let the result
shape the plan.

Outcome per object: ACC versus not ACC, among NOM, ACC and PART objects (secondary:
PART versus not PART). Model: speaker-clustered linear probability model of the
outcome on birth year, adjusted for genre and source (speaker_test.adjusted_test,
D-034, D-037). Every row of the output is named in ANALYSIS_PLAN.md; nothing else
is computed.
"""
import argparse
import csv
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from speaker_test import adjusted_test  # noqa: E402

PLAN = os.path.join(HERE, "ANALYSIS_PLAN.md")
PRECISE = 10
OUTCOMES = ("NOM", "ACC", "PART")
PRIMARY_CONTROLS = ("genre", "source_collection")
MIN_SPEAKERS = 5


def plan_is_frozen(path=PLAN):
    """True only if a line of the plan starts with "Status: **frozen" (prose mentioning it does not count)."""
    with open(path, encoding="utf-8") as f:
        return any(line.startswith("Status: **frozen") for line in f)


def _mid(lo, hi):
    if not lo or not hi or float(hi) - float(lo) > PRECISE:
        return None
    return (float(lo) + float(hi)) / 2


def cells(rows, time="birth", controls=PRIMARY_CONTROLS, target="ACC"):
    """[(speaker, time_in_years, control_labels, successes, n)] aggregated over objects."""
    d = {}
    for r in rows:
        t = _mid(r["birth_lo"], r["birth_hi"]) if time == "birth" else _mid(r["recording_lo"], r["recording_hi"])
        if t is None:
            continue
        key = (r["speaker_id"], t, tuple(r[c] or "unknown" for c in controls))
        k, n = d.get(key, (0, 0))
        d[key] = (k + (r["case"] == target), n + 1)
    return [(g, t, lab, k, n) for (g, t, lab), (k, n) in sorted(d.items())]


def run(rows, label, n_boot, rng, time="birth", controls=PRIMARY_CONTROLS, target="ACC"):
    cs = cells(rows, time, controls, target)
    n_spk, n_obj = len({c[0] for c in cs}), sum(c[4] for c in cs)
    if n_spk < MIN_SPEAKERS:
        return f"| {label} | {n_spk} | {n_obj} | too few speakers | |"
    slope, p = adjusted_test(cs, n_boot, rng, controls=bool(controls))
    if slope is None:
        return f"| {label} | {n_spk} | {n_obj} | time not separable from controls | |"
    return f"| {label} | {n_spk} | {n_obj} | {100 * slope:+.1f} | {p:.3f} |"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("objects")
    ap.add_argument("out")
    ap.add_argument("--boot", type=int, default=9999)
    ap.add_argument("--plan", default=PLAN)
    a = ap.parse_args(argv)
    if not plan_is_frozen(a.plan):
        sys.exit("ANALYSIS_PLAN.md is not frozen (Gate 3). Freeze the plan before looking at outcomes.")
    with open(a.objects, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f)
                if r["case"] in OUTCOMES and _mid(r["birth_lo"], r["birth_hi"]) is not None]
    rng = random.Random(20261105)
    b = a.boot
    lines = ["# Study B2 results: object case by time", "",
             "Built by `case_change/b2_test.py` after the analysis plan was frozen. Each row is a "
             "speaker-clustered regression of the outcome on time; the estimate is the change in the outcome "
             "share in percentage points per decade; p is from "
             f"{b} wild-cluster-bootstrap draws by speaker (D-034, D-037).", "",
             "## Primary and secondary tests", "",
             "| Analysis | Speakers | Objects | Change per decade (points) | p |", "|---|---|---|---|---|",
             run(rows, "PRIMARY: ACC, birth year, adjusted for genre and source", b, rng),
             run(rows, "ACC, birth year, unadjusted", b, rng, controls=()),
             run(rows, "ACC, birth year, adjusted for genre only", b, rng, controls=("genre",)),
             run(rows, "ACC, recording year (real time), adjusted for genre and source", b, rng, time="recording"),
             run(rows, "PART, birth year, adjusted for genre and source", b, rng, target="PART"),
             run(rows, "ACC, birth year, adjusted for genre, source and clause TAM group", b, rng,
                 controls=PRIMARY_CONTROLS + ("tam_group",)),
             "", "## Robustness checks (primary model)", "",
             "| Analysis | Speakers | Objects | Change per decade (points) | p |", "|---|---|---|---|---|",
             run([r for r in rows if r["loan"] == "0"], "Native nouns only (no BOR tag)", b, rng),
             run([r for r in rows if r["pronoun"] == "0"], "No pronoun objects", b, rng),
             run([r for r in rows if r["align_ok"] == "true" and r["unsure_gloss"] == "0"],
                 "Aligned, no % glosses", b, rng),
             run([r for r in rows if r["birth_precision"] in ("year", "date")], "Exact birth years only", b, rng),
             run([r for r in rows if r["dialect"] != "Anabar"], "Without Anabar", b, rng)]
    for src in sorted({r["source_collection"] for r in rows}):
        lines.append(run([r for r in rows if r["source_collection"] == src], f"Source {src} only",
                         b, rng, controls=("genre",)))
    lines += ["", "## Leave one speaker out (primary model)", "",
              "| Speaker left out | Speakers | Objects | Change per decade (points) | p |", "|---|---|---|---|---|"]
    for s in sorted({r["speaker_id"] for r in rows}):
        lines.append(run([r for r in rows if r["speaker_id"] != s], s, min(b, 999), rng))
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[:16]))


if __name__ == "__main__":
    main()
