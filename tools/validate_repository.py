#!/usr/bin/env python3
"""Run lightweight, hardware-independent repository checks."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".cfg",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".json",
    ".md",
    ".py",
    ".rules",
    ".sh",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PERSONAL_PATH_PATTERNS = {
    "Linux home path": re.compile(r"/home/(?!\$USER(?:/|$)|<user>(?:/|$)|\.\.\.(?:/|$))[^/\s`'\"<>]+/"),
    "macOS home path": re.compile(r"/Users/(?!\$USER(?:/|$)|<user>(?:/|$))[^/\s`'\"<>]+/"),
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s`'\"<>]+\\"),
    "file URI home path": re.compile(r"file:///home/"),
}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / item.decode() for item in result.stdout.split(b"\0") if item]


def read_text(path: Path) -> str | None:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def validate_personal_paths(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        if path.resolve() == Path(__file__).resolve():
            continue
        text = read_text(path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in PERSONAL_PATH_PATTERNS.items():
                if pattern.search(line):
                    relative = path.relative_to(ROOT)
                    errors.append(f"{relative}:{line_number}: {label}")
    return errors


def clean_markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    elif " " in target:
        target = target.split(" ", maxsplit=1)[0]
    return unquote(target.split("#", maxsplit=1)[0])


def validate_markdown_links(files: list[Path]) -> tuple[list[str], int]:
    errors: list[str] = []
    checked = 0
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            raw_target = match.group(1).strip()
            if raw_target.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#")):
                continue
            target = clean_markdown_target(raw_target)
            if not target:
                continue
            checked += 1
            line_number = text.count("\n", 0, match.start()) + 1
            if target.startswith(("/", "file://")):
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: root/absolute link: {raw_target}")
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(ROOT):
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: link leaves repository: {raw_target}")
            elif not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: missing link target: {raw_target}")
    return errors, checked


def main() -> int:
    files = tracked_files()
    errors = validate_personal_paths(files)
    link_errors, checked_links = validate_markdown_links(files)
    errors.extend(link_errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(files)} tracked files.")
    print(f"Validated {checked_links} local Markdown links.")
    print("No machine-specific personal paths found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
