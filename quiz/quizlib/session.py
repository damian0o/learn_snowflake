"""One interactive quiz session: ask, judge, explain, update progress."""
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List

from .bank import Question
from .leitner import Card, update
from .matching import LETTERS, Presented, check_answer, present
from .progress import now_iso

_HINTS = {
    "mcq": "one letter, e.g. b",
    "multi": "the letters of every correct option, e.g. ac",
    "tf": "t or f",
    "fill": "a short answer",
}


@dataclass
class SessionResult:
    asked: int = 0
    correct: int = 0
    missed_ids: List[str] = field(default_factory=list)
    aborted: bool = False


def format_question(index: int, total: int, p: Presented) -> str:
    q = p.question
    lines = ["Q%d/%d  [%s]" % (index, total, q.concept), q.prompt]
    if q.type in ("mcq", "multi"):
        lines.extend("  %s) %s" % (LETTERS[i], opt) for i, opt in enumerate(p.options))
        if q.type == "multi":
            lines.append("(choose all that apply, e.g. ac)")
    elif q.type == "tf":
        lines.append("(t/f)")
    else:
        lines.append("(type your answer)")
    return "\n".join(lines) + "\n"


def _correct_text(p: Presented) -> str:
    q = p.question
    if q.type == "tf":
        return "true" if q.answer else "false"
    if q.type == "fill":
        return str(q.answer[0])
    return p.correct_letters()


def read_path(concept: str, vault_dir: Path) -> str:
    for folder in ("Concepts", "Conventions"):
        if (Path(vault_dir) / folder / ("%s.md" % concept)).is_file():
            return "vault/%s/%s.md" % (folder, concept)
    return "vault/Concepts/%s.md" % concept


def run_session(questions: List[Question], progress: Dict[str, Card], ask: Callable[[str], str],
                out: Callable[[str], None], rng: random.Random, vault_dir: Path,
                now: Callable[[], str] = now_iso) -> SessionResult:
    res = SessionResult()
    total = len(questions)
    for i, q in enumerate(questions, start=1):
        p = present(q, rng)
        out(format_question(i, total, p))
        try:
            while True:
                verdict = check_answer(p, ask("> "))
                if verdict is not None:
                    break
                out("Not understood. Answer with %s." % _HINTS[q.type])
        except (EOFError, KeyboardInterrupt):
            res.aborted = True
            out("\nStopped. Progress for answered questions is kept.")
            break
        res.asked += 1
        progress[q.id] = update(progress.get(q.id, Card()), verdict, now())
        if verdict:
            res.correct += 1
            out("Correct.")
        else:
            res.missed_ids.append(q.id)
            out("Wrong. Correct answer: %s" % _correct_text(p))
        out(q.explanation)
        out("Read: %s\n" % read_path(q.concept, vault_dir))
    if res.asked:
        pct = round(100.0 * res.correct / res.asked)
        out("Score: %d/%d (%d%%)" % (res.correct, res.asked, pct))
    if res.missed_ids:
        by_id = {q.id: q for q in questions}
        missed = sorted({by_id[m].concept for m in res.missed_ids})
        out("Missed concepts: %s" % ", ".join(missed))
    return res
