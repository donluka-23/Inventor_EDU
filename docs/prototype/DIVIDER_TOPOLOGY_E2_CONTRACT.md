# CORE-001C-E2 divider topology contract

```python
bind_ideal_divider_to_snapshot(
    catalog: CatalogSnapshot,
    snapshot: CircuitSnapshot,
    binding: DividerTopologyBinding,
    hypothesis: IdealDividerHypothesis,
) -> DividerTopologyReport
```

`DividerTopologyBinding` is an immutable schema 1.0 request with catalog and snapshot digests, the test-only qualification, and seven `TerminalAnchor` records. Each anchor pins a physical `TerminalRef` and the owning instance's exact definition digest. Roles are source output, receiver input, reference ground, and high/low ends of the two separate synthetic resistor bodies.

CORE validates the catalog and snapshot and owns conductors, junctions, ideal ties and net membership. E2 requires two distinct synthetic `passive_resistor` instances with exactly two unbound passive contacts and no internal ideal tie. Source and receiver anchors must be distinct signal devices with appropriate declared contact roles. The ground anchor belongs to the receiver. For a reviewed nonsynthetic receiver it must carry admitted typed ground power-domain mapping. These metadata checks establish virtual roles. They establish no signal capability.

The three required groups are source output with top high, top low with bottom high and receiver input, and bottom low with reference ground. Their CORE net IDs must differ. Source and midpoint allow only the specified terminals. Ground allows the specified terminals and ground aliases that CORE connects inside the isolated receiver with no external wires. Other contacts on these nets leave unloaded model scope unresolved. CORE junctions can route conductors without adding electrical terminal members. Isolated nets outside the motif remain outside its scope.

The report includes current digests, replayable binding and hypothesis hashes, observed anchors, representative source/midpoint/ground net IDs, full members and connection IDs for the observed role nets, per-rule states and prerequisites. An anchor's MATCHED state here describes exact identity resolution. The subsequent motif checks establish whether that anchor participates in the required pattern. Observed nets referenced by failed checks show where roles landed, including split and merged nets.

Stale bindings and structural violations yield `MOTIF_NOT_ADMITTED` with `MATH_WITHHELD`. An added unknown branch, missing/stale E1 association or unsupported correlation yields `MODEL_SCOPE_UNRESOLVED` with `MATH_WITHHELD`. Malformed typed records and rejected canonical graphs raise existing validation errors. The only success is `CANONICAL_MOTIF_MATCHED` and `MATH_EXECUTED_CONDITIONALLY`. It contains the original E1 report and its calculation digest. A withheld result contains no E1 report or calculation digest.

The E1 association must already match the exact current CORE catalog and snapshot digests. E1 owns all numerical assumptions and calculations. Its internal physical provenance stays `NOT_ESTABLISHED`. E2 establishes virtual netlist membership only. Actual component values and receiver loading remain INDETERMINATE, and source drive, power-off and transients are NOT_EVALUATED. Reports remain `TEST_ONLY_NOT_PRODUCTION` and `HARDWARE_COMPATIBILITY_NOT_PROVEN`. The composite catalog has its own locally derived digest. The original B GPIO fact set does not bind to it.

## Replay

```powershell
python -X utf8 -B -m examples.core001c_e2_divider_topology
python -X utf8 -B -m examples.core001c_e2_divider_topology --json
```

The demo generates the admitted in-memory fixture, moves the receiver and return in two separate negative cases, and restores the original wiring. It prints actual CORE nets and links the conditional calculation only to the matching snapshots.
