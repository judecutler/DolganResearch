"""The two-stage tagger.

Stage 1 predicts predicates (pred) from the word's own features.
Stage 2 predicts the argument role (S, O, -) and the zero subject (0.1, 0.2, 0.3, -) from the
word's features plus its position relative to the predicted predicates. During training,
stage-2 features use out-of-fold stage-1 predictions, so stage 2 learns from the same kind
of noisy predicate guesses it will see on new text (stacking, Wolpert 1992).

Training needs scikit-learn. A trained tagger exports to plain JSON (to_json), and
LinearModel / Tagger.from_json predict with the Python standard library only, so the
tagger runs on any machine with Python 3.
"""
import json
import math
from collections import Counter

from features import add_pred_context

STAGE1 = ("pred", "sub")
STAGE2 = ("role", "zero")


class LinearModel:
    """Multinomial logistic regression with sparse binary features (prediction only)."""

    def __init__(self, classes, weights, intercept):
        self.classes = list(classes)
        self.w = weights          # feature -> list of per-class weights
        self.b = list(intercept)

    def proba(self, x):
        if len(self.classes) == 1:
            return {self.classes[0]: 1.0}
        z = list(self.b)
        for k, v in x.items():
            ws = self.w.get(k)
            if ws:
                for c, wc in enumerate(ws):
                    z[c] += wc * v
        if len(z) == 1:  # binary: sklearn stores one row for the positive class
            p = 1 / (1 + math.exp(-z[0]))
            return {self.classes[0]: 1 - p, self.classes[1]: p}
        m = max(z)
        e = [math.exp(v - m) for v in z]
        s = sum(e)
        return {c: e[i] / s for i, c in enumerate(self.classes)}

    @classmethod
    def from_sklearn(cls, vec, clf):
        W = clf.coef_
        names = vec.get_feature_names_out()
        weights = {}
        for j, name in enumerate(names):
            col = [float(W[c, j]) for c in range(W.shape[0])]
            if any(abs(v) > 1e-6 for v in col):
                weights[str(name)] = col
        return cls([str(c) for c in clf.classes_], weights, [float(v) for v in clf.intercept_])

    def to_dict(self):
        return {"classes": self.classes, "weights": self.w, "intercept": self.b}


def _fit(X, y, C, min_count=2):
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.linear_model import LogisticRegression
    if len(set(y)) < 2:  # e.g. a corpus without subordinate-clause annotation
        return LinearModel([y[0]] if y else ["-"], {}, [])
    keep = {k for k, n in Counter(k for x in X for k in x).items() if n >= min_count}
    vec = DictVectorizer()
    M = vec.fit_transform([{k: v for k, v in x.items() if k in keep} for x in X])
    clf = LogisticRegression(C=C, max_iter=3000)
    clf.fit(M, y)
    return LinearModel.from_sklearn(vec, clf)


def _oof_probs(X, y, groups, C, positive, folds=3):
    """Out-of-fold P(positive) for the training words."""
    from sklearn.model_selection import GroupKFold
    probs = [0.0] * len(X)
    for tr, te in GroupKFold(n_splits=folds).split(X, y, groups):
        m = _fit([X[i] for i in tr], [y[i] for i in tr], C)
        for i in te:
            probs[i] = m.proba(X[i]).get(positive, 0.0)
    return probs


class Tagger:
    def __init__(self, stage1=None, stage2=None, meta=None):
        self.stage1 = stage1
        self.stage2 = stage2 or {}
        self.meta = meta or {}

    @classmethod
    def train(cls, d, C=None, meta=None):
        """d: dict from data.load (X, pred, sub, role, zero, text, utt_id, ps, case)."""
        C = dict({"pred": 0.3, "sub": 0.3, "role": 0.3, "zero": 0.3}, **(C or {}))
        s1 = {t: _fit(d["X"], d[t], C[t]) for t in STAGE1}
        probs = {t: _oof_probs(d["X"], d[t], d["text"], C[t], t) for t in STAGE1}
        X2 = add_pred_context(d["X"], d["utt_id"], d["ps"], d["case"], probs["pred"], sub_probs=probs["sub"])
        s2 = {t: _fit(X2, d[t], C[t]) for t in STAGE2}
        return cls(s1, s2, dict(meta or {}, C=C))

    def stage2_features(self, d):
        p = {t: [m.proba(x).get(t, 0.0) for x in d["X"]] for t, m in self.stage1.items()}
        return p, add_pred_context(d["X"], d["utt_id"], d["ps"], d["case"], p["pred"], sub_probs=p["sub"])

    def predict(self, d):
        """{'pred': [P(pred)], 'sub': [P(in subordinate clause)], 'role': [{class: p}], 'zero': [...]}."""
        p, X2 = self.stage2_features(d)
        out = dict(p)
        for t, m in self.stage2.items():
            out[t] = [m.proba(x) for x in X2]
        return out

    def to_json(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"meta": self.meta, "stage1": {t: m.to_dict() for t, m in self.stage1.items()},
                       "stage2": {t: m.to_dict() for t, m in self.stage2.items()}}, f)

    @classmethod
    def from_json(cls, path):
        with open(path, encoding="utf-8") as f:
            j = json.load(f)
        lm = lambda d: LinearModel(d["classes"], d["weights"], d["intercept"])  # noqa: E731
        return cls({t: lm(m) for t, m in j["stage1"].items()}, {t: lm(m) for t, m in j["stage2"].items()}, j["meta"])
