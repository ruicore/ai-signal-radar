from __future__ import annotations

from datetime import date

from scripts.generate_monthly_review import previous_month, render


def test_previous_month_rolls_back_across_year_boundary() -> None:
    assert previous_month(date(2026, 1, 1)) == "2025-12"


def test_render_monthly_review_from_records_and_indexes() -> None:
    records = [
        {
            "date": "2026-06-15",
            "title": "Weekly Radar",
            "themes": ["agent-runtime", "coding-agents"],
            "markdown_path": "radars/2026/2026-06-15.md",
            "signals": [
                {
                    "title": "Remote agents need workspaces",
                    "summary": "Persistent workspace substrate matters.",
                    "themes": ["agent-runtime"],
                }
            ],
            "ideas": [
                {
                    "title": "Workspace Contract",
                    "summary": "Define the minimal runtime contract.",
                    "themes": ["agent-runtime", "coding-agents"],
                }
            ],
        }
    ]
    indexes = {"summary": {"weekly_radar_count": 1, "signal_count": 1, "idea_count": 1}}

    output = render("2026-06", records, indexes)

    assert "# Monthly AI Signal Review: 2026-06" in output
    assert "- Reviewed weekly radars: 1" in output
    assert "- 2026-06-15: [Weekly Radar](../../radars/2026/2026-06-15.md)" in output
    assert "- 2026-06-15 / Remote agents need workspaces (agent-runtime)" in output
    assert "- 2026-06-15 / Workspace Contract (agent-runtime, coding-agents)" in output
