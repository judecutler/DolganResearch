"""Read the corpus metadata file (.coma) and parse its date fields.

Speaker records hold names, family and residence data. Only the fields listed in
config.COMA_SPEAKER_KEYS are ever read out (decisions D-011, D-017).
"""
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from .config import COMA_SPEAKER_KEYS, COMA_TEXT_KEYS, UNKNOWN_VALUES


@dataclass(frozen=True)
class Year:
    """A year known exactly or only as a range."""
    lo: int
    hi: int
    precision: str      # "date", "year", "range", "decade", "century"
    uncertain: bool     # the source marks it with "?"

    @property
    def mid(self):
        return (self.lo + self.hi) / 2


_PATTERNS = (
    (re.compile(r"^(\d{4})\.\d{2}\.\d{2}\.?$"), lambda m: (int(m[1]), int(m[1]), "date")),
    (re.compile(r"^(\d{4})$"), lambda m: (int(m[1]), int(m[1]), "year")),
    (re.compile(r"^(\d{4})\s*[/-]\s*(\d{4})$"), lambda m: (int(m[1]), int(m[2]), "range")),
    (re.compile(r"^(\d{3})0s$"), lambda m: (int(m[1]) * 10, int(m[1]) * 10 + 9, "decade")),
    (re.compile(r"^(\d{3})X$"), lambda m: (int(m[1]) * 10, int(m[1]) * 10 + 9, "decade")),
    (re.compile(r"^(\d{2})XX$"), lambda m: (int(m[1]) * 100, int(m[1]) * 100 + 99, "century")),
)


def parse_year(raw):
    """Parse INEL date strings (002, Q11, Q12, Q15). None if unknown or unrecognised."""
    s = (raw or "").strip()
    if s in UNKNOWN_VALUES:
        return None
    uncertain = "?" in s
    s = re.sub(r"\s*\(\?\)\s*$|\s*\?\s*$", "", s).strip()
    for pat, make in _PATTERNS:
        m = pat.match(s)
        if m:
            lo, hi, precision = make(m)
            if lo > hi:
                return None
            return Year(lo, hi, precision, uncertain)
    return None


def _value(raw):
    v = (raw or "").strip()
    return None if v in UNKNOWN_VALUES else v


@dataclass(frozen=True)
class Speaker:
    sigle: str
    sex: str
    birth_raw: str
    birth: Year
    dialect: str
    l1: str
    l2: str


@dataclass(frozen=True)
class Communication:
    name: str
    transcripts: tuple      # transcription file basenames without extension
    keys: dict              # only the whitelisted keys

    def get(self, key):
        return _value(self.keys.get(COMA_TEXT_KEYS[key]))


def read_coma(path):
    root = ET.parse(path).getroot()
    speakers = {}
    for s in root.iter("Speaker"):
        sigle = (s.findtext("Sigle") or "").strip()
        keys = {}
        for k in s.iter("Key"):
            keys.setdefault(k.get("Name"), k.text)
        birth_raw = (keys.get(COMA_SPEAKER_KEYS["birth"]) or "").strip()
        speakers[sigle] = Speaker(
            sigle=sigle,
            sex=(s.findtext("Sex") or "").strip(),
            birth_raw=birth_raw,
            birth=parse_year(birth_raw),
            dialect=_value(keys.get(COMA_SPEAKER_KEYS["dialect"])),
            l1=_value(keys.get(COMA_SPEAKER_KEYS["l1"])),
            l2=_value(keys.get(COMA_SPEAKER_KEYS["l2"])),
        )

    wanted = set(COMA_TEXT_KEYS.values())
    comms = []
    for c in root.iter("Communication"):
        keys = {}
        for k in c.iter("Key"):
            if k.get("Name") in wanted:
                keys.setdefault(k.get("Name"), k.text)
        files = []
        for t in c.iter("Transcription"):
            fn = (t.findtext("Filename") or "").strip()
            if fn.lower().endswith(".exb"):
                files.append(os.path.splitext(os.path.basename(fn.replace("\\", "/")))[0])
        comms.append(Communication(c.get("Name") or "", tuple(files), keys))
    return speakers, comms


def communications_by_text(comms):
    """text_id -> Communication, matched on transcript file name, then on the name."""
    out = {}
    for c in comms:
        for t in c.transcripts:
            out.setdefault(t, c)
    for c in comms:
        out.setdefault(c.name, c)
    return out


def infer_dolgan_source(published, archive, year):
    """Source collection from three fields (002, Q13). An inference, not metadata."""
    tdnt = bool(archive) and "TDNT" in archive
    if tdnt:
        return "TDNT_archive"
    if year is None:
        return "unknown"
    if published and year.hi <= 1999:
        return "published_folklore"
    if not published and 2007 <= year.lo and year.hi <= 2010:
        return "fieldwork_2007_2010"
    if not published and year.lo == 2017:
        return "fieldwork_2017"
    return "unknown"
