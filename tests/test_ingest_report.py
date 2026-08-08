from __future__ import annotations

from datetime import date

import pytest

from scripts.ingest_report import extract_sections, record_from_markdown


def test_extract_sections_from_markdown_headings() -> None:
    markdown = "# Weekly Radar\n\n## Agents\n\nAgent tooling matured.\n\n## Evals\n\nMore evals."

    assert extract_sections(markdown) == [
        {"title": "Agents", "summary": "Agent tooling matured."},
        {"title": "Evals", "summary": "More evals."},
    ]


def test_record_requires_reviewed_status_and_paths() -> None:
    markdown = "# Weekly Radar\n\n## Agents\n\nAgent tooling matured."

    record = record_from_markdown(
        radar_type="systems",
        report_date=date(2026, 6, 15),
        markdown=markdown,
        title=None,
        themes=["agents", "agents", "evals"],
        source_file=None,
    )

    assert record["title"] == "Weekly Radar"
    assert record["schema_version"] == "2.0"
    assert record["radar_type"] == "systems"
    assert record["status"] == "reviewed"
    assert record["themes"] == ["agents", "evals"]
    assert record["markdown_path"] == "radars/systems/2026/2026-06-15.md"
    assert record["source"] == {
        "generator": "ChatGPT",
        "reviewed_before_ingestion": True,
    }


def test_creation_record_requires_and_preserves_observation_window() -> None:
    record = record_from_markdown(
        radar_type="creation",
        report_date=date(2026, 8, 5),
        markdown="# AI Native Creation Radar\n",
        title=None,
        themes=["personal-software"],
        source_file=None,
        window_start=date(2026, 7, 30),
        window_end=date(2026, 8, 5),
    )

    assert record["observation_window"] == {"start": "2026-07-30", "end": "2026-08-05"}
    assert record["markdown_path"] == "radars/creation/2026/2026-08-05.md"


def test_creation_record_rejects_missing_observation_window() -> None:
    with pytest.raises(ValueError, match="require an observation window"):
        record_from_markdown(
            radar_type="creation",
            report_date=date(2026, 8, 5),
            markdown="# AI Native Creation Radar\n",
            title=None,
            themes=[],
            source_file=None,
        )
