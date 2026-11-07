"""Study D: three possible Russian-driven shifts in Dolgan, by speaker birth year.

    python3 case_change/russian_shift.py data/derived/dolgan reports/study_d_russian_shift.md

Pre-specified in case_change/STUDY_D_PLAN.md (committed before the first run).
D1 overt personal-pronoun subjects vs zero subjects; D2 PST2 vs PST1 among finite
pasts; D3 converbs among lexical verbs; PC (positive control) Russian-origin words.
Same speaker-clustered wild bootstrap as B2 (D-034, D-037); Holm over D1-D3.
"""
import argparse
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "shared"))

from b2_test import BIRTH_BINS, FALLBACK_CONTROLS, PRIMARY_CONTROLS, _bin, _mid, cells, choose_controls  # noqa: E402
from evid_descriptives import finite_pasts  # noqa: E402
from inel import gloss  # noqa: E402
from inel.load import table  # noqa: E402
from speaker_test import adjusted_test  # noqa: E402

SEED = 20261106
LOO_BOOT = 999
MIN_SPEAKERS = 5
HYPOTHESES = ("D1", "D2", "D3")
TITLES = {
    "D1": "overt personal-pronoun subject (vs zero subject); predicted up",
    "D2": "PST2 among finite pasts (vs PST1); predicted down",
    "D3": "converb among lexical verbs; predicted down",
    "PC": "Russian-origin word among glossed words (positive control); predicted up",
}
Y = lambda r: r["y"]  # noqa: E731


def attach(tokens, texts, speakers):
    """Give each token its text's genre, source and recording years and its speaker's birth years."""
    tx = {t["text_id"]: t for t in texts}
    sp = {s["speaker_id"]: s for s in speakers}
    for t in tokens:
        x, s = tx.get(t["text_id"], {}), sp.get(t["speaker_id"], {})
        t["genre"] = x.get("genre", "") or "unknown"
        t["source_collection"] = x.get("source_collection", "") or "unknown"
        t["recording_lo"], t["recording_hi"] = x.get("recording_lo", ""), x.get("recording_hi", "")
        t["birth_lo"], t["birth_hi"] = s.get("birth_lo", ""), s.get("birth_hi", "")
    return tokens


def _unit(t, y):
    return {k: t[k] for k in ("speaker_id", "genre", "source_collection", "recording_lo", "recording_hi",
                              "birth_lo", "birth_hi")} | {"y": int(y)}


def d1_units(tokens):
    """Subjects from SyF: 1 = overt personal pronoun (form pro*, ps pers), 0 = zero subject (form 0*)."""
    out = []
    for t in tokens:
        for item in (t.get("SyF") or "").split():
            form, _, func = item.partition(":")
            if func != "S":
                continue
            if form.startswith("0"):
                out.append(_unit(t, 0))
            elif form.startswith("pro") and t["ps"] == "pers":
                out.append(_unit(t, 1))
    return out


def d2_units(tokens):
    return [_unit(t, y) for t, y in finite_pasts(tokens)]


def d3_units(tokens):
    return [_unit(t, gloss.has_component(t["ge"], "CVB")) for t in tokens if t["ps"] == "v" and t["ge"]]


def pc_units(tokens):
    def rus(t):
        return t["BOR"].lstrip("%").startswith("RUS") or t["CS"].startswith("RUS")
    return [_unit(t, rus(t)) for t in tokens if t["ge"]]


def dated(units):
    return [u for u in units if _mid(u["birth_lo"], u["birth_hi"]) is not None]


def holm(ps):
    """Holm-adjusted p-values, same order as the input; None stays None."""
    idx = sorted((i for i, p in enumerate(ps) if p is not None), key=lambda i: ps[i])
    m, out, run = len(idx), [None] * len(ps), 0.0
    for rank, i in enumerate(idx):
        run = max(run, min(1.0, (m - rank) * ps[i]))
        out[i] = run
    return out


def test(units, rng, n_boot, time="birth", controls=PRIMARY_CONTROLS):
    """(speakers, units, estimate per decade or None, p or None, note)."""
    cs = cells(units, time, controls, Y)
    n_spk, n = len({c[0] for c in cs}), sum(c[4] for c in cs)
    if n_spk < MIN_SPEAKERS:
        return n_spk, n, None, None, "too few speakers"
    est, p = adjusted_test(cs, n_boot, rng, controls=bool(controls))
    if est is None:
        return n_spk, n, None, None, "time not separable from controls"
    return n_spk, n, est, p, ""


def _fmt(label, r, padj=None):
    n_spk, n, est, p, note = r
    if est is None:
        return f"| {label} | {n_spk} | {n} | {note} | | |"
    return f"| {label} | {n_spk} | {n} | {100 * est:+.2f} | {p:.4f} | " + ("" if padj is None else f"{padj:.4f}") + " |"


def describe(units):
    by_bin, by_spk = {}, {}
    for u in units:
        b = _mid(u["birth_lo"], u["birth_hi"])
        k, n = by_bin.get(_bin(b, BIRTH_BINS), (0, 0))
        by_bin[_bin(b, BIRTH_BINS)] = (k + u["y"], n + 1)
        k, n, _ = by_spk.get(u["speaker_id"], (0, 0, b))
        by_spk[u["speaker_id"]] = (k + u["y"], n + 1, b)
    out = ["| Birth bin | Units | Outcome 1 | Share |", "|---|---|---|---|"]
    out += [f"| {b} | {n} | {k} | {k / n:.1%} |" for b, (k, n) in sorted(by_bin.items())]
    out += ["", "| Speaker | Birth year | Units | Share |", "|---|---|---|---|"]
    out += [f"| {s} | {b:.0f} | {n} | {k / n:.1%} |"
            for s, (k, n, b) in sorted(by_spk.items(), key=lambda x: (x[1][2], x[0]))]
    return out


def analyse(tokens, n_boot=9999, seed=SEED):
    rng = random.Random(seed)
    sets = {"D1": dated(d1_units(tokens)),  # SyF items exist only in the 50 SyF texts
            "D2": dated(d2_units(tokens)), "D3": dated(d3_units(tokens)), "PC": dated(pc_units(tokens))}
    res = {}
    for h, units in sets.items():
        ctl, shares = choose_controls(units, Y)
        primary = test(units, rng, n_boot, controls=ctl) if ctl else (len({u["speaker_id"] for u in units}),
                                                                     len(units), None, None, "NOT CONFIRMATORY")
        res[h] = {"units": units, "ctl": ctl, "shares": shares, "primary": primary,
                  "unadj": test(units, rng, n_boot, controls=()),
                  "rec": test(units, rng, n_boot, time="recording", controls=ctl or PRIMARY_CONTROLS)}
    adj = holm([res[h]["primary"][3] for h in HYPOTHESES])
    for h, a in zip(HYPOTHESES, adj):
        res[h]["holm"] = a
        res[h]["loo"] = []
        if a is not None and a < 0.05:
            for s in sorted({u["speaker_id"] for u in res[h]["units"]}):
                rest = [u for u in res[h]["units"] if u["speaker_id"] != s]
                res[h]["loo"].append((s, test(rest, rng, LOO_BOOT, controls=res[h]["ctl"])))
    return res


def verdict(r):
    est, a = r["primary"][2], r.get("holm")
    if est is None or a is None:
        return "not testable"
    if a >= 0.05:
        return "not supported (Holm p >= 0.05)"
    signs = {e > 0 for _, (_, _, e, _, _) in r["loo"] if e is not None}
    return "**supported**" if signs == {est > 0} else "fragile (a leave-one-out estimate changes sign)"


def report(res, n_boot):
    names = lambda c: " and ".join("source" if x == "source_collection" else x for x in c)  # noqa: E731
    lines = ["# Study D results: possible Russian-driven shifts by birth year", "",
             "Built by `case_change/russian_shift.py` from the plan in `case_change/STUDY_D_PLAN.md`, committed "
             "before this run. Estimates are percentage points per decade of birth year; p from "
             f"{n_boot} wild-cluster-bootstrap draws by speaker ({LOO_BOOT} for leave-one-out), seed {SEED}. "
             "Holm correction over D1-D3; PC is a positive control, not corrected.", "",
             "## Primary tests", "",
             "| Hypothesis | Adjusted for | Speakers | Units | Change per decade (points) | p | Holm p | Verdict |",
             "|---|---|---|---|---|---|---|---|"]
    for h in HYPOTHESES + ("PC",):
        r = res[h]
        n_spk, n, est, p, note = r["primary"]
        ctl = names(r["ctl"]) if r["ctl"] else "none (decision rule)"
        cell = note if est is None else f"{100 * est:+.2f} | {p:.4f} | " + (
            f"{r['holm']:.4f}" if h != "PC" else "n/a")
        v = verdict(r) if h != "PC" else ("detects a difference (p < 0.05)" if p is not None and p < 0.05
                                         else "no difference detected")
        lines.append(f"| {h}: {TITLES[h]} | {ctl} | {n_spk} | {n} | {cell} | {v} |")
    lines += ["", "Decision rule (share of birth-year variance explained): " + "; ".join(
        f"{h} genre + source {res[h]['shares'].get(PRIMARY_CONTROLS, 0):.2f}"
        + (f", genre {res[h]['shares'][FALLBACK_CONTROLS]:.2f}" if FALLBACK_CONTROLS in res[h]["shares"] else "")
        for h in HYPOTHESES + ("PC",)) + "."]
    lines += ["", "## Secondary rows (not corrected)", "",
              "| Row | Speakers | Units | Change per decade (points) | p | |", "|---|---|---|---|---|---|"]
    for h in HYPOTHESES + ("PC",):
        lines.append(_fmt(f"{h}, unadjusted", res[h]["unadj"]))
        lines.append(_fmt(f"{h}, recording year, adjusted", res[h]["rec"]))
    for h in HYPOTHESES:
        if res[h]["loo"]:
            lines += ["", f"## {h}: leave one speaker out", "",
                      "| Speaker left out | Speakers | Units | Change per decade (points) | p | |",
                      "|---|---|---|---|---|---|"]
            lines += [_fmt(s, r) for s, r in res[h]["loo"]]
    for h in HYPOTHESES + ("PC",):
        lines += ["", f"## Descriptive: {h}, {TITLES[h]}", ""] + describe(res[h]["units"])
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("derived", help="folder with tokens.csv, texts.csv, speakers.csv")
    ap.add_argument("out")
    ap.add_argument("--boot", type=int, default=9999)
    a = ap.parse_args(argv)
    tokens = attach(table(a.derived, "tokens"), table(a.derived, "texts"), table(a.derived, "speakers"))
    res = analyse(tokens, a.boot)
    lines = report(res, a.boot)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[:14]))


if __name__ == "__main__":
    main()
