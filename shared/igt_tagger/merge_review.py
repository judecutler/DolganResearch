"""Merge the coders' review exports with the model's predictions.

    python3 shared/igt_tagger/merge_review.py REVIEW_DIR review_A.csv review_B.csv

REVIEW_DIR is the folder apply.py wrote (predictions.csv, queue.csv, key.csv). Writes there:
- final_roles.csv   every word: utt_id, idx, role (S/O/-), source (model, coder, agreed,
                    disputed, unsure), plus the coders' labels;
- agreement.md      Cohen's kappa between the coders on the words both decided, agreement
                    of each coder with the model, and counts of disputed and unsure words.

Disputed and unsure words keep role "?" until resolved: add a file resolved.csv
(item, word, label) to REVIEW_DIR after discussing them and run this again.
"""
import csv
import json
import os
import sys
from collections import Counter

MAP = {"S": "S", "O": "O", "N": "-", "U": "?"}


def _read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def kappa(pairs):
    """Cohen's kappa for a list of (label_a, label_b)."""
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def merge(review_dir, exports):
    key = {r["item"]: r for r in _read(os.path.join(review_dir, "key.csv"))}
    queue = {r["item"]: json.loads(r["words"]) for r in _read(os.path.join(review_dir, "queue.csv"))}
    resolved = {}
    rp = os.path.join(review_dir, "resolved.csv")
    if os.path.exists(rp):
        resolved = {(r["item"], int(r["word"])): MAP.get(r["label"], r["label"]) for r in _read(rp)}
    decisions = {}  # (item, word) -> {coder: label}
    for path in exports:
        for r in _read(path):
            decisions.setdefault((r["item"], int(r["word"])), {})[r["coder"]] = MAP[r["label"]]
    utt_item = {v["utt_id"]: k for k, v in key.items()}
    pairs, vs_model, counts, out = [], {}, Counter(), []
    pos = Counter()  # word position inside a queue item = order of the utterance's words
    for p in _read(os.path.join(review_dir, "predictions.csv")):
        item = utt_item.get(p["utt_id"])
        role, source, labs = p["role"], "model", {}
        if item is not None:
            w = pos[item]
            pos[item] += 1
            labs = decisions.get((item, w), {})
            flagged = queue[item][w]["flag"] if w < len(queue[item]) else False
            vals = set(labs.values())
            if (item, w) in resolved:
                role, source = resolved[(item, w)], "resolved"
            elif len(labs) >= 2 and len(vals) == 1 and "?" not in vals:
                role, source = next(iter(vals)), "agreed"
            elif len(labs) >= 2:
                role, source = "?", "disputed"
            elif len(labs) == 1:
                v = next(iter(vals))
                role, source = (v, "coder") if v != "?" else ("?", "unsure")
            if flagged and "A" in labs and "B" in labs:
                pairs.append((labs["A"], labs["B"]))
            if flagged:
                for c, v in labs.items():
                    vs_model.setdefault(c, []).append((v, p["role"]))
        counts[source] += 1
        out.append({"utt_id": p["utt_id"], "idx": p["idx"], "role": role, "source": source,
                    "model_role": p["role"], "coder_A": labs.get("A", ""), "coder_B": labs.get("B", "")})
    with open(os.path.join(review_dir, "final_roles.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    k = kappa(pairs)
    lines = ["# Review agreement", "",
             f"- Words decided by both coders (flagged words in overlap items): {len(pairs)}",
             f"- Cohen's kappa between coders: {'n/a' if k is None else f'{k:.3f}'}",
             f"- Raw agreement: {'n/a' if not pairs else f'{sum(a == b for a, b in pairs) / len(pairs):.1%}'}"]
    for c, pr in sorted(vs_model.items()):
        lines.append(f"- Coder {c} agrees with the model on {sum(a == b for a, b in pr) / len(pr):.1%} of "
                     f"{len(pr)} flagged words (kappa {kappa(pr):.3f})")
    lines += ["", "| Source of final label | Words |", "|---|---|"] + [f"| {s} | {n} |" for s, n in counts.most_common()]
    with open(os.path.join(review_dir, "agreement.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return counts, k


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    print(merge(sys.argv[1], sys.argv[2:]))
