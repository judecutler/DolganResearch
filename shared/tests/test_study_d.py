"""Study D (case_change/russian_shift.py) on SYNTH tokens. All forms and glosses are invented."""
import os
import random
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "case_change"))

import russian_shift as rs  # noqa: E402

BASE = {"text_id": "T1", "genre": "nar", "source_collection": "src", "recording_lo": "2000",
        "recording_hi": "2000", "birth_lo": "1950", "birth_hi": "1950", "speaker_id": "S1",
        "SyF": "", "ps": "", "ge": "", "BOR": "", "CS": "", "mc": ""}


def tok(**kw):
    return dict(BASE, **kw)


class UnitRulesTest(unittest.TestCase):
    def test_d1_counts_pronoun_and_zero_subjects_only(self):
        toks = [tok(SyF="pro.h:S", ps="pers"), tok(SyF="0.1.h:S v:pred", ps="v"),
                tok(SyF="np.h:S", ps="n"), tok(SyF="pro.h:S", ps="dempro"), tok(SyF="np:O", ps="n"),
                tok(SyF="pro:O", ps="pers")]
        self.assertEqual([u["y"] for u in rs.d1_units(toks)], [1, 0])

    def test_d2_finite_pasts_only(self):
        toks = [tok(ge="go-PST2-3SG"), tok(ge="go-PST1-3SG"), tok(ge="go-PST2-PTCP"), tok(ge="go-PRS-3SG")]
        self.assertEqual([u["y"] for u in rs.d2_units(toks)], [1, 0])

    def test_d3_converbs_among_lexical_verbs(self):
        toks = [tok(ps="v", ge="go-CVB.SEQ"), tok(ps="v", ge="go-PST1-3SG"), tok(ps="aux", ge="be-CVB.SEQ"),
                tok(ps="n", ge="house-NOM")]
        self.assertEqual([u["y"] for u in rs.d3_units(toks)], [1, 0])

    def test_pc_russian_words(self):
        toks = [tok(ge="x", BOR="RUS:cult"), tok(ge="x", BOR="%RUS:core"), tok(ge="x", CS="RUS:ext"),
                tok(ge="x", BOR="MONG:core"), tok(ge="x"), tok(ge="", BOR="RUS:cult")]
        self.assertEqual([u["y"] for u in rs.pc_units(toks)], [1, 1, 1, 0, 0])

    def test_attach_brings_text_and_speaker_fields(self):
        t = rs.attach([{"text_id": "A", "speaker_id": "X"}],
                      [{"text_id": "A", "genre": "conv", "source_collection": "fw", "recording_lo": "1990",
                        "recording_hi": "1991"}],
                      [{"speaker_id": "X", "birth_lo": "1930", "birth_hi": "1930"}])[0]
        self.assertEqual((t["genre"], t["source_collection"], t["birth_lo"], t["recording_hi"]),
                         ("conv", "fw", "1930", "1991"))


class HolmTest(unittest.TestCase):
    def test_holm(self):
        self.assertEqual([round(x, 3) for x in rs.holm([0.01, 0.04, 0.03])], [0.03, 0.06, 0.06])
        self.assertEqual(rs.holm([None, 0.02]), [None, 0.02])


class AnalyseTest(unittest.TestCase):
    """A strong invented trend in converbs is found; no trend in the others is found."""

    def test_end_to_end(self):
        rng = random.Random(3)
        toks = []
        for s in range(12):
            birth = 1900 + 8 * s
            for i in range(120):
                genre = ("nar", "conv", "flk")[(s + i) % 3]
                src = ("a", "b")[s % 2]
                b = dict(BASE, speaker_id=f"S{s}", birth_lo=str(birth), birth_hi=str(birth), genre=genre,
                         source_collection=src, recording_lo=str(birth + 60), recording_hi=str(birth + 60))
                p_cvb = 0.6 - 0.05 * s
                toks.append(dict(b, ps="v", ge="go-CVB.SEQ" if rng.random() < p_cvb else "go-PST1-3SG"))
                toks.append(dict(b, ps="v", ge="go-PST2-3SG" if rng.random() < 0.5 else "go-PST1-3SG"))
                toks.append(dict(b, ps="n", ge="x", BOR="RUS:cult" if rng.random() < 0.1 else ""))
                toks.append(dict(b, ps="pers", SyF="pro.h:S") if rng.random() < 0.3
                            else dict(b, ps="v", SyF="0.1.h:S v:pred", ge="go-PRS-1SG"))
        res = rs.analyse(toks, n_boot=199, seed=1)
        self.assertLess(res["D3"]["primary"][2], 0)
        self.assertLess(res["D3"]["holm"], 0.05)
        self.assertGreater(res["D1"]["holm"], 0.05)
        self.assertTrue(res["D3"]["loo"])
        self.assertIn("Holm", "\n".join(rs.report(res, 199)))


if __name__ == "__main__":
    unittest.main()
