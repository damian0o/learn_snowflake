"""Command-line interface: quiz.py <bank>|review|stats|lint [options]."""
import argparse
import random
import sys
from pathlib import Path
from typing import List, Optional

from .bank import Question, available_banks, load_bank, load_named
from .leitner import select_review
from .lint import concept_notes, lint_bank
from .progress import load_progress, save_progress
from .session import read_path, run_session
from .stats import box_distribution, per_concept, per_day, weakest

REPO = Path(__file__).resolve().parents[2]
SPECIAL = ("review", "stats", "lint")


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="quiz.py", description="Snowflake learning quiz runner.")
    p.add_argument("command", help="a bank name (e.g. day1), or review | stats | lint")
    p.add_argument("--n", type=int, default=None, help="ask at most N questions")
    p.add_argument("--tag", default=None, help="only questions carrying this tag")
    p.add_argument("--seed", type=int, default=None, help="seed for question and option order")
    p.add_argument("--day", type=int, default=None, help="lint: restrict to day N")
    p.add_argument("--vault", type=Path, default=REPO / "vault")
    p.add_argument("--bank-dir", type=Path, default=REPO / "quiz" / "bank")
    p.add_argument("--progress", type=Path, default=REPO / "quiz" / "results" / "progress.json")
    return p


def _filter(questions: List[Question], tag: Optional[str]) -> List[Question]:
    return [q for q in questions if tag is None or tag in q.tags]


def _ask_session(questions: List[Question], args, rng, stdin, stdout, out, err) -> int:
    questions = _filter(questions, args.tag)
    if not questions:
        out("No questions match.")
        return 0
    if args.n is not None:
        questions = questions[: args.n]
    progress = load_progress(args.progress, warn=err)

    def ask(prompt: str) -> str:
        stdout.write(prompt)
        stdout.flush()
        line = stdin.readline()
        if line == "":
            raise EOFError
        return line.rstrip("\n")

    run_session(questions, progress, ask, out, rng, args.vault)
    save_progress(args.progress, progress)
    return 0


def _cmd_stats(args, out) -> int:
    questions = load_bank([args.bank_dir / ("%s.yaml" % b) for b in available_banks(args.bank_dir)])
    progress = load_progress(args.progress)
    if not progress:
        out("No progress yet. Run a quiz first, e.g. python3 quiz/quiz.py day1")
        return 0
    out("Accuracy per day")
    for d in per_day(progress, questions):
        out("  %-12s %3d asked  %3d correct  %3d%%" % (d.name, d.asked, d.correct, round(100 * d.accuracy)))
    out("\nWeakest concepts (reread these)")
    for s in weakest(per_concept(progress, questions), n=5):
        out("  %3d%%  %s   Read: %s" % (round(100 * s.accuracy), s.name, read_path(s.name, args.vault)))
    dist = box_distribution(progress, [q.id for q in questions])
    out("\nLeitner boxes (1 = needs work, 3 = known)")
    for box in sorted(dist):
        out("  Box %d: %d" % (box, dist[box]))
    return 0


def _cmd_lint(args, out) -> int:
    names = available_banks(args.bank_dir)
    if args.day is not None:
        names = [n for n in names if n == "day%d" % args.day]
    questions = load_bank([args.bank_dir / ("%s.yaml" % n) for n in names])
    errors = lint_bank(questions, concept_notes(args.vault), day=args.day)
    for e in errors:
        out(e)
    return 1 if errors else 0


def main(argv: Optional[List[str]] = None, stdin=None, stdout=None, stderr=None) -> int:
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    args = _parser().parse_args(argv)

    def out(msg: str) -> None:
        stdout.write(msg + "\n")

    def err(msg: str) -> None:
        stderr.write(msg + "\n")

    rng = random.Random(args.seed)
    banks = available_banks(args.bank_dir)
    cmd = args.command
    if cmd == "stats":
        return _cmd_stats(args, out)
    if cmd == "lint":
        return _cmd_lint(args, out)
    if cmd == "review":
        questions = load_bank([args.bank_dir / ("%s.yaml" % b) for b in banks])
        progress = load_progress(args.progress, warn=err)
        order = select_review(progress, [q.id for q in questions], rng)
        by_id = {q.id: q for q in questions}
        return _ask_session([by_id[i] for i in order], args, rng, stdin, stdout, out, err)
    if cmd not in banks:
        err("Unknown command '%s'. Banks: %s; or review | stats | lint" % (cmd, ", ".join(banks) or "(none)"))
        return 2
    questions = load_named(args.bank_dir, cmd)
    rng.shuffle(questions)
    return _ask_session(questions, args, rng, stdin, stdout, out, err)
