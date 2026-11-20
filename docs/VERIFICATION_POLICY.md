# Verification, evidence and scope of simulation

## Terms
- **Connection model:** nodes/terminals connected by nets.
- **Rules check:** validates declarative conditions such as pin mode, electrical ranges, mandatory connections.
- **Electrical simulation:** computes voltages/currents over a physical mathematical model and specified conditions. May require SPICE models; is NOT firmware execution.
- **Firmware emulation:** processor/peripheral behavior and compatible code execution; does not automatically simulate external components' physics.
- **Safety:** beyond basic ERC; no total-safety claim absent full review and physical measurements.

## Result contract
`PASS`: a specific supported rule holds under recorded assumptions.
`FAIL`: a specific supported rule is violated, show counterexample and affected entities.
`UNKNOWN`: cannot establish result (missing source, version, operating mode, model, or out-of-scope condition).
`NOT_APPLICABLE`: rule does not apply and why.

## Engineering quality requirements
Every numeric parameter carries unit, type of limit (nominal/recommended/absolute-max/etc.), conditions, citation, revision and measurement/uncertainty status. A finding includes a rule ID, model ID, references to nets/pins/parts, calculation steps, assumptions, and an explanation key.

## Test classes per implemented rule
- Positive known fixture.
- Negative known counterexample.
- Boundary value and units.
- Unknown source/variant/mode.
- UI state change and stale-warning disappearance.
- Where practical, cross-check with independent analytical calculation or validated tool/hardware measurement.

## First simulation path
Start without SPICE: deterministic wiring rules and analytical physical laws when exact part data exists. Add an external simulator only after an ADR proves a real case needs it, licenses/model coverage are approved, and a numerical-oracle comparison is available. Do not imply an electrical transient graph reflects actual hardware without a validated model.
