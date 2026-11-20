# Observed project status

- Snapshot date: 2026-11-20.
- Product: Georgian-first beginner electronics workspace with scoped interactive wiring validation.
- GitHub baseline is published on `main`. The original starter governance task `BOOT-001` was not run as a separate task.
- P1 / CORE-001A: IMPLEMENTED and independently audited with restrictions. Deterministic connectivity is available for reviewed catalogs and validated snapshots. The independent audit is on `codex/core-001a-acceptance-audit`.
- CORE-001A-R1: PARTIAL at that checkpoint. The research conformance audit reproduced the mapping-kind false positive and requested a schema decision. See the [R1 execution report](../reports/CORE-001A-R1-REPORT.md) and [research conformance audit](../reports/CORE-001A-RESEARCH_CONFORMANCE_AUDIT.md).
- CORE-001A-R2: Implemented owner-selected Option A1 as catalog v1.1 with typed mapping evidence. Legacy v1.0 topology remains readable and its resolved mappings are unknown for typed evidence. See the [R2 execution report](../reports/CORE-001A-R2-REPORT.md) for verification.
- P2 headless evaluator: NOT_STARTED.
- P3 2D editor: NOT_STARTED.
- P4 physics adapter: NOT_STARTED.
- P5 lesson UX testing: NOT_STARTED.
- P6 demo: NOT_STARTED.
- Installed CORE-001A dependencies are pinned and recorded in the OSS register for review. Distribution clearance remains pending.
- Positive GPIO findings require a separately reviewed catalog pin and typed v1.1 evidence. Formal decision documentation, serializer validation, finding vocabulary, electrical model scope and UI framework remain open. ADR-0002 remains PROPOSED / HOLD. CORE-001B and CORE-001C have no execution authorization.

Only an explicitly authorized task may update this document, with factual results. Task reports are evidence, not automatic approvals.
