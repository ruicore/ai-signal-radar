from __future__ import annotations

from scripts.render_markdown import render


def test_render_prefers_raw_markdown() -> None:
    record = {"raw_markdown": "# Approved\n\nBody.\n"}

    assert render(record) == "# Approved\n\nBody.\n"


def test_render_structured_record() -> None:
    record = {
        "date": "2026-06-15",
        "title": "Weekly Radar",
        "themes": ["agents"],
        "signals": [{"title": "Agent Tooling", "summary": "Tooling improved."}],
        "ideas": [],
    }

    output = render(record)

    assert "# Weekly Radar" in output
    assert "- agents" in output
    assert "### Agent Tooling" in output

