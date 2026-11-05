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
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inel import config, gloss, tables  # noqa: E402
from inel.coma import communications_by_text, read_coma  # noqa: E402
from inel.exb import read_exb  # noqa: E402


def find_inputs(raw):
    exbs = sorted(glob.glob(os.path.join(raw, "**", "*.exb"), recursive=True))
    comas = sorted(glob.glob(os.path.join(raw, "**", "*.coma"), recursive=True))
    if not exbs:
        sys.exit(f"no .exb files under {raw}")
    if len(comas) != 1:
        sys.exit(f"expected exactly one .coma under {raw}, found {len(comas)}: {comas}")
    return exbs, comas[0]


def write_csv(path, columns, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="raise", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def syf_last_part(v):
    """002's rule for objects: the text after the last ':' of a SyF value (Q9)."""
    return v.rsplit(":", 1)[-1] if ":" in v else ""


def count(corpus, texts, speakers_rows, utts, toks, morphs, coma_speakers, parse_errors):
    c = {
        "transcripts": len(texts),
        "parse_errors": len(parse_errors),
        "speaker_ids_in_exb": len(speakers_rows),
        "speakers_in_exb_and_coma": sum(1 for s in speakers_rows if s["in_coma"]),
        "tx_events": len(toks),
        "tx_events_in_utterances": sum(1 for t in toks if not t["utt_id"].endswith("#orphan")),
        "ref_events": len(utts),
        "words_with_mb": sum(1 for t in toks if t["mb"]),
        "words_mb_ge_mismatch": sum(1 for t in toks if t["mb"] and t["ge"]
                                    and len(gloss.split_morphs(t["mb"])) != len(gloss.split_morphs(t["ge"]))),
        "words_align_false": sum(1 for t in toks if t["align_ok"] == "false"),
        "texts_with_SyF": sum(1 for t in texts if t["has_SyF"]),
        "morphemes": len(morphs),
    }
    ends_o = [t for t in toks if syf_last_part(t["SyF"]) == "O"]
    c["words_syf_ends_O"] = len(ends_o)
    for case in ("ACC", "NOM", "PART"):
        c[f"syf_ends_O_{case}"] = sum(1 for t in ends_o if t["case"] == case)
    c["ge_EVID"] = sum(1 for t in toks if gloss.has_component(t["ge"], "EVID", certain_only=True))
    c["ge_INFER"] = sum(1 for t in toks if gloss.has_component(t["ge"], "INFER", certain_only=True))
    c["ge_PST2"] = sum(1 for t in toks if gloss.has_component(t["ge"], "PST2", certain_only=True))
    c["mp_TAK_ge_COND1"] = sum(1 for m in morphs if m["form_underlying"] == "TAK" and m["gloss_overt"] == "COND1")
    ge_pieces = [m.text for t in toks for m in gloss.split_morphs(t["ge"])]
    c["ge_zero_NOM_morphs"] = sum(1 for g in ge_pieces if g.endswith(".[NOM]"))
    c["ge_ACC_morphs"] = sum(1 for g in ge_pieces if g == "ACC")
    c["speakers_with_birth_year"] = sum(1 for s in speakers_rows if s["birth_lo"] != "")
    c["source_unknown_texts"] = sum(1 for t in texts if t["source_collection"] == "unknown")
    return c


def build(corpus, raw, out):
    if corpus not in config.CORPORA:
        sys.exit(f"corpus must be one of {config.CORPORA}")
    exbs, coma_path = find_inputs(raw)
    coma_speakers, comms = read_coma(coma_path)
    by_text = communications_by_text(comms)

    texts, utts, toks, morphs, qa, errors = [], [], [], [], [], []
    unknown_tiers = set()
    for path in exbs:
        try:
            tr = read_exb(path)
        except Exception as ex:  # one bad file must not stop the build; it is reported
            errors.append((path, repr(ex)))
            qa.append({"corpus": corpus, "text_id": os.path.basename(path), "token_id": "",
                       "flag": "parse_error", "detail": repr(ex)})
            continue
        unknown_tiers |= tr.unknown_tiers
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
    write_csv(os.path.join(out, "texts.csv"), tables.TEXT_COLUMNS, texts)
    write_csv(os.path.join(out, "speakers.csv"), tables.SPEAKER_COLUMNS, spk)
    write_csv(os.path.join(out, "utterances.csv"), tables.UTTERANCE_COLUMNS, utts)
    write_csv(os.path.join(out, "tokens.csv"), tables.TOKEN_COLUMNS, toks)
    write_csv(os.path.join(out, "morphemes.csv"), tables.MORPHEME_COLUMNS, morphs)
    write_csv(os.path.join(out, "qa_flags.csv"), tables.QA_COLUMNS, qa)
    counts = count(corpus, texts, spk, utts, toks, morphs, coma_speakers, errors)
    with open(os.path.join(out, "counts.json"), "w", encoding="utf-8") as f:
        json.dump({"corpus": corpus, "raw": os.path.abspath(raw), "coma": os.path.basename(coma_path),
                   "counts": counts}, f, indent=2, sort_keys=True)
    return counts


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    c = build(*sys.argv[1:])
    print(json.dumps(c, indent=2, sort_keys=True))
