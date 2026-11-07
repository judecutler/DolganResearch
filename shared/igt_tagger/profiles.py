"""Language profiles: typological settings that tune the tagger to a language.

The tagger learns three copies of every feature (Daume III 2007, "Frustratingly easy domain
adaptation"):
  - a shared copy, learned from all training languages;
  - a type copy, shared only by languages with the same profile type (word order,
    affix position, alignment);
  - a language copy, for that language alone.
Languages of the same type pool evidence (Dolgan and Evenki are both verb-final,
suffixing, nominative-accusative), while a verb-initial or ergative language does not
inherit their position rules. A language with no training data at all falls back on the
shared and type copies.

Profiles come from two places:
  1. declared values, with a source, for the languages we know (DECLARED below);
  2. values estimated from the language's own glossed text (estimate()), used when a value
     is not declared and reported next to the declared one as a check.
"""
from igt import CASES, NOMINAL_PS, VERBAL_PS, case_of, parse_gloss

# Declared profiles. Sources are general typological descriptions; each value is checked
# against the corpus by estimate() in the evaluation report.
DECLARED = {
    "dolgan": {"order": "OV", "affix": "suffix", "align": "acc", "prodrop": True, "dom": True,
               "source": "Turkic, close to Sakha; SOV with looser order (Stapert 2013, ch. 7); "
                         "differential object marking NOM/ACC/PART (Daebritz 2023)"},
    "evenki": {"order": "OV", "affix": "suffix", "align": "acc", "prodrop": True, "dom": True,
               "source": "Tungusic; SOV, suffixing, accusative and indefinite accusative "
                         "(Sheifer and Bolshakova 2023 slides; INEL Evenki glosses ACC, ACC.INDF)"},
}
KEYS = ("order", "affix", "align")


def type_key(profile):
    return "-".join(str(profile.get(k, "?")) for k in KEYS)


def estimate(rows):
    """Profile values estimated from glossed tokens of one language (no labels used).

    order: share of accusative-marked nominals that precede the next verb in their utterance.
    affix: share of glossed words whose grammatical labels follow the lemma.
    align: 'erg' if ERG labels outnumber ACC labels, else 'acc'.
    """
    from igt import group_utterances
    before = after = acc = erg = suffix = prefix = 0
    for _, toks in group_utterances(rows):
        a = [(t.get("ps", ""), parse_gloss(t.get("ge", ""))) for t in toks]
        verbs = [i for i, (ps, _) in enumerate(a) if ps in VERBAL_PS]
        for i, (ps, g) in enumerate(a):
            c = case_of(g["tags"])
            acc += c == "ACC"
            erg += c == "ERG"
            ge = toks[i].get("ge", "")
            if g["tags"] and ge:
                first = ge.split("-")[0].split(".")[0].strip("[]")
                if first.isupper() and first in CASES | {"NEG", "CAUS"}:
                    prefix += 1
                else:
                    suffix += 1
            if ps in NOMINAL_PS and c == "ACC" and verbs:
                if any(v > i for v in verbs):
                    before += 1
                else:
                    after += 1
    n = before + after
    return {"order": "OV" if n and before / n >= 0.5 else ("VO" if n else "?"),
            "order_share_OV": round(before / n, 3) if n else None,
            "affix": "suffix" if suffix >= prefix else "prefix",
            "align": "erg" if erg > acc else "acc",
            "n_acc": acc, "n_erg": erg}


def profile_for(language, rows=None):
    """Declared profile, with missing keys filled from estimate(rows)."""
    p = dict(DECLARED.get(language, {}))
    if rows is not None and any(k not in p for k in KEYS):
        est = estimate(rows)
        for k in KEYS:
            p.setdefault(k, est[k])
    for k in KEYS:
        p.setdefault(k, "?")
    return p


def augment(feats, language, profile, copies=("shared", "type", "lang")):
    """Daume-style feature augmentation, plus a few profile-conditioned conjunctions."""
    t = type_key(profile)
    out = []
    for f in feats:
        g = {}
        for k, v in f.items():
            if "shared" in copies:
                g[k] = v
            if "type" in copies:
                g["T:" + t + "|" + k] = v
            if "lang" in copies:
                g["L:" + language + "|" + k] = v
        out.append(g)
    return out
