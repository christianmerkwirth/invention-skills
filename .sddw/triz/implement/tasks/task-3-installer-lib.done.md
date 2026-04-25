# Task 3: Installer shared lib — canonical source loader and idempotency

Completed successfully.

## Verification Results

### Automated Tests
Ran `PYTHONPATH=. pytest tests/test_source.py tests/test_idempotency.py`:
- `tests/test_source.py`: 25 passed
- `tests/test_idempotency.py`: 12 passed
- Total: 37 passed

### Manual Verification
- Verified `install/lib/source.py` implements strict frontmatter validation (FR-03).
- Verified `install/lib/idempotency.py` uses sha256 for content comparison (FR-05).
- Verified `pyproject.toml` contains correct metadata and dev dependencies.
- Confirmed all required `__init__.py` files are present.
- Confirmed type annotations are used throughout the implementation.
