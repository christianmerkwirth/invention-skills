# Task 8: README and install contract documentation

## Trace
- **FR-IDs:** FR-06 (porting documentation)
- **Depends on:** task-4, task-5

## Files
- `README.md` — create

## Architecture

### Components
Top-level `README.md` is the single user-facing document. It serves three audiences:
1. **End users** — what the suite is, how to install, how to use the skills
2. **Authors** — how to add or edit a skill in the canonical source
3. **Porters** — how to write an installer for a new CLI without editing any skill source file (the FR-06 install contract)

### Data Flow
README is static documentation. Reflects what tasks 1–7 actually shipped (write this last so the contract is real, not aspirational).

## Contracts

### Required README sections (in order)

```markdown
# TRIZ Skills for Coding CLIs

[2-3 sentence description: what this is, who it's for]

## Skills in the suite
[Bullet list of the 5 skills, each with one-line description]

## Install

### Claude Code
```
python -m install.install_claude_code
```
[Brief explanation of what this writes and where]

### Gemini CLI
```
python -m install.install_gemini_cli
```
[Brief explanation of what this writes and where]

### Both
[Note that scripts are idempotent — safe to re-run after `git pull`]

## Using a skill
[Brief example: invoke `triz-contradiction` with two parameters; show the kind of output to expect]

## Authoring a new skill
[How to add a new file to `skills/`. The canonical source schema. The runtime protocol the body should follow.]

## Porting to another CLI                            ← FR-06 lives here
[The install contract. See "Install contract" subsection requirements below.]

## Repo layout
[Tree of the repo with one-line description of each directory]

## Reference data
[What lives in `reference/`, when each file is loaded by skills]

## Testing
```
pytest
```
[What's tested, what's not (skill prompts are qualitative — test by running)]

## License
[TBD by author — placeholder ok]
```

### "Porting to another CLI" section — required content (FR-06)

This section MUST include all four items below. A reader of an unlisted CLI must be able to write their own installer using only this section, without reading any skill source.

1. **Canonical source schema** — exact frontmatter shape and the four allowed keys (`name`, `description`, `version`, `tags`). Reference task-3's schema definition.
2. **Target format requirements** — for any CLI installer to be correct:
   - One target artifact per skill (the CLI's native skill/extension format)
   - The artifact's "name" field MUST equal the canonical `name`
   - The artifact's "description" field MUST equal the canonical `description`
   - The skill body MUST be embedded verbatim (no rewriting; no path translation)
   - A `reference/` copy MUST be available to the skill at runtime via the relative path `reference/<file>`
   - The installer MUST be idempotent (use content-hash compare; do not blindly overwrite)
3. **Worked example** — a complete walk-through showing how the canonical `skills/triz-contradiction.md` becomes:
   - Claude Code's `~/.claude/skills/triz-contradiction/SKILL.md` + bundled `reference/`
   - Gemini CLI's `~/.gemini/extensions/triz-contradiction/gemini-extension.json` + `commands/triz-contradiction.toml` + bundled `reference/`
   Show the input file contents and both output forms side-by-side. The reader should understand the transformation pattern from this single example.
4. **Suggested implementation skeleton** — pseudocode (~10 lines) showing the loop: `for each skill in load_skills(): emit native artifacts; copy reference/`. Reference `install/lib/source.py` as the reusable source loader (Python).

## Data Models

(No new data models — this is documentation reflecting models defined in tasks 1–6.)

## Design Decisions

### Single README, no separate `docs/` directory
- **Chosen:** Everything in one `README.md`
- **Rationale:** v1 is small enough that one file is more discoverable than a `docs/` tree. GitHub renders README on the repo home page — porting docs are immediately visible.
- **Rejected:** `docs/PORTING.md`, `docs/AUTHORING.md`, etc. — adds navigation overhead for a small project.

### Worked example shows BOTH Claude and Gemini transformations
- **Chosen:** Side-by-side example in the porting section
- **Rationale:** A reader writing a third installer benefits from seeing the pattern (verbatim body + minimal frontmatter projection + reference bundle) demonstrated twice. One example might look like an artifact of one CLI's quirks; two examples reveal the underlying contract.
- **Rejected:** One example only — risk that the reader generalizes wrong.

### Document the contract, not the code
- **Chosen:** Porting section describes WHAT the installer must produce, not HOW (no Python-specific instructions beyond the optional skeleton)
- **Rationale:** FR-06 says "without editing any skill source file" — the contract is portable across implementation languages.
- **Rejected:** "Here's how to write a Python installer" tutorial — narrows the audience to Python users.

### Write README last
- **Chosen:** Depends on tasks 4 and 5 so the documented contract reflects what was actually built
- **Rationale:** Writing docs first risks documenting an idealized installer that diverges from reality. Reflect the shipped behavior verbatim.

## Acceptance Criteria

### FR-06: Install contract documented
- GIVEN the repo README
- WHEN a user of an unlisted CLI reads the "Porting to another CLI" section
- THEN they SHALL find:
  - the canonical source schema (4 frontmatter keys named explicitly)
  - the target format requirements (the 6 invariants listed above in `Contracts`)
  - a worked example showing the canonical input AND both Claude and Gemini outputs
- AND they SHALL be able to author their own installer using only this section, without modifying any skill source file

## Done Criteria
- [ ] `README.md` exists at repo root
- [ ] All required sections present in the order listed above
- [ ] Install commands documented match the actual `--help` output of `install_claude_code.py` and `install_gemini_cli.py`
- [ ] "Porting to another CLI" section contains all 4 required items (schema, target requirements, worked example, skeleton)
- [ ] Worked example shows the transformation of `skills/triz-contradiction.md` into both Claude and Gemini output forms with literal file contents
- [ ] No section refers to features that aren't implemented (idempotency claim matches what tests verify; install paths match what installers actually write)
- [ ] All 5 skill names listed match the files in `skills/`
