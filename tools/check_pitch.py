#!/usr/bin/env python3
"""Enforce the vault's style contract ("the pitch").

    python3 tools/check_pitch.py                 # all notes in Concepts/, Conventions/, Syllabus/
    python3 tools/check_pitch.py --day 1         # only notes tagged day1
    python3 tools/check_pitch.py vault/Concepts/Caching.md ...   # just these notes

Checks per note: prose word budget, required headings, banned phrases.
Prose = words outside fenced blocks, table lines, heading lines, frontmatter
and the "Explain it to a teammate" section. Prints `PITCH <path>: <issue>`
per problem, or `OK: N notes checked`. Exit 1 on any issue.
"""
import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

BUDGETS = {"Concepts": 300, "Conventions": 300, "Syllabus": 900}
REQUIRED = {
    "Concepts": ["## Numbers", "## How it works", "## Probe", "## Cost", "## Traps", "## Related"],
    "Conventions": ["## Examples", "## Why", "## Probe", "## Related"],
}
BANNED = [
    "seamless", "effortless", "elastic", "in one sentence", "why it matters",
    "coming from hadoop", "the brain", "the muscles",
]
EXPLAIN_HEADING = "## Explain it to a teammate"
FOLDERS = tuple(BUDGETS)

_FENCE_RE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.S | re.M)
_WORD_RE = re.compile(r"[A-Za-z0-9_']+")


def strip_frontmatter(text: str) -> Tuple[List[str], str]:
    """Return (tags, body). Tags come from an inline `[a, b]` list or a `- item` block."""
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---\n", 4)
    if end == -1:
        return [], text
    fm, body = text[4:end], text[end + 5:]
    tags: List[str] = []
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("tags:"):
            continue
        rest = line[len("tags:"):].strip()
        if rest.startswith("["):
            tags = [t.strip().strip("'\"") for t in rest.strip("[]").split(",") if t.strip()]
        else:
            for nxt in lines[i + 1:]:
                if nxt.strip().startswith("- "):
                    tags.append(nxt.strip()[2:].strip().strip("'\""))
                else:
                    break
        break
    return tags, body


def prose_words(body: str) -> int:
    body = body.split(EXPLAIN_HEADING)[0]
    body = _FENCE_RE.sub("", body)
    kept = [l for l in body.splitlines() if not l.lstrip().startswith(("|", "#"))]
    return len(_WORD_RE.findall("\n".join(kept)))


def missing_headings(body: str, required: Sequence[str]) -> List[str]:
    lines = {l.strip() for l in body.splitlines()}
    return [h for h in required if not any(l == h or l.startswith(h + " ") for l in lines)]


def banned_hits(body: str, phrases: Sequence[str] = BANNED) -> List[str]:
    low = body.lower()
    hits = [(low.find(p), p) for p in phrases if p in low]
    return [p for _, p in sorted(hits)]


def check_note(path: Path, vault_dir: Path, budgets: Dict[str, int] = BUDGETS) -> List[str]:
    rel = Path(path).resolve().relative_to(Path(vault_dir).resolve())
    folder = rel.parts[0]
    if folder not in budgets:
        return []
    _, body = strip_frontmatter(Path(path).read_text(encoding="utf-8"))
    issues: List[str] = []
    n = prose_words(body)
    if n > budgets[folder]:
        issues.append("prose %d > %d" % (n, budgets[folder]))
    for h in missing_headings(body, REQUIRED.get(folder, [])):
        issues.append("missing heading %s" % h)
    if folder == "Conventions" and "**Rule:**" not in body:
        issues.append("missing **Rule:** line")
    for p in banned_hits(body):
        issues.append("banned phrase '%s'" % p)
    return issues


def _candidates(vault_dir: Path, day: Optional[int], explicit: Sequence[str]) -> List[Path]:
    if explicit:
        return [Path(p) for p in explicit]
    paths: List[Path] = []
    for folder in FOLDERS:
        d = vault_dir / folder
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.md")):
            if day is not None:
                tags, _ = strip_frontmatter(p.read_text(encoding="utf-8"))
                if "day%d" % day not in tags:
                    continue
            paths.append(p)
    return paths


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Check vault notes against the style contract.")
    parser.add_argument("--vault", default="vault", type=Path)
    parser.add_argument("--day", type=int, default=None)
    parser.add_argument("notes", nargs="*")
    args = parser.parse_args(argv)
    vault_dir = Path(args.vault)
    paths = _candidates(vault_dir, args.day, args.notes)
    failures = 0
    for p in paths:
        issues = check_note(p, vault_dir)
        rel = p.resolve().relative_to(vault_dir.resolve())
        for issue in issues:
            print("PITCH %s: %s" % (rel.as_posix(), issue))
        failures += bool(issues)
    if failures:
        return 1
    print("OK: %d notes checked" % len(paths))
    return 0


if __name__ == "__main__":
    sys.exit(main())
