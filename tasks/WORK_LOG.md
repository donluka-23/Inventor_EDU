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

## 2026-11-20 — CAP-001

- Archived all four owner-provided Research F–I files byte-for-byte in one dedicated commit.
- Discovered physical GPIO contacts through the existing catalog and verifier. The discovered domains drove the existing SYN-001 generator, which evaluated 20 assignments.
- All 89 regression tests and the separate authentic GPIO source gate passed. See the [execution report](../reports/CAP-001-REPORT.md). Owner review is pending.

## 2026-11-20 — EDU-001

- Replayed the real CAP/SYN/CORE correction cycle, withdrew the prior GPIO34 hint, and preserved the remaining board, firmware, electrical and separate boot uncertainties.
- Engineering and replay gates passed. Overall outcome PARTIAL pending independent human review and owner approval of the Georgian preview wording. See the [execution report](../reports/EDU-001-REPORT.md).

## 2026-11-20 — CHAT-001

- Added the bounded local action controller and Georgian loopback forms. Exercised actual source inspection, recomputation, hint withdrawal and reset through HTTP form submissions.
- Preserved the EDU wording gate. The review packet has blank human-review fields. See the [execution report](../reports/CHAT-001-REPORT.md). Owner review is pending.

## 2026-11-20 — CORE-001C-E1

- Verified exact ideal DC divider equations, tolerance bounds and conditional HIGH margins. The existing two-component CORE snapshot serves only as a digest association.
- Preserved distinct unresolved hardware evidence and physics scopes. See the [execution report](../reports/CORE-001C-E1-REPORT.md). Owner review is pending.

## 2026-11-21 — CORE-001C-E2

- Admitted an in-memory composite catalog with exact reviewed source-context definitions and two synthetic resistor bodies. Verified the canonical motif, two independent wiring rejections and exact recovery after restoring a conductor.
- E1 math remains conditional, and actual component values and hardware compatibility remain unestablished. See the [execution report](../reports/CORE-001C-E2-REPORT.md). Owner review is pending.

## 2026-11-21 — EDU-T1

- Added the single independent GPIO input and electrical-scope item to the test-only loopback preview. Verified fresh CORE/B scoring, withholding of pre-answer evidence, and rejection of repeated and stale submissions.
- Georgian language review remains pending. See the [execution report](../reports/EDU-T1-REPORT.md). Owner review is pending.

## 2026-11-21 — DS-002B revision 2

- Tested the isolated component canvas with live Wokwi Elements, nominal V4 contact geometry, genuine pointer and keyboard wiring, and deterministic visual workspace interchange.
- Recorded PARTIAL_V4_ASSET_PENDING. The nominal board asset lacks exact WROOM-32E provenance. See the [execution report](../reports/DS-002B-REV2-REPORT.md) for browser evidence and open owner decisions.

## 2026-11-21 — DS-002B-R3

- Verified the exact 32E assembly in Espressif's pinned overview. Opaque callouts cover J2.8 and other hardware details. Recorded the source, rights and candidate findings as OWNER_DECISION_REQUIRED.
- Re-ran the R2 interaction baseline and targeted Python regressions. The gate stopped replacement rendering and geometry. See the [R3 report](../reports/DS-002B-R3-REPORT.md).
