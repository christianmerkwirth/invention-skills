# Requirements: TRIZ Skills for Coding CLIs

## 1. Project

- Path: `.`

The target codebase is the current working directory (`invention-skills/`), which already contains the source research document at `doc/TRIZ for Software Engineering.md`.

---

## 2. Purpose

Give developers in Claude Code, Gemini CLI, and other compatible coding CLIs a portable suite of TRIZ-grounded skills that detect architectural contradictions, recommend the inventive principles that have historically resolved them, and apply the chosen principle directly to the user's code — replacing ad-hoc compromises with deterministic, evidence-backed refactors.

---

## 3. User Stories

- As a developer stuck on a trade-off, I want to name two conflicting parameters and receive ranked inventive principles with code-ready suggestions, so that I can resolve the contradiction without compromising either parameter.
- As an architect reviewing a proposed design, I want a skill to surface hidden contradictions and map them to applicable GoF patterns or TRIZ principles, so that I catch weak designs before code is written.
- As a developer refactoring legacy code, I want a skill to audit a module for ideality gaps — waste, complexity, harmful effects — and propose principle-grounded refactors, so that I can simplify without breaking behaviour.
- As a developer new to TRIZ, I want an interactive skill to browse the 21 IT parameters and 40 inventive principles with concrete software examples, so that I build fluency with the framework.
- As an Agile practitioner, I want a sprint skill that reframes backlog items as contradictions and extracts positive/negative effects from prototype reviews, so that each sprint systematically eliminates trade-offs rather than compounding them.
- As a skill author/user, I want to install the same skill suite in Claude Code, Gemini CLI, or another compatible CLI with a single install command, so that portability isn't an ongoing maintenance burden.

---

## 4. Functional Requirements

### Skill Suite Composition

- FR-01: The suite SHALL include at least five focused skills covering the confirmed use cases: contradiction resolution, design audit, code refactoring, TRIZ reference/learning, and Agile'TRIZ sprint planning/retro.
- FR-02: Each skill SHALL be invokable independently by its own name and SHALL NOT require a central dispatcher skill to mediate access.

### Cross-CLI Portability

- FR-03: Each skill SHALL exist as a single tool-agnostic Markdown instruction file in a canonical repo location, with no Claude-Code-specific or Gemini-CLI-specific frontmatter embedded in the source.
- FR-04: The suite SHALL ship install scripts that place skills into Claude Code's skills directory and Gemini CLI's extension directory using each tool's native format.
- FR-05: Install scripts SHALL be idempotent — re-running them SHALL NOT corrupt, duplicate, or orphan installed skills.
- FR-06: The repo SHOULD document the install contract (source schema, required target fields, worked example) so users of other compatible coding CLIs can author their own installer without editing any skill source file.

### TRIZ Reasoning Transparency

- FR-07: Before proposing a change, a skill SHALL name the inventive principle (number and name from the 40), the IT parameter(s) involved (from the 21), and the contradiction the principle resolves.
- FR-08: A skill SHALL NOT apply a code change without first presenting its TRIZ reasoning and receiving explicit user confirmation.
- FR-09: A skill SHALL NOT force-fit a principle when no top-ranked matrix result addresses the described contradiction; it SHALL report the gap and list what was tried.

### Scope and Safety

- FR-10: A skill SHALL limit file edits to modules tied to the contradiction the user described and SHALL NOT opportunistically refactor neighbouring code without explicit confirmation.
- FR-11: A skill SHALL NOT introduce new major dependencies, frameworks, or languages as its solution; it SHALL work within the codebase's existing stack unless the user explicitly opts in.
- FR-12: A skill SHALL confirm with the user before destructive operations (file deletion, history rewrite, dropping tables, force pushes).

### Reference Content

- FR-13: The suite SHALL embed the 21 IT parameters and the 40 inventive principles with their software analogies as structured reference data loadable on demand by any skill, rather than duplicating the content inside each skill's prompt.
- FR-14: The suite SHOULD include the documented GoF ↔ TRIZ pattern correlations as reference data available to the design-audit and refactor skills.
- FR-15: The sprint skill SHALL provide a morphological-matrix workflow (generate a limited set of combined ideas from intersecting principles) and a prototype-review workflow (extract positive/negative effects as fresh contradictions) consistent with the Agile'TRIZ framework.

---

## 5. Acceptance Criteria

### FR-01: Suite covers the five use cases

**Happy path:**
- GIVEN a fresh install of the suite
- WHEN the user lists the available TRIZ skills
- THEN the list SHALL contain at least one skill each for: contradiction resolution, design audit, refactoring, TRIZ reference/learning, and Agile'TRIZ sprint planning/retro

### FR-02: Skills invokable independently

**Happy path:**
- GIVEN the suite is installed
- WHEN the user invokes any single skill by name (e.g. `triz-contradiction`)
- THEN the skill SHALL execute without requiring any other skill in the suite to be loaded or invoked first

### FR-03: Single neutral source

**Happy path:**
- GIVEN the canonical skill directory in the repo
- WHEN a developer inspects a skill file
- THEN the file SHALL contain instructions and reference links only, with no Claude- or Gemini-specific frontmatter keys embedded in the source

### FR-04: Install scripts for both CLIs

**Happy path — Claude Code:**
- GIVEN a machine with Claude Code installed
- WHEN the user runs the Claude install script
- THEN the skills SHALL appear in Claude Code's skills directory in its native format and SHALL be invokable from Claude Code

**Happy path — Gemini CLI:**
- GIVEN a machine with Gemini CLI installed
- WHEN the user runs the Gemini install script
- THEN the skills SHALL appear in Gemini CLI's extension directory in its native format and SHALL be invokable from Gemini CLI

### FR-05: Idempotent install

**Happy path:**
- GIVEN the skills are already installed
- WHEN the install script is re-run
- THEN no duplicate files, broken symlinks, or corrupted frontmatter SHALL result
- AND the script SHALL report which entries were already up to date vs. updated

### FR-06: Install contract documented

**Happy path:**
- GIVEN the repo README
- WHEN a user of an unlisted CLI reads the "Porting" section
- THEN they SHALL find the canonical source schema, the target format requirements, and a worked example sufficient to author their own installer without modifying any skill source file

### FR-07: Reasoning named

**Happy path:**
- GIVEN a user invokes the contradiction skill with two conflicting parameters (e.g. Security vs. Speed)
- WHEN the skill responds
- THEN the response SHALL name at least one inventive principle by its number and name (e.g. "Principle 24 — Mediator"), the two IT parameter names from the 21, and a one-sentence statement of the contradiction being resolved

### FR-08: No silent changes

**Happy path:**
- GIVEN a skill has identified a principle and a candidate code change
- WHEN it is about to write to a file
- THEN it SHALL present the reasoning and proposed diff and SHALL wait for explicit user confirmation before editing

**Failure path:**
- GIVEN the user rejects the proposal
- WHEN the skill completes
- THEN it SHALL NOT have written to any file

### FR-09: Acknowledge gaps

**Failure path:**
- GIVEN a user-described contradiction for which the top-ranked matrix results are all weak fits
- WHEN the skill responds
- THEN it SHALL report the weak-fit status, list the principles it considered, and decline to apply any of them rather than force-fitting the closest match

### FR-10: Scope to the problem

**Happy path:**
- GIVEN a contradiction the user scoped to module A
- WHEN the skill applies a change
- THEN it SHALL edit only files in module A

**Edge case:**
- GIVEN the skill identifies a related improvement in module B
- WHEN proposing the change
- THEN it SHALL either exclude module B from the patch or explicitly list module B files and request confirmation before touching them

### FR-11: No new major deps

**Happy path:**
- GIVEN a Python project using Flask
- WHEN the skill recommends applying Principle 24 (Mediator)
- THEN it SHALL propose a solution using Flask or the existing stack, not a new framework or message broker the project doesn't already depend on

**Edge case:**
- GIVEN no viable solution exists within the current stack
- WHEN proposing
- THEN the skill SHALL state that explicitly and let the user opt in to adding a dependency

### FR-12: Destructive-op confirmation

**Happy path:**
- GIVEN a principle suggests removing a legacy module or dropping a database table
- WHEN the skill reaches the destructive step
- THEN it SHALL require explicit user confirmation for each destructive operation

### FR-13: Reference data loadable

**Happy path:**
- GIVEN any skill in the suite
- WHEN it needs to cite a parameter or principle
- THEN it SHALL load the structured reference (e.g. `reference/parameters.md`, `reference/principles.md`) from a known path rather than embedding the full list inside its own prompt

### FR-14: GoF citation

**Happy path:**
- GIVEN the design-audit skill is invoked on a design whose contradiction maps to a known GoF ↔ TRIZ correlation (e.g. Adapter ↔ Principle 24 Mediator)
- WHEN proposing
- THEN the skill SHALL cite both the inventive principle and the corresponding GoF pattern, linking back to the reference entry

### FR-15: Sprint workflows

**Happy path — morphological matrix:**
- GIVEN the sprint skill is invoked during backlog refinement with a set of user stories
- WHEN it runs the morphological-matrix workflow
- THEN it SHALL produce a bounded set of combined ideas (one selection per row) and name the principles each idea draws from

**Happy path — prototype review:**
- GIVEN the sprint skill is invoked at sprint review with a completed prototype
- WHEN it runs the effects-extraction workflow
- THEN it SHALL list the prototype's positive effects and harmful effects and reframe each harmful effect as a fresh contradiction for the next sprint

---

## 6. Constraints

### In Scope

- A suite of at least five focused TRIZ skills: contradiction resolver, design auditor, refactor assistant, reference/tutor, Agile'TRIZ sprint skill
- Canonical skill sources in tool-agnostic Markdown (single source of truth)
- Install scripts for Claude Code and Gemini CLI
- A documented install contract enabling third-party CLI ports without editing skill sources
- Structured reference data: 21 IT parameters, 40 inventive principles with software analogies, GoF ↔ TRIZ pattern correlations
- TRIZ reasoning transparency — every change names the principle, parameters, and contradiction it resolves
- Scope discipline — skills operate only on the user-named module

### Out of Scope

- Semantic TRIZ / NLP automation (live patent-database queries, natural-language parameter extraction) — deferred; v1 uses static matrices and structured lookups
- CALDET enterprise methodology integration — too large for v1; Agile'TRIZ covers the sprint-level need
- A central "master" TRIZ dispatcher skill — explicitly rejected (FR-02)
- Native packaging for CLIs beyond Claude Code and Gemini CLI — third-party CLIs supported only via the documented install contract (FR-06)
- Web dashboards, GUIs, patent-database integrations, live LLM fine-tunes

### Prohibitions

- SHALL NOT apply code changes without surfacing TRIZ reasoning and confirming with the user — prevents silent architectural drift
- SHALL NOT force-fit a principle when top-ranked matrix results are weak matches — honesty over appearance of competence
- SHALL NOT expand scope beyond the user's named module without explicit confirmation — prevents opportunistic refactor blast radius
- SHALL NOT introduce new dependencies, frameworks, or languages unilaterally — respects the existing stack's constraints
- SHALL NOT perform destructive operations (file delete, history rewrite, drop table, force push) without explicit confirmation
- SHALL NOT embed Claude-Code-specific or Gemini-CLI-specific frontmatter or assumptions in the canonical skill source files — breaks the portability contract

### Testing Approach

- Selective TDD — TDD for the install scripts (idempotency, target-path correctness, native-format emission) and for the reference-data loaders (parameters and principles integrity, count assertions, schema checks). Test-after for the skill prompts themselves, since their value is qualitative and best verified by running them against real contradictions.
