"""Study A, exploratory: what the corpus glosses alone say about evidential forms.

    python3 shared/evid_descriptives.py data/derived/dolgan data/derived/evenki reports/study_a_descriptives.md

Uses the annotators' glosses only, not Jude and Dustan's coding, so every number is
labelled exploratory. The questions:
  1. How often each evidential or past form occurs per 1,000 glossed words, by genre,
     in Dolgan and Evenki.
  2. Is the indirect past PST2 (-BIt, the "postterminal", D-022) the usual past of
     folklore, and the direct past PST1 the usual past of personal narrative and
     conversation?
  3. Is PST2 rarer with first-person subjects, as a "not witnessed" reading predicts?
Tests are speaker-clustered (speaker_test.adjusted_test with a 0/1 predictor). Output
holds counts only: no sentences, no speaker IDs.
"""
import argparse
import os
import random
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "case_change"))

from inel import gloss  # noqa: E402
from inel.load import table  # noqa: E402
from speaker_test import adjusted_test  # noqa: E402

# label -> whether participles count. Finite forms only for tense labels.
FORMS = {
    "dolgan": (("EVID", True), ("INFER", True), ("PST2", False), ("PST1", False), ("COND1", False)),
    "evenki": (("EVID", True), ("PST", False), ("PRF", False), ("AOR", False)),
}


def is_form(ge, label, participles_ok):
    if not gloss.has_component(ge, label, certain_only=True):
        return False
    return participles_ok or not gloss.has_component(ge, "PTCP")


def person_group(ge):
    pn = gloss.person_number(ge) or ""
    return pn[:1] if pn[:1] in "123" and pn else "none"


def rates(tokens, corpus):
    words = Counter(t["genre"] for t in tokens if t["ge"])
    hits = {lab: Counter() for lab, _ in FORMS[corpus]}
    spk = {lab: defaultdict(set) for lab, _ in FORMS[corpus]}
    for t in tokens:
        if not t["ge"]:
            continue
        for lab, ptcp in FORMS[corpus]:
            if is_form(t["ge"], lab, ptcp):
                hits[lab][t["genre"]] += 1
                spk[lab][t["genre"]].add(t["speaker_id"])
    labs = [lab for lab, _ in FORMS[corpus]]
    out = ["| Genre | Glossed words | " + " | ".join(f"{lab} per 1,000 (n; speakers)" for lab in labs) + " |",
           "|---|---|" + "---|" * len(labs)]
    for g in sorted(words):
        cells = [f"{1000 * hits[lab][g] / words[g]:.2f} ({hits[lab][g]}; {len(spk[lab][g])})" for lab in labs]
        out.append(f"| {g} | {words[g]} | " + " | ".join(cells) + " |")
    return out


def finite_pasts(tokens):
    """Dolgan finite past verbs: (token, 1 if PST2 else 0)."""
    out = []
    for t in tokens:
        ge = t["ge"]
        if not ge or gloss.has_component(ge, "PTCP"):
            continue
        p2, p1 = gloss.has_component(ge, "PST2", True), gloss.has_component(ge, "PST1", True)
        if p2 != p1:
            out.append((t, int(p2)))
    return out


def share_table(pasts, key, label):
    c = defaultdict(lambda: [0, 0])
    for t, y in pasts:
        c[key(t)][0] += y
        c[key(t)][1] += 1
    out = [f"| {label} | Finite past verbs | PST2 | PST2 share |", "|---|---|---|---|"]
    for k in sorted(c):
        k2, n = c[k]
        out.append(f"| {k} | {n} | {k2} | {k2 / n:.1%} |")
    return out


def binary_cells(pasts, x_of, controls=()):
    d = {}
    for t, y in pasts:
        x = x_of(t)
        if x is None:
            continue
        key = (t["speaker_id"], x, tuple(t.get(c, "") or "unknown" for c in controls))
        k, n = d.get(key, (0, 0))
        d[key] = (k + y, n + 1)
    return [(g, x, lab, k, n) for (g, x, lab), (k, n) in sorted(d.items())]


def test_row(label, cells, n_boot, rng, controls):
    n_spk, n = len({c[0] for c in cells}), sum(c[4] for c in cells)
    if n_spk < 5 or len({c[1] for c in cells}) < 2:
        return f"| {label} | {n_spk} | {n} | not testable | |"
    est, p = adjusted_test(cells, n_boot, rng, controls=bool(controls), scale=1)
    if est is None:
        return f"| {label} | {n_spk} | {n} | not separable from controls | |"
    return f"| {label} | {n_spk} | {n} | {100 * est:+.1f} | {p:.3f} |"


def with_text_fields(tokens, texts):
    by = {t["text_id"]: t for t in texts}
    for t in tokens:
        tx = by.get(t["text_id"], {})
        t["genre"] = tx.get("genre", "") or "unknown"
        t["source"] = tx.get("source_collection", "") or "unknown"
    return tokens


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dolgan")
    ap.add_argument("evenki")
    ap.add_argument("out")
    ap.add_argument("--boot", type=int, default=9999)
    a = ap.parse_args(argv)
    dlg = with_text_fields(table(a.dolgan, "tokens"), table(a.dolgan, "texts"))
    evk = with_text_fields(table(a.evenki, "tokens"), table(a.evenki, "texts"))
    pasts = finite_pasts(dlg)
    rng = random.Random(20261106)
    b = a.boot
    genre_x = lambda t: {"flk": 1, "nar": 0}.get(t["genre"])  # noqa: E731
    first_x = lambda t: {"1": 1, "3": 0}.get(person_group(t["ge"])) if t["genre"] in ("nar", "conv") else None  # noqa: E731
    lines = ["# Study A, exploratory: evidential and past forms in the corpus glosses", "",
             "Built by `shared/evid_descriptives.py`. **Exploratory.** These counts use the INEL annotators' "
             "glosses (only glosses without `%`), not Jude and Dustan's coding, and no hypothesis was fixed "
             "in advance. Tense forms are counted only on finite verbs (no `PTCP`).", "",
             "## 1. Forms per 1,000 glossed words, by genre", "", "### Dolgan", ""] + rates(dlg, "dolgan") + [
             "", "### Evenki", ""] + rates(evk, "evenki") + [
             "", "## 2. Dolgan finite past verbs: PST2 (indirect) versus PST1 (direct)", "",
             ] + share_table(pasts, lambda t: t["genre"], "Genre") + [""] + share_table(
                 pasts, lambda t: person_group(t["ge"]), "Subject person") + [""] + share_table(
                 [(t, y) for t, y in pasts if t["genre"] in ("flk", "nar", "conv")],
                 lambda t: f"{t['genre']}, person {person_group(t['ge'])}", "Genre and person") + [
             "", "## 3. Speaker-clustered tests (exploratory)", "",
             "Estimates are differences in PST2 share in percentage points; p from "
             f"{b} wild-cluster-bootstrap draws by speaker.", "",
             "| Comparison | Speakers | Verbs | Difference (points) | p |", "|---|---|---|---|---|",
             test_row("Folklore minus personal narrative (flk vs nar)", binary_cells(pasts, genre_x), b, rng, ()),
             test_row("The same, adjusted for source", binary_cells(pasts, genre_x, ("source",)), b, rng, ("source",)),
             test_row("First minus third person subject, nar and conv only", binary_cells(pasts, first_x), b, rng, ()),
             test_row("The same, adjusted for genre", binary_cells(pasts, first_x, ("genre",)), b, rng, ("genre",))]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
