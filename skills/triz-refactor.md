---
name: triz-refactor
description: Refactors a module by applying a chosen TRIZ principle or auditing for ideality gaps.
version: 0.1.0
tags: [triz, refactor, ideality]
---

## When to invoke
Invoke this skill to refactor existing code to improve ideality (reduce waste, complexity, harmful effects) or to apply a specific TRIZ principle to resolve a known issue.

## Inputs needed
A module path AND either (a) a stated contradiction, or (b) a request to "audit for ideality gaps".

## Reference data used
- `reference/principles.md`
- `reference/matrix.json` (if a contradiction is provided)

## Procedure
1. Receive the module path and the specific contradiction or the request to audit for ideality gaps.
2. If auditing for ideality gaps, identify areas of waste, unnecessary complexity, or harmful side-effects. If a contradiction was stated, resolve it using `reference/matrix.json`.
3. Propose a refactoring plan that cites the specific TRIZ principle to be applied.
4. Stop. Ask the user to confirm. Do not proceed until they reply.
5. Apply the edits strictly scoped to the specified module.
6. Confirm separately before performing any destructive operation. Do not add any new major dependencies.

## Output format
A diff summary of the proposed changes, a citation of the applied principle, and a brief rationale explaining how it improves ideality or resolves the contradiction.
