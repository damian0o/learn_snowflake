import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_pitch  # noqa: E402

FM = "---\ntags: [concept, day1, compute]\ndocs: https://x\n---\n"


def note(body, fm=FM):
    return fm + body


def test_strip_frontmatter_returns_tags_and_body_for_inline_and_block_lists():
    tags, body = check_pitch.strip_frontmatter(FM + "# T\n\nx")
    assert tags == ["concept", "day1", "compute"] and body == "# T\n\nx"
    tags2, _ = check_pitch.strip_frontmatter("---\ntags:\n  - concept\n  - day2\n---\nbody")
    assert tags2 == ["concept", "day2"]


def test_prose_words_excludes_fences_tables_headings_and_explain_section():
    body = ("# Title\n\none two three\n\n```mermaid\nA --> B\n|--x\n```\n\n"
            "| a | b |\n|---|---|\n| c | d |\n\n~~~\nfour five\n~~~\n\n- six seven\n\n"
            "## Explain it to a teammate (fill in yourself)\n\n> eight nine ten\n")
    assert check_pitch.prose_words(body) == 5   # one two three six seven


def test_prose_words_counts_wikilink_words_and_callouts():
    assert check_pitch.prose_words("> [!warning] Not yet\n> alpha [[Query Pruning]]\n") == 6


def test_missing_headings_reports_only_absent_ones():
    body = "## Numbers\n## How it works\n## Probe\n## Related\n"
    assert check_pitch.missing_headings(body, check_pitch.REQUIRED["Concepts"]) == ["## Cost", "## Traps"]


def test_banned_hits_is_case_insensitive_and_reports_phrase():
    assert check_pitch.banned_hits("Our Elastic compute is Seamless.") == ["elastic", "seamless"]
    assert check_pitch.banned_hits("nothing here") == []


def test_check_note_flags_budget_headings_and_banned(tmp_path):
    v = tmp_path / "vault"
    (v / "Concepts").mkdir(parents=True)
    p = v / "Concepts" / "X.md"
    p.write_text(note("# X\n\n" + ("word " * 301) + "\n\nseamless\n\n## Related\n"))
    issues = check_pitch.check_note(p, v)
    assert any(i.startswith("prose 3") and "> 300" in i for i in issues)
    assert "missing heading ## Numbers" in issues
    assert "banned phrase 'seamless'" in issues


def test_check_note_uses_syllabus_budget_and_no_heading_rule(tmp_path):
    v = tmp_path / "vault"
    (v / "Syllabus").mkdir(parents=True)
    p = v / "Syllabus" / "Day 9.md"
    p.write_text("---\ntags: [syllabus, day9]\n---\n# D\n\n" + ("w " * 850))
    assert check_pitch.check_note(p, v) == []


def test_check_note_requires_rule_line_in_conventions(tmp_path):
    v = tmp_path / "vault"
    (v / "Conventions").mkdir(parents=True)
    p = v / "Conventions" / "Naming - Tables.md"
    p.write_text("---\ntags: [convention, day3]\n---\n# N\n\n## Examples\n## Why\n## Probe\n## Related\n")
    assert check_pitch.check_note(p, v) == ["missing **Rule:** line"]


def test_main_scopes_by_day_and_accepts_explicit_paths(tmp_path, capsys):
    v = tmp_path / "vault"
    (v / "Concepts").mkdir(parents=True)
    good = v / "Concepts" / "Good.md"
    good.write_text(note("# G\n\nfine\n\n## Numbers\n## How it works\n## Probe\n## Cost\n## Traps\n## Related\n"))
    bad = v / "Concepts" / "Bad.md"
    bad.write_text(note("# B\n\nelastic\n", fm="---\ntags: [concept, day2]\n---\n"))
    assert check_pitch.main(["--vault", str(v), "--day", "1"]) == 0
    assert "OK: 1 notes checked" in capsys.readouterr().out
    assert check_pitch.main(["--vault", str(v)]) == 1
    assert "PITCH Concepts/Bad.md: banned phrase 'elastic'" in capsys.readouterr().out
    assert check_pitch.main(["--vault", str(v), str(good)]) == 0
