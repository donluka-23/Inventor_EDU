# Observed project status

- Snapshot date: 2026-11-20.
- Product: Georgian-first beginner electronics workspace with scoped interactive wiring validation.
- GitHub baseline is published on `main`. The original starter governance task `BOOT-001` was not run as a separate task.
- P1 / CORE-001A: IMPLEMENTED and independently audited with restrictions. Deterministic connectivity is available for reviewed catalogs and validated snapshots. The independent audit is on `codex/core-001a-acceptance-audit`.
- CORE-001A-R1: PARTIAL at that checkpoint. The research conformance audit reproduced the mapping-kind false positive and requested a schema decision. See the [R1 execution report](../reports/CORE-001A-R1-REPORT.md) and [research conformance audit](../reports/CORE-001A-RESEARCH_CONFORMANCE_AUDIT.md).
- CORE-001A-R2: Implemented owner-selected Option A1 as catalog v1.1 with typed mapping evidence. Legacy v1.0 topology remains readable and its resolved mappings are unknown for typed evidence. See the [R2 execution report](../reports/CORE-001A-R2-REPORT.md) for verification.
- DATA-001: PARTIAL. Authentic pinned LibrePCB generic 0603 resistor structure imported into catalog v1.1, with two distinct contacts and deterministic topology. The exact YAGEO MPN-to-footprint relationship remains unverified and its manufacturer-specific catalog admission is on hold. See the [execution report](../reports/DATA-001-REPORT.md) and [source ledger](../reports/DATA-001_SOURCE_AND_EVIDENCE_LEDGER.md).
- P2 headless evaluator: CORE-001B-01 implemented and verified for bounded source-reviewed GPIO capability, flash reservation, and missing-context findings. [Execution report](../reports/CORE-001B-01-REPORT.md) and [source and rule ledger](../reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md). Production trust and hardware validation remain unestablished.
- P3 2D editor: NOT_STARTED.
- P4 physics adapter: NOT_STARTED.
- P5 lesson UX testing: NOT_STARTED.
- P6 demo: NOT_STARTED.
- DEMO-001: Headless HCSR04 GPIO wiring bridge implemented and verified in the test-only fixture scope. The [owner-frozen master plan](prototype/MASTER_PLAN.md) and [execution report](../reports/DEMO-001-REPORT.md) record the result. Interactive and electrical demo gates remain unmet.
- SYN-001: Bounded headless two-role candidate generation implemented. S01–S18 passed in the test-only scope. The GPIO18 Trig alternative passed direction and retained unresolved board availability, electrical and firmware checks. Owner acceptance is pending. See the [execution report](../reports/SYN-001-REPORT.md).
- CAP-001: Evidence-backed terminal discovery implemented in the test-only scope. Each role discovered five physical contacts. The existing SYN-001 engine evaluated 20 assignments with 11 known hard rejections and 9 alternatives with unresolved obligations. The four owner-provided Research F–I originals are tracked in a dedicated archival commit. Owner acceptance is pending. See the [execution report](../reports/CAP-001-REPORT.md).
- EDU-001: PARTIAL. The test-only headless correction cycle and engineering evidence gates passed. The Georgian wording remains a review preview pending independent human review and owner approval. See the [execution report](../reports/EDU-001-REPORT.md).
- CHAT-001: Local-only Georgian learning preview implemented. Loopback form submissions recompute the selected fixture assignment and replace obsolete feedback. Language review remains pending. See the [execution report](../reports/CHAT-001-REPORT.md) and [wording packet](reviews/EDU001_KA_WORDING_REVIEW_PACKET.md).
- CORE-001C-E1: Exact unloaded-divider mathematics and conditional HIGH margin verified in an isolated model. Hardware compatibility and physical divider provenance remain unestablished. See the [execution report](../reports/CORE-001C-E1-REPORT.md).
- CORE-001C-E2: The test-only virtual divider matches three canonical CORE nets and links the conditional E1 model. Two rewired cases withheld math, and restoring the wire recovered the original digests. Actual component values and hardware compatibility remain unestablished. See the [execution report](../reports/CORE-001C-E2-REPORT.md).
- Installed CORE-001A dependencies are pinned and recorded in the OSS register for review. Distribution clearance remains pending.
- Positive GPIO findings require independently reviewed catalog and fact-set pins and typed v1.1 mapping evidence. Formal decision documentation, serializer validation, electrical model scope and UI framework remain open. ADR-0002 remains PROPOSED / HOLD. CORE-001C is awaiting separate authorization.

Only an explicitly authorized task may update this document, with factual results. Task reports are evidence, not automatic approvals.
