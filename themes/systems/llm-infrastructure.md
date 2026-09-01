# llm-infrastructure

## Summary

Infrastructure for LLM-powered systems, including inference substrate, agent execution platforms, orchestration, cost controls, and workload-level scaling.

## Related Reports

- 2026-06-15: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-06-15.md)
- 2026-06-29: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-06-29.md)
- 2026-08-09: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-08-09.md)
- 2026-08-23: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-08-23.md)
- 2026-08-30: [AI Systems Engineering 技术雷达（高信号版）](../../radars/systems/2026/2026-08-30.md)

## Notable Recurring Signals

- LLM infrastructure for agents is broadening from inference to execution substrate, isolation, policy, tool access, workload evaluation, and cost controls.
- Realtime inference, shared environment services, request-to-kernel tracing, and compiler-gated optimization are emerging as distinct infrastructure layers around model serving.
- Inference routers increasingly trade off queue load, prefix and KV locality,
  session affinity, tenant namespace, topology, latency class, and cost.
- Schedulers are beginning to consume power, thermal, cooling, and facility events
  alongside compute and queue state; static production artifacts can also keep
  model calls out of deterministic runtime paths.
- Hardware selection increasingly depends on model-specific compiler, kernel,
  memory, interconnect, serving, power, and portability trade-offs.
