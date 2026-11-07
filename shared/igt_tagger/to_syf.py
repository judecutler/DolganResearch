"""Write tagger/reviewed labels back as INEL-style SyF tags, so every existing study script
(extract_objects.py, russian_shift.py, clause_dom.py ...) runs unchanged on the larger corpus.

    python3 shared/igt_tagger/to_syf.py data/derived/dolgan REVIEW_DIR data/derived/dolgan_expanded

REVIEW_DIR holds predictions.csv and, once the review is merged, final_roles.csv. Words with
a reviewed label use it; others use the model's label. Words still marked "?" (disputed or
unsure) get no role. New columns:
- tokens.csv: syf_source = inel | human | model | none;
- texts.csv: syf_source = inel | tagger.
Every analysis on the expanded corpus must report results with and without the
tagger-labelled texts, and with the source as a control.

Tags written: S/O on pronouns (ps pers, dempro, emphpro, indfpro, posspr, que) as pro:S /
pro:O, otherwise np:S / np:O; predicates with P(pred) >= 0.5 as v:pred (verbs and
auxiliaries), cop (copulas) or n:pred (other); zero subjects as 0.N:S before the predicate
tag. Animacy (.h) is not predicted, so it is never written.
"""
import csv
import os
import shutil
import sys

PRO = {"pers", "dempro", "emphpro", "indfpro", "posspr", "que"}
HUMAN_SOURCES = {"agreed", "coder", "resolved"}


def _read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write(path, rows, cols):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def syf_tag(ps, role, p_pred, zero):
    items = []
    if p_pred >= 0.5:
        if zero in ("0.1", "0.2", "0.3"):
            items.append(zero + ":S")
        items.append("v:pred" if ps in ("v", "aux") else "cop" if ps == "cop" else "n:pred")
    if role in ("S", "O"):
        items.append(("pro:" if ps in PRO else "np:") + role)
    return " ".join(items)


def expand(derived, review_dir, out):
    os.makedirs(out, exist_ok=True)
    pred = {(r["utt_id"], r["idx"]): r for r in _read(os.path.join(review_dir, "predictions.csv"))}
    final = {}
    fp = os.path.join(review_dir, "final_roles.csv")
    if os.path.exists(fp):
        final = {(r["utt_id"], r["idx"]): r for r in _read(fp)}
    tokens = _read(os.path.join(derived, "tokens.csv"))
    n = {"inel": 0, "human": 0, "model": 0, "none": 0}
    for t in tokens:
        k = (t["utt_id"], t["idx"])
        if k not in pred:
            t["syf_source"] = "inel" if t.get("SyF") else "none"
        else:
            p = pred[k]
            role, src = p["role"], "model"
            if k in final and final[k]["source"] in HUMAN_SOURCES:
                role, src = final[k]["role"], "human"
            elif k in final and final[k]["role"] == "?":
                role, src = "-", "none"
            t["SyF"] = syf_tag(t.get("ps", ""), role, float(p["p_pred"]), p["zero"])
            t["syf_source"] = src
        n[t["syf_source"]] += 1
    _write(os.path.join(out, "tokens.csv"), tokens, list(tokens[0].keys()))
    texts = _read(os.path.join(derived, "texts.csv"))
    tagged = {p[0].split("#")[0] for p in pred}
    for t in texts:
        t["syf_source"] = "inel" if t.get("has_SyF") == "1" else ("tagger" if t["text_id"] in tagged else "none")
        if t["syf_source"] == "tagger":
            t["has_SyF"] = "1"
    _write(os.path.join(out, "texts.csv"), texts, list(texts[0].keys()))
    for name in ("speakers.csv", "utterances.csv", "morphemes.csv", "counts.json"):
        src = os.path.join(derived, name)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(out, name))
    return n


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    print(expand(*sys.argv[1:]))
