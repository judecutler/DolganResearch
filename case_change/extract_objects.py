"""Study B: one row per object (SyF function O), with speaker and clause context.

    python3 case_change/extract_objects.py data/derived/dolgan data/derived/dolgan/objects.csv

Rows are design data only. Gate 0 reports counts from this table but never the
outcome (case) split by cohort: that waits until the analysis plan is frozen
(Gate 3, case_change/ANALYSIS_PLAN.md).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))

from inel import gloss  # noqa: E402
from inel.load import num, table, write  # noqa: E402

COLUMNS = (
    "token_id", "utt_id", "text_id", "corpus", "speaker_id", "birth_lo", "birth_hi", "birth_mid",
    "birth_precision", "recording_lo", "recording_hi", "age_at_recording", "genre",
    "source_collection", "dialect", "rule_hit", "syf", "syf_form", "human", "pronoun", "ps",
    "case", "case_flag", "plural", "person", "derivational", "ist", "bor", "bor_morph", "loan",
    "stem", "prev_ps", "align_ok", "unsure_gloss", "pred_token_id", "pred_labels", "pred_neg",
    "pred_position", "n_preds_in_utt",
)


def objects(tokens, texts, speakers, corpus):
    text = {t["text_id"]: t for t in texts}
    spk = {s["speaker_id"]: s for s in speakers}
    by_utt = {}
    for t in tokens:
        by_utt.setdefault(t["utt_id"], []).append(t)

    rows = []
    for utt_id, words in by_utt.items():
        preds = [i for i, w in enumerate(words) if "pred" in gloss.overt_functions(w["SyF"])]
        for i, w in enumerate(words):
            if "O" not in gloss.overt_functions(w["SyF"]):
                continue
            after = [p for p in preds if p > i]
            before = [p for p in preds if p < i]
            p = after[0] if after else (before[-1] if before else None)
            pw = words[p] if p is not None else None
            labels = gloss.grammatical_labels(pw["ge"]) if pw else []
            form = next(f for f, fn in gloss.annotation_items(w["SyF"]) if fn == "O" and not f.startswith("0"))
            tx, s = text.get(w["text_id"], {}), spk.get(w["speaker_id"], {})
            bmid, rlo, rhi = num(s.get("birth_mid")), num(tx.get("recording_lo")), num(tx.get("recording_hi"))
            stem = gloss.stem_gloss(w["ge"])
            case, flag = w["case"], w["case_flag"]
            rows.append({
                "token_id": w["token_id"], "utt_id": utt_id, "text_id": w["text_id"], "corpus": corpus,
                "speaker_id": w["speaker_id"], "birth_lo": s.get("birth_lo", ""),
                "birth_hi": s.get("birth_hi", ""), "birth_mid": s.get("birth_mid", ""),
                "birth_precision": s.get("birth_precision", ""),
                "recording_lo": tx.get("recording_lo", ""), "recording_hi": tx.get("recording_hi", ""),
                "age_at_recording": "" if bmid is None or rlo is None else round((rlo + rhi) / 2 - bmid, 1),
                "genre": tx.get("genre", ""), "source_collection": tx.get("source_collection", ""),
                "dialect": tx.get("dialect", ""), "rule_hit": "SyF_overt_O", "syf": w["SyF"],
                "syf_form": form, "human": int(".h" in form),
                "pronoun": int(form.startswith("pro")), "ps": w["ps"],
                "case": case if w["ge"] else "unglossed", "case_flag": flag or ("" if case else "no_case_label"),
                "plural": int(gloss.is_plural(w["ge"])), "person": gloss.person_number(w["ge"]) or "",
                "derivational": " ".join(gloss.derivational_flags(w["ge"], corpus)),
                "ist": w["IST"] or w["IST_cover"], "bor": w["BOR"], "bor_morph": w["BOR_Morph"],
                "loan": int(bool(w["BOR"])),
                "stem": "<capitalised>" if gloss.looks_like_name(stem) else stem,
                "prev_ps": words[i - 1]["ps"] if i > 0 else "",
                "align_ok": w["align_ok"],
                "unsure_gloss": int(any(g.unsure or g.unknown for g in gloss.glosses(w["ge"]))),
                "pred_token_id": pw["token_id"] if pw else "",
                "pred_labels": " ".join(labels), "pred_neg": int("NEG" in labels),
                "pred_position": "" if p is None else ("after" if p > i else "before"),
                "n_preds_in_utt": len(preds),
            })
    return rows


def main(derived, out):
    tokens = table(derived, "tokens")
    corpus = tokens[0]["corpus"] if tokens else ""
    rows = objects(tokens, table(derived, "texts"), table(derived, "speakers"), corpus)
    write(out, COLUMNS, rows)
    return rows


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    print(len(main(*sys.argv[1:])), "objects")
