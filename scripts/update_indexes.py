"""Rebuild agent-friendly indexes from structured weekly radar JSON files."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
INDEX_ROOT = REPO_ROOT / "indexes"
THEMES_ROOT = REPO_ROOT / "themes"


def load_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(DATA_ROOT.glob("*/*.json")):
        records.append(json.loads(path.read_text(encoding="utf-8")))
    return records


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_weekly_index(records: list[dict[str, Any]]) -> list[dict[str, object]]:
    return [
        {
            "date": record["date"],
            "title": record["title"],
            "themes": record.get("themes", []),
            "markdown_path": record["markdown_path"],
            "data_path": f"data/{record['date'][:4]}/{record['date']}.json",
        }
        for record in sorted(records, key=lambda item: item["date"])
    ]


def build_theme_index(records: list[dict[str, Any]]) -> dict[str, list[dict[str, str]]]:
    themes: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in sorted(records, key=lambda item: item["date"]):
        for theme in record.get("themes", []):
            themes[theme].append(
                {
                    "date": record["date"],
                    "title": record["title"],
                    "markdown_path": record["markdown_path"],
                }
            )
    return dict(sorted(themes.items()))


def write_theme_readme(theme_index: dict[str, list[dict[str, str]]]) -> None:
    lines = ["# Themes", ""]
    if not theme_index:
        lines.append("No reviewed radar themes have been indexed yet.")
    for theme, entries in theme_index.items():
        lines.extend([f"## {theme}", ""])
        for entry in entries:
            lines.append(f"- {entry['date']}: [{entry['title']}](../{entry['markdown_path']})")
        lines.append("")
    THEMES_ROOT.mkdir(parents=True, exist_ok=True)
    (THEMES_ROOT / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_summary(records: list[dict[str, Any]]) -> dict[str, object]:
    theme_counts: Counter[str] = Counter()
    signal_count = 0
    idea_count = 0
    for record in records:
        theme_counts.update(record.get("themes", []))
        signal_count += len(record.get("signals", []))
        idea_count += len(record.get("ideas", []))

    return {
        "weekly_radar_count": len(records),
        "signal_count": signal_count,
        "idea_count": idea_count,
        "theme_counts": dict(sorted(theme_counts.items())),
    }


def main() -> int:
    records = load_records()
    theme_index = build_theme_index(records)
    write_json(INDEX_ROOT / "weekly_radars.json", build_weekly_index(records))
    write_json(INDEX_ROOT / "themes.json", theme_index)
    write_json(INDEX_ROOT / "summary.json", build_summary(records))
    write_theme_readme(theme_index)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

