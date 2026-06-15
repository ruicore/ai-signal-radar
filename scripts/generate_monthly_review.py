"""Generate a deterministic monthly review from reviewed weekly radar JSON."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("month", help="Month to review, formatted YYYY-MM.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path. Defaults to indexes/monthly_reviews/YYYY-MM.md.",
    )
    return parser.parse_args()


def load_month(month: str) -> list[dict[str, Any]]:
    year = month[:4]
    records: list[dict[str, Any]] = []
    for path in sorted((REPO_ROOT / "data" / year).glob(f"{month}-*.json")):
        records.append(json.loads(path.read_text(encoding="utf-8")))
    return records


def render(month: str, records: list[dict[str, Any]]) -> str:
    lines = [f"# Monthly AI Signal Review: {month}", ""]
    if not records:
        return "\n".join([*lines, "No reviewed weekly radars found for this month.", ""])

    theme_counts: Counter[str] = Counter()
    for record in records:
        theme_counts.update(record.get("themes", []))

    lines.extend(["## Reviewed Radars", ""])
    for record in records:
        lines.append(f"- {record['date']}: [{record['title']}](../{record['markdown_path']})")

    lines.extend(["", "## Theme Frequency", ""])
    if theme_counts:
        for theme, count in sorted(theme_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"- {theme}: {count}")
    else:
        lines.append("- No themes recorded.")

    lines.extend(["", "## Signals To Revisit", ""])
    for record in records:
        for signal in record.get("signals", []):
            lines.append(f"- {record['date']} / {signal['title']}")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    output = args.output or REPO_ROOT / "indexes" / "monthly_reviews" / f"{args.month}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(args.month, load_month(args.month)), encoding="utf-8")
    print(output.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

