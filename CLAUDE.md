# Instructions for Claude sessions in this repo

## Project
Two linked studies on Dolgan (Turkic, Taymyr), using the INEL Dolgan Corpus 2.0 and INEL Evenki Corpus 2.0 (Hamburg):
- **Study A, evidentiality**: Jude and Dustan annotate by hand. Claude prepares the data.
- **Study B, case change across speaker generations**: Claude builds the computational pipeline. Humans review.

Jude and Dustan are linguists who have not run a corpus project before. Explain choices briefly and say what you are unsure of.

## Two Claude sessions
- **Web Claude** (claude.ai, team account): planning, writing code, analysis design, literature checks. It cannot download from the web, cannot install packages, and has never seen the real corpus. It tests only on synthetic fixtures.
- **Desktop Claude** (Claude desktop app, Jude's personal account): runs anything that needs network or permissions: downloads, packages, running code on the real corpus, committing results.
- The sessions cannot see each other's chats. **This repo is the only shared memory.**

## At the start of every session
1. `git pull`.
2. Read `PLAN.md`.
3. Read every file in `handoff/` that is addressed to you and whose Status is not `done`.
4. Do the work. Write results into that task file's Results section, set its Status, update `PLAN.md`, commit, push.

## Rules
1. **Never commit corpus files**: `.exb`, `.exs`, `.coma`, `.wav`, `.mp3`, `.zip`, or anything under `data/raw/`. Short excerpts (at most 30 lines, with attribution) may go in `handoff/outputs/`.
2. **Never invent linguistic data, glosses, citations or numbers.** If you did not read it in the corpus or a source, say so. Mark anything unchecked `UNVERIFIED`.
3. **Every claim that something is unstudied needs a record** in `docs/LITERATURE_LEDGER.md`: the queries run (at least 4, at least one non-English), the closest work found, and why it does not fill the gap.
4. **If blocked or unsure, set the task to `blocked` and write down exactly what you saw.** Do not guess and carry on.
5. **Stay in your folders.** Web Claude owns `shared/`, `case_change/`, `docs/`. Humans own `evidentiality/` and `annotations/`. Desktop Claude owns `reports/`, `data/MANIFEST.json`, and `handoff/outputs/`. To change something outside your folders, open a handoff task.
6. **Stdlib-first Python.** Parsers use `xml.etree` and `csv` so they run without installs. Analysis may use pandas and statsmodels, and R for mixed models (decision D-005, still open).
7. **Parsers need tests**: synthetic fixtures for web Claude, real-data spot checks for desktop Claude. Counts must reconcile with the corpus documentation (see `docs/CORPUS_NOTES.md`) or the discrepancy must be explained.
8. **Treat each speaker as a cluster.** Tokens from one speaker are not independent. Do not report token-level p-values without speaker-level structure.
9. **Privacy:** derived tables use speaker IDs and birth year only. No names, family details or coordinates.
10. **Pull before you push.** Small commits. Do not rewrite history. Do not force-push.
11. **Large outputs go to files, not chat.** Put reports in `reports/` or `handoff/outputs/NNN/` and summarize in a few lines.
12. Record any new decision in `docs/DECISIONS.md`.

## Commit messages
Short imperative subject. End with the attribution lines your environment gives you.
