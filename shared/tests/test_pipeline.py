import csv
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, os.path.join(ROOT, "shared"), os.path.join(ROOT, "case_change")]

import fixtures  # noqa: E402
import run_all  # noqa: E402
import workbook  # noqa: E402
from inel import gloss, xlsx  # noqa: E402
from qa_report import check  # noqa: E402


def read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


class PipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        t = cls.tmp.name
        for c in ("dolgan", "evenki"):
            fixtures.write_corpus(os.path.join(t, "raw", f"{c}-2.0"), c)
        cls.exit = run_all.main(["--raw-root", os.path.join(t, "raw"), "--derived", os.path.join(t, "derived"),
                                 "--reports", os.path.join(t, "reports"), "--pilot-n", "4"])
        cls.d = os.path.join(t, "derived")
        cls.r = os.path.join(t, "reports")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_fixture_counts_differ_from_real_corpus_so_run_fails(self):
        self.assertEqual(self.exit, 1)
        with open(os.path.join(self.r, "qa_report.md"), encoding="utf-8") as f:
            self.assertIn("DIFF", f.read())

    def test_objects_have_case_speaker_and_predicate(self):
        objs = {o["token_id"]: o for o in read(os.path.join(self.d, "dolgan", "objects.csv"))}
        o = objs["SpkB_SpkC_2009_Test_conv#002.w01"]
        self.assertEqual((o["case"], o["human"], o["plural"], o["speaker_id"], o["birth_mid"]),
                         ("ACC", "1", "1", "SpkC", "1948.0"))
        self.assertEqual((o["pred_token_id"], o["pred_labels"], o["pred_position"]),
                         ("SpkB_SpkC_2009_Test_conv#002.w04", "PST1", "after"))
        self.assertEqual(objs["SpkB_SpkC_2009_Test_conv#001.w01"]["loan"], "1")
        self.assertEqual(objs["SpkB_SpkC_2009_Test_conv#002.w02"]["case"], "PART")
        self.assertEqual(len(objs), 4)

    def test_evenki_objects_use_evenki_labels(self):
        cases = sorted(o["case"] for o in read(os.path.join(self.d, "evenki", "objects.csv")))
        self.assertEqual(cases, ["ACC", "ACC.INDF", "NOM"])

    def test_candidates_record_the_rule(self):
        c = {x["tx"]: x for x in read(os.path.join(self.d, "dolgan", "evid_candidates.csv"))}
        self.assertEqual((c["eːt"]["tier"], c["eːt"]["rules"]), ("1", "ge_EVID"))
        self.assertEqual((c["keldek"]["rules"], c["keldek"]["target_morph"]), ("mp_TAK_not_INFER", "TAK"))
        self.assertEqual(c["ebit"]["rules"], "copula_BIT")
        self.assertIn("[[eːt]]", c["eːt"]["context"])
        self.assertNotIn("köstör,", c)

    def test_b1_candidates_follow_siegl_patterns(self):
        b1 = {c["tx"]: c for c in read(os.path.join(self.d, "dolgan", "b1_candidates.csv"))}
        self.assertEqual(b1["aptaːga"]["rules"], "copula_next")
        self.assertEqual(b1["vospitatelʼinnan"]["rules"], "ins_nominal")
        self.assertNotIn("dʼi͡ege", b1)

    def test_gate0_hides_outcomes_by_cohort(self):
        with open(os.path.join(self.r, "gate0_feasibility.md"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("At least 15 speakers", text)
        for case in ("ACC", "PART"):
            self.assertNotIn(f"| {case} |", text.split("### Study B1")[0])

    def test_pilot_sheets_are_identical_and_complete(self):
        wb = os.path.join(self.d, "workbooks")
        a, b = (xlsx.read(os.path.join(wb, f"pilot_sheet_{s}.xlsx")) for s in "AB")
        self.assertEqual([r["item_id"] for r in a], [r["item_id"] for r in b])
        self.assertEqual(len(a), 4)
        self.assertIn("is_evidential_use", a[0])
        self.assertNotIn("rules", a[0])
        b1 = xlsx.read(os.path.join(wb, "b1_sheet_A.xlsx"))
        self.assertEqual(len(b1), 2)
        self.assertIn("is_secondary_predicate", b1[0])


class WorkbookTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = self.tmp.name
        self.cands = os.path.join(t, "c.csv")
        cols = ["token_id", "utt_id", "text_id", "corpus", "speaker_id", "tier", "rules", "tx", "genre",
                "source_collection", "birth_mid", "recording_lo", "recording_hi", "context", "gloss_line", "fe"]
        rows = [dict(zip(cols, [f"t{i}", "u", "x", "dolgan", f"s{i % 5}", "2", "mp_BIT", "w", "nar", "src",
                                "1950.0", "2009", "2009", "ctx", "gl", "fe"])) for i in range(100)]
        rows += [dict(zip(cols, [f"e{i}", "u", "x", "dolgan", "s0", "1", "ge_EVID", "w", "nar", "src", "",
                                 "", "", "ctx", "gl", "fe"])) for i in range(10)]
        with open(self.cands, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)

    def tearDown(self):
        self.tmp.cleanup()

    def test_sampling_keeps_tier1_caps_tier2_and_spreads_speakers(self):
        key = workbook.build("main", self.tmp.name, [self.cands], per_rule=20)
        self.assertEqual(sum(k["tier"] == "1" for k in key), 10)
        self.assertEqual(sum(k["tier"] == "2" for k in key), 20)
        again = workbook.build("main", self.tmp.name, [self.cands], per_rule=20)
        self.assertEqual(key, again)
        self.assertEqual(sum(k["overlap"] for k in key), round(30 * 0.15))

    def test_merge_rejects_values_outside_codebook_and_computes_kappa(self):
        key = workbook.build("main", self.tmp.name, [self.cands], per_rule=20)
        for s, value in (("A", "yes"), ("B", "yes")):
            path = os.path.join(self.tmp.name, f"main_sheet_{s}.xlsx")
            rows = xlsx.read(path)
            for i, r in enumerate(rows):
                r["is_evidential_use"] = value if i % 2 else "no"
            rows[0]["person"] = "4"
            header = list(rows[0])
            xlsx.write(path, header, rows)
        errors = workbook.merge(os.path.join(self.tmp.name, "main_key.csv"),
                                os.path.join(self.tmp.name, "main_sheet_A.xlsx"),
                                os.path.join(self.tmp.name, "main_sheet_B.xlsx"),
                                os.path.join(self.tmp.name, "m"))
        self.assertTrue(any("person='4'" in e for e in errors))
        merged = read(os.path.join(self.tmp.name, "m_merged.csv"))
        self.assertEqual(len(merged), len(key))

    def test_kappa(self):
        self.assertAlmostEqual(workbook.kappa([("a", "a"), ("b", "b"), ("a", "b"), ("b", "a")]), 0.0)
        self.assertAlmostEqual(workbook.kappa([("a", "a"), ("b", "b")]), 1.0)
        self.assertIsNone(workbook.kappa([("a", "a"), ("a", "a")]))
        self.assertIsNone(workbook.kappa([]))


class QaCheckTest(unittest.TestCase):
    def test_missing_count_is_inconclusive_and_min_checks_are_lower_bounds(self):
        rows = {r[0]: r[3] for r in check({"a": 5, "b": 7}, {"a": 5, "b": (6, "min"), "c": 1})}
        self.assertEqual(rows, {"a": "MATCH", "b": "MATCH", "c": "INCONCLUSIVE"})
        self.assertEqual(check({"b": 5}, {"b": (6, "min")})[0][3], "DIFF")


class AnnotationItemsTest(unittest.TestCase):
    def test_items(self):
        self.assertEqual(gloss.annotation_items("0.3.h:S v:pred"), [("0.3.h", "S"), ("v", "pred")])
        self.assertEqual(gloss.overt_functions("0.3.h:S v:pred"), ["pred"])
        self.assertEqual(gloss.annotation_items("np:S cop"), [("np", "S cop")])
        self.assertEqual(gloss.overt_functions(""), [])


if __name__ == "__main__":
    unittest.main()
