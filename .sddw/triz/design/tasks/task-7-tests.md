# Task 7: Tests for installers and reference loaders

## Trace
- **FR-IDs:** FR-04 (verifies install paths), FR-05 (idempotency), FR-13 (reference data integrity)
- **Depends on:** task-2, task-4, task-5

## Files
- `tests/__init__.py` — create (empty)
- `tests/conftest.py` — create
- `tests/test_source_loader.py` — create
- `tests/test_reference_data.py` — create
- `tests/test_install_claude.py` — create
- `tests/test_install_gemini.py` — create
- `tests/test_idempotency.py` — create

## Architecture

### Components
Pytest test modules. No new production code. Each test module verifies one slice:
- `test_source_loader`: schema enforcement in `lib.source.load_skills` (FR-03 mechanism)
- `test_reference_data`: structural integrity of `reference/*` (FR-13)
- `test_install_claude`: target-format correctness for Claude Code (FR-04 Claude path)
- `test_install_gemini`: target-format correctness for Gemini CLI (FR-04 Gemini path)
- `test_idempotency`: no-op re-runs and selective rewrites (FR-05)

### Data Flow
Tests use `tmp_path` (pytest fixture) as the install target — never touch `~/.claude` or `~/.gemini`. Reference data tests parse the actual repo `reference/*` files.

## Contracts

### Test discovery
Pytest discovers tests via `pyproject.toml` config from task-3. Run with:
```
pytest                    # all tests
pytest tests/test_install_claude.py    # one file
```

### `tests/conftest.py`
Provides shared fixtures:
- `repo_root`: `Path` to the repo root (resolves from `__file__`)
- `skills_dir`: `repo_root / "skills"`
- `reference_dir`: `repo_root / "reference"`

## Data Models

### Required test cases per file

#### `test_source_loader.py`
- `test_loads_valid_skill` — a valid frontmatter parses into a `Skill`
- `test_rejects_unknown_frontmatter_key` — frontmatter with `claude-tools: [...]` raises `SourceError` naming the key
- `test_rejects_name_filename_mismatch` — `name: foo` in `bar.md` raises `SourceError`
- `test_rejects_missing_required_field` — frontmatter missing `description` raises `SourceError`
- `test_loads_all_repo_skills` — `load_skills(skills_dir)` succeeds against the actual `skills/` directory; returns exactly 5 skills with names from the FR-01 set

#### `test_reference_data.py`
- `test_parameters_count_is_21` — parse `reference/parameters.md`, assert 21 entries with IDs 1..21
- `test_principles_count_is_40` — parse `reference/principles.md`, assert 40 entries with IDs 1..40
- `test_gof_mappings_resolve_to_principles` — every principle ID in `gof-mappings.md` is in 1..40
- `test_matrix_cells_well_formed` — `reference/matrix.json` parses, every cell key matches `\d+-\d+`, every parameter ID in 1..21, every principle ID in 1..40
- `test_matrix_sources_resolve` — every `sources` key referenced by any cell has a matching entry in `reference/matrix-sources.md`
- `test_matrix_has_minimum_cells` — at least 3 populated cells (per task-2 minimum bar)

#### `test_install_claude.py`
- `test_creates_skill_dir_per_skill` — running install (with `tmp_path` target) creates `<tmp>/<name>/SKILL.md` for each skill
- `test_skill_md_frontmatter_keys` — each `SKILL.md` has exactly `name` and `description` (no `version`, no `tags`)
- `test_skill_md_body_matches_canonical` — body content of `SKILL.md` equals the canonical body (after frontmatter stripping)
- `test_reference_bundled_per_skill` — each `<tmp>/<name>/reference/` contains every file from the repo's `reference/`
- `test_dry_run_writes_nothing` — `--dry-run` prints plan but creates no files in `tmp_path`

#### `test_install_gemini.py`
- `test_creates_extension_per_skill` — running install creates `<tmp>/<name>/gemini-extension.json` and `commands/<name>.toml` for each skill
- `test_manifest_keys` — manifest JSON has exactly `name`, `version`, `description`
- `test_command_toml_has_prompt` — `.toml` file has `prompt = """..."""` containing the canonical body
- `test_reference_bundled_per_extension` — each `<tmp>/<name>/reference/` contains every file from the repo's `reference/`
- `test_dry_run_writes_nothing` — `--dry-run` writes nothing
- `test_emit_raises_on_triple_quote_body` — synthetic skill with `"""` in body causes `EmitError`

#### `test_idempotency.py`
- `test_rerun_writes_nothing` (Claude) — install once, then again with no source change, assert second run reports `up-to-date` for every skill and the file mtimes/hashes are unchanged
- `test_rerun_writes_nothing` (Gemini) — same for Gemini installer
- `test_edited_body_triggers_only_that_skill_rewrite` (Claude) — edit one canonical body, re-run, assert only that skill's `SKILL.md` rewritten
- `test_edited_body_triggers_only_that_skill_rewrite` (Gemini) — same for Gemini, asserting `commands/<name>.toml` rewritten
- `test_changed_reference_triggers_reference_rewrite_in_all_skills` — modify `reference/parameters.md`, re-run, assert that file is rewritten under every skill but `SKILL.md` files are untouched

## Design Decisions

### `tmp_path` for install targets, never real `~/.claude` / `~/.gemini`
- **Chosen:** Every install test passes `--target tmp_path`
- **Rationale:** Tests must not touch the user's actual CLI installs. `tmp_path` (pytest builtin) is auto-cleaned per test.
- **Rejected:** Mocking `Path.home()` — fragile, easy to leak; `tmp_path` is the canonical pytest pattern.

### Test the actual repo content, not synthesized fixtures
- **Chosen:** `test_loads_all_repo_skills` and reference-data tests run against the real `skills/` and `reference/` directories
- **Rationale:** These are the integration tests that catch "the canonical content drifted from the schema." Synthetic-only tests would pass while production data was broken.
- **Rejected:** All-synthetic fixtures — would pass even if a contributor added a malformed reference file.

### TDD per requirements: tests written for installers and loaders; not for skill prompts
- **Chosen:** Test the install-time mechanics. Skill body quality is verified by running the skills against real contradictions, not by unit tests.
- **Rationale:** Per requirements section 6 ("Selective TDD") — TDD for installers and reference loaders, test-after for skill prompts (qualitative).
- **Rejected:** Snapshot tests of skill body output — brittle and don't measure what matters (does the skill actually resolve the contradiction).

## Acceptance Criteria

### FR-04: Install scripts for both CLIs (verified by tests)
- WHEN `test_install_claude.py` and `test_install_gemini.py` are run
- THEN they SHALL pass, demonstrating the installers create the expected target structure for each CLI

### FR-05: Idempotent install (verified by tests)
- WHEN `test_idempotency.py` is run
- THEN it SHALL pass, demonstrating: re-running with no change writes nothing; editing one source rewrites only that target

### FR-13: Reference data loadable (verified by structural tests)
- WHEN `test_reference_data.py` is run
- THEN it SHALL pass, demonstrating: 21 parameters present, 40 principles present, all cross-refs resolve

## Done Criteria
- [ ] `pytest` from repo root passes with all tests in this task
- [ ] Each test in the lists above exists and passes
- [ ] Tests use `tmp_path` for any install target — no test touches `~/.claude` or `~/.gemini`
- [ ] CI-friendly: tests do not require network, do not require Claude Code or Gemini CLI to be installed
- [ ] `pytest -v` output shows ≥ 25 test cases passing
