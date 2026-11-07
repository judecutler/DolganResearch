"""Turn INEL derived tables (tokens.csv, texts.csv, speakers.csv) into tagger examples."""
import csv
import os

from features import utterance_features
from valency import estimate as valency_estimate
from igt import case_of, group_utterances, labels, parse_gloss

TASKS = ("role", "pred", "zero", "sub")
BINS = ((None, 1920, "-1919"), (1920, 1940, "1920-1939"), (1940, 1960, "1940-1959"), (1960, None, "1960-"))


def _read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _birth_bin(sp):
    lo, hi = sp.get("birth_lo"), sp.get("birth_hi")
    if not lo or not hi or float(hi) - float(lo) > 10:
        return "unknown"
    y = (float(lo) + float(hi)) / 2
    for a, b, name in BINS:
        if (a is None or y >= a) and (b is None or y < b):
            return name
    return "unknown"


def load(derived_dir, language, feature_set="full", tagged=True, lang_feature=False, use_valency=False):
    """Examples from texts with (tagged=True) or without (tagged=False) SyF annotation.

    Returns dict of parallel lists: X (feature dicts), role, pred, zero, text, speaker, bin,
    case, ps, utt_id, idx.
    """
    texts = {t["text_id"]: t for t in _read(os.path.join(derived_dir, "texts.csv"))}
    speakers = {s["speaker_id"]: s for s in _read(os.path.join(derived_dir, "speakers.csv"))}
    all_rows = _read(os.path.join(derived_dir, "tokens.csv"))
    val = valency_estimate(all_rows) if use_valency else None
    rows = [r for r in all_rows if (texts.get(r["text_id"], {}).get("has_SyF") == "1") == tagged]
    out = {k: [] for k in ("X", "role", "pred", "zero", "sub", "text", "speaker", "bin", "case", "ps", "utt_id", "idx")}
    for utt, toks in group_utterances(rows):
        feats = utterance_features(toks, feature_set, language if lang_feature else None, val)
        for r, f in zip(toks, feats):
            role, pred, zero = labels(r.get("SyF", ""))
            out["X"].append(f)
            out["role"].append(role)
            out["pred"].append(pred)
            out["zero"].append(zero)
            span = (r.get("SyF", "") + " " + r.get("SyF_cover", "")).split()
            out["sub"].append("sub" if any(x.startswith("s:") for x in span) else "-")
            out["text"].append(r["text_id"])
            out["speaker"].append(r["speaker_id"])
            out["bin"].append(_birth_bin(speakers.get(r["speaker_id"], {})))
            out["case"].append(case_of(parse_gloss(r.get("ge", ""))["tags"]) or "none")
            out["ps"].append(r.get("ps", ""))
            out["utt_id"].append(utt)
            out["idx"].append(r.get("idx", ""))
    return out


def holdout_texts(texts, share=0.2, seed=20261107):
    """A fixed set of texts kept out of all development, for the final test only."""
    import random
    t = sorted(set(texts))
    random.Random(seed).shuffle(t)
    return set(t[:max(1, int(round(share * len(t))))])


def subset(d, keep):
    """Rows of d whose index is in keep (a list of indices)."""
    return {k: [v[i] for i in keep] for k, v in d.items()}
