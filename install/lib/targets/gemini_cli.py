"""Transformer for Gemini CLI extensions.

Converts a canonical Skill into a set of EmittedFiles representing
a Gemini CLI extension, including its manifest, slash command,
and bundled reference files.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from install.lib.source import Skill


class EmitError(Exception):
    """Raised when a skill cannot be transformed into a Gemini extension."""


@dataclass(frozen=True)
class EmittedFile:
    """A file to be written to the target directory."""
    path: Path
    content: bytes


def emit(skills: list[Skill], target_root: Path, reference_files: list[Path]) -> list[EmittedFile]:
    """Compute the files that should exist for `skills` as a single 'triz' Gemini extension under `target_root`.
    
    Pre: target_root is an absolute path (may not yet exist).
    Post: returns:
      - <target_root>/triz/gemini-extension.json
      - <target_root>/triz/commands/<skill.name>.toml for each skill
      - <target_root>/triz/reference/<file> for each reference file
    Does NOT touch the filesystem.
    """
    if not skills:
        return []

    ext_name = "triz"
    ext_dir = target_root / ext_name
    results = []

    # gemini-extension.json
    manifest = {
        "name": ext_name,
        "version": skills[0].version,
        "description": "TRIZ skills for software engineering"
    }
    manifest_bytes = json.dumps(manifest, indent=2).encode("utf-8")
    results.append(EmittedFile(
        path=ext_dir / "gemini-extension.json",
        content=manifest_bytes
    ))

    # commands/<skill.name>.toml
    for skill in skills:
        if '"""' in skill.body:
            raise EmitError(f"Skill body for {skill.name} contains '\"\"\"' which conflicts with TOML triple quotes.")
        
        # Ensure description double-quotes are escaped if any
        safe_description = skill.description.replace('"', '\\"')
        command_toml = (
            f'description = "{safe_description}"\n'
            f'prompt = """\n{skill.body}\n"""\n'
        )
        results.append(EmittedFile(
            path=ext_dir / "commands" / f"{skill.name}.toml",
            content=command_toml.encode("utf-8")
        ))

    # reference files
    for ref_file in reference_files:
        results.append(EmittedFile(
            path=ext_dir / "reference" / ref_file.name,
            content=ref_file.read_bytes()
        ))
    
    return results
