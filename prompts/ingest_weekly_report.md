# Weekly Radar Ingestion Instruction

You are helping Ray maintain `ai-signal-radar`, a reviewed personal AI systems
engineering signal repository for future Codex and AI agents.

## Non-negotiables

- Do not ingest unreviewed reports.
- Confirm Ray has approved the weekly report before treating it as canonical.
- Do not call the OpenAI API.
- Do not generate a report automatically.
- Preserve the approved report text in `radars/YYYY/YYYY-MM-DD.md`.
- Create structured JSON in `data/YYYY/YYYY-MM-DD.json`.
- Update indexes and derived theme views after ingestion.

## Expected flow

1. Receive Ray's approved weekly ChatGPT report.
2. Determine the report date. If missing, ask Ray before writing files.
3. Save the reviewed Markdown report to `radars/YYYY/YYYY-MM-DD.md`.
4. Extract durable, agent-friendly structure into `data/YYYY/YYYY-MM-DD.json`:
   - title
   - reviewed status
   - themes
   - signals
   - ideas
   - source metadata
5. Run `uv run python scripts/update_indexes.py`.
6. Run validation:
   - `uv run ruff check .`
   - `uv run pytest`
7. Commit and push only after Ray confirms the diff.

## Agent reading priority

When using this repository as context, prefer:

1. `data/` JSON files for structured retrieval.
2. `indexes/` for aggregate navigation.
3. `themes/` for recurring patterns.
4. `radars/` for original reviewed prose.

