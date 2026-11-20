# INVENTOR EDU prototype master plan

## Plan metadata

- Plan ID: `INVENTOR-EDU-PROTOTYPE`
- Plan version: `1.0`
- State: `OWNER-FROZEN`
- Primary concept: `BOUNDED_GOAL_TO_CIRCUIT`
- First lesson: `HCSR04_GPIO_WIRING`
- Architecture authority: `OWNER_AND_RESEARCH_CONVERSATION`
- Execution authority: `CODEX_SINGLE_TASK_ONLY`

## Milestone table

| ID | Deliverable | Required gate | State at plan creation |
|---|---|---|---|
| DEMO-001 | Headless scenario-to-verification bridge | Real net-derived GPIO requests and correct scoped findings | AUTHORIZED |
| DEMO-002 | Owner-approved frontend technology and UX contract | UI architecture, OSS rights and event semantics approved outside Codex | PLANNED / NOT_AUTHORIZED |
| DEMO-003 | Minimal interactive 2D wiring editor | Physical terminal events, wire changes, topology invariance, undo/redo | PLANNED / NOT_AUTHORIZED |
| DEMO-004 | Frontend-to-verifier integration and Georgian feedback | No UI-hardcoded findings, stale finding removal, evidence anchors | PLANNED / NOT_AUTHORIZED |
| DEMO-005 | Bounded Georgian goal interpretation and project setup | Deterministic requirements, explicit ambiguity and reproducibility | PLANNED / NOT_AUTHORIZED |
| CORE-001C | Source-backed bounded electrical verification | Independently approved numeric facts, conditions and oracles | PLANNED / NOT_AUTHORIZED |
| DEMO-006 | Complete demo acceptance and pilot evidence | Existing DEMO.md conditions, independent testing and actual users | PLANNED / NOT_AUTHORIZED |

Milestone IDs are planning references, not execution permissions.

CORE-001C may be scheduled independently if its approved evidence and prerequisites become available.

The project must not claim complete `docs/DEMO.md` acceptance before the real voltage-case requirement has been satisfied.

## Fixed non-goals

- General-purpose Wokwi clone.
- MCU firmware emulator.
- General SPICE simulation engine.
- Universal electronics component ontology.
- Arbitrary natural-language circuit generation.
- LLM-generated engineering safety verdicts.
- Mass datasheet scraping.
- Full classroom management system.
- Subscription/payment infrastructure.
- Marketplace.
- Unlimited component catalog.
- Unlicensed Wokwi assets or proprietary simulator embedding.

## Deferred opportunity register

Record these opportunities without implementation authorization:

**OPP-01 — Wokwi-compatible project import.** Revisit if actual pilot users demand project interoperability and the exact format/rights can be verified.

**OPP-02 — Wokwi Elements or another OSS visual renderer.** Revisit during DEMO-002 only after exact repository, dependency, asset and license review.

**OPP-03 — LLM-assisted Georgian intent parsing.** Revisit after deterministic task coverage and measured parser failures justify recurring API cost.

**OPP-04 — Expanded component acquisition.** Revisit after an additional component family shows measurable reuse benefit and source review capacity.

**OPP-05 — Controlled evidence acquisition automation.** Revisit when actual curation volume and source-revision failures justify it. No automatic trust promotion.

**OPP-06 — Educational analytics/adaptive feedback.** Revisit after baseline usability and learning outcomes have been measured.

**OPP-07 — Classroom, reseller or B2B commercial features.** Revisit after actual customer interviews and documented budget signals.

**OPP-08 — Additional simulation engines.** Revisit only for a defined physics/firmware job not met by existing verified methods, with scientific and license approval.

## Risks that must not disappear

Record:

- Exact physical hardware revision may remain unverified.
- Retailer sensor identity is not proof of OEM electrical characteristics.
- GPIO direction PASS is not full board availability PASS.
- A correct digest is not proof of an externally trusted source.
- User-supplied expected hashes cannot establish their own provenance.
- Required rule completeness must not be delegated to arbitrary UI callers.
- Missing electrical facts must remain UNKNOWN or NOT_EVALUATED.
- A specific GPIO fix does not imply whole-project correctness.
- Frontend geometry must not alter electrical topology.
- User-displayed pin labels cannot replace canonical physical terminal IDs.
- The prototype must remain extensible beyond ESP32 and HC-SR04.
- Commercial demand and educational superiority remain unverified.
- The current main branch does not represent the latest accepted task-branch implementation history.

## Change control

This document must not be changed merely because Codex finds a convenient alternative.

For a proposed change, record in the task report:

- `CHANGE_REQUEST_ID`
- affected milestone/requirement;
- observed contradiction or new evidence;
- existing decision;
- proposed alternative;
- compatibility impact;
- engineering and licensing implications;
- test impact;
- decision requested from the owner.

Do not implement the proposal until a new owner-authorized task is issued.

Do not append invented future milestones.

Only an explicit future owner-approved plan revision may change this master plan.
