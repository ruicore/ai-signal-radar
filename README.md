# ai-signal-radar

`ai-signal-radar` is Ray's reviewed, multi-track AI signal repository. Its
primary reader is future Codex and AI agents that need durable context for
product ideas, engineering directions, creation patterns, and recurring
signals.

This is not a news archive. Reports become canonical only after Ray reviews
them. The repository currently has two independent but cross-searchable tracks:

- `systems`: AI systems engineering, agent runtimes, infrastructure, security,
  evaluation, and operational architecture.
- `creation`: AI-native products and works that create a meaningful new human
  behavior, medium, personal tool, learning experience, or cultural form.

The repository name remains intentionally broad: both tracks are AI signals,
and the shared repository makes cross-track patterns retrievable without
collapsing their evidence standards or schemas into one research lens.

## Canonical paths

Each record is uniquely identified by `radar_type + date`:

```text
radars/<track>/YYYY/YYYY-MM-DD.md
data/<track>/YYYY/YYYY-MM-DD.json
```

The Markdown file preserves the approved report. The JSON file contains the
durable, agent-friendly extraction. Prefer structured JSON for retrieval, then
the approved Markdown, then derived indexes and theme views.

Creation records additionally preserve an observation window. Their signals
may carry domain, creator, evidence level, what was created, what AI changed,
the resulting human behavior, and a transferable idea. Creation patterns are
stored separately from individual cases so they can recur across reports.

## Human-reviewed ingestion flow

1. ChatGPT generates a radar report outside this repository.
2. Ray reviews and approves it.
3. Codex stores the approved Markdown under its explicit track.
4. Codex extracts structured JSON conforming to `schemas/radar.schema.json`.
5. Codex regenerates indexes and the aggregate theme view.
6. Codex validates schema, paths, pairings, theme references, and deterministic
   outputs before committing.

The track must never be inferred from a vague title when ingestion intent is
unclear. Creation reports require explicit observation-window start and end
dates. Missing evidence stays missing; it must not be upgraded or fabricated.

## Creation admission standard

A Creation Radar case should normally meet all three conditions:

- the work or product is accessible enough to inspect;
- the changed human behavior can be explained;
- the constraint changed by AI is explicit.

Volume, speed, or an AI label alone is insufficient. Record evidence levels
faithfully, distinguish creator/vendor claims from first-hand checks, and do
not treat a generated draft or press article as proof of live-product behavior.

## Derived navigation

- `indexes/radars.json`: all reviewed records, ordered by date and track.
- `indexes/tracks.json`: per-track record navigation.
- `indexes/themes.json`: cross-track theme occurrences with track provenance.
- `indexes/summary.json`: repository and per-track counts.
- `themes/README.md`: generated cross-track theme navigation.
- `themes/<track>/`: curated track-specific theme definitions and recurring
  judgments.
- `ideas/`: ideas promoted from recurring signals or explicit report takeaways.

Derived files must be regenerated rather than manually reconciled:

```bash
uv run python scripts/update_indexes.py
```

## Monthly reviews

Monthly reviews are deterministic review aids generated from canonical JSON:

```text
reports/monthly/<track>/YYYY-MM.md
```

Run one track locally with:

```bash
uv run python scripts/generate_monthly_review.py YYYY-MM --track systems
uv run python scripts/generate_monthly_review.py YYYY-MM --track creation
```

## Repository layout

- `radars/`: approved source reports, partitioned by track.
- `data/`: structured records, partitioned by track.
- `themes/`: generated cross-track navigation and curated track definitions.
- `ideas/`: promoted product and project ideas.
- `indexes/`: deterministic machine-readable navigation.
- `reports/`: deterministic monthly and future period reviews.
- `inbox/`: temporary staging for approved reports.
- `scripts/`: ingestion, indexing, rendering, review, and validation tools.
- `schemas/`: the multi-track content contract.
- `prompts/`: agent instructions for repeatable ingestion.

## Validation contract

CI and local validation use:

```bash
uv sync
uv run ruff check .
uv run pytest
uv run python scripts/validate_content.py
uv run python scripts/update_indexes.py
git diff --exit-code
```

The validator requires every Markdown report and JSON record to form a matching
track/date pair, every nested theme reference to exist at record level, and all
derived outputs to match the deterministic generators.
