"""Would tagging the 86 untagged Dolgan texts give Study B enough power? Design only.

    python3 case_change/power_expansion.py data/derived/dolgan reports/power_expansion.md [--sims 200]

Reads the current object table's design columns (as power.py does) and, for the untagged
texts, the tagger's P(object) for each nominal (data/derived/dolgan/review_key/predictions.csv).
The expected number of objects per speaker and text is the sum of P(O): the model is
calibrated (reports/tagger_eval.md), so this estimates how many objects the review will
confirm. No case value is read anywhere: predictions.csv has a case column, and this
script does not open it.

Compares the power of the B2-type test (birth year, adjusted for genre and source, wild
cluster bootstrap by speaker) for: the current data; current plus expanded; and the
within-genre designs (narrative only, conversation only) that Study D showed are needed.
"""
import argparse
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from power import _mid, cells_from, read_design  # noqa: E402
from speaker_test import collinearity, power_cells  # noqa: E402

PRED_COLS = ("utt_id", "text_id", "speaker_id", "ps", "p_O")  # never "case"
NOMINAL_PS = {"n", "pers", "dempro", "propr", "emphpro", "indfpro", "posspr", "que", "quant", "cardnum", "adj"}


def expected_objects(derived):
    texts = {t["text_id"]: t for t in csv.DictReader(open(os.path.join(derived, "texts.csv"), encoding="utf-8"))}
    spk = {s["speaker_id"]: s for s in csv.DictReader(open(os.path.join(derived, "speakers.csv"), encoding="utf-8"))}
    sums = {}
    with open(os.path.join(derived, "review_key", "predictions.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r = {k: r[k] for k in PRED_COLS}
            if r["ps"] in NOMINAL_PS:
                k = (r["speaker_id"], r["text_id"])
                sums[k] = sums.get(k, 0.0) + float(r["p_O"])
    rows = []
    for (s, t), e in sorted(sums.items()):
        tx, sp = texts.get(t, {}), spk.get(s, {})
        row = {"speaker_id": s, "birth_lo": sp.get("birth_lo", ""), "birth_hi": sp.get("birth_hi", ""),
               "birth_mid": "", "recording_lo": tx.get("recording_lo", ""), "recording_hi": tx.get("recording_hi", ""),
               "genre": tx.get("genre", ""), "source_collection": tx.get("source_collection", ""), "n_preds_in_utt": ""}
        rows += [dict(row) for _ in range(int(round(e)))]
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("derived")
    ap.add_argument("out")
    ap.add_argument("--sims", type=int, default=200)
    a = ap.parse_args(argv)
    current = read_design(os.path.join(a.derived, "objects.csv"))
    new = expected_objects(a.derived)
    designs = {
        "current, all genres": current,
        "current + expanded, all genres": current + new,
        "current + expanded, narrative only": [r for r in current + new if r["genre"] == "nar"],
        "current + expanded, conversation only": [r for r in current + new if r["genre"] == "conv"],
        "current, narrative only": [r for r in current if r["genre"] == "nar"],
    }
    lines = ["# Study B: would the expansion add power? (design only)", "",
             "Built by `case_change/power_expansion.py`. Expected new objects per speaker and text = sum of the "
             "tagger's P(object) over nominals in the untagged texts (the model is calibrated). No case value was "
             f"read. Test: birth year adjusted for genre and source (genre only within one genre); baseline accusative "
             f"share 0.8 (an input); {a.sims} simulations per cell; wild cluster bootstrap by speaker.", "",
             "| Design | Speakers with a birth year | Objects | Birth-year variance explained by controls | "
             "Power OR 1.5, SD 0.5 | OR 1.5, SD 1.0 | OR 2.0, SD 0.5 | OR 2.0, SD 1.0 |", "|---|---|---|---|---|---|---|---|"]
    for name, rows in designs.items():
        ctl = ("source_collection",) if "only" in name else ("genre", "source_collection")
        cells = cells_from(rows, "birth", ctl, 1)
        n_spk = len({c[0] for c in cells})
        r2 = collinearity([(g, t, lab, 0, n) for g, t, lab, n in cells]) if cells else None
        vals = []
        for orat in (1.5, 2.0):
            for sd in (0.5, 1.0):
                vals.append(power_cells(cells, 0.8, math.log(orat), sd, n_sim=a.sims, seed=7, controls=True)
                            if n_spk >= 5 else None)
        lines.append(f"| {name} | {n_spk} | {sum(c[3] for c in cells)} | " + ("n/a" if r2 is None else f"{r2:.2f}") + " | "
                     + " | ".join("n/a" if v is None else f"{v:.2f}" for v in vals) + " |")
        print(lines[-1], flush=True)
    lines += ["", "Within one genre the controls are source only. Speakers with a birth-year range over 10 years are "
                  "left out, as in B2."]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
