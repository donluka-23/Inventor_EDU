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
