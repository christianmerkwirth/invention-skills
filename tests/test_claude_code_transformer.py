"""Tests for install.lib.targets.claude_code — Claude Code transformer."""

from __future__ import annotations

from pathlib import Path

import pytest

from install.lib.source import Skill
from install.lib.targets.claude_code import EmittedFile, emit


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_skill() -> Skill:
    """Return a minimal Skill for testing."""
    return Skill(
        name="triz-contradiction",
        description="Resolve a stated contradiction between two IT parameters using TRIZ matrix lookup.",
        version="0.1.0",
        body="# Contradiction Resolver\n\nLook up `reference/parameters.md` for param IDs.\n",
        source_path=Path("/repo/skills/triz-contradiction.md"),
    )


@pytest.fixture()
def reference_dir(tmp_path: Path) -> Path:
    """Create a temporary reference/ directory with sample files."""
    d = tmp_path / "reference"
    d.mkdir()
    (d / "parameters.md").write_text("# Parameters\n", encoding="utf-8")
    (d / "principles.md").write_text("# Principles\n", encoding="utf-8")
    (d / "matrix.json").write_text("{}\n", encoding="utf-8")
    return d


@pytest.fixture()
def reference_files(reference_dir: Path) -> list[Path]:
    """Return sorted list of reference file paths."""
    return sorted(reference_dir.iterdir())


@pytest.fixture()
def target_root(tmp_path: Path) -> Path:
    """Return a target directory path (does not need to exist)."""
    return tmp_path / "claude_skills"


# ---------------------------------------------------------------------------
# emit() — SKILL.md
# ---------------------------------------------------------------------------


class TestEmitSkillMd:
    def test_skill_md_is_first_emitted(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        result = emit(sample_skill, target_root, reference_files)
        assert result[0].path.name == "SKILL.md"

    def test_skill_md_path(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        result = emit(sample_skill, target_root, reference_files)
        expected = target_root / "triz-contradiction" / "SKILL.md"
        assert result[0].path == expected

    def test_skill_md_frontmatter_has_name_and_description(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        result = emit(sample_skill, target_root, reference_files)
        text = result[0].content.decode("utf-8")
        assert text.startswith("---\n")
        assert "name: triz-contradiction\n" in text
        assert "description: Resolve a stated contradiction" in text

    def test_skill_md_frontmatter_omits_version(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        result = emit(sample_skill, target_root, reference_files)
        text = result[0].content.decode("utf-8")
        assert "version:" not in text

    def test_skill_md_frontmatter_omits_tags(
        self,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        skill = Skill(
            name="tagged",
            description="Has tags.",
            version="1.0.0",
            body="body\n",
            source_path=Path("/repo/skills/tagged.md"),
        )
        result = emit(skill, target_root, reference_files)
        text = result[0].content.decode("utf-8")
        assert "tags:" not in text

    def test_skill_md_frontmatter_has_exactly_two_keys(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        """Only name and description should appear in frontmatter."""
        result = emit(sample_skill, target_root, reference_files)
        text = result[0].content.decode("utf-8")
        # Extract frontmatter block
        parts = text.split("---\n")
        # parts[0] is empty (before first ---), parts[1] is FM, parts[2:] is body
        fm_lines = [l for l in parts[1].strip().split("\n") if l.strip()]
        assert len(fm_lines) == 2
        keys = {l.split(":")[0].strip() for l in fm_lines}
        assert keys == {"name", "description"}

    def test_skill_md_body_preserved_verbatim(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        result = emit(sample_skill, target_root, reference_files)
        text = result[0].content.decode("utf-8")
        assert sample_skill.body in text

    def test_skill_md_is_valid_utf8(
        self,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        skill = Skill(
            name="unicode",
            description="Handles unicode: é, ñ, ü",
            version="0.1.0",
            body="Body with special chars: 日本語\n",
            source_path=Path("/repo/skills/unicode.md"),
        )
        result = emit(skill, target_root, reference_files)
        text = result[0].content.decode("utf-8")
        assert "日本語" in text
        assert "é, ñ, ü" in text


# ---------------------------------------------------------------------------
# emit() — reference files
# ---------------------------------------------------------------------------


class TestEmitReferenceFiles:
    def test_reference_files_count(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        result = emit(sample_skill, target_root, reference_files)
        # 1 SKILL.md + N reference files
        assert len(result) == 1 + len(reference_files)

    def test_reference_files_in_skill_subdir(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        result = emit(sample_skill, target_root, reference_files)
        ref_dir = target_root / "triz-contradiction" / "reference"
        for ef in result[1:]:
            assert ef.path.parent == ref_dir

    def test_reference_file_names_preserved(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        result = emit(sample_skill, target_root, reference_files)
        emitted_names = {ef.path.name for ef in result[1:]}
        source_names = {p.name for p in reference_files}
        assert emitted_names == source_names

    def test_reference_file_content_matches_source(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        result = emit(sample_skill, target_root, reference_files)
        for ef in result[1:]:
            source = next(p for p in reference_files if p.name == ef.path.name)
            assert ef.content == source.read_bytes()

    def test_no_reference_files(
        self,
        sample_skill: Skill,
        target_root: Path,
    ) -> None:
        result = emit(sample_skill, target_root, [])
        assert len(result) == 1
        assert result[0].path.name == "SKILL.md"


# ---------------------------------------------------------------------------
# emit() — does not touch filesystem
# ---------------------------------------------------------------------------


class TestEmitPurity:
    def test_does_not_create_target_root(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        assert not target_root.exists()
        emit(sample_skill, target_root, reference_files)
        assert not target_root.exists()

    def test_returns_emitted_file_instances(
        self,
        sample_skill: Skill,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        result = emit(sample_skill, target_root, reference_files)
        for ef in result:
            assert isinstance(ef, EmittedFile)
            assert isinstance(ef.path, Path)
            assert isinstance(ef.content, bytes)


# ---------------------------------------------------------------------------
# emit() — multiple skills
# ---------------------------------------------------------------------------


class TestEmitMultipleSkills:
    def test_two_skills_get_separate_dirs(
        self,
        target_root: Path,
        reference_files: list[Path],
    ) -> None:
        skill_a = Skill(
            name="alpha",
            description="First.",
            version="1.0.0",
            body="A body\n",
            source_path=Path("/repo/skills/alpha.md"),
        )
        skill_b = Skill(
            name="bravo",
            description="Second.",
            version="1.0.0",
            body="B body\n",
            source_path=Path("/repo/skills/bravo.md"),
        )
        result_a = emit(skill_a, target_root, reference_files)
        result_b = emit(skill_b, target_root, reference_files)

        assert result_a[0].path.parent.name == "alpha"
        assert result_b[0].path.parent.name == "bravo"
