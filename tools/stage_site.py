#!/usr/bin/env python3
"""Stage the Obsidian vault as Quartz content.

    python3 tools/stage_site.py vault _quartz/content

Copies every note out of the vault (skipping Templates/ and .obsidian/),
moves a leading `# Heading` into frontmatter `title:` so Quartz shows one
title per page, and publishes the Home note as index.md (rewriting links to
it) so the site root is the Home note. The output directory is emptied first.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple

SKIP_DIRS = ("Templates", ".obsidian")
HOME_NOTE = "00 Home"
HOME_ALIAS = "Home"
HOME_LINK_RE = re.compile(r"\[\[" + re.escape(HOME_NOTE) + r"(\|[^\]]*)?\]\]")


def split_frontmatter(text: str) -> Tuple[Optional[str], str]:
    """Return (frontmatter_without_fences, body). Frontmatter is None if absent."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + len("\n---\n"):]


def hoist_title(text: str) -> str:
    """Move a leading `# Title` line into frontmatter `title:`; otherwise unchanged."""
    fm, body = split_frontmatter(text)
    stripped = body.lstrip("\n")
    if not stripped.startswith("# "):
        return text
    first, _, rest = stripped.partition("\n")
    title = first[2:].strip()
    if fm is not None and any(line.startswith("title:") for line in fm.splitlines()):
        return text
    quoted = '"' + title.replace("\\", "\\\\").replace('"', '\\"') + '"'
    fm_lines = (fm.rstrip("\n") + "\n") if fm else ""
    return "---\n" + fm_lines + "title: " + quoted + "\n---\n" + rest


def rewrite_home_links(text: str) -> str:
    """[[00 Home]] -> [[index|Home]], [[00 Home|x]] -> [[index|x]]."""
    return HOME_LINK_RE.sub(lambda m: "[[index" + (m.group(1) or "|" + HOME_ALIAS) + "]]", text)


def iter_notes(vault_dir: Path, skip_dirs: Iterable[str] = SKIP_DIRS) -> Iterable[Path]:
    skip = set(skip_dirs)
    for path in sorted(vault_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(vault_dir)
        if rel.parts[0] in skip:
            continue
        yield path


def stage(vault_dir: Path, out_dir: Path, skip_dirs: Iterable[str] = SKIP_DIRS) -> int:
    """Rebuild out_dir from vault_dir. Returns the number of markdown notes staged."""
    vault_dir = Path(vault_dir)
    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    notes = 0
    for src in iter_notes(vault_dir, skip_dirs):
        rel = src.relative_to(vault_dir)
        if rel == Path(HOME_NOTE + ".md"):
            rel = Path("index.md")
        dst = out_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix.lower() == ".md":
            text = rewrite_home_links(src.read_text(encoding="utf-8"))
            dst.write_text(hoist_title(text), encoding="utf-8")
            notes += 1
        else:
            shutil.copy2(src, dst)
    return notes


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("vault", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args(argv)
    count = stage(args.vault, args.out)
    print("staged %d notes into %s" % (count, args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
