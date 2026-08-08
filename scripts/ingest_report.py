"""Ingest a Ray-approved report into one repository radar track."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
RADAR_TYPES = ("systems", "creation")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--track",
        choices=RADAR_TYPES,
        default="systems",
        help="Radar track. Defaults to systems for backward-compatible CLI use.",
    )
    parser.add_argument("--date", required=True, help="Reviewed report date, formatted YYYY-MM-DD.")
    parser.add_argument("--input", type=Path, help="Approved Markdown report. Defaults to stdin.")
    parser.add_argument("--title", help="Override report title.")
    parser.add_argument(
        "--window-start", help="Observation-window start date, formatted YYYY-MM-DD."
    )
    parser.add_argument("--window-end", help="Observation-window end date, formatted YYYY-MM-DD.")
    parser.add_argument(
        "--theme",
        action="append",
        default=[],
        help="Theme to attach to the report. Can be repeated.",
    )
    parser.add_argument(
        "--yes-reviewed",
        action="store_true",
        help="Confirm the report was reviewed by Ray before ingestion.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing radar and data files for the same date.",
    )
    return parser.parse_args()


def read_markdown(input_path: Path | None) -> str:
    if input_path is None:
        return sys.stdin.read().strip() + "\n"
    return input_path.read_text(encoding="utf-8").strip() + "\n"


def first_heading(markdown: str) -> str | None:
    for line in markdown.splitlines():
        match = HEADING_RE.match(line)
        if match:
            return match.group(2).strip()
    return None


def extract_sections(markdown: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in markdown.splitlines():
        match = HEADING_RE.match(line)
        if match:
            if current_title and current_lines:
                sections.append(
                    {"title": current_title, "summary": "\n".join(current_lines).strip()}
                )
            current_title = match.group(2).strip()
            current_lines = []
            continue
        if current_title:
            current_lines.append(line)

    if current_title and current_lines:
        sections.append({"title": current_title, "summary": "\n".join(current_lines).strip()})

    return [section for section in sections if section["summary"]]


def record_from_markdown(
    radar_type: str,
    report_date: date,
    markdown: str,
    title: str | None,
    themes: list[str],
    source_file: Path | None,
    window_start: date | None = None,
    window_end: date | None = None,
) -> dict[str, object]:
    if radar_type not in RADAR_TYPES:
        raise ValueError(f"unsupported radar track: {radar_type}")
    if (window_start is None) != (window_end is None):
        raise ValueError("observation window requires both start and end dates")
    if radar_type == "creation" and (window_start is None or window_end is None):
        raise ValueError("creation reports require an observation window")
    if window_start and window_end and window_start > window_end:
        raise ValueError("observation-window start must not be after its end")

    markdown_path = f"radars/{radar_type}/{report_date:%Y}/{report_date.isoformat()}.md"
    unique_themes = sorted({theme.strip() for theme in themes if theme.strip()})
    sections = extract_sections(markdown)
    signals = [
        {"title": section["title"], "summary": section["summary"], "themes": unique_themes}
        for section in sections
    ]

    return {
        "schema_version": "2.0",
        "radar_type": radar_type,
        "date": report_date.isoformat(),
        "title": title or first_heading(markdown) or f"AI Signal Radar {report_date.isoformat()}",
        "status": "reviewed",
        "reviewed_by": "Ray",
        "source": {
            "generator": "ChatGPT",
            "reviewed_before_ingestion": True,
            **({"source_file": str(source_file)} if source_file else {}),
        },
        "themes": unique_themes,
        "signals": signals,
        "ideas": [],
        **(
            {
                "observation_window": {
                    "start": window_start.isoformat(),
                    "end": window_end.isoformat(),
                }
            }
            if window_start and window_end
            else {}
        ),
        "markdown_path": markdown_path,
        "raw_markdown": markdown,
    }


def write_outputs(record: dict[str, object], markdown: str, force: bool) -> tuple[Path, Path]:
    report_date = date.fromisoformat(str(record["date"]))
    radar_type = str(record["radar_type"])
    radar_path = (
        REPO_ROOT
        / "radars"
        / radar_type
        / f"{report_date:%Y}"
        / f"{report_date.isoformat()}.md"
    )
    data_path = (
        REPO_ROOT
        / "data"
        / radar_type
        / f"{report_date:%Y}"
        / f"{report_date.isoformat()}.json"
    )

    for path in (radar_path, data_path):
        if path.exists() and not force:
            raise FileExistsError(f"{path} already exists. Re-run with --force to overwrite.")

    radar_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    radar_path.write_text(markdown, encoding="utf-8")
    data_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return radar_path, data_path


def main() -> int:
    args = parse_args()
    if not args.yes_reviewed:
        print(
            "Refusing ingestion: pass --yes-reviewed after Ray approves the report.",
            file=sys.stderr,
        )
        return 2

    report_date = date.fromisoformat(args.date)
    window_start = date.fromisoformat(args.window_start) if args.window_start else None
    window_end = date.fromisoformat(args.window_end) if args.window_end else None
    markdown = read_markdown(args.input)
    record = record_from_markdown(
        args.track,
        report_date,
        markdown,
        args.title,
        args.theme,
        args.input,
        window_start,
        window_end,
    )
    radar_path, data_path = write_outputs(record, markdown, args.force)
    print(radar_path.relative_to(REPO_ROOT))
    print(data_path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
