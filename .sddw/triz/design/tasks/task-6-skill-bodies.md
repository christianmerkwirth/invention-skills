# Task 6: Author the five canonical TRIZ skill bodies

## Trace
- **FR-IDs:** FR-01, FR-02, FR-03, FR-07, FR-08, FR-09, FR-10, FR-11, FR-12, FR-15
- **Depends on:** task-1, task-2, task-3

## Files
- `skills/triz-reference.md` — create
- `skills/triz-contradiction.md` — create
- `skills/triz-design-audit.md` — create
- `skills/triz-refactor.md` — create
- `skills/triz-sprint.md` — create

## Architecture

### Components
Each skill is a single canonical Markdown file consumed by the installers. The skill body is plain Markdown instructions for an LLM — no tool-specific syntax, no code execution, no embedded JSON. References to data files use relative paths (`reference/parameters.md`) that resolve at runtime in both Claude Code and Gemini CLI install layouts.

### The shared runtime protocol (every skill follows this)
This protocol is defined once in the README (task-8) and each skill body invokes it. The skill body does NOT re-state the full protocol — it references it and adds its skill-specific reasoning.

1. **Receive input.** Parse what the user gave (parameter names, module path, backlog item, etc.).
2. **Load reference.** Read only the reference files this skill needs (e.g., `parameters.md`, `principles.md`, `matrix.json`).
3. **Reason.** Identify the inventive principle(s), parameter(s), and the contradiction. Cite by ID and name.
4. **Honest gap.** If no strong match in the matrix, report the gap, list what was tried, and STOP. Do not force-fit. (FR-09)
5. **Propose.** Present the proposed change (diff for refactors, plan for audits, ranked options for sprint).
6. **Confirm.** Pause and ask the user explicitly to confirm. Do not proceed until they reply. (FR-08)
7. **Apply within scope.** If confirmed, edit only files within the user-named module. (FR-10) Confirm separately before each destructive op. (FR-12) Do not introduce new major dependencies. (FR-11)

## Contracts

### Canonical frontmatter (per task-3 schema)
Every skill file MUST conform to:
```yaml
---
name: triz-<purpose>
description: <one-line, present-tense, says what the skill does>
version: 0.1.0
tags: [triz]                  # optional
---
```
- `name` MUST equal the filename stem
- No frontmatter keys other than `name`, `description`, `version`, `tags`

### Body conventions
- Every skill body SHALL include sections: `## When to invoke`, `## Inputs needed`, `## Reference data used`, `## Procedure`, `## Output format`
- The `## Procedure` section SHALL invoke the shared runtime protocol's confirm-before-write rule explicitly: "Stop. Ask the user to confirm. Do not proceed until they reply."
- Bodies SHALL NOT mention "AskUserQuestion", "MCP", "tool calls", or any other tool-specific construct — these break FR-03

## Data Models

### Per-skill scope (what each one does)

#### `triz-reference` — TRIZ reference / tutor (FR-01 reference, FR-13)
Browses the 21 parameters, 40 principles, and GoF correlations interactively.
- **Inputs:** Free-text query ("show me principle 24", "what's parameter 16?", "explain the GoF Adapter mapping").
- **Reference loaded:** `parameters.md`, `principles.md`, `gof-mappings.md` (lazy — only what the query needs).
- **Procedure:** Resolve query → fetch matching entries → present with software analogy and cross-references.
- **No file edits.** This skill is read-only — does not write to user files. Skip the confirm-before-write step (nothing to confirm).

#### `triz-contradiction` — contradiction resolver (FR-01 contradiction, FR-07, FR-09)
The flagship skill: name two conflicting parameters, get ranked principles + a code-ready suggestion.
- **Inputs:** Two parameter names or IDs (improving, worsening), plus optional module/file scope.
- **Reference loaded:** `parameters.md` (resolve names → IDs), `matrix.json` (cell lookup), `principles.md` (expand each principle with its software analogy), `gof-mappings.md` (cite GoF pattern if any).
- **Procedure:** Resolve params → look up cell → if empty, FR-09 honest-gap response → if populated, present top 1–3 principles with rationale → propose a concrete code change scoped to the named module → confirm → apply.
- **Output:** Names the principle (ID + name), the two parameters, the contradiction in one sentence, then the diff.

#### `triz-design-audit` — design auditor (FR-01 audit, FR-14)
Reviews a proposed design or module to surface hidden contradictions and map them to GoF + TRIZ principles.
- **Inputs:** A design doc path, a module path, or a description of an architecture.
- **Reference loaded:** `principles.md`, `gof-mappings.md`, `matrix.json` (when audit surfaces a candidate contradiction).
- **Procedure:** Scan the design → enumerate suspected contradictions → for each, look up matrix → present principles + GoF pattern (when correlation exists per FR-14) → confirm → produce an audit report (no code edits unless user requests refactor).
- **Output:** Audit report listing contradictions found, principles considered, GoF patterns applicable, and recommended next steps.

#### `triz-refactor` — refactor assistant (FR-01 refactor)
Refactors a module by applying a chosen principle.
- **Inputs:** A module path AND either (a) a stated contradiction or (b) "audit for ideality gaps" (waste, complexity, harmful effects).
- **Reference loaded:** `principles.md`, `matrix.json` (if contradiction provided).
- **Procedure:** Identify ideality gaps OR resolve user-stated contradiction → propose refactor citing the principle → confirm → apply edits scoped to the module (FR-10) → confirm separately for any destructive op (FR-12) → do not add new major deps (FR-11).
- **Output:** Diff summary + principle citation + brief rationale.

#### `triz-sprint` — Agile'TRIZ sprint skill (FR-01 sprint, FR-15)
Two workflows in one skill: morphological matrix at backlog refinement, prototype-effects extraction at sprint review.
- **Inputs:** Backlog items (for morphological mode) OR a prototype description / completed feature (for effects-extraction mode).
- **Reference loaded:** `principles.md` for both modes; `matrix.json` only when effects-extraction surfaces a contradiction.
- **Procedure (morphological):** Reframe backlog items as contradictions → enumerate candidate principles per row → generate a bounded set of combined ideas (one selection per row) → name the principles each idea draws from. Present ideas; do not auto-apply.
- **Procedure (effects-extraction):** Take prototype → list positive effects → list harmful effects → reframe each harmful effect as a fresh contradiction (improving X / worsening Y) for next sprint. No code edits.
- **Output:** For morphological: a small ranked idea list with principle attributions. For effects-extraction: an updated contradiction backlog.

## Design Decisions

### One file per skill, no shared "library" body
- **Chosen:** Each skill is an independent file; the shared runtime protocol lives in the README, not in another skill
- **Rationale:** FR-02 requires each skill to be invokable independently with no central dispatcher. Bodies are kept tight by referencing (not duplicating) the protocol.
- **Rejected:** A "triz-base" skill that others import — there is no skill import mechanism in either Claude Code or Gemini CLI; would force a runtime dispatcher (forbidden by FR-02).

### `triz-reference` is read-only — explicit exception to confirm-before-write
- **Chosen:** This skill never writes to user files; the runtime protocol's confirm step is N/A
- **Rationale:** It's a learning/lookup skill. Confirming a "show me principle 24" response is friction without value.
- **Rejected:** Force the protocol uniformly — would create empty confirmation prompts on every reference query.

### Skill body uses prose for confirmation, not tool-specific syntax
- **Chosen:** "Stop. Ask the user to confirm the proposed change. Do not proceed until they reply." (per Decision 1, locked)
- **Rationale:** FR-03 forbids Claude- or Gemini-specific syntax. Plain English is interpreted natively by both runtimes.
- **Rejected:** Pseudo-syntax like `{{confirm}}` — would require installer templating (we explicitly rejected stub injection in Decision 1).

### Skill body cites reference files by relative path, not by inline copy
- **Chosen:** "Load `reference/parameters.md`" rather than embedding parameter content in the prompt
- **Rationale:** FR-13. Keeps bodies compact; reference is the single source of truth even at runtime.
- **Rejected:** Inline parameter and principle text into each body — bloats every skill, drifts from the reference files over time.

## Acceptance Criteria

### FR-01: Suite covers the five use cases
- GIVEN a fresh install of the suite
- WHEN the user lists the available TRIZ skills
- THEN the list SHALL contain at least one skill each for: contradiction resolution (`triz-contradiction`), design audit (`triz-design-audit`), refactoring (`triz-refactor`), TRIZ reference/learning (`triz-reference`), and Agile'TRIZ sprint planning/retro (`triz-sprint`)

### FR-02: Skills invokable independently
- GIVEN the suite is installed
- WHEN the user invokes any single skill by name (e.g., `triz-contradiction`)
- THEN the skill SHALL execute without requiring any other skill in the suite to be loaded or invoked first

### FR-03: Single neutral source
- GIVEN any skill file in `skills/`
- WHEN inspected
- THEN the file SHALL contain only `name`, `description`, `version`, and optionally `tags` in frontmatter
- AND the body SHALL NOT mention any Claude- or Gemini-specific tool, command, or syntax

### FR-07: Reasoning named (asserted by triz-contradiction body)
- GIVEN the user invokes `triz-contradiction` with two parameters (e.g., Security vs. Speed)
- WHEN the skill responds
- THEN the response SHALL name an inventive principle by ID and name, the two parameter names, and a one-sentence statement of the contradiction

### FR-08: No silent changes (asserted by skill body procedure)
- GIVEN a skill has identified a candidate change
- WHEN about to write
- THEN it SHALL present reasoning + diff and SHALL wait for explicit confirmation
- GIVEN the user rejects
- WHEN the skill completes
- THEN no file SHALL have been written

### FR-09: Acknowledge gaps (asserted by triz-contradiction body)
- GIVEN the matrix cell for the user-named contradiction is absent
- WHEN the skill responds
- THEN it SHALL report the gap, list considered principles, and decline to apply

### FR-10: Scope to the problem (asserted by skill body procedure)
- GIVEN a contradiction scoped to module A
- WHEN the skill applies a change
- THEN it SHALL edit only files in module A

### FR-11: No new major deps (asserted by skill body procedure)
- WHEN proposing a change
- THEN the skill SHALL use the existing stack
- AND if no in-stack solution exists, SHALL state this and require user opt-in for new dependencies

### FR-12: Destructive-op confirmation (asserted by skill body procedure)
- WHEN a step deletes files / drops tables / rewrites history
- THEN the skill SHALL require explicit confirmation for each destructive operation

### FR-15: Sprint workflows (asserted by triz-sprint body)
- GIVEN `triz-sprint` invoked with backlog items
- WHEN it runs morphological-matrix mode
- THEN it SHALL produce a bounded combined-idea set with principle attributions
- GIVEN `triz-sprint` invoked with a completed prototype
- WHEN it runs effects-extraction mode
- THEN it SHALL list positive + harmful effects and reframe each harmful effect as a fresh contradiction

## Done Criteria
- [ ] All 5 files exist in `skills/`
- [ ] Each file passes `lib.source.load_skills` validation (no schema errors)
- [ ] Each frontmatter has exactly the keys `name`, `description`, `version` (tags optional)
- [ ] Each body has the 5 required sections (`When to invoke`, `Inputs needed`, `Reference data used`, `Procedure`, `Output format`)
- [ ] No body mentions "AskUserQuestion", "MCP", "tool", or any Claude/Gemini-specific term (grep check)
- [ ] `triz-contradiction` body explicitly references the matrix lookup AND the FR-09 gap path
- [ ] `triz-sprint` body documents both morphological and effects-extraction modes
- [ ] Every body that may write files explicitly states "Stop. Ask the user to confirm. Do not proceed until they reply."
- [ ] `triz-reference` is documented as read-only and does NOT include the confirm-before-write step
