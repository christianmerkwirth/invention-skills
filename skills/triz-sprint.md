---
name: triz-sprint
description: Applies TRIZ in Agile workflows for morphological backlog refinement and prototype effects extraction.
version: 0.1.0
tags: [triz, agile, sprint, planning, review]
---

## When to invoke
Invoke this skill during backlog refinement to generate combined ideas (morphological matrix mode) or during sprint review to extract effects from a completed prototype (effects-extraction mode).

## Inputs needed
Either a list of backlog items (for morphological mode) OR a prototype description or completed feature (for effects-extraction mode).

## Reference data used
- `reference/principles.md` (for both modes)
- `reference/matrix.json` (only when effects-extraction surfaces a contradiction)

## Procedure
1. Receive inputs and determine the mode.
2. **For morphological mode (backlog refinement):**
   - Reframe backlog items as contradictions.
   - Enumerate candidate principles per row.
   - Generate a bounded set of combined ideas by making one selection per row.
   - Name the principles each idea draws from.
   - Present the ideas to the user. Do not automatically apply them.
3. **For effects-extraction mode (sprint review):**
   - Take the prototype description.
   - List the positive effects achieved.
   - List the harmful side-effects or unresolved issues.
   - Reframe each harmful effect as a fresh contradiction (improving X / worsening Y) for the next sprint backlog.
4. Stop. Ask the user to confirm. Do not proceed until they reply.
5. Finalize the output based on user feedback. No code edits are performed by this skill.

## Output format
- For morphological mode: A small ranked list of combined ideas with principle attributions.
- For effects-extraction mode: An updated contradiction backlog listing positive effects and reframed harmful effects.
