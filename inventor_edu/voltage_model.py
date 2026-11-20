"""Exact, conditional mathematics for an ideal unloaded two-resistor divider."""

from decimal import Decimal, InvalidOperation
from fractions import Fraction
from typing import Annotated, Literal

from pydantic import BeforeValidator, Field, ValidationError, ValidationInfo, model_validator

from .core import compute_nets
from .gpio_facts import canonical_json, digest_bytes
from .models import CatalogSnapshot, CircuitSnapshot, Digest, Identifier, Nonempty, Record

MODEL_VERSION = "ideal-divider-e1-v1"
PLACES = 12
Unit = Literal["V", "ohm"]
Rule = Literal[
    "MODEL_EQUATION", "MODEL_HIGH_MARGIN", "HARDWARE_LOGIC_HIGH", "HARDWARE_LOGIC_LOW",
    "SIGNAL_APPLICABILITY", "GPIO_PIN_STRESS", "SOURCE_DRIVE_CURRENT", "POWER_OFF", "TRANSIENT",
    "NETWORK_PHYSICALLY_REPRESENTED",
]
Status = Literal[
    "COMPLETED", "POSITIVE", "NEGATIVE", "ZERO", "INDETERMINATE", "NOT_EVALUATED", "NOT_ESTABLISHED",
]


class VoltageModelInputError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _bounded_decimal(value: object, info: ValidationInfo) -> Decimal:
    if info.mode == "json" and isinstance(value, str) and len(value) <= 96:
        try:
            value = Decimal(value)
        except InvalidOperation as exc:
            raise ValueError("INVALID_DECIMAL") from exc
    if not isinstance(value, Decimal) or not value.is_finite():
        raise ValueError("FINITE_DECIMAL_REQUIRED")
    parts = value.as_tuple()
    if len(parts.digits) > 32 or not -64 <= parts.exponent <= 64 or value.copy_abs() > Decimal("1e12"):
        raise ValueError("DECIMAL_OUT_OF_RANGE")
    return value


BoundedDecimal = Annotated[Decimal, BeforeValidator(_bounded_decimal)]


class VoltageInterval(Record):
    lower: BoundedDecimal
    upper: BoundedDecimal
    unit: Literal["V", "mV"]
    assumption_id: Identifier

    @model_validator(mode="after")
    def _bounds(self):
        if not 0 <= self.lower <= self.upper:
            raise ValueError("INVALID_VOLTAGE_BOUNDS")
        return self


class ResistanceInterval(Record):
    lower: BoundedDecimal
    upper: BoundedDecimal
    unit: Literal["ohm", "kΩ"]
    assumption_id: Identifier
    tolerance_percent: BoundedDecimal = Decimal("0")

    @model_validator(mode="after")
    def _bounds(self):
        if not 0 < self.lower <= self.upper:
            raise ValueError("INVALID_RESISTANCE_BOUNDS")
        if not 0 <= self.tolerance_percent < 100:
            raise ValueError("INVALID_TOLERANCE")
        return self


class AssumptionRecord(Record):
    record_id: Identifier
    provenance: Literal[
        "MODEL_ASSUMPTION", "MANUFACTURER_GUARANTEE", "MANUFACTURER_DOCUMENT",
        "RETAILER_DESCRIPTION", "MEASUREMENT", "UNKNOWN",
    ]
    description: Nonempty
    condition: Nonempty
    source_ref: Nonempty | None = None
    revision: Nonempty | None = None
    locator: Nonempty | None = None

    @model_validator(mode="after")
    def _source(self):
        if self.provenance not in {"MODEL_ASSUMPTION", "UNKNOWN"} and not all(
            (self.source_ref, self.revision, self.locator)
        ):
            raise ValueError("CONTEXT_SOURCE_REFERENCE_REQUIRED")
        return self


class ThresholdHypothesis(Record):
    required_high: VoltageInterval


class SnapshotAssociation(Record):
    """Digest reference only. No component or net proof attaches to these fields."""

    catalog_digest: Digest
    snapshot_digest: Digest

    @classmethod
    def from_core(cls, catalog: CatalogSnapshot, snapshot: CircuitSnapshot) -> "SnapshotAssociation":
        topology = compute_nets(catalog, snapshot)
        return cls(catalog_digest=catalog.catalog_digest, snapshot_digest=topology.snapshot_sha256)


class IdealDividerHypothesis(Record):
    hypothesis_id: Identifier
    scope: Literal["IDEAL_DC_UNLOADED_2R"]
    model_assumption_id: Identifier
    parameter_relationship: Literal["INDEPENDENT", "CORRELATED"]
    input_voltage: VoltageInterval
    r_top: ResistanceInterval
    r_bottom: ResistanceInterval
    assumptions: Annotated[tuple[AssumptionRecord, ...], Field(min_length=1, max_length=32)]
    threshold: ThresholdHypothesis | None = None
    association: SnapshotAssociation | None = None

    @model_validator(mode="after")
    def _trace(self):
        records = {record.record_id: record for record in self.assumptions}
        if len(records) != len(self.assumptions):
            raise ValueError("DUPLICATE_PROVENANCE_ID")
        required_ids = {self.model_assumption_id, self.input_voltage.assumption_id,
                        self.r_top.assumption_id, self.r_bottom.assumption_id}
        if self.threshold is not None:
            required_ids.add(self.threshold.required_high.assumption_id)
        if any(key not in records or records[key].provenance != "MODEL_ASSUMPTION" for key in required_ids):
            raise ValueError("NUMERIC_INPUT_REQUIRES_EXPLICIT_MODEL_ASSUMPTION")
        return self


class ExactValue(Record):
    numerator: int
    denominator: int
    decimal_12dp: str
    unit: Unit


class ExactRange(Record):
    lower: ExactValue
    upper: ExactValue


class ModelCalculation(Record):
    input_voltage: ExactRange
    r_top_effective: ExactRange
    r_bottom_effective: ExactRange
    required_high: ExactRange | None
    output_voltage: ExactRange | None
    high_margin: ExactValue | None
    assumed_high_requirement_met: bool | None
    steps: tuple[str, ...]


class ScopedModelFinding(Record):
    rule_id: Rule
    status: Status
    qualification: Literal["MODEL_ONLY", "CONDITIONAL_ON_ASSUMPTIONS", "EVIDENCE_LIMITED"]
    reason_code: Identifier
    calculation_digest: Digest
    missing_prerequisites: tuple[Identifier, ...] = ()


class VoltageModelReport(Record):
    model_version: Literal["ideal-divider-e1-v1"] = MODEL_VERSION
    restriction: Literal["TEST_ONLY_NOT_PRODUCTION"] = "TEST_ONLY_NOT_PRODUCTION"
    qualification: Literal["MODEL_ONLY"] = "MODEL_ONLY"
    explanation_code: Literal["NOT_PROVEN_HARDWARE_COMPATIBILITY"] = "NOT_PROVEN_HARDWARE_COMPATIBILITY"
    physical_network_provenance: Literal["NOT_ESTABLISHED"] = "NOT_ESTABLISHED"
    hypothesis: IdealDividerHypothesis
    calculation: ModelCalculation
    calculation_digest: Digest
    findings: tuple[ScopedModelFinding, ...]


def _exact(value: Fraction, unit: Unit) -> ExactValue:
    scale = 10**PLACES
    rounded = round(value * scale)
    whole, fraction = divmod(abs(rounded), scale)
    sign = "-" if rounded < 0 else ""
    return ExactValue(numerator=value.numerator, denominator=value.denominator,
                      decimal_12dp=f"{sign}{whole}.{fraction:0{PLACES}d}", unit=unit)


def _exact_range(bounds: tuple[Fraction, Fraction], unit: Unit) -> ExactRange:
    return ExactRange(lower=_exact(bounds[0], unit), upper=_exact(bounds[1], unit))


def _volts(interval: VoltageInterval) -> tuple[Fraction, Fraction]:
    factor = 1000 if interval.unit == "mV" else 1
    return Fraction(interval.lower) / factor, Fraction(interval.upper) / factor


def _ohms(interval: ResistanceInterval) -> tuple[Fraction, Fraction]:
    factor = 1000 if interval.unit == "kΩ" else 1
    tolerance = Fraction(interval.tolerance_percent) / 100
    return Fraction(interval.lower) * factor * (1 - tolerance), Fraction(interval.upper) * factor * (1 + tolerance)


def _calculate(hypothesis: IdealDividerHypothesis) -> ModelCalculation:
    vin = _volts(hypothesis.input_voltage)
    top, bottom = _ohms(hypothesis.r_top), _ohms(hypothesis.r_bottom)
    high = None if hypothesis.threshold is None else _volts(hypothesis.threshold.required_high)
    steps = (
        "Convert mV to V and kΩ to ohm before applying the equation.",
        "Expand each resistance interval by its own tolerance: lower*(1-t), upper*(1+t), t=percent/100.",
        "KCL: I_top = I_bottom. KVL: V_in = I*(R_top + R_bottom).",
        "V_out = V_in * R_bottom / (R_top + R_bottom).",
    )
    output = margin = None
    if hypothesis.parameter_relationship == "INDEPENDENT":
        output = (vin[0] * bottom[0] / (top[1] + bottom[0]),
                  vin[1] * bottom[1] / (top[0] + bottom[1]))
        steps += (
            "Lower corner: Vin_min * Rbottom_min / (Rtop_max + Rbottom_min).",
            "Upper corner: Vin_max * Rbottom_max / (Rtop_min + Rbottom_max).",
        )
        if high is not None:
            margin = output[0] - high[1]
            steps += ("Conditional HIGH margin: Vout_min - assumed_VIH_required_max. Equality meets the modeled inequality.",)
    else:
        steps += ("Correlated parameters: no admitted joint envelope, so the rectangular corner method is not applied.",)
    return ModelCalculation(
        input_voltage=_exact_range(vin, "V"), r_top_effective=_exact_range(top, "ohm"),
        r_bottom_effective=_exact_range(bottom, "ohm"), required_high=None if high is None else _exact_range(high, "V"),
        output_voltage=None if output is None else _exact_range(output, "V"),
        high_margin=None if margin is None else _exact(margin, "V"),
        assumed_high_requirement_met=None if margin is None else margin >= 0, steps=steps,
    )


def evaluate_ideal_divider(hypothesis: IdealDividerHypothesis) -> VoltageModelReport:
    """Evaluate DC sidecar assumptions. Source declarations confer no hardware authority."""
    try:
        hypothesis = IdealDividerHypothesis.model_validate(hypothesis)
    except ValidationError as exc:
        raise VoltageModelInputError("INVALID_DIVIDER_HYPOTHESIS") from exc
    hypothesis = hypothesis.model_copy(update={
        "assumptions": tuple(sorted(hypothesis.assumptions, key=lambda row: row.record_id)),
    })
    calculation = _calculate(hypothesis)
    digest = digest_bytes(canonical_json({
        "model_version": MODEL_VERSION, "hypothesis": hypothesis.model_dump(mode="json"),
        "calculation": calculation.model_dump(mode="json"),
    }))
    correlated = calculation.output_voltage is None
    margin = calculation.high_margin
    if correlated:
        high_status, high_reason, high_missing = "INDETERMINATE", "JOINT_ENVELOPE_REQUIRED", ("admitted_joint_envelope",)
    elif margin is None:
        high_status, high_reason, high_missing = "NOT_EVALUATED", "ASSUMED_VIH_REQUIRED", ("assumed_vih_max",)
    else:
        high_status = "NEGATIVE" if margin.numerator < 0 else "POSITIVE" if margin.numerator > 0 else "ZERO"
        high_reason = ("ASSUMED_HIGH_INEQUALITY_UNSATISFIED" if high_status == "NEGATIVE"
                       else "ASSUMED_HIGH_INEQUALITY_SATISFIED")
        high_missing = ()
    rows = (
        ("MODEL_EQUATION", "INDETERMINATE", "MODEL_ONLY", "JOINT_ENVELOPE_REQUIRED", ("admitted_joint_envelope",))
        if correlated else ("MODEL_EQUATION", "COMPLETED", "MODEL_ONLY", "IDEAL_DC_DIVIDER_COMPUTED", ()),
        ("MODEL_HIGH_MARGIN", high_status, "CONDITIONAL_ON_ASSUMPTIONS", high_reason, high_missing),
        ("HARDWARE_LOGIC_HIGH", "INDETERMINATE", "EVIDENCE_LIMITED", "DEVICE_HIGH_ENVELOPE_NOT_ADMITTED",
         ("maker_voh_min_under_load", "receiver_vih_in_applicable_conditions", "exact_board_input_operating_state")),
        ("HARDWARE_LOGIC_LOW", "INDETERMINATE", "EVIDENCE_LIMITED", "DEVICE_LOW_ENVELOPE_NOT_ADMITTED",
         ("maker_vol_max_under_load", "receiver_vil_in_applicable_conditions")),
        ("SIGNAL_APPLICABILITY", "INDETERMINATE", "EVIDENCE_LIMITED", "BOARD_AND_SIGNAL_SCOPE_NOT_ESTABLISHED",
         ("exact_hardware_variant_and_revision", "input_configuration_and_loading", "supply_and_temperature_bounds")),
        ("GPIO_PIN_STRESS", "INDETERMINATE", "EVIDENCE_LIMITED", "PIN_SPECIFIC_STRESS_RATING_REQUIRED",
         ("pin_specific_absolute_input_limits", "pin_clamp_and_injection_limits")),
        ("SOURCE_DRIVE_CURRENT", "NOT_EVALUATED", "EVIDENCE_LIMITED", "SOURCE_DRIVE_MODEL_OUT_OF_SCOPE",
         ("maker_output_current_and_voltage_characteristic",)),
        ("POWER_OFF", "NOT_EVALUATED", "EVIDENCE_LIMITED", "POWER_OFF_MODEL_OUT_OF_SCOPE", ("unpowered_pin_behavior",)),
        ("TRANSIENT", "NOT_EVALUATED", "EVIDENCE_LIMITED", "TRANSIENT_MODEL_OUT_OF_SCOPE",
         ("load_capacitance_and_edge_timing",)),
        ("NETWORK_PHYSICALLY_REPRESENTED", "NOT_ESTABLISHED", "MODEL_ONLY", "HYPOTHESIS_NOT_IN_VERIFIED_NETLIST",
         ("validated_resistor_instances_and_terminal_topology",)),
    )
    findings = tuple(ScopedModelFinding(rule_id=rule, status=status, qualification=qualification,
                                       reason_code=reason, missing_prerequisites=missing, calculation_digest=digest)
                     for rule, status, qualification, reason, missing in rows)
    return VoltageModelReport(hypothesis=hypothesis, calculation=calculation, calculation_digest=digest, findings=findings)
