"""Tests for install.install_claude_code — CLI installer."""

from __future__ import annotations

from pathlib import Path

import pytest

from install.lib.source import Skill
from install.lib.targets.claude_code import emit
from install.install_claude_code import _write_file, main
from install.lib.targets.claude_code import EmittedFile


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def repo_layout(tmp_path: Path) -> Path:
    """Create a minimal repo layout with skills/ and reference/."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    ref_dir = tmp_path / "reference"
    ref_dir.mkdir()

    # A valid skill
    (skills_dir / "triz-contradiction.md").write_text(
        "---\n"
        "name: triz-contradiction\n"
        "description: Resolve contradictions using TRIZ.\n"
        "version: 0.1.0\n"
        "---\n"
        "# TRIZ Contradiction\n\n"
        "Look up `reference/parameters.md`.\n",
        encoding="utf-8",
    )

    # Reference files
    (ref_dir / "parameters.md").write_text("# Parameters\n", encoding="utf-8")
    (ref_dir / "principles.md").write_text("# Principles\n", encoding="utf-8")
    (ref_dir / "matrix.json").write_text("{}\n", encoding="utf-8")
    (ref_dir / "gof-mappings.md").write_text("# GoF\n", encoding="utf-8")
    (ref_dir / "matrix-sources.md").write_text("# Sources\n", encoding="utf-8")

    return tmp_path


@pytest.fixture()
def target_dir(tmp_path: Path) -> Path:
    """Return a target directory for installation."""
    return tmp_path / "target_skills"


# ---------------------------------------------------------------------------
# _write_file
# ---------------------------------------------------------------------------


class TestWriteFile:
    def test_installs_new_file(self, tmp_path: Path) -> None:
        ef = EmittedFile(path=tmp_path / "new.md", content=b"hello")
        status = _write_file(ef, dry_run=False)
        assert status == "installed"
        assert (tmp_path / "new.md").read_bytes() == b"hello"

    def test_updates_changed_file(self, tmp_path: Path) -> None:
        f = tmp_path / "existing.md"
        f.write_bytes(b"old content")
        ef = EmittedFile(path=f, content=b"new content")
        status = _write_file(ef, dry_run=False)
        assert status == "updated"
        assert f.read_bytes() == b"new content"

    def test_up_to_date_matching_file(self, tmp_path: Path) -> None:
        f = tmp_path / "same.md"
        f.write_bytes(b"same content")
        ef = EmittedFile(path=f, content=b"same content")
        status = _write_file(ef, dry_run=False)
        assert status == "up-to-date"

    def test_dry_run_does_not_write(self, tmp_path: Path) -> None:
        ef = EmittedFile(path=tmp_path / "nope.md", content=b"data")
        status = _write_file(ef, dry_run=True)
        assert status == "installed"
        assert not (tmp_path / "nope.md").exists()

    def test_dry_run_reports_updated(self, tmp_path: Path) -> None:
        f = tmp_path / "old.md"
        f.write_bytes(b"old")
        ef = EmittedFile(path=f, content=b"new")
        status = _write_file(ef, dry_run=True)
        assert status == "updated"
        # Content should be unchanged
        assert f.read_bytes() == b"old"

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        nested = tmp_path / "a" / "b" / "c" / "file.md"
        ef = EmittedFile(path=nested, content=b"deep")
        _write_file(ef, dry_run=False)
        assert nested.read_bytes() == b"deep"


# ---------------------------------------------------------------------------
# main() — integration (uses monkeypatch to override repo_root)
# ---------------------------------------------------------------------------


class TestMainIntegration:
    def test_dry_run_prints_plans(
        self, repo_layout: Path, target_dir: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "install.install_claude_code._repo_root", lambda: repo_layout
        )
        rc = main(["--dry-run", "--target", str(target_dir)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "[dry-run]" in out
        assert "triz-contradiction" in out
        # Nothing should be written
        assert not target_dir.exists()

    def test_install_creates_skill_dir(
        self, repo_layout: Path, target_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "install.install_claude_code._repo_root", lambda: repo_layout
        )
        rc = main(["--target", str(target_dir)])
        assert rc == 0
        skill_dir = target_dir / "triz-contradiction"
        assert skill_dir.is_dir()
        assert (skill_dir / "SKILL.md").is_file()

    def test_install_creates_reference_dir(
        self, repo_layout: Path, target_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "install.install_claude_code._repo_root", lambda: repo_layout
        )
        main(["--target", str(target_dir)])
        ref_dir = target_dir / "triz-contradiction" / "reference"
        assert ref_dir.is_dir()
        assert (ref_dir / "parameters.md").is_file()
        assert (ref_dir / "principles.md").is_file()
        assert (ref_dir / "matrix.json").is_file()

    def test_skill_md_has_only_name_and_description(
        self, repo_layout: Path, target_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "install.install_claude_code._repo_root", lambda: repo_layout
        )
        main(["--target", str(target_dir)])
        skill_md = (target_dir / "triz-contradiction" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        # Parse frontmatter
        parts = skill_md.split("---\n")
        fm_lines = [l for l in parts[1].strip().split("\n") if l.strip()]
        keys = {l.split(":")[0].strip() for l in fm_lines}
        assert keys == {"name", "description"}

    def test_idempotent_rerun(
        self, repo_layout: Path, target_dir: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "install.install_claude_code._repo_root", lambda: repo_layout
        )
        # First run
        main(["--target", str(target_dir)])
        capsys.readouterr()  # clear output

        # Second run — everything should be up-to-date
        rc = main(["--target", str(target_dir)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "up-to-date" in out
        assert "installed" not in out
        assert "updated" not in out

    def test_update_skill_only_rewrites_changed(
        self, repo_layout: Path, target_dir: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "install.install_claude_code._repo_root", lambda: repo_layout
        )
        # First install
        main(["--target", str(target_dir)])
        capsys.readouterr()

        # Modify the skill source
        skill_file = repo_layout / "skills" / "triz-contradiction.md"
        skill_file.write_text(
            "---\n"
            "name: triz-contradiction\n"
            "description: Updated description.\n"
            "version: 0.2.0\n"
            "---\n"
            "# Updated Body\n\nNew content.\n",
            encoding="utf-8",
        )

        # Re-run
        rc = main(["--target", str(target_dir)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "updated" in out

        # Verify the SKILL.md has new content
        skill_md = (target_dir / "triz-contradiction" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert "Updated description." in skill_md
        assert "# Updated Body" in skill_md

    def test_source_error_returns_exit_1(
        self, repo_layout: Path, target_dir: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "install.install_claude_code._repo_root", lambda: repo_layout
        )
        # Corrupt the skill file
        skill_file = repo_layout / "skills" / "triz-contradiction.md"
        skill_file.write_text("no frontmatter here\n", encoding="utf-8")

        rc = main(["--target", str(target_dir)])
        assert rc == 1
        err = capsys.readouterr().err
        assert "error:" in err

    def test_install_reports_installed(
        self, repo_layout: Path, target_dir: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "install.install_claude_code._repo_root", lambda: repo_layout
        )
        rc = main(["--target", str(target_dir)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "installed" in out
        assert "triz-contradiction" in out

    def test_multiple_skills(
        self, repo_layout: Path, target_dir: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "install.install_claude_code._repo_root", lambda: repo_layout
        )
        # Add a second skill
        (repo_layout / "skills" / "triz-ideality.md").write_text(
            "---\n"
            "name: triz-ideality\n"
            "description: Evaluate ideality of a system.\n"
            "version: 0.1.0\n"
            "---\n"
            "# Ideality\n",
            encoding="utf-8",
        )

        rc = main(["--target", str(target_dir)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "triz-contradiction" in out
        assert "triz-ideality" in out
        assert (target_dir / "triz-contradiction" / "SKILL.md").is_file()
        assert (target_dir / "triz-ideality" / "SKILL.md").is_file()
