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

    def test_false_positive_rate_is_near_alpha(self):
        design = [(1920 + 3 * i, 20) for i in range(20)]
        self.assertLess(st.power(design, 0.8, 0.0, 0.5, n_sim=200, n_perm=99, seed=11), 0.11)

    def test_power_design_reads_no_outcome(self):
        with tempfile.TemporaryDirectory() as t:
            path = os.path.join(t, "objects.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["speaker_id", "birth_lo", "birth_hi", "birth_mid"])
                w.writerows([["a", "1930", "1930", "1930"], ["a", "1930", "1930", "1930"],
                             ["b", "1950", "1950", "1950"], ["c", "1900", "1999", "1949.5"]])
            self.assertEqual(power.design_from(path), [(1930.0, 2), (1950.0, 1)])


class FreezeGateTest(unittest.TestCase):
    def test_b2_test_refuses_before_the_plan_is_frozen(self):
        import b2_test
        self.assertFalse(b2_test.plan_is_frozen())
        with self.assertRaises(SystemExit):
            b2_test.main(["unused.csv", "unused.md"])


if __name__ == "__main__":
    unittest.main()
