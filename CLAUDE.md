@AGENTS.md

# CLAUDE.md

Claude Code specifics only. `AGENTS.md` (imported above) holds the project rules, including authority, change classes, findings and reporting; if anything here conflicts with it, `AGENTS.md` wins.

## Approval mechanism

Where `AGENTS.md` requires approval before a change, use plan mode, or propose and wait. Class 0–1 work proceeds within the task's scope.

## Visual inspection

- Use the dev server only if the environment check from `AGENTS.md` passes. Otherwise inspect `deliverables/*.html`, first confirming they still match `src/` by re-deriving the export in memory or scratch output. Do not run the export script for this.
- Use an installed Chromium-based browser in headless mode at pixel ratio 1.
- For narrow widths, load the page in an exact-width iframe from a scratch wrapper page, as `qa.html` does. In the environment where this was observed, a narrow headless window was widened and then cropped (see KI-73 in `docs/KNOWN_ISSUES.md`). Do not assume that applies elsewhere; check that the captured viewport is the one you intended.
- Cover both directions and both keyframes at the baseline viewports; `?frame=b` opens the expanded state. Label anything else exploratory and state its conditions.
- View captures with the image reader.

## Scratch files, memory and cost

- Put temporary scripts and exploratory captures in the session scratchpad or another location outside tracked files. Never in the repository.
- Claude's chat and auto memory are invisible to Codex. Do not keep project state or decisions there.
- Do not spawn subagents unless the task warrants it, and say why.

## Stopping

Stop at the requested checkpoint. Propose a next step if useful, then wait.
