# Reviewed Radar Ingestion Instruction

You are helping Ray maintain `ai-signal-radar`, a reviewed multi-track AI signal
repository for future Codex and AI agents.

## Non-negotiables

- Do not ingest unreviewed reports.
- Confirm Ray approved the report before treating it as canonical.
- Do not call the OpenAI API or generate a replacement report.
- Select an explicit `systems` or `creation` track.
- Preserve approved text in `radars/<track>/YYYY/YYYY-MM-DD.md`.
- Create structured JSON in `data/<track>/YYYY/YYYY-MM-DD.json`.
- Creation records require observation-window start and end dates.
- Preserve evidence levels and distinguish first-hand checks, real products,
  creator claims, vendor claims, and secondary reporting.
- Update indexes and derived theme navigation after ingestion.

## Expected flow

1. Receive Ray's approved report.
2. Determine its track, canonical date, and (for creation) observation window.
3. Preserve the approved Markdown without substantive rewriting.
4. Extract only supported, durable fields into `schemas/radar.schema.json`.
5. Add new explicit themes under `themes/<track>/` when genuinely needed.
6. Run `uv run python scripts/update_indexes.py`.
7. Run ruff, pytest, and `scripts/validate_content.py`.
8. Commit and push only when authorized.

## Creation extraction

For each qualifying case, preserve the title and concise summary. When the
report supports them, also extract:

- domain and creator;
- evidence level and source links;
- what was created;
- what AI changed;
- the new human behavior;
- the transferable idea.

Store recurring creation forms in `patterns`; do not inflate production volume
or generation speed into a pattern without a durable behavior change.

## Agent reading priority

1. `data/` JSON for structured retrieval.
2. `indexes/` for aggregate and per-track navigation.
3. `themes/` for recurring patterns and definitions.
4. `radars/` for the original reviewed reasoning and caveats.
