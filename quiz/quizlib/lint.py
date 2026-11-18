"""Validation of question banks against the vault's concept notes."""
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

from .bank import Question

ID_RE = re.compile(r"^(d[1-3]|cum)-[a-z]+-\d{3}$")
TYPES = ("mcq", "multi", "tf", "fill")
NOTE_FOLDERS = ("Concepts", "Conventions")
_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.S)


def frontmatter_tags(text: str) -> Set[str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return set()
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return set()
    tags = data.get("tags") if isinstance(data, dict) else None
    if tags is None:
        return set()
    if isinstance(tags, str):
        return {tags}
    return {str(t) for t in tags}


def concept_notes(vault_dir: Path) -> Dict[str, Set[str]]:
    notes: Dict[str, Set[str]] = {}
    for folder in NOTE_FOLDERS:
        root = Path(vault_dir) / folder
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            notes[path.stem] = frontmatter_tags(path.read_text(encoding="utf-8"))
    return notes


def _is_str(x: Any) -> bool:
    return isinstance(x, str) and x.strip() != ""


def _lint_question(q: Question, notes: Dict[str, Set[str]]) -> List[str]:
    errs: List[str] = []
    e = lambda msg: errs.append("%s: %s" % (q.id or "<no id>", msg))  # noqa: E731
    if not ID_RE.match(q.id):
        e("id does not match %s" % ID_RE.pattern)
    if q.type not in TYPES:
        e("type '%s' is not one of %s" % (q.type, ", ".join(TYPES)))
    if q.difficulty not in (1, 2, 3):
        e("difficulty must be 1, 2 or 3")
    if not q.tags or not all(_is_str(t) for t in q.tags):
        e("tags must be a non-empty list of strings")
    if not _is_str(q.prompt):
        e("prompt is empty")
    if not _is_str(q.explanation):
        e("explanation is empty")
    if q.concept not in notes:
        e("concept '%s' has no note in Concepts/ or Conventions/" % q.concept)
    for i, opt in enumerate(q.options):
        if not _is_str(opt):
            e("option %d is not a string (%r); quote it in YAML" % (i + 1, opt))
    if q.type in ("mcq", "multi"):
        if len(q.options) < 3:
            e("needs at least 3 options")
        if len(set(map(str, q.options))) != len(q.options):
            e("options are not unique")
    if q.type == "mcq":
        if not _is_str(q.answer):
            e("answer %r is not a string; quote it in YAML" % (q.answer,))
        elif q.answer not in q.options:
            e("answer '%s' is not one of the options" % q.answer)
    elif q.type == "multi":
        if not isinstance(q.answer, list) or len(q.answer) < 2:
            e("multi answer must be a list of at least 2 options")
        else:
            for a in q.answer:
                if not _is_str(a):
                    e("multi answer %r is not a string; quote it in YAML" % (a,))
                elif a not in q.options:
                    e("answer '%s' is not one of the options" % a)
    elif q.type == "tf":
        if not isinstance(q.answer, bool):
            e("tf answer must be true or false")
        if q.options:
            e("tf questions take no options")
    elif q.type == "fill":
        if not isinstance(q.answer, list) or not q.answer:
            e("fill answer must be a non-empty list of accepted strings")
        else:
            for a in q.answer:
                if not _is_str(a):
                    e("fill answer %r is not a string; quote it in YAML" % (a,))
        if q.options:
            e("fill questions take no options")
    return errs


def lint_bank(questions: List[Question], notes: Dict[str, Set[str]], day: Optional[int] = None) -> List[str]:
    errs: List[str] = []
    seen: Set[str] = set()
    for q in questions:
        if q.id in seen:
            errs.append("%s: duplicate id" % q.id)
        seen.add(q.id)
        errs.extend(_lint_question(q, notes))
    covered = {q.concept for q in questions}
    want = "day%d" % day if day is not None else None
    for name in sorted(notes):
        if want is not None and want not in notes[name]:
            continue
        if name not in covered:
            errs.append("coverage: note '%s' has no question" % name)
    return errs
