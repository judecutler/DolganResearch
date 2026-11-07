"""A memory-based glosser: transcription -> segmentation, gloss and part of speech.

Trained on a glossed corpus of the same language (INEL tokens.csv: tx, mb, ge, ps).
1. Known word forms get their most frequent analysis; if the form is ambiguous, the
   analysis seen most often before the next word's form is preferred (a bigram backoff).
2. Unknown forms are split into a known stem plus a chain of known suffixes (surface
   forms, so vowel-harmony allomorphs are learned as listed), choosing the split whose
   suffix chain is most frequent in training. This is the usual approach for agglutinative
   languages with a small corpus.
3. Anything else is left unglossed and flagged for a human.

Standard library only. Every output carries a confidence label (known/ambiguous/split/
none) so the review step can show the uncertain words first.

    python3 shared/igt_tagger/glosser.py evaluate data/derived/dolgan [--test-share 0.2]
"""
import csv
import os
import random
import re
import sys
from collections import Counter, defaultdict

PUNCT = re.compile(r"[\"'«»“”„.,!?;:()\[\]–—…]+")


def norm(tx):
    return PUNCT.sub("", (tx or "").lower()).strip()


def _morphs(mb):
    return [m for m in re.split(r"[-=]", mb or "") if m]


def _gl(ge):
    return [m for m in re.split(r"[-=]", ge or "") if m]


class Glosser:
    def __init__(self, strategy="ending", ps_model=None):
        self.strategy = strategy
        self.ps_model = ps_model  # optional model.LinearModel over char_features (train_ps_model)
        self.forms = defaultdict(Counter)        # form -> Counter((mb, ge, ps))
        self.bigram = defaultdict(Counter)       # (form, next form) -> Counter(analysis)
        self.prevgram = defaultdict(Counter)     # (previous form, form) -> Counter(analysis)
        self.stems = defaultdict(Counter)        # stem surface -> Counter((stem gloss, ps))
        self.suffix = defaultdict(Counter)       # suffix surface -> Counter(gloss)
        self.chains = Counter()                  # tuple of suffix glosses -> count
        self.endings = defaultdict(Counter)      # last k letters -> Counter((suffix surface, suffix glosses, ps))

    def train(self, rows):
        rows = [r for r in rows if r.get("ge") and r.get("mb")]
        for k, r in enumerate(rows):
            f = norm(r["tx"])
            if not f:
                continue
            a = (r["mb"], r["ge"], r.get("ps", ""))
            self.forms[f][a] += 1
            nxt = norm(rows[k + 1]["tx"]) if k + 1 < len(rows) and rows[k + 1].get("utt_id") == r.get("utt_id") else ""
            self.bigram[(f, nxt)][a] += 1
            prv = norm(rows[k - 1]["tx"]) if k > 0 and rows[k - 1].get("utt_id") == r.get("utt_id") else ""
            self.prevgram[(prv, f)][a] += 1
            ms, gs = _morphs(r["mb"]), _gl(r["ge"])
            if len(ms) != len(gs) or not ms:
                continue
            self.stems[ms[0].lower()][(gs[0], r.get("ps", ""))] += 1
            for m, g in zip(ms[1:], gs[1:]):
                self.suffix[m.lower()][g] += 1
            self.chains[tuple(gs[1:])] += 1
            suf = "".join(ms[1:]).lower()
            if f.endswith(suf):
                for k in range(1, min(8, len(f)) + 1):
                    self.endings[f[-k:]][(suf, tuple(gs[1:]), r.get("ps", ""))] += 1
        return self

    def _by_ending(self, f, min_count=2):
        """Analysis of the suffixes from the longest word ending seen in training."""
        for k in range(min(8, len(f) - 1), 0, -1):
            c = self.endings.get(f[-k:])
            if c and sum(c.values()) >= min_count:
                (suf, gl, ps), _ = c.most_common(1)[0]
                stem = f[:len(f) - len(suf)] if suf and f.endswith(suf) else f
                if not stem:
                    continue
                sg = self.stems[stem].most_common(1)[0][0][0] if stem in self.stems else "???"
                mb = "-".join([stem] + ([suf] if suf else []))
                return mb, "-".join([sg] + list(gl)), ps
        return None

    def _split(self, f):
        """Best (mb, ge, ps) for an unknown form from a known stem and known suffixes."""
        best = None
        for cut in range(len(f) - 1, 0, -1):
            stem, rest = f[:cut], f[cut:]
            if stem not in self.stems:
                continue
            for segs in self._segment(rest):
                gl = tuple(self.suffix[s].most_common(1)[0][0] for s in segs)
                score = self.chains.get(gl, 0) + 0.01 * sum(self.suffix[s].most_common(1)[0][1] for s in segs)
                if best is None or score > best[0]:
                    (sg, ps), _ = self.stems[stem].most_common(1)[0]
                    best = (score, "-".join([stem] + list(segs)), "-".join([sg] + list(gl)), ps)
        return best[1:] if best and best[0] > 0 else None

    def _segment(self, rest, depth=0):
        if not rest:
            yield []
            return
        if depth > 6:
            return
        for k in range(len(rest), 0, -1):
            s = rest[:k]
            if s in self.suffix:
                for tail in self._segment(rest[k:], depth + 1):
                    yield [s] + tail

    def gloss(self, words):
        """[(mb, ge, ps, confidence)] for a list of transcribed words of one utterance."""
        out = []
        fs = [norm(w) for w in words]
        for k, f in enumerate(fs):
            if f in self.forms:
                c = self.forms[f]
                nxt = fs[k + 1] if k + 1 < len(fs) else ""
                prv = fs[k - 1] if k > 0 else ""
                votes = Counter()
                for a_, n_ in c.items():
                    votes[a_] = n_ / sum(c.values())
                for ctx in (self.bigram.get((f, nxt)), self.prevgram.get((prv, f))):
                    if ctx:
                        tot = sum(ctx.values())
                        for a_, n_ in ctx.items():
                            votes[a_] += 2 * n_ / tot
                a = votes.most_common(1)[0][0]
                share = c[a] / sum(c.values())
                out.append((*a, "known" if share >= 0.9 else "ambiguous"))
            else:
                s = self._split(f) if f else None
                e = self._by_ending(f) if f else None
                if e and self.ps_model is not None:
                    p = self.ps_model.proba(char_features(f))
                    e = (e[0], e[1], max(p, key=p.get))
                if self.strategy == "ending" and e:
                    out.append((*e, "ending"))
                elif s:
                    out.append((*s, "split"))
                elif e:
                    out.append((*e, "ending"))
                else:
                    out.append(("", "", "", "none"))
        return out


def char_features(f):
    """Word-shape features for guessing the part of speech of an unseen form."""
    x = {"len=" + str(min(len(f), 12)): 1}
    for k in range(1, 7):
        if len(f) > k:
            x["suf%d=%s" % (k, f[-k:])] = 1
    for k in range(1, 4):
        if len(f) > k:
            x["pre%d=%s" % (k, f[:k])] = 1
    return x


def train_ps_model(rows, C=1.0, min_count=2):
    """Part-of-speech guesser for unseen forms (needs scikit-learn; predicts without it)."""
    from model import _fit
    rows = [r for r in rows if r.get("ge") and r.get("ps") and norm(r["tx"])]
    return _fit([char_features(norm(r["tx"])) for r in rows], [r["ps"] for r in rows], C, min_count)


def _utts(rows):
    by = defaultdict(list)
    for r in rows:
        by[r["utt_id"]].append(r)
    for v in by.values():
        v.sort(key=lambda r: int(r.get("idx") or 0))
    return by


def evaluate(derived, share=0.2, seed=20261107, strategy="ending", ps_model=False):
    with open(os.path.join(derived, "tokens.csv"), encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f)]
    texts = sorted({r["text_id"] for r in rows})
    random.Random(seed).shuffle(texts)
    test = set(texts[:int(round(share * len(texts)))])
    train = [r for r in rows if r["text_id"] not in test]
    g = Glosser(strategy, train_ps_model(train) if ps_model else None).train(train)
    stats = defaultdict(Counter)
    case_re = re.compile(r"\b(NOM|ACC|PART|DAT/LOC|DAT|LOC|ABL|INSTR|COM|PROPR|CAR|GEN|COMP|ALL|LAT|PROL)\b")
    for u, ws in _utts([r for r in rows if r["text_id"] in test]).items():
        ws = [w for w in ws if w.get("ge")]
        if not ws:
            continue
        for w, (mb, ge, ps, conf) in zip(ws, g.gloss([w["tx"] for w in ws])):
            for key in (conf, "all"):
                s = stats[key]
                s["n"] += 1
                s["ge_exact"] += ge == w["ge"]
                s["ps"] += ps == w["ps"]
                s["mb_exact"] += mb == w["mb"]
                tc = case_re.findall(w["ge"])
                pc = case_re.findall(ge)
                s["case_n"] += bool(tc)
                s["case_ok"] += bool(tc) and tc[-1:] == pc[-1:]
    return {k: {"words": v["n"], "gloss_exact": v["ge_exact"] / v["n"], "ps": v["ps"] / v["n"],
                "segmentation_exact": v["mb_exact"] / v["n"],
                "case_correct": v["case_ok"] / v["case_n"] if v["case_n"] else None}
            for k, v in stats.items()}, len(test)


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "evaluate":
        res, n = evaluate(sys.argv[2], strategy=sys.argv[3] if len(sys.argv) > 3 else "ending")
        print(f"held-out texts: {n}")
        for k, v in sorted(res.items(), key=lambda x: -x[1]["words"]):
            print(k, {a: (round(b, 3) if isinstance(b, float) else b) for a, b in v.items()})
    else:
        sys.exit(__doc__)
