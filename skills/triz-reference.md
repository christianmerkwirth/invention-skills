---
name: triz-reference
description: Browses the TRIZ parameters, principles, and GoF correlations interactively.
version: 0.1.0
tags: [triz, reference, learning]
---

## When to invoke
Invoke this skill to learn about TRIZ, look up specific parameters or principles, or understand how TRIZ principles map to software design patterns like the Gang of Four (GoF) patterns.

## Inputs needed
A free-text query from the user (e.g., "show me principle 24", "what's parameter 16?", "explain the GoF Adapter mapping").

## Reference data used
- `reference/parameters.md` (lazy load only what the query needs)
- `reference/principles.md` (lazy load only what the query needs)

## Procedure
1. Receive input query from the user.
2. Load only the reference files needed to resolve the query.
3. Resolve the query by fetching matching entries.
4. Present the findings, including the software analogy and any relevant cross-references.
5. Do not edit any files. This skill is strictly read-only.

## Output format
A concise, informative response answering the user's query, citing specific TRIZ parameters, principles, and software analogies.
