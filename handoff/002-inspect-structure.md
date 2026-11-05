# 002: Inspect the real corpus structure

- **From:** web Claude
- **To:** desktop Claude
- **Status:** blocked-by-001
- **Created:** 2026-11-04
- **Depends on:** 001

## Goal
Web Claude knows the INEL file format only from the documentation PDFs and has never seen a real file. Before writing the parser, it needs the actual structure. This task answers a fixed list of questions about the files in `data/raw/`. It builds no tools. Throwaway scripts go in `scratch/002/`, which is git-ignored. Copy any script worth keeping into `handoff/outputs/002/` so the work can be repeated.

## Questions to answer
Answer for **both** corpora, and say where they differ.

**A. File layout**
1. For one `.exb` per Dolgan genre folder: list the tiers. For each give its `category`, its `display-name`, its `speaker` attribute, and its `type`. Say which tiers are `t` (transcription) and which are `a` (annotation).
2. Is there one set of tiers per speaker (for example `tx [SPK]`, `mb [SPK]`) or one set per file? How are speaker codes written?
3. What is the difference between `.exb` and `.exs` in practice? Which one lists the segmentation, and does it contain anything the `.exb` lacks?

**B. Alignment** (this decides the parser's design)
4. Show 10 consecutive events from one fully glossed utterance, for tiers `tx`, `mb`, `mp`, `ge`, `mc`, `ps`: event start/end ids, and text. Is each word one event, with morphemes separated inside the event text?
5. What characters separate morphemes in `mb`, `mp`, `ge`? (`-`, `=`, `.`, `~`, others.) How are clitics marked? How are zero morphs and portmanteau glosses written?
6. For one text, count how many words have the same number of `mb` morphs and `ge` glosses, and how many differ. Show 5 mismatches.

**C. Optional tiers**
7. For each text, say which of `SyF`, `SeR`, `IST`, `Top`, `Foc`, `BOR`, `BOR-Phon`, `BOR-Morph`, `CS`, `ExLocPoss` are present and non-empty. Write the table to `handoff/outputs/002/tier_coverage_<corpus>.csv`.
8. Which spelling do the files use: `BOR-Phon` or `BORphon`? Are both used?
9. Show five `SyF` values that end in `:O` and five that end in `:S`. Show every distinct `SeR` role value with its count, and the five most common `SeR` form values.
10. Does `SeR` role `St` appear? Show five examples with their free translations. (Hypothesis to test: it may mark secondary predicates.)

**D. Metadata (`.coma`)**
11. List every speaker field in the Dolgan `.coma`. For `date of birth`: how many speakers have a value, and show all the distinct formats (full date, year only, partial, text such as "ca. 1930").
12. List every communication field. For `year of recording`, `genre`, `dialect`: how many texts have a value, and the distinct values with counts.
13. Is there a field that identifies the source collection (published folklore, TDNT, Stapert fieldwork, 2017 experiment)? If not, which field or naming pattern reveals it?
14. Are there Anabar speakers or texts (as opposed to Taymyr)? Look at the dialect and region fields.
15. Evenki: the same questions for date of birth and recording year. How many speakers are marked unknown?

**E. Labels**
16. Census of every distinct gloss label in `ge` (English glosses) with counts, written to `handoff/outputs/002/gloss_census_<corpus>.csv`. Split labels into stems/words vs. grammatical labels.
17. For case: show the counts for NOM, ACC, ACC.INDEF, PART, DAT, DAT/LOC, LOC, ABL, ALL, LAT, INSTR, COM, PROL, GEN, COMP, and any other case-like label.
18. For evidentiality: list every token whose `ge` contains `EVID` or `INFER`, with `mb` form, `mp` form, `mc`, and the free translation. Also list the five most common labels in the tense and mood slots (`PST1`, `PST2`, and so on), each with 3 example forms. We need to know which label the postterminal (-BIt) and the inferential (-DAK) carry. Do not assume.
19. For objects: how do the `mc` and `ge` tiers mark a nominative-marked object? Show five examples of an object tagged `:O` with no case suffix.

**F. Reconciliation and oddities**
20. Count transcripts, speakers, utterances and words (tokens in `tx`). Compare with the documentation (Dolgan 2.0: 136 transcripts, 74 speakers, 14,193 utterances, 97,625 tokens; Evenki 2.0 website: 612 texts, 19,931 sentences, 93,264 tokens). Note how you counted a token.
21. Anything strange: empty tiers, encoding problems, mixed Cyrillic and Latin, `%` and `%%` markers (how many), texts with no glosses, duplicated ids, files that fail to parse.

## Expected outputs
- `handoff/outputs/002/structure_report.md`: answers keyed by the question numbers above, with short excerpts
- `handoff/outputs/002/tier_coverage_dolgan.csv`, `tier_coverage_evenki.csv`
- `handoff/outputs/002/gloss_census_dolgan.csv`, `gloss_census_evenki.csv`
- Results section below: five-line summary and any blockers

## Acceptance checks
- [ ] Every question number is answered or marked "could not determine, because ...".
- [ ] No excerpt is longer than 30 lines. Every excerpt names its source file and corpus.
- [ ] No corpus files and no speaker names are committed.

---

## Results
*(desktop Claude fills in)*

- **Date finished:**
- **Five-line summary:**
- **Questions that could not be answered:**
- **Surprises:**
- **Questions for web Claude:**
