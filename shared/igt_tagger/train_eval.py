"""Train and evaluate the two-stage argument tagger (needs scikit-learn and numpy).

    python3 shared/igt_tagger/train_eval.py DERIVED_DIR OUT.json [--models MODEL_DIR]

DERIVED_DIR holds one folder per language (dolgan/, evenki/) with tokens.csv, texts.csv,
speakers.csv. Only numbers go into OUT.json: no corpus text.

Protocol:
- 20% of each language's tagged texts are a held-out test set (data.holdout_texts, fixed
  seed). They were not looked at during feature development; they are used once here.
- On the other 80% ("dev"): grouped 5-fold cross-validation by text, with the
  regularisation strength chosen inside each training fold (nested, 3-fold).
- Then a model trained on all dev texts is scored once on the held-out texts.
- Cross-language: a model trained on one language's dev texts, scored on the other's
  held-out texts, next to the in-language score on the same texts.
- Learning curve: models trained on 10/25/50/100% of dev texts (with and without the other
  language's data added), scored on held-out texts.
- Routing: for the review queue rule (flag a nominal if the top probability is below a
  threshold, or if it is unmarked and P(O) is at least a floor), the workload and the
  accuracy after a perfect human corrects every flagged word.
"""
import argparse
import json
import os
import random
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import holdout_texts, load, subset  # noqa: E402
from igt import NOMINAL_PS  # noqa: E402
from model import Tagger  # noqa: E402
from profiles import augment, estimate, profile_for  # noqa: E402

C_GRID = (0.1, 0.3, 1.0)
POS = {"role": ("S", "O"), "pred": ("pred",), "zero": ("0.1", "0.2", "0.3"), "sub": ("sub",)}
LANGS = ("dolgan", "evenki")
THRESHOLDS = (0.7, 0.8, 0.9, 0.95)
FLOORS = (None, 0.05, 0.1, 0.2)


def f1s(y, yhat, pos):
    out = {}
    for c in pos:
        tp = sum(1 for a, b in zip(y, yhat) if a == c and b == c)
        fp = sum(1 for a, b in zip(y, yhat) if a != c and b == c)
        fn = sum(1 for a, b in zip(y, yhat) if a == c and b != c)
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        out[c] = {"p": p, "r": r, "f1": 2 * p * r / (p + r) if p + r else 0.0, "n": tp + fn}
    out["macro_f1"] = sum(out[c]["f1"] for c in pos) / len(pos)
    return out


def hard(out, task):
    if task in ("pred", "sub"):
        return [task if p >= 0.5 else "-" for p in out[task]]
    return [max(p, key=p.get) for p in out[task]]


def score(d, out):
    return {t: f1s(d[t], hard(out, t), POS[t]) for t in POS}


def rule_role(d):
    """Case-only baseline: accusative/partitive nominal -> O; first unmarked nominal before a verb -> S."""
    res = []
    for i, x in enumerate(d["X"]):
        ps, case = d["ps"][i], d["case"][i]
        if ps in NOMINAL_PS and case in ("ACC", "PART"):
            res.append("O")
        elif ps in NOMINAL_PS and case == "NOM" and x.get("nom_rank=0") and not x.get("dright=none"):
            res.append("S")
        else:
            res.append("-")
    return res


def train(d, C, meta=None):
    return Tagger.train(d, {t: C for t in ("pred", "sub", "role", "zero")}, meta)


def choose_C(d):
    from sklearn.model_selection import GroupKFold
    best = (-1, C_GRID[0])
    for C in C_GRID:
        ys, ps = [], []
        for tr, te in GroupKFold(n_splits=3).split(d["X"], d["role"], d["text"]):
            m = train(subset(d, tr), C)
            ps += hard(m.predict(subset(d, te)), "role")
            ys += [d["role"][i] for i in te]
        s = f1s(ys, ps, POS["role"])["macro_f1"]
        best = max(best, (s, C))
    return best[1]


def nested_oof(d, log, name):
    from sklearn.model_selection import GroupKFold
    n = len(d["X"])
    out = {"pred": [0.0] * n, "sub": [0.0] * n, "role": [None] * n, "zero": [None] * n}
    chosen = []
    for k, (tr, te) in enumerate(GroupKFold(n_splits=5).split(d["X"], d["role"], d["text"])):
        dtr = subset(d, tr)
        C = choose_C(dtr)
        chosen.append(C)
        o = train(dtr, C).predict(subset(d, te))
        for t in out:
            for j, i in enumerate(te):
                out[t][i] = o[t][j]
        log(f"{name} outer fold {k + 1}/5, C={C}")
    return out, chosen


def flags(d, out, thr, floor):
    res = []
    for i in range(len(d["X"])):
        r = out["role"][i]
        nominal = d["ps"][i] in NOMINAL_PS
        f = nominal and (max(r.values()) < thr or (floor is not None and d["case"][i] == "NOM"
                                                  and r.get("O", 0) >= floor))
        res.append(f)
    return res


def routing(d, out):
    pred = hard(out, "role")
    utts = defaultdict(list)
    for i, u in enumerate(d["utt_id"]):
        utts[u].append(i)
    nominal = [i for i in range(len(pred)) if d["ps"][i] in NOMINAL_PS]
    nom_obj = [i for i in range(len(pred)) if d["role"][i] == "O" and d["case"][i] == "NOM"]
    rows = []
    for thr in THRESHOLDS:
        for floor in FLOORS:
            fl = flags(d, out, thr, floor)
            final = [d["role"][i] if fl[i] else pred[i] for i in range(len(pred))]
            sc = f1s(d["role"], final, POS["role"])
            rows.append({"threshold": thr, "floor": floor,
                         "flagged_words": sum(fl), "flagged_share_of_nominals": sum(fl) / len(nominal),
                         "utterances_to_review": sum(1 for ii in utts.values() if any(fl[i] for i in ii)),
                         "utterances_total": len(utts),
                         "S_f1": sc["S"]["f1"], "O_f1": sc["O"]["f1"], "O_p": sc["O"]["p"], "O_r": sc["O"]["r"],
                         "NOM_O_recall": sum(final[i] == "O" for i in nom_obj) / max(1, len(nom_obj)),
                         "auto_errors": sum(1 for i in range(len(pred)) if not fl[i] and pred[i] != d["role"][i])})
    return rows


def details(d, out):
    pred = hard(out, "role")
    by_case = defaultdict(lambda: [0, 0])
    for a, b, c in zip(d["role"], pred, d["case"]):
        if a == "O":
            k = c if c in ("ACC", "NOM", "PART") else "other"
            by_case[k][0] += b == "O"
            by_case[k][1] += 1
    by_bin = {}
    for b in sorted(set(d["bin"])):
        ii = [i for i in range(len(pred)) if d["bin"][i] == b]
        s = f1s([d["role"][i] for i in ii], [pred[i] for i in ii], POS["role"])
        nomo = [i for i in ii if d["role"][i] == "O" and d["case"][i] == "NOM"]
        s["NOM_O_found"], s["NOM_O_n"] = sum(pred[i] == "O" for i in nomo), len(nomo)
        s["speakers"] = len({d["speaker"][i] for i in ii})
        by_bin[b] = s
    # Calibration of P(O): predicted vs observed rate in probability bins (nominals only)
    cal = defaultdict(lambda: [0.0, 0, 0])
    for i in range(len(pred)):
        if d["ps"][i] in NOMINAL_PS:
            p = out["role"][i].get("O", 0)
            k = min(9, int(p * 10))
            cal[k][0] += p
            cal[k][1] += d["role"][i] == "O"
            cal[k][2] += 1
    calib = {f"{k / 10:.1f}": {"mean_p": v[0] / v[2], "observed": v[1] / v[2], "n": v[2]} for k, v in sorted(cal.items())}
    return {"O_recall_by_case": {k: {"found": v[0], "n": v[1]} for k, v in by_case.items()},
            "by_birth_bin": by_bin, "calibration_O": calib, "rule_baseline": f1s(d["role"], rule_role(d), POS["role"]),
            "majority": f1s(d["role"], ["-"] * len(pred), POS["role"])}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("derived")
    ap.add_argument("out")
    ap.add_argument("--models", help="folder to write the final trained models (JSON)")
    ap.add_argument("--skip-nested", action="store_true")
    a = ap.parse_args(argv)
    t0 = time.time()
    log = lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", flush=True)  # noqa: E731
    res = {"protocol": __doc__, "profiles": {}, "sizes": {}}
    dev, test = {}, {}
    for lang in LANGS:
        import csv as _csv
        with open(os.path.join(a.derived, lang, "tokens.csv"), encoding="utf-8") as f:
            res["profiles"][lang] = {"declared": profile_for(lang), "estimated": estimate(list(_csv.DictReader(f)))}
        d = load(os.path.join(a.derived, lang), lang)
        ho = holdout_texts(d["text"])
        dev[lang] = subset(d, [i for i, t in enumerate(d["text"]) if t not in ho])
        test[lang] = subset(d, [i for i, t in enumerate(d["text"]) if t in ho])
        res["sizes"][lang] = {s: {"texts": len(set(x["text"])), "words": len(x["X"]), "speakers": len(set(x["speaker"])),
                                  "S": x["role"].count("S"), "O": x["role"].count("O")}
                              for s, x in (("dev", dev[lang]), ("test", test[lang]))}
        log(f"{lang}: {res['sizes'][lang]}")
    final_C = {}
    for lang in LANGS:
        r = res[lang] = {}
        if not a.skip_nested:
            oof, chosen = nested_oof(dev[lang], log, lang)
            r["dev_cv"] = {"scores": score(dev[lang], oof), "C_chosen": chosen, **details(dev[lang], oof),
                           "routing": routing(dev[lang], oof)}
            final_C[lang] = Counter(chosen).most_common(1)[0][0]
        else:
            final_C[lang] = 0.3
        m = train(dev[lang], final_C[lang], {"language": lang, "trained_on": "dev texts"})
        o = m.predict(test[lang])
        r["test"] = {"scores": score(test[lang], o), **details(test[lang], o), "routing": routing(test[lang], o)}
        log(f"{lang} held-out role macro F1 {r['test']['scores']['role']['macro_f1']:.3f}")
    # Cross-language and pooled, all scored on the target's held-out texts
    res["transfer"] = {}
    for src, tgt in (("dolgan", "evenki"), ("evenki", "dolgan")):
        C = final_C[tgt]
        o = train(dev[src], C).predict(test[tgt])
        res["transfer"][f"{src} only -> {tgt}"] = score(test[tgt], o)
        both = {k: dev[tgt][k] + dev[src][k] for k in dev[tgt]}
        o = train(both, C).predict(test[tgt])
        res["transfer"][f"{tgt} + {src} plain -> {tgt}"] = score(test[tgt], o)
        aug = dict(both, X=augment(dev[tgt]["X"], tgt, profile_for(tgt)) + augment(dev[src]["X"], src, profile_for(src)))
        o = train(aug, C).predict(dict(test[tgt], X=augment(test[tgt]["X"], tgt, profile_for(tgt))))
        res["transfer"][f"{tgt} + {src} augmented -> {tgt}"] = score(test[tgt], o)
        log(f"transfer {src}->{tgt} done")
    # Learning curve on held-out texts
    res["curve"] = {}
    for lang in LANGS:
        other = "evenki" if lang == "dolgan" else "dolgan"
        texts = sorted(set(dev[lang]["text"]))
        for frac in (0.1, 0.25, 0.5, 1.0):
            reps = 3 if frac < 1.0 else 1
            for rep in range(reps):
                rng = random.Random(100 + rep)
                pick = set(rng.sample(texts, max(1, int(round(frac * len(texts))))))
                part = subset(dev[lang], [i for i, t in enumerate(dev[lang]["text"]) if t in pick])
                variants = {"alone": (part, test[lang])}
                if frac < 1.0:
                    variants["+other plain"] = ({k: part[k] + dev[other][k] for k in part}, test[lang])
                    variants["+other augmented"] = (
                        dict({k: part[k] + dev[other][k] for k in part},
                             X=augment(part["X"], lang, profile_for(lang)) + augment(dev[other]["X"], other, profile_for(other))),
                        dict(test[lang], X=augment(test[lang]["X"], lang, profile_for(lang))))
                for v, (tr, te) in variants.items():
                    o = train(tr, final_C[lang]).predict(te)
                    res["curve"].setdefault(f"{lang} {frac} {v}", []).append(
                        {"texts": len(pick), "role_macro_f1": f1s(te["role"], hard(o, "role"), POS["role"])["macro_f1"]})
            log(f"curve {lang} {frac} done")
    if a.models:
        os.makedirs(a.models, exist_ok=True)
        for lang in LANGS:
            full = {k: dev[lang][k] + test[lang][k] for k in dev[lang]}
            train(full, final_C[lang], {"language": lang, "trained_on": "all tagged texts",
                                        "C": final_C[lang]}).to_json(os.path.join(a.models, f"{lang}_tagger.json"))
            log(f"saved final {lang} model")
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    log("done")


if __name__ == "__main__":
    main()
