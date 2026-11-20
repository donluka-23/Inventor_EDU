# Implementation work log — append-only

## 2026-11-20 — starter package created
- Added the new repository's instructions, scope, evidence-gated roadmap, model-selection research task and OSS intake records.
- No application code, physical simulator, model data library or test suite was implemented.
- First active task: P1-001.

Format for further entries: date; task ID; observable changes; test commands/outputs; decisions; remaining risks; links to commit/PR; next task.

## 2026-11-20 — CORE-001A-R1
- Audited CORE-001A against Research A and the approved amendments. Verified the pinned connectivity suite and reproduced a mapping-kind false positive in memory.
- Added regression coverage for v1 evidence checks and catalog source-revision binding. See [R1 execution report](../reports/CORE-001A-R1-REPORT.md) for commands, results and Git verification, and [conformance audit](../reports/CORE-001A-RESEARCH_CONFORMANCE_AUDIT.md) for the traceability matrix.
- Reconciled project tracking and OSS metadata. R1 is PARTIAL pending an owner-approved persistence and provenance decision. No follow-up implementation was authorized.

## 2026-11-20 — CORE-001A-R2
- Applied the owner-selected Option A1. Catalog v1.1 binds verified mappings to typed contact, kind and target evidence. Legacy catalogs retain persisted bytes and resolve mapping authority as unknown.
- Verified migration fixtures, old and new digests, and stable connectivity with the pinned suite. See the [R2 execution report](../reports/CORE-001A-R2-REPORT.md) for commands, counts and publication evidence.
- Owner review remains pending. B and C need separate authorization. External catalog trust, serializer validation and finding vocabulary remain distinct concerns.

## 2026-11-20 — DATA-001
- Pinned and parsed authentic CC0 LibrePCB generic resistor records. Generated a v1.1 catalog and verified separate pads, explicit wiring and deterministic replay.
- Ran 29 tests with authentic source files present. Documented exact YAGEO source facts separately and held manufacturer-specific admission pending an exact footprint/contact match and independent review.
- See the [execution report](../reports/DATA-001-REPORT.md) and [source ledger](../reports/DATA-001_SOURCE_AND_EVIDENCE_LEDGER.md). Outcome PARTIAL. Follow-up work requires separate authorization.

## 2026-11-20 — CORE-001B-01
- Added bounded deterministic GPIO checks over CORE-001A-R2 topology and typed evidence. Published separate fact and catalog pins for the documented test-only -32E profile.
- Authentic GPIO sources passed explicit admission. The missing-source control failed as required. Full discovery passed 44 methods, including the authentic DATA-001 cases.
- See the [execution report](../reports/CORE-001B-01-REPORT.md) and [source and rule ledger](../reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md). Outcome PASS in the test scope. Deployment trust and physical hardware validation remain separate.

## 2026-11-20 — DEMO-001
- Preserved the owner-frozen prototype plan and implemented the scoped HCSR04 bridge from canonical nets to real GPIO checks.
- Authentic GPIO source admission passed. Full discovery passed 54 tests, including the authentic DATA-001 tests. The wrong Trig contact failed and the corrected contact passed physical capability. Electrical compatibility stayed delegated.
- See the [execution report](../reports/DEMO-001-REPORT.md). No interactive acceptance, hardware testing or later milestone authorization was established.

## 2026-11-20 — SYN-001

- Generated reviewed two-role physical assignments through real CORE topology and GPIO verification. Observed two hard rejections and one incomplete alternative in the reviewed fixture.
- S01–S18 and all 72 discovered regression tests passed. Separate authentic GPIO source admission passed. See the [execution report](../reports/SYN-001-REPORT.md) for counts, uncertainty and reproducible traces. Owner review is pending.
