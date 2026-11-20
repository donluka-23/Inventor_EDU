"""Independent E1-01 through E1-18 oracles for the bounded sidecar model."""

from decimal import Context, Decimal, localcontext
from fractions import Fraction
from itertools import product
import json
import unittest

from pydantic import ValidationError

from examples.core001c_e1_voltage_cases import fixture_cases
from examples.edu001_learning_cycle import load_fixture
from inventor_edu.core import compute_nets, create_snapshot
from inventor_edu.voltage_model import (
    AssumptionRecord, IdealDividerHypothesis, ResistanceInterval, SnapshotAssociation, ThresholdHypothesis,
    VoltageInterval, VoltageModelInputError, evaluate_ideal_divider,
)
from tests.core001a_fixtures import t, wire

D = Decimal
F = Fraction


def voltage(low, high=None, unit="V", key="input"):
    return VoltageInterval(lower=D(low), upper=D(low if high is None else high), unit=unit, assumption_id=key)


def resistor(value, high=None, unit="kΩ", tolerance="0"):
    return ResistanceInterval(lower=D(value), upper=D(value if high is None else high), unit=unit,
                              tolerance_percent=D(tolerance), assumption_id="resistors")


def hypothesis(vin=None, top=None, bottom=None, threshold=None, **updates):
    assumptions = tuple(AssumptionRecord(record_id=key, provenance="MODEL_ASSUMPTION",
                                         description=f"Test-only {key}.", condition="Bounded model fixture.")
                        for key in ("ideal", "input", "resistors", "vih"))
    values = dict(hypothesis_id="independent-oracle", scope="IDEAL_DC_UNLOADED_2R", model_assumption_id="ideal",
                  parameter_relationship="INDEPENDENT", input_voltage=vin or voltage("5"),
                  r_top=top or resistor("10"), r_bottom=bottom or resistor("10"), assumptions=assumptions,
                  threshold=threshold)
    return IdealDividerHypothesis(**(values | updates))


def exact(item):
    return F(item.numerator, item.denominator)


def status(report, rule):
    return next(item for item in report.findings if item.rule_id == rule)


class VoltageModelTests(unittest.TestCase):
    def test_E1_01_equal_resistors(self):
        result = evaluate_ideal_divider(hypothesis())
        self.assertEqual(status(result, "MODEL_EQUATION").status, "COMPLETED")
        self.assertEqual(result.calculation.output_voltage.lower.unit, "V")
        self.assertEqual(exact(result.calculation.output_voltage.lower), F(5, 2))
        self.assertEqual(exact(result.calculation.output_voltage.upper), F(5, 2))

    def test_E1_02_six_point_eight_kilohm_top(self):
        result = evaluate_ideal_divider(hypothesis(top=resistor("6.8")))
        self.assertEqual(exact(result.calculation.output_voltage.lower), F(125, 42))
        self.assertEqual(result.calculation.output_voltage.lower.decimal_12dp, "2.976190476190")

    def test_E1_03_swapped_resistors(self):
        result = evaluate_ideal_divider(hypothesis(bottom=resistor("6.8")))
        self.assertEqual(exact(result.calculation.output_voltage.lower), F(85, 42))
        self.assertEqual(result.calculation.output_voltage.lower.decimal_12dp, "2.023809523810")

    def test_E1_04_tolerance_corners_match_exhaustive_kcl_oracle(self):
        case = hypothesis(vin=voltage("4.5", "5.25"), top=resistor("6.8", tolerance="1"),
                          bottom=resistor("10", tolerance="1"))
        result = evaluate_ideal_divider(case).calculation
        corners = [(v / a) / (F(1, a) + F(1, b)) for v, a, b in
                   product((F(9, 2), F(21, 4)), (6732, 6868), (9900, 10100))]
        self.assertEqual((min(corners), max(corners)), (F(22275, 8384), F(53025, 16832)))
        self.assertEqual((exact(result.output_voltage.lower), exact(result.output_voltage.upper)),
                         (min(corners), max(corners)))
        self.assertEqual(exact(result.r_top_effective.lower), 6732)
        self.assertEqual(exact(result.r_bottom_effective.upper), 10100)

    def test_E1_05_negative_high_distance_is_a_model_result(self):
        threshold = ThresholdHypothesis(required_high=voltage("2.55", key="vih"))
        result = evaluate_ideal_divider(hypothesis(threshold=threshold))
        self.assertEqual(exact(result.calculation.high_margin), -F(1, 20))
        self.assertIs(result.calculation.assumed_high_requirement_met, False)
        self.assertEqual(status(result, "MODEL_HIGH_MARGIN").status, "NEGATIVE")
        self.assertEqual(status(result, "HARDWARE_LOGIC_LOW").status, "INDETERMINATE")

    def test_E1_06_positive_high_distance_uses_required_upper_bound(self):
        threshold = ThresholdHypothesis(required_high=voltage("2.4", "2.55", key="vih"))
        result = evaluate_ideal_divider(hypothesis(top=resistor("6.8"), threshold=threshold))
        self.assertEqual(exact(result.calculation.high_margin), F(179, 420))
        self.assertIs(result.calculation.assumed_high_requirement_met, True)
        self.assertEqual(status(result, "MODEL_HIGH_MARGIN").qualification, "CONDITIONAL_ON_ASSUMPTIONS")
        self.assertEqual(status(result, "HARDWARE_LOGIC_HIGH").status, "INDETERMINATE")

    def test_E1_07_equality_and_subdisplay_precision_sign(self):
        for value, sign in (("2.5", "ZERO"), ("2.5000000000001", "NEGATIVE")):
            with self.subTest(value=value), localcontext(Context(prec=2)):
                threshold = ThresholdHypothesis(required_high=voltage(value, key="vih"))
                report = evaluate_ideal_divider(hypothesis(threshold=threshold))
                self.assertEqual(status(report, "MODEL_HIGH_MARGIN").status, sign)
                self.assertEqual(report.calculation.high_margin.decimal_12dp, "0.000000000000")
                self.assertIs(report.calculation.assumed_high_requirement_met, sign == "ZERO")
        for value, display in (("0.000000000001", "0.000000000000"), ("0.000000000003", "0.000000000002")):
            result = evaluate_ideal_divider(hypothesis(vin=voltage(value)))
            self.assertEqual(result.calculation.output_voltage.lower.decimal_12dp, display)

    def test_E1_08_explicit_unit_conversion_and_dimension_rejection(self):
        left = evaluate_ideal_divider(hypothesis(vin=voltage("0.05")))
        right = evaluate_ideal_divider(hypothesis(vin=voltage("50", unit="mV"), top=resistor("10000", unit="ohm")))
        self.assertEqual(left.calculation, right.calculation)
        self.assertEqual(exact(right.calculation.output_voltage.lower), F(1, 40))
        with self.assertRaises(ValidationError):
            voltage("50", unit="mA")
        with self.assertRaises(ValidationError):
            resistor("10", unit="mV")

    def test_E1_09_missing_maker_voh_preserves_indeterminate_hardware_high(self):
        case = fixture_cases()[0]
        result = evaluate_ideal_divider(case)
        self.assertEqual(exact(result.calculation.input_voltage.lower), 5)
        findings = status(result, "HARDWARE_LOGIC_HIGH")
        self.assertEqual(findings.status, "INDETERMINATE")
        self.assertIn("maker_voh_min_under_load", findings.missing_prerequisites)
        with self.assertRaisesRegex(VoltageModelInputError, "INVALID_DIVIDER_HYPOTHESIS"):
            evaluate_ideal_divider(case.model_copy(update={
                "input_voltage": case.input_voltage.model_copy(update={"assumption_id": "retail-context"}),
            }))

    def test_E1_10_supply_document_cannot_establish_pin_stress(self):
        case = fixture_cases()[1]
        document = next(item for item in case.assumptions if item.record_id == "supply-context")
        self.assertEqual(document.provenance, "MANUFACTURER_DOCUMENT")
        self.assertIn("VDD33", document.description)
        findings = status(evaluate_ideal_divider(case), "GPIO_PIN_STRESS")
        self.assertEqual(findings.status, "INDETERMINATE")
        self.assertIn("pin_specific_absolute_input_limits", findings.missing_prerequisites)

    def test_E1_11_reject_malformed_or_unbounded_inputs(self):
        constructors = (
            lambda: resistor("0"), lambda: resistor("-1"), lambda: resistor("3", "2"),
            lambda: resistor("1", tolerance="-1"), lambda: resistor("1", tolerance="100"),
            lambda: resistor("NaN"), lambda: voltage("Infinity"), lambda: voltage("4", "3"),
            lambda: voltage("-1"), lambda: voltage("0E+80"), lambda: voltage("1.1E+12"),
            lambda: VoltageInterval(lower=0.1, upper=D("0.2"), unit="V", assumption_id="input"),
            lambda: VoltageInterval.model_validate_json('{"lower":0.1,"upper":"0.2","unit":"V","assumption_id":"input"}'),
            lambda: hypothesis(scope="LOADED"), lambda: hypothesis(scope=None),
            lambda: hypothesis(model_assumption_id="missing"), lambda: hypothesis(assumptions=()),
        )
        for constructor in constructors:
            with self.subTest(check=constructor), self.assertRaises(ValidationError):
                constructor()
        invalid = hypothesis().model_copy(update={"r_top": resistor("1").model_copy(update={"lower": D("0")})})
        with self.assertRaises(VoltageModelInputError):
            evaluate_ideal_divider(invalid)

    def test_E1_12_low_high_applicability_and_unmodeled_physics_are_distinct(self):
        report = evaluate_ideal_divider(hypothesis())
        for rule in ("HARDWARE_LOGIC_HIGH", "HARDWARE_LOGIC_LOW", "SIGNAL_APPLICABILITY"):
            self.assertEqual(status(report, rule).status, "INDETERMINATE")
        self.assertIn("maker_vol_max_under_load", status(report, "HARDWARE_LOGIC_LOW").missing_prerequisites)
        for rule in ("MODEL_HIGH_MARGIN", "SOURCE_DRIVE_CURRENT", "POWER_OFF", "TRANSIENT"):
            self.assertEqual(status(report, rule).status, "NOT_EVALUATED")
        self.assertIsNone(report.calculation.high_margin)

    def test_E1_13_correlated_envelope_blocks_rectangular_corners(self):
        case = hypothesis(vin=voltage("4", "5"), threshold=ThresholdHypothesis(required_high=voltage("2", key="vih")),
                          parameter_relationship="CORRELATED")
        report = evaluate_ideal_divider(case)
        self.assertIsNone(report.calculation.output_voltage)
        self.assertIsNone(report.calculation.assumed_high_requirement_met)
        for rule in ("MODEL_EQUATION", "MODEL_HIGH_MARGIN"):
            row = status(report, rule)
            self.assertEqual((row.status, row.reason_code), ("INDETERMINATE", "JOINT_ENVELOPE_REQUIRED"))

    def test_E1_14_synthetic_generic_fixture_has_no_esp32_dependency(self):
        case = hypothesis(vin=voltage("12"), top=resistor("2"), bottom=resistor("4"),
                          threshold=ThresholdHypothesis(required_high=voltage("7", key="vih")),
                          hypothesis_id="synthetic-receiver-X")
        report = evaluate_ideal_divider(case)
        self.assertEqual(exact(report.calculation.output_voltage.lower), 8)
        self.assertEqual(exact(report.calculation.high_margin), 1)
        self.assertIsNone(report.hypothesis.association)

    def test_E1_15_canonical_order_and_changed_assumptions(self):
        case = hypothesis()
        doc = case.model_dump(mode="json")
        doc["assumptions"].reverse()
        reordered = IdealDividerHypothesis.model_validate_json(json.dumps(dict(reversed(tuple(doc.items())))))
        original = evaluate_ideal_divider(case)
        self.assertEqual(original, evaluate_ideal_divider(reordered))
        amended = case.model_copy(update={"assumptions": (
            case.assumptions[0].model_copy(update={"description": "Different provenance."}), *case.assumptions[1:],
        )})
        changed = evaluate_ideal_divider(amended)
        self.assertEqual(original.calculation, changed.calculation)
        self.assertNotEqual(original.calculation_digest, changed.calculation_digest)

    def test_E1_16_changed_real_snapshot_is_a_distinct_association(self):
        catalog, _, instances = load_fixture()
        first = create_snapshot(catalog, instances=instances, junctions=(), conductors=())
        second = create_snapshot(catalog, instances=instances, junctions=(),
                                 conductors=(wire("echo", t("sensor", "Echo"), t("board", "J3.8")),))
        reports = [evaluate_ideal_divider(hypothesis(association=SnapshotAssociation.from_core(catalog, graph)))
                   for graph in (first, second)]
        self.assertEqual(reports[0].calculation, reports[1].calculation)
        self.assertNotEqual(reports[0].calculation_digest, reports[1].calculation_digest)
        self.assertEqual([report.physical_network_provenance for report in reports], ["NOT_ESTABLISHED"] * 2)

    def test_E1_17_existing_core_fixture_has_no_resistor_instances(self):
        catalog, _, instances = load_fixture()
        graph = create_snapshot(catalog, instances=instances, junctions=(), conductors=(
            wire("syn-TRIG_OUTPUT", t("sensor", "Trig"), t("board", "J3.9")),
            wire("syn-ECHO_INPUT", t("sensor", "Echo"), t("board", "J3.8")),
        ))
        associated = fixture_cases()[0]
        self.assertEqual(associated.association.snapshot_digest, compute_nets(catalog, graph).snapshot_sha256)
        self.assertEqual({item.instance_id for item in graph.instances}, {"board", "sensor"})
        report = evaluate_ideal_divider(associated)
        self.assertEqual(status(report, "NETWORK_PHYSICALLY_REPRESENTED").status, "NOT_ESTABLISHED")
        self.assertNotIn("net_id", report.model_dump())

    def test_E1_18_no_real_hardware_acceptance_even_with_declared_guarantee(self):
        for case in fixture_cases():
            extra = AssumptionRecord(record_id="unadmitted-guarantee", provenance="MANUFACTURER_GUARANTEE",
                                     description="Negative control declaration only.", condition="No admitted device facts.",
                                     source_ref="test", revision="test", locator="test")
            result = evaluate_ideal_divider(case.model_copy(update={"assumptions": (*case.assumptions, extra)}))
            fields = result.model_dump_json()
            for forbidden in ('"PASS"', "SAFE", "READY_TO_BUILD", "FULLY_COMPATIBLE", "HARDWARE_VERIFIED"):
                self.assertNotIn(forbidden, fields)
            self.assertEqual(result.explanation_code, "NOT_PROVEN_HARDWARE_COMPATIBILITY")
            self.assertTrue(all(row.calculation_digest == result.calculation_digest for row in result.findings))
