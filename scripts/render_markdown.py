"""Render a weekly radar JSON record back to Markdown."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def render(record: dict[str, object]) -> str:
    raw_markdown = record.get("raw_markdown")
    if isinstance(raw_markdown, str) and raw_markdown.strip():
        return raw_markdown.strip() + "\n"

    lines = [f"# {record['title']}", "", f"Date: {record['date']}", "Status: reviewed", ""]
    themes = record.get("themes", [])
    if themes:
        lines.extend(["## Themes", "", *[f"- {theme}" for theme in themes], ""])

    signals = record.get("signals", [])
    if signals:
        lines.extend(["## Signals", ""])
        for signal in signals:
            lines.extend([f"### {signal['title']}", "", str(signal["summary"]).strip(), ""])

    ideas = record.get("ideas", [])
    if ideas:
        lines.extend(["## Ideas", ""])
        for idea in ideas:
            lines.extend([f"### {idea['title']}", "", str(idea["summary"]).strip(), ""])

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    record = json.loads(args.json_file.read_text(encoding="utf-8"))
    markdown = render(record)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

