import json
import re
from pathlib import Path

def test_parameters_count_is_21(reference_dir: Path) -> None:
    content = (reference_dir / "parameters.md").read_text(encoding="utf-8")
    ids = set()
    for line in content.splitlines():
        match = re.match(r'^\|\s*(\d+)\s*\|', line)
        if match:
            ids.add(int(match.group(1)))
    assert ids == set(range(1, 22))

def test_principles_count_is_40(reference_dir: Path) -> None:
    content = (reference_dir / "principles.md").read_text(encoding="utf-8")
    ids = set()
    for line in content.splitlines():
        match = re.match(r'^\|\s*(\d+)\s*\|', line)
        if match:
            ids.add(int(match.group(1)))
    assert ids == set(range(1, 41))

def test_matrix_cells_well_formed(reference_dir: Path) -> None:
    data = json.loads((reference_dir / "matrix.json").read_text(encoding="utf-8"))
    for key, cell in data["cells"].items():
        assert re.match(r'^\d+-\d+$', key)
        p1, p2 = map(int, key.split('-'))
        assert 1 <= p1 <= 21
        assert 1 <= p2 <= 21
        for p_id in cell["principles"]:
            assert 1 <= p_id <= 40

def test_matrix_has_minimum_cells(reference_dir: Path) -> None:
    data = json.loads((reference_dir / "matrix.json").read_text(encoding="utf-8"))
    assert len(data["cells"]) >= 3
