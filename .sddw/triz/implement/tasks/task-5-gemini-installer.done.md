# Task 5 Completion Report: Gemini CLI installer + transformer

## Summary
Implemented the pure transformer `install/lib/targets/gemini_cli.py` to calculate emitted file paths and contents for Gemini CLI extensions. Implemented the CLI runner `install/install_gemini_cli.py` using argparse, loading skills via `install.lib.source` and using idempotent writes via `install.lib.idempotency`. Verified that the transformer creates a manifest file, a command TOML file, and copies the reference directory properly. Added unit tests for the transformer to ensure it successfully generates the artifacts and rejects TOML triple-quote collisions.

## Technical notes
- `emit()` in the transformer correctly computes the layout for Gemini CLI: `gemini-extension.json`, `commands/<skill>.toml`, and `reference/*`.
- `emit()` explicitly checks and raises an `EmitError` if a triple-quote (`"""`) exists in the canonical markdown body, since this would break TOML multi-line string parsing for the `prompt`.
- `install_gemini_cli.py` exposes `--dry-run` and `--target` CLI flags, with a default target of `~/.gemini/extensions`.
- Handled skill-level status aggregation (`installed`, `updated`, `up-to-date`) dynamically, consistent with the Claude installer implementation.

## Verification
- Verified all acceptance criteria using `pytest` for the `emit` unit tests. The script behaves correctly on dry-runs (even if no skills are present), and dynamically generates output identical in structure to the requirements. Idempotency correctly uses hash checks before mutating standard files.