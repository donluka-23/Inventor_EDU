INVENTOR EDU — CORE-001C-E2
Topology-Grounded Two-Resistor Divider Motif: Canonical Nets, Conditional Model Binding, and Fail-Closed Evaluation
Task ID: CORE-001C-E2
Revision: 1 — OWNER-FROZEN, single-task execution handoff
Repository: D:\Inventor_EDU
Remote: https://github.com/donluka-23/Inventor_EDU.git
Required predecessor: origin/codex/core-001c-e1-voltage-math
Expected predecessor HEAD at preparation: 7d60e6e8143030c4ec32ad69ae3c19225f474546
New branch: codex/core-001c-e2-divider-topology
Authority: This frozen task and accepted repo governance. Research reports are evidence and historical context, not autonomous implementation instructions.
Output scope: Test-only, read-only application adapter and genuine new headless engineering capability. No hardware-compatibility claim.
1. Why E2 is necessary
E1 correctly computes a mathematical, unloaded ideal two-resistor voltage divider with exact interval arithmetic. Its optional SnapshotAssociation stores CORE digests only; it does not prove resistor instances or the relevant net pattern exist. In the current E1 demonstration, the canonical snapshot has board and sensor with Trig/Echo wires, no resistor network. The report explicitly says NETWORK_PHYSICALLY_REPRESENTED=NOT_ESTABLISHED and NOT_PROVEN_HARDWARE_COMPATIBILITY.

E2 must turn this limitation into an actual, falsifiable software capability: recognize a precisely bound two-resistor canonical virtual circuit topology before allowing the E1 mathematical result to be associated with that topology.

Do not confuse: a resistor represented as a two-terminal component in a CORE snapshot; a resistor's independently established ohmic value; the real physical resistor a learner might hold; and a manufacturer's electrical guarantee. They are four separate propositions.

A measured goal for this session is a real netlist change that changes the motif verdict and invalidates the old model association, without changing any older engineering engine.
2. Source and architecture gates before coding
Read actual code and exact signatures, then report the BOOT BRIEF:
- AGENTS.md, docs/DECISION_AUTHORITY.md, docs/SESSION_PROTOCOL.md, docs/OSS_POLICY.md, docs/VERIFICATION_POLICY.md, docs/DECISIONS.md, docs/STATUS.md, tasks/NEXT.md;
- accepted ADR-0001 and docs/prototype/MASTER_PLAN.md version 1.5;
- inventor_edu/models.py, inventor_edu/core.py, inventor_edu/voltage_model.py and associated tests, fixtures, source ledger and prior E1 report;
- reports/DATA-001-REPORT.md, particularly the generic passive two-terminal structural fixture and its held exact YAGEO admission;
- Research C §4, §§9–10.2 and §17.1, if present locally. The current DeviceDefinition.device_class implementation is an extensible Identifier; do not rely on superseded research prose claiming that only two literal device classes exist.
Owner-frozen architectural selection for E2: represent each of the two resistor bodies as a normal component instance with two distinct terminal refs in the existing CatalogSnapshot and CircuitSnapshot. Bind those terminal roles through a separate narrowly typed read-only E2 motif request. Let CORE alone own conductors, junctions and nets. A resistor is not an ideal wire and not an InternalIdealTie.

No CORE schema change is approved. Do not implement Research C's other alternatives or a universal passive-device ontology. If the exact current schemas cannot express this without a schema change, stop with OWNER_DECISION_REQUIRED, show the contradiction and do not improvise one.
3. Approved fixture and provenance
- For the primary demonstration, reuse the existing reviewed exact DevKitC-32E + Adafruit #3942 identities as source-context records if their canonical catalog can be faithfully extended for the isolated E2 test.
- Add exactly two synthetic, clearly test-only two-terminal passive resistor definitions to a separately generated test-only composite catalog. The synthetic resistor value, tolerance and actual material must not be called verified manufacturer properties.
- Existing DATA-001 LibrePCB generic resistor structure may be consulted as an independent structural check; the held YAGEO-to-footprint match may not be admitted as a manufacturer's exact part. Do not modify that importer, records, or source evidence.
- A composite catalog necessarily changes the catalog digest. The currently pinned B GPIO fact-set's catalog binding must therefore not be reused as if it were verified for the composite catalog. This E2 is a CORE+E1 isolated topology experiment, not a new B/EDU/CHAT hardware report.
- Build the composite fixture through existing CORE catalog admission and deterministic digest verification. Never call a test-built catalog hash an independently approved commercial source pin.
- Preserve E1's assumption-bound Vin, Rtop, Rbottom, tolerances and threshold as model inputs only.
- Do not add external source downloads, dependencies or database persistence.
If a test-only composite fixture is incompatible with exact board/sensor identity or catalog validation, switch to a clearly labeled fully synthetic board/source/receiver/passives motif fixture only as the fallback described in the execution report, not silently. Report that the exact ESP32 scenario was blocked; overall product-integration acceptance must remain PARTIAL, not a fake PASS.
4. Precise topology motif
A typed E2 request shall provide immutable, exact terminal role anchors, not merely net-name strings:
- source_out: source or sensor signal terminal, for this demo sensor/Echo;
- receiver_input: receiver board terminal, for this demo board/J3.8 (GPIO19);
- reference_ground: reviewed board ground contact, for this demo a real GND terminal;
- r_top_hi, r_top_lo: two distinct terminal refs on one declared resistor instance;
- r_bottom_hi, r_bottom_lo: two distinct terminal refs on a different resistor instance;
- exact component instance IDs, definition digests, current catalog digest and actual CORE-computed snapshot digest;
- the linked E1 IdealDividerHypothesis or its immutable model digest and exact association, as needed for the minimal adapter;
- a test-only trust/assumption qualification.
Required net partition, computed only via compute_nets:
1. NET_SOURCE: source_out and r_top_hi are on the same net.
2. NET_MID: r_top_lo, r_bottom_hi, and receiver_input are on the same net.
3. NET_GROUND: r_bottom_lo and reference_ground are on the same net.
4. Those three nets must be pairwise distinct.
5. The two resistor devices have no internal ideal tie and each belongs to the declared two-terminal passive fixture. A resistor's two terminals must not be the same CORE net.
6. Reject parallel/bypass ideal wires that short the source to mid, mid to ground, or source to ground.
7. Reject any unreviewed additional terminal on the source or midpoint nets when its electrical effect is unknown; do not assume that branch is an open circuit. Explicitly permit only exact verified internal ground ties on the ground net if present in the reviewed board catalog.
8. If an arbitrary extra component, external load, active element, powered rail or ambiguous shared net changes the stated unloaded 2R conditions, return MOTIF_NOT_ADMITTED or MODEL_SCOPE_UNRESOLVED, with exact reason and affected net members. Do not blindly calculate an unloaded divider result over it.
9. Source drive, physical resistor properties, receiver input leakage/pulls, power-off, and transient behavior stay separate INDETERMINATE or NOT_EVALUATED obligations.
Do not infer resistor conduction by treating r_top_hi and r_top_lo as the same net. The resistor's voltage-drop relationship belongs to E1's explicit mathematical assumptions, not CORE wire topology.
5. API/result contract
Create inventor_edu/divider_topology.py with the smallest strict immutable public DTOs and a pure function, e.g.:
bind_ideal_divider_to_snapshot(
    catalog: CatalogSnapshot,
    snapshot: CircuitSnapshot,
    binding: DividerTopologyBinding,
    hypothesis: IdealDividerHypothesis,
) -> DividerTopologyReport
The function must recompute real CORE topology and verify the exact references; it must not accept caller-supplied topology summaries or UI coordinates as proof. Independently validate every role's owner instance, terminal, device shape and snapshot identity.

Use explicit, non-deceptive states such as:
- CANONICAL_MOTIF_MATCHED — a topology fact about the virtual graph only;
- MOTIF_NOT_ADMITTED — structurally incorrect graph;
- MODEL_SCOPE_UNRESOLVED — graph exists but unloaded 2R assumptions cannot be established from allowed shape;
- MATH_EXECUTED_CONDITIONALLY — E1 was invoked only after a matching motif and explicit E1 assumptions;
- MATH_WITHHELD — do not attach numerical output on a failed or unresolved motif.
Do not emit SAFE, ELECTRICAL_COMPATIBLE, REAL_HARDWARE_HIGH, READY_TO_BUILD, or PHYSICALLY_VERIFIED.

Report must include:
- matched or rejected role anchors and exact three expected net IDs;
- snapshot and catalog digests, model digest and algorithm version;
- explicit observed net members and affected connection IDs for failed checks;
- exact reason codes, unmet prerequisites and per-rule statuses;
- optional immutable original E1 VoltageModelReport only if its assumption-bound math is actually run after successful motif admission;
- a separate model_values_are_assumptions disclosure and actual_component_value_not_admitted disclosure;
- TEST_ONLY_NOT_PRODUCTION, HARDWARE_COMPATIBILITY_NOT_PROVEN.
Do not change E1's VoltageModelReport.physical_network_provenance or pretend E1 acquired new source data. E2's CANONICAL_MOTIF_MATCHED asserts only virtual netlist membership, not that the actual hardware has been built.
6. Falsifiable example and independent oracle
Implement one executable headless demo of the same input assumption with two different real CORE netlists:

Case A — correct virtual divider motif
sensor/Echo --- r_top.high [R_TOP] r_top.low --- (MID) --- board/GPIO19
                                             |
                                        r_bottom.high
                                          [R_BOTTOM]
                                        r_bottom.low
                                             |
                                           GND
These are two resistor component bodies, not ideal-wire paths through the bodies. Case A must show the actual three-net partition and the conditional E1 numerical result, preserving unverified load/hardware conditions.

Case B — wrong topology

Change a real Conductor endpoint so the receiver is tied to the source or the bottom-resistor return is on the source net (construct at least two independent negative examples). CORE must produce a new snapshot and net partition. E2 must withhold the E1-attached result and report the exact topology failure. It must not display stale Case A values as applicable to Case B.

Revert the connection and prove the original canonical net partition and model association are recovered with stable digests.

An independent oracle must list the exact expected net member sets using explicit contact IDs, not use the E2 matcher to predict its own expected output.
7. Mandatory acceptance gates
Create tests/test_core001c_e2_divider_topology.py, with independent tests for at least:
1. Exact source, receiver, ground and resistor terminal identities.
2. Two different resistor instances with distinct terminal refs.
3. Three independent CORE nets with exact expected member sets.
4. Correct separation of a resistor body from ideal wire connectivity.
5. A topology-only motif match does not assert material/manufacturer/real-hardware proof.
6. Correct motif admits the unchanged E1 assumption-based numerical result.
7. Wrong midpoint/source connection rejects without attached math.
8. Shorted resistor terminals reject without attached math.
9. Missing ground or wrong reference ground rejects.
10. Missing or duplicate resistor instance, wrong definition digest or nonexistent terminal rejects.
11. Wrong snapshot/catalog digest or stale association rejects or returns explicit stale scope.
12. Unreviewed extra load on midpoint withholds unloaded-model result.
13. Additional unknown contact on source net never silently passes.
14. Reordered conductor order and reversed wire endpoints preserve equivalent motif and digest.
15. Changing a wire produces a new snapshot; old model association never appears current.
16. Changing R assumptions changes model digest without creating manufacturer authority.
17. Non-ESP32 synthetic two-resistor circuit matches through the same generic algorithm.
18. Existing B fact-set pins are not misapplied to the recomposed catalog; no new B authority inferred.
19. Negatives cannot return SAFE, ELECTRICAL_COMPATIBLE, HARDWARE_HIGH or PHYSICALLY_VERIFIED.
20. Full prior regression, authentic GPIO admission and deterministic CLI replay pass.
Use separate expected constants and structural network oracles rather than deriving test expectations from the implementation.
8. Scope and prohibited changes
Authorized additions:
- inventor_edu/divider_topology.py
- tests/test_core001c_e2_divider_topology.py
- examples/core001c_e2_divider_topology.py
- docs/prototype/DIVIDER_TOPOLOGY_E2_CONTRACT.md
- tasks/CORE-001C-E2.md
- reports/CORE-001C-E2-REPORT.md
Factual updates allowed:
- docs/STATUS.md
- tasks/NEXT.md
- tasks/WORK_LOG.md
- docs/prototype/MASTER_PLAN.md only version 1.5 → 1.6, append a bounded E2 row, preserve every fixed non-goal, risk, previous gate and deferred milestone.
If an additional test-only fixture file is strictly required, stop for owner authorization unless it can be implemented as an in-memory fixture within the new test/example files above. Do not create new production catalogs.

Read-only, no modifications: existing models.py, core.py, gpio_facts.py, gpio_verify.py, voltage_model.py, synthesis.py, capability_discovery.py, educational_feedback.py, learning_session.py, local HTTP preview, prior tests, DATA-001 importer and candidate files, source ledgers, research F–I/J, governance, decisions, licenses and dependency locks.

Not authorized: general circuit simulator, numeric nodal solver, SPICE, firmware, new source downloader, generic resistor catalog intake, real GPIO safety verdicts, localization approval, 2D editor, learner mode architecture, general NLP, any LLM call, new app dependency, tests that simply assert PASS for unknown physical facts.
9. Engineering quality and execution discipline
- Start by verifying remote baseline SHA and reading governance. Record BOOT BRIEF and exact public API signatures.
- Maintain a simple rule authority matrix: CORE establishes net membership; E2 establishes only exact motif membership; E1 establishes conditional model mathematics; source/assumption gates retain their origin. E2 may not overrule these layers.
- For each new MOTIF rule, give a positive example, a negative counterexample, an unknown/extra-load example, and an independent structural oracle.
- Record a source/assumption table showing what is reviewed, synthetic, or unverified and what claim each can support.
- All records immutable/versioned with exact digests and stable ordering.
- Fail closed on malformed, conflicting, stale or ambiguous input; do not downgrade a violation to an unconditional success.
- No hardcoded GPIO19, HC-SR04 or board brand in the generic motif algorithm. Exact names may appear in fixture data only.
- Do not classify a successful mathematical formula as physical hardware compatibility.
- Do not claim performance of a measured human learner. No UX or language-review claims.
- Stop and ask owner for any architecture/schema/dependency/model scope change not frozen here.
10. Report, Git and completion
Run and record:
- Python, pinned dependency versions and preflight;
- targeted E2 acceptance suite;
- complete unittest discover -s tests -v regressions;
- authentic GPIO source-admission gate with actual pinned input material;
- demo twice in fresh processes, byte-stable summary/JSON where applicable;
- exact net member sets, actual failure reasons, E1 math inclusion/withholding and timing;
- any blocked criteria and remaining unverified facts.
Create reports/CORE-001C-E2-REPORT.md with BOOT BRIEF, changed file manifest, actual commands/exit codes, independent oracles, source/evidence distinctions, full current architecture status, known limitations and precise next owner decisions.

Commit only authorized paths on codex/core-001c-e2-divider-topology, push and independently verify live remote SHA. Do not merge main. No next task selection or autonomous implementation.

PASS gate: A two-resistor virtual circuit appears as real separate passive instances with real CORE-computed source/mid/ground nets; conditional E1 math is linked only when that exact motif is present; a physically altered conductor invalidates its association; unknown hardware electrical conditions remain clearly unproven; all prior tests stay green.

If the existing catalog/core semantics prevent the required example without changing frozen interfaces, report PARTIAL/`BLOCKED` and return the precise owner decision instead of inventing an alternative architecture.

EXECUTE CORE-001C-E2 ONLY.