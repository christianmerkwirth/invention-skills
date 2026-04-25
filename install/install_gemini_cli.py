"""CLI wrapper to install skills for Gemini CLI."""

import argparse
import sys
from pathlib import Path

from install.lib.idempotency import file_matches
from install.lib.source import SourceError, load_reference_files, load_skills
from install.lib.targets.gemini_cli import emit, EmittedFile, EmitError


def _repo_root() -> Path:
    """Return the repository root directory."""
    return Path(__file__).resolve().parent.parent


def _write_file(ef: EmittedFile, dry_run: bool) -> str:
    """Write an emitted file conditionally and return its status.
    
    Returns 'up-to-date', 'installed', or 'updated'.
    """
    if file_matches(ef.path, ef.content):
        return "up-to-date"
    
    existed = ef.path.exists()
    
    if not dry_run:
        ef.path.parent.mkdir(parents=True, exist_ok=True)
        ef.path.write_bytes(ef.content)
        
    if not existed:
        return "installed"
    return "updated"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install skills for Gemini CLI.")
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.home() / ".gemini" / "extensions",
        help="Target directory (defaults to ~/.gemini/extensions)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions but write nothing",
    )
    args = parser.parse_args(argv)

    project_root = _repo_root()
    skills_dir = project_root / "skills"
    reference_dir = project_root / "reference"

    target_root = args.target.resolve()

    try:
        skills = load_skills(skills_dir)
        reference_files = load_reference_files(reference_dir)
    except SourceError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"error: reading source files: {e}", file=sys.stderr)
        return 1

    prefix = "[dry-run] " if args.dry_run else ""

    try:
        emitted_files = emit(skills, target_root, reference_files)
    except EmitError as e:
        print(f"error: emitting triz extension: {e}", file=sys.stderr)
        return 1
    
    # Calculate extension level status based on file level statuses
    ext_status = "up-to-date"
    for emitted in emitted_files:
        file_status = _write_file(emitted, args.dry_run)
        if file_status == "installed" and ext_status != "updated":
            ext_status = "installed"
        elif file_status == "updated":
            ext_status = "updated"

    ext_dir = target_root / "triz"
    print(f"{prefix}{ext_status}: triz -> {ext_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
