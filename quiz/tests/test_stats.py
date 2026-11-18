from quizlib.bank import Question
from quizlib.leitner import Card
from quizlib.stats import ConceptStat, box_distribution, per_concept, per_day, weakest


def mk(id_, concept, source="day1"):
    return Question(id=id_, type="tf", concept=concept, tags=["x"], difficulty=1, prompt="p",
                    options=[], answer=True, explanation="e", source=source)


QS = [mk("d1-a-001", "Alpha"), mk("d1-a-002", "Alpha"), mk("d1-b-001", "Beta"), mk("d2-c-001", "Gamma", "day2")]
PROG = {"d1-a-001": Card(box=2, asked=2, correct=1), "d1-a-002": Card(box=1, asked=1, correct=0),
        "d2-c-001": Card(box=3, asked=4, correct=4)}


def test_per_concept_aggregates():
    stats = per_concept(PROG, QS)
    assert [s.name for s in stats] == ["Alpha", "Beta", "Gamma"]
    alpha = stats[0]
    assert (alpha.asked, alpha.correct) == (3, 1) and abs(alpha.accuracy - 1 / 3) < 1e-9
    assert stats[1].asked == 0 and stats[1].accuracy == 0.0


def test_weakest_excludes_unasked_and_sorts():
    w = weakest(per_concept(PROG, QS), n=5)
    assert [s.name for s in w] == ["Alpha", "Gamma"]
    assert [s.name for s in weakest(per_concept(PROG, QS), n=1)] == ["Alpha"]


def test_box_distribution_counts_unseen_as_box1():
    assert box_distribution(PROG, [q.id for q in QS]) == {1: 2, 2: 1, 3: 1}


def test_per_day_groups_by_source():
    days = per_day(PROG, QS)
    assert [(d.name, d.asked, d.correct) for d in days] == [("day1", 3, 1), ("day2", 4, 4)]
