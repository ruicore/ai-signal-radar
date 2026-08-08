# Agent Contract

This repository is a human-reviewed, multi-track AI signal record. Treat the
checked-in content as durable research context, not as a general news archive.

## Track ownership

- `systems` owns AI systems engineering, infrastructure, runtime, security,
  evaluation, and architecture signals.
- `creation` owns AI-native works and products where an accessible artifact,
  explainable behavior change, and explicit AI-changed constraint justify
  inclusion.
- Keep the tracks distinct even when they share a date or theme. A canonical
  record key is `radar_type + date`.

## Ingestion rules

- Ingest only after Ray approves a report.
- Preserve the approved Markdown without substantive rewriting.
- Never fabricate a date, observation window, source, theme, evidence level,
  signal, pattern, or idea.
- Creation records require an explicit observation window.
- Do not upgrade a creator claim, vendor claim, secondary report, or generated
  draft into first-hand evidence.
- Store canonical pairs at `radars/<track>/YYYY/YYYY-MM-DD.md` and
  `data/<track>/YYYY/YYYY-MM-DD.json`.
- Conform structured data to `schemas/radar.schema.json`.

## Derived content

- Treat `indexes/*.json` and `themes/README.md` as generated outputs.
- Preserve curated definitions under `themes/<track>/` and update them
  additively when a report introduces a genuine recurring theme.
- Generate monthly reviews separately per track under
  `reports/monthly/<track>/`.

## Required validation

Before committing an ingestion or contract change, run:

```bash
uv run ruff check .
uv run pytest
uv run python scripts/validate_content.py
uv run python scripts/update_indexes.py
git diff --check
```

After regenerating indexes, confirm a second generator run produces no diff.
