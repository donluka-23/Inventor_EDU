# CORE-001C-E1 voltage model contract

```python
evaluate_ideal_divider(hypothesis: IdealDividerHypothesis) -> VoltageModelReport
SnapshotAssociation.from_core(catalog: CatalogSnapshot, snapshot: CircuitSnapshot) -> SnapshotAssociation
```

This isolated sidecar models a nonnegative applied DC input, a strictly positive top resistance between source and output, a strictly positive bottom resistance between output and ground, and no output load. `IdealDividerHypothesis` requires the explicit `IDEAL_DC_UNLOADED_2R` scope and an `INDEPENDENT` or `CORRELATED` declaration. An optional `ThresholdHypothesis.required_high` gives the assumed required HIGH interval. The upper endpoint is the comparison threshold.

`VoltageInterval` uses V or mV. `ResistanceInterval` uses ohm or kΩ and allows `0 ≤ tolerance_percent < 100`. Tolerance expands the declared nominal interval using its lower endpoint times `1-t` and upper endpoint times `1+t`, with `t = tolerance_percent/100`. Values are Python `Decimal` instances or decimal strings on the JSON wire. Each finite scalar is limited to 32 coefficient digits, an exponent from −64 to 64 and absolute magnitude at most 10¹² in its declared unit. Inverted bounds, wrong units, floats, unsupported scope, duplicate provenance IDs and missing linked assumptions reject. Immutable record validation rejects malformed constructors. The evaluator wraps invalid hypotheses in `VoltageModelInputError(INVALID_DIVIDER_HYPOTHESIS)`.

The scope and every numerical input reference an explicit `MODEL_ASSUMPTION` record. Contextual manufacturer documents or claimed guarantees, retail descriptions, measurements and unknowns are distinct provenance declarations. They do not change hardware eligibility. Non-assumption source declarations require their source, revision and locator. The calculator performs no manufacturer-evidence admission.

KCL equates both resistor currents. KVL gives `I = Vin / (Rtop + Rbottom)`; multiplying by `Rbottom` gives `Vout`. For nonnegative input, `Vout` is nondecreasing with Vin and bottom resistance and nonincreasing with top resistance. The independent lower corner uses lowest Vin and bottom resistance with highest top resistance. The upper corner reverses those choices. Declared correlations with no admitted joint envelope leave the equation and margin INDETERMINATE.

All computation and comparisons use reduced rational numbers. `ExactValue` carries numerator, denominator, base unit, and a 12-place round-half-to-even display. Comparisons do not use the display. `Vout_min − assumed_VIH_max` classifies the HIGH margin as NEGATIVE, ZERO or POSITIVE. ZERO meets the modeled inequality. This comparison has no real LOW or HIGH guarantee. `ModelCalculation` includes normalized exact inputs, output, margin and ordered derivation steps.

The digest covers the model version, exact derived trace, declared inputs, ordered provenance records and optional digest association. Reordering JSON fields or provenance records does not change the digest. Changing a declared assumption, input representation or snapshot association may change it while the rational math stays identical. `SnapshotAssociation.from_core` uses the existing CORE validator and topology computation to obtain the digest pair. Direct association records are references. Under this contract every scenario has `physical_network_provenance=NOT_ESTABLISHED`.

`VoltageModelReport` is `MODEL_ONLY` and `TEST_ONLY_NOT_PRODUCTION`. Separate findings retain HIGH, LOW, applicability, pin stress, source drive, power-off, transient and physical network limitations, including the missing prerequisites and a reference to the calculation digest. CORE-001B coverage and all existing interfaces stay unchanged.

## Replay

```powershell
python -X utf8 -B -m examples.core001c_e1_voltage_cases
python -X utf8 -B -m examples.core001c_e1_voltage_cases --json
```

The example emits a neutral technical summary or UTF-8 JSON for two nominal proposals and one tolerance envelope. It associates the existing board/sensor wiring but the resistor network exists only in the mathematical hypothesis.
