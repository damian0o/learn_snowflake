import random

import pytest

from quizlib.bank import Question
from quizlib.matching import Presented, check_answer, normalize_fill, parse_letters, present


def q(type_, options=None, answer=None):
    return Question(id="d1-x-001", type=type_, concept="C", tags=["day1"], difficulty=1,
                    prompt="p", options=options or [], answer=answer, explanation="e")


@pytest.fixture
def mcq():
    return q("mcq", ["Cloud Services", "Query Processing", "Database Storage", "Snowsight"], "Query Processing")


@pytest.fixture
def multi():
    return q("multi", ["A", "B", "C", "D"], ["A", "C"])


@pytest.fixture
def tf():
    return q("tf", answer=True)


@pytest.fixture
def fill():
    return q("fill", answer=["Query Processing", "compute layer"])


def test_present_shuffles_deterministically_with_seed(mcq):
    a = present(mcq, random.Random(7)).options
    b = present(mcq, random.Random(7)).options
    assert a == b
    assert sorted(a) == sorted(mcq.options)
    orders = {tuple(present(mcq, random.Random(s)).options) for s in range(20)}
    assert len(orders) > 1
    assert mcq.options[0] == "Cloud Services"  # original untouched


def test_mcq_correct_letter_follows_shuffle(mcq):
    p = present(mcq, random.Random(3))
    assert p.options[ord(p.correct_letters()) - ord("a")] == "Query Processing"
    assert check_answer(p, p.correct_letters()) is True
    assert check_answer(p, p.correct_letters().upper()) is True


def test_mcq_wrong_letter_false_and_out_of_range_none(mcq):
    p = present(mcq, random.Random(3))
    wrong = next(l for l in "abcd" if l != p.correct_letters())
    assert check_answer(p, wrong) is False
    assert check_answer(p, "z") is None
    assert check_answer(p, "") is None
    assert check_answer(p, "ab") is None


def test_multi_requires_exact_set(multi):
    p = present(multi, random.Random(1))
    good = p.correct_letters()
    assert len(good) == 2
    assert check_answer(p, good) is True
    assert check_answer(p, ",".join(good)) is True
    assert check_answer(p, " ".join(good).upper()) is True
    assert check_answer(p, good[0]) is False
    assert check_answer(p, "abcd") is False
    assert check_answer(p, "a9") is None


def test_tf_accepts_variants(tf):
    p = present(tf, random.Random(1))
    assert p.options == [] and p.correct_letters() == ""
    for s in ["t", "T", "true", "yes", "y"]:
        assert check_answer(p, s) is True
    for s in ["f", "false", "no", "N"]:
        assert check_answer(p, s) is False
    assert check_answer(p, "maybe") is None
    assert check_answer(p, "") is None


def test_fill_normalizes(fill):
    p = present(fill, random.Random(1))
    for s in ["query processing", "  Query   Processing. ", "`compute layer`", '"Compute Layer"', "compute layer;"]:
        assert check_answer(p, s) is True, s
    assert check_answer(p, "storage") is False


def test_fill_empty_is_none(fill):
    p = present(fill, random.Random(1))
    assert check_answer(p, "   ") is None


def test_normalize_fill_and_parse_letters():
    assert normalize_fill("  'Hello   World'. ") == "hello world"
    assert parse_letters("a, C") == {"a", "c"}
    assert parse_letters("ac") == {"a", "c"}
    assert parse_letters("a1") is None
    assert parse_letters("") is None
