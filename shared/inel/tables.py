"""Turn parsed transcripts and metadata into the tables of docs/DATA_PREP_PLAN.md.

IDs come from the files, not from row order: utt_id = <text_id>#<nnn> (utterance
order in the file), token_id = <utt_id>.w<nn>. Words inside no utterance get
utt_id <text_id>#orphan and a QA flag.
"""
from . import gloss
from .coma import infer_dolgan_source, parse_year

TEXT_COLUMNS = (
    "corpus", "text_id", "genre", "genre_folder", "recording_raw", "recording_lo", "recording_hi",
    "recording_precision", "dialect", "dialect_group", "source_collection", "source_inferred",
    "speakers", "n_speakers", "n_utterances", "n_tokens", "n_tokens_glossed", "has_SyF", "has_SeR",
    "has_IST", "has_coma_record",
)
SPEAKER_COLUMNS = (
    "corpus", "speaker_id", "sex", "birth_lo", "birth_hi", "birth_mid",
    "birth_precision", "birth_uncertain", "dialect", "l1", "l2", "n_texts", "n_tokens",
    "in_coma",
)
UTTERANCE_COLUMNS = (
    "utt_id", "corpus", "text_id", "speaker_id", "t_start", "t_end", "n_words", "ref", "ts",
    "st", "fe", "fg", "fr", "ltr", "nt",
)
TOKEN_COLUMNS = (
    "token_id", "utt_id", "corpus", "text_id", "speaker_id", "idx", "tx", "mb", "mp", "ge",
    "gr", "mc", "ps", "SyF", "SyF_cover", "SeR", "SeR_cover", "IST", "IST_cover", "Top", "Foc",
    "BOR", "BOR_Phon", "BOR_Morph", "CS", "ExLocPoss", "n_morphs", "align_ok", "case",
    "case_flag",
)
MORPHEME_COLUMNS = (
    "token_id", "m_idx", "kind", "form_surface", "form_underlying", "gloss_en", "gloss_overt",
    "gloss_zero", "gloss_unsure",
)
QA_COLUMNS = ("corpus", "text_id", "token_id", "flag", "detail")


def _v(x):
    return "" if x is None else x


def alignment(tiers):
    """(n_morphs, align_ok). align_ok is "" for words with no morph analysis (D-018: mc ignored)."""
    pieces = [len(gloss.split_morphs(tiers.get(t, ""))) for t in ("mb", "mp", "ge")]
    if not any(pieces):
        return 0, ""
    return pieces[0], "true" if len(set(pieces)) == 1 else "false"


def transcript_rows(tr, corpus):
    utt_rows, tok_rows, mor_rows, qa = [], [], [], []
    for kind, detail in tr.issues:
        qa.append({"corpus": corpus, "text_id": tr.text_id, "token_id": "", "flag": kind, "detail": detail})

    def time(i):
        t = tr.times[i] if 0 <= i < len(tr.times) else None
        return "" if t is None else f"{t:.3f}"

    groups = [(f"{tr.text_id}#{n:03d}", u.speaker, u.words, u) for n, u in enumerate(tr.utterances, 1)]
    if tr.orphan_words:
        groups.append((f"{tr.text_id}#orphan", None, tr.orphan_words, None))

    for utt_id, spk, words, u in groups:
        if u is not None:
            row = {"utt_id": utt_id, "corpus": corpus, "text_id": tr.text_id, "speaker_id": spk,
                   "t_start": time(u.start), "t_end": time(u.end), "n_words": len(words)}
            for t in ("ref", "ts", "st", "fe", "fg", "fr", "ltr", "nt"):
                row[t] = u.tiers.get(t, "")
            utt_rows.append(row)
        for i, w in enumerate(words, 1):
            token_id = f"{utt_id}.w{i:02d}"
            if u is None:
                qa.append({"corpus": corpus, "text_id": tr.text_id, "token_id": token_id,
                           "flag": "word_outside_utterance", "detail": w.tx})
            n_morphs, ok = alignment(w.tiers)
            ge = w.tiers.get("ge", "")
            case, case_flag = gloss.word_case(ge, corpus)
            row = {"token_id": token_id, "utt_id": utt_id, "corpus": corpus, "text_id": tr.text_id,
                   "speaker_id": w.speaker, "idx": i, "tx": w.tx, "n_morphs": n_morphs,
                   "align_ok": ok, "case": _v(case), "case_flag": case_flag}
            for t in ("mb", "mp", "ge", "gr", "mc", "ps", "SyF", "SeR", "IST", "Top", "Foc",
                      "BOR", "BOR-Phon", "BOR-Morph", "CS", "ExLocPoss"):
                row[t.replace("-", "_")] = w.tiers.get(t, "")
            for t in ("SyF", "SeR", "IST"):
                row[f"{t}_cover"] = w.covering.get(t, "")
            tok_rows.append(row)
            if ok == "false":
                qa.append({"corpus": corpus, "text_id": tr.text_id, "token_id": token_id,
                           "flag": "morph_gloss_mismatch",
                           "detail": f"mb={w.tiers.get('mb', '')} ge={ge}"})
            if ok == "true":
                mb = gloss.split_morphs(w.tiers["mb"])
                mp = gloss.split_morphs(w.tiers["mp"])
                for m, p, g in zip(mb, mp, gloss.split_morphs(ge)):
                    pg = gloss.parse_gloss(g.text)
                    mor_rows.append({
                        "token_id": token_id, "m_idx": m.idx, "kind": m.kind,
                        "form_surface": m.text, "form_underlying": p.text, "gloss_en": g.text,
                        "gloss_overt": pg.overt, "gloss_zero": ".".join(pg.zeros),
                        "gloss_unsure": "unknown" if pg.unknown else ("unsure" if pg.unsure else ""),
                    })
    return utt_rows, tok_rows, mor_rows, qa


def text_row(tr, corpus, genre_folder, comm, utt_rows, tok_rows):
    rec_raw = comm.get("recording") if comm else None
    rec = parse_year(rec_raw)
    if corpus == "dolgan":
        dialect = comm.get("dialect_dolgan") if comm else None
        group = None
        source = infer_dolgan_source(comm.get("published"), comm.get("archive"), rec) if comm else "unknown"
        inferred = "true"
    else:
        dialect = comm.get("dialect_evenki") if comm else None
        group = comm.get("dialect_group_evenki") if comm else None
        source = (comm.get("source_type_evenki") if comm else None) or "unknown"
        inferred = "false"
    spk = sorted({t["speaker_id"] for t in tok_rows} | {u["speaker_id"] for u in utt_rows})
    return {
        "corpus": corpus, "text_id": tr.text_id,
        "genre": _v(comm.get("genre") if comm else None) or genre_folder,
        "genre_folder": genre_folder, "recording_raw": _v(rec_raw),
        "recording_lo": rec.lo if rec else "", "recording_hi": rec.hi if rec else "",
        "recording_precision": rec.precision if rec else "", "dialect": _v(dialect),
        "dialect_group": _v(group), "source_collection": source, "source_inferred": inferred,
        "speakers": " ".join(spk), "n_speakers": len(spk), "n_utterances": len(utt_rows),
        "n_tokens": len(tok_rows),
        "n_tokens_glossed": sum(1 for t in tok_rows if t["ge"]),
        "has_SyF": int(any(t["SyF"] or t["SyF_cover"] for t in tok_rows)),
        "has_SeR": int(any(t["SeR"] or t["SeR_cover"] for t in tok_rows)),
        "has_IST": int(any(t["IST"] or t["IST_cover"] for t in tok_rows)),
        "has_coma_record": int(comm is not None),
    }


def speaker_rows(corpus, coma_speakers, tok_rows):
    texts, tokens = {}, {}
    for t in tok_rows:
        texts.setdefault(t["speaker_id"], set()).add(t["text_id"])
        tokens[t["speaker_id"]] = tokens.get(t["speaker_id"], 0) + 1
    rows = []
    for sid in sorted(texts):
        s = coma_speakers.get(sid)
        b = s.birth if s else None
        rows.append({
            "corpus": corpus, "speaker_id": sid, "sex": s.sex if s else "",
            "birth_lo": b.lo if b else "", "birth_hi": b.hi if b else "",
            "birth_mid": b.mid if b else "", "birth_precision": b.precision if b else "",
            "birth_uncertain": int(b.uncertain) if b else "",
            "dialect": _v(s.dialect if s else None), "l1": _v(s.l1 if s else None),
            "l2": _v(s.l2 if s else None), "n_texts": len(texts[sid]), "n_tokens": tokens[sid],
            "in_coma": int(s is not None),
        })
    return rows

