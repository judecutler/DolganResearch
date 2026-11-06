"""Study B1: candidate secondary predicates (dative versus instrumental), for human vetting.

    python3 case_change/extract_b1.py data/derived/dolgan data/derived/dolgan/b1_candidates.csv

No tag marks secondary predicates (D-021). The rules follow the only Dolgan examples
in Siegl (2015: 269-270): a role noun in the instrumental or dative next to the copula
"be" (ex. 30, *ńučča aptaa-ga e-te* 'was (as) a Russian sorcerer') or after a verb it
describes (ex. 29b, *vospitatel-nnan ... üleelir* 'works as an educator'). Rules:
  copula_next   INS or DAT/LOC nominal followed within 2 words by a verb glossed "be"
                or "become", or a word whose SyF has function "cop", with no other
                verb in between (handoff 003: in 139 of 267 hits a lexical verb stood
                between, so the noun most likely belonged to that verb)
  syf_pred      INS or DAT/LOC nominal whose own SyF function is "pred"
  ins_nominal   any other INS nominal with no SeR role (role nouns 'as X'); Dolgan only
The rules are a high-recall net. Humans decide every item. The output holds corpus
text, so it stays in data/derived/.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))

from inel import gloss  # noqa: E402
from inel.load import table, write  # noqa: E402

CASES = ("INS", "DAT/LOC")
# Part-of-speech values that are not nominal. The full ps inventory is UNVERIFIED;
# the QA report lists it.
NON_NOMINAL_PS = ("v", "cop", "ptcl", "conj", "interj", "adv", "post", "")
COPULA_STEMS = ("be", "become")
WINDOW = 2
VERBAL_PS = ("v", "aux", "cop")
COLUMNS = (
    "token_id", "utt_id", "text_id", "corpus", "speaker_id", "rules", "tx", "case", "ps", "SyF", "SeR",
    "next_verb", "genre", "source_collection", "recording_lo", "recording_hi", "birth_mid",
    "context", "gloss_line", "fe",
)


def _is_copula(w):
    return gloss.stem_gloss(w["ge"]) in COPULA_STEMS or any(
        fn.startswith("cop") or fn.endswith("cop") for fn in gloss.overt_functions(w["SyF"]))


def candidates(tokens, utterances, texts, speakers):
    utt = {u["utt_id"]: u for u in utterances}
    text = {t["text_id"]: t for t in texts}
    spk = {s["speaker_id"]: s for s in speakers}
    by_utt = {}
    for t in tokens:
        by_utt.setdefault(t["utt_id"], []).append(t)
    rows = []
    for utt_id, words in by_utt.items():
        for i, w in enumerate(words):
            if w["case"] not in CASES or w["ps"] in NON_NOMINAL_PS:
                continue
            rules = []
            nxt = []
            for x in words[i + 1:i + 1 + WINDOW]:
                if _is_copula(x):
                    nxt = [x]
                    break
                if x["ps"] in VERBAL_PS:
                    break  # another verb comes first: the noun belongs to it, not to the copula
            if nxt:
                rules.append("copula_next")
            if "pred" in gloss.overt_functions(w["SyF"]):
                rules.append("syf_pred")
            if not rules and w["case"] == "INS" and not w["SeR"] and w["ps"] == "n":
                rules.append("ins_nominal")
            if not rules:
                continue
            tx, s = text.get(w["text_id"], {}), spk.get(w["speaker_id"], {})
            rows.append({
                "token_id": w["token_id"], "utt_id": utt_id, "text_id": w["text_id"],
                "corpus": w["corpus"], "speaker_id": w["speaker_id"], "rules": " ".join(rules), "tx": w["tx"],
                "case": w["case"], "ps": w["ps"], "SyF": w["SyF"], "SeR": w["SeR"],
                "next_verb": nxt[0]["ge"] if nxt else "", "genre": tx.get("genre", ""),
                "source_collection": tx.get("source_collection", ""),
                "recording_lo": tx.get("recording_lo", ""), "recording_hi": tx.get("recording_hi", ""),
                "birth_mid": s.get("birth_mid", ""),
                "context": " ".join(f"[[{x['tx']}]]" if j == i else x["tx"] for j, x in enumerate(words)),
                "gloss_line": " ".join(f"[[{x['ge'] or '?'}]]" if j == i else (x["ge"] or "?")
                                       for j, x in enumerate(words)),
                "fe": utt.get(utt_id, {}).get("fe", ""),
            })
    return rows


def main(derived, out):
    rows = candidates(table(derived, "tokens"), table(derived, "utterances"), table(derived, "texts"),
                      table(derived, "speakers"))
    write(out, COLUMNS, rows)
    return rows


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    print(len(main(*sys.argv[1:])), "B1 candidates")
