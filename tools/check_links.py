#!/usr/bin/env python3
"""Vault graph integrity: no dangling wikilinks, no orphan concept notes, quiz concepts resolve.

Usage: python3 tools/check_links.py [--vault V] [--bank-dir B] [--day N]
"""
import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "quiz"))

from quizlib.bank import available_banks, load_bank  # noqa: E402
from quizlib.lint import frontmatter_tags  # noqa: E402

WIKILINK_RE = re.compile(r"!?\[\[([^\]\[]+?)\]\]")
_FENCE_RE = re.compile(r"```.*?```", re.S)
_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def find_wikilinks(text: str) -> Set[str]:
    text = _FENCE_RE.sub("", text)
    text = _INLINE_CODE_RE.sub("", text)
    targets: Set[str] = set()
    for m in WIKILINK_RE.finditer(text):
        target = re.split(r"[|#^]", m.group(1), maxsplit=1)[0].strip()
        if target:
            targets.add(target)
    return targets


@dataclass
class VaultIndex:
    notes: Dict[str, Path] = field(default_factory=dict)
    display: Dict[str, str] = field(default_factory=dict)
    links: Dict[str, Set[str]] = field(default_factory=dict)
    link_text: Dict[str, Dict[str, str]] = field(default_factory=dict)
    tags: Dict[str, Set[str]] = field(default_factory=dict)
    duplicates: List[str] = field(default_factory=list)


def scan_vault(vault_dir: Path, skip_dirs: Tuple[str, ...] = ("Templates", ".obsidian")) -> VaultIndex:
    idx = VaultIndex()
    vault_dir = Path(vault_dir)
    for path in sorted(vault_dir.rglob("*.md")):
        rel = path.relative_to(vault_dir)
        if any(part in skip_dirs for part in rel.parts[:-1]):
            continue
        key = path.stem.lower()
        if key in idx.notes:
            idx.duplicates.append(path.stem)
            continue
        text = path.read_text(encoding="utf-8")
        idx.notes[key] = path
        idx.display[key] = path.stem
        idx.tags[key] = frontmatter_tags(text)
        targets = find_wikilinks(text)
        idx.links[key] = {t.lower() for t in targets}
        idx.link_text[key] = {t.lower(): t for t in targets}
    return idx


def dangling(index: VaultIndex) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for src in sorted(index.links):
        for target in sorted(index.links[src]):
            if target not in index.notes:
                out.append((index.display[src], index.link_text[src][target]))
    return out


def orphans(index: VaultIndex, folders: Tuple[str, ...] = ("Concepts", "Conventions"),
            day: Optional[int] = None) -> List[str]:
    inbound: Set[str] = set()
    for src, targets in index.links.items():
        inbound.update(t for t in targets if t != src)
    want = "day%d" % day if day is not None else None
    out: List[str] = []
    for key, path in sorted(index.notes.items()):
        if path.parent.name not in folders and not any(p in folders for p in path.parts):
            continue
        if want is not None and want not in index.tags.get(key, set()):
            continue
        if key not in inbound:
            out.append(index.display[key])
    return out


def unresolved_quiz_concepts(concepts: Set[str], index: VaultIndex) -> List[str]:
    return sorted(c for c in concepts if c.lower() not in index.notes)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--vault", type=Path, default=REPO / "vault")
    p.add_argument("--bank-dir", type=Path, default=REPO / "quiz" / "bank")
    p.add_argument("--day", type=int, default=None, help="only check orphans among notes tagged dayN")
    args = p.parse_args(argv)

    index = scan_vault(args.vault)
    problems: List[str] = []
    problems.extend("DUPLICATE %s (same note name in two folders)" % d for d in index.duplicates)
    problems.extend("DANGLING [[%s]] in %s" % (target, src) for src, target in dangling(index))
    problems.extend("ORPHAN %s (no note links to it)" % o for o in orphans(index, day=args.day))

    if args.bank_dir.is_dir():
        names = available_banks(args.bank_dir)
        if args.day is not None:
            names = [n for n in names if n == "day%d" % args.day]
        questions = load_bank([args.bank_dir / ("%s.yaml" % n) for n in names])
        problems.extend("QUIZ %s (concept named in bank has no note)" % c
                        for c in unresolved_quiz_concepts({q.concept for q in questions}, index))

    if problems:
        for line in problems:
            print(line)
        return 1
    n_links = sum(len(v) for v in index.links.values())
    print("OK: %d notes, %d links" % (len(index.notes), n_links))
    return 0


if __name__ == "__main__":
    sys.exit(main())
