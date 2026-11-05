"""Read one EXMARaLDA basic transcription (.exb) into words and utterances.

Structure (handoff 002, Q1 to Q4): one set of tiers per speaker; the speaker is
the tier's `speaker` attribute (tier ids drop the "-SIGLE" suffix in
single-speaker files, so ids are never used). Each word is one `tx` event; its
word-level annotations are events with the same start and end. Utterance tiers
(`ref`, `fe`, ...) span many words.
"""
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from .config import KNOWN_TIERS, SPAN_TIERS, UTTERANCE_TIERS, WORD_TIERS


@dataclass
class Word:
    speaker: str
    start: int          # timeline index
    end: int
    tx: str
    tiers: dict         # tier -> value of the event with exactly this span
    covering: dict      # span tier -> value of a multi-word event covering this word


@dataclass
class Utterance:
    speaker: str
    start: int
    end: int
    tiers: dict         # utterance tier -> value
    words: list = field(default_factory=list)


@dataclass
class Transcript:
    text_id: str
    path: str
    speakers: dict      # speaker id in the file (= .coma Sigle) -> abbreviation
    times: list         # timeline index -> seconds or None
    utterances: list
    orphan_words: list  # words inside no `ref` event
    unknown_tiers: set
    issues: list        # (kind, detail)


def _clean(s):
    return (s or "").strip()


def read_exb(path):
    root = ET.parse(path).getroot()
    tli = list(root.iter("tli"))
    index = {t.get("id"): i for i, t in enumerate(tli)}
    times = [float(t.get("time")) if t.get("time") else None for t in tli]

    # 002 matched the speaker `id` (not the abbreviation) to the .coma Sigle.
    speakers = {s.get("id"): _clean(s.findtext("abbreviation")) for s in root.iter("speaker")}

    issues = []
    unknown = set()
    by_speaker = {}
    for tier in root.iter("tier"):
        cat = tier.get("category")
        spk = tier.get("speaker")
        if cat not in KNOWN_TIERS:
            unknown.add(cat)
        events = by_speaker.setdefault(spk, {}).setdefault(cat, [])
        for e in tier.iter("event"):
            a, b = index.get(e.get("start")), index.get(e.get("end"))
            if a is None or b is None:
                issues.append(("bad_timeline_ref", f"{cat} {e.get('start')}-{e.get('end')}"))
                continue
            events.append((a, b, _clean(e.text)))

    utterances, orphans = [], []
    for spk, cats in by_speaker.items():
        u, o = _assemble(spk, cats, issues)
        utterances.extend(u)
        orphans.extend(o)
    utterances.sort(key=lambda u: (u.start, u.end, u.speaker))

    text_id = os.path.splitext(os.path.basename(path))[0]
    return Transcript(text_id, path, speakers, times, utterances, orphans, unknown, issues)


def _assemble(spk, cats, issues):
    exact = {cat: {(a, b): v for a, b, v in evs} for cat, evs in cats.items()}
    tx = sorted(cats.get("tx", []))
    word_spans = {(a, b) for a, b, _ in tx}

    for cat in WORD_TIERS:
        for span in exact.get(cat, {}):
            if span not in word_spans and cat not in SPAN_TIERS:
                issues.append(("word_tier_event_without_word", f"{spk} {cat} {span}"))

    multi = {cat: [(a, b, v) for a, b, v in cats.get(cat, []) if (a, b) not in word_spans]
             for cat in SPAN_TIERS}

    words = []
    for a, b, v in tx:
        tiers = {cat: exact[cat][(a, b)] for cat in WORD_TIERS if (a, b) in exact.get(cat, {})}
        covering = {}
        for cat, evs in multi.items():
            hits = [val for s, e, val in evs if s <= a and b <= e]
            if hits:
                covering[cat] = " | ".join(hits)
        words.append(Word(spk, a, b, v, tiers, covering))

    utts = []
    for a, b, v in sorted(cats.get("ref", [])):
        tiers = {"ref": v}
        for cat in UTTERANCE_TIERS:
            if cat != "ref" and (a, b) in exact.get(cat, {}):
                tiers[cat] = exact[cat][(a, b)]
        utts.append(Utterance(spk, a, b, tiers))

    orphans = []
    j = 0
    for w in words:
        while j < len(utts) and utts[j].end <= w.start:
            j += 1
        # 002's rule (wordlib.words): a word belongs to the ref whose span contains its start.
        if j < len(utts) and utts[j].start <= w.start < utts[j].end:
            utts[j].words.append(w)
        else:
            orphans.append(w)
    return utts, orphans
