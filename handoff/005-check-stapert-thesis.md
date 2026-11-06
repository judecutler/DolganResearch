# 005: Check Stapert (2013) for case counts by speaker age

- **From:** web Claude
- **To:** desktop Claude
- **Status:** done
- **Created:** 2026-11-05
- **Depends on:** none (can run with or after 003)

## Goal
Study B claims that nobody has counted Dolgan case marking by speaker age or recording period (`docs/LITERATURE_LEDGER.md`, Study B, falsification pass). The closest work web Claude could not open is Stapert's 2013 Leiden thesis. Its chapters were off the web session's fetch allowlist. If any chapter counts case by speaker age, the claim drops to PARTIAL, and the plan must change before more work goes into Study B.

## Steps
1. In the built-in browser, open https://scholarlypublications.universiteitleiden.nl/access/item%3A2940587/view (Stapert, E. L. 2013, *Contact-induced change in Dolgan*, LOT 336). Download the chapter PDFs and the English summary (items about 2940590 to 2940602) into `scratch/005/`. Do not commit them.
2. Search each PDF's text (for example `pdftotext` if installed, or Python) for: `case`, `instrumental`, `dative`, `partitive`, `accusative`, `object`, `secondary predicat`, `depictive`, `age`, `generation`, `younger`, `older`, `born`.
3. For every passage about case **and** speaker age, generation or recording time, write the chapter, page, a quote of at most 3 lines, and whether it gives counts.
4. Also record the thesis's table of contents (chapter titles only).

## Expected outputs
- `handoff/outputs/005/stapert_check.md`: table of contents, then the passages from step 3, or the sentence "no passage combines case with age, generation or period".

## Acceptance checks
- [ ] Every chapter was searched, or the ones that could not be downloaded are listed.
- [ ] No PDF is committed.

---

## Results

- **Date finished:** 2026-11-06
- **Downloaded:** the repository's single "Full text" PDF (424 pages; every chapter, the references and the English summary), md5 `2b434b10739996f83b122bbd920ab96c`, into `scratch/005/` (git-ignored). The shell's network is blocked for this host (HTTP 403), so I downloaded it in the built-in browser. A copy is also in Jude's Downloads folder.
- **Searched:** all 10 chapters, the references and the summary, for all 13 terms. Counts per chapter are in `handoff/outputs/005/stapert_check.md`. "Secondary predicat" and "depictive" do not occur.
- **Table of contents:** in the output file.
- **Passages combining case with age:** one. Ch 5, pp. 187-188: the variation between Sakha and Dolgan stems in case-inflected relational nouns "does not play any role" by age, with no counts by age (counts are given by village only). Related: Ch 7, pp. 257-258, Table 7.3 counts OV vs VO by three age groups (2, 2 and 1 speakers). That is word order, not case.
- **Verdict:** no passage counts case marking by speaker age, generation or recording period. Whether the Ch 5 passage changes the Study B novelty claim to PARTIAL is for web Claude (and Jude) to decide. It should at least be cited.
- **Acceptance:** every chapter searched (one full-text PDF instead of separate chapter files); no PDF committed.
