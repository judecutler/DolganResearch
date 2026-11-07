"""Markdown report from train_eval.py's JSON (numbers only, no corpus text).

    python3 shared/igt_tagger/report.py EVAL.json reports/tagger_eval.md [--speaker SPK.json] [--glosser GLOSS.json]
"""
import json
import sys


def pct(x):
    return "n/a" if x is None else f"{100 * x:.1f}"


def prf(s, c):
    return f"{pct(s[c]['p'])} / {pct(s[c]['r'])} / {pct(s[c]['f1'])}"


def main(argv):
    res = json.load(open(argv[0], encoding="utf-8"))
    L = ["# Argument tagger: evaluation", "",
         "Built by `shared/igt_tagger/train_eval.py`; design and caveats in `docs/TAGGER_NOTES.md`. "
         "P / R / F1 are precision, recall and F1 in percent. Everything is scored on texts the model did not "
         "train on. 'Held-out' texts (20% of each language's tagged texts) were set aside before development "
         "and used once.", "", "## Data", "",
         "| Language | Split | Texts | Speakers | Words | S | O |", "|---|---|---|---|---|---|---|"]
    for lang, sz in res["sizes"].items():
        for split, s in sz.items():
            L.append(f"| {lang} | {split} | {s['texts']} | {s['speakers']} | {s['words']} | {s['S']} | {s['O']} |")
    L += ["", "## Language profiles (declared vs estimated from the language's own glossed text)", ""]
    for lang, p in res["profiles"].items():
        d, e = p["declared"], p["estimated"]
        L.append(f"- **{lang}**: declared {d.get('order')}, {d.get('affix')}, {d.get('align')}; estimated "
                 f"{e['order']} (share of accusative nominals before their verb {e['order_share_OV']}), "
                 f"{e['affix']}, {e['align']} (ACC labels {e['n_acc']}, ERG labels {e['n_erg']}).")
    for lang in ("dolgan", "evenki"):
        r = res[lang]
        L += ["", f"## {lang.capitalize()}", ""]
        rows = []
        for name in ("dev_cv", "test"):
            if name not in r:
                continue
            s = r[name]["scores"]
            label = "dev, 5-fold nested CV" if name == "dev_cv" else "held-out texts"
            rows.append(f"| {label} | {prf(s['role'], 'S')} | {prf(s['role'], 'O')} | {pct(s['role']['macro_f1'])} | "
                        f"{pct(s['pred']['macro_f1'])} | {pct(s['sub']['macro_f1'])} | {pct(s['zero']['macro_f1'])} |")
            b = r[name]["rule_baseline"]
            rows.append(f"| ... case-only rule baseline | {prf(b, 'S')} | {prf(b, 'O')} | {pct(b['macro_f1'])} | | | |")
        L += ["| Evaluation | S (P/R/F1) | O (P/R/F1) | Role macro-F1 | Predicate F1 | Subordinate F1 | Zero-subject macro-F1 |",
              "|---|---|---|---|---|---|---|"] + rows
        if "dev_cv" in r:
            L.append(f"\nRegularisation chosen in the nested folds: {r['dev_cv']['C_chosen']}.")
        for name in ("dev_cv", "test"):
            if name not in r:
                continue
            x = r[name]
            label = "dev CV" if name == "dev_cv" else "held-out"
            L += ["", f"**Objects found, by case ({label}):** " + "; ".join(
                f"{k} {v['found']}/{v['n']} ({pct(v['found'] / v['n'] if v['n'] else None)}%)"
                for k, v in sorted(x["O_recall_by_case"].items()))]
            if lang == "dolgan":
                L += ["", f"**By speaker birth group ({label}):** does the model work equally well for old and "
                          "young speakers?", "", "| Birth group | Speakers | S F1 | O F1 | Unmarked objects found |",
                      "|---|---|---|---|---|"]
                for b, s in x["by_birth_bin"].items():
                    L.append(f"| {b} | {s['speakers']} | {pct(s['S']['f1'])} | {pct(s['O']['f1'])} | "
                             f"{s['NOM_O_found']}/{s['NOM_O_n']} |")
        cal_src = "dev CV" if "dev_cv" in r else "held-out texts"
        cal = r.get("dev_cv", r["test"])["calibration_O"]
        L += ["", f"**Calibration of P(object)** on nominals ({cal_src}): mean predicted vs observed share of objects.", "",
              "| P(O) bin | Words | Mean predicted | Observed |", "|---|---|---|---|"]
        L += [f"| {k} | {v['n']} | {v['mean_p']:.2f} | {v['observed']:.2f} |" for k, v in cal.items()]
        for name in ("dev_cv", "test"):
            if name not in r:
                continue
            label = "dev CV" if name == "dev_cv" else "held-out texts"
            L += ["", f"**Review routing ({label}).** A nominal is flagged if the model's top probability is "
                      "below the threshold, or if it is unmarked and P(O) is at least the floor. Scores assume "
                      "a human corrects every flagged word.", "",
                  "| Threshold | Unmarked-object floor | Flagged words | Share of nominals | Utterances to review | "
                  "S F1 after review | O F1 after review | Unmarked objects found |", "|---|---|---|---|---|---|---|---|"]
            for q in r[name]["routing"]:
                L.append(f"| {q['threshold']} | {q['floor'] if q['floor'] is not None else 'none'} | {q['flagged_words']} | "
                         f"{pct(q['flagged_share_of_nominals'])} | {q['utterances_to_review']} of {q['utterances_total']} | "
                         f"{pct(q['S_f1'])} | {pct(q['O_f1'])} | {pct(q['NOM_O_recall'])} |")
    L += ["", "## Transfer between languages (scored on the target's held-out texts)", "",
          "| Training data | Role macro-F1 | S F1 | O F1 | Predicate F1 | Zero-subject macro-F1 |", "|---|---|---|---|---|---|"]
    for k, s in res["transfer"].items():
        L.append(f"| {k} | {pct(s['role']['macro_f1'])} | {pct(s['role']['S']['f1'])} | {pct(s['role']['O']['f1'])} | "
                 f"{pct(s['pred']['macro_f1'])} | {pct(s['zero']['macro_f1'])} |")
    L += ["", "## How much tagged text does a language need? (held-out role macro-F1; mean of 3 random draws "
              "below 100%)", "", "| Language | Share of dev texts | Texts | Alone | + other language | "
              "+ other language, augmented |", "|---|---|---|---|---|---|"]
    for lang in ("dolgan", "evenki"):
        for frac in ("0.1", "0.25", "0.5", "1.0"):
            def m(v):
                xs = res["curve"].get(f"{lang} {frac} {v}")
                return (sum(x["role_macro_f1"] for x in xs) / len(xs), xs[0]["texts"]) if xs else (None, None)
            a, n = m("alone")
            L.append(f"| {lang} | {frac} | {n} | {pct(a)} | {pct(m('+other plain')[0])} | "
                     f"{pct(m('+other augmented')[0])} |")
    opts = dict(zip(argv[2::2], argv[3::2]))
    if "--speaker" in opts:
        sp = json.load(open(opts["--speaker"], encoding="utf-8"))["speaker_cv"]
        L += ["", "## Unseen speakers (speaker-disjoint 5-fold CV on all tagged texts, C = 0.3)", "",
              "No speaker is in both training and test. The held-out texts above share speakers with training.", "",
              "| Language | S (P/R/F1) | O (P/R/F1) | Role macro-F1 | Predicate F1 | Zero-subject macro-F1 |",
              "|---|---|---|---|---|---|"]
        for lang, r in sp.items():
            s_ = r["scores"]
            L.append(f"| {lang} | {prf(s_['role'], 'S')} | {prf(s_['role'], 'O')} | {pct(s_['role']['macro_f1'])} | "
                     f"{pct(s_['pred']['macro_f1'])} | {pct(s_['zero']['macro_f1'])} |")
        b = sp["dolgan"]["by_birth_bin"]
        L += ["", "**Dolgan, unseen speakers, by birth group:**", "",
              "| Birth group | Speakers | S F1 | O F1 | Unmarked objects found |", "|---|---|---|---|---|"]
        L += [f"| {k} | {v['speakers']} | {pct(v['S']['f1'])} | {pct(v['O']['f1'])} | {v['NOM_O_found']}/{v['NOM_O_n']} |"
              for k, v in b.items()]
    if "--glosser" in opts:
        g = json.load(open(opts["--glosser"], encoding="utf-8"))
        L += ["", "## Glosser (held-out texts)", "", "| Language | Words | Kind | Share | Exact gloss | Part of speech | Case |",
              "|---|---|---|---|---|---|---|"]
        for lang, (r, _) in g.items():
            tot = r["all"]["words"]
            for k in ("all", "known", "ambiguous", "ending", "split", "none"):
                if k in r:
                    v = r[k]
                    L.append(f"| {lang} | {v['words']} | {k} | {pct(v['words'] / tot)} | {pct(v['gloss_exact'])} | "
                             f"{pct(v['ps'])} | {pct(v['case_correct'])} |")
    with open(argv[1], "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
