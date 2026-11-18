from pathlib import Path

import pytest

from quizlib.bank import Question, load_named
from quizlib.lint import ID_RE, TYPES, concept_notes, lint_bank


def mk(**kw):
    base = dict(id="d1-arch-001", type="mcq", concept="Three-Layer Architecture", tags=["day1"], difficulty=1,
                prompt="p?", options=["A", "B", "C"], answer="A", explanation="because", source="day1")
    base.update(kw)
    return Question(**base)


NOTES = {"Three-Layer Architecture": {"concept", "day1"}, "Cloud Services Layer": {"concept", "day1"},
         "Micro-partitions": {"concept", "day1"}, "Query Processing Layer": {"concept", "day1"},
         "Naming - Warehouses": {"convention", "day2"}}


def test_clean_bank_has_no_errors(tmp_bank):
    qs = load_named(tmp_bank, "day1")
    assert lint_bank(qs, NOTES, day=1) == []


def test_duplicate_id_reported():
    errs = lint_bank([mk(), mk(concept="Cloud Services Layer")], NOTES, day=None)
    assert any(e.startswith("d1-arch-001: duplicate id") for e in errs)


def test_bad_id_and_type_and_difficulty():
    errs = lint_bank([mk(id="bad", type="essay", difficulty=7)], {}, day=None)
    joined = "\n".join(errs)
    assert "bad: id does not match" in joined and "type 'essay'" in joined and "difficulty" in joined
    assert ID_RE.match("cum-mix-001") and not ID_RE.match("d4-x-001") and TYPES == ("mcq", "multi", "tf", "fill")


def test_mcq_answer_not_in_options():
    errs = lint_bank([mk(answer="Z")], NOTES, day=None)
    assert any("answer 'Z' is not one of the options" in e for e in errs)


def test_lint_rejects_non_string_options_and_answers():
    errs = lint_bank([
        mk(id="d1-a-001", options=["A", True, "C"], answer="A"),
        mk(id="d1-a-002", type="fill", options=[], answer=[False, "x"], concept="Cloud Services Layer"),
        mk(id="d1-a-003", answer=1, concept="Micro-partitions"),
        mk(id="d1-a-004", type="tf", options=[], answer="true", concept="Query Processing Layer"),
    ], NOTES, day=None)
    joined = "\n".join(errs)
    assert "d1-a-001: option" in joined and "not a string" in joined
    assert "d1-a-002: fill answer" in joined
    assert "d1-a-003: answer" in joined and "not a string" in joined
    assert "d1-a-004: tf answer must be true or false" in joined


def test_multi_rules():
    errs = lint_bank([mk(type="multi", options=["A", "B", "C"], answer=["A"]),
                      mk(id="d1-arch-002", type="multi", options=["A", "B", "C"], answer=["A", "Q"], concept="Micro-partitions")],
                     NOTES, day=None)
    joined = "\n".join(errs)
    assert "at least 2" in joined and "'Q' is not one of the options" in joined


def test_unknown_concept():
    errs = lint_bank([mk(concept="Nope")], NOTES, day=None)
    assert any("concept 'Nope' has no note" in e for e in errs)


def test_coverage_scoped_by_day():
    qs = [mk(concept=c) for c in ["Three-Layer Architecture", "Cloud Services Layer", "Micro-partitions", "Query Processing Layer"]]
    for i, q in enumerate(qs):
        q.id = "d1-arch-%03d" % (i + 1)
    assert lint_bank(qs, NOTES, day=1) == []
    errs = lint_bank(qs, NOTES, day=None)
    assert errs == ["coverage: note 'Naming - Warehouses' has no question"]


def test_concept_notes_reads_frontmatter_tags(tmp_path):
    (tmp_path / "Concepts").mkdir()
    (tmp_path / "Conventions" / "sub").mkdir(parents=True)
    (tmp_path / "Concepts" / "A.md").write_text("---\ntags: [concept, day1]\n---\n# A\n")
    (tmp_path / "Conventions" / "sub" / "Naming - B.md").write_text("---\ntags: convention\ndocs: x\n---\n# B\n")
    (tmp_path / "Concepts" / "C.md").write_text("# C\nno frontmatter\n")
    (tmp_path / "Other.md").write_text("---\ntags: [concept]\n---\n")
    assert concept_notes(tmp_path) == {"A": {"concept", "day1"}, "Naming - B": {"convention"}, "C": set()}


def test_scalar_tags_and_options_rejected():
    errs = lint_bank([mk(tags="day1"), mk(id="d1-arch-002", options="A, B, C", concept="Cloud Services Layer")], NOTES, day=None)
    joined = "\n".join(errs)
    assert "d1-arch-001: tags must be a list" in joined
    assert "d1-arch-002: options must be a list" in joined
    assert "option 1 is not a string" not in joined  # no per-character noise
