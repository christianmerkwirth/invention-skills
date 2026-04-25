"""Tests for install.lib.source — canonical skill loader."""

from __future__ import annotations

from pathlib import Path

import pytest

from install.lib.source import Skill, SourceError, load_reference_files, load_skills

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_skills_dir(tmp_path: Path) -> Path:
    """Return a temporary skills/ directory."""
    d = tmp_path / "skills"
    d.mkdir()
    return d


@pytest.fixture()
def mock_reference_dir(tmp_path: Path) -> Path:
    """Return a temporary reference/ directory with sample files."""
    d = tmp_path / "reference"
    d.mkdir()
    (d / "parameters.md").write_text("# Parameters\n")
    (d / "principles.md").write_text("# Principles\n")
    (d / "matrix.json").write_text("{}\n")
    (d / ".hidden").write_text("secret\n")
    (d / "notes.txt").write_text("ignored\n")
    sub = d / "subdir"
    sub.mkdir()
    (sub / "nested.md").write_text("nested\n")
    return d


def _write_skill(
    mock_skills_dir: Path,
    name: str,
    *,
    description: str = "A test skill.",
    version: str = "0.1.0",
    tags: str | None = None,
    extra_fm: str = "",
    body: str = "# Body\nHello.\n",
) -> Path:
    """Write a minimal canonical skill file and return its path."""
    lines = [
        "---",
        f"name: {name}",
        f"description: {description}",
        f"version: {version}",
    ]
    if tags is not None:
        lines.append(f"tags: {tags}")
    if extra_fm:
        # extra_fm may contain trailing newline; split and add each line
        for fm_line in extra_fm.rstrip("\n").split("\n"):
            lines.append(fm_line)
    lines.append("---")
    fm = "\n".join(lines) + "\n"
    path = mock_skills_dir / f"{name}.md"
    path.write_text(fm + body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# load_skills — happy path
# ---------------------------------------------------------------------------


class TestLoadSkillsHappy:
    def test_single_valid_skill(self, mock_skills_dir: Path) -> None:
        _write_skill(mock_skills_dir, "alpha")
        result = load_skills(mock_skills_dir)
        assert len(result) == 1
        skill = result[0]
        assert skill.name == "alpha"
        assert skill.description == "A test skill."
        assert skill.version == "0.1.0"
        assert "# Body" in skill.body
        assert skill.source_path == (mock_skills_dir / "alpha.md").resolve()

    def test_multiple_skills_sorted_by_name(self, mock_skills_dir: Path) -> None:
        _write_skill(mock_skills_dir, "charlie")
        _write_skill(mock_skills_dir, "alpha")
        _write_skill(mock_skills_dir, "bravo")
        result = load_skills(mock_skills_dir)
        assert [s.name for s in result] == ["alpha", "bravo", "charlie"]

    def test_tags_optional_and_parsed(self, mock_skills_dir: Path) -> None:
        _write_skill(mock_skills_dir, "tagged", tags="[triz, test]")
        result = load_skills(mock_skills_dir)
        # Tags are parsed but not stored on Skill (the schema validates but
        # the dataclass deliberately omits tags — task spec shows only the 4
        # fields).
        assert result[0].name == "tagged"

    def test_empty_tags(self, mock_skills_dir: Path) -> None:
        _write_skill(mock_skills_dir, "empty-tags", tags="[]")
        result = load_skills(mock_skills_dir)
        assert result[0].name == "empty-tags"

    def test_body_preserved_verbatim(self, mock_skills_dir: Path) -> None:
        body = "Line 1\n\nLine 3 with special chars: é, ñ, ü\n"
        _write_skill(mock_skills_dir, "verbatim", body=body)
        result = load_skills(mock_skills_dir)
        assert result[0].body.strip() == body.strip()

    def test_semver_prerelease(self, mock_skills_dir: Path) -> None:
        _write_skill(mock_skills_dir, "pre", version="1.0.0-beta.1")
        result = load_skills(mock_skills_dir)
        assert result[0].version == "1.0.0-beta.1"

    def test_semver_build_metadata(self, mock_skills_dir: Path) -> None:
        _write_skill(mock_skills_dir, "build", version="2.3.4+build.567")
        result = load_skills(mock_skills_dir)
        assert result[0].version == "2.3.4+build.567"


# ---------------------------------------------------------------------------
# load_skills — error paths
# ---------------------------------------------------------------------------


class TestLoadSkillsErrors:
    def test_no_md_files(self, mock_skills_dir: Path) -> None:
        with pytest.raises(SourceError, match="no \\*.md files found"):
            load_skills(mock_skills_dir)

    def test_missing_frontmatter_delimiter(self, mock_skills_dir: Path) -> None:
        (mock_skills_dir / "bad.md").write_text("no frontmatter here\n")
        with pytest.raises(SourceError, match="does not start with '---'"):
            load_skills(mock_skills_dir)

    def test_no_closing_delimiter(self, mock_skills_dir: Path) -> None:
        (mock_skills_dir / "bad.md").write_text("---\nname: bad\n")
        with pytest.raises(SourceError, match="no closing '---'"):
            load_skills(mock_skills_dir)

    def test_missing_required_name(self, mock_skills_dir: Path) -> None:
        (mock_skills_dir / "noname.md").write_text(
            "---\ndescription: x\nversion: 0.1.0\n---\nbody\n"
        )
        with pytest.raises(SourceError, match="missing required.*'name'"):
            load_skills(mock_skills_dir)

    def test_missing_required_description(self, mock_skills_dir: Path) -> None:
        (mock_skills_dir / "nodesc.md").write_text(
            "---\nname: nodesc\nversion: 0.1.0\n---\nbody\n"
        )
        with pytest.raises(SourceError, match="missing required.*'description'"):
            load_skills(mock_skills_dir)

    def test_missing_required_version(self, mock_skills_dir: Path) -> None:
        (mock_skills_dir / "nover.md").write_text(
            "---\nname: nover\ndescription: x\n---\nbody\n"
        )
        with pytest.raises(SourceError, match="missing required.*'version'"):
            load_skills(mock_skills_dir)

    def test_unknown_key_raises_source_error(self, mock_skills_dir: Path) -> None:
        """FR-03: Claude/Gemini-specific keys must be rejected."""
        _write_skill(
            mock_skills_dir, "bad-key", extra_fm="claude-tools: something\n"
        )
        with pytest.raises(SourceError, match="disallowed key.*claude-tools"):
            load_skills(mock_skills_dir)

    def test_multiple_unknown_keys(self, mock_skills_dir: Path) -> None:
        _write_skill(
            mock_skills_dir,
            "many-bad",
            extra_fm="gemini-ext: a\nclaude-tools: b\n",
        )
        with pytest.raises(SourceError, match="disallowed key"):
            load_skills(mock_skills_dir)

    def test_name_mismatch_raises_source_error(self, mock_skills_dir: Path) -> None:
        (mock_skills_dir / "actual.md").write_text(
            "---\nname: wrong\ndescription: x\nversion: 0.1.0\n---\nbody\n"
        )
        with pytest.raises(SourceError, match="'name' is 'wrong'.*'actual'"):
            load_skills(mock_skills_dir)

    def test_invalid_semver(self, mock_skills_dir: Path) -> None:
        _write_skill(mock_skills_dir, "badver", version="not-a-version")
        with pytest.raises(SourceError, match="valid semver"):
            load_skills(mock_skills_dir)

    def test_malformed_frontmatter_line(self, mock_skills_dir: Path) -> None:
        (mock_skills_dir / "bad.md").write_text("---\nno-colon-here\n---\nbody\n")
        with pytest.raises(SourceError, match="malformed frontmatter"):
            load_skills(mock_skills_dir)

    def test_malformed_tags_not_flow_sequence(self, mock_skills_dir: Path) -> None:
        _write_skill(mock_skills_dir, "bad-tags", tags="not-a-list")
        with pytest.raises(SourceError, match="flow sequence"):
            load_skills(mock_skills_dir)


# ---------------------------------------------------------------------------
# load_reference_files
# ---------------------------------------------------------------------------


class TestLoadReferenceFiles:
    def test_returns_md_and_json(self, mock_reference_dir: Path) -> None:
        result = load_reference_files(mock_reference_dir)
        names = [p.name for p in result]
        assert "parameters.md" in names
        assert "principles.md" in names
        assert "matrix.json" in names

    def test_excludes_hidden_files(self, mock_reference_dir: Path) -> None:
        result = load_reference_files(mock_reference_dir)
        names = [p.name for p in result]
        assert ".hidden" not in names

    def test_excludes_subdirectories(self, mock_reference_dir: Path) -> None:
        result = load_reference_files(mock_reference_dir)
        names = [p.name for p in result]
        assert "nested.md" not in names

    def test_excludes_non_md_json(self, mock_reference_dir: Path) -> None:
        result = load_reference_files(mock_reference_dir)
        names = [p.name for p in result]
        assert "notes.txt" not in names

    def test_paths_are_absolute(self, mock_reference_dir: Path) -> None:
        result = load_reference_files(mock_reference_dir)
        for p in result:
            assert p.is_absolute()

    def test_paths_are_sorted(self, mock_reference_dir: Path) -> None:
        result = load_reference_files(mock_reference_dir)
        assert result == sorted(result)

    def test_loads_all_repo_skills(self, skills_dir: Path) -> None:
        result = load_skills(skills_dir)
        assert len(result) == 5
        names = {s.name for s in result}
        assert names == {"triz-contradiction", "triz-design-audit", "triz-refactor", "triz-reference", "triz-sprint"}
