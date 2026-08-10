# ai-security

## Summary

Security boundaries for AI systems, including scoped credentials, sandboxing, review gates, audit logs, threat detection, and secret handling.

## Related Reports

- 2026-06-15: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-06-15.md)
- 2026-06-29: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-06-29.md)
- 2026-08-07: [AI Agent 生态与社区创造周报](../../radars/systems/2026/2026-08-07.md)
- 2026-08-09: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-08-09.md)

## Notable Recurring Signals

- Higher-capability agents are increasing the need for scoped credentials, evidence-backed actions, confirmation gates, validation, and auditable security boundaries.
- Runtime writes and agent-generated patches need deterministic approval, lint, authorization, and audit boundaries outside the model prompt.
- Agent authorization is becoming history-aware: temporal prerequisites, accumulated exposure, request-based limits, and capability ratchets require durable state and atomic tool-execution boundaries.
