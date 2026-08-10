# observability

## Summary

Observability for AI and agent systems, including traces, tool-call metrics, latency, error rates, health signals, audit trails, and operational dashboards.

## Related Reports

- 2026-06-15: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-06-15.md)
- 2026-06-29: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-06-29.md)
- 2026-08-07: [AI Agent 生态与社区创造周报](../../radars/systems/2026/2026-08-07.md)
- 2026-08-09: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-08-09.md)

## Notable Recurring Signals

- Agent observability needs to capture tool calls, tenant or workspace context, latency, errors, spend, audit trails, and task outcome telemetry.
- Useful coding-agent telemetry is moving toward runtime identity, per-turn trajectories, tool use, API-equivalent cost, and validation outcomes.
- LLM serving traces need to correlate logical requests and scheduler batches with host launches, CUDA kernels, collectives, and logs before learned diagnosis is applied.
