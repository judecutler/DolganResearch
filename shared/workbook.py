"""Study A: build annotation workbooks from evidential candidates, and merge them back.

Build (pilot: the same items for both annotators; main: 15% hidden overlap):
    python3 shared/workbook.py build pilot  OUT_DIR CANDIDATES.csv [CANDIDATES.csv ...] --n 40
    python3 shared/workbook.py build main   OUT_DIR CANDIDATES.csv [...] --per-rule 60 --exclude OUT_DIR/pilot_key.csv

Study B1 vetting sheets use the same builder with another codebook:
    python3 shared/workbook.py build pilot OUT_DIR b1_candidates.csv --n 1000 --prefix b1 \
        --codebook shared/config/b1_codebook.json

Merge (validates every value against the codebook, then computes agreement):
    python3 shared/workbook.py merge OUT_DIR/main_key.csv SHEET_A.xlsx SHEET_B.xlsx OUT_PREFIX

Sampling (D-020): every tier-1 candidate is kept; tier-2 candidates are sampled per
rule, spread across speakers by round robin, with a fixed seed so the sheet is
reproducible. Items are shuffled so rule and speaker order give nothing away. The
rule that found an item, the speaker, birth year and recording year are kept in the
key, not the sheet, so they do not steer coding (D-039).
"""
import argparse
import csv
import json
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inel import xlsx  # noqa: E402
from inel.load import write  # noqa: E402

SEED = 20261105
CODEBOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "evid_codebook.json")
# Coders see no speaker, birth year or recording year: Studies A and B1 compare those later,
# so coding blind to them keeps the codes from leaning toward an expected trend (D-039).
CONTEXT = ("item_id", "corpus", "genre", "source_collection", "word", "sentence", "glosses", "translation")
KEY = ("item_id", "token_id", "utt_id", "text_id", "corpus", "speaker_id", "birth_year", "recording_year",
       "tier", "rules", "sheet", "overlap")


def codebook(path=CODEBOOK):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r.setdefault("tier", "1")
    return rows


def round_robin(groups, k, rng):
    """Up to k items, taking one from each group in turn (groups shuffled, items shuffled)."""
    queues = [rng.sample(v, len(v)) for _, v in sorted(groups.items())]
    rng.shuffle(queues)
    picked = []
    while len(picked) < k and any(queues):
        for q in queues:
            if q and len(picked) < k:
                picked.append(q.pop())
    return picked


def _group(items, key):
    g = {}
    for c in items:
        g.setdefault(key(c), []).append(c)
    return g


def sample(cands, per_rule, rng):
    """All tier-1 items, plus up to per_rule tier-2 items for each first rule, spread over speakers."""
    keep = [c for c in cands if c["tier"] == "1"]
    by_rule = _group([c for c in cands if c["tier"] == "2"], lambda c: c["rules"].split()[0])
    for rule in sorted(by_rule):
        keep += round_robin(_group(by_rule[rule], lambda c: c["speaker_id"]), per_rule, rng)
    return keep


def pilot_sample(cands, n, rng):
    """Half tier 1 and half tier 2 where possible, each spread over rules.

    Tier 2 outnumbers tier 1 about 40 to 1 in Dolgan, so a plain random sample would
    pilot the codebook on almost no glossed evidentials.
    """
    t1 = [c for c in cands if c["tier"] == "1"]
    t2 = [c for c in cands if c["tier"] == "2"]
    n2 = min(len(t2), n - min(len(t1), n // 2))
    n1 = min(len(t1), n - n2)
    rule = lambda c: c["rules"].split()[0]  # noqa: E731
    return round_robin(_group(t1, rule), n1, rng) + round_robin(_group(t2, rule), n2, rng)


def _year(lo, hi):
    if not lo:
        return ""
    return lo if lo == hi else f"{lo}-{hi}"


def sheet_row(item_id, c):
    return {
        "item_id": item_id, "corpus": c["corpus"], "genre": c["genre"],
        "source_collection": c["source_collection"], "word": c["tx"],
        "sentence": c["context"], "glosses": c["gloss_line"], "translation": c["fe"],
    }


def build(mode, out, cand_paths, n=40, per_rule=60, overlap=0.15, exclude=None, codebook_path=CODEBOOK, prefix=None):
    rng = random.Random(SEED)
    cands = [c for p in cand_paths for c in read_csv(p)]
    skip = {r["token_id"] for r in read_csv(exclude)} if exclude else set()
    cands = [c for c in cands if c["token_id"] not in skip]
    if mode == "pilot":
        items = pilot_sample(cands, n, rng)
    else:
        items = sample(cands, per_rule, rng)
    rng.shuffle(items)

    book = codebook(codebook_path)
    prefix = prefix or mode
    coding = list(book["columns"]) + list(book["free_text"])
    header = list(CONTEXT) + coding
    widths = {"sentence": 60, "glosses": 60, "translation": 50, "note": 40, "word": 16}

    key, sheets = [], {"A": [], "B": []}
    n_overlap = len(items) if mode == "pilot" else round(len(items) * overlap)
    double = set(rng.sample(range(len(items)), n_overlap))
    single = [i for i in range(len(items)) if i not in double]
    to_a = set(single[::2])
    for i, c in enumerate(items):
        item_id = f"{mode[0].upper()}{i + 1:04d}"
        both = i in double
        who = ("A", "B") if both else (("A",) if i in to_a else ("B",))
        for s in who:
            sheets[s].append(sheet_row(item_id, c))
        key.append({"item_id": item_id, "token_id": c["token_id"], "utt_id": c["utt_id"],
                    "text_id": c["text_id"], "corpus": c["corpus"], "speaker_id": c["speaker_id"],
                    "birth_year": c["birth_mid"].replace(".0", "") if c.get("birth_mid") else "",
                    "recording_year": _year(c["recording_lo"], c["recording_hi"]), "tier": c["tier"],
                    "rules": c["rules"], "sheet": "".join(who), "overlap": int(both)})
    os.makedirs(out, exist_ok=True)
    for s, rows in sheets.items():
        rows.sort(key=lambda r: r["item_id"])
        xlsx.write(os.path.join(out, f"{prefix}_sheet_{s}.xlsx"), header, rows,
                   dropdowns=book["columns"], editable=coding, widths=widths)
    write(os.path.join(out, f"{prefix}_key.csv"), KEY, key)
    return key


def kappa(pairs):
    """Cohen's kappa for a list of (a, b) labels. None if undefined."""
    if not pairs:
        return None
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def merge(key_path, a_path, b_path, out_prefix, codebook_path=CODEBOOK):
    book = codebook(codebook_path)
    key = {r["item_id"]: r for r in read_csv(key_path)}
    errors, coded = [], {}
    for who, path in (("A", a_path), ("B", b_path)):
        rows = xlsx.read(path)
        seen = set()
        for r in rows:
            iid = r.get("item_id", "")
            if iid not in key or who not in key[iid]["sheet"]:
                errors.append(f"{who}: unknown or misplaced item_id {iid!r}")
                continue
            seen.add(iid)
            for col, allowed in book["columns"].items():
                v = (r.get(col) or "").strip()
                if v and v not in allowed:
                    errors.append(f"{who} {iid}: {col}={v!r} is not in the codebook")
            coded[(who, iid)] = r
        missing = {i for i, k in key.items() if who in k["sheet"]} - seen
        errors += [f"{who}: item {i} missing from the sheet" for i in sorted(missing)]
        first = next(iter(book["columns"]))
        uncoded = sorted(i for i in seen if not (coded[(who, i)].get(first) or "").strip())
        if uncoded:
            errors.append(f"{who}: {len(uncoded)} items have no `{first}` yet (first: {uncoded[0]})")

    cols = list(book["columns"]) + list(book["free_text"])
    merged = []
    for iid, k in key.items():
        row = dict(k)
        for who in ("A", "B"):
            r = coded.get((who, iid), {})
            for c in cols:
                row[f"{c}_{who}"] = (r.get(c) or "").strip()
        merged.append(row)
    write(out_prefix + "_merged.csv", list(KEY) + [f"{c}_{w}" for w in "AB" for c in cols], merged)

    lines = ["# Annotation agreement", "", f"Key: `{os.path.basename(key_path)}`. Items: {len(key)}. "
             f"Double-coded: {sum(1 for k in key.values() if k['overlap'] == '1')}.", ""]
    if errors:
        lines += ["## Problems (fix the sheets and merge again)", ""] + [f"- {e}" for e in errors] + [""]
    lines += ["## Cohen's kappa on double-coded items", "",
              "| Column | Items coded by both | Raw agreement | Kappa |", "|---|---|---|---|"]
    for c in book["columns"]:
        pairs = [(m[f"{c}_A"], m[f"{c}_B"]) for m in merged
                 if m["overlap"] == "1" and m[f"{c}_A"] and m[f"{c}_B"]]
        k = kappa(pairs)
        raw = sum(a == b for a, b in pairs) / len(pairs) if pairs else None
        lines.append(f"| `{c}` | {len(pairs)} | {'' if raw is None else f'{raw:.2f}'} | "
                     f"{('no items' if not pairs else 'undefined') if k is None else f'{k:.2f}'} |")
    lines += ["", "Kappa is undefined when both annotators used one value only. A low kappa means the "
              "codebook needs work, not the annotators (evidentiality/PLAN.md)."]
    with open(out_prefix + "_agreement.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return errors


def main(argv):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("mode", choices=("pilot", "main"))
    b.add_argument("out")
    b.add_argument("candidates", nargs="+")
    b.add_argument("--n", type=int, default=40)
    b.add_argument("--per-rule", type=int, default=60)
    b.add_argument("--exclude")
    b.add_argument("--codebook", default=CODEBOOK)
    b.add_argument("--prefix")
    m = sub.add_parser("merge")
    m.add_argument("key")
    m.add_argument("sheet_a")
    m.add_argument("sheet_b")
    m.add_argument("out_prefix")
    m.add_argument("--codebook", default=CODEBOOK)
    a = p.parse_args(argv)
    if a.cmd == "build":
        key = build(a.mode, a.out, a.candidates, a.n, a.per_rule, exclude=a.exclude,
                    codebook_path=a.codebook, prefix=a.prefix)
        print(len(key), "items;", sum(int(k["overlap"]) for k in key), "double-coded")
    else:
        errors = merge(a.key, a.sheet_a, a.sheet_b, a.out_prefix, a.codebook)
        print(f"{len(errors)} problems; see {a.out_prefix}_agreement.md")
        return 1 if errors else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
