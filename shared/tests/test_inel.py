import csv
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import fixtures  # noqa: E402
from build_tables import build  # noqa: E402
from inel import gloss  # noqa: E402
from inel.coma import Year, infer_dolgan_source, parse_year  # noqa: E402


def read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


class GlossTest(unittest.TestCase):
    def test_zero_nominative_is_a_case(self):
        self.assertEqual(gloss.word_case("exhibition-PL.[NOM]", "dolgan"), ("NOM", ""))

    def test_overt_cases_by_corpus(self):
        self.assertEqual(gloss.word_case("icehole-ACC", "dolgan")[0], "ACC")
        self.assertEqual(gloss.word_case("that-DAT/LOC", "evenki")[0], "DAT/LOC")
        self.assertEqual(gloss.word_case("long/distant-ACC.INDF", "evenki")[0], "ACC.INDF")
        self.assertEqual(gloss.word_case("PRO.3-PL-ACC-3PL", "evenki")[0], "ACC")
        self.assertEqual(gloss.word_case("PRO.1SG.ACC", "evenki")[0], "ACC")
        self.assertEqual(gloss.word_case("x-INSTR", "dolgan")[0], "INS")
        self.assertEqual(gloss.word_case("x-INS", "evenki")[0], "INS")

    def test_verbs_and_stems_have_no_case(self):
        self.assertEqual(gloss.word_case("be.visible-PRS.[3SG]", "dolgan"), (None, ""))
        self.assertEqual(gloss.word_case("human.being", "dolgan"), (None, ""))

    def test_clitic_split(self):
        kinds = [m.kind for m in gloss.split_morphs("kel-leg-e=j")]
        self.assertEqual(kinds, ["stem", "suffix", "suffix", "clitic"])

    def test_labels_and_person(self):
        self.assertTrue(gloss.has_component("be-EVID.[3SG]", "EVID"))
        self.assertTrue(gloss.has_component("x-%EVID", "EVID"))
        self.assertFalse(gloss.has_component("x-%EVID", "EVID", certain_only=True))
        self.assertEqual(gloss.person_number("clothes-PL-2PL-ACC"), "2PL")
        self.assertEqual(gloss.grammatical_labels("come-PST2.[3SG]"), ["PST2", "3SG"])
        self.assertTrue(gloss.is_plural("human.being-PL-ACC"))
        self.assertTrue(gloss.looks_like_name("Anys"))
        self.assertFalse(gloss.looks_like_name("EVID"))


class YearTest(unittest.TestCase):
    def test_formats_seen_in_002(self):
        self.assertEqual(parse_year("1935"), Year(1935, 1935, "year", False))
        self.assertEqual(parse_year("1930/1935"), Year(1930, 1935, "range", False))
        self.assertEqual(parse_year("1912-1913"), Year(1912, 1913, "range", False))
        self.assertEqual(parse_year("1948.04.12."), Year(1948, 1948, "date", False))
        self.assertEqual(parse_year("1948.04.12"), Year(1948, 1948, "date", False))
        self.assertEqual(parse_year("1920s"), Year(1920, 1929, "decade", False))
        self.assertEqual(parse_year("1910s (?)"), Year(1910, 1919, "decade", True))
        self.assertEqual(parse_year("199X"), Year(1990, 1999, "decade", False))
        self.assertEqual(parse_year("19XX"), Year(1900, 1999, "century", False))

    def test_unknown(self):
        for raw in ("...", "", None, "about then"):
            self.assertIsNone(parse_year(raw))

    def test_source_inference(self):
        y = parse_year
        self.assertEqual(infer_dolgan_source("Efremov 2000", None, y("1964")), "published_folklore")
        self.assertEqual(infer_dolgan_source(None, "TDNT 12", y("199X")), "TDNT_archive")
        self.assertEqual(infer_dolgan_source(None, None, y("2009")), "fieldwork_2007_2010")
        self.assertEqual(infer_dolgan_source(None, None, y("2017")), "fieldwork_2017")
        self.assertEqual(infer_dolgan_source(None, None, y("1990")), "unknown")


class BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = {}
        for corpus in ("dolgan", "evenki"):
            raw = fixtures.write_corpus(os.path.join(cls.tmp.name, "raw", corpus), corpus)
            out = os.path.join(cls.tmp.name, "out", corpus)
            build(corpus, raw, out)
            cls.out[corpus] = out

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def table(self, corpus, name):
        return read(os.path.join(self.out[corpus], name + ".csv"))

    def counts(self, corpus):
        with open(os.path.join(self.out[corpus], "counts.json"), encoding="utf-8") as f:
            return json.load(f)["counts"]

    def test_every_tx_event_is_a_token(self):
        self.assertEqual(len(self.table("dolgan", "tokens")), 18)
        self.assertEqual(self.counts("dolgan")["ref_events"], 5)

    def test_speaker_comes_from_attribute_in_single_and_multi_files(self):
        toks = self.table("dolgan", "tokens")
        by_id = {t["token_id"]: t["speaker_id"] for t in toks}
        self.assertEqual(by_id["SpkA_1990_Test_flk#001.w01"], "SpkA")
        self.assertEqual(by_id["SpkB_SpkC_2009_Test_conv#002.w01"], "SpkC")

    def test_word_tiers_align_by_span(self):
        t = {r["token_id"]: r for r in self.table("dolgan", "tokens")}
        w = t["SpkA_1990_Test_flk#001.w03"]
        self.assertEqual((w["tx"], w["ge"], w["SyF"], w["SeR"], w["case"]),
                         ("ojbonu", "icehole-ACC", "np:O", "np:Th", "ACC"))
        self.assertEqual(t["SpkA_1990_Test_flk#003.w01"]["SyF_cover"], "s:comp")
        self.assertEqual(t["SpkA_1990_Test_flk#003.w03"]["SyF_cover"], "")

    def test_misaligned_word_is_kept_and_flagged(self):
        t = {r["token_id"]: r for r in self.table("dolgan", "tokens")}
        self.assertEqual(t["SpkB_SpkC_2009_Test_conv#002.w04"]["align_ok"], "false")
        flags = {(q["token_id"], q["flag"]) for q in self.table("dolgan", "qa_flags")}
        self.assertIn(("SpkB_SpkC_2009_Test_conv#002.w04", "morph_gloss_mismatch"), flags)
        self.assertIn(("SpkA_1990_Test_flk#orphan.w01", "word_outside_utterance"), flags)
        self.assertIn(("", "unknown_tier"), {(q["token_id"], q["flag"]) for q in self.table("dolgan", "qa_flags")})

    def test_unanalysed_word_has_empty_alignment(self):
        t = {r["tx"]: r for r in self.table("dolgan", "tokens")}
        self.assertEqual((t["vsʼo"]["align_ok"], t["vsʼo"]["n_morphs"]), ("", "0"))

    def test_morphemes_carry_clitics_and_zeros(self):
        m = [r for r in self.table("dolgan", "morphemes") if r["token_id"] == "SpkA_1990_Test_flk#002.w03"]
        self.assertEqual([r["kind"] for r in m], ["stem", "suffix", "suffix", "clitic"])
        self.assertEqual(m[2]["form_underlying"], "tA")
        z = [r for r in self.table("dolgan", "morphemes") if r["token_id"] == "SpkA_1990_Test_flk#001.w02"]
        self.assertEqual((z[1]["gloss_overt"], z[1]["gloss_zero"]), ("3SG", "NOM"))

    def test_metadata_is_joined_and_private_fields_never_leave_the_coma(self):
        texts = {r["text_id"]: r for r in self.table("dolgan", "texts")}
        self.assertEqual(texts["SpkB_SpkC_2009_Test_conv"]["dialect"], "Anabar")
        self.assertEqual(texts["SpkA_1990_Test_flk"]["source_collection"], "published_folklore")
        spk = {r["speaker_id"]: r for r in self.table("dolgan", "speakers")}
        self.assertEqual((spk["SpkB"]["birth_lo"], spk["SpkB"]["birth_hi"]), ("1930", "1940"))
        self.assertEqual(spk["SpkC"]["birth_precision"], "date")
        for name in os.listdir(self.out["dolgan"]):
            with open(os.path.join(self.out["dolgan"], name), encoding="utf-8") as f:
                body = f.read()
            self.assertNotIn("SECRET", body, name)
            self.assertNotIn("04.12", body, name)

    def test_counts_used_for_reconciliation(self):
        c = self.counts("dolgan")
        self.assertEqual((c["words_syf_ends_O"], c["syf_ends_O_ACC"], c["syf_ends_O_NOM"], c["syf_ends_O_PART"]),
                         (4, 2, 1, 1))
        self.assertEqual((c["ge_EVID"], c["ge_INFER"], c["mp_TAK_ge_COND1"], c["ge_PST2"]), (1, 2, 1, 3))
        e = self.counts("evenki")
        self.assertEqual((e["ge_EVID"], e["words_syf_ends_O"], e["speakers_with_birth_year"]), (1, 3, 0))


if __name__ == "__main__":
    unittest.main()
