"""Canonical skill source loader.

Parses skill files from the ``skills/`` directory and discovers reference
files in ``reference/``.  This module is the single point of truth for the
skill source schema defined by FR-03.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Public exception
# ---------------------------------------------------------------------------


class SourceError(Exception):
    """Raised on any canonical source schema violation."""


# ---------------------------------------------------------------------------
# Public data model
# ---------------------------------------------------------------------------

_SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)

_ALLOWED_KEYS = frozenset({"name", "description", "version", "tags"})


@dataclass(frozen=True)
class Skill:
    """A parsed canonical skill source."""

    name: str  # slug from frontmatter; matches filename stem
    description: str  # one-line, both Claude & Gemini consume natively
    version: str  # semver string
    body: str  # everything after the frontmatter, verbatim
    source_path: Path  # for debugging/error messages


# ---------------------------------------------------------------------------
# Frontmatter parser (stdlib-only, no PyYAML)
# ---------------------------------------------------------------------------


def _parse_frontmatter(text: str, source_path: Path) -> tuple[dict[str, str | list[str]], str]:
    """Split *text* into (frontmatter-dict, body).

    Supports only the strict subset accepted by the canonical schema:
    scalar string values and ``tags`` as a flow-sequence of strings.
    """
    if not text.startswith("---"):
        raise SourceError(
            f"{source_path}: file does not start with '---' frontmatter delimiter"
        )

    # Find closing '---' (must be on its own line after the opening one).
    lines = text.split("\n")
    end_idx: int | None = None
    for i, line in enumerate(lines[1:], start=1):
        if line.rstrip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise SourceError(
            f"{source_path}: no closing '---' frontmatter delimiter found"
        )

    fm_lines = lines[1:end_idx]
    body = "\n".join(lines[end_idx + 1 :])

    result: dict[str, str | list[str]] = {}
    for lineno, raw in enumerate(fm_lines, start=2):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue  # blank line or comment inside frontmatter

        if ":" not in stripped:
            raise SourceError(
                f"{source_path}:{lineno}: malformed frontmatter line: {raw!r}"
            )

        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        if key == "tags":
            result[key] = _parse_tag_list(value, source_path, lineno)
        else:
            result[key] = value

    return result, body


def _parse_tag_list(value: str, source_path: Path, lineno: int) -> list[str]:
    """Parse a YAML flow-sequence like ``[triz, contradiction]``."""
    if not (value.startswith("[") and value.endswith("]")):
        raise SourceError(
            f"{source_path}:{lineno}: 'tags' must be a YAML flow sequence "
            f"like [tag1, tag2], got: {value!r}"
        )
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [t.strip() for t in inner.split(",") if t.strip()]


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def _validate_frontmatter(
    fm: dict[str, str | list[str]],
    source_path: Path,
    expected_stem: str,
) -> None:
    """Raise ``SourceError`` if the frontmatter violates the canonical schema."""

    # Unknown keys
    unknown = set(fm.keys()) - _ALLOWED_KEYS
    if unknown:
        raise SourceError(
            f"{source_path}: frontmatter contains disallowed key(s): "
            f"{', '.join(sorted(unknown))}. "
            f"Only {sorted(_ALLOWED_KEYS)} are permitted (FR-03)."
        )

    # Required keys
    for required in ("name", "description", "version"):
        if required not in fm:
            raise SourceError(
                f"{source_path}: missing required frontmatter key '{required}'"
            )

    # name must match filename stem
    name = fm["name"]
    if name != expected_stem:
        raise SourceError(
            f"{source_path}: frontmatter 'name' is {name!r} but filename "
            f"stem is {expected_stem!r}; they must match"
        )

    # version must be semver
    version = fm["version"]
    if not isinstance(version, str) or not _SEMVER_RE.match(version):
        raise SourceError(
            f"{source_path}: 'version' must be a valid semver string, "
            f"got {version!r}"
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_skills(skills_dir: Path) -> list[Skill]:
    """Parse every ``*.md`` in *skills_dir* as a canonical skill source.

    Pre:
        *skills_dir* exists and contains at least one ``*.md`` file.

    Post:
        Returns a list ordered alphabetically by ``name``.

    Raises:
        SourceError: on missing or malformed YAML frontmatter, missing
            required fields (``name``, ``description``, ``version``),
            frontmatter containing keys other than ``{name, description,
            version, tags}`` (enforces FR-03), or ``name`` not matching
            the filename stem.
    """
    md_files = sorted(skills_dir.glob("*.md"))
    if not md_files:
        raise SourceError(f"{skills_dir}: no *.md files found")

    skills: list[Skill] = []
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text, path)
        _validate_frontmatter(fm, path, expected_stem=path.stem)

        skills.append(
            Skill(
                name=str(fm["name"]),
                description=str(fm["description"]),
                version=str(fm["version"]),
                body=body,
                source_path=path.resolve(),
            )
        )

    skills.sort(key=lambda s: s.name)
    return skills


def load_reference_files(reference_dir: Path) -> list[Path]:
    """Return all files in *reference_dir* that should be bundled with skills.

    Pre:
        *reference_dir* exists.

    Post:
        List of absolute paths, sorted.  Includes ``*.md`` and ``*.json``.
        Excludes hidden files and any subdirectories.
    """
    result: list[Path] = []
    for child in reference_dir.iterdir():
        if child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if child.suffix in (".md", ".json"):
            result.append(child.resolve())

    result.sort()
    return result
