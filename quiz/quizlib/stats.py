"""Aggregating progress into per-concept and per-day statistics."""
from dataclasses import dataclass
from typing import Dict, List

from .bank import Question
from .leitner import MAX_BOX, Card


@dataclass
class ConceptStat:
    name: str
    asked: int = 0
    correct: int = 0

    @property
    def accuracy(self) -> float:
        return self.correct / self.asked if self.asked else 0.0


def _aggregate(progress: Dict[str, Card], questions: List[Question], key) -> List[ConceptStat]:
    stats: Dict[str, ConceptStat] = {}
    for q in questions:
        name = key(q)
        stat = stats.setdefault(name, ConceptStat(name))
        card = progress.get(q.id)
        if card:
            stat.asked += card.asked
            stat.correct += card.correct
    return [stats[k] for k in sorted(stats)]


def per_concept(progress: Dict[str, Card], questions: List[Question]) -> List[ConceptStat]:
    return _aggregate(progress, questions, lambda q: q.concept)


def per_day(progress: Dict[str, Card], questions: List[Question]) -> List[ConceptStat]:
    return _aggregate(progress, questions, lambda q: q.source)


def weakest(stats: List[ConceptStat], n: int = 5) -> List[ConceptStat]:
    asked = [s for s in stats if s.asked > 0]
    return sorted(asked, key=lambda s: (s.accuracy, s.name))[:n]


def box_distribution(progress: Dict[str, Card], all_ids: List[str]) -> Dict[int, int]:
    dist = {b: 0 for b in range(1, MAX_BOX + 1)}
    for qid in all_ids:
        card = progress.get(qid)
        dist[card.box if card else 1] += 1
    return dist
