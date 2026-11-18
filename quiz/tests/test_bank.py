import pytest

from quizlib.bank import available_banks, load_bank, load_named


def test_load_named_reads_all_fields(tmp_bank):
    qs = load_named(tmp_bank, "day1")
    assert [q.id for q in qs] == ["d1-arch-001", "d1-arch-002", "d1-arch-003", "d1-arch-004"]
    assert qs[0].type == "mcq"
    assert qs[0].options == ["Cloud Services", "Query Processing", "Database Storage"]
    assert qs[0].answer == "Query Processing"
    assert qs[0].concept == "Three-Layer Architecture"
    assert qs[0].tags == ["day1", "architecture"]
    assert qs[0].difficulty == 1
    assert qs[0].explanation.startswith("Virtual warehouses")
    assert qs[0].source == "day1"


def test_tf_and_fill_have_empty_options(tmp_bank):
    qs = load_named(tmp_bank, "day1")
    assert qs[2].type == "tf" and qs[2].options == [] and qs[2].answer is True
    assert qs[3].type == "fill" and qs[3].options == [] and qs[3].answer == ["Query Processing", "compute layer"]


def test_load_named_missing_raises(tmp_bank):
    with pytest.raises(FileNotFoundError, match="No bank named 'day9'"):
        load_named(tmp_bank, "day9")


def test_available_banks_sorted(tmp_bank):
    (tmp_bank / "cumulative.yaml").write_text("[]")
    assert available_banks(tmp_bank) == ["cumulative", "day1"]


def test_load_bank_concatenates_and_rejects_non_list(tmp_bank):
    (tmp_bank / "x.yaml").write_text("a: 1")
    with pytest.raises(ValueError, match="bank must be a list"):
        load_bank([tmp_bank / "x.yaml"])
    (tmp_bank / "y.yaml").write_text("[]")
    assert len(load_bank([tmp_bank / "day1.yaml", tmp_bank / "y.yaml"])) == 4


def test_scalar_tags_and_options_are_kept_as_is_not_split(tmp_bank):
    (tmp_bank / "bad.yaml").write_text(
        "- {id: d1-a-001, type: mcq, concept: C, tags: day1, difficulty: 1, prompt: p, options: 'a, b, c', answer: a, explanation: e}\n")
    q = load_named(tmp_bank, "bad")[0]
    assert q.tags == "day1"
    assert q.options == "a, b, c"
