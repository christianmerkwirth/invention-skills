import pytest
from pathlib import Path

@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).parent.parent.resolve()

@pytest.fixture
def skills_dir(repo_root: Path) -> Path:
    return repo_root / "skills"

@pytest.fixture
def reference_dir(repo_root: Path) -> Path:
    return repo_root / "reference"
