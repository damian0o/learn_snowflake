"""Persisting learner progress (one Card per question id) as JSON."""
import json
import os
import shutil
import sys
import tempfile
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict

from .leitner import Card

VERSION = 1


def _stderr(msg: str) -> None:
    print(msg, file=sys.stderr)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _reset(path: Path, reason: str, warn: Callable[[str], None]) -> Dict[str, Card]:
    backup = path.with_name(path.name + ".bak")
    shutil.copyfile(path, backup)
    warn("Progress file %s is corrupt (%s); backed up to %s and starting fresh." % (path, reason, backup))
    return {}


def load_progress(path: Path, warn: Callable[[str], None] = _stderr) -> Dict[str, Card]:
    path = Path(path)
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return _reset(path, "invalid JSON: %s" % exc, warn)
    if not isinstance(raw, dict) or raw.get("version") != VERSION or not isinstance(raw.get("cards"), dict):
        return _reset(path, "unknown format or version", warn)
    try:
        return {qid: Card(**fields) for qid, fields in raw["cards"].items()}
    except TypeError as exc:
        return _reset(path, "bad card fields: %s" % exc, warn)


def save_progress(path: Path, progress: Dict[str, Card]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": VERSION, "cards": {qid: asdict(card) for qid, card in progress.items()}}
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".progress-", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")
    os.replace(tmp, path)
