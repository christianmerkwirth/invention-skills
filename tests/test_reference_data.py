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

def test_gof_mappings_resolve_to_principles(reference_dir: Path) -> None:
    content = (reference_dir / "gof-mappings.md").read_text(encoding="utf-8")
    for line in content.splitlines():
        # Match data rows: | Pattern | Category | ID | ...
        if line.startswith('|') and '---' not in line and 'Pattern' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                try:
                    p_id = int(parts[3])
                    assert 1 <= p_id <= 40
                except ValueError:
                    pass

def test_matrix_cells_well_formed(reference_dir: Path) -> None:
    data = json.loads((reference_dir / "matrix.json").read_text(encoding="utf-8"))
    for key, cell in data["cells"].items():
        assert re.match(r'^\d+-\d+$', key)
        p1, p2 = map(int, key.split('-'))
        assert 1 <= p1 <= 21
        assert 1 <= p2 <= 21
        for p_id in cell["principles"]:
            assert 1 <= p_id <= 40

def test_matrix_sources_resolve(reference_dir: Path) -> None:
    data = json.loads((reference_dir / "matrix.json").read_text(encoding="utf-8"))
    sources_content = (reference_dir / "matrix-sources.md").read_text(encoding="utf-8")
    
    defined_sources = set()
    for line in sources_content.splitlines():
        if line.startswith('## '):
            defined_sources.add(line[3:].strip())
            
    for cell in data["cells"].values():
        for source in cell.get("sources", []):
            assert source in defined_sources

def test_matrix_has_minimum_cells(reference_dir: Path) -> None:
    data = json.loads((reference_dir / "matrix.json").read_text(encoding="utf-8"))
    assert len(data["cells"]) >= 3
