import io
import json
from pathlib import Path

import pytest

from quizlib.cli import main

BANK = """
- id: d1-a-001
  type: tf
  concept: Alpha
  tags: [day1, architecture]
  difficulty: 1
  prompt: Alpha is true.
  answer: true
  explanation: Alpha explanation.
- id: d1-a-002
  type: tf
  concept: Beta
  tags: [day1, storage]
  difficulty: 1
  prompt: Beta is true.
  answer: true
  explanation: Beta explanation.
"""


@pytest.fixture
def env(tmp_path):
    vault = tmp_path / "vault"
    (vault / "Concepts").mkdir(parents=True)
    (vault / "Concepts" / "Alpha.md").write_text("---\ntags: [concept, day1]\n---\n# Alpha\n")
    (vault / "Concepts" / "Beta.md").write_text("---\ntags: [concept, day1]\n---\n# Beta\n")
    bank = tmp_path / "bank"
    bank.mkdir()
    (bank / "day1.yaml").write_text(BANK)
    progress = tmp_path / "results" / "progress.json"
    return {"vault": vault, "bank": bank, "progress": progress}


def run(env, args, stdin=""):
    out, err = io.StringIO(), io.StringIO()
    code = main(args + ["--vault", str(env["vault"]), "--bank-dir", str(env["bank"]), "--progress", str(env["progress"])],
                stdin=io.StringIO(stdin), stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def test_runs_named_bank_end_to_end(env):
    code, out, err = run(env, ["day1", "--seed", "1"], stdin="t\nf\n")
    assert code == 0 and "Score: 1/2 (50%)" in out and "Read: vault/Concepts/" in out
    data = json.loads(env["progress"].read_text())
    assert set(data["cards"]) == {"d1-a-001", "d1-a-002"}


def test_n_larger_than_bank_asks_all(env):
    code, out, err = run(env, ["day1", "--n", "50"], stdin="t\nt\n")
    assert code == 0 and "Q2/2" in out and "Score: 2/2" in out


def test_tag_filter_limits_questions(env):
    code, out, err = run(env, ["day1", "--tag", "storage"], stdin="t\n")
    assert code == 0 and "Q1/1\nBeta is true." in out


def test_no_match_exits_cleanly(env):
    code, out, err = run(env, ["day1", "--tag", "nothing"])
    assert code == 0 and "No questions match." in out
    assert not env["progress"].exists()


def test_unknown_command_returns_2(env):
    code, out, err = run(env, ["day9"])
    assert code == 2 and "Unknown command 'day9'" in err and "day1" in err and "review | stats | lint" in err


def test_lint_reports_and_returns_1(env):
    (env["vault"] / "Concepts" / "Gamma.md").write_text("---\ntags: [concept, day1]\n---\n")
    code, out, err = run(env, ["lint"])
    assert code == 1 and "coverage: note 'Gamma' has no question" in out
    code, out, err = run(env, ["lint", "--day", "2"])
    assert code == 0


def test_stats_after_session_lists_weakest(env):
    run(env, ["day1", "--seed", "1"], stdin="t\nf\n")
    code, out, err = run(env, ["stats"])
    assert code == 0 and "day1" in out and "Weakest" in out
    assert "Read: vault/Concepts/" in out and "Box 1:" in out


def test_stats_with_no_progress(env):
    code, out, err = run(env, ["stats"])
    assert code == 0 and "No progress yet" in out


def test_review_puts_box1_first(env):
    run(env, ["day1", "--seed", "1"], stdin="t\nf\n")   # question order with seed 1; one right one wrong
    data = json.loads(env["progress"].read_text())
    missed = [k for k, v in data["cards"].items() if v["box"] == 1][0]
    code, out, err = run(env, ["review", "--seed", "1"], stdin="t\nt\n")
    first_prompt = out.split("Q1/")[1].split("\n")[1]
    concept = "Alpha" if missed == "d1-a-001" else "Beta"
    assert first_prompt == "%s is true." % concept


def test_eof_mid_session_saves_partial(env):
    code, out, err = run(env, ["day1", "--seed", "1"], stdin="t\n")
    assert code == 0 and "Stopped." in out
    assert len(json.loads(env["progress"].read_text())["cards"]) == 1
