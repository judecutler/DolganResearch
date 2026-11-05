"""Gate 0 feasibility report: is there enough data of the right kind?

    python3 shared/gate0.py OUT.md data/derived/dolgan data/derived/evenki

Reads tables, objects.csv and evid_candidates.csv. Reports design counts only
(speakers, cohorts, sources, token totals). It never shows an outcome by cohort,
such as object case by birth decade: that stays hidden until the analysis plan is
frozen at Gate 3. Thresholds are the placeholders in docs/ROADMAP_CLAUDE_WEB.md.
Decades are a provisional binning for counting only; the real bins are D-013.
"""
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inel.load import num, table  # noqa: E402

PRECISE = 10  # a birth year counts as usable if its range is at most this many years
THRESHOLDS = {"speakers": 15, "cohorts": 3, "per_cohort": 5, "objects": 200, "object_speakers": 15,
              "max_share": 0.25}


def decade(x):
    return f"{int(x // 10 * 10)}s"


def crosstab(pairs, rows_label, cols_label):
    c = Counter(pairs)
    if not c:
        return ["(none)"]
    rows = sorted({a for a, _ in c})
    cols = sorted({b for _, b in c})
    out = [f"| {rows_label} \\ {cols_label} | " + " | ".join(str(x) for x in cols) + " | total |",
           "|" + "---|" * (len(cols) + 2)]
    for r in rows:
        vals = [c.get((r, k), 0) for k in cols]
        out.append(f"| {r} | " + " | ".join(str(v) if v else "." for v in vals) + f" | {sum(vals)} |")
    return out


def usable(s):
    lo, hi = num(s["birth_lo"]), num(s["birth_hi"])
    return lo is not None and hi - lo <= PRECISE


def dolgan_section(d):
    spk = table(d, "speakers")
    texts = {t["text_id"]: t for t in table(d, "texts")}
    toks = table(d, "tokens")
    objs = table(d, "objects")
    cands = table(d, "evid_candidates")
    good = {s["speaker_id"]: s for s in spk if usable(s)}
    dec = {sid: decade(num(s["birth_mid"])) for sid, s in good.items()}
    verdicts = []
    out = ["## Dolgan", "", "### Speakers and birth years", ""]
    prec = Counter(s["birth_precision"] or "unknown" for s in spk)
    out.append(f"{len(spk)} speakers appear in transcripts. Birth-year precision: "
               + ", ".join(f"{k} {v}" for k, v in sorted(prec.items()))
               + f". Usable (range of {PRECISE} years or less): **{len(good)}**.")
    tok_by = Counter(t["speaker_id"] for t in toks)
    by_dec = Counter(dec.values())
    out += ["", "| Birth decade (provisional) | Speakers | Tokens |", "|---|---|---|"]
    for k in sorted(by_dec):
        out.append(f"| {k} | {by_dec[k]} | {sum(tok_by[s] for s in dec if dec[s] == k)} |")
    cohorts_ok = sum(1 for v in by_dec.values() if v >= THRESHOLDS["per_cohort"])
    verdicts.append(("At least 15 speakers with a usable birth year", len(good), len(good) >= THRESHOLDS["speakers"]))
    verdicts.append(("At least 3 provisional cohorts with 5 or more speakers", cohorts_ok,
                     cohorts_ok >= THRESHOLDS["cohorts"]))

    spk_texts = defaultdict(set)
    for t in toks:
        spk_texts[t["speaker_id"]].add(t["text_id"])
    pairs_src = [(dec[s], texts[t]["source_collection"]) for s in dec for t in spk_texts[s]]
    pairs_gen = [(dec[s], texts[t]["genre"]) for s in dec for t in spk_texts[s]]
    pairs_rec = [(dec[s], decade(num(texts[t]["recording_lo"]))) for s in dec for t in spk_texts[s]
                 if texts[t]["recording_lo"]]
    out += ["", "### Are birth cohort, source, genre and recording date tangled?",
            "", "Counts are (speaker, text) pairs. If each cohort sits in one source or genre, "
            "a cohort effect cannot be told apart from a source or genre effect.", ""]
    out += crosstab(pairs_src, "birth", "source (inferred)") + [""]
    out += crosstab(pairs_gen, "birth", "genre") + [""]
    out += crosstab(pairs_rec, "birth", "recording decade")

    syf_texts = {t for t, r in texts.items() if r["has_SyF"] == "1"}
    syf_spk = {t["speaker_id"] for t in toks if t["text_id"] in syf_texts}
    out += ["", "### `SyF` coverage (Study B needs it to find objects)", "",
            f"`SyF` is non-empty in {len(syf_texts)} of {len(texts)} texts. Speakers in those texts: "
            f"{len(syf_spk)}, of whom {len(syf_spk & set(good))} have a usable birth year.", ""]
    out += crosstab([(texts[t]["source_collection"], texts[t]["genre"]) for t in syf_texts],
                    "source", "genre (texts with SyF)")

    o_good = [o for o in objs if o["speaker_id"] in good]
    per = Counter(o["speaker_id"] for o in o_good)
    share = max(per.values()) / len(o_good) if o_good else 0
    out += ["", "### Study B objects (counts only, no case by cohort)", "",
            f"{len(objs)} objects in total; {len(o_good)} from {len(per)} speakers with a usable birth year. "
            f"Largest single-speaker share: {share:.0%}. Speakers with 20 or more objects: "
            f"{sum(1 for v in per.values() if v >= 20)}.", "",
            "| Birth decade (provisional) | Speakers with objects | Objects |", "|---|---|---|"]
    for k in sorted(by_dec):
        ss = [s for s in per if dec[s] == k]
        out.append(f"| {k} | {len(ss)} | {sum(per[s] for s in ss)} |")
    out += ["", "Objects by source (all speakers): " + ", ".join(
        f"{k} {v}" for k, v in Counter(o["source_collection"] for o in objs).most_common()) + ".",
        "Objects with a `BOR` value (possible loans, a confounder for zero marking): "
        f"{sum(1 for o in objs if o['loan'] == '1')}. With no predicate found in the utterance: "
        f"{sum(1 for o in objs if not o['pred_token_id'])}."]
    verdicts.append(("At least 200 objects from speakers with a usable birth year", len(o_good),
                     len(o_good) >= THRESHOLDS["objects"]))
    verdicts.append(("Objects come from at least 15 such speakers", len(per), len(per) >= THRESHOLDS["object_speakers"]))
    verdicts.append(("No speaker gives more than 25% of objects", f"{share:.0%}", share <= THRESHOLDS["max_share"]))

    b1 = table(d, "b1_candidates")
    b1_spk = {c["speaker_id"] for c in b1}
    out += ["", "### Study B1 (secondary predicates): candidates for human vetting", "",
            "No tag marks secondary predicates (D-021). `case_change/extract_b1.py` applies rules built "
            "from Siegl (2015)'s examples. Counts are by rule, source and recording decade only, not by "
            f"case, because case is the B1 outcome. Candidates: {len(b1)}, from {len(b1_spk)} speakers "
            f"({len(b1_spk & set(good))} with a usable birth year).", ""]
    out += crosstab([(c["rules"].split()[0], texts[c["text_id"]]["source_collection"]) for c in b1],
                    "rule", "source") + [""]
    out += crosstab([(c["rules"].split()[0], decade(num(c["recording_lo"])) if c["recording_lo"] else "unknown")
                     for c in b1], "rule", "recording decade")
    verdicts.append(("B1: at least 30 candidates from at least 10 speakers (before vetting)",
                     f"{len(b1)} from {len(b1_spk)}", len(b1) >= 30 and len(b1_spk) >= 10))
    return out + _evid(cands, good, dec), verdicts


def _evid(cands, good, dec):
    out = ["", "### Study A candidates", "", "| Rule (first rule that found it) | Tier | Words | Speakers | "
           "From speakers with usable birth year |", "|---|---|---|---|---|"]
    by = defaultdict(list)
    for c in cands:
        by[(c["rules"].split()[0], c["tier"])].append(c)
    for (r, tier), cs in sorted(by.items(), key=lambda x: (x[0][1], x[0][0])):
        sp = {c["speaker_id"] for c in cs}
        out.append(f"| `{r}` | {tier} | {len(cs)} | {len(sp)} | {sum(1 for c in cs if c['speaker_id'] in good)} |")
    gen = Counter((c["rules"].split()[0], c["genre"]) for c in cands)
    out += ["", "By genre: " + "; ".join(f"`{r}` {g} {n}" for (r, g), n in sorted(gen.items())) + "."]
    return out


def evenki_section(d):
    texts = table(d, "texts")
    spk = table(d, "speakers")
    objs = table(d, "objects")
    cands = table(d, "evid_candidates")
    out = ["## Evenki (baseline; no cohort analysis)", "",
           f"{len(texts)} texts, {len(spk)} speakers, {sum(1 for s in spk if usable(s))} with a usable birth year. "
           f"{len(objs)} objects. Texts by dialect and source:", ""]
    out += crosstab([(t["dialect"] or "unknown", t["source_collection"]) for t in texts], "dialect", "source")
    out += ["", "Objects by source: " + ", ".join(
        f"{k} {v}" for k, v in Counter(o["source_collection"] for o in objs).most_common()) + "."]
    return out + _evid(cands, set(), {})


def main(out_path, dolgan_dir, evenki_dir=None):
    body, verdicts = dolgan_section(dolgan_dir)
    lines = ["# Gate 0: feasibility", "",
             "Built by `shared/gate0.py`. Design counts only; outcomes by cohort stay hidden until Gate 3. "
             "Decades are a provisional binning for counting (D-013 sets the real bins).", "",
             "## Summary", "", "| Check | Value | Result |", "|---|---|---|"]
    lines += [f"| {name} | {val} | {'PASS' if ok else ('FAIL' if ok is not None else 'human')} |"
              for name, val, ok in verdicts]
    lines += [""] + body
    if evenki_dir:
        lines += [""] + evenki_section(evenki_dir)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return verdicts


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    for name, val, ok in main(*sys.argv[1:]):
        print(f"{'PASS' if ok else ('FAIL' if ok is not None else 'human')}  {name}: {val}")
