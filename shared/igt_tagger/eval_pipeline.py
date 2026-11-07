"""End-to-end check: tag held-out texts from their transcription alone (automatic glosses),
and compare with tagging from INEL's hand glosses.

    python3 shared/igt_tagger/eval_pipeline.py data/derived/dolgan dolgan OUT.json

The held-out texts are data.holdout_texts (the same 20% as train_eval.py). The glosser is
trained on every other text of the language; the tagger on the other tagged texts.
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import holdout_texts, load, subset  # noqa: E402
from features import utterance_features  # noqa: E402
from glosser import Glosser, train_ps_model  # noqa: E402
from igt import case_of, parse_gloss  # noqa: E402
from model import Tagger  # noqa: E402
from train_eval import POS, f1s, hard  # noqa: E402


def _auto(d, by, glosser, keep):
    """{word index: (features, case, ps)} from automatic glosses, for utterances of texts in keep."""
    out = {}
    i = 0
    while i < len(d["X"]):
        u = d["utt_id"][i]
        j = i
        while j < len(d["X"]) and d["utt_id"][j] == u:
            j += 1
        if d["text"][i] in keep:
            toks = [by[(u, d["idx"][k])] for k in range(i, j)]
            auto = [{"ps": ps, "ge": ge} for (_, ge, ps, _) in glosser.gloss([t["tx"] for t in toks])]
            for k, x, a in zip(range(i, j), utterance_features(auto), auto):
                out[k] = (x, case_of(parse_gloss(a["ge"])["tags"]) or "none", a["ps"])
        i = j
    return out


def main(derived, language, out_json, C=0.3):
    d = load(derived, language)
    ho = holdout_texts(d["text"])
    dev = subset(d, [i for i, t in enumerate(d["text"]) if t not in ho])
    test = subset(d, [i for i, t in enumerate(d["text"]) if t in ho])
    tagger = Tagger.train(dev, {t: C for t in ("pred", "sub", "role", "zero")})
    with open(os.path.join(derived, "tokens.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    train_rows = [r for r in rows if r["text_id"] not in ho]
    g = Glosser(ps_model=train_ps_model(train_rows) if "--ps-model" in sys.argv else None).train(train_rows)
    by = {(r["utt_id"], r["idx"]): r for r in rows}
    # Rebuild the test set's features from automatic glosses, utterance by utterance
    auto_X, auto_case, auto_ps = [], [], []
    i = 0
    while i < len(test["X"]):
        u = test["utt_id"][i]
        j = i
        while j < len(test["X"]) and test["utt_id"][j] == u:
            j += 1
        toks = [by[(u, test["idx"][k])] for k in range(i, j)]
        gl = g.gloss([t["tx"] for t in toks])
        auto = [{"ps": ps, "ge": ge} for (_, ge, ps, _) in gl]
        auto_X += utterance_features(auto)
        auto_case += [case_of(parse_gloss(a["ge"])["tags"]) or "none" for a in auto]
        auto_ps += [a["ps"] for a in auto]
        i = j
    hand = tagger.predict(test)
    # Train-test match: a second tagger trained on *automatic* glosses of the dev texts
    # (jackknifed: each dev text glossed by a glosser that never saw it)
    dev_texts = sorted(set(dev["text"]))
    folds = [set(dev_texts[k::5]) for k in range(5)]
    jk = {}
    for fold in folds:
        gk = Glosser().train([r for r in rows if r["text_id"] not in ho and r["text_id"] not in fold])
        jk.update(_auto(dev, by, gk, keep=fold))
    order = list(range(len(dev["X"])))
    dev_auto = dict(dev, X=[jk[k][0] for k in order], case=[jk[k][1] for k in order], ps=[jk[k][2] for k in order])
    tagger_auto = Tagger.train(dev_auto, {t: C for t in ("pred", "sub", "role", "zero")})
    auto_d = dict(test, X=auto_X, case=auto_case, ps=auto_ps)
    auto_out = tagger.predict(auto_d)
    res = {}
    auto_out2 = tagger_auto.predict(auto_d)
    for name, o in (("hand glosses", hand), ("automatic glosses", auto_out),
                    ("automatic glosses, tagger trained on automatic glosses", auto_out2)):
        res[name] = {t: f1s(test[t], hard(o, t), POS[t]) for t in ("role", "pred", "zero")}
        pred = hard(o, "role")
        nomo = [k for k in range(len(pred)) if test["role"][k] == "O" and test["case"][k] == "NOM"]
        res[name]["NOM_O_found"] = (sum(pred[k] == "O" for k in nomo), len(nomo))
    res["gloss_case_agreement"] = sum(a == b for a, b in zip(auto_case, test["case"])) / len(auto_case)
    res["gloss_ps_agreement"] = sum(a == b for a, b in zip(auto_ps, test["ps"])) / len(auto_ps)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    for k in ("hand glosses", "automatic glosses", "automatic glosses, tagger trained on automatic glosses"):
        r = res[k]
        print(f"{k}: role macro-F1 {r['role']['macro_f1']:.3f} (S {r['role']['S']['f1']:.3f}, O {r['role']['O']['f1']:.3f}), "
              f"pred {r['pred']['macro_f1']:.3f}, zero {r['zero']['macro_f1']:.3f}, unmarked O found {r['NOM_O_found']}")
    print("case agreement auto vs hand:", round(res["gloss_case_agreement"], 3), "ps:", round(res["gloss_ps_agreement"], 3))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 3:
        sys.exit(__doc__)
    main(*args)
