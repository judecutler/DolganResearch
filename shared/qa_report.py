"""QA report: do the tables match what handoff 002 measured on the real files?

    python3 shared/qa_report.py OUT.md data/derived/dolgan data/derived/evenki

Each check compares a count from the build with the figure from handoff 002
(config.EXPECTED_002). MATCH and DIFF are exact comparisons; "min" checks pass
when the count is at least the 002 figure. A missing count is INCONCLUSIVE,
never a pass. Only labels and counts are written, no corpus text.
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inel import config, gloss  # noqa: E402
from inel.load import table  # noqa: E402


def check(counts, expected):
    rows = []
    for name, exp in expected.items():
        value, kind = exp if isinstance(exp, tuple) else (exp, "eq")
        got = counts.get(name)
        if got is None:
            status = "INCONCLUSIVE"
        elif kind == "min":
            status = "MATCH" if got >= value else "DIFF"
        else:
            status = "MATCH" if got == value else "DIFF"
        rows.append((name, value if kind == "eq" else f">= {value}", got, status))
    return rows


def top(counter, n=15):
    return ", ".join(f"`{k or '(empty)'}` {v}" for k, v in counter.most_common(n))


def section(derived):
    with open(os.path.join(derived, "counts.json"), encoding="utf-8") as f:
        meta = json.load(f)
    corpus, counts = meta["corpus"], meta["counts"]
    rows = check(counts, config.EXPECTED_002[corpus])
    toks = table(derived, "tokens")
    texts = table(derived, "texts")
    qa = table(derived, "qa_flags")

    out = [f"## {corpus.capitalize()}", ""]
    n_diff = sum(r[3] != "MATCH" for r in rows)
    out.append(f"**Verdict: {'all checks MATCH' if not n_diff else f'{n_diff} of {len(rows)} checks do not match'}.**")
    out += ["", "| Count | Handoff 002 | This build | Status |", "|---|---|---|---|"]
    out += [f"| `{n}` | {e} | {g} | {s} |" for n, e, g, s in rows]

    doc = config.DOCUMENTED[corpus]
    out += ["", "Documentation figures (D-016; reported, not checked): " + ", ".join(
        f"{k} {v}" for k, v in doc.items()) + f". This build: transcripts {counts['transcripts']}, "
        f"utterances (`ref`) {counts['ref_events']}, tokens (`tx`) {counts['tx_events']}."]

    out += ["", "### QA flags", "", "| Flag | Count |", "|---|---|"]
    out += [f"| `{k}` | {v} |" for k, v in sorted(Counter(q["flag"] for q in qa).items())]
    unknown = sorted(q["detail"] for q in qa if q["flag"] == "unknown_tier")
    if unknown:
        out += ["", "Tiers not in `config.py` (carried nowhere; check whether they matter): " +
                ", ".join(f"`{u}`" for u in unknown)]

    funcs = Counter(fn for t in toks for fn in gloss.overt_functions(t["SyF"]))
    zero = Counter(fn for t in toks for f, fn in gloss.annotation_items(t["SyF"]) if f.startswith("0"))
    o_rule = counts["words_syf_ends_O"]
    o_items = sum(1 for t in toks if "O" in gloss.overt_functions(t["SyF"]))
    out += ["", "### Values that later steps rely on", "",
            f"- Objects: {o_rule} words by 002's rule (last `SyF` part is `O`), {o_items} by this "
            "pipeline's rule (any overt `form:O` item). The object table uses the second.",
            f"- `SyF` overt functions: {top(funcs)}.",
            f"- `SyF` zero-argument items: {top(zero, 8)}.",
            f"- `BOR` values (the object table treats any non-empty value as a loan; **check this**): "
            f"{top(Counter(t['BOR'] for t in toks if t['BOR']))}.",
            f"- `IST` values (the Study A rule `IST_quot` looks for `quot`; **check the spelling**): "
            f"{top(Counter(v for t in toks for v in (t['IST'] or '').split()), 20)}.",
            f"- Case labels on all words: {top(Counter(t['case'] for t in toks if t['case']))}.",
            f"- Source collection per text (inferred for Dolgan, D-013 note): "
            f"{top(Counter(t['source_collection'] for t in texts))}.",
            f"- Dialect per text: {top(Counter(t['dialect'] for t in texts))}.",
            f"- Part-of-speech (`ps`) values: {top(Counter(t['ps'] for t in toks), 30)}.",
            f"- Words with more than one case label: {sum(1 for t in toks if t['case_flag'])}."]
    return out, n_diff


def main(out_path, *derived_dirs):
    lines = ["# QA report", "",
             "Built by `shared/qa_report.py`. Compares the derived tables with the counts desktop Claude "
             "measured in handoff 002 (`handoff/outputs/002/structure_report.md`). No corpus text in this file.", ""]
    total = 0
    for d in derived_dirs:
        s, n = section(d)
        lines += s + [""]
        total += n
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return total


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    n = main(*sys.argv[1:])
    print("checks not matching:", n)
