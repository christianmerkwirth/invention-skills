---
name: triz-design-audit
description: Reviews a proposed design or module to surface hidden contradictions and map them to GoF and TRIZ principles.
---

## When to invoke
Invoke this skill to review a new architecture, a design document, or an existing module to identify latent trade-offs and suggest improvements using TRIZ and GoF patterns.

## Inputs needed
A path to a design document, a module path, or a natural language description of an architecture.

## Reference data used
- `reference/principles.md`
- `reference/matrix.json` (when the audit surfaces a candidate contradiction)

## Procedure
1. Receive the design document, module path, or description.
2. Scan the provided design context to enumerate suspected hidden contradictions or trade-offs.
3. For each suspected contradiction, look up the relevant parameters and check `reference/matrix.json`.
4. Identify candidate principles and corresponding GoF patterns (if a correlation exists).
5. Stop. Ask the user to confirm the audit findings and recommended next steps. Do not proceed until they reply.
6. Produce a final audit report. Do not execute code edits unless the user explicitly requests a refactor as a follow-up.

## Output format
An audit report listing the hidden contradictions found, the TRIZ principles considered, the GoF patterns applicable, and recommended next steps.
