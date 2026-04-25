# TRIZ Skills for Coding CLIs

A suite of specialized tools that bring the Theory of Inventive Problem Solving (TRIZ) into modern software engineering workflows. This repository provides canonical skill definitions and reference data, along with installers for popular AI coding assistants like Claude Code and Gemini CLI, enabling them to systematically resolve contradictions, audit designs, and improve system ideality.

## Skills in the suite
- **triz-contradiction**: Resolves software engineering contradictions by identifying conflicting parameters and suggesting principles.
- **triz-design-audit**: Reviews a proposed design or module to surface hidden contradictions and map them to GoF and TRIZ principles.
- **triz-refactor**: Refactors a module by applying a chosen TRIZ principle or auditing for ideality gaps.
- **triz-reference**: Browses the TRIZ parameters, principles, and GoF correlations interactively.
- **triz-sprint**: Applies TRIZ in Agile workflows for morphological backlog refinement and prototype effects extraction.

## Install

### Claude Code
```bash
python -m install.install_claude_code
```
This installer reads the canonical skill source files and generates Claude Code compatible skills (with frontmatter stripped and bundled reference data) in your local Claude config directory (defaults to `~/.claude/skills`).

### Gemini CLI
```bash
python -m install.install_gemini_cli
```
This installer reads the canonical skill source files and generates Gemini CLI compatible extensions. Each skill is packaged with a `gemini-extension.json`, a command TOML file containing the skill body and description, and the bundled reference data in your local Gemini config directory (defaults to `~/.gemini/extensions`).

### Both
Note that both install scripts are idempotent. They use content-hash comparisons to determine if files have changed, meaning it is perfectly safe to re-run them repeatedly after a `git pull` without blindly overwriting files.

## Using a skill
Once installed, you can invoke a skill directly through your CLI agent. For example, using the contradiction resolver:
```
invoke triz-contradiction. I want to improve speed, but that worsens security. Scope: backend/auth.
```
The agent will consult the TRIZ contradiction matrix, map these concepts to software parameters, and output a suggested architectural principle (e.g., "Segmentation" or "Prior Action") along with a proposed code diff.

## Authoring a new skill
To author a new skill, create a new Markdown file in the `skills/` directory. The file must follow the canonical source schema: it needs standard YAML frontmatter defining `name`, `description`, `version`, and `tags`, followed by a Markdown body containing the skill's instructions or prompt. The runtime protocol dictates that the body will have access to the `reference/` data via the relative path `reference/<file>`.

## Porting to another CLI

This section contains the install contract. A reader of an unlisted CLI can write their own installer using only this section, without reading any skill source file.

### 1. Canonical source schema
The canonical source consists of Markdown files with YAML frontmatter. The frontmatter MUST contain exactly the following four allowed keys:
- `name` (string)
- `description` (string)
- `version` (string)
- `tags` (list of strings)

The rest of the file is the skill body (Markdown text).

### 2. Target format requirements
For any CLI installer to be correct, it must uphold these invariants:
- **One target artifact per skill** (the CLI's native skill/extension format).
- The artifact's **name** field MUST equal the canonical `name`.
- The artifact's **description** field MUST equal the canonical `description`.
- The skill **body** MUST be embedded verbatim (no rewriting; no path translation).
- A copy of the **`reference/`** directory MUST be available to the skill at runtime via the relative path `reference/<file>`.
- The installer MUST be **idempotent** (use content-hash compare; do not blindly overwrite).

### 3. Worked example
Here is a complete walk-through showing how the canonical `skills/triz-contradiction.md` is transformed by installers.

**Input: `skills/triz-contradiction.md`**
```markdown
---
name: triz-contradiction
description: Resolves software engineering contradictions by identifying conflicting parameters and suggesting principles.
version: 0.1.0
tags: [triz, contradiction, problem-solving]
---

## When to invoke
Invoke this skill when facing a technical trade-off or contradiction where improving one aspect worsens another (e.g., improving speed worsens security).

[... rest of the body ...]
```

**Output for Claude Code:**
Produces `~/.claude/skills/triz-contradiction/SKILL.md` (and copies `reference/` into `~/.claude/skills/triz-contradiction/reference/`):
```markdown
---
name: triz-contradiction
description: Resolves software engineering contradictions by identifying conflicting parameters and suggesting principles.
---

## When to invoke
Invoke this skill when facing a technical trade-off or contradiction where improving one aspect worsens another (e.g., improving speed worsens security).

[... rest of the body ...]
```

**Output for Gemini CLI:**
Produces `~/.gemini/extensions/triz-contradiction/gemini-extension.json`:
```json
{
  "name": "triz-contradiction",
  "version": "0.1.0",
  "description": "Resolves software engineering contradictions by identifying conflicting parameters and suggesting principles."
}
```
And produces `~/.gemini/extensions/triz-contradiction/commands/triz-contradiction.toml` (along with copying `reference/` to `~/.gemini/extensions/triz-contradiction/reference/`):
```toml
description = "Resolves software engineering contradictions by identifying conflicting parameters and suggesting principles."
prompt = """

## When to invoke
Invoke this skill when facing a technical trade-off or contradiction where improving one aspect worsens another (e.g., improving speed worsens security).

[... rest of the body ...]
"""
```

### 4. Suggested implementation skeleton
Here is pseudocode showing the general loop for an installer. You can refer to `install/lib/source.py` for a reusable source loader in Python.

```python
from install.lib.source import load_skills
import shutil

def install_for_my_cli():
    for skill in load_skills("skills"):
        target_dir = f"~/.my-cli/plugins/{skill.name}"
        
        # 1. Emit native artifacts using skill.name, skill.description, skill.body
        emit_native_artifact(target_dir, skill)
        
        # 2. Copy reference directory
        shutil.copytree("reference", f"{target_dir}/reference", dirs_exist_ok=True)
        
        # Note: Implement idempotency by hashing files before writing!
```

## Repo layout
- `doc/` — Background and methodology documentation (e.g., TRIZ for Software Engineering).
- `install/` — Install scripts and reusable installer library for target CLIs.
- `reference/` — Static data files (matrices, parameters, principles) used by the skills at runtime.
- `skills/` — Canonical Markdown source files for the TRIZ skills.
- `tests/` — Test suite for the installers and source loaders.

## Reference data
The `reference/` directory contains JSON and Markdown files loaded by skills during execution to map problems to TRIZ solutions. This includes `parameters.md` for parameter definitions, `matrix.json` for the contradiction matrix, `principles.md` for inventive principles, and `gof-mappings.md` for corresponding software design patterns. These files must be accessible relative to the installed skill's root at `reference/<file>`.

## Testing
Run the test suite using pytest:
```bash
pytest
```
The test suite verifies the behavior of the source loaders, target format transformers (such as Claude Code and Gemini CLI builders), and idempotency checks. Note that the skill prompts themselves are qualitative and should be verified by running them in your target CLI agent.

## License
MIT License
