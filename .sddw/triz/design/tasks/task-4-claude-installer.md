# Task 4: Claude Code installer + transformer

## Trace
- **FR-IDs:** FR-04 (Claude path), FR-05 (idempotent install)
- **Depends on:** task-3

## Files
- `install/install_claude_code.py` — create
- `install/lib/targets/claude_code.py` — create

## Architecture

### Components
- `lib.targets.claude_code`: pure transformer — given a `Skill` and a target root, computes what files need to exist and their content. — new
- `install_claude_code`: thin CLI wrapper — parses args, loads canonical sources, calls the transformer, performs the writes via the idempotency primitive. — new

### Data Flow
```
skills/*.md + reference/* → load_skills() / load_reference_files()
                          → claude_code.emit(skill, target_root, reference_files)
                          → returns list of (path, content) tuples
                          → install_claude_code writes only those whose hash differs
                          → prints per-skill status (installed | up-to-date | updated)
```

### Target layout (what gets written into `~/.claude/skills/`)

```
~/.claude/skills/
└── triz-contradiction/                  # one dir per skill, named by skill.name
    ├── SKILL.md                         # frontmatter (name, description) + body
    └── reference/                       # bundled copy of repo's reference/
        ├── parameters.md
        ├── principles.md
        ├── gof-mappings.md
        ├── matrix.json
        └── matrix-sources.md
```

Each skill gets its own complete `reference/` copy (per Decision 3, locked in design).

## Contracts

### CLI surface
```
python -m install.install_claude_code [--dry-run] [--target PATH]
```

- `--target PATH`: defaults to `~/.claude/skills`
- `--dry-run`: print actions but write nothing
- Stdout: one line per skill: `<status>: <skill-name> -> <path>` where status ∈ `{installed, up-to-date, updated}`. `installed` = path didn't exist; `updated` = path existed with different content; `up-to-date` = hash matched.
- Exit code: 0 on success, 1 on any error (e.g., source schema violation).

### Internal interface

```python
# install/lib/targets/claude_code.py

@dataclass(frozen=True)
class EmittedFile:
    path: Path        # absolute path under target_root
    content: bytes    # exact bytes to write

def emit(skill: Skill, target_root: Path, reference_files: list[Path]) -> list[EmittedFile]:
    """Compute the files that should exist for `skill` under `target_root`.
    Pre: target_root is an absolute path (may not yet exist).
    Post: returns:
      - one EmittedFile for SKILL.md (frontmatter with name+description, then body)
      - one EmittedFile per reference file, mirrored under <skill_dir>/reference/
    Does NOT touch the filesystem.
    """
```

### Claude Code SKILL.md format

```markdown
---
name: triz-contradiction
description: Resolve a stated contradiction between two IT parameters using TRIZ matrix lookup.
---

<verbatim body from canonical source — paths inside the body that referenced
"reference/parameters.md" still resolve, because we mirror reference/ alongside SKILL.md>
```

The transformer:
1. Strips `version` and `tags` from the canonical frontmatter (Claude Code doesn't consume them — keeping them would add noise without value)
2. Keeps `name` and `description` only
3. Emits the body verbatim — no rewriting, no path translation needed because the relative `reference/` path is preserved by the install layout

## Data Models

(Defined inline in Contracts above — `EmittedFile` dataclass.)

## Design Decisions

### Pure transformer + thin runner separation
- **Chosen:** `emit()` returns data; the CLI runner does I/O
- **Rationale:** Makes the transformer trivially unit-testable (no tmpdir setup needed for the core logic). Mirrors how the Gemini transformer (task-5) is structured, so testing patterns are shared.
- **Rejected:** `emit()` writes directly — couples logic to filesystem; tests need tmpdirs for every assertion.

### Bundle reference into each skill dir (not a shared dir)
- **Chosen:** Each skill gets `<skill_dir>/reference/` with full copy
- **Rationale:** Locked in design Decision 3. Skill is self-contained at runtime; uninstalling one skill doesn't break others; relative paths in skill bodies always work.
- **Rejected:** `~/.claude/skills/triz-reference-data/` shared dir referenced by `../triz-reference-data/parameters.md` from each skill — fragile, breaks if user uninstalls one skill.

### Strip canonical-only frontmatter on emit
- **Chosen:** Emit only `name` + `description` to Claude's SKILL.md
- **Rationale:** Keeps the emitted file minimal and matches Claude Code's documented frontmatter contract. `version` and `tags` are useful for the canonical source (idempotency, future filtering) but aren't read by Claude Code.
- **Rejected:** Pass through all frontmatter — risks Claude Code emitting warnings about unknown keys; bloat with no benefit.

### Idempotency: per-file hash, not per-skill
- **Chosen:** Each emitted file is independently hash-compared and conditionally written
- **Rationale:** If only the skill body changed but reference files didn't, only SKILL.md gets rewritten. Sharper "updated" status, less filesystem churn.
- **Rejected:** Hash the whole skill dir as one unit — coarser, requires writing all files even when most are unchanged.

## Acceptance Criteria

### FR-04 (Claude Code path): Install script for Claude Code
- GIVEN a machine with Claude Code installed
- WHEN the user runs `python -m install.install_claude_code`
- THEN `~/.claude/skills/<skill-name>/SKILL.md` SHALL exist for each canonical skill
- AND each SKILL.md SHALL have valid frontmatter with `name` and `description` keys (and no others)
- AND the skill SHALL be invokable from Claude Code

### FR-05: Idempotent install
- GIVEN the skills are already installed
- WHEN `install_claude_code` is re-run with no source changes
- THEN no file SHALL be rewritten
- AND every skill line SHALL report `up-to-date`

- GIVEN the canonical source for one skill has been edited
- WHEN `install_claude_code` is re-run
- THEN only that skill's SKILL.md SHALL be rewritten
- AND that line SHALL report `updated`; others report `up-to-date`

## Done Criteria
- [ ] `python -m install.install_claude_code --dry-run` runs without writing and prints per-skill plans
- [ ] Running without `--dry-run` creates `~/.claude/skills/<name>/SKILL.md` for each canonical skill
- [ ] Each SKILL.md frontmatter contains exactly `name` and `description` (no `version`, `tags`, or other keys)
- [ ] Each skill dir contains a `reference/` subdir with copies of every file from the repo's `reference/`
- [ ] Re-running with no source changes writes zero files and prints `up-to-date` for every skill
- [ ] Editing one skill body and re-running rewrites only that skill's SKILL.md
- [ ] `--target` flag overrides the default `~/.claude/skills` location
- [ ] Exit code 1 when canonical source has a schema violation; error message names the offending file
