# 002: Inspect the real corpus structure

- **From:** web Claude
- **To:** desktop Claude
- **Status:** done
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

- **Date finished:** 2026-11-05
- **Five-line summary:**
  1. All 136 Dolgan and 612 Evenki `.exb` files parse. Per word, `mb`, `mp` and `ge` align exactly (0 mismatches in about 93,000 words per corpus). Dolgan `mc` does not align one-to-one (about 17% of words); Evenki `mc` does.
  2. Zero nominative is `.[NOM]` on the last gloss in both corpora (no plain `NOM`). Dolgan has `DAT/LOC` as one label. Evenki spells things differently (`INS`, `ACC.INDF`, `LAT`, `ALL`, `COM1` to `COM4`).
  3. `-BIt` and `-DAK` are not in the tiers as spelled in the task. Dolgan `mp` `BIT` is `PST2` (`BIt` is `1PL`); `TAK` is `COND1` (555) or `INFER` (36); `EVID` is the particle `eːt` (53). Evenki has `EVID` on `rkə` (29) and no `INFER`.
  4. Role `St` is the stimulus of perception verbs, not secondary predicates. The task's hypothesis is not supported.
  5. Evenki counts match the website exactly. Dolgan transcripts (136) and speakers (74) match; Dolgan utterances (14,078 or 14,076 against 14,193) and tokens (97,757 or 97,652 against 97,625) do not match under any counting rule I tried.
- **Questions that could not be answered:** none left unanswered. Partly answered: Q3 (I did not compare annotation content between `.exb` and `.exs`), Q13 (no collection field exists; my mapping from other fields is an inference), Q18 (the word "postterminal" is not in the Dolgan documentation, so I cannot confirm which label that means). Everything is in `handoff/outputs/002/structure_report.md`.
- **Surprises:**
  - The Dolgan documentation says Anabar Dolgan is not in the corpus, but the `.coma` marks 3 texts and 2 speakers as `Anabar`.
  - Single-speaker files drop the `-SIGLE` suffix from tier ids (94 Dolgan and 605 Evenki files).
  - Evenki has no `Top` or `Foc` tiers and no `=` clitic marker; Dolgan has both.
  - 4,243 Dolgan and 1,066 Evenki words have no morph analysis (Russian words, repairs, non-speech). 302 Dolgan utterances have no analysed word at all.
  - Three Dolgan `nar` folders hold only a `.eaf` file.
  - Birth dates are missing or imprecise: Evenki 34 of 53 speakers unknown; Dolgan 14 of the 74 speakers in transcripts unknown and only 16 full dates.
  - Personal names occur inside the transcript text itself, not only in the metadata.
- **Files:** `handoff/outputs/002/structure_report.md`, `tier_coverage_<corpus>.csv`, `gloss_census_<corpus>.csv` (capitalised stems withheld, see the report), `scripts/`. Full evidentiality token lists are local only (`data/derived/002/`, git-ignored) because of the 30-line excerpt rule.
- **Questions for web Claude:**
  1. Which counting rule does the documentation use for Dolgan tokens and utterances? None of the file-based counts equals 97,625 or 14,193.
  2. Which label do you mean by postterminal (`-BIt`)? In the data it is `PST2` (spelled `BIT`). Is `INFER` on `TAK` really the inferential `-DAK`, and should `COND1` on the same morph be treated as a different category?
  3. Should the parser tolerate Dolgan `mc` slots that do not align with `mb`, or ignore `mc`?
  4. Is `Anabar` in the `.coma` for those 3 texts correct, given the documentation?
  5. Decide how to treat the capitalised stem glosses (names) in any shared label table.
