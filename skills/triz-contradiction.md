---
name: triz-contradiction
description: Resolves software engineering contradictions by identifying conflicting parameters and suggesting principles.
version: 0.1.0
tags: [triz, contradiction, problem-solving]
---

## When to invoke
Invoke this skill when facing a technical trade-off or contradiction where improving one aspect worsens another (e.g., improving speed worsens security).

## Inputs needed
Two parameter names or IDs (the parameter to improve and the parameter that worsens), plus an optional module or file scope for the solution.

## Reference data used
- `reference/parameters.md` (to resolve names to IDs)
- `reference/matrix.json` (for contradiction cell lookup)
- `reference/principles.md` (to expand principles with software analogies)

## Procedure
1. Receive the inputs (improving parameter, worsening parameter, and optional scope).
2. Load `reference/parameters.md` to map the input names to exact parameter IDs.
3. Look up the contradiction in `reference/matrix.json` using the IDs.
4. If the matrix cell is empty, report the gap honestly, list the principles considered based on general heuristics, and STOP. Do not force a fit.
5. If the matrix cell is populated, present the top 1 to 3 principles with rationale. Expand them using `reference/principles.md`.
6. Propose a concrete code change scoped strictly to the user-named module.
7. Stop. Ask the user to confirm. Do not proceed until they reply.
8. If confirmed, apply edits only within the specified module scope. Confirm separately before any destructive operation. Do not introduce new major dependencies without explicit opt-in.

## Output format
A response that names the principle (by ID and name), the two parameters, the contradiction in a single sentence, and a proposed code diff or plan.
