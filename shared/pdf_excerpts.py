"""Short, page-numbered excerpts from a PDF around search terms, for web Claude to read.

    python3 shared/pdf_excerpts.py PAPER.pdf OUT.md --terms partitive imperative "Evenki" [--context 1]

Needs the `pdftotext` program (poppler). Writes term counts per page and at most
--max-hits excerpts of at most 2 * context + 1 lines each, so that the output stays
a set of short quotations, not a copy of the paper. The PDF itself is never committed.
"""
import argparse
import re
import shutil
import subprocess
import sys


def pages(pdf):
    if not shutil.which("pdftotext"):
        sys.exit("pdftotext not found: install poppler, or report this in the handoff")
    text = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, check=True,
                          text=True, encoding="utf-8", errors="replace").stdout
    parts = text.split("\f")
    return parts[:-1] if parts and not parts[-1].strip() else parts  # pdftotext ends with a page break


def excerpts(page_texts, terms, context=1, max_hits=40):
    """[(pdf page, term, lines)] for the first max_hits matching lines, overlaps merged."""
    pats = [(t, re.compile(re.escape(t), re.IGNORECASE)) for t in terms]
    out, counts = [], {t: {} for t in terms}
    for pno, page in enumerate(page_texts, 1):
        lines = page.splitlines()
        taken = set()
        for i, line in enumerate(lines):
            for t, pat in pats:
                if pat.search(line):
                    counts[t][pno] = counts[t].get(pno, 0) + 1
                    if i not in taken and len(out) < max_hits:
                        lo, hi = max(0, i - context), min(len(lines), i + context + 1)
                        taken.update(range(lo, hi))
                        out.append((pno, t, [x.strip() for x in lines[lo:hi] if x.strip()]))
    return out, counts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("out")
    ap.add_argument("--terms", nargs="+", required=True)
    ap.add_argument("--context", type=int, default=1)
    ap.add_argument("--max-hits", type=int, default=40)
    a = ap.parse_args(argv)
    texts = pages(a.pdf)
    hits, counts = excerpts(texts, a.terms, a.context, a.max_hits)
    lines = [f"# Excerpts from `{a.pdf.replace(chr(92), '/').split('/')[-1]}`", "",
             f"{len(texts)} PDF pages. Built by `shared/pdf_excerpts.py`; page numbers are PDF pages.", "",
             "## Term counts (PDF pages where the term occurs)", ""]
    for t in a.terms:
        c = counts[t]
        lines.append(f"- **{t}**: {sum(c.values())} lines on pages "
                     + (", ".join(f"{p} ({n})" for p, n in sorted(c.items())) or "none"))
    lines += ["", f"## Excerpts (first {a.max_hits} hits)", ""]
    for pno, t, ex in hits:
        lines += [f"**p. {pno}** ({t})", "", "> " + "\n> ".join(ex), ""]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{len(hits)} excerpts -> {a.out}")


if __name__ == "__main__":
    main()
