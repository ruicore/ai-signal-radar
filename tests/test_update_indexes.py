from __future__ import annotations

from scripts.update_indexes import build_radar_index, build_summary, build_track_index


def test_same_date_can_exist_in_independent_tracks() -> None:
    records = [
        {
            "radar_type": "systems",
            "date": "2026-08-05",
            "title": "Systems",
            "themes": ["agent-runtime"],
            "signals": [],
            "ideas": [],
            "markdown_path": "radars/systems/2026/2026-08-05.md",
        },
        {
            "radar_type": "creation",
            "date": "2026-08-05",
            "title": "Creation",
            "themes": ["personal-software"],
            "signals": [],
            "patterns": [],
            "ideas": [],
            "markdown_path": "radars/creation/2026/2026-08-05.md",
        },
    ]

    assert len(build_radar_index(records)) == 2
    assert set(build_track_index(records)) == {"creation", "systems"}
    assert build_summary(records)["radar_counts"] == {"creation": 1, "systems": 1}
