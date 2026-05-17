# TRIZ Skills for Claude Code

A suite of Claude Code skills that bring the Theory of Inventive Problem Solving (TRIZ) into software engineering workflows: systematically resolving contradictions, auditing designs, and improving system ideality.

## Skills

- **triz-contradiction** — Resolves software engineering contradictions by identifying conflicting parameters and suggesting principles.
- **triz-design-audit** — Reviews a proposed design or module to surface hidden contradictions and map them to GoF and TRIZ principles.
- **triz-refactor** — Refactors a module by applying a chosen TRIZ principle or auditing for ideality gaps.
- **triz-reference** — Browses the TRIZ parameters, principles, and GoF correlations interactively.
- **triz-sprint** — Applies TRIZ in Agile workflows for morphological backlog refinement and prototype effects extraction.

## Install

Each directory under `skills/` is already a valid Claude Code skill (a `SKILL.md` plus a `reference/` symlink to the shared `reference/` data). Install by copying or symlinking into `~/.claude/skills/`:

```bash
# Live-link from this checkout (recommended — picks up git pulls automatically):
mkdir -p ~/.claude/skills
for d in skills/*/; do ln -sfn "$(pwd)/$d" ~/.claude/skills/"$(basename "$d")"; done

# Or copy (snapshot — re-run after each git pull):
cp -rL skills/* ~/.claude/skills/
```

Both forms are idempotent. Use `cp -rL` (capital L) so the `reference/` symlinks are dereferenced into real directories at the destination.

## Using a skill

Once installed, invoke through Claude Code:

```
Use triz-contradiction. I want to improve speed, but that worsens security. Scope: backend/auth.
```

Claude consults the TRIZ contradiction matrix, maps the concepts to software parameters, and suggests an architectural principle (e.g. "Segmentation", "Prior Action") with a proposed code diff.

## Authoring a new skill

Create a new directory under `skills/`:

```
skills/my-new-skill/
  SKILL.md                       # frontmatter: name + description; then body
  reference -> ../../reference   # symlink, if the skill consumes shared reference data
```

`SKILL.md` follows Claude Code's canonical [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) format — YAML frontmatter with `name` and `description`, followed by Markdown body. The body can reference bundled files via the relative path `reference/<file>`.

## Repo layout

- `doc/` — Background and methodology (TRIZ for Software Engineering).
- `reference/` — Shared static data (parameters, principles, contradiction matrix) loaded by skills at runtime.
- `skills/` — One directory per skill in Claude Code's canonical format.

## License

MIT
