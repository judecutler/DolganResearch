"""Raw transcribed text -> glossed IGT -> argument tags, in one run.

    python3 shared/igt_tagger/pipeline.py TRAIN_DERIVED NEW_UTTERANCES.csv MODEL.json OUT_DIR

TRAIN_DERIVED: an INEL derived folder of the same language (tokens.csv with tx, mb, ge,
  ps), used to train the glosser.
NEW_UTTERANCES.csv: one row per utterance with columns utt_id, text_id, speaker_id, tx
  (the transcription, words separated by spaces) and optionally fe (free translation).
MODEL.json: a trained argument tagger (train_eval.py --models).

Writes OUT_DIR/tokens.csv, texts.csv, speakers.csv, utterances.csv in the INEL derived
format, with the glosser's analysis in mb, ge and ps and its confidence in gloss_conf
(known, ambiguous, ending, none), so apply.py can build a review queue from it. Glosses
from the glosser are drafts: a human must check them (at least every word whose
gloss_conf is not "known") before any analysis uses them.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glosser import Glosser  # noqa: E402


def _read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write(path, rows, cols):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


TOKEN_COLS = ("token_id", "utt_id", "corpus", "text_id", "speaker_id", "idx", "tx", "mb", "mp", "ge", "gr", "mc",
              "ps", "SyF", "SyF_cover", "BOR", "CS", "gloss_conf")


def gloss_utterances(train_derived, utterances, corpus="new"):
    g = Glosser().train(_read(os.path.join(train_derived, "tokens.csv")))
    tokens = []
    for u in utterances:
        words = (u.get("tx") or "").split()
        for i, (w, (mb, ge, ps, conf)) in enumerate(zip(words, g.gloss(words)), 1):
            tokens.append({"token_id": f"{u['utt_id']}.{i}", "utt_id": u["utt_id"], "corpus": corpus,
                           "text_id": u["text_id"], "speaker_id": u.get("speaker_id", ""), "idx": str(i),
                           "tx": w, "mb": mb, "mp": "", "ge": ge, "gr": "", "mc": "", "ps": ps, "SyF": "",
                           "SyF_cover": "", "BOR": "", "CS": "", "gloss_conf": conf})
    return tokens


def run(train_derived, utterances_csv, out_dir, corpus="new"):
    utts = _read(utterances_csv)
    os.makedirs(out_dir, exist_ok=True)
    tokens = gloss_utterances(train_derived, utts, corpus)
    _write(os.path.join(out_dir, "tokens.csv"), tokens, TOKEN_COLS)
    texts = sorted({u["text_id"] for u in utts})
    _write(os.path.join(out_dir, "texts.csv"), [{"text_id": t, "has_SyF": "0", "genre": "", "source_collection": corpus}
                                                for t in texts], ("text_id", "has_SyF", "genre", "source_collection"))
    spk = sorted({u.get("speaker_id", "") for u in utts})
    _write(os.path.join(out_dir, "speakers.csv"), [{"speaker_id": s} for s in spk], ("speaker_id", "birth_lo", "birth_hi"))
    _write(os.path.join(out_dir, "utterances.csv"), utts, ("utt_id", "text_id", "speaker_id", "tx", "fe"))
    conf = {}
    for t in tokens:
        conf[t["gloss_conf"]] = conf.get(t["gloss_conf"], 0) + 1
    return {"utterances": len(utts), "words": len(tokens), "gloss_confidence": conf}


def main(argv):
    if len(argv) != 4:
        sys.exit(__doc__)
    train_derived, utts, model, out = argv
    print(run(train_derived, utts, out))
    import apply
    print(apply.build(model, out, os.path.join(out, "review"), "new", 0.9, 0.05, 0.1, "new-texts-1"))


if __name__ == "__main__":
    main(sys.argv[1:])
