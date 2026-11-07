"""Unsupervised verb transitivity from raw glossed text (no syntactic labels needed).

For each verb gloss lemma: the share of its occurrences with an accusative-marked nominal
among the three preceding words, smoothed toward the language-wide rate. Computed from
every glossed text of a language, tagged or not, so rare verbs in the tagged texts still
get an estimate. This is the language's own evidence about which verbs take objects,
which helps decide whether an unmarked noun before the verb is its object.
"""
from collections import Counter

from igt import NOMINAL_PS, VERBAL_PS, case_of, group_utterances, parse_gloss

WINDOW = 3


def estimate(rows, prior_weight=5.0):
    seen, with_acc = Counter(), Counter()
    for _, toks in group_utterances(rows):
        g = [(t.get("ps", ""), parse_gloss(t.get("ge", ""))) for t in toks]
        for i, (ps, gl) in enumerate(g):
            if ps in VERBAL_PS and gl["lemma"]:
                seen[gl["lemma"]] += 1
                if any(g[j][0] in NOMINAL_PS and case_of(g[j][1]["tags"]) == "ACC"
                       for j in range(max(0, i - WINDOW), i)):
                    with_acc[gl["lemma"]] += 1
    base = sum(with_acc.values()) / max(1, sum(seen.values()))
    return {v: (with_acc[v] + prior_weight * base) / (n + prior_weight) for v, n in seen.items()}, base


def bucket(rate, base):
    if rate is None:
        return "unk"
    r = rate / base if base else 0
    return "vlow" if r < 0.5 else "low" if r < 0.9 else "mid" if r < 1.3 else "high" if r < 2 else "vhigh"
