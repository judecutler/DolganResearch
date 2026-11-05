"""Reading INEL morph strings and glosses.

Conventions (handoff 002, Q5): "-" separates suffixes and "=" clitics; "." joins
components of one gloss; a zero morph is written ".[X]" at the end of a gloss;
"%" marks an unsure gloss and "%%" an unknown one. "DAT/LOC" is one label.
"""
import re
from dataclasses import dataclass

from .config import CASE_LABELS, DERIVATIONAL_CASE_LIKE

_SPLIT = re.compile(r"([-=])")
_ZERO = re.compile(r"\.\[([^\]]*)\]")
PERSON = re.compile(r"^[123](SG|PL)$")


@dataclass(frozen=True)
class Morph:
    idx: int
    kind: str          # "stem", "suffix" or "clitic"
    text: str          # the piece as written


def split_morphs(s):
    """Split a morph or gloss string into pieces, keeping what joins each to the last."""
    if not s:
        return []
    parts = _SPLIT.split(s)
    out = [Morph(0, "stem", parts[0])]
    for i in range(1, len(parts), 2):
        out.append(Morph(len(out), "suffix" if parts[i] == "-" else "clitic", parts[i + 1]))
    return out


@dataclass(frozen=True)
class Gloss:
    raw: str
    overt: str               # the gloss without its zero-morph brackets and % marks
    zeros: tuple             # labels in ".[...]", e.g. ("NOM",) or ("IMP.2SG",)
    unsure: bool             # "%" prefix
    unknown: bool            # "%%"

    @property
    def components(self):
        return tuple(self.overt.split(".")) if self.overt else ()

    @property
    def zero_components(self):
        return tuple(c for z in self.zeros for c in z.split("."))

    @property
    def all_components(self):
        return self.components + self.zero_components

    @property
    def is_grammatical(self):
        """True for labels like PST1 or DAT/LOC; False for stems like human.being."""
        return bool(self.overt) and self.overt == self.overt.upper() and any(ch.isalpha() for ch in self.overt)


def parse_gloss(piece):
    unknown = "%%" in piece
    unsure = piece.startswith("%") and not unknown
    zeros = tuple(_ZERO.findall(piece))
    overt = _ZERO.sub("", piece).lstrip("%")
    return Gloss(piece, overt, zeros, unsure, unknown)


def glosses(ge):
    return [parse_gloss(m.text) for m in split_morphs(ge)]


@dataclass(frozen=True)
class CaseHit:
    morph_idx: int
    label: str        # shared label, e.g. "INS" for Dolgan INSTR
    raw: str          # label as written
    zero: bool


def case_hits(ge, corpus):
    """Every case marked in a word's gloss, overt or zero, in morph order."""
    table = CASE_LABELS[corpus]
    hits = []
    for i, g in enumerate(glosses(ge)):
        if g.overt in table:
            hits.append(CaseHit(i, table[g.overt], g.overt, False))
        else:
            comps = g.components
            for j, c in enumerate(comps):
                pair = ".".join(comps[j:j + 2])
                if pair in table and j + 1 < len(comps):
                    hits.append(CaseHit(i, table[pair], pair, False))
                    break
                if c in table and g.is_grammatical:
                    hits.append(CaseHit(i, table[c], c, False))
                    break
        if "NOM" in g.zero_components:
            hits.append(CaseHit(i, "NOM", ".[NOM]", True))
    return hits


def word_case(ge, corpus):
    """(case, flag). The word's case is the last case marked; flag notes oddities."""
    hits = case_hits(ge, corpus)
    if not hits:
        return None, ""
    labels = {h.label for h in hits}
    return hits[-1].label, ("multiple_cases" if len(labels) > 1 else "")


def has_component(ge, label, certain_only=False):
    """True if any morph gloss has `label` as a whole component (overt or zero).

    certain_only skips glosses marked "%" or "%%", as handoff 002 counted them.
    """
    return any(label in g.all_components for g in glosses(ge)
               if not (certain_only and (g.unsure or g.unknown)))


def grammatical_labels(ge):
    """Grammatical components of a word's gloss after the stem, overt and zero."""
    out = []
    for i, g in enumerate(glosses(ge)):
        if i > 0 and g.is_grammatical:
            out.extend(g.components)
        out.extend(g.zero_components)
    return out


def person_number(ge):
    """Possessive or person marking on a word, e.g. "3SG". None if absent."""
    found = [c for g in glosses(ge)[1:] for c in g.all_components if PERSON.match(c)]
    return found[-1] if found else None


def is_plural(ge):
    return any("PL" in g.all_components for g in glosses(ge)[1:])


def derivational_flags(ge, corpus):
    return [lab for lab in DERIVATIONAL_CASE_LIKE[corpus] if has_component(ge, lab)]


def stem_gloss(ge):
    gs = glosses(ge)
    return gs[0].overt if gs else ""


def looks_like_name(stem):
    """Capitalised lexical glosses are people, places or peoples (002, Q16)."""
    return bool(stem) and stem[0].isupper() and stem != stem.upper()


def annotation_items(value):
    """Split a SyF or SeR value into (form, function) items.

    One event can hold several items, e.g. "0.3.h:S v:pred" (a zero subject and
    the verb) or "0.3.h:Poss np.h:St" (002, Q9, Q10). A bare word such as "cop"
    attaches to the item before it. Items whose form starts with "0" are zero
    (unexpressed) arguments, not the word itself.
    """
    items = []
    for part in (value or "").split():
        if ":" in part:
            form, func = part.rsplit(":", 1)
            items.append([form, func])
        elif items:
            items[-1][1] += " " + part
    return [(f, fn) for f, fn in items]


def overt_functions(value):
    return [fn for f, fn in annotation_items(value) if not f.startswith("0")]
