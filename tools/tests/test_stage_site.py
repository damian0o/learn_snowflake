import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import stage_site  # noqa: E402


def make_vault(tmp_path):
    v = tmp_path / "vault"
    (v / "Concepts").mkdir(parents=True)
    (v / "Templates").mkdir()
    (v / ".obsidian").mkdir()
    (v / "00 Home.md").write_text("---\ntags: [home]\n---\n# Learn Snowflake\n\nHello [[Caching]].\n")
    (v / "Concepts" / "Caching.md").write_text("---\ntags: [concept]\n---\n# Caching\n\nBody.\n")
    (v / "Concepts" / "No Front.md").write_text("# No Front\n\nBody.\n")
    (v / "Concepts" / "Fancy.md").write_text('---\ntags: [x]\n---\n# Day 1 - The "big" picture\n\nBody.\n')
    (v / "Templates" / "Concept.md").write_text("# <Concept name>\n")
    (v / ".obsidian" / "app.json").write_text("{}")
    return v


def test_copies_notes_preserving_folders_and_skips_templates_and_obsidian(tmp_path):
    v = make_vault(tmp_path)
    out = tmp_path / "content"
    stage_site.stage(v, out)
    assert (out / "Concepts" / "Caching.md").exists()
    assert (out / "index.md").exists()
    assert not (out / "Templates").exists()
    assert not (out / ".obsidian").exists()


def test_home_note_becomes_index_and_links_to_it_are_rewritten(tmp_path):
    v = make_vault(tmp_path)
    (v / "Concepts" / "Caching.md").write_text("# Caching\n\nBack to [[00 Home]]. Also [[00 Home|the start]].\n")
    out = tmp_path / "content"
    stage_site.stage(v, out)
    assert not (out / "00 Home.md").exists()
    index = (out / "index.md").read_text()
    assert index.startswith('---\ntags: [home]\ntitle: "Learn Snowflake"\n---\n')
    assert "Hello [[Caching]]." in index
    caching = (out / "Concepts" / "Caching.md").read_text()
    assert "Back to [[index|Home]]. Also [[index|the start]]." in caching


def test_clears_stale_files_in_out_dir(tmp_path):
    v = make_vault(tmp_path)
    out = tmp_path / "content"
    out.mkdir()
    (out / "stale.md").write_text("old")
    stage_site.stage(v, out)
    assert not (out / "stale.md").exists()


def test_leading_h1_moves_into_frontmatter_title(tmp_path):
    v = make_vault(tmp_path)
    out = tmp_path / "content"
    stage_site.stage(v, out)
    assert (out / "Concepts" / "Caching.md").read_text() == "---\ntags: [concept]\ntitle: \"Caching\"\n---\n\nBody.\n"
    assert (out / "Concepts" / "No Front.md").read_text() == "---\ntitle: \"No Front\"\n---\n\nBody.\n"
    assert (out / "Concepts" / "Fancy.md").read_text().startswith('---\ntags: [x]\ntitle: "Day 1 - The \\"big\\" picture"\n---\n')


def test_returns_count_of_notes_and_main_reports_it(tmp_path, capsys):
    v = make_vault(tmp_path)
    out = tmp_path / "content"
    assert stage_site.stage(v, out) == 4
    assert stage_site.main([str(v), str(out)]) == 0
    assert "4 notes" in capsys.readouterr().out
