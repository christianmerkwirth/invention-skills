"""Tests for install.lib.idempotency — sha256 content comparison."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import pytest

from install.lib.idempotency import content_hash, file_matches

# ---------------------------------------------------------------------------
# content_hash
# ---------------------------------------------------------------------------


class TestContentHash:
    def test_bytes_input(self) -> None:
        data = b"hello world"
        expected = hashlib.sha256(data).hexdigest()
        assert content_hash(data) == expected

    def test_str_input(self) -> None:
        data = "hello world"
        expected = hashlib.sha256(data.encode("utf-8")).hexdigest()
        assert content_hash(data) == expected

    def test_str_and_bytes_same_result(self) -> None:
        assert content_hash("café") == content_hash("café".encode("utf-8"))

    def test_empty_input(self) -> None:
        expected = hashlib.sha256(b"").hexdigest()
        assert content_hash(b"") == expected
        assert content_hash("") == expected

    def test_deterministic(self) -> None:
        assert content_hash("same") == content_hash("same")

    def test_different_inputs_differ(self) -> None:
        assert content_hash("a") != content_hash("b")


# ---------------------------------------------------------------------------
# file_matches
# ---------------------------------------------------------------------------


class TestFileMatches:
    def test_matching_content_str(self, tmp_path: Path) -> None:
        f = tmp_path / "file.txt"
        f.write_text("hello", encoding="utf-8")
        assert file_matches(f, "hello") is True

    def test_matching_content_bytes(self, tmp_path: Path) -> None:
        f = tmp_path / "file.bin"
        f.write_bytes(b"\x00\x01\x02")
        assert file_matches(f, b"\x00\x01\x02") is True

    def test_non_matching_content(self, tmp_path: Path) -> None:
        f = tmp_path / "file.txt"
        f.write_text("old", encoding="utf-8")
        assert file_matches(f, "new") is False

    def test_nonexistent_file(self, tmp_path: Path) -> None:
        assert file_matches(tmp_path / "nope", "anything") is False

    def test_empty_file_matches_empty(self, tmp_path: Path) -> None:
        f = tmp_path / "empty"
        f.write_bytes(b"")
        assert file_matches(f, b"") is True

    def test_empty_file_does_not_match_nonempty(self, tmp_path: Path) -> None:
        f = tmp_path / "empty"
        f.write_bytes(b"")
        assert file_matches(f, "content") is False


# ---------------------------------------------------------------------------
# Idempotency Install Tests
# ---------------------------------------------------------------------------

from install.install_claude_code import main as claude_main
from install.install_gemini_cli import main as gemini_main

@pytest.fixture()
def repo_layout(tmp_path: Path) -> Path:
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    ref_dir = tmp_path / "reference"
    ref_dir.mkdir()

    (skills_dir / "skill-a.md").write_text("---\nname: skill-a\ndescription: A\nversion: 0.1.0\n---\nBody A", encoding="utf-8")
    (skills_dir / "skill-b.md").write_text("---\nname: skill-b\ndescription: B\nversion: 0.1.0\n---\nBody B", encoding="utf-8")

    (ref_dir / "parameters.md").write_text("# Parameters\n", encoding="utf-8")
    return tmp_path

def test_rerun_writes_nothing_claude(repo_layout: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("install.install_claude_code._repo_root", lambda: repo_layout)
    target = tmp_path / "claude"
    
    rc = claude_main(["--target", str(target)])
    assert rc == 0
    assert "installed" in capsys.readouterr().out
    
    # Store mtimes
    mtimes = {p: p.stat().st_mtime for p in target.rglob("*") if p.is_file()}
    
    rc = claude_main(["--target", str(target)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "up-to-date" in out
    assert "installed" not in out
    
    # Verify mtimes unchanged
    new_mtimes = {p: p.stat().st_mtime for p in target.rglob("*") if p.is_file()}
    assert mtimes == new_mtimes

def test_rerun_writes_nothing_gemini(repo_layout: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("install.install_gemini_cli._repo_root", lambda: repo_layout)
    target = tmp_path / "gemini"
    
    rc = gemini_main(["--target", str(target)])
    assert rc == 0
    assert "installed" in capsys.readouterr().out
    
    mtimes = {p: p.stat().st_mtime for p in target.rglob("*") if p.is_file()}
    
    rc = gemini_main(["--target", str(target)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "up-to-date" in out
    assert "installed" not in out
    
    new_mtimes = {p: p.stat().st_mtime for p in target.rglob("*") if p.is_file()}
    assert mtimes == new_mtimes

def test_edited_body_triggers_only_that_skill_rewrite_claude(repo_layout: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("install.install_claude_code._repo_root", lambda: repo_layout)
    target = tmp_path / "claude"
    claude_main(["--target", str(target)])
    capsys.readouterr() # clear
    
    # Edit skill-a
    (repo_layout / "skills" / "skill-a.md").write_text("---\nname: skill-a\ndescription: A\nversion: 0.1.0\n---\nBody A CHANGED", encoding="utf-8")
    
    claude_main(["--target", str(target)])
    out = capsys.readouterr().out
    assert "updated: skill-a" in out
    assert "up-to-date: skill-b" in out

def test_edited_body_triggers_only_that_skill_rewrite_gemini(repo_layout: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("install.install_gemini_cli._repo_root", lambda: repo_layout)
    target = tmp_path / "gemini"
    gemini_main(["--target", str(target)])
    capsys.readouterr() # clear
    
    mtime_b = (target / "triz" / "commands" / "skill-b.toml").stat().st_mtime
    
    # Edit skill-a
    (repo_layout / "skills" / "skill-a.md").write_text("---\nname: skill-a\ndescription: A\nversion: 0.1.0\n---\nBody A CHANGED", encoding="utf-8")
    
    gemini_main(["--target", str(target)])
    out = capsys.readouterr().out
    assert "updated: triz" in out
    
    new_mtime_b = (target / "triz" / "commands" / "skill-b.toml").stat().st_mtime
    assert mtime_b == new_mtime_b

def test_changed_reference_triggers_reference_rewrite_in_all_skills(repo_layout: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("install.install_claude_code._repo_root", lambda: repo_layout)
    target = tmp_path / "claude"
    claude_main(["--target", str(target)])
    capsys.readouterr() # clear
    
    # Edit reference
    (repo_layout / "reference" / "parameters.md").write_text("# Parameters CHANGED\n", encoding="utf-8")
    
    claude_main(["--target", str(target)])
    out = capsys.readouterr().out
    
    assert "updated: skill-a" in out
    assert "updated: skill-b" in out
