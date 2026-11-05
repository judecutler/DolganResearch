# shared/

Code used by both studies: reads the raw INEL files and writes the cleaned tables described in [`docs/DATA_PREP_PLAN.md`](../docs/DATA_PREP_PLAN.md).

Owner: web Claude. Nothing is built yet. Planned layout (work packages WP3 to WP8 in [`docs/ROADMAP_CLAUDE_WEB.md`](../docs/ROADMAP_CLAUDE_WEB.md)):

```
shared/
  inel/               parser package (stdlib only): coma.py, exb.py, tiers.py, tables.py
  config/
    tiers.yaml        tier names and aliases (e.g. BOR-Phon / BORphon)
    gloss_map.yaml    gloss label -> analysis category (needs human sign-off)
  tests/
    fixtures/         small synthetic EXMARaLDA files (made-up content, real structure)
  build_tables.py     command-line entry point
```

Nothing here is written until handoff task 002 returns the real file structure.
