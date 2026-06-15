# ai-signal-radar

`ai-signal-radar` is Ray's long-term personal AI systems engineering signal
repository. Its primary reader is future Codex and AI agents that need durable
context for product ideas, engineering directions, and recurring signals.

This is not a news archive. It is a reviewed personal signal repository.
Weekly ChatGPT-generated radar reports are approved by Ray before ingestion.
Only reviewed reports should become canonical repository data.

Codex should treat this repository as long-term context for future product and
project ideas. Prefer the structured JSON under `data/`, then the reviewed
Markdown under `radars/`, then derived indexes under `indexes/` and `themes/`.

## Human-in-the-loop flow

1. ChatGPT generates a weekly radar report.
2. Ray reviews and approves the report.
3. Ray pastes the approved report to Codex.
4. Codex ingests it into `radars/YYYY/YYYY-MM-DD.md` and
   `data/YYYY/YYYY-MM-DD.json`.
5. Codex updates indexes and themes.
6. Codex commits and pushes the reviewed update.

## Repository layout

- `radars/`: reviewed weekly radar reports in Markdown.
- `data/`: structured JSON records derived from reviewed weekly reports.
- `themes/`: derived theme views and theme notes.
- `ideas/`: product and project ideas promoted from recurring signals.
- `indexes/`: searchable indexes for agents.
- `inbox/`: temporary staging area for approved reports before ingestion.
- `scripts/`: local maintenance scripts.
- `schemas/`: JSON schemas for structured records.
- `prompts/`: agent instructions for repeatable workflows.

## Local validation

```bash
uv sync
uv run ruff check .
uv run pytest
```

