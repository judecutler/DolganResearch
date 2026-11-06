"""Study B2 design report: how tangled time is with genre and source, and the power of
each test, from the real design without looking at the outcome.

    python3 case_change/power.py data/derived/dolgan/objects.csv reports/power_b2.md [--sims 200]

Reads only the columns in DESIGN_COLUMNS (speaker, birth and recording years, genre,
source). The case column is never read, so this can run before Gate 3 (D-026). It
counts every object, including the few whose case is not NOM, ACC or PART, so the
object counts are slightly higher than in the analysis.

Takes about 5 to 10 minutes at 200 simulations per cell: run it in the background.
"""
import argparse
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from speaker_test import collinearity, power_cells  # noqa: E402

PRECISE = 10
DESIGN_COLUMNS = ("speaker_id", "birth_lo", "birth_hi", "birth_mid", "recording_lo", "recording_hi",
                  "genre", "source_collection")
CONTROL_SETS = {"none": (), "genre": ("genre",), "genre + source": ("genre", "source_collection")}
ODDS_RATIOS = (1.0, 1.2, 1.35, 1.5, 2.0)
SDS = (0.5, 1.0)


def read_design(path):
    """Object rows reduced to DESIGN_COLUMNS. No other column leaves this function."""
    with open(path, encoding="utf-8") as f:
        return [{k: r.get(k, "") for k in DESIGN_COLUMNS} for r in csv.DictReader(f)]


def _mid(lo, hi):
    if not lo or not hi or float(hi) - float(lo) > PRECISE:
        return None
    return (float(lo) + float(hi)) / 2


def design_from(objects_csv, min_tokens=1):
    """[(birth_mid, n_objects)] for speakers with a usable birth year."""
    counts, birth = {}, {}
    for r in read_design(objects_csv):
        if _mid(r["birth_lo"], r["birth_hi"]) is None:
            continue
        counts[r["speaker_id"]] = counts.get(r["speaker_id"], 0) + 1
        birth[r["speaker_id"]] = float(r["birth_mid"])
    return [(birth[s], n) for s, n in sorted(counts.items()) if n >= min_tokens]


def cells_from(rows, time="birth", controls=(), min_tokens=3):
    """[(speaker, time_in_years, control_labels, n)] for the cell tests.

    time "birth": the speaker's birth year (apparent time). time "recording": the text's
    recording year (real time). Rows without a usable year are dropped, and so are
    speakers with fewer than min_tokens objects left.
    """
    cells, per = {}, {}
    for r in rows:
        t = _mid(r["birth_lo"], r["birth_hi"]) if time == "birth" else _mid(r["recording_lo"], r["recording_hi"])
        if t is None or (time == "recording" and _mid(r["birth_lo"], r["birth_hi"]) is None):
            continue
        key = (r["speaker_id"], t, tuple(r[c] or "unknown" for c in controls))
        cells[key] = cells.get(key, 0) + 1
        per[r["speaker_id"]] = per.get(r["speaker_id"], 0) + 1
    return [(g, t, lab, n) for (g, t, lab), n in sorted(cells.items()) if per[g] >= min_tokens]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("objects")
    p.add_argument("out")
    p.add_argument("--base", type=float, default=0.8)
    p.add_argument("--sims", type=int, default=200)
    p.add_argument("--min-tokens", type=int, default=3)
    a = p.parse_args(argv)
    rows = read_design(a.objects)
    birth = cells_from(rows, "birth", (), a.min_tokens)
    if len({g for g, *_ in birth}) < 4:
        sys.exit("fewer than 4 speakers with a usable birth year and enough objects: no power analysis possible")
    se = 2 * math.sqrt(0.0475 / a.sims)
    lines = ["# Study B2: design and power", "",
             "Built by `case_change/power.py` from design columns only (speaker, birth and recording years, "
             "genre, source). The outcome was not read. Every simulated effect is an odds ratio per decade; "
             f"baseline accusative share {a.base} (an input); {a.sims} simulations per cell; alpha 0.05; "
             "wild cluster bootstrap by speaker (D-034). Row 1.0 is the false-positive rate: within about "
             f"{se:.2f} of 0.05 is consistent with a correct test. Speaker SD is the between-speaker spread on "
             "the log-odds scale, unknown until the outcome is seen. The simulations give genre and source "
             "no effect of their own; with such an effect, only the adjusted tests keep their false-positive "
             "rate (D-037).", "", "## How tangled is time with genre and source?", "",
             "Share of the object-weighted variance of the time variable explained by the controls. 0 means "
             "independent, 1 means time cannot be told apart from them. Above about 0.8 an adjusted test has "
             "little information left.", "", "| Time variable | Controls | Speakers | Objects | Explained |",
             "|---|---|---|---|---|"]
    for time in ("birth", "recording"):
        for name, ctl in list(CONTROL_SETS.items())[1:]:
            cells = cells_from(rows, time, ctl, a.min_tokens)
            r2 = collinearity([(g, t, lab, 0, n) for g, t, lab, n in cells]) if cells else None
            lines.append(f"| {time} year | {name} | {len({c[0] for c in cells})} | {sum(c[3] for c in cells)} | "
                         + ("n/a" if r2 is None else f"{r2:.2f}") + " |")
    for time in ("birth", "recording"):
        lines += ["", f"## Power, time = {time} year", "",
                  "| Odds ratio per decade | " + " | ".join(f"{c}, SD {sd}" for c in CONTROL_SETS for sd in SDS) + " |",
                  "|---|" + "---|" * (len(CONTROL_SETS) * len(SDS))]
        designs = {c: cells_from(rows, time, ctl, a.min_tokens) for c, ctl in CONTROL_SETS.items()}
        for orat in ODDS_RATIOS:
            vals = [power_cells(designs[c], a.base, math.log(orat), sd, n_sim=a.sims, seed=7,
                                controls=bool(CONTROL_SETS[c])) for c in CONTROL_SETS for sd in SDS]
            lines.append(f"| {orat} | " + " | ".join(f"{v:.2f}" for v in vals) + " |")
            print(lines[-1], flush=True)
    lines += ["", "Report in the paper the smallest odds ratio with power 0.8 or more for the test the frozen "
              "plan names as primary."]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
