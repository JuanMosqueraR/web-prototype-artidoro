# AGENTS.md

# Artidoro Hero Lab — Agent Instructions

This repository is a visual and interaction laboratory for a possible redesign of Artidoro Rodríguez Coffee.

It is NOT yet the production website.

## Source of truth

Before making changes, read:

1. `README.md`
2. `docs/PROJECT_BRIEF.md`
3. `docs/CREATIVE_DIRECTIONS.md`
4. `docs/ASSET_AUDIT.md`
5. `docs/IMPLEMENTATION_STATUS.md`
6. `docs/DECISIONS.md`

Also inspect:

- `audit/`
- `qa/`
- `src/`
- `public/`
- recent Git history

Do not rely on chat history when repository documentation or implementation is available.

## Current experiment

The Hero Lab compares two independent creative directions:

- A — Perú, en profundidad
- B — Fuera de la lata

Both use the same commercial reference product:

- Café Amazonas
- 250 g
- Rodríguez de Mendoza
- Notes: naranja y melaza

The purpose is to compare the directions under similar conditions before choosing whether either deserves further development.

## Important constraints

Do NOT:

- choose a winning direction unless explicitly asked;
- merge A and B into a hybrid without explicit approval;
- continue into a full homepage without explicit approval;
- build PDP, PLP, cart, checkout, or Shopify integration unless explicitly requested;
- silently replace provisional assets;
- treat generated or provisional assets as official Artidoro material;
- invent claims, awards, reviews, certifications, origin data, or business facts;
- change locked creative decisions merely to make implementation easier;
- refactor unrelated code during focused tasks.

## Assets

Respect the classifications documented in `docs/ASSET_AUDIT.md`:

- `REAL_ASSET`
- `USABLE_WITH_PREPARATION`
- `MISSING_ASSET`

Known gaps include provisional visual material. Always preserve that distinction.

If an asset is missing, report the gap before substituting it.

## Visual comparison integrity

A and B must remain comparable.

When working on both:

- maintain equivalent implementation quality;
- test the same breakpoints;
- avoid polishing one substantially more than the other unless explicitly requested;
- preserve CTA, product visibility, trust signal, and interaction availability where documented.

## Responsive targets

Primary validation targets:

- Desktop: 1440 × 900
- Mobile: 390 × 844

Do not treat mobile as a scaled desktop composition.

## Performance principles

This is a visual lab, but it should not establish patterns that are obviously unsuitable for ecommerce.

Prefer:

- HTML/CSS;
- lightweight transforms;
- SVG where appropriate;
- optimized images;
- progressive enhancement.

Avoid heavy dependencies, WebGL, autoplay video, or large visual payloads unless clearly justified.

The base experience should remain understandable with reduced motion.

## Workflow

For non-trivial work:

1. inspect relevant documentation and code;
2. describe the intended change briefly;
3. modify only the necessary files;
4. run appropriate checks;
5. inspect desktop and mobile when visual behavior changes;
6. report:
   - files changed;
   - validation performed;
   - known limitations;
   - any new decision or gap discovered.

## Git

Treat the current Git history as part of the project record.

Do not rewrite history.

Prefer small, descriptive commits.

Do not commit generated junk, secrets, credentials, local environment files, or temporary screenshots unless they are intentionally part of QA documentation.

## Decision handling

Use `docs/DECISIONS.md`.

If a requested change conflicts with a `LOCKED` decision:

- do not silently override it;
- identify the conflict;
- request or document explicit approval before changing it.

Do not resolve `OPEN` decisions autonomously unless explicitly asked.

## Current project phase

The current phase is:

Hero Lab validation.

The next phase is NOT assumed.

Do not automatically continue into homepage implementation after completing a task.