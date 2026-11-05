"""Synthetic INEL-style files for tests. NOT corpus data.

The XML layout copies what handoff 002 found in the real files (tier naming,
speaker attribute, shared timeline, `.[NOM]` zeros, `=` clitics). Word forms
marked REAL are copied from the excerpts in handoff/outputs/002/structure_report.md
(INEL Dolgan and Evenki Corpus 2.0, CC BY-NC-SA 4.0). Forms marked SYNTH are made
up to exercise a code path and must never be read as Dolgan or Evenki.
Speaker sigles, text ids and dates are made up.
"""
import os
from xml.sax.saxutils import escape, quoteattr

# Each word: tx, then tier values. Utterances group words; None = no ref (orphan words).
DOLGAN_SINGLE = {
    "text_id": "SpkA_1990_Test_flk",
    "genre": "flk",
    "speakers": ["SpkA"],
    "utterances": [
        ("SpkA", {"ref": "SpkA_1990_Test_flk.001", "fe": "free translation one"}, [
            {"tx": "ɨj", "mb": "ɨj", "mp": "ɨj", "ge": "moon.[NOM]", "mc": "n.[n:case]", "ps": "n"},  # REAL
            {"tx": "külüːge", "mb": "külüːg-e", "mp": "külük-tA", "ge": "shadow-3SG.[NOM]",
             "mc": "n-n:(poss).[n:case]", "ps": "n", "SyF": "np:S"},  # REAL
            {"tx": "ojbonu", "mb": "ojbon-u", "mp": "ojbon-nI", "ge": "icehole-ACC", "mc": "n-n:case",
             "ps": "n", "SyF": "np:O", "SeR": "np:Th"},  # REAL
            {"tx": "köstör,", "mb": "köst-ör", "mp": "köhün-Ar", "ge": "be.visible-PRS.[3SG]",
             "mc": "v-v:tense.[v:pred.pn]", "ps": "v", "SyF": "v:pred"},  # REAL
        ]),
        ("SpkA", {"ref": "SpkA_1990_Test_flk.002", "fe": "free translation two"}, [
            {"tx": "bɨraktaga", "mb": "bɨrak-tag-a", "mp": "bɨrak-TAK-tA", "ge": "throw-INFER-3SG",
             "mc": "v-v:mood-v:poss.pn", "ps": "v", "SyF": "0.3.h:S v:pred"},  # REAL
            {"tx": "eːt", "mb": "eːt", "mp": "eːt", "ge": "EVID", "mc": "ptcl", "ps": "ptcl"},  # REAL
            {"tx": "kellegej?", "mb": "kel-leg-e=j", "mp": "kel-TAK-tA=Ij", "ge": "come-INFER-3SG=Q",
             "mc": "v-v:mood-v:poss.pn-ptcl", "ps": "v"},  # REAL
            {"tx": "vsʼo"},  # REAL form (002 Q21), no analysis
        ]),
        ("SpkA", {"ref": "SpkA_1990_Test_flk.003", "fe": "free translation three"}, [
            {"tx": "keldek", "mb": "kel-dek", "mp": "kel-TAK", "ge": "come-COND1", "mc": "v-v:mood",
             "ps": "v", "SyF": "v:pred"},  # SYNTH
            {"tx": "kelbit", "mb": "kel-bit", "mp": "kel-BIT", "ge": "come-PST2.[3SG]",
             "mc": "v-v:tense.[v:pred.pn]", "ps": "v", "SyF": "v:pred"},  # SYNTH
            {"tx": "ebit", "mb": "e-bit", "mp": "e-BIT", "ge": "be-PST2.[3SG]",
             "mc": "v-v:tense.[v:pred.pn]", "ps": "cop"},  # SYNTH
        ]),
        (None, {}, [{"tx": "((laugh))"}]),
    ],
    # Two-word clause-level SyF event over words 1-2 of utterance 3 (002 Q9: "s:comp").
    "span_events": [("SpkA", 2, 0, 1, "SyF", "s:comp")],
}

DOLGAN_MULTI = {
    "text_id": "SpkB_SpkC_2009_Test_conv",
    "genre": "conv",
    "speakers": ["SpkB", "SpkC"],
    "utterances": [
        ("SpkB", {"ref": "SpkB_SpkC_2009_Test_conv.SpkB.001", "fe": "free translation B1"}, [
            {"tx": "vɨstavkalar", "mb": "vɨstavka-lar", "mp": "vɨstavka-LAr", "ge": "exhibition-PL.[NOM]",
             "mc": "n-n:(num)-n:case", "ps": "n", "SyF": "np:O", "BOR": "RUS:cult"},  # REAL form; mp, BOR SYNTH
            {"tx": "körbüt", "mb": "kör-büt", "mp": "kör-BIT", "ge": "see-PST2.[3SG]",
             "mc": "v-v:tense.[v:pred.pn]", "ps": "v", "SyF": "0.3.h:S v:pred"},  # SYNTH
        ]),
        ("SpkC", {"ref": "SpkB_SpkC_2009_Test_conv.SpkC.001", "fe": "free translation C1"}, [
            {"tx": "kihileri", "mb": "kihi-ler-i", "mp": "kihi-LAr-tI", "ge": "human.being-PL-ACC",
             "mc": "n-n:(num)-n:case", "ps": "n", "SyF": "np.h:O",
             "SeR": "0.3.h:Poss np.h:St"},  # REAL form; mp SYNTH
            {"tx": "ette", "mb": "et-te", "mp": "et-PART", "ge": "meat-PART", "mc": "n-n:case",
             "ps": "n", "SyF": "np:O"},  # SYNTH
            {"tx": "taːstaːk", "mb": "taːs-taːk", "mp": "taːs-LAːK", "ge": "stone-PROPR.[NOM]",
             "mc": "n-n>adj.[n:case]", "ps": "adj"},  # SYNTH
            {"tx": "aldʼatta", "mb": "aldʼat-t-a", "mp": "aldʼat-TI-tA", "ge": "break-PST1",
             "mc": "v-v:tense-v:pred.pn", "ps": "v", "SyF": "v:pred"},  # SYNTH, deliberately misaligned
        ]),
    ],
    "span_events": [],
}

EVENKI_SINGLE = {
    "text_id": "SpkE_2019_Test_flk",
    "genre": "flk",
    "speakers": ["SpkE"],
    "utterances": [
        ("SpkE", {"ref": "SpkE_2019_Test_flk.001", "fe": "free translation E1"}, [
            {"tx": "hiŋərəkoːr", "mb": "hiŋərə-koː-r", "mp": "hiŋərə-kəːn-l", "ge": "mouse-DIM1-PL.[NOM]",
             "mc": "n-n:(eval)-n:(num).[n:case]", "ps": "n", "SyF": "np:O"},  # REAL; mp SYNTH
            {"tx": "nuŋarwatin", "mb": "nuŋa-r-wa-tin", "mp": "nuŋan-l-wə-tin", "ge": "PRO.3-PL-ACC-3PL",
             "mc": "pers-n:(num)-n:case-n:poss", "ps": "pers", "SyF": "pro.h:O"},  # REAL; mp, mc SYNTH
            {"tx": "gorojoː", "mb": "goro-joː", "mp": "goro-jə", "ge": "long/distant-ACC.INDF",
             "mc": "adj-n:case", "ps": "adv", "SyF": "np:O"},  # REAL
            {"tx": "birkə.", "mb": "bi-rkə", "mp": "bi-rkə", "ge": "be-EVID.[3SG]",
             "mc": "v-v:mood2.[v:pn2]", "ps": "v", "SyF": "v:pred"},  # REAL
        ]),
    ],
    "span_events": [],
}


def exb_xml(spec):
    tli = []
    tiers = {}   # (speaker, category) -> list of (start, end, text)
    t = 0
    for spk, utt_tiers, words in spec["utterances"]:
        start = t
        for w in words:
            for cat, val in w.items():
                tiers.setdefault((spk, cat), []).append((t, t + 1, val))
            t += 1
        if spk is not None:
            for cat, val in utt_tiers.items():
                tiers.setdefault((spk, cat), []).append((start, t, val))
    for spk, utt_no, w0, w1, cat, val in spec["span_events"]:
        first = sum(len(u[2]) for u in spec["utterances"][:utt_no])
        tiers.setdefault((spk, cat), []).append((first + w0, first + w1 + 1, val))
    tli = [f'<tli id="T{i}" time="{i * 0.5:.1f}"/>' for i in range(t + 1)]

    multi = len(spec["speakers"]) > 1
    spk_xml = "".join(f'<speaker id={quoteattr(s)}><abbreviation>{s}</abbreviation><sex value="u"/></speaker>'
                      for s in spec["speakers"])
    tier_xml = []
    for (spk, cat), evs in tiers.items():
        if spk is None:
            spk = spec["speakers"][0]
        tid = f"{cat}-{spk}" if multi else cat
        typ = "t" if cat == "tx" else "a"
        ev = "".join(f'<event start="T{a}" end="T{b}">{escape(v)} </event>' for a, b, v in evs)
        tier_xml.append(f'<tier id={quoteattr(tid)} speaker={quoteattr(spk)} category={quoteattr(cat)} '
                        f'type="{typ}" display-name={quoteattr(tid)}>{ev}</tier>')
    tier_xml.append(f'<tier id="nt-x" speaker="{spec["speakers"][0]}" category="weird" type="a" display-name="nt-x"></tier>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<basic-transcription><head><meta-information>'
            f'<project-name>TEST</project-name><transcription-name>{spec["text_id"]}</transcription-name>'
            f'</meta-information><speakertable>{spk_xml}</speakertable></head><basic-body>'
            f'<common-timeline>{"".join(tli)}</common-timeline>{"".join(tier_xml)}</basic-body></basic-transcription>\n')


def coma_xml(speakers, comms):
    """speakers: list of (sigle, sex, birth). comms: list of (name, transcript_file, {key: value})."""
    sp = "".join(
        f'<Speaker Id="S{i}"><Sigle>{s}</Sigle><Pseudo>p{i}</Pseudo><KnownHuman>true</KnownHuman><Sex>{sex}</Sex>'
        f'<Description><Key Name="4 Date of birth">{escape(b)}</Key><Key Name="2a Given name">SECRET</Key>'
        f'<Key Name="2 Dialect">Upper</Key></Description></Speaker>'
        for i, (s, sex, b) in enumerate(speakers))
    co = "".join(
        f'<Communication Id="C{i}" Name="{n}"><Description>'
        + "".join(f'<Key Name={quoteattr(k)}>{escape(v)}</Key>' for k, v in keys.items())
        + f'</Description><Transcription Id="T{i}"><Name>{n}</Name><Filename>{f}</Filename></Transcription></Communication>'
        for i, (n, f, keys) in enumerate(comms))
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<Corpus><CorpusData>{co}{sp}</CorpusData></Corpus>\n'


DOLGAN_COMA = (
    [("SpkA", "f", "1935"), ("SpkB", "m", "1930/1940"), ("SpkC", "f", "1948.04.12."), ("SpkZ", "m", "1920s")],
    [("SpkA_1990_Test_flk", "SpkA_1990_Test_flk.exb",
      {"1 Genre": "flk", "2b Date of recording": "1990", "3 Dialect": "Upper", "2 Published in": "Some 2000 volume"}),
     ("SpkB_SpkC_2009_Test_conv", "SpkB_SpkC_2009_Test_conv.exb",
      {"1 Genre": "conv", "2b Date of recording": "2009", "3 Dialect": "Anabar", "1a Archive (sound)": "..."})],
)
EVENKI_COMA = (
    [("SpkE", "unknown", "...")],
    [("SpkE_2019_Test_flk", "SpkE_2019_Test_flk.exb",
      {"1 Genre": "flk", "2b Date of recording": "201X", "3b Dialect": "Sym", "3a Dialectal group": "Southern",
       "2 Source type": "INEL collection: audio"})],
)


def write_corpus(root, corpus):
    specs = {"dolgan": [DOLGAN_SINGLE, DOLGAN_MULTI], "evenki": [EVENKI_SINGLE]}[corpus]
    coma = {"dolgan": DOLGAN_COMA, "evenki": EVENKI_COMA}[corpus]
    for spec in specs:
        d = os.path.join(root, spec["genre"], spec["text_id"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, spec["text_id"] + ".exb"), "w", encoding="utf-8") as f:
            f.write(exb_xml(spec))
    with open(os.path.join(root, f"{corpus}.coma"), "w", encoding="utf-8") as f:
        f.write(coma_xml(*coma))
    return root
