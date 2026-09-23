# CLAUDE.md

# Claude Code Instructions — Artidoro Hero Lab

Before working in this repository, read `AGENTS.md`.

Then read all files under `/docs`, especially:

- `docs/PROJECT_BRIEF.md`
- `docs/CREATIVE_DIRECTIONS.md`
- `docs/ASSET_AUDIT.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/DECISIONS.md`

## Working style

This repository already contains an implemented Hero Lab.

Do not assume the task is greenfield.

Inspect existing code before proposing replacements.

Prefer editing the current implementation over rebuilding it unless the user explicitly requests a rewrite.

Keep changes tightly scoped.

Do not proactively:
- redesign;
- combine creative directions;
- add sections;
- migrate frameworks;
- introduce large dependencies;
- generate substitute brand assets;
- continue toward a production ecommerce.

## Visual work

When modifying visuals or interaction:

- preserve the documented creative intent;
- validate desktop 1440×900;
- validate mobile 390×844;
- check both interaction states where relevant;
- preserve reduced-motion behavior;
- report visual regressions or compromises explicitly.

Do not compensate for a weak asset by silently changing the creative concept.

## Documentation

If implementation changes invalidate repository documentation, update the relevant `/docs` file in the same task.

Do not duplicate project history inside this file.

`AGENTS.md` and `/docs` remain the source of truth for project rules and decisions.

## Completion

At the end of a task, summarize:

- what changed;
- what was tested;
- what remains provisional;
- whether any `OPEN` decision now requires user review.

Stop at the requested checkpoint.