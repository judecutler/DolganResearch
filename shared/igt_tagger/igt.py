"""Language-general reading of interlinear glossed text (IGT) for the argument tagger.

Input is one row per word with at least: utt_id, idx, ps (part of speech), ge (English
gloss line, Leipzig-style: lemma-SUFFIX.SUFFIX, zero morphs in brackets like [NOM]).
Optional: SyF (INEL syntactic function tags, used only as training labels).

Nothing here is specific to Dolgan. The gloss conventions are the Leipzig Glossing Rules
as used by INEL, so any corpus glossed that way (INEL Evenki, Selkup, Kamas, Nganasan,
DoReCo, IMTVault ...) can be read without changes. Language-specific gloss labels can be
mapped onto the universal ones in ALIASES.
"""
import re

# Universal case labels. Aliases map other spellings onto them.
CASES = {"NOM", "ACC", "GEN", "DAT", "LOC", "DAT/LOC", "ABL", "INSTR", "COM", "ALL", "LAT", "PROL",
         "PART", "COMP", "PROPR", "CAR", "ERG", "ABS", "OBL", "VOC", "ESS", "TRANSL", "EQU", "ELAT",
         "ILL", "INESS", "SOC"}
ALIASES = {"INS": "INSTR", "PRT": "PART", "ACC.INDF": "ACC"}
FINITE_TAM = {"PST", "PRS", "FUT", "AOR", "NFUT", "IMP", "COND", "HAB", "IPFV", "PFV", "PRF", "SBJV", "OPT",
              "NEC", "DEB", "INFER", "EVID", "JUSS", "HORT", "PROB", "POT", "IMM"}
NONFINITE = ("PTCP", "CVB", "INF", "NMLZ", "SUP", "PURP")
PERSON = re.compile(r"^([123])(SG|PL|DU)?$")
NOMINAL_PS = {"n", "pers", "dempro", "propr", "emphpro", "indfpro", "posspr", "que", "quant", "cardnum",
              "adj", "pro", "np", "collnum", "ordnum"}
VERBAL_PS = {"v", "aux", "cop"}
PRONOUN_LEMMA_PERSON = {"i": "1", "we": "1", "me": "1", "us": "1", "you": "2", "thou": "2",
                        "he": "3", "she": "3", "it": "3", "they": "3", "him": "3", "her": "3", "them": "3"}


def _norm(tag):
    tag = tag.strip("[]")
    tag = re.sub(r"(?<=[A-Z])\d+$", "", tag)  # COND1 -> COND, COM1 -> COM, EMPH13 -> EMPH
    return ALIASES.get(tag, tag)


def parse_gloss(ge):
    """{'lemma', 'tags' (normalised grammatical labels), 'zero' (labels in brackets), 'n_morphs'}."""
    ge = (ge or "").strip()
    if not ge:
        return {"lemma": "", "tags": [], "zero": set(), "n_morphs": 0}
    morphs = [m for m in re.split(r"[-=]", ge) if m]
    lemma_parts = []
    tags, zero = [], set()
    for i, m in enumerate(morphs):
        for sub in m.split("."):
            if not sub:
                continue
            is_zero = sub.startswith("[") or sub.endswith("]")
            core = sub.strip("[]")
            if core and (core.isupper() or PERSON.match(core)):
                t = _norm(core)
                tags.append(t)
                if is_zero:
                    zero.add(t)
            elif i == 0 and core:
                lemma_parts.append(core.lower())
    return {"lemma": ".".join(lemma_parts), "tags": tags, "zero": zero, "n_morphs": len(morphs)}


def case_of(tags):
    """The last case label (case is word-final in suffixing languages); None if none."""
    for t in reversed(tags):
        if t in CASES:
            return t
    return None


def person_of(g):
    for t in reversed(g["tags"]):
        m = PERSON.match(t)
        if m:
            return m.group(1)
    return None


def finiteness(tags):
    if any(t in NONFINITE for t in tags):
        return next(t for t in tags if t in NONFINITE)
    if any(t in FINITE_TAM for t in tags):
        return "finite"
    return "none"


def labels(syf):
    """Training labels from an INEL SyF value: role S/O/-, pred yes/no, zero-subject person."""
    role, pred, zero = "-", "-", "-"
    for item in (syf or "").split():
        form, _, func = item.partition(":")
        if func == "S" and form.startswith("0"):
            p = form.split(".")[1] if "." in form else "x"
            zero = "0." + (p if p in ("1", "2", "3") else "x")
        elif form.startswith("0"):
            continue  # zero object (e.g. 0.3:O) sits on the verb: not an overt argument
        elif func in ("S", "O") and role == "-":
            role = func
        elif func == "pred" or form == "cop":
            pred = "pred"
    return role, pred, zero


def group_utterances(rows):
    """[(utt_id, [rows in idx order])], keeping first-seen utterance order."""
    out, by = [], {}
    for r in rows:
        u = r["utt_id"]
        if u not in by:
            by[u] = []
            out.append((u, by[u]))
        by[u].append(r)
    for _, toks in out:
        toks.sort(key=lambda r: int(r.get("idx") or 0))
    return out
