# Starter prompt for desktop Claude

Paste everything below the line into the Claude desktop app (the one linked to the personal Pro account, with the folder for this repo connected).

---

I'm working on a corpus linguistics project with a partner. The repo is https://github.com/judecutler/DolganResearch. You are the "desktop Claude": you run the things that need network access or permissions on my computer (downloads, packages, running code on the real data, committing results). A second Claude, "web Claude", works from claude.ai on planning and code. You can't see its chats and it can't see yours, so the repo is our only shared memory.

Please do this now:

1. Clone the repo into the connected folder, or `git pull` if it is already there.
2. Read `CLAUDE.md`, then `PLAN.md`, then `handoff/README.md`.
3. Do handoff task `handoff/001-environment-and-download.md` step by step. It downloads two public corpora (INEL Dolgan 2.0 and INEL Evenki 2.0) from Universität Hamburg and records the versions. Do not install any packages in this task; just report what is installed.
4. If task 001 succeeds, do `handoff/002-inspect-structure.md` as well. It answers a fixed list of questions about the real file structure.
5. Fill in the Results section of each task file, update the status table in `handoff/README.md` and `PLAN.md`, then commit and push.

Rules to keep in mind (the full list is in `CLAUDE.md`):
- Never commit the corpus files (`.exb`, `.exs`, `.coma`, `.wav`, `.mp3`, `.zip`, or anything under `data/raw/`). `.gitignore` already blocks them, but check `git status` before each commit.
- Do not invent anything. If a number, label or file isn't what the task expects, say so in the Results and set the task to `blocked`. Don't guess and carry on.
- Excerpts of corpus text in your reports must be 30 lines or fewer, each with its source file named.
- Do not put speaker names or personal details in anything you commit.
- If a checksum doesn't match, stop and tell me.

When you're finished, tell me in a few lines what you did, what surprised you, and whether anything is blocked. Then I'll pass the results to web Claude.
