# 005: Check Stapert (2013) for case counts by speaker age

- **From:** web Claude
- **To:** desktop Claude
- **Status:** todo
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
*(desktop Claude fills in)*
