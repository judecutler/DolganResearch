"""Study A: find every word that might carry an evidential, and say which rule found it.

    python3 shared/evid_candidates.py data/derived/dolgan data/derived/dolgan/evid_candidates.csv

High recall on purpose: annotators can discard a false hit but never see a missed one.
Rules (D-020; forms from handoff 002, Q18):
  tier 1  ge_EVID, ge_INFER     the corpus glosses the word as evidential
  tier 2  mp_TAK_not_INFER      Dolgan TAK glossed COND1 or another label
          mp_BIT                Dolgan BIT (PST2 or PTCP.PST), the postterminal (D-022)
          copula_BIT            BIT on a stem glossed "be" (the copula, per Däbritz 2023)
          IST_quot              IST tag containing "quot" (quotative frames; spelling UNVERIFIED)
          particle_buollaga     the particle *buollaga* (from -TAK; Skribnik and Aikhenvald 2024: 1018),
                                matched on the transcription; Dolgan only; spelling UNVERIFIED
          evenki_PRF            Evenki perfect (PRF): Malchukov (1999, 2000) describe the Tungusic
                                perfect as the main indirect-evidential form (ledger, Study A)
The output holds corpus sentences: it stays in data/derived/ (git-ignored).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inel import gloss  # noqa: E402
from inel.load import table, write  # noqa: E402

COLUMNS = (
    "token_id", "utt_id", "text_id", "corpus", "speaker_id", "tier", "rules", "target_morph",
    "tx", "mb", "mp", "ge", "ps", "IST", "genre", "source_collection", "birth_mid",
    "recording_lo", "recording_hi", "context", "gloss_line", "fe",
)


def _morphs(w):
    if w["align_ok"] != "true":
        return []
    return list(zip(gloss.split_morphs(w["mp"]), gloss.split_morphs(w["ge"])))


def rules_for(w, corpus):
    """(rule names, index of the matched morph or -1)."""
    hits, where = [], -1
    for label in ("EVID", "INFER"):
        if gloss.has_component(w["ge"], label):
            hits.append(f"ge_{label}")
    ms = _morphs(w)
    if corpus == "dolgan":
        stem = gloss.stem_gloss(w["ge"])
        for i, (p, g) in enumerate(ms):
            comps = gloss.parse_gloss(g.text).components
            form = gloss.parse_gloss(p.text).overt  # mp can carry zeros too, e.g. IAK.[tA] (002, Q5)
            if form == "TAK" and "INFER" not in comps:
                hits.append("mp_TAK_not_INFER")
                where = i
            if form == "BIT":
                hits.append("copula_BIT" if stem == "be" else "mp_BIT")
                where = i
    if corpus == "dolgan" and "ollag" in w.get("tx", "").lower().replace("\u0361", "") and "INFER" not in w["ge"] \
            and not any(gloss.parse_gloss(p.text).overt == "TAK" for p, _ in ms):
        hits.append("particle_buollaga")
    if corpus == "evenki" and gloss.has_component(w["ge"], "PRF"):
        hits.append("evenki_PRF")
    if "quot" in (w["IST"] + " " + w["IST_cover"]).lower():
        hits.append("IST_quot")
    if where < 0 and hits:
        for i, (p, g) in enumerate(ms):
            if {"EVID", "INFER", "PRF"} & set(gloss.parse_gloss(g.text).all_components):
                where = i
    return hits, where


def candidates(tokens, utterances, texts, speakers, corpus):
    utt = {u["utt_id"]: u for u in utterances}
    text = {t["text_id"]: t for t in texts}
    spk = {s["speaker_id"]: s for s in speakers}
    by_utt = {}
    for t in tokens:
        by_utt.setdefault(t["utt_id"], []).append(t)
    rows = []
    for utt_id, words in by_utt.items():
        for i, w in enumerate(words):
            hits, where = rules_for(w, corpus)
            if not hits:
                continue
            tier = 1 if any(h.startswith("ge_") for h in hits) else 2
            ctx = " ".join(f"[[{x['tx']}]]" if j == i else x["tx"] for j, x in enumerate(words))
            gl = " ".join(f"[[{x['ge'] or '?'}]]" if j == i else (x["ge"] or "?") for j, x in enumerate(words))
            tx, s = text.get(w["text_id"], {}), spk.get(w["speaker_id"], {})
            target = gloss.split_morphs(w["mp"])[where].text if where >= 0 else ""
            if "#orphan" in utt_id:
                ctx = gl = w["tx"]
            rows.append({
                "token_id": w["token_id"], "utt_id": utt_id, "text_id": w["text_id"], "corpus": corpus,
                "speaker_id": w["speaker_id"], "tier": tier, "rules": " ".join(hits),
                "target_morph": target, "tx": w["tx"], "mb": w["mb"], "mp": w["mp"], "ge": w["ge"],
                "ps": w["ps"], "IST": w["IST"] or w["IST_cover"], "genre": tx.get("genre", ""),
                "source_collection": tx.get("source_collection", ""), "birth_mid": s.get("birth_mid", ""),
                "recording_lo": tx.get("recording_lo", ""), "recording_hi": tx.get("recording_hi", ""),
                "context": ctx, "gloss_line": gl, "fe": utt.get(utt_id, {}).get("fe", ""),
            })
    return rows


def main(derived, out):
    tokens = table(derived, "tokens")
    corpus = tokens[0]["corpus"] if tokens else ""
    rows = candidates(tokens, table(derived, "utterances"), table(derived, "texts"),
                      table(derived, "speakers"), corpus)
    write(out, COLUMNS, rows)
    return rows


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    print(len(main(*sys.argv[1:])), "candidates")
