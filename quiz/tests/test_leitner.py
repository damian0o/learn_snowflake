import random

from quizlib.leitner import MAX_BOX, Card, select_review, update


def test_new_card_defaults():
    c = Card()
    assert (c.box, c.asked, c.correct, c.last_asked, c.last_result) == (1, 0, 0, None, None)
    assert MAX_BOX == 3


def test_correct_moves_up_and_caps_at_3():
    c = Card()
    c = update(c, True, "t1")
    assert (c.box, c.asked, c.correct, c.last_asked, c.last_result) == (2, 1, 1, "t1", True)
    c = update(c, True, "t2")
    assert c.box == 3
    c = update(c, True, "t3")
    assert c.box == 3 and c.asked == 3 and c.correct == 3


def test_wrong_resets_to_1_from_any_box():
    c = Card(box=3, asked=5, correct=5)
    c = update(c, False, "t9")
    assert (c.box, c.asked, c.correct, c.last_result) == (1, 6, 5, False)


def test_update_is_pure():
    c = Card()
    update(c, True, "t1")
    assert c.box == 1 and c.asked == 0


def test_select_review_order_and_unseen_as_box1():
    progress = {"a": Card(box=2), "b": Card(box=3), "c": Card(box=1), "d": Card(box=3)}
    ids = ["a", "b", "c", "d", "e"]  # e unseen -> box 1
    order = select_review(progress, ids, random.Random(0))
    assert set(order[:2]) == {"c", "e"}
    assert order[2] == "a"
    assert set(order[3:]) == {"b", "d"}


def test_box3_sample_size_respected():
    progress = {str(i): Card(box=3) for i in range(10)}
    order = select_review(progress, list(progress), random.Random(0), box3_sample=4)
    assert len(order) == 4 and len(set(order)) == 4
