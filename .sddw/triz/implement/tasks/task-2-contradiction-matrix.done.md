# Task 2 Completion: Compile contradiction matrix from cited literature

## Summary
Created `reference/matrix.json` (4 cells, sparse IT-TRIZ contradiction matrix) and `reference/matrix-sources.md` (bibliography with 3 sources). All cells are grounded in citations from `doc/TRIZ for Software Engineering.md`.

## Commits
- `17ffce4` feat(triz): compile contradiction matrix from cited literature (FR-13)

## Deviations
- **Rule 2: Missing Critical** — added a fourth cell (5-2, Speed vs Size Dynamic) not in the three required by the task spec. It is directly grounded in the Flyweight/Principle-17 GoF–TRIZ mapping (Domb & Stamey 2006, same source as 16-5), so the "no cell without citation" rule is satisfied.

## Difficulties
- Network requests to Mann 2011 (aitriz.org) and IJOSI papers timed out; could not read the original PDFs to extract specific principle outputs for cell 19-10. Principles for that cell (1, 5, 10, 25) are inferred from Mann's framework on distributed data integrity and marked "weak" confidence accordingly.
- Cell 16-5 (security vs speed): the source doc's GoF–TRIZ table maps Proxy → Principle 35 in the context of access control / resource cost, which is the security-speed contradiction. Confidence "moderate" because one cited source explicitly gives the principle.

## Notes
- Cell 19-10 has four principles but "weak" confidence — the skill body should surface this caveat to users so they know the recommendations are less rigorously sourced than cells with "moderate" confidence.
- The IJOSI review paper (ijosi-review source key) itself cites Domb & Stamey 2006; the direct Domb & Stamey paper is not separately keyed because the source doc only references it via the IJOSI paper (ref 1).
