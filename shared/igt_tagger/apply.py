"""Apply a trained tagger to untagged texts and build the human review queue.

Standard library only, so it runs on any computer with Python 3:

    python3 shared/igt_tagger/apply.py MODEL.json data/derived/dolgan OUT_DIR [--threshold 0.9]

Writes the queue to OUT_DIR and everything coders must not see to OUT_DIR_key (keep both
under data/derived/, never commit them):
- predictions.csv  every word of every untagged text with the predicted predicate,
                   role and zero-subject probabilities;
- queue.csv        one row per utterance that needs a human, with the words, glosses,
                   translation, the model's suggestion for every word, and which words are
                   flagged. No speaker, birth year, recording year or text name
                   (blind coding, as in the Study A sheets);
- key.csv          item id -> utterance id, text, speaker (for merging; not for coders).

A word is flagged when the model is unsure (top probability below --threshold) or when it
is an unmarked (nominative) nominal with P(O) of at least --nom-object-floor. The second
rule exists because unmarked objects are what the model misses most, and missing them
more for some speakers than others would bias any case-marking analysis.
"""
import argparse
import csv
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import load  # noqa: E402
from igt import NOMINAL_PS  # noqa: E402
from model import Tagger  # noqa: E402
from profiles import augment, profile_for  # noqa: E402


def _read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def item_id(utt_id, salt):
    return hashlib.sha1((salt + utt_id).encode("utf-8")).hexdigest()[:10]


def flag_words(d, out, threshold, nom_floor):
    flags = []
    for i in range(len(d["X"])):
        role = out["role"][i]
        top = max(role.values())
        nominal = d["ps"][i] in NOMINAL_PS
        f = nominal and (top < threshold or (d["case"][i] == "NOM" and role.get("O", 0) >= nom_floor))
        flags.append(bool(f))
    return flags


def build(model_path, derived_dir, out_dir, language, threshold, nom_floor, overlap, salt):
    tagger = Tagger.from_json(model_path)
    d = load(derived_dir, language, tagged=False)
    if tagger.meta.get("augment"):
        d["X"] = augment(d["X"], language, profile_for(language))
    out = tagger.predict(d)
    flags = flag_words(d, out, threshold, nom_floor)
    os.makedirs(out_dir, exist_ok=True)
    toks = {(r["utt_id"], r["idx"]): r for r in _read(os.path.join(derived_dir, "tokens.csv"))}
    utts = {u["utt_id"]: u for u in _read(os.path.join(derived_dir, "utterances.csv"))}
    os.makedirs(out_dir + "_key", exist_ok=True)
    with open(os.path.join(out_dir + "_key", "predictions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["utt_id", "idx", "text_id", "speaker_id", "ps", "case", "p_pred", "p_S", "p_O",
                    "p_none", "role", "zero", "flagged"])
        for i in range(len(d["X"])):
            r = out["role"][i]
            z = out["zero"][i]
            w.writerow([d["utt_id"][i], d["idx"][i], d["text"][i], d["speaker"][i], d["ps"][i], d["case"][i],
                        f"{out['pred'][i]:.3f}", f"{r.get('S', 0):.3f}", f"{r.get('O', 0):.3f}",
                        f"{r.get('-', 0):.3f}", max(r, key=r.get), max(z, key=z.get), int(flags[i])])
    by_utt = {}
    for i, u in enumerate(d["utt_id"]):
        by_utt.setdefault(u, []).append(i)
    queue, key = [], []
    for u, ii in by_utt.items():
        if not any(flags[i] for i in ii):
            continue
        words = []
        for i in ii:
            t = toks[(u, d["idx"][i])]
            r = out["role"][i]
            words.append({"tx": t["tx"], "ge": t["ge"], "ps": t["ps"], "case": d["case"][i],
                          "pred": round(out["pred"][i], 2), "S": round(r.get("S", 0), 2),
                          "O": round(r.get("O", 0), 2), "flag": flags[i],
                          "suggest": max(r, key=r.get)})
        iid = item_id(u, salt)
        queue.append({"item": iid, "translation": utts.get(u, {}).get("fe", ""), "words": json.dumps(words, ensure_ascii=False),
                      "n_flagged": sum(w_["flag"] for w_ in words)})
        key.append({"item": iid, "utt_id": u, "text_id": d["text"][ii[0]], "speaker_id": d["speaker"][ii[0]]})
    # Batch 1 first: narrative and conversation from speakers with a usable birth year (the
    # texts that let generations be compared within one genre, see Study D). Inside a batch,
    # hash order interleaves texts and speakers, so coders never see a text in sequence.
    texts = {t["text_id"]: t for t in _read(os.path.join(derived_dir, "texts.csv"))}
    speakers = {s["speaker_id"]: s for s in _read(os.path.join(derived_dir, "speakers.csv"))}

    def batch(k):
        t, s = texts.get(k["text_id"], {}), speakers.get(k["speaker_id"], {})
        dated = s.get("birth_lo") and s.get("birth_hi") and float(s["birth_hi"]) - float(s["birth_lo"]) <= 10
        return 1 if dated and t.get("genre") in ("nar", "conv") else 2
    batch_of = {k["item"]: batch(k) for k in key}
    for q in queue:
        q["batch"] = batch_of[q["item"]]
    queue.sort(key=lambda q: (q["batch"], q["item"]))
    n_overlap = int(round(overlap * len(queue)))
    step = max(1, int(round(1 / overlap))) if overlap else 0
    for k, q in enumerate(queue):
        # overlap items spread evenly through the queue, so kappa covers both batches
        q["coder"] = "both" if step and k % step == 0 else ("A" if k % 2 else "B")
    os.makedirs(out_dir + "_key", exist_ok=True)
    for name, rows, cols in (("queue.csv", queue, ["item", "batch", "coder", "n_flagged", "translation", "words"]),
                             ("key.csv", key, ["item", "utt_id", "text_id", "speaker_id"])):
        folder = out_dir if name == "queue.csv" else out_dir + "_key"
        with open(os.path.join(folder, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    return {"words": len(d["X"]), "flagged_words": sum(flags), "utterances": len(by_utt), "queue": len(queue),
            "overlap_items": sum(q["coder"] == "both" for q in queue),
            "batch1_items": sum(q["batch"] == 1 for q in queue),
            "batch1_flagged_words": sum(q["n_flagged"] for q in queue if q["batch"] == 1)}


def build_calibration(derived_dir, out_dir, language, text_ids, salt="calibration-1"):
    """A queue from texts INEL already tagged: every nominal flagged, no model suggestions,
    both coders do every item. Merging it against INEL's tags gives each coder's agreement
    with the original annotators (merge_review.py, then compare final_roles with INEL)."""
    d = load(derived_dir, language, tagged=True)
    keep = set(text_ids)
    ii = [i for i, t in enumerate(d["text"]) if t in keep]
    toks = {(r["utt_id"], r["idx"]): r for r in _read(os.path.join(derived_dir, "tokens.csv"))}
    utts = {u["utt_id"]: u for u in _read(os.path.join(derived_dir, "utterances.csv"))}
    by_utt = {}
    for i in ii:
        by_utt.setdefault(d["utt_id"][i], []).append(i)
    queue, key, gold = [], [], []
    for u, idx in by_utt.items():
        words = []
        for k, i in enumerate(idx):
            t = toks[(u, d["idx"][i])]
            flag = d["ps"][i] in NOMINAL_PS
            words.append({"tx": t["tx"], "ge": t["ge"], "ps": t["ps"], "case": d["case"][i], "pred": "",
                          "S": "", "O": "", "flag": flag, "suggest": ""})
            gold.append({"item": item_id(u, salt), "word": k, "inel_role": d["role"][i]})
        if not any(w["flag"] for w in words):
            continue
        iid = item_id(u, salt)
        queue.append({"item": iid, "coder": "both", "n_flagged": sum(w["flag"] for w in words),
                      "translation": utts.get(u, {}).get("fe", ""), "words": json.dumps(words, ensure_ascii=False)})
        key.append({"item": iid, "utt_id": u, "text_id": d["text"][idx[0]], "speaker_id": d["speaker"][idx[0]]})
    queue.sort(key=lambda q: q["item"])
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(out_dir + "_key", exist_ok=True)
    for name, rows, cols in (("queue.csv", queue, ["item", "coder", "n_flagged", "translation", "words"]),
                             ("key.csv", key, ["item", "utt_id", "text_id", "speaker_id"]),
                             ("inel_gold.csv", gold, ["item", "word", "inel_role"])):
        folder = out_dir if name == "queue.csv" else out_dir + "_key"
        with open(os.path.join(folder, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    return {"items": len(queue), "words_to_code": sum(q["n_flagged"] for q in queue)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model")
    ap.add_argument("derived")
    ap.add_argument("out_dir")
    ap.add_argument("--language", default="dolgan")
    ap.add_argument("--threshold", type=float, default=0.9)
    ap.add_argument("--nom-object-floor", type=float, default=0.05)
    ap.add_argument("--overlap", type=float, default=0.1, help="share of items both coders do (for kappa)")
    ap.add_argument("--salt", default="dolgan-review-1")
    a = ap.parse_args(argv)
    print(build(a.model, a.derived, a.out_dir, a.language, a.threshold, a.nom_object_floor, a.overlap, a.salt))


if __name__ == "__main__":
    main()
