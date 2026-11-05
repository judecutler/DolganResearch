"""Run the whole data pipeline for both corpora (handoff 003).

    python3 shared/run_all.py                      # uses data/raw/<corpus>-2.0
    python3 shared/run_all.py --raw-root DIR --derived DIR --reports DIR

Writes tables, objects.csv, evid_candidates.csv and b1_candidates.csv to data/derived/<corpus>/ (git-ignored, contains corpus text),
reports with counts and labels only to reports/, and the Study A pilot
workbooks to data/derived/workbooks/ (git-ignored, contains sentences).
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "case_change"))

import build_tables  # noqa: E402
import evid_candidates  # noqa: E402
import extract_b1  # noqa: E402
import extract_objects  # noqa: E402
import gate0  # noqa: E402
import qa_report  # noqa: E402
import workbook  # noqa: E402


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--raw-root", default=os.path.join(ROOT, "data", "raw"))
    p.add_argument("--derived", default=os.path.join(ROOT, "data", "derived"))
    p.add_argument("--reports", default=os.path.join(ROOT, "reports"))
    p.add_argument("--pilot-n", type=int, default=40)
    a = p.parse_args(argv)

    dirs = {}
    for corpus in ("dolgan", "evenki"):
        raw = os.path.join(a.raw_root, f"{corpus}-2.0")
        out = os.path.join(a.derived, corpus)
        print(f"[{corpus}] building tables from {raw}", flush=True)
        build_tables.build(corpus, raw, out)
        n_obj = len(extract_objects.main(out, os.path.join(out, "objects.csv")))
        n_cand = len(evid_candidates.main(out, os.path.join(out, "evid_candidates.csv")))
        n_b1 = len(extract_b1.main(out, os.path.join(out, "b1_candidates.csv")))
        print(f"[{corpus}] {n_obj} objects, {n_cand} evidential candidates, {n_b1} B1 candidates", flush=True)
        dirs[corpus] = out

    os.makedirs(a.reports, exist_ok=True)
    qa_path = os.path.join(a.reports, "qa_report.md")
    n_diff = qa_report.main(qa_path, dirs["dolgan"], dirs["evenki"])
    g0_path = os.path.join(a.reports, "gate0_feasibility.md")
    verdicts = gate0.main(g0_path, dirs["dolgan"], dirs["evenki"])
    wb = os.path.join(a.derived, "workbooks")
    pilot = workbook.build("pilot", wb, [os.path.join(dirs[c], "evid_candidates.csv") for c in ("dolgan",)],
                           n=a.pilot_n)

    b1 = workbook.build("pilot", wb, [os.path.join(dirs["dolgan"], "b1_candidates.csv")], n=100000,
                        codebook_path=os.path.join(HERE, "config", "b1_codebook.json"), prefix="b1")
    print(f"B1 vetting workbooks (all candidates, both annotators): {len(b1)} items -> {wb}")
    print(f"QA: {n_diff} checks do not match handoff 002 -> {qa_path}")
    for name, val, ok in verdicts:
        print(f"Gate 0 {'PASS' if ok else ('FAIL' if ok is not None else 'human')}: {name}: {val}")
    print(f"Pilot workbooks: {len(pilot)} items -> {wb}")
    return 1 if n_diff else 0


if __name__ == "__main__":
    sys.exit(main())
