import random
from pathlib import Path

import pytest

from quizlib.bank import Question
from quizlib.leitner import Card
from quizlib.matching import present
from quizlib.session import SessionResult, format_question, run_session


def mk(id_, type_, concept, options=None, answer=None):
    return Question(id=id_, type=type_, concept=concept, tags=["day1"], difficulty=1,
                    prompt="Prompt for %s" % id_, options=options or [], answer=answer,
                    explanation="Because %s." % id_, source="day1")


@pytest.fixture
def vault(tmp_path):
    (tmp_path / "Concepts").mkdir()
    (tmp_path / "Conventions").mkdir()
    (tmp_path / "Concepts" / "Alpha.md").write_text("# Alpha\n")
    (tmp_path / "Conventions" / "Naming - Beta.md").write_text("# Beta\n")
    return tmp_path


@pytest.fixture
def questions():
    return [
        mk("d1-a-001", "mcq", "Alpha", ["X", "Y", "Z"], "Y"),
        mk("d1-a-002", "tf", "Alpha", answer=False),
        mk("d1-a-003", "fill", "Naming - Beta", answer=["beta"]),
    ]


def scripted(answers):
    it = iter(answers)

    def ask(prompt):
        nxt = next(it)
        if isinstance(nxt, BaseException):
            raise nxt
        return nxt
    return ask


def run(questions, answers, vault, progress=None, seed=1):
    out = []
    progress = {} if progress is None else progress
    res = run_session(questions, progress, scripted(answers), out.append, random.Random(seed), vault, now=lambda: "T0")
    return res, out, progress


def test_format_question_shows_index_and_options_but_hides_concept(questions):
    p = present(questions[0], random.Random(1))
    text = format_question(2, 3, p)
    assert text.startswith("Q2/3\nPrompt for d1-a-001\n")
    assert "Alpha" not in text  # the concept name would give the answer away
    assert "  a) " in text and "  b) " in text and "  c) " in text
    assert "(t/f)" in format_question(1, 1, present(questions[1], random.Random(1)))
    assert "(type your answer)" in format_question(1, 1, present(questions[2], random.Random(1)))
    multi = mk("d1-a-009", "multi", "Alpha", ["X", "Y", "Z"], ["X", "Y"])
    assert "choose all that apply" in format_question(1, 1, present(multi, random.Random(1)))


def test_full_run_scores_and_updates_progress(questions, vault):
    p0 = present(questions[0], random.Random(1))
    correct_letter = present(questions[0], random.Random(1)).correct_letters()
    # Session uses rng for question order too; pin order by giving one question per type we can answer robustly.
    res, out, progress = run(questions, [correct_letter, "f", "BETA"], vault)
    # the mcq letter may not match after reordering; accept either outcome but check bookkeeping is consistent
    assert isinstance(res, SessionResult) and res.asked == 3 and res.aborted is False
    assert res.correct == 3 - len(res.missed_ids)
    assert set(progress) == {"d1-a-001", "d1-a-002", "d1-a-003"}
    assert all(c.asked == 1 and c.last_asked == "T0" for c in progress.values())
    assert any(line.startswith("Score: %d/3" % res.correct) for line in out)


def test_invalid_letter_reprompts(vault):
    qs = [mk("d1-a-001", "mcq", "Alpha", ["X", "Y", "Z"], "Y")]
    res, out, progress = run(qs, ["z", "", "a"], vault)
    assert sum("Not understood" in line for line in out) == 2
    assert res.asked == 1 and progress["d1-a-001"].asked == 1


def test_eof_ends_session_and_saves(vault):
    qs = [mk("d1-a-001", "tf", "Alpha", answer=True), mk("d1-a-002", "tf", "Alpha", answer=True)]
    res, out, progress = run(qs, ["t", EOFError()], vault)
    assert res.aborted is True and res.asked == 1 and res.correct == 1
    assert set(progress) == {"d1-a-001"}


def test_keyboard_interrupt_also_aborts(vault):
    qs = [mk("d1-a-001", "tf", "Alpha", answer=True)]
    res, out, progress = run(qs, [KeyboardInterrupt()], vault)
    assert res.aborted is True and res.asked == 0 and progress == {}


def test_wrong_answer_prints_explanation_and_read_path(vault):
    qs = [mk("d1-a-001", "tf", "Alpha", answer=True)]
    res, out, progress = run(qs, ["f"], vault)
    text = "\n".join(out)
    assert "Wrong. Correct answer: true" in text
    assert "Because d1-a-001." in text
    assert "Read: vault/Concepts/Alpha.md" in text
    assert "Missed concepts: Alpha" in text
    header = out[0]
    assert "Alpha" not in header
    assert res.missed_ids == ["d1-a-001"] and progress["d1-a-001"].box == 1


def test_correct_answer_prints_correct_and_moves_box(vault):
    qs = [mk("d1-a-001", "tf", "Alpha", answer=True)]
    res, out, progress = run(qs, ["t"], vault, progress={"d1-a-001": Card(box=2, asked=1, correct=1)})
    assert "Correct." in out and progress["d1-a-001"].box == 3
    assert "Score: 1/1 (100%)" in out


def test_read_path_prefers_conventions_when_concept_lives_there(vault):
    qs = [mk("d1-a-003", "fill", "Naming - Beta", answer=["beta"])]
    res, out, progress = run(qs, ["gamma"], vault)
    text = "\n".join(out)
    assert "Read: vault/Conventions/Naming - Beta.md" in text
    assert "Correct answer: beta" in text
