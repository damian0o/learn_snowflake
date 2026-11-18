from pathlib import Path

import pytest

from check_links import dangling, find_wikilinks, main, orphans, scan_vault, unresolved_quiz_concepts


def write(vault: Path, rel: str, text: str) -> None:
    p = vault / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


@pytest.fixture
def vault(tmp_path):
    v = tmp_path / "vault"
    write(v, "00 Home.md", "# Home\n[[Day 1]] [[Virtual Warehouse|warehouses]]\n")
    write(v, "Syllabus/Day 1.md", "---\ntags: [syllabus, day1]\n---\n[[virtual warehouse]] [[Caching#Result cache]]\n")
    write(v, "Concepts/Virtual Warehouse.md", "---\ntags: [concept, day1]\n---\n# VW\n[[Caching]] ![[Diagram]]\n```\n[[Not A Link]]\n```\ninline `[[Also Not]]` here\n")
    write(v, "Concepts/Caching.md", "---\ntags: [concept, day1]\n---\n# Caching\n[[Virtual Warehouse]]\n")
    write(v, "Concepts/Lonely.md", "---\ntags: [concept, day2]\n---\n# Lonely\n[[Caching]]\n")
    write(v, "Concepts/Diagram.md", "---\ntags: [concept, day1]\n---\n# D\n[[Caching]]\n")
    write(v, "Templates/Concept.md", "[[<parent idea>]] [[Nope]]\n")
    write(v, ".obsidian/graph.json", "{}")
    return v


def test_find_wikilinks_variants():
    text = "[[A]] [[B|alias]] [[C#Head]] ![[D]] [[E^blk]] [[F#H|al]]"
    assert find_wikilinks(text) == {"A", "B", "C", "D", "E", "F"}


def test_links_in_code_blocks_ignored():
    text = "[[Real]]\n```sql\nSELECT [[Fake]]\n```\nand `[[Fake2]]` end\n"
    assert find_wikilinks(text) == {"Real"}


def test_scan_skips_templates_and_obsidian(vault):
    idx = scan_vault(vault)
    assert "concept" not in idx.notes and "templates" not in {Path(p).parent.name.lower() for p in idx.notes.values()}
    assert set(idx.display.values()) == {"00 Home", "Day 1", "Virtual Warehouse", "Caching", "Lonely", "Diagram"}
    assert idx.tags["lonely"] == {"concept", "day2"}


def test_case_insensitive_resolution(vault):
    idx = scan_vault(vault)
    assert dangling(idx) == []


def test_dangling_reported_with_source(vault):
    write(vault, "Concepts/Caching.md", "---\ntags: [concept, day1]\n---\n[[Virtual Warehouse]] [[Missing Note]]\n")
    assert dangling(scan_vault(vault)) == [("Caching", "Missing Note")]


def test_orphans_only_in_concept_folders_and_scoped_by_day(vault):
    idx = scan_vault(vault)
    assert orphans(idx) == ["Lonely"]
    assert orphans(idx, day=1) == []
    assert orphans(idx, day=2) == ["Lonely"]
    # Home has no inbound links but is not in a concept folder
    assert "00 Home" not in orphans(idx)


def test_duplicate_stems_reported(vault):
    write(vault, "Conventions/Caching.md", "---\ntags: [convention]\n---\n[[Virtual Warehouse]]\n")
    assert main(["--vault", str(vault)]) == 1


def test_unresolved_quiz_concepts(vault):
    idx = scan_vault(vault)
    assert unresolved_quiz_concepts({"Caching", "Ghost", "virtual warehouse"}, idx) == ["Ghost"]


def test_main_returns_1_on_problem_and_0_when_clean(vault, tmp_path, capsys):
    bank = tmp_path / "bank"
    bank.mkdir()
    (bank / "day1.yaml").write_text(
        "- {id: d1-a-001, type: tf, concept: Caching, tags: [day1], difficulty: 1, prompt: p, answer: true, explanation: e}\n")
    assert main(["--vault", str(vault), "--bank-dir", str(bank)]) == 1
    assert "ORPHAN Lonely" in capsys.readouterr().out
    assert main(["--vault", str(vault), "--bank-dir", str(bank), "--day", "1"]) == 0
    assert capsys.readouterr().out.startswith("OK:")
    (bank / "day1.yaml").write_text(
        "- {id: d1-a-001, type: tf, concept: Ghost, tags: [day1], difficulty: 1, prompt: p, answer: true, explanation: e}\n")
    assert main(["--vault", str(vault), "--bank-dir", str(bank), "--day", "1"]) == 1
    assert "QUIZ Ghost" in capsys.readouterr().out
