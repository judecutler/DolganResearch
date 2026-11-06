"""What the INEL Dolgan and Evenki 2.0 files contain, as found in handoff 002.

Every value here comes from `handoff/outputs/002/structure_report.md`. Change a
value only with evidence from the real files, and say where in the commit.
"""

WORD_TIERS = (
    "mb", "mp", "ge", "gg", "gr", "mc", "ps",
    "SyF", "SeR", "IST", "Top", "Foc",
    "BOR", "BOR-Phon", "BOR-Morph", "CS", "ExLocPoss",
)

# Annotation tiers whose events can span several words (report Q9: SyF "s:comp").
# BOR, BOR-Morph and ExLocPoss events can also span several words (handoff 006, 1,280 events).
SPAN_TIERS = ("SyF", "SeR", "IST", "Top", "Foc", "CS", "BOR", "BOR-Morph", "ExLocPoss")
COVER_TIERS = ("SyF", "SeR", "IST", "BOR", "BOR-Morph", "ExLocPoss")  # carried as <tier>_cover columns

UTTERANCE_TIERS = ("ref", "st", "stl", "ts", "fe", "fg", "fr", "ltr", "nt", "nto", "lte", "ltg")

KNOWN_TIERS = frozenset(("tx",) + WORD_TIERS + UTTERANCE_TIERS)

# Morph separators (Q5): "-" suffix boundary, "=" clitic boundary (Dolgan only).
MORPH_SEPARATORS = "-="

# Case labels as written in `ge`, mapped to one label set shared by both corpora.
# Zero nominative is never written as a label: it is ".[NOM]" on the last gloss (Q5, Q17).
CASE_LABELS = {
    "dolgan": {
        "ACC": "ACC", "PART": "PART", "DAT/LOC": "DAT/LOC", "ABL": "ABL",
        "INSTR": "INS", "GEN": "GEN", "COMP": "COMP",
    },
    "evenki": {
        "ACC": "ACC", "ACC.INDF": "ACC.INDF", "DAT/LOC": "DAT/LOC",
        "ABL": "ABL", "ABL2": "ABL", "ALL": "ALL", "LAT": "LAT", "LAT2": "LAT",
        "INS": "INS", "COM1": "COM", "COM2": "COM", "COM3": "COM", "COM4": "COM",
        "PROL": "PROL", "VOC": "VOC", "COMP": "COMP",
    },
}

# Labels that contain a case component but are listed apart from case in 002 (Q17).
NOT_CASE = {"dolgan": frozenset(), "evenki": frozenset({"LAT.ADV"})}

# Dolgan PROPR (proprietive) is derivational, not case. Carried as a flag.
DERIVATIONAL_CASE_LIKE = {"dolgan": ("PROPR",), "evenki": ()}

CORPORA = ("dolgan", "evenki")

# Real-data counts measured by desktop Claude in handoff 002. The build compares
# its own counts against these, so a run on the real corpus checks itself.
# "min" marks counts that 002 took only over words whose mc, mp and ge align
# (report Q18), so the full count can only be equal or larger.
EXPECTED_002 = {
    "dolgan": {
        "transcripts": 136,
        "speakers_in_exb_and_coma": 74,
        "speaker_ids_in_exb": 77,
        "tx_events": 97652,
        "ref_events": 14076,
        "words_with_mb": 93409,
        "words_mb_ge_mismatch": 0,
        "words_syf_ends_O": 1307,
        "syf_ends_O_ACC": 1056,
        "syf_ends_O_NOM": 216,
        "syf_ends_O_PART": 23,
        "ge_EVID": 53,
        "ge_INFER": 36,
        "mp_TAK_ge_COND1": (555, "min"),
        "ge_PST2": (2415, "min"),
        "ge_zero_NOM_morphs": 21167,
        "ge_ACC_morphs": 6608,
        "texts_with_SyF": 50,
    },
    "evenki": {
        "transcripts": 612,
        "speakers_in_exb_and_coma": 53,
        "speaker_ids_in_exb": 53,
        "tx_events": 93411,
        "ref_events": 19931,
        "words_with_mb": 92345,
        "words_mb_ge_mismatch": 0,
        "words_syf_ends_O": 1691,
        "ge_EVID": 28,
        "ge_zero_NOM_morphs": 28291,
        "ge_ACC_morphs": 5483,
        "texts_with_SyF": 131,
    },
}

# Documentation figures (D-016): reported, never used as pass/fail.
DOCUMENTED = {
    "dolgan": {"transcripts": 136, "speakers": 74, "utterances": 14193, "tokens": 97625},
    "evenki": {"transcripts": 612, "utterances": 19931, "tokens": 93264},
}

# `.coma` key names (Q11, Q12, Q15). Only these fields are ever read into tables.
COMA_SPEAKER_KEYS = {
    "birth": "4 Date of birth",
    "dialect": "2 Dialect",
    "l1": "1 First language",
    "l2": "1 Second language",
}
COMA_TEXT_KEYS = {
    "recording": "2b Date of recording",
    "genre": "1 Genre",
    "dialect_dolgan": "3 Dialect",
    "dialect_evenki": "3b Dialect",
    "dialect_group_evenki": "3a Dialectal group",
    "published": "2 Published in",
    "archive": "1a Archive (sound)",
    "source_type_evenki": "2 Source type",
    "has_audio_evenki": "6 Has audio",
}
UNKNOWN_VALUES = frozenset(("", "...", "…"))

# DRAFT, needs human sign-off (WP6). Clause TAM groups for Study B2, from the verb's
# gloss labels. The split follows Däbritz (2023: 196): "partitive-marked objects are
# closely connected to the imperative mood and prospective tense-aspect". Labels are
# the Dolgan ones seen in handoff 002 (Q18). First matching group wins, in this order.
TAM_GROUPS = (
    ("imperative", ("IMP",)),
    ("prospective", ("FUT", "PURP", "INTNS.FUT")),
    ("conditional", ("COND1", "COND2", "COND")),
    ("inferential", ("INFER",)),
    ("past", ("PST1", "PST2", "PST")),
    ("present_habitual", ("PRS", "HAB", "AOR")),
)
