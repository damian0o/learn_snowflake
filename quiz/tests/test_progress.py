import json
import re

from quizlib.leitner import Card
from quizlib.progress import load_progress, now_iso, save_progress


def test_missing_file_gives_empty(tmp_path):
    assert load_progress(tmp_path / "p.json") == {}


def test_roundtrip(tmp_path):
    p = tmp_path / "deep" / "p.json"
    data = {"d1-a-001": Card(box=2, asked=3, correct=2, last_asked="2026-11-18T09:15:00Z", last_result=True)}
    save_progress(p, data)
    raw = json.loads(p.read_text())
    assert raw["version"] == 1 and set(raw["cards"]) == {"d1-a-001"}
    assert load_progress(p) == data


def test_corrupt_file_backed_up_and_reset(tmp_path):
    p = tmp_path / "p.json"
    p.write_text("{not json")
    warnings = []
    assert load_progress(p, warn=warnings.append) == {}
    assert (tmp_path / "p.json.bak").read_text() == "{not json"
    assert warnings and "corrupt" in warnings[0].lower()


def test_unknown_version_is_treated_as_corrupt(tmp_path):
    p = tmp_path / "p.json"
    p.write_text(json.dumps({"version": 99, "cards": {}}))
    warnings = []
    assert load_progress(p, warn=warnings.append) == {}
    assert (tmp_path / "p.json.bak").exists() and warnings


def test_now_iso_format():
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", now_iso())
