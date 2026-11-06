"""Study B1: instrumental versus dative secondary predicates by time, after human vetting.

    python3 case_change/b1_test.py b1_merged.csv data/derived/dolgan/b1_candidates.csv \\
        data/derived/dolgan/speakers.csv reports/b1_results.md

b1_merged.csv is the output of `shared/workbook.py merge` for the B1 sheets. An item
enters the analysis if both coders said `is_secondary_predicate` = yes, or, when Jude
and Dustan have added a `resolved` column after discussing disagreements, if
`resolved` = yes. Reads the outcome, so it refuses to run until the analysis plan is
frozen (Gate 3). Follows the B1 section of case_change/ANALYSIS_PLAN.md.
"""
import argparse
import csv
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from b2_test import BIRTH_BINS, PLAN, RECORDING_BINS, _bin, _mid, plan_is_frozen  # noqa: E402
from speaker_test import adjusted_test  # noqa: E402

MIN_ITEMS, MIN_SPEAKERS = 30, 10
CASES = ("INS", "DAT/LOC")


def accepted(m):
    if (m.get("resolved") or "").strip():
        return m["resolved"].strip() == "yes"
    return m.get("is_secondary_predicate_A") == "yes" and m.get("is_secondary_predicate_B") == "yes"


def _binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def exact_interval(k, n, alpha=0.05):
    """Clopper-Pearson interval for k successes in n, by bisection."""
    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    low = 0.0 if k == 0 else solve(lambda p: 1 - _binom_cdf(k - 1, n, p) < alpha / 2)
    high = 1.0 if k == n else solve(lambda p: _binom_cdf(k, n, p) > alpha / 2)
    return low, high


def load(merged_path, cands_path, speakers_path):
    with open(merged_path, encoding="utf-8") as f:
        ok = {m["token_id"] for m in csv.DictReader(f) if accepted(m)}
    with open(speakers_path, encoding="utf-8") as f:
        usable = {s["speaker_id"] for s in csv.DictReader(f) if _mid(s["birth_lo"], s["birth_hi"]) is not None}
        f.seek(0)
        births = {s["speaker_id"]: (s["birth_lo"], s["birth_hi"]) for s in csv.DictReader(f)}
    with open(cands_path, encoding="utf-8") as f:
        rows = [c for c in csv.DictReader(f) if c["token_id"] in ok and c["case"] in CASES]
    for c in rows:
        c["birth_lo"], c["birth_hi"] = births.get(c["speaker_id"], ("", ""))
        c["_usable"] = c["speaker_id"] in usable
    return rows


def cells(rows, time, controls):
    d = {}
    for r in rows:
        t = _mid(r["birth_lo"], r["birth_hi"]) if time == "birth" else _mid(r["recording_lo"], r["recording_hi"])
        if t is None:
            continue
        key = (r["speaker_id"], t, tuple(r[c] or "unknown" for c in controls))
        k, n = d.get(key, (0, 0))
        d[key] = (k + (r["case"] == "INS"), n + 1)
    return [(g, t, lab, k, n) for (g, t, lab), (k, n) in sorted(d.items())]


def count_table(rows, title, key):
    c = {}
    for r in rows:
        k = key(r)
        if k:
            a = c.setdefault(k, [0, 0])
            a[0] += r["case"] == "INS"
            a[1] += 1
    out = [f"| {title} | Items | INS | INS share | 95% exact interval |", "|---|---|---|---|---|"]
    for k in sorted(c):
        ins, n = c[k]
        lo, hi = exact_interval(ins, n)
        out.append(f"| {k} | {n} | {ins} | {ins / n:.1%} | {lo:.1%} to {hi:.1%} |")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("merged")
    ap.add_argument("candidates")
    ap.add_argument("speakers")
    ap.add_argument("out")
    ap.add_argument("--boot", type=int, default=9999)
    ap.add_argument("--plan", default=PLAN)
    a = ap.parse_args(argv)
    if not plan_is_frozen(a.plan):
        sys.exit("ANALYSIS_PLAN.md is not frozen (Gate 3). Freeze the plan before looking at outcomes.")
    rows = load(a.merged, a.candidates, a.speakers)
    dated = [r for r in rows if r["_usable"]]
    n_spk = len({r["speaker_id"] for r in dated})
    lines = ["# Study B1 results: instrumental versus dative secondary predicates", "",
             f"Built by `case_change/b1_test.py`. Accepted items: {len(rows)}; from speakers with a usable birth "
             f"year: {len(dated)} from {n_spk} speakers. Minimum for tests (plan): {MIN_ITEMS} items from "
             f"{MIN_SPEAKERS} speakers.", "", "## Counts", ""]
    lines += count_table(dated, "Birth bin", lambda r: _bin(_mid(r["birth_lo"], r["birth_hi"]), BIRTH_BINS))
    rec = lambda r: _bin(_mid(r["recording_lo"], r["recording_hi"]), RECORDING_BINS) if _mid(  # noqa: E731
        r["recording_lo"], r["recording_hi"]) else ""
    lines += [""] + count_table(rows, "Recording bin (all accepted items)", rec)
    lines += [""] + count_table(rows, "Genre (all accepted items)", lambda r: r["genre"])
    if len(dated) < MIN_ITEMS or n_spk < MIN_SPEAKERS:
        lines += ["", "**Too few items for a test (plan, B1 minimum). The corpus cannot test Siegl's (2015) claim; "
                  "the counts above are descriptive only.**"]
    else:
        rng = random.Random(20261105)
        lines += ["", "## Tests", "", "| Analysis | Speakers | Items | Change in INS share per decade (points) | p |",
                  "|---|---|---|---|---|"]
        for label, sub, time, ctl in (("Birth year, adjusted for genre and source", dated, "birth",
                                       ("genre", "source_collection")),
                                      ("Recording year, adjusted for genre", rows, "recording", ("genre",))):
            cs = cells(sub, time, ctl)
            est, p = adjusted_test(cs, a.boot, rng)
            n = sum(c[4] for c in cs)
            spk = len({c[0] for c in cs})
            lines.append(f"| {label} | {spk} | {n} | "
                         + ("not separable from controls | |" if est is None else f"{100 * est:+.1f} | {p:.3f} |"))
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
