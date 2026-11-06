import csv
import os
import random
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "case_change"))

import power  # noqa: E402
import speaker_test as st  # noqa: E402


class SpeakerTestTest(unittest.TestCase):
    def test_detects_a_strong_trend_and_not_a_null(self):
        rng = random.Random(3)
        design = [(1920 + 3 * i, 30) for i in range(20)]
        strong = st.simulate(design, 0.8, 1.5, 0.3, rng)
        self.assertLess(st.trend_test(strong, 499, rng)[1], 0.01)
        flat = [(b, 24, 30) for b, _ in design]
        self.assertGreater(st.trend_test(flat, 499, rng)[1], 0.5)

    def test_adjustment_removes_a_trend_that_genre_alone_explains(self):
        # Old speakers tell folklore, where the share is 0.5; everyone else 0.9, at any birth year.
        cells = []
        for i in range(8):
            cells.append((f"old{i}", 1890 + 3 * i, ("flk",), 20, 40))
            cells.append((f"new{i}", 1930 + 4 * i, ("nar",), 36, 40))
        for i in range(4):  # a few speakers with both genres keep time and genre apart
            cells.append((f"mix{i}", 1905 + 10 * i, ("flk",), 10, 20))
            cells.append((f"mix{i}", 1905 + 10 * i, ("nar",), 18, 20))
        rng = random.Random(1)
        self.assertLess(st.adjusted_test(cells, 499, rng, controls=False)[1], 0.01)
        slope, p = st.adjusted_test(cells, 499, rng, controls=True)
        self.assertAlmostEqual(slope, 0.0, places=6)
        self.assertGreater(p, 0.5)

    def test_redundant_controls_do_not_break_the_fit(self):
        # Genre "flk" and source "pub" pick out exactly the same objects.
        cells = [(f"s{i}", 1900 + 10 * i, ("flk", "pub") if i < 3 else ("nar", "arch"), 10 + i, 20)
                 for i in range(7)]
        slope, p = st.adjusted_test(cells, 99, random.Random(2))
        self.assertIsNotNone(p)

    def test_false_positive_rate_is_near_alpha(self):
        design = [(1920 + 3 * i, 20) for i in range(20)]
        self.assertLess(st.power(design, 0.8, 0.0, 0.5, n_sim=200, n_boot=99, seed=11), 0.09)

    def test_false_positive_rate_when_the_youngest_speakers_have_few_objects(self):
        # Handoff 003: in the real design the speakers with 4 to 8 objects are all born last.
        # Permuting birth years gave about 0.14 here; the wild bootstrap gives about 0.05.
        design = ([(1890 + 2 * i, 45) for i in range(4)] + [(1915 + 2 * i, 50) for i in range(14)]
                  + [(1965, 30), (1968, 25), (1975, 8), (1992, 4), (2003, 8)])
        fpr = st.power(design, 0.8, 0.0, 0.0, n_sim=300, n_boot=99, seed=5)
        self.assertLess(fpr, 0.09)
        self.assertGreater(fpr, 0.02)

    def test_power_design_reads_no_outcome(self):
        with tempfile.TemporaryDirectory() as t:
            path = os.path.join(t, "objects.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["speaker_id", "birth_lo", "birth_hi", "birth_mid"])
                w.writerows([["a", "1930", "1930", "1930"], ["a", "1930", "1930", "1930"],
                             ["b", "1950", "1950", "1950"], ["c", "1900", "1999", "1949.5"]])
            self.assertEqual(power.design_from(path), [(1930.0, 2), (1950.0, 1)])

    def test_design_reader_drops_the_outcome_column(self):
        with tempfile.TemporaryDirectory() as t:
            path = os.path.join(t, "objects.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["speaker_id", "birth_lo", "birth_hi", "birth_mid", "genre", "case"])
                w.writerow(["a", "1930", "1930", "1930", "nar", "ACC"])
            rows = power.read_design(path)
            self.assertNotIn("case", rows[0])
            self.assertNotIn("ACC", rows[0].values())
            out = os.path.join(t, "design.csv")
            power.main(["--export-design", path, out])
            with open(out, encoding="utf-8") as f:
                header = f.readline()
            self.assertNotIn("case", header.split(","))
            self.assertNotIn("ACC", open(out, encoding="utf-8").read())


class FreezeGateTest(unittest.TestCase):
    def test_b2_test_refuses_before_the_plan_is_frozen(self):
        import b2_test
        self.assertFalse(b2_test.plan_is_frozen())
        with self.assertRaises(SystemExit):
            b2_test.main(["unused.csv", "unused.md"])


def _tok(i, tx, ps, ge="", case="", syf="", ser=""):
    """A minimal SYNTH token row (all forms invented) for the extractor tests."""
    return {"token_id": f"T#1.w{i}", "utt_id": "T#1", "text_id": "T", "corpus": "dolgan", "speaker_id": "S1",
            "tx": tx, "ps": ps, "ge": ge, "case": case, "case_flag": "", "SyF": syf, "SeR": ser,
            "IST": "", "IST_cover": "", "BOR": "", "BOR_Morph": "", "align_ok": "true"}


class ExtractorReviewTest(unittest.TestCase):
    """Fixes for desktop's questions in handoff 003."""

    def test_object_predicate_must_be_verbal(self):
        import extract_objects
        words = [_tok(1, "verb1", "v", "see-PST", syf="v:pred"), _tok(2, "obj", "n", "fish-ACC", "ACC", "np:O"),
                 _tok(3, "adv1", "adv", "then", syf="adv:pred")]
        rows = extract_objects.objects(words, [], [], "dolgan")
        self.assertEqual(rows[0]["pred_token_id"], "T#1.w1")  # the verb before, not the adverb after
        self.assertEqual(rows[0]["pred_position"], "before")

    def test_copula_rule_stops_at_an_intervening_verb(self):
        import extract_b1
        adjacent = [_tok(1, "noun1", "n", "sorcerer-DAT/LOC", "DAT/LOC"), _tok(2, "cop1", "v", "be-PST")]
        blocked = [_tok(1, "noun1", "n", "sorcerer-DAT/LOC", "DAT/LOC"), _tok(2, "verb1", "v", "go-CVB"),
                   _tok(3, "cop1", "v", "be-PST")]
        self.assertEqual([r["rules"] for r in extract_b1.candidates(adjacent, [], [], [])], ["copula_next"])
        self.assertEqual(extract_b1.candidates(blocked, [], [], []), [])


class MultiWordTagTest(unittest.TestCase):
    """Handoff 006: multi-word BOR events must reach the words they cover."""

    def test_multi_word_bor_event_marks_the_object_as_a_loan(self):
        import build_tables
        import extract_objects
        from fixtures import write_corpus
        with tempfile.TemporaryDirectory() as t:
            raw = os.path.join(t, "raw")
            write_corpus(raw, "dolgan")
            out = os.path.join(t, "out")
            build_tables.build("dolgan", raw, out)
            rows = extract_objects.main(out, os.path.join(out, "o.csv"))
            obj = next(r for r in rows if r["stem"] == "icehole")
            self.assertEqual(obj["loan"], 1)
            self.assertEqual(obj["bor"], "RUS:core")


class ClauseTypeTest(unittest.TestCase):
    """Study C clause classification (STUDY_C_PLAN.md)."""

    def test_irrealis_wins_and_digits_are_stripped(self):
        import clause_dom
        self.assertEqual(clause_dom.clause_type("NEG IMP 2SG"), "irrealis")
        self.assertEqual(clause_dom.clause_type("COND1 3SG"), "irrealis")
        self.assertEqual(clause_dom.clause_type("DESID AOR 3SG"), "irrealis")
        self.assertEqual(clause_dom.clause_type("PST2 3SG"), "realis")
        self.assertEqual(clause_dom.clause_type("PTCP 3SG"), "other")
        self.assertEqual(clause_dom.clause_type(""), "")
        self.assertEqual(clause_dom.clause_type("PROB 3SG"), "other")
        self.assertEqual(clause_dom.clause_type("PROB 3SG", clause_dom.IRREALIS_EXTENDED), "irrealis")

    def test_odds_ratio_compares_clause_types(self):
        import clause_dom
        rows = ([{"pred_labels": "IMP 2SG", "_y": 1}] * 3 + [{"pred_labels": "IMP 2SG", "_y": 0}] * 1
                + [{"pred_labels": "PST 3SG", "_y": 1}] * 1 + [{"pred_labels": "PST 3SG", "_y": 0}] * 3)
        self.assertAlmostEqual(clause_dom.odds_ratio(rows), (3.5 / 1.5) / (1.5 / 3.5))
        self.assertIsNone(clause_dom.odds_ratio(rows[:4]))


class B1TestTest(unittest.TestCase):
    def test_exact_interval_matches_known_values(self):
        import b1_test
        lo, hi = b1_test.exact_interval(5, 10)
        self.assertAlmostEqual(lo, 0.1871, places=3)
        self.assertAlmostEqual(hi, 0.8129, places=3)
        self.assertAlmostEqual(b1_test.exact_interval(0, 10)[1], 0.3085, places=3)

    def test_resolved_column_overrides_the_two_codes(self):
        import b1_test
        self.assertTrue(b1_test.accepted({"is_secondary_predicate_A": "yes", "is_secondary_predicate_B": "yes"}))
        self.assertFalse(b1_test.accepted({"is_secondary_predicate_A": "yes", "is_secondary_predicate_B": "no"}))
        self.assertTrue(b1_test.accepted({"is_secondary_predicate_A": "yes", "is_secondary_predicate_B": "no",
                                          "resolved": "yes"}))

    def test_b1_refuses_before_the_plan_is_frozen(self):
        import b1_test
        with self.assertRaises(SystemExit):
            b1_test.main(["m.csv", "c.csv", "s.csv", "out.md"])


class CollinearTimeTest(unittest.TestCase):
    """Review 2026-11-06: a control that duplicates time must not be pruned away."""

    def test_control_identical_to_time_makes_time_unidentified(self):
        cells = [(f"o{i}", 1900, ("flk",), 10, 20) for i in range(6)] + \
                [(f"n{i}", 1960, ("nar",), 16, 20) for i in range(6)]
        self.assertEqual(st.collinearity(cells), 1.0)
        self.assertEqual(st.adjusted_test(cells, 99, random.Random(1)), (None, None))
        self.assertIsNotNone(st.adjusted_test(cells, 99, random.Random(1), controls=False)[1])

    def test_decision_rule_falls_back_to_genre_then_to_none(self):
        import b2_test

        def rows(src_tangled, genre_tangled):
            out = []
            for i in range(8):
                b = 1900 + 10 * i
                # Tangled: a new genre and source every two decades, which explains about 95% of birth year.
                genre = f"g{i // 2}" if genre_tangled else ("flk" if i % 2 else "nar")
                src = f"s{i // 2}" if src_tangled else ("pub" if i % 3 else "arch")
                for _ in range(5):
                    out.append({"speaker_id": f"s{i}", "birth_lo": str(b), "birth_hi": str(b), "case": "ACC",
                                "genre": genre, "source_collection": src})
            return out
        self.assertEqual(b2_test.choose_controls(rows(False, False))[0], b2_test.PRIMARY_CONTROLS)
        self.assertIsNone(b2_test.choose_controls(rows(True, True))[0])


class ReproducibleTest(unittest.TestCase):
    """Handoff 007: the design report changed with PYTHONHASHSEED."""

    def test_simulation_does_not_depend_on_the_hash_seed(self):
        import subprocess
        code = ("import sys; sys.path.insert(0, %r); import speaker_test as st; "
                "d = [('s%%d' %% i, 1900 + 7 * i, ('g%%d' %% (i %% 3),), 10 + i) for i in range(12)]; "
                "import random; print(st.simulate_cells(d, 0.5, 0.2, 2.0, random.Random(3)))") % os.path.join(os.path.dirname(os.path.dirname(HERE)), "case_change")
        outs = {subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                               env=dict(os.environ, PYTHONHASHSEED=h)).stdout for h in ("1", "2", "3")}
        self.assertEqual(len(outs), 1, outs)


if __name__ == "__main__":
    unittest.main()

