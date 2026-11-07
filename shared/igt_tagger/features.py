"""Feature dictionaries for each word of an utterance, from the IGT alone.

Two feature sets:
- "universal": gloss labels, part of speech, position and context. No lemmas. Transfers
  between languages that share the Leipzig labels.
- "full": universal plus English gloss lemmas of the word and of its nearest verbs. The
  gloss line is in English for every INEL corpus, so lemma features (for instance that
  "take" usually has an object) can also transfer between languages.
"""
from valency import bucket as vbucket
from igt import FINITE_TAM, NOMINAL_PS, PRONOUN_LEMMA_PERSON, VERBAL_PS, case_of, finiteness, parse_gloss, person_of


def _bucket(d):
    if d is None:
        return "none"
    return str(d) if d <= 3 else "4+"


def _verb_like(t):
    return t["ps"] in VERBAL_PS or (t["fin"] == "finite" and t["ps"] not in NOMINAL_PS)


def analyse(rows):
    """Per-word summaries the features are built from."""
    out = []
    for r in rows:
        g = parse_gloss(r.get("ge", ""))
        ps = (r.get("ps") or "").strip() or "none"
        pers = person_of(g)
        poss = None
        if ps in NOMINAL_PS and ps != "pers":
            # On a noun, a person label is the possessor; the noun itself is third person
            poss, pers = pers, "3"
        if ps == "pers" and not pers:
            pers = PRONOUN_LEMMA_PERSON.get(g["lemma"].split(".")[0])
        out.append({"ps": ps, "case": case_of(g["tags"]) or "none", "zero_case": bool(g["zero"] & {"NOM"}),
                    "tags": set(g["tags"]), "zero": set(g["zero"]), "fin": finiteness(g["tags"]), "pers": pers,
                    "lemma": g["lemma"], "poss": poss, "glossed": bool(g["n_morphs"]), "n_morphs": g["n_morphs"]})
    return out


def utterance_features(rows, feature_set="full", language=None, valency=None):
    """One feature dict per word."""
    a = analyse(rows)
    n = len(a)
    verbs = [i for i, t in enumerate(a) if _verb_like(t)]
    finite_verbs = [i for i in verbs if a[i]["fin"] == "finite"]
    nom_nominals = [i for i, t in enumerate(a) if t["ps"] in NOMINAL_PS and t["case"] == "NOM"]
    feats = []
    for i, t in enumerate(a):
        f = {"bias": 1, "ps=" + t["ps"]: 1, "case=" + t["case"]: 1, "fin=" + t["fin"]: 1,
             "ps_case=" + t["ps"] + "_" + t["case"]: 1, "glossed=" + str(t["glossed"]): 1,
             "nm=" + _bucket(t["n_morphs"]): 1}
        if t["zero_case"]:
            f["zero_nom"] = 1
        for z in t["zero"]:
            # Zero morphs written in brackets, e.g. predicative [3SG] on a nominal predicate
            f["zero=" + z] = 1
            f["ps_zero=" + t["ps"] + "_" + z] = 1
        for tag in ("PL", "POSS", "INDF", "NEG", "Q", "EMPH", "PROPR", "CAUS", "PASS"):
            if tag in t["tags"]:
                f["has=" + tag] = 1
        if t["poss"]:
            f["poss=" + t["poss"]] = 1
        if t["pers"]:
            f["pers=" + t["pers"]] = 1
            f["ps_pers=" + t["ps"] + "_" + t["pers"]] = 1
        f["first"] = int(i == 0)
        f["last"] = int(i == n - 1)
        f["relpos=" + str(min(4, int(5 * i / max(n, 1))))] = 1
        f["len=" + _bucket(n // 3)] = 1
        for k in (-2, -1, 1, 2):
            j = i + k
            if 0 <= j < n:
                f[f"ps{k:+d}=" + a[j]["ps"]] = 1
                f[f"case{k:+d}=" + a[j]["case"]] = 1
                if a[j]["fin"] != "none":
                    f[f"fin{k:+d}=" + a[j]["fin"]] = 1
            else:
                f[f"ps{k:+d}=BOUND"] = 1
        # Noun-phrase shape: INEL tags only the head (last word) of a noun phrase
        nxt = a[i + 1] if i + 1 < n else None
        prv = a[i - 1] if i > 0 else None
        f["np_next=" + t["case"] + "_" + (nxt["ps"] + "_" + nxt["case"] if nxt else "END")] = 1
        f["np_prev=" + t["case"] + "_" + (prv["ps"] + "_" + prv["case"] if prv else "BEGIN")] = 1
        cop_near = [j for j in range(i + 1, min(n, i + 4)) if a[j]["ps"] == "cop"]
        if cop_near:
            f["cop_within=" + str(cop_near[0] - i) + "_" + t["case"]] = 1
        right = [j for j in verbs if j > i]
        left = [j for j in verbs if j < i]
        rv = right[0] if right else None
        lv = left[-1] if left else None
        # Clause structure approximation: which verb governs this word? A converb or
        # participle right after the word heads its own (dependent) clause unless it forms
        # a complex predicate with an adjacent finite verb.
        if rv is not None:
            rv2 = right[1] if len(right) > 1 else None
            f["rv2=" + (a[rv2]["fin"] + "_" + _bucket(rv2 - rv) if rv2 is not None else "none")] = 1
            f["rv_rv2=" + a[rv]["fin"] + "_" + (a[rv2]["fin"] if rv2 is not None else "none") + "_" + t["case"]] = 1
            f["finite_right=" + str(any(a[j]["fin"] == "finite" for j in right))] = 1
        f["dright=" + _bucket(None if rv is None else rv - i)] = 1
        f["dleft=" + _bucket(None if lv is None else i - lv)] = 1
        f["n_verbs=" + _bucket(len(verbs))] = 1
        f["n_finite=" + _bucket(len(finite_verbs))] = 1
        f["is_last_verb"] = int(bool(verbs) and i == verbs[-1])
        f["is_last_finite"] = int(bool(finite_verbs) and i == finite_verbs[-1])
        before = [j for j in nom_nominals if j < (rv if rv is not None else n)]
        if i in nom_nominals:
            f["nom_rank=" + _bucket(before.index(i) if i in before else None)] = 1
            f["n_nom_before_verb=" + _bucket(len(before))] = 1
        if valency and rv is not None and t["ps"] in NOMINAL_PS:
            rates, base = valency
            vb = vbucket(rates.get(a[rv]["lemma"]), base)
            f["rv_trans=" + vb] = 1
            f["rv_trans_case=" + vb + "_" + t["case"]] = 1
        for name, j in (("rv", rv), ("lv", lv)):
            if j is not None:
                f[name + "_fin=" + a[j]["fin"]] = 1
                tam = sorted(a[j]["tags"] & FINITE_TAM)
                if tam:
                    # Clause type of the governing verb: object marking can depend on it (Study C)
                    f[name + "_tam=" + tam[0]] = 1
                    if t["ps"] in NOMINAL_PS:
                        f[name + "_tam_case=" + tam[0] + "_" + t["case"]] = 1
                if a[j]["pers"]:
                    f[name + "_pers=" + a[j]["pers"]] = 1
                    if t["pers"]:
                        f[name + "_pers_match=" + str(t["pers"] == a[j]["pers"])] = 1
        if t["ps"] in VERBAL_PS:
            has_overt_nom_before = any(j < i for j in nom_nominals)
            f["overt_nom_before=" + str(has_overt_nom_before)] = 1
        if feature_set == "full":
            if t["lemma"]:
                f["lem=" + t["lemma"]] = 1
            for name, j in (("rv", rv), ("lv", lv)):
                if j is not None and a[j]["lemma"]:
                    f[name + "_lem=" + a[j]["lemma"]] = 1
                    if t["ps"] in NOMINAL_PS:
                        f[name + "_lem_case=" + a[j]["lemma"] + "_" + t["case"]] = 1
        if language:
            f = {**f, **{"lang=" + language: 1}}
        feats.append(f)
    return feats


def _pbucket(p):
    return "0" if p < 0.2 else "1" if p < 0.5 else "2" if p < 0.8 else "3"


def add_pred_context(X, utt_ids, ps, cases, pred_probs, threshold=0.5, sub_probs=None):
    """Stage-2 features: where this word sits relative to the *predicted* predicates.

    X, utt_ids, ps, cases and pred_probs are parallel lists in utterance order. Returns new
    feature dicts (the input is not changed). Predicates include nominal and adjectival
    ones ("X is a chairman"), which the verb-based stage-1 features cannot see.
    """
    out = []
    i = 0
    n_all = len(X)
    while i < n_all:
        j = i
        while j < n_all and utt_ids[j] == utt_ids[i]:
            j += 1
        idx = list(range(i, j))
        preds = [k for k in idx if pred_probs[k] >= threshold]
        noms = [k for k in idx if cases[k] == "NOM"]
        for k in idx:
            f = dict(X[k])
            f["my_predp=" + _pbucket(pred_probs[k])] = 1
            if sub_probs is not None:
                # Is this word inside a subordinate clause? INEL tags S and O in main clauses only
                f["my_subp=" + _pbucket(sub_probs[k])] = 1
                f["my_subp_case=" + _pbucket(sub_probs[k]) + "_" + cases[k]] = 1
            f["n_pred=" + _bucket(len(preds))] = 1
            r = [p for p in preds if p > k]
            l = [p for p in preds if p < k]
            f["pr_dist=" + _bucket(r[0] - k if r else None)] = 1
            f["pl_dist=" + _bucket(k - l[-1] if l else None)] = 1
            if r:
                f["pr_ps=" + (ps[r[0]] or "none")] = 1
                f["pr_ps_case=" + (ps[r[0]] or "none") + "_" + cases[k]] = 1
                if cases[k] == "NOM":
                    before = [m for m in noms if m < r[0]]
                    f["nom_rank_pred=" + _bucket(len(before) - 1 - before.index(k) if k in before else None)] = 1
            if l:
                f["pl_ps_case=" + (ps[l[-1]] or "none") + "_" + cases[k]] = 1
            f["between_preds=" + str(bool(r and l))] = 1
            out.append(f)
        i = j
    return out
