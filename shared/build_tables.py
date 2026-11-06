"""Build the derived tables for one corpus.

    python3 shared/build_tables.py dolgan data/raw/dolgan-2.0 data/derived/dolgan

Reads every .exb under the raw folder and the single .coma file, and writes
texts.csv, speakers.csv, utterances.csv, tokens.csv, morphemes.csv, qa_flags.csv
and counts.json. Stdlib only. Never writes into the raw folder.
"""
import csv
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inel import config, gloss, tables  # noqa: E402
from inel.coma import communications_by_text, read_coma  # noqa: E402
from inel.exb import read_exb  # noqa: E402
from inel.load import write  # noqa: E402


def find_inputs(raw, corpus):
    """The .coma and the transcripts, laid out as 002 found them: <root>/<genre>/<text>/<id>.exb.

    The corpus root is the folder holding the .coma (the raw folder or one level below).
    Only <root>/*/*/*.exb is read, as in 002, so .exb files in utility folders are ignored.
    """
    for depth in ("*.coma", os.path.join("*", "*.coma")):
        comas = sorted(glob.glob(os.path.join(raw, depth)))
        if comas:
            break
    named = [c for c in comas if os.path.basename(c).lower().startswith(corpus)]
    if len(comas) > 1 and len(named) == 1:
        comas = named
    if len(comas) != 1:
        sys.exit(f"expected one .coma in {raw} or one folder below it, found {len(comas)}: {comas}")
    root = os.path.dirname(comas[0])
    exbs = sorted(glob.glob(os.path.join(root, "*", "*", "*.exb")))
    if not exbs:
        other = sorted(glob.glob(os.path.join(raw, "**", "*.exb"), recursive=True))[:5]
        sys.exit(f"no <genre>/<text>/*.exb under {root}; .exb files found elsewhere: {other}")
    return exbs, comas[0]


def syf_last_part(v):
    """002's rule for objects: the text after the last ':' of a SyF value (Q9)."""
    v = v.strip()
    return v.rsplit(":", 1)[-1] if ":" in v else ""


_CASES_002 = {"ACC", "DAT", "LOC", "ABL", "ALL", "LAT", "INS", "INSTR", "COM", "PROL", "GEN", "PART", "COMP", "VOC"}


def case_002(ge):
    """Object case exactly as handoff 002 classified it (scripts/q_main_d.py), for reconciliation only."""
    ge = ge.strip()
    if not ge:
        return "no_ge"
    if re.search(r"\.\[NOM\]$", ge):
        return "NOM"
    comps = set(re.split(r"[.\[\]/]", ".".join(m.text for m in gloss.split_morphs(ge))))
    if "ACC" in comps:
        return "ACC"
    other = comps & (_CASES_002 - {"ACC"})
    return ",".join(sorted(other)) if other else "none"


def count(texts, speakers_rows, utts, toks, morphs, side):
    c = {
        "transcripts": len(texts),
        "parse_errors": side["parse_errors"],
        "speaker_ids_in_exb": len(side["exb_speakers"]),
        "speakers_in_exb_and_coma": len(side["exb_speakers"] & side["coma_speakers"]),
        "speakers_with_words": len(speakers_rows),
        "tx_events": len(toks),
        "tx_events_in_utterances": sum(1 for t in toks if "#orphan" not in t["utt_id"]),
        "ref_events": len(utts),
        "words_with_mb": side["mb_events"],
        "words_with_nonempty_mb": sum(1 for t in toks if t["mb"]),
        "words_mb_ge_mismatch": sum(1 for t in toks if t["mb"] and t["ge"]
                                    and len(gloss.split_morphs(t["mb"])) != len(gloss.split_morphs(t["ge"]))),
        "words_align_false": sum(1 for t in toks if t["align_ok"] == "false"),
        "texts_with_SyF": sum(1 for t in texts if t["has_SyF"]),
        "morphemes": len(morphs),
    }
    ends_o = [t for t in toks if syf_last_part(t["SyF"]) == "O"]
    c["words_syf_ends_O"] = len(ends_o)
    for case in ("ACC", "NOM", "PART"):
        c[f"syf_ends_O_{case}"] = sum(1 for t in ends_o if case_002(t["ge"]) == case)
    c["ge_EVID"] = sum(1 for t in toks if gloss.has_component(t["ge"], "EVID", certain_only=True))
    c["ge_INFER"] = sum(1 for t in toks if gloss.has_component(t["ge"], "INFER", certain_only=True))
    c["ge_PST2"] = sum(1 for t in toks if gloss.has_component(t["ge"], "PST2", certain_only=True))
    c["mp_TAK_ge_COND1"] = sum(1 for m in morphs if gloss.parse_gloss(m["form_underlying"]).overt == "TAK"
                               and m["gloss_overt"] == "COND1")
    ge_pieces = [m.text for t in toks for m in gloss.split_morphs(t["ge"])]
    c["ge_zero_NOM_morphs"] = sum(1 for g in ge_pieces if g.endswith(".[NOM]") or g == "[NOM]")
    c["ge_ACC_morphs"] = sum(1 for g in ge_pieces if g == "ACC")
    c["speakers_with_birth_year"] = sum(1 for s in speakers_rows if s["birth_lo"] != "")
    c["source_unknown_texts"] = sum(1 for t in texts if t["source_collection"] == "unknown")
    return c


def build(corpus, raw, out):
    if corpus not in config.CORPORA:
        sys.exit(f"corpus must be one of {config.CORPORA}")
    exbs, coma_path = find_inputs(raw, corpus)
    coma_speakers, comms = read_coma(coma_path)
    by_text = communications_by_text(comms)

    texts, utts, toks, morphs, qa, errors = [], [], [], [], [], []
    unknown_tiers, exb_speakers, mb_events = set(), set(), 0
    for path in exbs:
        try:
            tr = read_exb(path)
        except Exception as ex:  # one bad file must not stop the build; it is reported
            errors.append((path, repr(ex)))
            qa.append({"corpus": corpus, "text_id": os.path.basename(path), "token_id": "",
                       "flag": "parse_error", "detail": repr(ex)})
            continue
        unknown_tiers |= tr.unknown_tiers
        exb_speakers |= set(tr.speakers)
        mb_events += sum(1 for u in tr.utterances for w in u.words if "mb" in w.tiers)
        mb_events += sum(1 for w in tr.orphan_words if "mb" in w.tiers)
        u, t, m, q = tables.transcript_rows(tr, corpus)
        genre_folder = os.path.basename(os.path.dirname(os.path.dirname(path)))
        comm = by_text.get(tr.text_id)
        if comm is None:
            q.append({"corpus": corpus, "text_id": tr.text_id, "token_id": "",
                      "flag": "no_coma_record", "detail": ""})
        texts.append(tables.text_row(tr, corpus, genre_folder, comm, u, t))
        utts += u
        toks += t
        morphs += m
        qa += q

    spk = tables.speaker_rows(corpus, coma_speakers, toks)
    for s in spk:
        if not s["in_coma"]:
            qa.append({"corpus": corpus, "text_id": "", "token_id": "", "flag": "speaker_not_in_coma",
                       "detail": s["speaker_id"]})
    for tier in sorted(unknown_tiers):
        qa.append({"corpus": corpus, "text_id": "", "token_id": "", "flag": "unknown_tier", "detail": tier})

    os.makedirs(out, exist_ok=True)
    write(os.path.join(out, "texts.csv"), tables.TEXT_COLUMNS, texts)
    write(os.path.join(out, "speakers.csv"), tables.SPEAKER_COLUMNS, spk)
    write(os.path.join(out, "utterances.csv"), tables.UTTERANCE_COLUMNS, utts)
    write(os.path.join(out, "tokens.csv"), tables.TOKEN_COLUMNS, toks)
    write(os.path.join(out, "morphemes.csv"), tables.MORPHEME_COLUMNS, morphs)
    write(os.path.join(out, "qa_flags.csv"), tables.QA_COLUMNS, qa)
    side = {"parse_errors": len(errors), "exb_speakers": exb_speakers, "coma_speakers": set(coma_speakers),
            "mb_events": mb_events}
    counts = count(texts, spk, utts, toks, morphs, side)
    with open(os.path.join(out, "counts.json"), "w", encoding="utf-8") as f:
        json.dump({"corpus": corpus, "raw": os.path.abspath(raw), "coma": os.path.basename(coma_path),
                   "counts": counts}, f, indent=2, sort_keys=True)
    return counts


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    c = build(*sys.argv[1:])
    print(json.dumps(c, indent=2, sort_keys=True))
