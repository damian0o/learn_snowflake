"""Leitner box scheduling: three boxes, up on correct, back to 1 on wrong."""
import random
from dataclasses import dataclass, replace
from typing import Dict, List, Optional

MAX_BOX = 3


@dataclass
class Card:
    box: int = 1
    asked: int = 0
    correct: int = 0
    last_asked: Optional[str] = None
    last_result: Optional[bool] = None


def update(card: Card, correct: bool, now: str) -> Card:
    return replace(
        card,
        box=min(card.box + 1, MAX_BOX) if correct else 1,
        asked=card.asked + 1,
        correct=card.correct + (1 if correct else 0),
        last_asked=now,
        last_result=correct,
    )


def select_review(progress: Dict[str, Card], all_ids: List[str], rng: random.Random,
                  box3_sample: int = 5) -> List[str]:
    boxes: Dict[int, List[str]] = {1: [], 2: [], 3: []}
    for qid in all_ids:
        card = progress.get(qid)
        boxes[card.box if card else 1].append(qid)
    rng.shuffle(boxes[1])
    rng.shuffle(boxes[2])
    sample = rng.sample(boxes[3], min(box3_sample, len(boxes[3])))
    return boxes[1] + boxes[2] + sample
