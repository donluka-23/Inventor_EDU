INVENTOR EDU — CORE-001C-E1
Evidence-Gated Voltage Mathematics and Conditional Engineering Findings
Task ID: CORE-001C-E1
Revision: 1 — OWNER-PROPOSED, SINGLE EXECUTION TASK
Repository: D:\Inventor_EDU
Remote: https://github.com/donluka-23/Inventor_EDU.git
Expected predecessor: origin/codex/chat-001-local-learning-session at ebb373fef5d4506d4ffd382d421f4a4712a59a13 (verify live SHA first; stop on mismatch).
New branch: codex/core-001c-e1-voltage-math
Authority: This owner handoff plus accepted repository governance, not open-ended research proposals.
Output: Executable, independently tested numerical model capability, NOT certified hardware compatibility.
1 — Why this task exists
The latest CHAT-001 checkpoint proved loopback HTTP form transitions and retained real CORE/B findings, but reported PASS_TEST_ONLY_PREVIEW, incomplete visual-browser automation, and PENDING_HUMAN_REVIEW Georgian wording. These are still open. The user-facing project can currently demonstrate GPIO-capability failures and corrections; it cannot compute the simplest voltage-divider scenario or establish electrical compatibility. This blocks a meaningful part of docs/DEMO.md and the project's engineering-education value.

Develop one genuinely new computation, not a larger menu, an LLM explanation, or additional unverified sensor facts:
Given an explicit, typed ideal two-resistor divider model and bounded numerical inputs, compute the output-voltage range and a separate conditional logic-high margin, with exact units, mathematical derivation, source/assumption provenance, and faithful UNKNOWN/NOT_EVALUATED gates.

The same algorithms must work on a synthetic non-ESP32 example. One fixed HC-SR04 answer is unacceptable. Never claim that a resistor network exists in the canonical physical snapshot unless the current CORE topology actually contains those components and nets. It currently does not.
2 — Research foundation; approved subset only
Research C, Electrical Compatibility, Bounded Physical Models and Scientific Computations, is relevant research, not implementation authority. This handoff adopts only:
- Ohm's law and Kirchhoff circuit laws for an ideal, DC, unloaded 2R divider; optional explicitly parameterized resistive loading only if all independent numerical oracles pass.
- Unit-aware, bounded voltage/resistance intervals, including tolerance and extreme-value evaluation.
- Separate LOGIC_HIGH_GUARANTEE, LOGIC_LOW_GUARANTEE, PIN_STRESS, SOURCE_DRIVE, POWER_OFF, TRANSIENT, and PHYSICAL_NETWORK_PROVENANCE scopes; do not collapse to an overall SAFE verdict.
- Provenance-sensitive distinction between manufacturer guarantee, distributor/retailer description, measured value, approved assumption and unknown.
- PASS only for a fully supported, stated rule and modeled assumptions; INDETERMINATE when physical source facts or operating conditions are insufficient; NOT_EVALUATED for unimplemented physics. Use MODEL_ONLY / CONDITIONAL_ON_ASSUMPTIONS qualification in all mathematical examples.
- No SPICE, generic MNA, LLM, new runtime dependency, or speculative GPIO abs-max assertion.
Critical evidence constraints: Adafruit #3942 seller language describing Echo as “5V logic” is not a guaranteed VOH_min/`VOL_max` waveform envelope; the ESP32-WROOM-32E VDD33 absolute-max supply rating is not a GPIO input-pin absolute-max limit. A typical 5V label must not become a guaranteed 4.75–5.25V source. Extending datasheet threshold formulas beyond their documented conditions requires an explicit model assumption, not a sourced device guarantee. Verify actual source-revision details from the existing ledger; don't invent them.
3 — Non-negotiable engineering boundaries
1. CORE-001A owns topology. No changes to models.py, core.py, net algorithms or terminal identity. A proposed 2R circuit is a separately typed analytical hypothesis, not a physical circuit asserted by existing CircuitSnapshot.
2. CORE-001B owns GPIO checks. Its positive/unknown statuses stay unchanged. This task does not replace ELECTRICAL_COMPATIBILITY=NOT_EVALUATED from existing B.
3. CAP/SYN/EDU/CHAT stay unchanged. No HTTP or chat integration, no unreviewed Georgian language changes, no research-guided automatic pedagogy.
4. The calculator may carry an optional validated catalog_digest/`snapshot_digest` as an association, not proof that the hypothesized resistors are present. Explicit field physical_network_provenance=NOT_ESTABLISHED is mandatory for the first fixture.
5. Provenance is not established by a hash alone. Caller-provided pins or numbers are not promotion to manufacturer facts. All fixture assumptions must be labelled and reproducible.
6. Do not turn a negative conditional logic-high margin into a claim that the MCU definitely reads LOW, or a positive margin into a global hardware PASS.
7. If a prerequisite requires a new canonical resistor device model, a changed source admissibility rule, or unapproved solver dependency, STOP that subtask with OWNER_DECISION_REQUIRED; do not silently modify the architecture.
4 — Minimal public API contract
Add an isolated, strict, immutable module, tentatively:
- inventor_edu/voltage_model.py
- VoltageInterval, ResistanceInterval, IdealDividerHypothesis, ThresholdHypothesis, AssumptionRecord, ModelCalculation, ScopedModelFinding, VoltageModelReport, VoltageModelInputError.
- evaluate_ideal_divider(hypothesis: IdealDividerHypothesis) -> VoltageModelReport.
These are suggested exact names; document any minimal contract adjustment before writing code. Avoid an expansive ontology. Define and reject nonfinite values, negative/zero resistance, malformed voltage bounds, invalid tolerance ranges, inconsistent units, missing model scope, and unsupported network kinds. Use Python decimal.Decimal or fractions.Fraction with documented rounding and comparison semantics, not unconstrained binary float or unit-guessing. Explicit V, mV, ohm and kΩ conversions must pass dimensional tests.

For an unloaded 2R divider with R_top from source to output and R_bottom from output to ground:

V_out = V_in * R_bottom / (R_top + R_bottom).

For independent nonnegative input intervals, monotonic corners must use V_in_min * R_bottom_min/(R_top_max+R_bottom_min) for lower, and V_in_max * R_bottom_max/(R_top_min+R_bottom_max) for upper. If parameters are correlated, do NOT silently apply rectangular independent extrema; either validate an explicit admissible joint envelope or return INDETERMINATE for unsupported correlation.

A ThresholdHypothesis may provide a clearly marked assumed VIH requirement for an illustrative comparator. Model-threshold inequality: calculated V_out_min >= assumed_VIH_required_max. Report exact margin and zero-margin boundaries. A model-only satisfied/unsatisfied comparison must not be rendered as real hardware PASS/FAIL without device-grade prerequisites.

Return independently typed results:
- MODEL_EQUATION: math completed or invalid.
- MODEL_HIGH_MARGIN: model-only positive/negative/zero result, bound to assumptions.
- HARDWARE_LOGIC_HIGH: INDETERMINATE unless all required externally qualified device facts and applicability conditions are available (do not implement manufacturer-grade acceptance in this E1 task).
- GPIO_PIN_STRESS: INDETERMINATE / NOT_EVALUATED, not inferred from module supply rating.
- SOURCE_DRIVE_CURRENT, POWER_OFF, TRANSIENT: NOT_EVALUATED or INDETERMINATE with exact reason codes.
- NETWORK_PHYSICALLY_REPRESENTED: NOT_ESTABLISHED for sidecar hypotheses.
Every numerical result needs: units, input values/ranges, model identity/version, assumptions, calculation steps, a stable digest, rule ID, status/qualification, and unclosed prerequisites. Output cannot contain SAFE, READY_TO_BUILD, FULLY_COMPATIBLE, HARDWARE_VERIFIED, or an implicit electrical PASS.
5 — Independent acceptance oracles (E1-01 to E1-18)
Use independently calculated expected values, not only snapshots or the implementation's own helpers:
1. 5V, 10kΩ top / 10kΩ bottom → exactly 2.5V unloaded.
2. 5V, 6.8kΩ top / 10kΩ bottom → 2.976190476...V.
3. Swapped 10kΩ top / 6.8kΩ bottom → 2.023809523...V; ordering matters.
4. Monotone corner bounds for input 4.5–5.25V, both resistors ±1%, top 6.8kΩ/bottom 10kΩ: approximately [2.656846374..., 3.150249524...]V; independent fraction/Decimal oracle.
5. 5V, 10k/10k, assumed VIH=0.75×3.4V=2.55V → model-only margin −0.05V; not a guaranteed real LOW.
6. 5V, 6.8k/10k, assumed VIH=2.55V → positive model-only margin; no full hardware PASS.
7. Exact equality to threshold → zero margin, never rounded positive.
8. 0.05 V and 50 mV equivalent; reject a current unit where voltage is required.
9. Missing manufacturer VOH_min with valid nominal source value → HARDWARE_LOGIC_HIGH INDETERMINATE.
10. Module VDD33 abs-max without pin-specific rating → PIN_STRESS cannot pass.
11. Zero/negative resistor, tolerance <0, invalid range, NaN/Infinity all rejected.
12. Low, high and general signal applicability checks independently labelled; absence of LOW envelope cannot yield a LOW PASS.
13. A declared correlated source/supply relationship cannot be independently extremized without an approved model.
14. Synthetic non-ESP32 numerical case executes unchanged algorithm.
15. Order-only serialization variation preserves canonical math; changed assumptions change digest.
16. Identical model with a changed snapshot_digest remains a new, traceable association and cannot reuse an old physical proof.
17. No physically represented resistors in existing CORE snapshot → NETWORK_PHYSICALLY_REPRESENTED=NOT_ESTABLISHED; do not claim canonical resistor net membership.
18. No false real-hardware electrical PASS anywhere in the included evidence-limited fixture; full regression incl. all previous CHAT/EDU/SYN/CAP/CORE/DATA tests remains green.
Optional only with no delay to mandatory acceptance: an explicit 100kΩ shunt load oracle via two mathematically independent methods (Thevenin and KCL) for V_in=5V, R_top=6.8kΩ, R_bottom=10kΩ: ~2.860411899V. Do not add load support merely to increase functionality count.
6 — User-visible, falsifiable outcome
Produce a single headless Georgian-compatible structured demonstration (not newly authored, unreviewed free-form Georgian pedagogical text) that presents:
- The same nominal 5V input under 10k/10k versus 6.8k/10k proposals.
- Numerically distinct Vout and threshold margins with exact assumption flags.
- A trace from input units, formula and source/assumption classification to the scoped finding.
- An explicit explanation code for NOT_PROVEN_HARDWARE_COMPATIBILITY and the list of missing maker/board facts.
- An explicit statement that the resistors are hypothesized, not in the verified physical netlist.
Both machine-readable JSON and a concise neutral technical summary must be deterministic. Expose no global safety verdict.
7 — Authorized files / governance
Allowed additions:
- inventor_edu/voltage_model.py
- tests/test_core001c_e1_voltage_model.py
- examples/core001c_e1_voltage_cases.py
- docs/prototype/VOLTAGE_MODEL_E1_CONTRACT.md
- tasks/CORE-001C-E1.md
- reports/CORE-001C-E1-REPORT.md
Allowed factual updates only: docs/STATUS.md, tasks/NEXT.md, tasks/WORK_LOG.md. Update docs/prototype/MASTER_PLAN.md from 1.4 to 1.5 only to record this isolated mathematical experiment as an authorized substep; preserve the existing CORE-001C full acceptance gate, deferred UI and other restrictions. Do not rewrite the milestone as production-ready.

Forbidden changes: models.py, core.py, gpio_facts.py, gpio_verify.py, capability_discovery.py, synthesis.py, educational_feedback.py, learning_session.py, existing UI/server and CLI, existing tests, evidence catalogs, archived Research F–I, governance/ADRs, dependency locks. Research C is context only if actually accessible; do not create a supposed original copy.

Read the repository's AGENTS.md, docs/DECISION_AUTHORITY.md, docs/SESSION_PROTOCOL.md, docs/OSS_POLICY.md and current verification policy before changing files. Do not use open-ended internet or Codex independent design selection to expand the task.
8 — Test, provenance, performance, publication
Mandatory BOOT BRIEF: verify remote baseline SHA, history includes Research F–I archival commit, clean worktree, exact APIs, existing models and fixture binding. If a real contradiction is found, file OWNER_DECISION_REQUIRED and stop only the blocked work.

Record numerical precision and runtime on both nominal and interval cases; measure, never invent. Run new independent test suite, entire existing unittest discovery, authentic GPIO source-admission gate, two byte-identical JSON replays. Count and describe all unsupported claims; false hardware PASS must equal zero.

Create exactly one branch codex/core-001c-e1-voltage-math, commit only authorized files, push it and verify remote HEAD. Do not merge main, do not start another task, and do not modify Georgian review flags.

Report complete command lines, environment, mathematical oracles, all facts vs assumptions, failed/blocked checks, limitations, exact Git SHAs, and final PASS / PARTIAL / BLOCKED. PASS is permitted only for the bounded mathematical computation, never for overall hardware safety or electrical compatibility.

Execute CORE-001C-E1 only.