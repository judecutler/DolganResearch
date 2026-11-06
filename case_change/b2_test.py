"""Study B2: the pre-specified time test of object case marking.

    python3 case_change/b2_test.py data/derived/dolgan/objects.csv reports/b2_results.md

This reads the outcome, so it refuses to run until case_change/ANALYSIS_PLAN.md
has a line starting "Status: **frozen" (Gate 3). Running it earlier would let the result
shape the plan.

Outcome per object: ACC versus not ACC, among NOM, ACC and PART objects (secondary:
PART versus not PART). B3: verb before object (VO), among objects in utterances with
exactly one predicate. Model: speaker-clustered linear probability model of the
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

from speaker_test import adjusted_test, collinearity  # noqa: E402

PLAN = os.path.join(HERE, "ANALYSIS_PLAN.md")
PRECISE = 10
OUTCOMES = ("NOM", "ACC", "PART")
PRIMARY_CONTROLS = ("genre", "source_collection")
FALLBACK_CONTROLS = ("genre",)
MAX_COLLINEARITY = 0.90  # the plan's decision rule
MIN_SPEAKERS = 5
LOO_BOOT = 999


def plan_is_frozen(path=PLAN):
    """True only if a line of the plan starts with "Status: **frozen" (prose mentioning it does not count)."""
    with open(path, encoding="utf-8") as f:
        return any(line.startswith("Status: **frozen") for line in f)


def _mid(lo, hi):
    if not lo or not hi or float(hi) - float(lo) > PRECISE:
        return None
    return (float(lo) + float(hi)) / 2


def is_vo(r):
    """B3: the verb comes before the object, in an utterance with exactly one predicate."""
    return r["pred_position"] == "before"


def cells(rows, time="birth", controls=PRIMARY_CONTROLS, target="ACC"):
    """[(speaker, time_in_years, control_labels, successes, n)] aggregated over objects.

    target is a case label (success = the object has that case) or a function of the row.
    """
    hit = target if callable(target) else (lambda r: r["case"] == target)
    d = {}
    for r in rows:
        t = _mid(r["birth_lo"], r["birth_hi"]) if time == "birth" else _mid(r["recording_lo"], r["recording_hi"])
        if t is None:
            continue
        key = (r["speaker_id"], t, tuple(r[c] or "unknown" for c in controls))
        k, n = d.get(key, (0, 0))
        d[key] = (k + bool(hit(r)), n + 1)
    return [(g, t, lab, k, n) for (g, t, lab), (k, n) in sorted(d.items())]


def choose_controls(rows, target="ACC"):
    """The plan's decision rule, from the design only: (controls, explained shares) or (None, ...)."""
    shares = {}
    for ctl in (PRIMARY_CONTROLS, FALLBACK_CONTROLS):
        r2 = collinearity(cells(rows, "birth", ctl, target))
        shares[ctl] = r2
        if r2 is not None and r2 < MAX_COLLINEARITY:
            return ctl, shares
    return None, shares


def rule_lines(name, ctl, shares):
    out = [f"Decision rule ({name}): birth-year variance explained by genre + source "
           f"{shares.get(PRIMARY_CONTROLS, 0):.2f}"]
    if FALLBACK_CONTROLS in shares:
        out[0] += f", by genre alone {shares[FALLBACK_CONTROLS]:.2f}"
    names = " and ".join("source" if c == "source_collection" else c for c in ctl or ())
    out[0] += (f". Primary test adjusts for {names}." if ctl else
               ". **Both are 0.90 or more: no confirmatory test; report the descriptive tables only.**")
    return out


def run(rows, label, n_boot, rng, time="birth", controls=PRIMARY_CONTROLS, target="ACC"):
    cs = cells(rows, time, controls, target)
    n_spk, n_obj = len({c[0] for c in cs}), sum(c[4] for c in cs)
    if n_spk < MIN_SPEAKERS:
        return f"| {label} | {n_spk} | {n_obj} | too few speakers | |"
    slope, p = adjusted_test(cs, n_boot, rng, controls=bool(controls))
    if slope is None:
        return f"| {label} | {n_spk} | {n_obj} | time not separable from controls | |"
    return f"| {label} | {n_spk} | {n_obj} | {100 * slope:+.1f} | {p:.3f} |"


# Names sort in time order. D-013 proposal in ANALYSIS_PLAN.md.
BIRTH_BINS = ((None, 1920, "-1919"), (1920, 1940, "1920-1939"), (1940, 1960, "1940-1959"), (1960, None, "1960-"))
RECORDING_BINS = ((None, 1980, "-1979"), (1980, 2000, "1980-1999"), (2000, None, "2000-"))


def _bin(year, bins):
    for lo, hi, name in bins:
        if (lo is None or year >= lo) and (hi is None or year < hi):
            return name
    return ""


def descriptive(rows):
    """Case counts by birth bin, recording bin, and birth bin x genre; per-speaker shares."""
    out = []
    for title, key in (
            ("Birth bin", lambda r: _bin(_mid(r["birth_lo"], r["birth_hi"]), BIRTH_BINS)),
            ("Recording bin", lambda r: _bin(_mid(r["recording_lo"], r["recording_hi"]) or 0, RECORDING_BINS)
             if _mid(r["recording_lo"], r["recording_hi"]) else "imprecise"),
            ("Birth bin, genre", lambda r: _bin(_mid(r["birth_lo"], r["birth_hi"]), BIRTH_BINS) + ", " + r["genre"])):
        c = {}
        for r in rows:
            c.setdefault(key(r), dict.fromkeys(OUTCOMES, 0))[r["case"]] += 1
        out += ["", f"| {title} | " + " | ".join(OUTCOMES) + " | ACC share |", "|---|" + "---|" * (len(OUTCOMES) + 1)]
        for k in sorted(c):
            n = sum(c[k].values())
            out.append(f"| {k} | " + " | ".join(str(c[k][x]) for x in OUTCOMES) + f" | {c[k]['ACC'] / n:.1%} |")
    return out


def speaker_points(rows):
    """[(speaker, birth year, objects, ACC share)]."""
    d = {}
    for r in rows:
        k, n = d.get(r["speaker_id"], (0, 0))
        d[r["speaker_id"]] = (k + (r["case"] == "ACC"), n + 1)
    birth = {r["speaker_id"]: _mid(r["birth_lo"], r["birth_hi"]) for r in rows}
    return [(s, birth[s], n, k / n) for s, (k, n) in sorted(d.items(), key=lambda x: birth[x[0]])]


def svg_plot(points, path):
    """Each speaker's ACC share against birth year; circle area proportional to object count."""
    w, h, m = 640, 360, 50
    xs = [b for _, b, _, _ in points]
    x0, x1 = min(xs) - 5, max(xs) + 5
    nmax = max(n for _, _, n, _ in points)
    sx = lambda b: m + (b - x0) / (x1 - x0) * (w - 2 * m)  # noqa: E731
    sy = lambda v: h - m - v * (h - 2 * m)  # noqa: E731
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" font-family="sans-serif" '
             'font-size="12"><rect width="100%" height="100%" fill="white"/>',
             f'<line x1="{m}" y1="{h - m}" x2="{w - m}" y2="{h - m}" stroke="#444"/>',
             f'<line x1="{m}" y1="{m}" x2="{m}" y2="{h - m}" stroke="#444"/>']
    for v in (0, 0.25, 0.5, 0.75, 1):
        parts.append(f'<text x="{m - 8}" y="{sy(v) + 4:.1f}" text-anchor="end">{v:.0%}</text>')
    for yr in range(int(x0 // 10 * 10 + 10), int(x1) + 1, 20):
        parts.append(f'<text x="{sx(yr):.1f}" y="{h - m + 18}" text-anchor="middle">{yr}</text>')
    for _, b, n, v in points:
        r = 3 + 12 * (n / nmax) ** 0.5
        parts.append(f'<circle cx="{sx(b):.1f}" cy="{sy(v):.1f}" r="{r:.1f}" fill="#3a6ea5" fill-opacity="0.55" '
                     'stroke="#1d3d63"/>')
    parts += [f'<text x="{w / 2}" y="{h - 12}" text-anchor="middle">Speaker birth year</text>',
              f'<text x="14" y="{h / 2}" text-anchor="middle" transform="rotate(-90 14 {h / 2})">'
              'Accusative share of objects</text></svg>']
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts) + "\n")


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
        dated = [r for r in csv.DictReader(f) if _mid(r["birth_lo"], r["birth_hi"]) is not None]
    rows = [r for r in dated if r["case"] in OUTCOMES]
    one_pred = [r for r in dated if r["n_preds_in_utt"] == "1" and r["pred_position"]]
    rng = random.Random(20261105)
    b = a.boot
    ctl, shares = choose_controls(rows)
    ctl3, shares3 = choose_controls(one_pred, is_vo)
    P = ctl or PRIMARY_CONTROLS
    P3 = ctl3 or PRIMARY_CONTROLS
    adj = lambda c: " and ".join("source" if x == "source_collection" else x for x in c)  # noqa: E731
    head = "PRIMARY" if ctl else "NOT CONFIRMATORY (decision rule)"
    head3 = "B3 PRIMARY" if ctl3 else "B3 NOT CONFIRMATORY (decision rule)"
    lines = ["# Study B2 results: object case by time", "",
             "Built by `case_change/b2_test.py` after the analysis plan was frozen. Each row is a "
             "speaker-clustered regression of the outcome on time; the estimate is the change in the outcome "
             "share in percentage points per decade; p is from "
             f"{b} wild-cluster-bootstrap draws by speaker ({LOO_BOOT} for leave-one-out rows) (D-034, D-037).", ""]
    lines += rule_lines("B2", ctl, shares) + [""] + rule_lines("B3", ctl3, shares3) + [
             "", "## Primary and secondary tests", "",
             "| Analysis | Speakers | Objects | Change per decade (points) | p |", "|---|---|---|---|---|",
             run(rows, f"{head}: ACC, birth year, adjusted for {adj(P)}", b, rng, controls=P),
             run(rows, "ACC, birth year, unadjusted", b, rng, controls=()),
             run(rows, "ACC, birth year, adjusted for genre only", b, rng, controls=("genre",)),
             run(rows, "ACC, recording year (real time), adjusted for genre and source", b, rng, time="recording"),
             run(rows, "PART, birth year, adjusted for genre and source", b, rng, target="PART"),
             run(rows, "ACC, birth year, adjusted for genre, source and clause TAM group", b, rng,
                 controls=PRIMARY_CONTROLS + ("tam_group",)),
             "", f"## Robustness checks (primary model, adjusted for {adj(P)})", "",
             "| Analysis | Speakers | Objects | Change per decade (points) | p |", "|---|---|---|---|---|",
             run([r for r in rows if r["loan"] == "0"], "Native nouns only (no BOR tag)", b, rng, controls=P),
             run([r for r in rows if r["pronoun"] == "0"], "No pronoun objects", b, rng, controls=P),
             run([r for r in rows if r["align_ok"] == "true" and r["unsure_gloss"] == "0"],
                 "Aligned, no % glosses", b, rng, controls=P),
             run([r for r in rows if r["birth_precision"] in ("year", "date")], "Exact birth years only", b, rng,
                 controls=P),
             run([r for r in rows if r["dialect"] != "Anabar"], "Without Anabar", b, rng, controls=P)]
    for src in sorted({r["source_collection"] for r in rows}):
        lines.append(run([r for r in rows if r["source_collection"] == src], f"Source {src} only",
                         b, rng, controls=("genre",)))
    lines += ["", "## B3: word order (verb before object), utterances with one predicate", "",
              "| Analysis | Speakers | Objects | Change per decade (points) | p |", "|---|---|---|---|---|",
              run(one_pred, f"{head3}: VO, birth year, adjusted for {adj(P3)}", b, rng, controls=P3, target=is_vo),
              run(one_pred, "B3: VO, birth year, unadjusted", b, rng, controls=(), target=is_vo),
              run(one_pred, "B3: VO, recording year, adjusted for genre and source", b, rng, time="recording",
                  target=is_vo),
              run([r for r in one_pred if r["pronoun"] == "0"], "B3: VO, no pronoun objects", b, rng,
                  controls=P3, target=is_vo)]
    lines += ["", f"## Leave one speaker out (primary model, adjusted for {adj(P)})", "",
              "| Speaker left out | Speakers | Objects | Change per decade (points) | p |", "|---|---|---|---|---|"]
    for s in sorted({r["speaker_id"] for r in rows}):
        lines.append(run([r for r in rows if r["speaker_id"] != s], s, LOO_BOOT, rng, controls=P))
    lines += ["", "## Real-time panel: speakers with objects in two or more recording years (descriptive)", "",
              "| Speaker | Recording year | NOM | ACC | PART |", "|---|---|---|---|---|"]
    years = {}
    for r in rows:
        y = _mid(r["recording_lo"], r["recording_hi"])
        if y is not None:
            years.setdefault(r["speaker_id"], {}).setdefault(y, dict.fromkeys(OUTCOMES, 0))[r["case"]] += 1
    for sp in sorted(years):
        if len(years[sp]) > 1 and max(years[sp]) - min(years[sp]) >= 10:
            lines += [f"| {sp} | {y:.0f} | " + " | ".join(str(c[x]) for x in OUTCOMES) + " |"
                      for y, c in sorted(years[sp].items())]
    points = speaker_points(rows)
    svg = os.path.splitext(a.out)[0] + "_speakers.svg"
    svg_plot(points, svg)
    lines += ["", "## Descriptive tables (not tests)", ""] + descriptive(rows) + [
        "", f"Per-speaker accusative shares are plotted in `{os.path.basename(svg)}` (circle area = objects).", "",
        "| Speaker | Birth year | Objects | ACC share |", "|---|---|---|---|"]
    lines += [f"| {sp} | {b:.0f} | {n} | {v:.1%} |" for sp, b, n, v in points]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[:16]))


if __name__ == "__main__":
    main()
