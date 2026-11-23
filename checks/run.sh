#!/usr/bin/env bash
# The whole quality gate, locally and in CI. Fails on the first problem.
#   checks/run.sh            (from the repo root, needs python3 with pyyaml and pytest)
#   docker compose run --rm checks
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== tests"
python3 -m pytest quiz/tests tools/tests -q

echo "== vault links"
python3 tools/check_links.py

echo "== vault pitch (prose budget, headings, banned phrases)"
python3 tools/check_pitch.py

echo "== question bank lint"
python3 quiz/quiz.py lint
echo "lint: OK"

echo "== all checks passed"
