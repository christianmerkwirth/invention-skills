"""Claude Code target transformer."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from install.lib.source import Skill


@dataclass(frozen=True)
class EmittedFile:
    path: Path
    content: bytes


def emit(skill: Skill, target_root: Path, reference_files: list[Path]) -> list[EmittedFile]:
    """Compute the files that should exist for `skill` under `target_root`.
    
    Pre: target_root is an absolute path (may not yet exist).
    Post: returns:
      - one EmittedFile for SKILL.md (frontmatter with name+description, then body)
      - one EmittedFile per reference file, mirrored under <skill_dir>/reference/
    Does NOT touch the filesystem.
    """
    skill_dir = target_root / skill.name
    emitted = []

    # Emit SKILL.md
    frontmatter = f"---\nname: {skill.name}\ndescription: {skill.description}\n---\n"
    skill_content = (frontmatter + skill.body).encode("utf-8")
    emitted.append(EmittedFile(path=skill_dir / "SKILL.md", content=skill_content))

    # Emit reference files
    ref_dir = skill_dir / "reference"
    for ref_path in reference_files:
        content = ref_path.read_bytes()
        emitted.append(EmittedFile(path=ref_dir / ref_path.name, content=content))

    return emitted
