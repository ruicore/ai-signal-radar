from __future__ import annotations

from datetime import date

from scripts.generate_monthly_review import previous_month, render


def test_previous_month_rolls_back_across_year_boundary() -> None:
    assert previous_month(date(2026, 1, 1)) == "2025-12"


def test_render_monthly_review_from_records_and_indexes() -> None:
    records = [
        {
            "date": "2026-06-15",
            "radar_type": "systems",
            "title": "Weekly Radar",
            "themes": ["agent-runtime", "coding-agents"],
            "markdown_path": "radars/systems/2026/2026-06-15.md",
            "signals": [
                {
                    "title": "Remote agents need workspaces",
                    "summary": "Persistent workspace substrate matters.",
                    "themes": ["agent-runtime"],
                }
            ],
            "patterns": [
                {
                    "title": "Durable Agent Work",
                    "summary": "Agent work persists across sessions.",
                    "outlook": "Likely to recur.",
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
    indexes = {
        "summary": {
            "radar_count": 1,
            "radar_counts": {"systems": 1},
            "signal_count": 1,
            "idea_count": 1,
        }
    }

    output = render("2026-06", records, "systems", indexes)

    assert "# Monthly AI Signal Review: systems / 2026-06" in output
    assert "- Reviewed radars: 1" in output
    assert "- Patterns captured: 1" in output
    assert "- 2026-06-15: [Weekly Radar](../../../radars/systems/2026/2026-06-15.md)" in output
    assert "- 2026-06-15 / Remote agents need workspaces (agent-runtime)" in output
    assert "- 2026-06-15 / Durable Agent Work (agent-runtime)" in output
    assert "- 2026-06-15 / Workspace Contract (agent-runtime, coding-agents)" in output
