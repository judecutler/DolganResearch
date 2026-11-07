"""IGT argument tagger on SYNTH data. Every form, gloss and label here is invented."""
import csv
import json
import os
import random
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "igt_tagger"))

from igt import case_of, labels, parse_gloss  # noqa: E402
from features import utterance_features  # noqa: E402
from profiles import augment, estimate, type_key  # noqa: E402
from merge_review import kappa  # noqa: E402

try:
    import sklearn  # noqa: F401
    HAVE_SK = True
except ImportError:
    HAVE_SK = False

NOUNS = ["man", "woman", "dog", "reindeer", "child"]
THINGS = ["fish", "meat", "sledge", "tent", "net"]
TRANS = ["eat", "take", "see", "make"]
INTRANS = ["go", "sleep", "come"]


def synth_corpus(root, n_tagged=12, n_untagged=4, seed=1):
    """A toy SOV, suffixing, nominative-accusative language with INEL-style tiers."""
    rng = random.Random(seed)
    os.makedirs(root, exist_ok=True)
    toks, texts, utts = [], [], []
    for t in range(n_tagged + n_untagged):
        tid = f"T{t}"
        tagged = t < n_tagged
        texts.append({"text_id": tid, "has_SyF": "1" if tagged else "0", "genre": "nar",
                      "source_collection": "synth"})
        for u in range(25):
            uid = f"{tid}#{u}"
            words = []
            if rng.random() < 0.6:
                words.append(("n", rng.choice(NOUNS) + ".[NOM]", "np.h:S"))
                obj_case = "ACC" if rng.random() < 0.7 else "[NOM]"
                words.append(("n", rng.choice(THINGS) + ("-ACC" if obj_case == "ACC" else ".[NOM]"), "np:O"))
                words.append(("v", rng.choice(TRANS) + "-PST-3SG", "v:pred"))
            else:
                words.append(("n", rng.choice(NOUNS) + ".[NOM]", "np.h:S"))
                if rng.random() < 0.5:
                    words.append(("n", "house-DAT", ""))
                words.append(("v", rng.choice(INTRANS) + "-PST-3SG", "v:pred"))
            if rng.random() < 0.2:  # dropped subject
                words = [w for w in words if w[2] != "np.h:S"]
                words = [(ps, ge, ("0.3.h:S v:pred" if syf == "v:pred" else syf)) for ps, ge, syf in words]
            for i, (ps, ge, syf) in enumerate(words, 1):
                toks.append({"token_id": f"{uid}.{i}", "utt_id": uid, "text_id": tid, "speaker_id": f"SP{t % 5}",
                             "idx": str(i), "tx": ge.split("-")[0].split(".")[0], "ge": ge, "mb": ge.lower(), "ps": ps,
                             "SyF": syf if tagged else "", "SyF_cover": ""})
            utts.append({"utt_id": uid, "fe": "synthetic translation"})
    speakers = [{"speaker_id": f"SP{i}", "birth_lo": str(1920 + 10 * i), "birth_hi": str(1920 + 10 * i)}
                for i in range(5)]
    for name, rows in (("tokens", toks), ("texts", texts), ("utterances", utts), ("speakers", speakers)):
        with open(os.path.join(root, name + ".csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    return root


class GlossTest(unittest.TestCase):
    def test_parse_gloss(self):
        g = parse_gloss("be.sick-NEG-PTCP.FUT-2SG-ACC")
        self.assertEqual(g["lemma"], "be.sick")
        self.assertEqual(case_of(g["tags"]), "ACC")
        g = parse_gloss("centre-1PL.[NOM]")
        self.assertEqual((case_of(g["tags"]), g["zero"]), ("NOM", {"NOM"}))
        self.assertEqual(parse_gloss("go-COND1-3SG")["tags"], ["COND", "3SG"])
        self.assertEqual(case_of(parse_gloss("house-INS")["tags"]), "INSTR")
        self.assertEqual(parse_gloss("")["n_morphs"], 0)

    def test_labels(self):
        self.assertEqual(labels("np.h:S"), ("S", "-", "-"))
        self.assertEqual(labels("pro:O"), ("O", "-", "-"))
        self.assertEqual(labels("0.1.h:S v:pred"), ("-", "pred", "0.1"))
        self.assertEqual(labels("cop"), ("-", "pred", "-"))
        self.assertEqual(labels("0.3:O v:pred"), ("-", "pred", "-"))  # zero object is not an overt O
        self.assertEqual(labels(""), ("-", "-", "-"))


class FeatureTest(unittest.TestCase):
    def test_features_see_case_and_verb_context(self):
        rows = [{"ps": "n", "ge": "man.[NOM]"}, {"ps": "n", "ge": "fish-ACC"}, {"ps": "v", "ge": "eat-PST-3SG"}]
        f = utterance_features(rows)
        self.assertIn("case=ACC", f[1])
        self.assertIn("dright=1", f[1])
        self.assertIn("rv_lem=eat", f[1])
        self.assertIn("nom_rank=0", f[0])
        self.assertNotIn("lem=fish", utterance_features(rows, "universal")[1])

    def test_noun_person_is_possessor(self):
        f = utterance_features([{"ps": "n", "ge": "father-3PL.[NOM]"}, {"ps": "v", "ge": "go-PST-3SG"}])
        self.assertIn("poss=3", f[0])
        self.assertIn("pers=3", f[0])

    def test_profiles(self):
        self.assertEqual(type_key({"order": "OV", "affix": "suffix", "align": "acc"}), "OV-suffix-acc")
        a = augment([{"x": 1}], "dolgan", {"order": "OV", "affix": "suffix", "align": "acc"})[0]
        self.assertEqual(set(a), {"x", "T:OV-suffix-acc|x", "L:dolgan|x"})
        with tempfile.TemporaryDirectory() as d:
            synth_corpus(d)
            with open(os.path.join(d, "tokens.csv"), encoding="utf-8") as f:
                est = estimate(list(csv.DictReader(f)))
        self.assertEqual((est["order"], est["affix"], est["align"]), ("OV", "suffix", "acc"))


class KappaTest(unittest.TestCase):
    def test_kappa(self):
        self.assertAlmostEqual(kappa([("S", "S"), ("O", "O"), ("S", "O"), ("O", "S")]), 0.0)
        self.assertAlmostEqual(kappa([("S", "S"), ("O", "O")]), 1.0)


@unittest.skipUnless(HAVE_SK, "training needs scikit-learn")
class EndToEndTest(unittest.TestCase):
    def test_train_export_apply_review_merge(self):
        from data import load
        from model import Tagger
        import apply as apply_mod
        import merge_review
        with tempfile.TemporaryDirectory() as root:
            synth_corpus(root)
            d = load(root, "synth")
            tagger = Tagger.train(d)
            out = tagger.predict(d)
            hard = [max(p, key=p.get) for p in out["role"]]
            acc = sum(a == b for a, b in zip(hard, d["role"])) / len(hard)
            self.assertGreater(acc, 0.9)
            # JSON export predicts the same probabilities with the standard library
            path = os.path.join(root, "m.json")
            tagger.to_json(path)
            back = Tagger.from_json(path).predict(d)
            for a, b in zip(out["role"][:50], back["role"][:50]):
                for k in a:
                    self.assertAlmostEqual(a[k], b[k], places=9)
            # apply -> queue -> fake review -> merge
            rd = os.path.join(root, "review")
            info = apply_mod.build(path, root, rd, "synth", threshold=0.99, nom_floor=0.05, overlap=0.5, salt="t")
            self.assertGreater(info["queue"], 0)
            with open(os.path.join(rd, "queue.csv"), encoding="utf-8") as f:
                q = list(csv.DictReader(f))
            self.assertNotIn("speaker", ",".join(q[0].keys()))
            for coder in ("A", "B"):
                with open(os.path.join(root, f"rev_{coder}.csv"), "w", newline="", encoding="utf-8") as f:
                    w = csv.writer(f, lineterminator="\n")
                    w.writerow(["item", "word", "tx", "label", "decided", "model_suggestion", "flagged", "changed",
                                "item_done", "note", "coder", "decided_at"])
                    for r in q:
                        if r["coder"] not in ("both", coder):
                            continue
                        for i, word in enumerate(json.loads(r["words"])):
                            lab = {"S": "S", "O": "O", "-": "N"}[word["suggest"]]
                            w.writerow([r["item"], i, word["tx"], lab, int(word["flag"]), lab, int(word["flag"]), 0, 1,
                                        "", coder, ""])
            counts, k = merge_review.merge(rd, [os.path.join(root, "rev_A.csv"), os.path.join(root, "rev_B.csv")])
            self.assertGreater(counts["agreed"], 0)
            self.assertEqual(counts["disputed"], 0)
            self.assertTrue(os.path.exists(os.path.join(rd + "_key", "final_roles.csv")))
            self.assertEqual(sorted(os.listdir(rd)), ["agreement.md", "queue.csv"])  # nothing coders must not see
            # write back as SyF: the study scripts then read the expanded corpus unchanged
            import to_syf
            n = to_syf.expand(root, rd, os.path.join(root, "expanded"))
            self.assertGreater(n["human"], 0)
            with open(os.path.join(rd, "queue.csv"), encoding="utf-8") as f:
                n_flag = sum(int(r["n_flagged"]) for r in csv.DictReader(f))
            self.assertLessEqual(n["human"], n_flag)  # only words a coder decided count as human
            self.assertGreater(n["inel"], 0)
            with open(os.path.join(root, "expanded", "texts.csv"), encoding="utf-8") as f:
                self.assertTrue(all(t["has_SyF"] == "1" for t in csv.DictReader(f)))
            self.assertEqual(to_syf.syf_tag("v", "-", 0.9, "0.3"), "0.3:S v:pred")
            self.assertEqual(to_syf.syf_tag("pers", "S", 0.1, "-"), "pro:S")
            # calibration queue against INEL's own tags
            cd = os.path.join(root, "calib")
            info = apply_mod.build_calibration(root, cd, "synth", ["T0"])
            self.assertGreater(info["items"], 0)
            with open(os.path.join(cd, "queue.csv"), encoding="utf-8") as f:
                cq = list(csv.DictReader(f))
            gold = {}
            self.assertEqual(os.listdir(cd), ["queue.csv"])
            with open(os.path.join(cd + "_key", "inel_gold.csv"), encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    gold[(r["item"], int(r["word"]))] = r["inel_role"]
            self.assertTrue(all(w["suggest"] == "" for r in cq for w in json.loads(r["words"])))
            ex = os.path.join(root, "calA.csv")
            with open(ex, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(["item", "word", "label", "coder"])
                for (item, word), g in gold.items():
                    w.writerow([item, word, {"S": "S", "O": "O", "-": "N"}[g], "A"])
            by = merge_review.compare_gold(cd, [ex])
            with open(os.path.join(cd, "calibration.md"), encoding="utf-8") as f:
                self.assertIn("100.0%", f.read())


if __name__ == "__main__":
    unittest.main()


class GlosserTest(unittest.TestCase):
    def test_known_and_unseen_forms(self):
        from glosser import Glosser
        rows = []
        for k, (tx, mb, ge, ps) in enumerate([
                ("balɨgɨ", "balɨk-ɨ", "fish-ACC", "n"), ("ete", "e-t-e", "be-PST1-3SG", "cop"),
                ("tabanɨ", "taba-nɨ", "reindeer-ACC", "n"), ("balɨk", "balɨk", "fish.[NOM]", "n"),
                ("kihini", "kihi-ni", "person-ACC", "n"), ("dʼi͡eni", "dʼi͡e-ni", "house-ACC", "n")] * 3):
            rows.append({"utt_id": f"u{k}", "idx": "1", "tx": tx, "mb": mb, "ge": ge, "ps": ps})
        g = Glosser().train(rows)
        out = g.gloss(["Balɨgɨ", "ogoni"])
        self.assertEqual(out[0][:3], ("balɨk-ɨ", "fish-ACC", "n"))
        self.assertEqual(out[0][3], "known")
        self.assertTrue(out[1][1].endswith("-ACC"))   # unseen stem, known ending
        self.assertEqual(out[1][3], "ending")


@unittest.skipUnless(HAVE_SK, "training needs scikit-learn")
class PipelineTest(unittest.TestCase):
    def test_raw_text_to_queue(self):
        from data import load
        from model import Tagger
        import pipeline
        with tempfile.TemporaryDirectory() as root:
            synth_corpus(os.path.join(root, "train"))
            Tagger.train(load(os.path.join(root, "train"), "synth")).to_json(os.path.join(root, "m.json"))
            with open(os.path.join(root, "train", "tokens.csv"), encoding="utf-8") as f:
                toks = [r for r in csv.DictReader(f) if r["text_id"] == "T15"]
            utts = {}
            for t in toks:
                utts.setdefault(t["utt_id"], []).append(t["tx"])
            path = os.path.join(root, "new.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(["utt_id", "text_id", "speaker_id", "tx", "fe"])
                for u, ws in utts.items():
                    w.writerow([u, "NEW1", "X", " ".join(ws), "t"])
            info = pipeline.run(os.path.join(root, "train"), path, os.path.join(root, "out"))
            self.assertEqual(info["words"], len(toks))
            c = info["gloss_confidence"]
            self.assertGreater(c.get("known", 0) + c.get("ambiguous", 0), 0.8 * len(toks))
            import apply
            q = apply.build(os.path.join(root, "m.json"), os.path.join(root, "out"), os.path.join(root, "out", "review"),
                            "synth", 0.99, 0.05, 0.1, "x")
            self.assertEqual(q["words"], len(toks))
