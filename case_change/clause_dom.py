"""Study C: object marking by clause type in Dolgan and Evenki (case_change/STUDY_C_PLAN.md).

    python3 case_change/clause_dom.py data/derived/dolgan/objects.csv data/derived/evenki/objects.csv \\
        reports/study_c_clause_dom.md [--boot 9999]

Writes counts and test results only: no sentences, no speaker IDs.
"""
import argparse
import csv
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from speaker_test import adjusted_test  # noqa: E402

IRREALIS = frozenset({"IMP", "FUT", "COND", "NEC", "DEB", "SBJV", "DESID", "POT", "CAP", "HORT", "JUSS"})
IRREALIS_EXTENDED = IRREALIS | {"INTNS", "PROB"}
REALIS = frozenset({"PST", "PRS", "HAB", "AOR", "NFUT"})

# corpus -> (indefinite-type marker, the other cases it is compared with)
OUTCOME = {"dolgan": ("PART", ("NOM", "ACC")), "evenki": ("ACC.INDF", ("NOM", "ACC"))}


def clause_type(pred_labels, irrealis=IRREALIS):
    """'irrealis', 'realis', 'other', or '' when no predicate was found."""
    if not pred_labels.strip():
        return ""
    comps = {re.sub(r"\d+$", "", c) for c in pred_labels.split()}
    if comps & irrealis:
        return "irrealis"
    if comps & REALIS:
        return "realis"
    return "other"


def load(path, corpus):
    marker, others = OUTCOME[corpus]
    with open(path, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["case"] in (marker,) + others]
    for r in rows:
        r["_y"] = int(r["case"] == marker)
        r["_corpus"] = corpus
    return rows


def cells(rows, irrealis=IRREALIS, controls=("genre",)):
    """[(speaker, x, control labels, successes, n)] with x = 1 for irrealis, 0 for realis."""
    d = {}
    for r in rows:
        ct = clause_type(r["pred_labels"], irrealis)
        if ct not in ("irrealis", "realis"):
            continue
        x = int(ct == "irrealis")
        labels = tuple(r[c] or "unknown" for c in controls)
        key = (r["_corpus"] + ":" + r["speaker_id"], x, labels)
        k, n = d.get(key, (0, 0))
        d[key] = (k + r["_y"], n + 1)
    return [(g, x, lab, k, n) for (g, x, lab), (k, n) in sorted(d.items())]


def odds_ratio(rows, irrealis=IRREALIS):
    """Irrealis-versus-realis odds ratio of the marker (0.5 added to each cell), or None."""
    c = {"irrealis": [0.5, 0.5], "realis": [0.5, 0.5]}
    seen = set()
    for r in rows:
        ct = clause_type(r["pred_labels"], irrealis)
        if ct in c:
            c[ct][0 if r["_y"] else 1] += 1
            seen.add(ct)
    if len(seen) < 2:
        return None
    return (c["irrealis"][0] / c["irrealis"][1]) / (c["realis"][0] / c["realis"][1])


def ratio_of_odds_ratios(dlg, evk, rng, boot=2000, irrealis=IRREALIS):
    """(OR Dolgan, OR Evenki, their ratio, 95% interval of the ratio) resampling speakers in each corpus.

    H4 on the odds scale: an additive (percentage-point) interaction would mostly reflect the
    different base rates of PART and ACC.INDF (review, 2026-11-06).
    """
    def by_speaker(rows):
        d = {}
        for r in rows:
            d.setdefault(r["speaker_id"], []).append(r)
        return list(d.values())
    sd, se = by_speaker(dlg), by_speaker(evk)
    ord_, ore = odds_ratio(dlg, irrealis), odds_ratio(evk, irrealis)
    if ord_ is None or ore is None:
        return ord_, ore, None, None, None
    draws = []
    for _ in range(boot):
        a = odds_ratio([r for g in (rng.choice(sd) for _ in sd) for r in g], irrealis)
        e = odds_ratio([r for g in (rng.choice(se) for _ in se) for r in g], irrealis)
        if a is not None and e is not None:
            draws.append(a / e)
    draws.sort()
    lo, hi = (draws[int(0.025 * len(draws))], draws[int(0.975 * len(draws)) - 1]) if draws else (None, None)
    return ord_, ore, ord_ / ore, lo, hi


def h4_line(label, dlg, evk, rng, irrealis=IRREALIS):
    ord_, ore, ratio, lo, hi = ratio_of_odds_ratios(dlg, evk, rng, irrealis=irrealis)
    if ratio is None:
        return f"| {label} | not computable | | | |"
    return f"| {label} | {ord_:.2f} | {ore:.2f} | {ratio:.2f} | {lo:.2f} to {hi:.2f} |"


def counts_table(rows, corpus):
    marker, others = OUTCOME[corpus]
    cases = (marker,) + others
    by = {}
    spk = {}
    for r in rows:
        ct = clause_type(r["pred_labels"]) or "no predicate"
        by.setdefault(ct, dict.fromkeys(cases, 0))[r["case"]] += 1
        if r["_y"]:
            spk.setdefault(ct, set()).add(r["speaker_id"])
    out = [f"| Clause type | " + " | ".join(cases) + f" | {marker} share | Speakers using {marker} |",
           "|---|" + "---|" * (len(cases) + 2)]
    for ct in ("irrealis", "realis", "other", "no predicate"):
        if ct not in by:
            continue
        c = by[ct]
        total = sum(c.values())
        out.append(f"| {ct} | " + " | ".join(str(c[x]) for x in cases)
                   + f" | {c[marker] / total:.1%} | {len(spk.get(ct, ()))} |")
    return out


def test_row(label, cs, n_boot, rng, controls=True):
    n_spk, n_obj = len({c[0] for c in cs}), sum(c[4] for c in cs)
    if n_spk < 5 or len({c[1] for c in cs}) < 2:
        return f"| {label} | {n_spk} | {n_obj} | not testable | |"
    est, p = adjusted_test(cs, n_boot, rng, controls=controls, scale=1)
    if est is None:
        return f"| {label} | {n_spk} | {n_obj} | not separable from controls | |"
    return f"| {label} | {n_spk} | {n_obj} | {100 * est:+.1f} | {p:.3f} |"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dolgan")
    ap.add_argument("evenki")
    ap.add_argument("out")
    ap.add_argument("--boot", type=int, default=9999)
    a = ap.parse_args(argv)
    dlg, evk = load(a.dolgan, "dolgan"), load(a.evenki, "evenki")
    nopro = [r for r in dlg + evk if r["pronoun"] == "0"]
    rng = random.Random(20261106)
    b = a.boot
    lines = ["# Study C: object marking by clause type, Dolgan and Evenki", "",
             "Built by `case_change/clause_dom.py` from the plan in `case_change/STUDY_C_PLAN.md`. Counts are "
             "objects (SyF function O) whose case is the marker or NOM/ACC. Estimates are the irrealis-minus-realis "
             "difference in the marker's share, in percentage points, from speaker-clustered regressions; p is "
             f"from {b} wild-cluster-bootstrap draws by speaker.", "",
             "## Counts by clause type", "", "### Dolgan (marker PART)", ""] + counts_table(dlg, "dolgan") + [
             "", "### Evenki (marker ACC.INDF)", ""] + counts_table(evk, "evenki") + [
             "", "## Tests", "", "| Test | Speakers | Objects | Irrealis minus realis (points) | p |",
             "|---|---|---|---|---|",
             test_row("H1 Dolgan PART, adjusted for genre", cells(dlg), b, rng),
             test_row("H3 Evenki ACC.INDF, adjusted for genre", cells(evk), b, rng),
             "", "## Robustness", "", "| Test | Speakers | Objects | Irrealis minus realis (points) | p |",
             "|---|---|---|---|---|",
             test_row("H1 extended irrealis (adds INTNS, PROB)", cells(dlg, IRREALIS_EXTENDED), b, rng),
             test_row("H3 extended irrealis", cells(evk, IRREALIS_EXTENDED), b, rng),
             test_row("H1 no pronoun objects", cells([r for r in nopro if r["_corpus"] == "dolgan"]), b, rng),
             test_row("H3 no pronoun objects", cells([r for r in nopro if r["_corpus"] == "evenki"]), b, rng),
             test_row("H1 unadjusted", cells(dlg, controls=()), b, rng, controls=False),
             test_row("H3 unadjusted", cells(evk, controls=()), b, rng, controls=False),
             "", "## H4: Dolgan versus Evenki on the odds scale", "",
             "Irrealis-versus-realis odds ratio of the marker in each corpus, and their ratio. A ratio above 1 "
             "means the clause effect is stronger in Dolgan. 95% interval from 2,000 draws resampling speakers "
             "within each corpus. Unadjusted for genre.", "",
             "| Analysis | OR Dolgan | OR Evenki | Ratio | 95% interval |", "|---|---|---|---|---|",
             h4_line("H4 core irrealis", dlg, evk, rng),
             h4_line("H4 extended irrealis", dlg, evk, rng, IRREALIS_EXTENDED),
             h4_line("H4 no pronoun objects", [r for r in nopro if r["_corpus"] == "dolgan"],
                     [r for r in nopro if r["_corpus"] == "evenki"], rng)]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
