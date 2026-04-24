# Task 5: Gemini CLI installer + transformer

## Trace
- **FR-IDs:** FR-04 (Gemini path), FR-05 (idempotent install)
- **Depends on:** task-3

## Files
- `install/install_gemini_cli.py` — create
- `install/lib/targets/gemini_cli.py` — create

## Architecture

### Components
- `lib.targets.gemini_cli`: pure transformer — given a `Skill` and a target root, computes Gemini-extension files. — new
- `install_gemini_cli`: thin CLI wrapper — same shape as `install_claude_code` (task-4). — new

### Data Flow
```
skills/*.md + reference/* → load_skills() / load_reference_files()
                          → gemini_cli.emit(skill, target_root, reference_files)
                          → returns list of (path, content) tuples
                          → install_gemini_cli writes only those whose hash differs
                          → prints per-skill status (installed | up-to-date | updated)
```

### Target layout (what gets written into `~/.gemini/extensions/`)

Per Decision 4 (locked): each skill becomes a Gemini extension exposing one custom slash command.

```
~/.gemini/extensions/
└── triz-contradiction/                       # one extension per skill
    ├── gemini-extension.json                 # extension manifest
    ├── commands/
    │   └── triz-contradiction.toml           # slash command definition
    └── reference/                            # bundled copy of repo's reference/
        ├── parameters.md
        ├── principles.md
        ├── gof-mappings.md
        ├── matrix.json
        └── matrix-sources.md
```

User invokes via `/triz-contradiction` in Gemini CLI.

## Contracts

### CLI surface
```
python -m install.install_gemini_cli [--dry-run] [--target PATH]
```

- `--target PATH`: defaults to `~/.gemini/extensions`
- `--dry-run`: print actions but write nothing
- Stdout/exit-code semantics identical to task-4's `install_claude_code` for consistency.

### Internal interface

```python
# install/lib/targets/gemini_cli.py

@dataclass(frozen=True)
class EmittedFile:
    path: Path
    content: bytes

def emit(skill: Skill, target_root: Path, reference_files: list[Path]) -> list[EmittedFile]:
    """Compute the files that should exist for `skill` as a Gemini extension under `target_root`.
    Pre: target_root is an absolute path (may not yet exist).
    Post: returns:
      - <target_root>/<skill.name>/gemini-extension.json
      - <target_root>/<skill.name>/commands/<skill.name>.toml
      - <target_root>/<skill.name>/reference/<file> for each reference file
    Does NOT touch the filesystem.
    """
```

### Gemini extension manifest

`gemini-extension.json`:
```json
{
  "name": "triz-contradiction",
  "version": "0.1.0",
  "description": "Resolve a stated contradiction between two IT parameters using TRIZ matrix lookup."
}
```

The transformer maps canonical `skill.name` → manifest `name`, canonical `skill.version` → manifest `version`, canonical `skill.description` → manifest `description`.

### Slash command file

`commands/<skill.name>.toml`:
```toml
description = "<skill.description>"
prompt = """
<verbatim body from canonical source>
"""
```

The body is embedded inside the `prompt` triple-quoted string. Any literal `"""` inside the body MUST be escaped or the transformer MUST raise `EmitError` (canonical bodies should not contain `"""`).

## Data Models

(Defined inline in Contracts above — `EmittedFile` dataclass, manifest schema, command schema.)

## Design Decisions

### Slash-command extension over context-file extension
- **Chosen:** Each skill is its own extension exposing one slash command (`/triz-contradiction`)
- **Rationale:** Locked in design Decision 4. Explicit invocation matches FR-02 ("invokable independently by its own name"); avoids loading all 5 skill bodies into every Gemini conversation's context.
- **Rejected:** Single extension with `GEMINI.md` context file holding all 5 skill descriptions — pulls all skill content into every chat session; harder to invoke a specific skill explicitly.
- **Rejected:** Hybrid (extension context + slash commands) — adds duplication and complexity for marginal UX gain.

### One extension per skill (not one umbrella extension with 5 commands)
- **Chosen:** `~/.gemini/extensions/triz-<name>/` per skill
- **Rationale:** User can disable/uninstall a single skill without affecting others. Per-skill `reference/` bundling (Decision 3) requires per-extension dirs anyway.
- **Rejected:** Single `~/.gemini/extensions/triz/` with `commands/triz-*.toml` — couples skills, complicates partial uninstall.

### Embed canonical body verbatim into the .toml prompt
- **Chosen:** Body is copied unchanged into the `prompt` field
- **Rationale:** The body's relative `reference/parameters.md` paths still resolve because we mirror `reference/` alongside the command file. No path translation needed.
- **Rejected:** Reformat the body (e.g., into a system prompt + user prompt structure) — would require canonical source to anticipate Gemini's prompt structure, breaking FR-03 portability.

### Idempotency strategy mirrors task-4
- **Chosen:** Per-file hash compare via `lib.idempotency.file_matches`
- **Rationale:** Same primitive shared across both installers; consistent UX.

## Acceptance Criteria

### FR-04 (Gemini CLI path): Install script for Gemini CLI
- GIVEN a machine with Gemini CLI installed
- WHEN the user runs `python -m install.install_gemini_cli`
- THEN `~/.gemini/extensions/<skill-name>/gemini-extension.json` SHALL exist for each canonical skill
- AND each extension SHALL contain a valid `commands/<skill-name>.toml`
- AND the skill SHALL be invokable from Gemini CLI as `/<skill-name>`

### FR-05: Idempotent install
- GIVEN the skills are already installed
- WHEN `install_gemini_cli` is re-run with no source changes
- THEN no file SHALL be rewritten
- AND every skill line SHALL report `up-to-date`

- GIVEN the canonical source for one skill has been edited
- WHEN `install_gemini_cli` is re-run
- THEN only that skill's `gemini-extension.json` and/or `commands/<name>.toml` SHALL be rewritten

## Done Criteria
- [ ] `python -m install.install_gemini_cli --dry-run` runs without writing and prints per-skill plans
- [ ] Running without `--dry-run` creates `~/.gemini/extensions/<name>/gemini-extension.json` and `commands/<name>.toml` for each canonical skill
- [ ] Manifest JSON parses and contains exactly the keys `name`, `version`, `description`
- [ ] Each extension dir contains a `reference/` subdir with copies of every file from the repo's `reference/`
- [ ] Re-running with no source changes writes zero files and prints `up-to-date` for every skill
- [ ] Editing one skill body and re-running rewrites only that skill's files
- [ ] Transformer raises `EmitError` if a canonical body contains `"""` (TOML triple-quote conflict)
- [ ] `--target` flag overrides the default `~/.gemini/extensions` location
