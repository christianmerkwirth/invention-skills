# Task 3: Installer shared lib — canonical source loader and idempotency

## Trace
- **FR-IDs:** FR-03 (canonical source schema), FR-05 (idempotency primitive)
- **Depends on:** none

## Files
- `install/__init__.py` — create (empty package marker)
- `install/lib/__init__.py` — create (empty package marker)
- `install/lib/source.py` — create
- `install/lib/idempotency.py` — create
- `install/lib/targets/__init__.py` — create (empty package marker; populated by tasks 4 & 5)
- `pyproject.toml` — create (project metadata + pytest config)

## Architecture

### Components
- `lib.source`: parses canonical skill files from `skills/` and discovers reference files in `reference/`. Single point of truth for the skill source schema. — new
- `lib.idempotency`: sha256 content compare for "should I write this file?" decisions. Used by every target transformer. — new
- `lib.targets`: package namespace for per-CLI transformers (Claude Code in task-4, Gemini CLI in task-5). — new

### Data Flow
Repo root → `lib.source.load_skills()` → list of `Skill` objects → consumed by target transformers → emit native artifacts.

## Contracts

### Internal Interfaces

```python
# install/lib/source.py

@dataclass(frozen=True)
class Skill:
    name: str           # slug from frontmatter; matches filename stem
    description: str    # one-line, both Claude & Gemini consume natively
    version: str        # semver string
    body: str           # everything after the frontmatter, verbatim
    source_path: Path   # for debugging/error messages

def load_skills(skills_dir: Path) -> list[Skill]:
    """Parse every *.md in skills_dir as a canonical skill source.
    Pre: skills_dir exists and contains at least one *.md file.
    Post: list ordered alphabetically by name. Raises SourceError on:
      - missing or malformed YAML frontmatter
      - missing required fields (name, description, version)
      - frontmatter contains keys other than: name, description, version, tags
        (enforces FR-03: no tool-specific keys)
      - name does not match filename stem
    """

def load_reference_files(reference_dir: Path) -> list[Path]:
    """Return all files in reference_dir that should be bundled with skills.
    Pre: reference_dir exists.
    Post: list of absolute paths, sorted. Includes *.md and *.json. Excludes
      hidden files and any subdirectories.
    """

class SourceError(Exception):
    """Raised on any canonical source schema violation."""
```

```python
# install/lib/idempotency.py

def content_hash(data: bytes | str) -> str:
    """Return sha256 hex digest. str input is encoded as UTF-8."""

def file_matches(path: Path, expected_content: bytes | str) -> bool:
    """True iff path exists and its content sha256 == content_hash(expected).
    Returns False if path does not exist."""
```

### Canonical skill source schema (defined here, consumed everywhere)

```markdown
---
name: triz-contradiction
description: Resolve a stated contradiction between two IT parameters using TRIZ matrix lookup.
version: 0.1.0
tags: [triz, contradiction]    # optional
---
# Body — Markdown instructions for the LLM, no tool-specific syntax.
```

**Hard rules enforced by `load_skills`:**
- Frontmatter MUST be a YAML block at the top of the file delimited by `---` lines
- Required keys: `name` (str), `description` (str), `version` (str matching semver)
- Optional keys: `tags` (list[str])
- ANY OTHER FRONTMATTER KEY is a violation of FR-03 and MUST raise `SourceError`
- `name` MUST equal the filename stem (so `skills/triz-foo.md` requires `name: triz-foo`)

## Data Models

(Defined inline in the Contracts section above — `Skill` dataclass.)

## Design Decisions

### Strict frontmatter allowlist (raise on unknown keys)
- **Chosen:** Loader rejects any frontmatter key not in `{name, description, version, tags}`
- **Rationale:** FR-03 forbids Claude- or Gemini-specific frontmatter in canonical sources. A whitelist is the only enforcement mechanism that catches accidental drift (someone adding `claude-tools:` or `gemini-extension:` to a skill source). Strict failure surfaces violations at install time, not at runtime.
- **Rejected:** Warn-and-continue on unknown keys — drift accumulates silently.

### Standard library only (no PyYAML, no Pydantic)
- **Chosen:** Use Python stdlib YAML parser — there isn't one, so use a minimal hand-rolled parser limited to the strict subset we accept (string scalars, list-of-strings, no nesting beyond that).
- **Rationale:** Zero install-time dependencies for users. The frontmatter we accept is trivial (4 known keys).
- **Rejected:** PyYAML — adds a dependency for users running the installer; many systems don't have it installed.
- **Rejected:** TOML frontmatter (Python 3.11+ has `tomllib`) — non-standard for Markdown frontmatter; tools won't render preview.

### Idempotency by content hash, not mtime
- **Chosen:** sha256 compare of file bytes
- **Rationale:** Re-running the installer after `git pull` should detect ACTUAL changes, not mtime drift. Hash compare is deterministic regardless of clock skew or filesystem.
- **Rejected:** mtime/size compare — false positives after `git checkout`, false negatives if content edited but size matches.

## Acceptance Criteria

### FR-03: Single neutral source
- GIVEN a `skills/foo.md` file with frontmatter containing a Claude- or Gemini-specific key
- WHEN `load_skills()` is called
- THEN it SHALL raise `SourceError` naming the offending key

### FR-05: Idempotent install (primitive)
- GIVEN a file whose content matches `expected_content`
- WHEN `file_matches(path, expected_content)` is called
- THEN it SHALL return `True`

## Done Criteria
- [ ] `install/lib/source.py` exposes `Skill`, `load_skills`, `load_reference_files`, `SourceError`
- [ ] `install/lib/idempotency.py` exposes `content_hash`, `file_matches`
- [ ] `load_skills` rejects frontmatter with unknown keys (raises `SourceError`)
- [ ] `load_skills` rejects when `name` field disagrees with filename stem
- [ ] `load_skills` accepts a valid skill file and returns a `Skill` with all fields populated
- [ ] No third-party Python dependencies declared in `pyproject.toml` (stdlib only for runtime; pytest is a dev dep)
- [ ] `pyproject.toml` configures pytest to discover tests in `tests/`
- [ ] All public functions have type annotations
