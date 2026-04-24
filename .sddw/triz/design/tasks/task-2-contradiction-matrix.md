# Task 2: Compile contradiction matrix from cited literature

## Trace
- **FR-IDs:** FR-13 (matrix as reference data), supports FR-07 and FR-09
- **Depends on:** task-1

## Files
- `reference/matrix.json` — create
- `reference/matrix-sources.md` — create (provenance bibliography)

## Architecture

### Components
- `reference/matrix.json`: sparse lookup mapping `(improving_param_id, worsening_param_id)` → ranked principle IDs with confidence and source citation — new
- `reference/matrix-sources.md`: human-readable bibliography listing every paper/source referenced in matrix cells — new

### Data Flow
At skill runtime: skill receives two parameter names from the user → resolves to IDs via `parameters.md` → looks up cell in `matrix.json` → if cell exists, presents ranked principles with confidence; if cell missing, triggers FR-09 honest-gap response listing what was tried.

## Data Models

### `reference/matrix.json`

Sparse JSON object. Cells with no entry mean "no cited evidence" — the contradiction skill MUST report this honestly per FR-09 rather than fabricate.

```json
{
  "schema_version": 1,
  "cells": {
    "<improving_id>-<worsening_id>": {
      "principles": [<int>, ...],
      "confidence": "strong" | "moderate" | "weak",
      "sources": ["<source-key>", ...],
      "notes": "optional one-line context"
    }
  }
}
```

- Cell key format: zero-padded not required, dash-separated, improving first. Example: `"19-10"` = improving system complexity (19) while worsening loss of data (10).
- `principles` is ordered by historical fit (best first), each ID 1–40 matching `principles.md`.
- `confidence`: `strong` = multiple sources agree on these principles; `moderate` = one cited source; `weak` = inferred / single anecdotal mention.
- `sources` keys reference entries in `matrix-sources.md`.

Cells MUST NOT be added without at least one citation. If a cell has no citation, omit it entirely.

### `reference/matrix-sources.md`

```markdown
# Matrix Source Bibliography

## mann-2011
Mann, D. (2011). *TRIZ and Software Innovation*. AITRIZ Articles.
URL: https://www.aitriz.org/articles/TRIZFeatures/323031312D30382D4D616E6E.pdf
Used for cells: 19-10, 5-16, ...

## domb-stamey-2006
Domb, E. & Stamey, J. (2006). ...
Used for cells: ...

## rea-1999
Rea, K.C. (1999). *TRIZ for Software — Using the Inventive Principles*. The TRIZ Journal.
Used for cells: ...
```

Each source key in `matrix.json` MUST have a matching entry in `matrix-sources.md`.

### Initial cell coverage (minimum bar for v1)

The matrix MUST contain at least the following cells, drawn directly from the cited examples in `doc/TRIZ for Software Engineering.md`:

- `19-10` (system complexity worsens data integrity) → cites Mann 2011, e.g., principles for distributed-data integrity (per source doc line 51)
- `9-6` (loss of time vs accuracy) → from Rea 1999 example (source doc line 115): principles 24 (Mediator), 26 (Copying)
- `16-5` (security vs speed) → cited as canonical example throughout the source doc

Beyond these three, the implementer SHOULD add any additional cells they can ground in the cited literature; cells without citation MUST be omitted.

## Contracts

### Internal Interface (skill consumes matrix.json)
- `matrix.lookup(improving_id: int, worsening_id: int) -> Cell | None`
  - Pre: both IDs in 1..21
  - Post: returns the cell verbatim, or `None` if the cell is absent. Caller (skill body) is responsible for FR-09 gap reporting on `None`.

This contract is conceptual — skills load the JSON file and read keys directly; no Python wrapper is shipped to skill runtimes.

## Design Decisions

### Sparse-cell encoding with explicit absence
- **Chosen:** Cells absent from `matrix.json` mean "no citation"; skills report a gap rather than guess
- **Rationale:** FR-09 explicitly forbids force-fitting principles when the matrix gives weak results. An empty cell IS the signal.
- **Rejected:** Dense matrix with `"confidence": "none"` placeholders — pollutes the file with hundreds of empty cells; ambiguous (does empty mean "researched and nothing found" or "not yet researched"?).

### Provenance per cell, in a separate sources file
- **Chosen:** Each cell lists `sources` keys; bibliography in `matrix-sources.md`
- **Rationale:** A user inspecting a recommendation can trace it to a paper. Honesty matters more than completeness for v1.
- **Rejected:** Inline citations as long strings in `matrix.json` — duplicates bibliographic data per cell, hard to keep consistent.

### v1 coverage: best-effort from cited sources, not exhaustive
- **Chosen:** Ship whatever cells the implementer can ground in the literature, accept partial coverage
- **Rationale:** The full IT-TRIZ matrix is not freely published in machine-readable form; transcribing every cell from Mann 2011 is out of scope for v1. Honest gap-reporting (FR-09) makes partial coverage tolerable.
- **Rejected:** Block v1 on full 21×21 coverage — would push delivery indefinitely.

## Acceptance Criteria

### FR-07: Reasoning named (matrix data supports this)
- GIVEN a user invokes the contradiction skill with two conflicting parameters that ARE in the matrix
- WHEN the skill responds
- THEN the response SHALL name at least one inventive principle by ID and name (looked up from matrix → principles.md)

### FR-09: Acknowledge gaps (matrix sparseness enables this)
- GIVEN a user-described contradiction whose `(improving, worsening)` cell is absent from `matrix.json`
- WHEN the skill responds
- THEN it SHALL report the gap, list what it considered, and decline to apply any principle

## Done Criteria
- [ ] `reference/matrix.json` exists, parses as valid JSON, conforms to the schema above
- [ ] At least 3 cells populated, each citing at least one source
- [ ] Every `sources` key in `matrix.json` resolves to an entry in `matrix-sources.md`
- [ ] Every principle ID in any `principles` array is in 1..40
- [ ] Every parameter ID in any cell key is in 1..21
- [ ] No cell exists without at least one citation
- [ ] `reference/matrix-sources.md` lists every cited source with a working URL or full bibliographic reference
