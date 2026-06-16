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

## Weekly operation flow

1. ChatGPT generates a weekly radar report.
2. Ray reviews and approves the report.
3. Ray pastes the approved report to Codex.
4. Codex ingests it into `radars/YYYY/YYYY-MM-DD.md` and
   `data/YYYY/YYYY-MM-DD.json`.
5. Codex updates indexes and themes with `scripts/update_indexes.py`.
6. Codex validates the content contract with `scripts/validate_content.py`.
7. Codex commits and pushes the reviewed update.

Weekly ingestion remains human-in-the-loop. Automation may validate, index, and
summarize reviewed records, but it should not decide which weekly report becomes
canonical repository data.

## What Ray should do every week

1. Generate the weekly radar report outside this repository.
2. Review the report for judgment, priority, and wording.
3. Only after approval, give the final reviewed report to Codex for ingestion.
4. Confirm the proposed date, title, themes, and generated file paths.
5. Let Codex run validation, update derived indexes, and commit the reviewed
   ingestion.

Ray does not need to manually edit indexes, theme navigation, or monthly review
scaffolds during normal weekly operation.

## Monthly review flow

The scheduled monthly workflow runs on the first day of each month and generates
the previous UTC month by default. It can also be run manually for a specific
`YYYY-MM` value.

Monthly reviews are written to:

```text
reports/monthly/YYYY-MM.md
```

The monthly review generator is deterministic and uses only reviewed JSON data
and repository indexes. It does not call the OpenAI API and does not replace
Ray's weekly review step. Its output is a review aid: counts, links, theme
frequency, signal titles, and idea titles from existing repository data.

Run it locally with:

```bash
uv run python scripts/generate_monthly_review.py YYYY-MM
```

## CI validation contract

CI protects the repository contract on every push and pull request:

- `uv run ruff check .`
- `uv run pytest`
- `uv run python scripts/validate_content.py`
- `uv run python scripts/update_indexes.py`
- `git diff --exit-code`

The content validator enforces these rules:

- Every `data/YYYY/*.json` record must validate against
  `schemas/weekly_radar.schema.json`.
- Every data record must point to its matching
  `radars/YYYY/YYYY-MM-DD.md` file.
- Every radar Markdown file must have a matching data JSON file.
- Signal and idea theme references must be present in the record-level themes.
- Derived indexes and `themes/README.md` must match the deterministic output of
  `scripts/update_indexes.py`.

If running `scripts/update_indexes.py` changes the working tree, CI fails until
the regenerated files are committed.

## Repository layout

- `radars/`: reviewed weekly radar reports in Markdown.
- `data/`: structured JSON records derived from reviewed weekly reports.
- `themes/`: derived theme views and theme notes.
- `ideas/`: product and project ideas promoted from recurring signals.
- `indexes/`: searchable indexes for agents.
- `reports/`: deterministic monthly and future period-review outputs.
- `inbox/`: temporary staging area for approved reports before ingestion.
- `scripts/`: local maintenance scripts.
- `schemas/`: JSON schemas for structured records.
- `prompts/`: agent instructions for repeatable workflows.

## Local validation

```bash
uv sync
uv run ruff check .
uv run pytest
uv run python scripts/validate_content.py
uv run python scripts/update_indexes.py
```
