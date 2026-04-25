# Verification Report: triz

## Summary
- **Date:** 2026-04-25
- **FRs:** 15/15 passed, 0 failed, 0 partial
- **Tests:** 88 passed, 0 failed, 0 skipped
- **Result:** PASS

## Test Execution
- **Runner:** pytest
- **Command:** `pytest tests/ -v`
- **Duration:** ~0.13s

### Failures
None.

## FR Verification

### FR-01: Suite covers five use cases — PASS

**Acceptance Criteria:**
- [x] Five distinct skills present for all use cases — verified by `test_source_loader.py::TestLoadReferenceFiles::test_loads_all_repo_skills`

**Done Criteria** (from task-6):
- [x] `skills/triz-contradiction.md` — contradiction resolution
- [x] `skills/triz-design-audit.md` — design audit
- [x] `skills/triz-refactor.md` — code refactoring
- [x] `skills/triz-reference.md` — TRIZ reference/learning
- [x] `skills/triz-sprint.md` — Agile'TRIZ sprint planning/retro

**Issues:** None.

---

### FR-02: Skills invokable independently — PASS

**Acceptance Criteria:**
- [x] Each skill file is standalone with no dependency on a central dispatcher

**Done Criteria** (from task-6):
- [x] No cross-skill `import` or dispatcher references in any skill body
- [x] Each skill's frontmatter is self-contained

**Issues:** None.

---

### FR-03: Single neutral source — PASS

**Acceptance Criteria:**
- [x] Skills contain only `name`, `description`, `version`, `tags` frontmatter — enforced by `load_skills()` strict allowlist, verified by `test_source_loader.py::TestLoadSkillsErrors::test_unknown_key_raises_source_error`

**Done Criteria** (from task-3):
- [x] `load_skills` rejects any frontmatter key outside `{name, description, version, tags}`
- [x] All five skill files pass `load_skills()` without `SourceError`

**Issues:** None.

---

### FR-04: Install scripts for both CLIs — PASS

**Acceptance Criteria:**
- [x] `install/install_claude_code.py` exists and places skills in Claude Code format — verified by `test_install_claude.py` (17 tests)
- [x] `install/install_gemini_cli.py` exists and places skills in Gemini CLI extension format — verified by `test_install_gemini.py` (9 tests)

**Done Criteria** (from tasks 4 & 5):
- [x] Claude Code: emits per-skill `.md` with only `name`/`description` frontmatter
- [x] Gemini CLI: emits `gemini-extension.json`, `commands/<skill>.toml`, and `reference/` bundle per skill
- [x] Both scripts support `--dry-run` and `--target` flags

**Issues:** None.

---

### FR-05: Idempotent install — PASS

**Acceptance Criteria:**
- [x] Re-running install writes nothing when content is unchanged — verified by `test_idempotency.py::test_rerun_writes_nothing_claude` and `test_rerun_writes_nothing_gemini`
- [x] Only changed files are rewritten — verified by `test_edited_body_triggers_only_that_skill_rewrite_claude/gemini`
- [x] Changed reference file triggers re-emit across all skills — verified by `test_changed_reference_triggers_reference_rewrite_in_all_skills`

**Done Criteria** (from task-3):
- [x] `content_hash` and `file_matches` use sha256 — `test_idempotency.py::TestContentHash` (6 tests), `TestFileMatches` (6 tests)

**Issues:** None.

---

### FR-06: Install contract documented — PASS

**Acceptance Criteria:**
- [x] README "Porting to another CLI" section contains canonical source schema, target format requirements, and worked example

**Done Criteria** (from task-8):
- [x] `README.md` exists at repo root
- [x] Includes worked example transforming `triz-contradiction.md` to both Claude Code and Gemini CLI formats
- [x] Includes pseudocode implementation skeleton

**Issues:** None.

---

### FR-07: Reasoning named — PASS

**Acceptance Criteria:**
- [x] Contradiction skill procedure names principle by ID and name, both IT parameters, and the contradiction in a single sentence before proposing changes — confirmed in `skills/triz-contradiction.md` step 5 and output format section

**Done Criteria** (from task-6):
- [x] All applicable skills include "Reference data used" section citing parameter/principle files

**Issues:** None.

---

### FR-08: No silent changes — PASS

**Acceptance Criteria:**
- [x] Skill presents reasoning and waits for confirmation before editing — `skills/triz-contradiction.md` step 7: "Stop. Ask the user to confirm. Do not proceed until they reply."
- [x] Skill does not write files if user rejects — conditional on step 7 gate

**Issues:** None.

---

### FR-09: Acknowledge gaps — PASS

**Acceptance Criteria:**
- [x] When matrix cell is empty, skill reports gap and declines to force-fit — `skills/triz-contradiction.md` step 4: "report the gap honestly, list the principles considered based on general heuristics, and STOP. Do not force a fit."

**Issues:** None.

---

### FR-10: Scope to the problem — PASS

**Acceptance Criteria:**
- [x] Skill proposes changes only within the user-named module — step 6: "scoped strictly to the user-named module"; step 8: "apply edits only within the specified module scope"

**Issues:** None.

---

### FR-11: No new major deps — PASS

**Acceptance Criteria:**
- [x] Skill does not introduce dependencies without opt-in — step 8: "Do not introduce new major dependencies without explicit opt-in."

**Issues:** None.

---

### FR-12: Destructive-op confirmation — PASS

**Acceptance Criteria:**
- [x] Skill confirms each destructive operation separately — step 8: "Confirm separately before any destructive operation."

**Issues:** None.

---

### FR-13: Reference data loadable — PASS

**Acceptance Criteria:**
- [x] 21 parameters present and structured — verified by `test_reference_data.py::test_parameters_count_is_21`
- [x] 40 principles present and structured — verified by `test_reference_data.py::test_principles_count_is_40`
- [x] Matrix cells well-formed with citations — verified by `test_reference_data.py::test_matrix_cells_well_formed` and `test_matrix_sources_resolve`

**Issues:** None.

---

### FR-14: GoF citation — PASS

**Acceptance Criteria:**
- [x] GoF mappings file present and cross-referenced to principles — verified by `test_reference_data.py::test_gof_mappings_resolve_to_principles`
- [x] `skills/triz-design-audit.md` and `skills/triz-contradiction.md` cite `reference/gof-mappings.md`

**Issues:** None.

---

### FR-15: Sprint workflows — PASS

**Acceptance Criteria:**
- [x] Morphological matrix mode: generates bounded combined ideas with principle attributions — `skills/triz-sprint.md` step 2
- [x] Effects-extraction mode: lists positive/harmful effects, reframes harmful effects as fresh contradictions — `skills/triz-sprint.md` step 3

**Issues:** None.

---

## Deviations
- Task 1: Rule 2 — added "Typical contradiction resolved" annotations to `reference/gof-mappings.md` — **accepted** (adds value without violating any FR)
- Task 2: Rule 2 — added a fourth matrix cell (5-2, Speed vs Size Dynamic) grounded in Flyweight/Principle-17 citation — **accepted** (expands useful coverage, citation rule satisfied)

## Remediation Tasks
None — all checks passed.

## Warnings
None.
