"""Presenting a question (shuffled options) and judging a typed answer."""
import random
import re
from dataclasses import dataclass, field
from typing import List, Optional, Set

from .bank import Question

LETTERS = "abcdefgh"
_TRUE = {"t", "true", "y", "yes"}
_FALSE = {"f", "false", "n", "no"}


@dataclass
class Presented:
    question: Question
    options: List[str] = field(default_factory=list)

    def correct_letters(self) -> str:
        q = self.question
        if q.type == "mcq":
            return LETTERS[self.options.index(q.answer)]
        if q.type == "multi":
            return "".join(sorted(LETTERS[self.options.index(a)] for a in q.answer))
        return ""


def present(q: Question, rng: random.Random) -> Presented:
    options = list(q.options)
    if q.type in ("mcq", "multi"):
        rng.shuffle(options)
    else:
        options = []
    return Presented(question=q, options=options)


def normalize_fill(s: str) -> str:
    s = s.strip().lower()
    s = s.strip("`'\"")
    s = re.sub(r"[.,;:!]+$", "", s)
    s = s.strip().strip("`'\"")
    return re.sub(r"\s+", " ", s).strip()


def parse_letters(given: str) -> Optional[Set[str]]:
    cleaned = re.sub(r"[\s,]+", "", given.lower())
    if not cleaned or any(ch not in LETTERS for ch in cleaned):
        return None
    return set(cleaned)


def check_answer(p: Presented, given: str) -> Optional[bool]:
    q = p.question
    if q.type == "tf":
        s = given.strip().lower()
        if s in _TRUE:
            return bool(q.answer) is True
        if s in _FALSE:
            return bool(q.answer) is False
        return None
    if q.type == "fill":
        s = normalize_fill(given)
        if not s:
            return None
        return s in {normalize_fill(a) for a in q.answer}
    letters = parse_letters(given)
    if letters is None:
        return None
    valid = set(LETTERS[: len(p.options)])
    if not letters <= valid:
        return None
    if q.type == "mcq":
        if len(letters) != 1:
            return None
        return letters == set(p.correct_letters())
    return letters == set(p.correct_letters())
