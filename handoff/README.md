# handoff/

How the two Claude sessions pass work to each other. They cannot see each other's chats, so everything goes through files here.

## The loop

1. The sender writes a task file `NNN-short-slug.md` from `TEMPLATE.md`, commits and pushes.
2. Jude tells the other Claude: *"Pull the repo, read CLAUDE.md and PLAN.md, then do the open tasks in handoff/ addressed to you."*
3. The assignee does the work and fills in the **Results** section of the same file. It sets Status and pushes.
4. Jude tells the sender: *"Pull and read handoff/NNN."*

Neither Claude can wake the other. Jude is the trigger each time.

## Status values

| Status | Meaning |
|---|---|
| `todo` | Written, nobody has started. |
| `in-progress` | Assignee has started. |
| `done` | Acceptance checks all passed. Results filled in. |
| `blocked` | Assignee could not finish. Results say exactly what was seen. The sender decides what happens next. |
| `needs-human` | A decision or action only Jude or Dustan can make. Results say what is needed. |
| `blocked-by-NNN` | Cannot start until task NNN is `done`. |

## Rules

- The sender edits the task body until it is `in-progress`. After that, only the assignee edits the Results section. Changes to the task go in a new task.
- If something is unclear or surprising, set `blocked` and describe it. Do not guess and carry on.
- Big outputs go in `handoff/outputs/NNN/`: keep each file small (under about 200 KB). Corpus text excerpts are limited to 30 lines per file, with attribution to the corpus.
- Never put corpus files, audio, or personal information about speakers in `handoff/`.
- Keep task files short. If a task has more than about eight steps, split it.

## Tasks

| ID | Task | Assignee | Status |
|---|---|---|---|
| 001 | [Environment check and corpus download](001-environment-and-download.md) | desktop Claude | done |
| 002 | [Inspect real corpus structure](002-inspect-structure.md) | desktop Claude | done |
| 003 | [Run the data pipeline on the real corpora](003-run-pipeline.md) | desktop Claude | done |
| 004 | [Decisions, reading and one email](004-for-jude-and-dustan.md) | Jude, Dustan | needs-human |
| 005 | [Check Stapert (2013) for case counts by age](005-check-stapert-thesis.md) | desktop Claude | done |
| 006 | [Rerun after the 003 fixes; check the BOR events](006-rerun-and-bor-check.md) | desktop Claude | done |
| 007 | [Rerun with the adjusted B2 design report](007-design-report.md) | desktop Claude | done |
| 008 | [Run Study C; fetch two papers](008-study-c-and-two-papers.md) | desktop Claude | done |
| 009 | [Run the Study A gloss descriptives](009-study-a-descriptives.md) | desktop Claude | done |

Update this table whenever a status changes.

The very first session of the desktop Claude starts from [`START_PROMPT_DESKTOP.md`](START_PROMPT_DESKTOP.md).
