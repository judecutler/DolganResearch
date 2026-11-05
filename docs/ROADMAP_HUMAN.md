# Roadmap for Jude and Dustan

This is the plain-language version. Technical detail is in `ROADMAP_CLAUDE_WEB.md` and `DATA_PREP_PLAN.md`. You don't need to read those to work.

## The project in five sentences
You are writing a paper on Dolgan, a Turkic language of northern Siberia with about 1,000 speakers. You use two public corpora from the University of Hamburg: recorded Dolgan texts, and Evenki texts for comparison. Every word in these texts is already split into morphemes and glossed. Claude prepares the data so that your time goes into reading sentences and making linguistic judgments. There are two studies: **A** (evidentiality, which you two lead by hand) and **B** (whether case use differs between older and younger speakers, which Claude builds and you review).

## Who does what

| | You two | Desktop Claude (Jude's computer) | Web Claude (this team account) |
|---|---|---|---|
| Downloads, runs code on the real corpus | triggers it | does it | writes the code |
| Reads papers, makes linguistic calls | **you** | no | helps search and summarise |
| Codes evidentiality sentences | **you** | no | builds the sheet and checks agreement |
| Case-change analysis | reviews | runs it | designs and writes it |
| Decides what counts as what | **you** | no | proposes, with reasons |

The two Claudes cannot talk to each other. They pass work through files in `handoff/`, and **you are the trigger** each time. See "The loop" below.

## Phases

Time estimates are guesses. Revise them after Phase 3.

### Phase 0: Setup (about 1 to 2 hours)
- Jude: add Dustan as a collaborator on the GitHub repo (Settings, then Collaborators).
- Dustan: accept the invite. You can read everything on the GitHub website without installing anything.
- Make a shared Zotero group library for papers, and an Overleaf project for the paper (or a Google Doc for early notes).
- **Done when:** both of you can open the repo and the shared library.

### Phase 1: Get the data (about 30 to 60 minutes of Jude's time)
- Jude opens the desktop app, pastes the starter prompt (given at the end of the chat where this repo was built, and saved as `handoff/START_PROMPT_DESKTOP.md`), and lets it do tasks 001 and 002.
- Then tell web Claude: "Pull the repo and read handoff 001 and 002."
- **Claude does:** download the two corpora, check them, inspect their real structure, then write the parser.
- **Done when:** `data/MANIFEST.json` exists and `handoff/002` is `done`.

### Phase 2: Read and scope (parallel with Phase 1; about 6 to 10 hours each)
Start now. It doesn't need the data. Reading list, in this order:

| Read | For | Where |
|---|---|---|
| Däbritz (2023), "Dolgan", *Journal of Endangered Languages* | The best short description of Dolgan, including evidentiality, case and object marking | https://dergipark.org.tr/tr/download/article-file/3631398 (open) |
| Däbritz (2022), *A Grammar of Dolgan*: §6.6 evidentiality and §4.2 case | What is already described. **Study A depends on §6.6.** | Brill. A Zenodo copy may exist (record 8232753; check) |
| INEL Dolgan Corpus documentation (PDF) | How the corpus is built | https://s3-uhh.lzs.uni-hamburg.de/gwiss-inel-corpora/remote/dolgan-2.0/documentation/INEL_Dolgan_Corpus.pdf |
| Siegl (2015), *Linguistica Uralica* 51(4) | The dative-to-instrumental claim (Study B) | https://digar.ee/arhiiv/en/download/230696 |
| Sheifer and Bolshakova (2023), workshop slides | The closest competitor on object marking | https://blogs.helsinki.fi/language-diversification-and-spread-north/files/2023/09/Sheifer-DOM-in-DLG.pdf |
| `docs/LITERATURE_LEDGER.md` | What is already done and what is only "probably open" | this repo |

Each of you writes one page: *what does §6.6 say about Dolgan evidentiality, and what would a corpus study add?* Compare your pages.

Also send **one short email** to the INEL team (inel@uni-hamburg.de) saying what you plan and asking whether anyone is already working on Dolgan evidentiality or case change. Ask Claude to draft it. Researchers expect this, and it is how you learn about work in press.

- **Done when:** both one-pagers exist and the email is sent.

### Phase 3: Gate 0, "is there enough data?" (about 1 hour, after Phase 1)
Claude produces `reports/gate0_feasibility.md`: how many speakers have birth years, how many sentences of each kind exist, and whether age is tangled up with recording source. **You read it and decide**, for each study: go, go with a narrower question, or switch to a backup.

This is a stop sign, not a formality. The honest outcome is sometimes "the data can't answer this".

### Phase 4: Make the codebook (about 4 to 6 hours together, Study A)
- Claude gives you a pilot sheet of about 30 to 50 sentences containing candidate evidential forms.
- You each code them **independently**, then compare and argue. Revise the categories (`evidentiality/PLAN.md` has a strawman to push against).
- Repeat if you still disagree a lot. This is Gate 2.
- **Also here:** you sign off the gloss map, a table saying which Dolgan and Evenki labels count as the same thing. Claude drafts it with reasons.
- **Done when:** you agree on the categories and the disagreements are about edge cases, not about what the categories mean.

### Phase 5: Annotate (Study A; about 5 to 10 hours each, depending on counts)
- Claude builds the main sheet in random order with a hidden overlap so agreement can be measured.
- You code your sheets. Don't edit the ID columns.
- Disagreements go into a third file and you settle them.
- **Done when:** the data is frozen and tagged `data-v1`.

### Phase 6: Analyse and write
- Study B: Claude runs the analysis it planned before seeing results. You check examples, argue with the interpretation, and write the linguistics.
- Study A: Claude runs the counts. You interpret.
- Before submitting: re-check the literature (Sheifer, the INEL team), email again, archive the code and data (Claude prepares it).

## The loop (how a handoff works)
1. One Claude writes a task file in `handoff/`.
2. Jude opens the **other** Claude and says: "Pull the repo, read CLAUDE.md and PLAN.md, then do the open tasks in handoff/ addressed to you."
3. It does the work and writes the results in the same file.
4. Jude goes back to the first Claude: "Pull and read handoff/NNN."

Each round takes a minute or two of your time. Keep tasks small.

## Decisions only you can make
| Decision | When |
|---|---|
| Whether each study survives Gate 0 | Phase 3 |
| Evidentiality categories | Phase 4 |
| What counts as the "same" case or tense across Dolgan and Evenki (the gloss map) | Phase 4 |
| Speaker age groups (cohort bins) | before analysis |
| One paper or two | before writing |
| Authorship and acknowledgements. Discuss early, in writing. | before writing |
| Licences, once you know what you'll release | before release |

Open decisions are logged in `docs/DECISIONS.md`.

## What could go wrong, honestly

| Problem | What it would mean | What we do |
|---|---|---|
| Speaker age and recording source are tangled together | We can't say whether a difference is about age or about how the text was collected | Gate 0 measures it; we control for source; we say so in the paper |
| Secondary predicates (Study B, first question) are too rare | That question can't be tested | Count first; report descriptively or drop |
| Someone publishes first (Sheifer on object marking; the INEL team) | Study B's object-marking question loses novelty | Frame around age; check before submitting; email early |
| "Open" turns out to be "someone did it in a source we couldn't reach" | We repeat existing work | The ledger lists what we couldn't read; Phase 2 reading closes the gaps |
| The corpus glossing is inconsistent in places | Wrong counts | Claude flags anything it can't align; sources are controlled |
| Evenki labels don't match Dolgan labels | The comparison is apples and oranges | The gloss map, signed off by you |
| Handoffs stall | Slow progress | Keep tasks small; trigger promptly |

## Words you'll see
- **Corpus:** a collection of recorded and transcribed texts.
- **INEL:** the Hamburg project that built these corpora.
- **`.exb`, `.coma`:** EXMARaLDA file types: `.exb` is a transcript, `.coma` holds the speaker and text metadata.
- **Tier:** one layer of annotation in a transcript (the word, its morphemes, its glosses, its translation, and so on).
- **Token:** one running word in the texts (so "the" twice is two tokens).
- **Gloss:** the interlinear label under a morpheme (`ACC`, `PST`).
- **Apparent time:** comparing speakers of different ages at one moment as a stand-in for change over time. It assumes that older speakers reflect an earlier state of the language.
- **Cohort:** a group of speakers born in the same period.
- **Random effect, "speaker as a cluster":** the statistical way of saying that sentences from one person are not independent evidence.
- **Cohen's kappa:** a measure of how much two coders agree beyond chance.
- **Gate:** a checkpoint at which you decide whether to continue, narrow, or switch.
- **Frozen data (`data-v1`):** a tagged snapshot that analysis reads, so results stay reproducible.
- **DOM:** differential object marking, where an object is marked differently depending on properties such as definiteness or clause type.
- **Ledger:** `docs/LITERATURE_LEDGER.md`, our record of what was checked and what could not be.

## Where to look
- Current status: `PLAN.md`
- What Claude is working on: `handoff/README.md` (task table)
- What was checked in the literature: `docs/LITERATURE_LEDGER.md`
- The real structure of the data: `docs/CORPUS_NOTES.md`
