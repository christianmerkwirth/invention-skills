# Task 6 Implementation Report

## Actions Taken
- Created `skills/triz-reference.md`
- Created `skills/triz-contradiction.md`
- Created `skills/triz-design-audit.md`
- Created `skills/triz-refactor.md`
- Created `skills/triz-sprint.md`

## Validation
- Confirmed canonical frontmatter (`name`, `description`, `version`, `tags`) for all files.
- Ensured required body sections (`When to invoke`, `Inputs needed`, `Reference data used`, `Procedure`, `Output format`) are present in all files.
- Confirmed "confirm before write" instructions are in procedures (except read-only `triz-reference`).
- Verified via regex search that tool-specific constructs (e.g., "AskUserQuestion", "MCP", "tool calls", "Claude", "Gemini") are entirely absent.
- Validated all 5 skills using `lib.source.load_skills(Path('skills'))`, parsing successfully without schema errors.