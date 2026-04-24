# Task 1: Author parameters, principles, and GoF reference data

## Trace
- **FR-IDs:** FR-13, FR-14
- **Depends on:** none

## Files
- `reference/parameters.md` — create
- `reference/principles.md` — create
- `reference/gof-mappings.md` — create

## Architecture

### Components
- `reference/` directory: structured reference data loaded on demand by every skill at runtime — new
- These three files are static content, shipped as-is into each skill's install target by the installer

### Data Flow
Source research doc (`doc/TRIZ for Software Engineering.md`) → manual extraction → structured Markdown reference files → bundled into each skill at install time → loaded by skill body when it needs to cite a parameter, principle, or pattern correlation.

## Data Models

### `reference/parameters.md`

Markdown file. Top section is a stable lookup table; per-parameter sections follow with the longer description. Both the table and the sections must be present so a skill can do quick lookup and deep reference from one file.

Required structure:

```markdown
# IT-TRIZ Parameters (21)

| ID | Name | One-line scope |
|----|------|----------------|
| 1 | Size (Static) | Compiled binary, lines of code, on-disk footprint |
| 2 | Size (Dynamic) | RAM, runtime heap, dynamic bandwidth |
| ... | ... | ... |

## 1. Size (Static)
**Scope:** ...
**Software examples:**
- ...
- ...

## 2. Size (Dynamic)
...
```

All 21 parameters from the source doc (`doc/TRIZ for Software Engineering.md` lines 25–49) must be present, in order, with IDs 1–21 matching the source table exactly.

### `reference/principles.md`

Same shape — top lookup table plus per-principle sections. All 40 principles, IDs 1–40, ordered as in the source doc (lines 65–113).

```markdown
# Inventive Principles (40)

| ID | Name | Software analogy (one line) |
|----|------|------------------------------|
| 1 | Segmentation | Microservices, modular decomposition |
| ... | ... | ... |

## 1. Segmentation
**Traditional concept:** Divide an object into independent parts.
**Software analogy:** Breaking monoliths into discrete components, microservices, subroutines.
**Examples:**
- ...
```

### `reference/gof-mappings.md`

```markdown
# GoF ↔ TRIZ Pattern Correlations

| GoF Pattern | Category | TRIZ Principle ID | TRIZ Principle Name | Insight |
|-------------|----------|-------------------|---------------------|---------|
| Adapter | Structural | 24 | Mediator | Translator between incompatible interfaces |
| Bridge | Structural | 2 | Extraction | Decouples abstraction from implementation |
| ... | ... | ... | ... | ... |
```

All seven correlations from `doc/TRIZ for Software Engineering.md` lines 127–133 must be present. Principle IDs in this file MUST match IDs in `reference/principles.md`.

## Design Decisions

### Source-of-truth format: structured Markdown
- **Chosen:** Markdown with both lookup tables and per-entry sections in the same file
- **Rationale:** Skills load these files into LLM context as text; Markdown is the native medium. Tables enable fast scanning; per-entry sections give the LLM enough context to reason. JSON would be smaller but harder for the LLM to read inline.
- **Rejected:** JSON/YAML reference files — would force every skill to render them back to prose for the LLM, wasting tokens.

### One file per concept (params, principles, GoF), not one combined
- **Chosen:** Three separate files
- **Rationale:** A skill that only needs parameters (e.g., the contradiction skill at lookup time) shouldn't pay the token cost of loading principles. Per-skill bodies will load only the files they need.
- **Rejected:** Single `reference.md` — breaks selective loading; FR-13 says "loadable on demand" which implies modular.

## Acceptance Criteria

### FR-13: Reference data loadable
- GIVEN any skill in the suite
- WHEN it needs to cite a parameter or principle
- THEN it SHALL load the structured reference (e.g., `reference/parameters.md`, `reference/principles.md`) from a known path rather than embedding the full list inside its own prompt

### FR-14: GoF citation
- GIVEN the design-audit skill is invoked on a design whose contradiction maps to a known GoF↔TRIZ correlation (e.g., Adapter ↔ Principle 24 Mediator)
- WHEN proposing
- THEN the skill SHALL cite both the inventive principle and the corresponding GoF pattern, linking back to the reference entry

## Done Criteria
- [ ] `reference/parameters.md` exists with exactly 21 entries, IDs 1–21 in order, names matching source doc
- [ ] `reference/principles.md` exists with exactly 40 entries, IDs 1–40 in order, names matching source doc
- [ ] `reference/gof-mappings.md` exists with at least the 7 correlations from the source doc
- [ ] Every principle ID referenced in `gof-mappings.md` exists in `principles.md`
- [ ] All three files are valid Markdown (renderable; no broken tables)
- [ ] No file contains Claude- or Gemini-specific syntax or frontmatter
