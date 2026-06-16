"""Generate a deterministic monthly review from reviewed weekly radar JSON and indexes."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
INDEX_ROOT = REPO_ROOT / "indexes"
MONTHLY_REPORT_ROOT = REPO_ROOT / "reports" / "monthly"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "month",
        nargs="?",
        help="Month to review, formatted YYYY-MM. Defaults to the previous UTC month.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path. Defaults to reports/monthly/YYYY-MM.md.",
    )
    return parser.parse_args()


def previous_month(today: date | None = None) -> str:
    current = today or datetime.now(UTC).date()
    first_day_this_month = current.replace(day=1)
    last_day_previous_month = first_day_this_month - timedelta(days=1)
    return f"{last_day_previous_month:%Y-%m}"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_month(month: str) -> list[dict[str, Any]]:
    year = month[:4]
    records: list[dict[str, Any]] = []
    for path in sorted((DATA_ROOT / year).glob(f"{month}-*.json")):
        records.append(load_json(path))
    return sorted(records, key=lambda item: item["date"])


def load_indexes() -> dict[str, Any]:
    indexes: dict[str, Any] = {}
    for name in ("weekly_radars", "themes", "summary"):
        path = INDEX_ROOT / f"{name}.json"
        indexes[name] = load_json(path) if path.exists() else None
    return indexes


def markdown_link(record: dict[str, Any]) -> str:
    return f"[{record['title']}](../../{record['markdown_path']})"


def count_monthly_items(records: list[dict[str, Any]]) -> tuple[int, int]:
    signal_count = sum(len(record.get("signals", [])) for record in records)
    idea_count = sum(len(record.get("ideas", [])) for record in records)
    return signal_count, idea_count


def render(month: str, records: list[dict[str, Any]], indexes: dict[str, Any] | None = None) -> str:
    indexes = indexes or {}
    signal_count, idea_count = count_monthly_items(records)
    lines = [f"# Monthly AI Signal Review: {month}", ""]
    lines.extend(
        [
            "Generated deterministically from reviewed radar data and repository indexes.",
            "No OpenAI API or external data was used.",
            "",
        ]
    )

    if not records:
        return "\n".join([*lines, "No reviewed weekly radars found for this month.", ""])

    theme_counts: Counter[str] = Counter()
    for record in records:
        theme_counts.update(record.get("themes", []))

    lines.extend(
        [
            "## Coverage",
            "",
            f"- Reviewed weekly radars: {len(records)}",
            f"- Signals captured: {signal_count}",
            f"- Ideas captured: {idea_count}",
            "",
        ]
    )

    summary = indexes.get("summary")
    if isinstance(summary, dict):
        lines.extend(
            [
                "## Repository Snapshot",
                "",
                f"- Total reviewed radars: {summary.get('weekly_radar_count', 0)}",
                f"- Total signals: {summary.get('signal_count', 0)}",
                f"- Total ideas: {summary.get('idea_count', 0)}",
                "",
            ]
        )

    lines.extend(["## Reviewed Radars", ""])
    for record in records:
        lines.append(f"- {record['date']}: {markdown_link(record)}")

    lines.extend(["", "## Theme Frequency", ""])
    if theme_counts:
        for theme, count in sorted(theme_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"- {theme}: {count}")
    else:
        lines.append("- No themes recorded.")

    lines.extend(["", "## Signals To Revisit", ""])
    signals_added = False
    for record in records:
        for signal in sorted(record.get("signals", []), key=lambda item: item["title"]):
            themes = ", ".join(signal.get("themes", [])) or "unthemed"
            lines.append(f"- {record['date']} / {signal['title']} ({themes})")
            signals_added = True
    if not signals_added:
        lines.append("- No signals captured.")

    lines.extend(["", "## Ideas To Revisit", ""])
    ideas_added = False
    for record in records:
        for idea in sorted(record.get("ideas", []), key=lambda item: item["title"]):
            themes = ", ".join(idea.get("themes", [])) or "unthemed"
            lines.append(f"- {record['date']} / {idea['title']} ({themes})")
            ideas_added = True
    if not ideas_added:
        lines.append("- No ideas captured.")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    month = args.month or previous_month()
    output = args.output or MONTHLY_REPORT_ROOT / f"{month}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(month, load_month(month), load_indexes()), encoding="utf-8")
    print(output.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
