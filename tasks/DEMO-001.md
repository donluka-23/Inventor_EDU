# INVENTOR EDU — DEMO-001
## Controlled Prototype Roadmap & Headless Scenario-to-Verification Bridge

**Task ID:** DEMO-001  
**Revision:** 1 — OWNER-FROZEN  
**Repository:** `D:\Inventor_EDU`  
**Remote:** `https://github.com/donluka-23/Inventor_EDU.git`  
**Authorized execution:** One task only  
**Task outcome:** A reproducible, headless integration connecting one physical sensor-wiring scenario to the existing GPIO verifier, plus a verbatim owner-approved prototype roadmap.

---

# 1. Authority boundary

You are an execution-only coding agent.

The owner and the separate architecture/research conversation have already made the product and engineering decisions for this task.

**Do not reinterpret Research F or Research G.**

Do not independently:

- choose the product direction;
- choose or revise the MVP scope;
- select the frontend framework;
- select OSS dependencies or licensing terms;
- redesign the canonical engineering model;
- choose new engineering algorithms;
- plan additional functionality;
- decide which research recommendations are important;
- revise the roadmap priorities;
- authorize the next milestone.

All relevant approved decisions are explicitly stated below.

Research F and G are supporting evidence, not instructions for Codex to generate a new strategy.

When an unresolved design decision prevents implementation, stop the affected work and report the exact decision required.

Do not silently substitute your preferred architecture.

---

# 2. Approved product direction

The target product is a Georgian-first educational engineering workspace.

The selected prototype concept is:

**Bounded Goal-to-Circuit.**

The full intended user journey is:

1. The learner describes or selects a supported project goal.
2. The system identifies its bounded engineering requirements.
3. An exact reviewed component profile is selected.
4. The learner edits physical connections in a 2D workspace.
5. The existing engineering engine evaluates applicable rules.
6. Findings identify exact physical terminals, nets and evidence.
7. Georgian guidance explains the error and corrective action.
8. The learner changes the circuit.
9. The system recomputes findings.
10. The outcome clearly distinguishes evaluated, unknown and unsupported properties.

The product must not claim full circuit simulation or physical safety without independent scientific evidence.

**DEMO-001 implements only the headless scenario-to-verification bridge.**

No frontend is authorized in this task.

---

# 3. Approved research decisions — do not reconsider

The following decisions have already been made by the architecture owner.

| Topic | Frozen decision |
|---|---|
| Product direction | Bounded Goal-to-Circuit |
| First board | Documented ESP32-DevKitC V4, orderable ESP32-DevKitC-32E |
| First sensor | Adafruit HC-SR04 product #3942, only within its reviewed evidence scope |
| First learning objective | Understand valid GPIO input/output capability and correct a physical connection |
| Existing topology | Reuse CORE-001A/R2 |
| Existing GPIO checks | Reuse CORE-001B-01 |
| Electrical computation | CORE-001C, separate future task |
| User intent interpretation | Explicit scenario selection in DEMO-001; Georgian parser later |
| AI | Not used in DEMO-001 |
| 2D editor | Required later; framework NOT selected |
| Wokwi simulation | No proprietary runtime integration |
| External data | Existing reviewed fixtures; no new importer |
| Verified facts | No invented hardware values or automatically promoted source claims |
| Commercial direction | Georgian private robotics academies are initial validation candidates, not confirmed buyers |

These decisions must not be changed while executing DEMO-001.

---

# 4. Persistent prototype plan

Create the file:

`docs/prototype/MASTER_PLAN.md`

This file is the owner-controlled, versioned development roadmap.

Use the following specification. Preserve its meaning and priority order without independently redesigning it.

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

---

# 5. Git baseline

Follow `AGENTS.md` and `docs/SESSION_PROTOCOL.md`.

Fetch the remote repository and inspect current local status.

The immediately preceding implementation branch is:

`origin/codex/core-001b-01-gpio-capability`

At handoff preparation, its HEAD was:

`0cdec11db446a6ea77ac74ef02dec0c2f995a3d6`

Verify the live SHA.

If it has changed, inspect and document the difference. Do not silently switch to another source branch.

Create:

`codex/demo-001-scenario-bridge`

from the verified predecessor.

Do not start from the outdated `main`.

Do not auto-merge to `main`.

Do not rewrite history, discard untracked work or alter other branches.

---

# 6. Mandatory source inspection

Read:

- `AGENTS.md`
- `docs/PRODUCT.md`
- `docs/DEMO.md`
- `docs/DECISION_AUTHORITY.md`
- `docs/DECISIONS.md`
- `docs/SESSION_PROTOCOL.md`
- `docs/VERIFICATION_POLICY.md`
- `docs/STATUS.md`
- `tasks/NEXT.md`
- `tasks/WORK_LOG.md`

Inspect the actual implementation:

- `inventor_edu/models.py`
- `inventor_edu/core.py`
- `inventor_edu/gpio_facts.py`
- `inventor_edu/gpio_verify.py`
- `data/gpio/devkitc_32e_catalog.json`
- `data/gpio/devkitc_32e_facts.json`
- `tests/test_gpio_capability.py`
- `tests/core001a_fixtures.py`

Read:

- `reports/CORE-001A-R2-REPORT.md`
- `reports/DATA-001-REPORT.md`
- `reports/CORE-001B-01-REPORT.md`
- `reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md`

The two research reports F/G need not be reinterpreted. The owner has already extracted the binding product decisions and milestones into this handoff.

If those research files are present, treat them as read-only historical context.

If absent, do not search for substitutes or interrupt execution merely to obtain them.

Before coding, produce a BOOT BRIEF confirming the exact existing APIs, source pins, permitted files and no unresolved semantic contradictions.

---

# 7. DEMO-001 implementation objective

Implement a headless adapter for one known scenario:

`HCSR04_GPIO_WIRING`

The scenario is selected explicitly by ID. Do not implement free-form language parsing.

Use exactly these logical signal roles:

| Sensor physical terminal | Required MCU direction |
|---|---|
| `sensor/Trig` | `GPIO_OUT` |
| `sensor/Echo` | `GPIO_IN` |

These roles are limited to the reviewed fixture and do not establish sensor voltage compatibility.

The circuit consists of:

- Instance `board`: selected exact ESP32 board.
- Instance `sensor`: selected HC-SR04 fixture.
- Physical terminals defined in the existing catalog.
- Explicit `Conductor` records between terminal references.

The adapter must determine which board contact is actually connected to each sensor terminal by examining the CORE-001A net partition.

It must not assume that the intended contact is always GPIO18 or GPIO19.

For example:

- `board/J2.5` connected to `sensor/Trig` means the board's GPIO34 contact is being used for an output requirement.
- `board/J3.9` connected to `sensor/Trig` means GPIO18 is being used for the same requirement.
- `board/J3.8` connected to `sensor/Echo` means GPIO19 is being used for an input requirement.

The software must discover these associations from validated net membership.

Do not implement them as special output cases in the verification engine.

---

# 8. Authorized architecture — thin scenario adapter

Create:

`inventor_edu/demo_bridge.py`

Do not modify the canonical model.

The new module is an application-level adapter, not a second engineering engine.

Expose exactly one public operation:

`analyze_hcsr04_wiring(catalog, snapshot, fact_set, trusted_catalog_sha256, trusted_factset_sha256) -> DemoWiringReport`

Use existing typed CORE-001A and CORE-001B records.

### Input requirements

- Exact loaded catalog.
- Existing validated circuit snapshot.
- Existing GPIO fact set.
- Expected catalog SHA-256 from an external trusted calling context.
- Expected fact-set SHA-256 from an external trusted calling context.

Do not generate trusted expected pins from the untrusted input itself.

No network access or external API calls occur in the analysis operation.

### Link-resolution procedure

1. Validate the circuit using existing CORE-001A functions.
2. Compute actual terminal-to-net membership.
3. Identify `sensor/Trig` and `sensor/Echo` using their exact physical terminal references.
4. For each sensor terminal, inspect its actual net membership.
5. Determine the corresponding board physical terminal from committed connectivity.
6. Ensure there is exactly one eligible board GPIO terminal for that signal.
7. Preserve non-GPIO, missing or ambiguous connections as unresolved conditions.
8. Generate the applicable GPIO requirement using the discovered board terminal.
9. Invoke the existing GPIO verifier.
10. Return the original scoped findings and coverage without rewriting their engineering meaning.

The adapter must not infer electrical connections from visual geometry or printed pin labels.

### Required unresolved states

For each sensor signal, distinguish:

- `CONNECTED_UNIQUE`
- `MISSING`
- `AMBIGUOUS`
- `NON_GPIO`
- `SHARED_SIGNAL_NET`

If multiple board GPIO contacts appear on the same sensor net, do not arbitrarily select one.

If Trig and Echo occupy the same electrical net, mark the scenario relationship as unresolved; do not fabricate a suitable connection or declare electrical damage.

If a connection reaches ground or another non-GPIO contact, do not generate a GPIO-direction PASS.

Missing connections are incomplete scenario structure, not automatically sourced electrical violations.

### Scenario result contract

Use a small immutable typed DTO, without changing CORE-001A persistence.

`DemoLinkResult`:

- `role`: `TRIG_OUTPUT` or `ECHO_INPUT`
- `sensor_terminal`: `TerminalRef`
- `board_terminal`: `TerminalRef | None`
- `net_id`: `str | None`
- `state`: one of the five link states above

`DemoWiringReport`:

- `scenario_id`: fixed `HCSR04_GPIO_WIRING`
- `scenario_version`: fixed `1.0`
- `catalog_digest`
- `snapshot_digest`
- `factset_digest`
- `links`: ordered tuple of `DemoLinkResult`
- `gpio_report`: existing `GpioVerificationReport | None`
- `authorization_scope`: fixed `TEST_ONLY_NOT_PRODUCTION`

No general-purpose `overall_safe`, `circuit_valid`, `simulation_success` or universal confidence field may be added.

Use existing canonical serialization behavior where applicable. Do not redefine the underlying topology hashes.

---

# 9. Mandatory check completeness

When a unique valid board GPIO contact is discovered, construct its requirement using the existing `GpioRequirement`.

For the Trig connection:

`requested_function = GPIO_OUT`

For the Echo connection:

`requested_function = GPIO_IN`

For each resolved role, request all of the following:

1. `PIN_MAPPING`
2. `PHYSICAL_CAPABILITY`
3. `BOARD_AVAILABILITY`
4. `ACTIVE_CONFIGURATION`
5. `ELECTRICAL_COMPATIBILITY`

The fifth check remains explicitly delegated to the future CORE-001C engine.

Use:

`operating_state = ACTIVE`

Do not allow the scenario adapter to omit a required check because a caller supplied a shorter list.

The fixed scenario owns its complete required-check selection.

Do not interpret an individual GPIO capability PASS as successful completion of all five checks.

The expected existing verifier behavior includes:

- A particular physical capability may PASS.
- Board availability may remain UNKNOWN.
- Active firmware configuration remains UNKNOWN without validated observation.
- Electrical compatibility remains NOT_EVALUATED.
- The full scenario therefore cannot be declared electrically safe.

Do not invent voltage thresholds or sensor drive limits.

---

# 10. Expected real cases

Use the pinned B test catalog and exact sensor fixture.

### Case A — Wrong output GPIO

Connect:

`board/J2.5 → sensor/Trig`

and:

`board/J3.8 → sensor/Echo`

Required result:

- Trig's discovered board contact is `J2.5`.
- Trig's `GPIO_OUT` physical capability is `FAIL / OUTPUT_NOT_CAPABLE`.
- Echo's `GPIO_IN` physical capability is `PASS / CAPABILITY_CONFIRMED`.
- Board availability, firmware and electrical coverage remain separately scoped.
- No overall circuit-safe conclusion.

### Case B — Corrected output GPIO

Change the Trig conductor to:

`board/J3.9 → sensor/Trig`

Keep:

`board/J3.8 → sensor/Echo`

Required result:

- The actual net changes.
- Trig's discovered board contact becomes `J3.9`.
- GPIO18 output physical capability returns scoped PASS.
- GPIO34 output FAIL no longer appears in the current result.
- Echo's separate result remains consistent.
- Unverified board, firmware and electrical conditions are not silently upgraded.

### Case C — Missing wire

Remove Trig's wire.

Required result:

- `MISSING` for the Trig link.
- No invented physical GPIO selection for that role.
- Echo remains evaluable independently if connected.

### Case D — Ambiguous wiring

Connect two different board GPIO contacts to the same Trig net.

Required result:

- `AMBIGUOUS`.
- No arbitrarily chosen GPIO capability PASS for Trig.
- No automatic short-circuit damage claim.

### Case E — Shared sensor net

Connect the sensor's Trig and Echo contacts into the same net.

Required result:

- `SHARED_SIGNAL_NET` on affected roles.
- No false claim that the functional sensor interface is correct.
- No unsupported physical-safety verdict.

### Case F — Untrusted evidence

Run with missing or incorrect external expected pins.

Required result:

- Preserve the existing CORE-001B trust behavior.
- No unsupported positive finding.
- No adapter-level bypass that computes its own trusted pin from the provided payload.

---

# 11. Acceptance tests

Create:

`tests/test_demo001_bridge.py`

At minimum implement the following independently derived tests.

| ID | Expected result |
|---|---|
| DEMO-A01 | Valid physical references and source catalog load |
| DEMO-A02 | J2.5→Trig yields output capability FAIL |
| DEMO-A03 | J3.9→Trig yields output capability PASS |
| DEMO-A04 | J3.8→Echo yields input capability PASS |
| DEMO-A05 | Removing a conductor removes its former GPIO finding from the current result |
| DEMO-A06 | Missing and ambiguous connections do not produce fabricated positive GPIO findings |
| DEMO-A07 | Shared Trig/Echo net does not produce an overall success claim |
| DEMO-A08 | Non-GPIO board contact cannot pass GPIO capability verification |
| DEMO-A09 | Invalid physical terminal raises the existing CORE-001A typed error |
| DEMO-A10 | Incorrect and missing evidence pins preserve CORE-001B trust restrictions |
| DEMO-A11 | Reordered equivalent conductor inputs preserve semantic net membership and findings |
| DEMO-A12 | Two component instances with identical display labels remain distinguishable by persistent instance ID |

Keep the golden expectations independent of the new adapter's own outputs.

Do not hardcode `FAIL` in response to a particular demo action.

The actual `GpioVerificationReport` must come from `verify_gpio_requirements()`.

When available, use existing catalog and fact-set fixtures and their known pinned digests without duplicating a manufacturer data catalog.

The acceptance suite must make it obvious whether the GPIO verifier truly ran.

---

# 12. Regression and source acceptance

Run:

- The existing CORE-001A regression tests.
- R1 and R2 tests.
- DATA-001 tests.
- CORE-001B GPIO tests.
- The new DEMO-001 tests.

Preserve all existing expected outcomes.

The previous CORE-001B report recorded 44 passing methods.

That number is only the historical baseline.

Report actual current counts.

Run authentic-source acceptance for the existing GPIO evidence using the pinned source artifacts when available.

Do not count missing-source skips as authentic-source PASS.

If the required source cache is absent and cannot lawfully be reconstructed, report `SOURCE_ACCEPTANCE_NOT_RUN` or `BLOCKED`, with the exact effect on acceptance.

No new source ingestion is authorized in this task.

---

# 13. Files authorized

Only the following changes are allowed.

### Create

- `tasks/DEMO-001.md`
- `docs/prototype/MASTER_PLAN.md`
- `inventor_edu/demo_bridge.py`
- `tests/test_demo001_bridge.py`
- `reports/DEMO-001-REPORT.md`

### Factual tracking updates, only if needed

- `docs/STATUS.md`
- `tasks/NEXT.md`
- `tasks/WORK_LOG.md`

Do not modify existing CORE-001A/B implementations, schemas, source catalogs or tests.

Do not modify Research F, Research G or other raw research.

Do not modify `docs/DEMO.md`, `docs/DECISIONS.md` or accepted/proposed ADRs.

Do not add dependencies, frontend packages, databases or new deployment configuration.

Do not implement DEMO-002 or any later milestone.

---

# 14. Changes, blockers and deviation handling

If actual existing API behavior contradicts this frozen specification:

1. Identify the exact file, line and runtime behavior.
2. Preserve the existing code.
3. Determine whether the task can proceed without changing the approved contract.
4. If not, stop the affected work.
5. Record the exact blocker and alternative options in the report.
6. Do not choose the architectural alternative yourself.

If only a safe, file-local implementation detail is missing, implement it within this task's existing contract.

Do not turn a small adapter into a new general scenario framework.

Do not design future code in order to reduce imagined long-term effort.

---

# 15. Required execution report

Create:

`reports/DEMO-001-REPORT.md`

The report must contain:

1. Task ID, revision and authority.
2. Exact predecessor branch and SHA.
3. BOOT BRIEF.
4. Actual source and API inspection.
5. Changed-file manifest.
6. Master-plan persistence confirmation.
7. Implemented adapter and exact types.
8. How sensor connections are resolved from real nets.
9. How required GPIO checks are generated.
10. Actual GPIO verifier integration.
11. Independently expected positive/negative cases.
12. All test commands and unedited outcomes.
13. Missing/unknown/ambiguous behavior.
14. Source and trust scope.
15. Full research-informed features not attempted.
16. Known limitations.
17. Any proposed plan changes — not implemented.
18. Decision requests for the owner.
19. Git branch, commit SHA and verified remote push.
20. Final outcome: `PASS`, `PARTIAL` or `BLOCKED`.

Report separately:

- Topology integration correctness.
- Requirement completeness.
- GPIO verifier integration.
- Evidence trust restrictions.
- Regression status.
- Prototype feature completeness.
- Full demo acceptance status.

A headless adapter PASS must not be presented as a completed interactive product.

---

# 16. Session completion

Follow the mandatory Git lifecycle.

Review the working tree and staged diff.

Commit only authorized files.

Scan for secrets and restricted source artifacts.

Push to:

`origin/codex/demo-001-scenario-bridge`

Verify the remote SHA.

Do not merge into `main`.

Do not start DEMO-002.

Return the report path and its complete Markdown content for review in the architecture conversation.

---

# 17. Final success condition

DEMO-001 succeeds only if a verified CORE-001A physical circuit can be transformed into exactly the required CORE-001B GPIO requests for the two supported sensor signal roles, and the actual GPIO verifier returns the expected results for wrong, corrected, incomplete and ambiguous wiring.

The adapter must remain device-family extensible at the engineering-core level without rewriting the existing verifier.

The selected scenario may be explicitly bounded to the reviewed ESP32/HC-SR04 fixture.

No new claim of physical safety, operating firmware or complete product functionality is authorized.

**Execute DEMO-001 only. Do not interpret the research, redesign the plan or initiate another milestone.**

**END OF FROZEN TASK.**