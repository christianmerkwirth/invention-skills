# TRIZ Skills

A suite of [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) that bring the Theory of Inventive Problem Solving (TRIZ) into software engineering workflows: systematically resolving contradictions, auditing designs, and improving system ideality. Works with Claude Code and Google Antigravity, which both consume the canonical `SKILL.md` format unchanged.

## Skills

- **triz-contradiction** — Resolves software engineering contradictions by identifying conflicting parameters and suggesting principles.
- **triz-design-audit** — Reviews a proposed design or module to surface hidden contradictions and map them to GoF and TRIZ principles.
- **triz-refactor** — Refactors a module by applying a chosen TRIZ principle or auditing for ideality gaps.
- **triz-reference** — Browses the TRIZ parameters, principles, and GoF correlations interactively.
- **triz-sprint** — Applies TRIZ in Agile workflows for morphological backlog refinement and prototype effects extraction.

## Install

Each directory under `skills/` is already a valid Agent Skill (a `SKILL.md` plus a `reference/` symlink to the shared reference data). Install by symlinking or copying into the host tool's skills directory.

### Claude Code

```bash
# Live-link from this checkout (picks up git pulls automatically):
mkdir -p ~/.claude/skills
for d in skills/*/; do ln -sfn "$(pwd)/$d" ~/.claude/skills/"$(basename "$d")"; done

# Or snapshot copy (re-run after each git pull):
cp -rL skills/* ~/.claude/skills/
```

### Google Antigravity / Jetski

Antigravity (and Google-internal Jetski) consume the same canonical `SKILL.md` format. Only the destination differs — expand the section that matches your setup:

<details>
<summary>Antigravity</summary>

Skills are installed into `~/.gemini/antigravity/skills/`.

```bash
# Global install (live-linked):
mkdir -p ~/.gemini/antigravity/skills
for d in skills/*/; do ln -sfn "$(pwd)/$d" ~/.gemini/antigravity/skills/"$(basename "$d")"; done

# Or per-workspace install:
mkdir -p .agents/skills
for d in skills/*/; do ln -sfn "$(pwd)/$d" .agents/skills/"$(basename "$d")"; done
```

See the [Antigravity Skills docs](https://antigravity.google/docs/skills) for details.

</details>

<details>
<summary>Jetski (Google-internal)</summary>

Skills are installed into `~/.gemini/jetski/skills/`.

```bash
# Global install (live-linked):
mkdir -p ~/.gemini/jetski/skills
for d in skills/*/; do ln -sfn "$(pwd)/$d" ~/.gemini/jetski/skills/"$(basename "$d")"; done

# Or per-workspace install:
mkdir -p .agents/skills
for d in skills/*/; do ln -sfn "$(pwd)/$d" .agents/skills/"$(basename "$d")"; done
```

</details>

Both forms are idempotent. Use `cp -rL` (capital L) when copying so the `reference/` symlinks are dereferenced into real directories at the destination.

### Gemini CLI (not directly supported)

Gemini CLI's [extension format](https://google-gemini.github.io/gemini-cli/docs/extensions/) is different — it expects a `gemini-extension.json` manifest plus TOML command files, not `SKILL.md`. There is no canonical-format install for Gemini CLI. If you need it, you can hand-wrap each skill as a Gemini extension by embedding the `SKILL.md` body into a `commands/<name>.toml` `prompt` field.

## Using a skill

Once installed, invoke through your agent:

```
Use triz-contradiction. I want to improve speed, but that worsens security. Scope: backend/auth.
```

The agent consults the TRIZ contradiction matrix, maps the concepts to software parameters, and suggests an architectural principle (e.g. "Segmentation", "Prior Action") with a proposed code diff.

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
