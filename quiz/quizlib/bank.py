"""Question bank loading. Banks are YAML lists of question mappings."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

import yaml


@dataclass
class Question:
    id: str
    type: str
    concept: str
    tags: List[str]
    difficulty: int
    prompt: str
    options: List[str]
    answer: Any
    explanation: str
    source: str = ""


def _keep_list(value: Any) -> Any:
    """Return [] for None, a copy for lists, and anything else unchanged so lint can reject it
    (list("day1") would silently become ['d', 'a', 'y', '1'])."""
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    return value


def _to_question(raw: Any, source: str) -> Question:
    if not isinstance(raw, dict):
        raise ValueError("%s: each question must be a mapping, got %r" % (source, type(raw).__name__))
    return Question(
        id=str(raw.get("id", "")),
        type=str(raw.get("type", "")),
        concept=str(raw.get("concept", "")),
        tags=_keep_list(raw.get("tags")),
        difficulty=raw.get("difficulty", 0),
        prompt=raw.get("prompt", ""),
        options=_keep_list(raw.get("options")),
        answer=raw.get("answer"),
        explanation=raw.get("explanation", ""),
        source=source,
    )


def load_bank(paths: List[Path]) -> List[Question]:
    questions: List[Question] = []
    for path in paths:
        path = Path(path)
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data is None:
            data = []
        if not isinstance(data, list):
            raise ValueError("%s: bank must be a list of questions" % path)
        questions.extend(_to_question(item, path.stem) for item in data)
    return questions


def load_named(bank_dir: Path, name: str) -> List[Question]:
    path = Path(bank_dir) / ("%s.yaml" % name)
    if not path.is_file():
        raise FileNotFoundError("No bank named '%s' in %s" % (name, bank_dir))
    return load_bank([path])


def available_banks(bank_dir: Path) -> List[str]:
    return sorted(p.stem for p in Path(bank_dir).glob("*.yaml"))
