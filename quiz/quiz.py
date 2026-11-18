#!/usr/bin/env python3
"""Entry point: python3 quiz/quiz.py day1 | review | stats | lint"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from quizlib.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
