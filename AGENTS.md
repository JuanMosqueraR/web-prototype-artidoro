# AGENTS.md

# Artidoro Hero Lab — Agent Instructions

This repository is a visual and interaction laboratory for a possible redesign of Artidoro Rodríguez Coffee. It is NOT the production website.

The experiment compares two independent creative directions (A and B) with a shared commercial product under comparable conditions. What is being compared, and with what, is defined in `docs/PROJECT_BRIEF.md` and `docs/DECISIONS.md`, not here.

This file holds durable, tool-neutral rules. Facts that change (observed problems, environment details, asset inventory, current phase) live in `docs/`.

## Source of truth

Read in this order, stopping when the task is covered:

1. `AGENTS.md` and `docs/DECISIONS.md` — always.
2. The docs the task needs:
   - `docs/PROJECT_BRIEF.md` — scope and shared product;
   - `docs/CREATIVE_DIRECTIONS.md` — implemented behaviour of A and B;
   - `docs/ASSET_AUDIT.md` and `audit/assets.json` — assets and provenance;
   - `docs/IMPLEMENTATION_STATUS.md` and `README.md` — stack, commands, limits;
   - `docs/KNOWN_ISSUES.md` — observed problems (not a backlog).
3. The code and evidence the task touches (`index.html`, `src/`, `public/`, `audit/`, `qa/`, `deliverables/`) and `git log`.

Each source answers one question:

- What MAY change → `docs/DECISIONS.md`.
- What it DOES today → the code. Docs are dated snapshots and can be stale.
- WHY it exists → `docs/PROJECT_BRIEF.md`.

If docs and code, or two docs, disagree: do not fix either side silently. Report both locations and follow `docs/DECISIONS.md` for what is allowed.

Explicit instructions and approvals given in the current task can be used directly; they do not have to be recorded first. The persistence rule applies to durable facts, decisions, constraints and context that must survive future sessions: if such information exists only in a conversation, ask for it to be recorded in the repo (or propose the text) so that later sessions do not depend on it. Do not rely on chat history when the repository can answer.

## Scope

Never, whatever the approval: invent, or present as fact, any claim, award, certification, metric, origin, provenance or other factual statement, or leave out its source so that an unverified statement reads as fact. The user may approve adding factual copy, but that copy must have provenance (see *Assets and copy*).

Do NOT, without explicit approval:

- choose a winning direction or merge A and B into a hybrid (L01, O01);
- continue into a homepage, PDP, PLP, cart, checkout or Shopify work (L02, L14, O06);
- generate AI imagery (L11, O05);
- redraw, reconstruct or complete brand artwork (Class 4; see *Assets and copy*);
- change a LOCKED decision, or resolve an OPEN one.

Also:

- **A finding is not a task.** When you notice a defect, discrepancy, stale doc or possible improvement outside your task, report it (what, where, evidence, conditions) and stop. Do not fix it "while you are here". Entries in `docs/KNOWN_ISSUES.md` and the limits in `docs/IMPLEMENTATION_STATUS.md` are observations, not an approved backlog.
- Do not refactor or reformat unrelated code during a focused task.
- Do not chain tasks or start a next phase. After the requested work, report and stop. The next phase is not assumed.
- Technical constraints are in `docs/DECISIONS.md` (L10). The lab should not establish patterns obviously unsuitable for ecommerce, and the base experience must stay understandable with reduced motion.

## Decisions

The user holds the authority to change a LOCKED item, resolve an OPEN item, change phase or scope, and choose A vs B. An agent never originates, reinterprets or infers such a decision.

- An agent may record in `docs/DECISIONS.md` a decision the user has just explicitly approved in the current task. It may change an item's documentary status only when the current instruction explicitly orders that change. It preserves the user's intent and scope literally, without broadening, narrowing or paraphrasing them. The user is not required to edit `docs/DECISIONS.md` by hand.
- To record a decision, append the next ID with date, wording, scope and a note of the approval. Never delete or rewrite existing rows; mark superseded ones with a reference.
- If a requested change conflicts with a LOCKED decision, do not override it silently: identify the conflict and get explicit approval first.
- **Exploration is not a decision.** Prototypes, proposals, audit findings, screenshots and code that happens to exist are exploratory until the user says otherwise. Nothing becomes LOCKED because it was built, committed or documented. Values found in code are the implemented baseline, not brand specifications.

**Explicit approval** is a clear instruction from the user, in the current task, naming the change. Silence, a related request, or approval of something else is not approval, and approval covers only what it names.

## Change classes

| Class | Examples | Rule |
|---|---|---|
| 0 Inspect | reading; exploratory QA with artifacts kept outside tracked files | free |
| 1 Describe | docs that describe the current state without changing authority, intent, scope, rules, or LOCKED/OPEN status | allowed within task scope |
| 2 Tooling | scripts, config, dependency/engine declarations, ignore rules, with no change to what A/B render | ask first; state what it writes |
| 3 Baseline | anything that changes what A or B render or how they behave | explicit approval; checkpoint commit first; regression QA after |
| 4 Assets / claims | adding, replacing, modifying, reprocessing or removing an asset, or factual copy | explicit approval and a provenance record; regression QA only if it changes what is rendered or the visible behaviour |
| 5 Decisions and governance | LOCKED/OPEN items, phase, scope, A vs B; changes to `AGENTS.md`, `CLAUDE.md`, authority rules, change classes, contractual scope or decision governance | the user decides; explicit approval required |

Workflow for non-trivial work:

1. Inspect the relevant docs and code.
2. Classify the change.
3. Class 2–5: state the intended change and wait for approval, unless the current request already gives that explicit approval; do not ask twice. The Git checkpoint rule still applies. Class 0–1: proceed within the task.
4. Change only what was approved. If an approved change makes docs stale, update the docs it invalidates in that same change (descriptive updates are Class 1; anything that changes rules or scope is Class 5). Flag stale snapshots.
5. Validate at the QA level that applies (below).
6. Report (see *Working across agents*).

## A/B comparison integrity

A and B must remain comparable. These are principles; the values belong to the implementation and to `docs/CREATIVE_DIRECTIONS.md`.

1. **Parity of evidence.** Any check, capture or measurement made on one direction is repeated on the other, under the same viewport, state and conditions, before any comparative statement.
2. **Contract vs observation.** Baseline conditions define the contract. Results outside them are observations: they do not redefine the specification, but they must be reported and they matter for any judgement made under those conditions.
3. **Conceptual vs unclassified differences.** A difference is conceptual when the docs record it as part of a direction's thesis. Any other difference between A and B (for example in copy, motion, weight, resource loading or asset finish) is a potential confound until the user or the documentation classifies it. Report it. Do not correct, equalise, hide or exploit it automatically.
4. **Provisional finish must not decide the concept.** Never judge a thesis on the finish of a provisional asset alone, and never compensate for a weak asset by changing the concept.
5. **Evidence declares its conditions.** Every visual or QA result states viewport, pixel ratio, browser or tool, keyframe/state, motion setting, what was loaded, and what it does not cover. Comparisons of weight or performance state what was loaded.
6. A change to one direction states whether the other needs an equivalent, and asks. Do not polish one direction substantially more than the other unless asked.
7. Shared commercial elements defined in the docs (product, CTA, trust signal) stay shared; keep product visibility and interaction availability as documented.

## QA

- **Baseline QA:** the reference viewports (L09) — desktop 1440 × 900 and mobile 390 × 844 — both directions, both keyframes, motion on and off. This is a QA contract, not a support claim for other sizes. Mobile is its own composition, not a scaled desktop. Baseline evidence in `qa/` is never overwritten; new evidence is added with date and conditions.
- **Regression QA:** after an approved Class 3 change, or a Class 4 change that affects what is rendered or the visible behaviour, repeat baseline QA on every affected direction, and on the counterpart when shared elements or parity are involved. Compare with `qa/measurements.json` and report deltas.
- **Exploratory QA:** any other viewport, browser, pixel ratio, state or tool. Observations only. They do not redefine the specification and do not create tasks. Keep the captures outside tracked files (git-ignored `qa/draft-*`, or a scratch directory).

Before reporting a capture, confirm it shows the intended layout viewport. Snapshots (captures, `deliverables/`, measurements and any other visual snapshot) describe the state when they were made. A Class 3 change, or a Class 4 change that affects what is rendered, can make them stale; a Class 4 change that does not affect what is rendered does not require regenerating them. Flag stale snapshots, and regenerate only when approved.

## Environment and reproducibility

Do not assume documented commands work on the machine in front of you.

- Before running project commands, dev servers, builds, exporters, asset-processing scripts, or any command whose result or writes depend on the environment, check tool versions against what `package.json` and the lockfile require, the OS, the locale/encoding, and what the command writes. Read-only commands such as `git status`, `git diff`, `git log` and reading files need no environment check.
- Report mismatches. Do not work around them by editing project files, installing or upgrading tooling, or changing system settings without approval (Class 2).
- Some scripts write to tracked baseline files (regenerated deliverables, prepared assets). Read a script and its outputs before running it, and run it only with approval and after a checkpoint.
- A command that worked in a previous environment is not evidence that it works here.
- Prefer read-only verification (in-memory regeneration, scratch output) to confirm claims about the baseline.
- Environment problems are recorded, not fixed inside an unrelated task.

## Assets and copy

- **Canonical record.** `audit/assets.json` is the canonical record of structured asset facts: source, original dimensions, preparation, classification/status and technical provenance. `docs/ASSET_AUDIT.md` is the human summary: classification, uncertainties, gaps and implications, linking to the canonical record. Do not duplicate structured values between them.
- Respect the classes defined in `docs/ASSET_AUDIT.md` (`REAL_ASSET`, `USABLE_WITH_PREPARATION`, `MISSING_ASSET`) and keep the `PROVISIONAL_ASSET` notices. Remove a notice only when the user confirms its gap is closed (L12).
- Never treat a generated or provisional asset as official material. If an asset is missing, report the gap before substituting it. Do not substitute silently.
- Derived assets must be reproducible from a source in `audit/source/` and a script in `scripts/`, or be declared manual. Do not reconstruct, redraw or complete brand artwork without explicit approval (Class 4), and never present the result as `REAL_ASSET` or official material. AI-generated imagery is governed by L11 and O05: it stays blocked until the user resolves O05, and would need its own classification; it is never `REAL_ASSET`.
- Adding, replacing, modifying, reprocessing or removing an asset is Class 4. Record the structured facts in `audit/assets.json` and update the summary in `docs/ASSET_AUDIT.md`.
- **Factual copy** (origin, altitude, tasting notes, roast cadence, locations, product claims) is Class 4 and must trace to the real product page or label, or to a source recorded in `audit/assets.json`. No approval waives this (see *Scope*). If copy and the real product label differ, report it. Do not choose one silently.
- New derived files or variants (exports, builds) declare how they were produced, or are marked manual, and are added to the structure table in `docs/IMPLEMENTATION_STATUS.md` in the same change.

## Git

History is the project record and, while there is no remote, the only backup.

- Never rewrite it: no rebase or amend of past commits, force operations, `reset --hard`, `clean`, or `checkout --` on files you did not create.
- Do not add remotes, push, rename or delete branches, or create or move tags without approval. Do not assume a `main` branch exists; check.
- Commit only when asked. One concern per commit (governance, tooling, rendering, assets, QA evidence), with a descriptive message and no unrelated files.
- Start every task with `git status`. Changes you did not make are not yours to touch; report them. End with a clean tree, or list what is uncommitted. One agent per working tree at a time.
- Before an approved Class 3 or 4 change, the current state must be committed so it can be restored (ask for the commit if it is not already authorized). The baseline commit `59320ee` ("baseline: Astra Work Hero Lab") is the reference for L13.
- Do not commit generated junk, secrets, credentials, local environment files, or exploratory captures.

## Working across agents

Claude Code and Codex alternate on this same repository.

- **The repo is the shared memory.** No agent can assume context from another agent's chats, private memory or prior sessions.
- Findings and important decisions must end up in the repo (with approval) or in the end-of-task report for the user to review. Do not leave them only in a conversation.
- Match effort to the task. Inspection, QA, documentation upkeep and small approved changes should be done without escalating. Recommend, never self-escalate to, a higher-cost agent for work that spans both directions' layout logic, reconciles LOCKED decisions with observed behaviour, or designs tooling or reproducibility changes.
- Open creative decisions belong to the user, not to any agent. Prepare options and evidence; do not choose.

End-of-task report: files changed; validation performed and its conditions; what was NOT covered; findings not acted on; new gaps; whether a LOCKED or OPEN item needs the user's review.

## Instruction files

`AGENTS.md` holds tool-neutral rules. Tool-specific files (such as `CLAUDE.md`) add only what is specific to that tool and must not contradict this file. Project facts, design behaviour, assets, decisions and observed issues live in `docs/` and are referenced, not copied. Instruction files do not hold project history or mutable state.
