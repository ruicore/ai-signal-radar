"""Validate reviewed radar content and derived index determinism."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.update_indexes import build_index_outputs  # noqa: E402

DATA_ROOT = REPO_ROOT / "data"
RADARS_ROOT = REPO_ROOT / "radars"
SCHEMA_PATH = REPO_ROOT / "schemas" / "weekly_radar.schema.json"


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return None, [f"{relative(path)}:{error.lineno}:{error.colno}: invalid JSON: {error.msg}"]

    if not isinstance(payload, dict):
        return None, [f"{relative(path)}: expected a JSON object"]

    return payload, []


def parse_date(value: object, context: str) -> tuple[date | None, list[str]]:
    if not isinstance(value, str):
        return None, [f"{context}: date must be a string"]
    try:
        return date.fromisoformat(value), []
    except ValueError:
        return None, [f"{context}: date must be formatted YYYY-MM-DD"]


def data_paths() -> list[Path]:
    return sorted(DATA_ROOT.rglob("*.json"))


def radar_paths() -> list[Path]:
    return sorted(RADARS_ROOT.rglob("*.md"))


def validate_file_shape(path: Path, root: Path, extension: str) -> list[str]:
    errors: list[str] = []
    rel_path = relative(path)

    if path.parent.parent != root:
        errors.append(f"{rel_path}: expected path shape {root.name}/YYYY/YYYY-MM-DD{extension}")

    year = path.parent.name
    if len(year) != 4 or not year.isdigit():
        errors.append(f"{rel_path}: parent directory must be a four-digit year")

    parsed, date_errors = parse_date(path.stem, rel_path)
    errors.extend(date_errors)
    if parsed and f"{parsed:%Y}" != year:
        errors.append(f"{rel_path}: filename date does not match parent year")

    if path.suffix != extension:
        errors.append(f"{rel_path}: expected {extension} file")

    return errors


def schema_errors(path: Path, record: dict[str, Any], validator: Draft202012Validator) -> list[str]:
    errors: list[str] = []
    for error in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        errors.append(f"{relative(path)}:{location}: {error.message}")
    return errors


def validate_record_paths(path: Path, record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rel_path = relative(path)
    record_date, date_errors = parse_date(record.get("date"), f"{rel_path}:date")
    errors.extend(date_errors)
    if record_date is None:
        return errors

    expected_data_path = Path("data") / f"{record_date:%Y}" / f"{record_date.isoformat()}.json"
    expected_markdown_path = (
        Path("radars") / f"{record_date:%Y}" / f"{record_date.isoformat()}.md"
    )

    if path.relative_to(REPO_ROOT) != expected_data_path:
        errors.append(f"{rel_path}: record date expects {expected_data_path.as_posix()}")

    markdown_path = record.get("markdown_path")
    if markdown_path != expected_markdown_path.as_posix():
        errors.append(
            f"{rel_path}: markdown_path must be {expected_markdown_path.as_posix()}"
        )

    markdown_file = REPO_ROOT / expected_markdown_path
    if not markdown_file.exists():
        errors.append(f"{rel_path}: missing matching {expected_markdown_path.as_posix()}")

    raw_markdown = record.get("raw_markdown")
    if isinstance(raw_markdown, str) and markdown_file.exists():
        current_markdown = markdown_file.read_text(encoding="utf-8").strip() + "\n"
        if raw_markdown.strip() + "\n" != current_markdown:
            errors.append(f"{rel_path}: raw_markdown does not match {relative(markdown_file)}")

    return errors


def validate_theme_references(path: Path, record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    record_theme_values = record.get("themes", [])
    if not isinstance(record_theme_values, list):
        return errors
    record_themes = {theme for theme in record_theme_values if isinstance(theme, str)}

    for collection_name in ("signals", "ideas"):
        collection = record.get(collection_name, [])
        if not isinstance(collection, list):
            continue
        for index, item in enumerate(collection):
            if not isinstance(item, dict):
                continue
            item_themes = item.get("themes", [])
            if not isinstance(item_themes, list):
                continue
            item_theme_values = {theme for theme in item_themes if isinstance(theme, str)}
            unknown = sorted(item_theme_values - record_themes)
            if unknown:
                errors.append(
                    f"{relative(path)}:{collection_name}[{index}]: "
                    f"themes not listed at record level: {', '.join(unknown)}"
                )

    return errors


def validate_radar_pairs(data_by_date: dict[str, Path]) -> list[str]:
    errors: list[str] = []
    for path in radar_paths():
        errors.extend(validate_file_shape(path, RADARS_ROOT, ".md"))
        parsed, date_errors = parse_date(path.stem, relative(path))
        errors.extend(date_errors)
        if parsed is None:
            continue
        expected = Path("data") / f"{parsed:%Y}" / f"{parsed.isoformat()}.json"
        if parsed.isoformat() not in data_by_date:
            errors.append(f"{relative(path)}: missing matching {expected.as_posix()}")
    return errors


def validate_indexes(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for relative_path, expected_content in build_index_outputs(records).items():
        path = REPO_ROOT / relative_path
        if not path.exists():
            errors.append(f"{relative_path.as_posix()}: missing derived index output")
            continue
        actual_content = path.read_text(encoding="utf-8")
        if actual_content != expected_content:
            errors.append(
                f"{relative_path.as_posix()}: stale derived output; "
                "run `uv run python scripts/update_indexes.py`"
            )
    return errors


def validate() -> list[str]:
    schema_payload = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema_payload)
    validator = Draft202012Validator(schema_payload, format_checker=FormatChecker())

    errors: list[str] = []
    records: list[dict[str, Any]] = []
    data_by_date: dict[str, Path] = {}

    for path in data_paths():
        errors.extend(validate_file_shape(path, DATA_ROOT, ".json"))
        record, json_errors = load_json(path)
        errors.extend(json_errors)
        if record is None:
            continue

        errors.extend(schema_errors(path, record, validator))
        errors.extend(validate_record_paths(path, record))
        errors.extend(validate_theme_references(path, record))

        record_date = record.get("date")
        if isinstance(record_date, str):
            if record_date in data_by_date:
                errors.append(
                    f"{relative(path)}: duplicate radar date also found in "
                    f"{relative(data_by_date[record_date])}"
                )
            data_by_date[record_date] = path

        records.append(record)

    errors.extend(validate_radar_pairs(data_by_date))
    errors.extend(validate_indexes(records))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Content validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Content validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
