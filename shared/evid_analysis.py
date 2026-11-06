"""Study A: analyse the merged main-round coding (docs/STUDY_A_MAIN_ROUND.md).

    python3 shared/evid_analysis.py main_merged.csv data/derived/dolgan data/derived/evenki \\
        reports/study_a_results.md

main_merged.csv is the output of `shared/workbook.py merge` for the main round. Each
item's code: a `resolved_is_evidential_use` column if Jude and Dustan added one; else
the shared code when both coders agree; else the single coder's code; a double-coded
disagreement with no resolution is left out and counted. For each corpus and rule
(the rule that found the item) it reports the share coded evidential with a 95%
interval from resampling speakers, and estimates evidential uses per 1,000 glossed
words by genre: candidates of that rule in the genre times the coded share.
"""
import argparse
import csv
import os
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inel.load import table  # noqa: E402

COL = "is_evidential_use"
MIN_GENRE_ITEMS = 20
BOOT = 2000


def final_code(m):
    if (m.get(f"resolved_{COL}") or "").strip():
        return m[f"resolved_{COL}"].strip()
    a, b = (m.get(f"{COL}_A") or "").strip(), (m.get(f"{COL}_B") or "").strip()
    if a and b:
        return a if a == b else "disagreement"
    return a or b


def share_with_interval(items, rng, boot=BOOT):
    """Share of 'yes' among yes/no items, and a 95% percentile interval resampling speakers."""
    yn = [(i["speaker_id"], i["_code"] == "yes") for i in items if i["_code"] in ("yes", "no")]
    if not yn:
        return None, None, None
    by = defaultdict(list)
    for s, y in yn:
        by[s].append(y)
    spk = sorted(by)
    est = sum(y for _, y in yn) / len(yn)
    draws = []
    for _ in range(boot):
        pick = [by[rng.choice(spk)] for _ in spk]
        n = sum(len(p) for p in pick)
        draws.append(sum(sum(p) for p in pick) / n)
    draws.sort()
    return est, draws[int(0.025 * boot)], draws[int(0.975 * boot) - 1]


def load_items(merged, cand_rows):
    cand = {c["token_id"]: c for c in cand_rows}
    with open(merged, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    items = []
    for m in rows:
        c = cand.get(m["token_id"])
        if c is None:
            continue
        items.append({"corpus": c["corpus"], "rule": c["rules"].split()[0], "genre": c["genre"] or "unknown",
                      "speaker_id": c["speaker_id"], "_code": final_code(m),
                      "info_source": (m.get("info_source_A") or m.get("info_source_B") or "").strip()})
    return items


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("merged")
    ap.add_argument("dolgan")
    ap.add_argument("evenki")
    ap.add_argument("out")
    a = ap.parse_args(argv)
    rng = random.Random(20261106)
    cands, words = [], Counter()
    for d in (a.dolgan, a.evenki):
        cands += table(d, "evid_candidates")
        for t in table(d, "texts"):
            words[(t["corpus"], t["genre"] or "unknown")] += int(t["n_tokens_glossed"] or 0)
    pop = Counter((c["corpus"], c["rules"].split()[0], c["genre"] or "unknown") for c in cands)
    items = load_items(a.merged, cands)
    codes = Counter(i["_code"] for i in items)
    lines = ["# Study A results: evidential use by form, genre and language", "",
             f"Built by `shared/evid_analysis.py`. Items: {len(items)}. Codes: "
             + ", ".join(f"{k or 'blank'} {v}" for k, v in sorted(codes.items()))
             + ". Shares are 'yes' among yes/no items; 95% intervals resample speakers "
             f"({BOOT} draws).", "", "## Share coded evidential, by rule", "",
             "| Corpus | Rule | Items | Yes | No | Unclear | Share | 95% interval |", "|---|---|---|---|---|---|---|---|"]
    by_rule = defaultdict(list)
    for i in items:
        by_rule[(i["corpus"], i["rule"])].append(i)
    shares = {}
    for (corp, rule), its in sorted(by_rule.items()):
        c = Counter(i["_code"] for i in its)
        est, lo, hi = share_with_interval(its, rng)
        shares[(corp, rule)] = est
        lines.append(f"| {corp} | `{rule}` | {len(its)} | {c['yes']} | {c['no']} | {c['unclear']} | "
                     + (" | " if est is None else f"{est:.1%} | {lo:.1%} to {hi:.1%}") + " |")
    lines += ["", f"## Share coded evidential, by rule and genre (cells with {MIN_GENRE_ITEMS}+ items)", "",
              "| Corpus | Rule | Genre | Items | Share | 95% interval |", "|---|---|---|---|---|---|"]
    by_rg = defaultdict(list)
    for i in items:
        by_rg[(i["corpus"], i["rule"], i["genre"])].append(i)
    genre_share = {}
    for key, its in sorted(by_rg.items()):
        if len(its) < MIN_GENRE_ITEMS:
            continue
        est, lo, hi = share_with_interval(its, rng)
        genre_share[key] = est
        if est is not None:
            lines.append(f"| {key[0]} | `{key[1]}` | {key[2]} | {len(its)} | {est:.1%} | {lo:.1%} to {hi:.1%} |")
    lines += ["", "## Estimated evidential uses per 1,000 glossed words, by genre", "",
              "Candidates of each rule in the genre times the coded share (the genre's own share where it has "
              f"{MIN_GENRE_ITEMS}+ items, otherwise the rule's overall share). No interval yet.", "",
              "| Corpus | Genre | Glossed words | Estimated evidential uses | Per 1,000 |", "|---|---|---|---|---|"]
    for (corp, genre), w in sorted(words.items()):
        total = 0.0
        for (c2, rule, g2), n in pop.items():
            if c2 == corp and g2 == genre:
                s = genre_share.get((corp, rule, genre), shares.get((corp, rule)))
                total += n * (s or 0.0)
        if w:
            lines.append(f"| {corp} | {genre} | {w} | {total:.0f} | {1000 * total / w:.2f} |")
    lines += ["", "## Information source among items coded evidential", "",
              "| Corpus | Rule | " + " | ".join(("inference-from-result", "inference-from-reasoning", "reported",
                                                "mirative-surprise", "other")) + " |", "|---|---|---|---|---|---|---|"]
    for (corp, rule), its in sorted(by_rule.items()):
        c = Counter(i["info_source"] for i in its if i["_code"] == "yes")
        lines.append(f"| {corp} | `{rule}` | " + " | ".join(str(c[k]) for k in (
            "inference-from-result", "inference-from-reasoning", "reported", "mirative-surprise", "other")) + " |")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
