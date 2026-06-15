from __future__ import annotations

from datetime import date

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
        report_date=date(2026, 6, 15),
        markdown=markdown,
        title=None,
        themes=["agents", "agents", "evals"],
        source_file=None,
    )

    assert record["title"] == "Weekly Radar"
    assert record["status"] == "reviewed"
    assert record["themes"] == ["agents", "evals"]
    assert record["markdown_path"] == "radars/2026/2026-06-15.md"
    assert record["source"] == {
        "generator": "ChatGPT",
        "reviewed_before_ingestion": True,
    }
