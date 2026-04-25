import json
import pytest
from pathlib import Path
from install.lib.source import Skill
from install.lib.targets.gemini_cli import emit, EmitError
from install.install_gemini_cli import main

def test_emit_success(tmp_path):
    skill1 = Skill(
        name="test-skill-1",
        description="A test skill 1",
        version="1.0.0",
        body="This is a test body 1.",
        source_path=Path("skills/test-skill-1.md"),
    )
    skill2 = Skill(
        name="test-skill-2",
        description="A test skill 2",
        version="1.0.0",
        body="This is a test body 2.",
        source_path=Path("skills/test-skill-2.md"),
    )
    
    target_root = tmp_path / "extensions"
    
    # Create mock reference files
    ref_dir = tmp_path / "reference"
    ref_dir.mkdir()
    ref_file1 = ref_dir / "test1.json"
    ref_file1.write_bytes(b'{"test": 1}')
    ref_file2 = ref_dir / "test2.md"
    ref_file2.write_bytes(b'# Test 2')
    
    reference_files = [ref_file1, ref_file2]
    
    emitted = emit([skill1, skill2], target_root, reference_files)
    
    # Should emit 1 manifest + 2 command toml + 2 ref files = 5 files
    assert len(emitted) == 5
    
    emitted_dict = {ef.path: ef.content for ef in emitted}
    
    ext_dir = target_root / "triz"
    
    # Check manifest
    manifest_path = ext_dir / "gemini-extension.json"
    assert manifest_path in emitted_dict
    manifest = json.loads(emitted_dict[manifest_path].decode("utf-8"))
    assert manifest["name"] == "triz"
    assert manifest["version"] == "1.0.0"
    
    # Check command TOML
    toml_path1 = ext_dir / "commands" / "test-skill-1.toml"
    assert toml_path1 in emitted_dict
    toml_content1 = emitted_dict[toml_path1].decode("utf-8")
    assert 'description = "A test skill 1"' in toml_content1
    assert 'prompt = """\nThis is a test body 1.\n"""' in toml_content1

    toml_path2 = ext_dir / "commands" / "test-skill-2.toml"
    assert toml_path2 in emitted_dict
    toml_content2 = emitted_dict[toml_path2].decode("utf-8")
    assert 'description = "A test skill 2"' in toml_content2
    assert 'prompt = """\nThis is a test body 2.\n"""' in toml_content2
    
    # Check reference files
    ref1_path = ext_dir / "reference" / "test1.json"
    assert ref1_path in emitted_dict
    assert emitted_dict[ref1_path] == b'{"test": 1}'
    
    ref2_path = ext_dir / "reference" / "test2.md"
    assert ref2_path in emitted_dict
    assert emitted_dict[ref2_path] == b'# Test 2'


def test_emit_fails_on_triple_quotes(tmp_path):
    skill = Skill(
        name="test-skill",
        description="A test skill",
        version="1.0.0",
        body='This body contains """ which is bad.',
        source_path=Path("skills/test-skill.md"),
    )
    
    target_root = tmp_path / "extensions"
    reference_files = []
    
    with pytest.raises(EmitError, match="conflicts with TOML triple quotes"):
        emit([skill], target_root, reference_files)


def test_emit_escapes_quotes_in_description(tmp_path):
    skill = Skill(
        name="test-skill",
        description='A test "skill"',
        version="1.0.0",
        body="Body",
        source_path=Path("skills/test-skill.md"),
    )
    
    target_root = tmp_path / "extensions"
    emitted = emit([skill], target_root, [])
    
    toml_path = target_root / "triz" / "commands" / "test-skill.toml"
    emitted_dict = {ef.path: ef.content for ef in emitted}
    toml_content = emitted_dict[toml_path].decode("utf-8")
    
    assert 'description = "A test \\"skill\\""' in toml_content


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
    return tmp_path


@pytest.fixture()
def target_dir(tmp_path: Path) -> Path:
    return tmp_path / "target_extensions"


def test_creates_single_extension(repo_layout: Path, target_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("install.install_gemini_cli._repo_root", lambda: repo_layout)
    rc = main(["--target", str(target_dir)])
    assert rc == 0
    ext_dir = target_dir / "triz"
    assert ext_dir.is_dir()
    assert (ext_dir / "gemini-extension.json").is_file()
    assert (ext_dir / "commands" / "triz-contradiction.toml").is_file()


def test_manifest_keys(repo_layout: Path, target_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("install.install_gemini_cli._repo_root", lambda: repo_layout)
    main(["--target", str(target_dir)])
    manifest_path = target_dir / "triz" / "gemini-extension.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert set(manifest.keys()) == {"name", "version", "description"}


def test_command_toml_has_prompt(repo_layout: Path, target_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("install.install_gemini_cli._repo_root", lambda: repo_layout)
    main(["--target", str(target_dir)])
    toml_path = target_dir / "triz" / "commands" / "triz-contradiction.toml"
    content = toml_path.read_text(encoding="utf-8")
    assert 'prompt = """\n# TRIZ Contradiction\n\nLook up `reference/parameters.md`.\n\n"""' in content


def test_reference_bundled(repo_layout: Path, target_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("install.install_gemini_cli._repo_root", lambda: repo_layout)
    main(["--target", str(target_dir)])
    ref_dir = target_dir / "triz" / "reference"
    assert ref_dir.is_dir()
    assert (ref_dir / "parameters.md").is_file()


def test_dry_run_writes_nothing(repo_layout: Path, target_dir: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("install.install_gemini_cli._repo_root", lambda: repo_layout)
    rc = main(["--dry-run", "--target", str(target_dir)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "[dry-run]" in out
    assert not target_dir.exists()
