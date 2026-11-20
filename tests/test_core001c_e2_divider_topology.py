"""Independent topology and evidence boundaries for E2."""

from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from examples.core001c_e1_voltage_cases import fixture_cases
from examples.core001c_e2_divider_topology import (
    admit_test_catalog, bind_fixture, contact, primary_fixture, rewire, run_cases, synthetic_definition, wire,
)
from examples.edu001_learning_cycle import CATALOG_PIN, FACTSET_PIN, load_fixture
from inventor_edu.core import compute_nets, create_snapshot
from inventor_edu.divider_topology import bind_ideal_divider_to_snapshot
from inventor_edu.gpio_facts import GpioVerificationError
from inventor_edu.gpio_verify import verify_gpio_requirements
from inventor_edu.models import ComponentInstance, EngineeringModelError, Junction, JunctionRef
from inventor_edu.voltage_model import evaluate_ideal_divider
from tests.core001a_fixtures import ZERO
from tests.test_core001c_e1_voltage_model import hypothesis

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ("T:r-top/high", "T:sensor/Echo")
MID = ("T:board/J3.8", "T:r-bottom/high", "T:r-top/low")
GROUND = ("T:board/J2.14", "T:board/J3.1", "T:board/J3.7", "T:r-bottom/low")


class DividerTopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, cls.instances, cls.roles, cls.wires = primary_fixture()
        cls.scenario = fixture_cases()[1]
        cls.snapshot = cls.graph(cls.wires)
        cls.binding, cls.model = bind_fixture(cls.catalog, cls.snapshot, cls.roles, cls.scenario)
        cls.match = cls.evaluate(cls.snapshot)

    @classmethod
    def graph(cls, wires, *, junctions=(), instances=None):
        return create_snapshot(cls.catalog, instances=cls.instances if instances is None else instances,
                               junctions=junctions, conductors=wires)

    @classmethod
    def evaluate(cls, snapshot, binding=None, model=None):
        if binding is None:
            binding, current = bind_fixture(cls.catalog, snapshot, cls.roles, cls.scenario)
            if model is None:
                model = current
        return bind_ideal_divider_to_snapshot(cls.catalog, snapshot, binding, model or cls.model)

    def assert_withheld(self, report, reason, state="MOTIF_NOT_ADMITTED"):
        self.assertEqual((report.motif_state, report.math_state), (state, "MATH_WITHHELD"))
        self.assertIsNone(report.model_report)
        self.assertIsNone(report.model_digest)
        return next(row for row in report.checks if row.reason_code == reason)

    def test_E2_01_exact_role_identity_and_definition_binding(self):
        result = {row.role: (row.anchor.ref.instance_id, row.anchor.ref.terminal_id) for row in self.match.anchors}
        self.assertEqual(result, {
            "source_out": ("sensor", "Echo"), "receiver_input": ("board", "J3.8"),
            "reference_ground": ("board", "J2.14"), "r_top_hi": ("r-top", "high"),
            "r_top_lo": ("r-top", "low"), "r_bottom_hi": ("r-bottom", "high"), "r_bottom_lo": ("r-bottom", "low"),
        })
        owners = {item.instance_id: item.definition_digest for item in self.instances}
        self.assertTrue(all(row.observed_definition_digest == owners[row.anchor.ref.instance_id]
                            and row.status == "MATCHED" for row in self.match.anchors))
        # The exact reviewed transmitter/receiver definition objects survive composition.
        base, _, _ = load_fixture()
        self.assertEqual(tuple(item for item in self.catalog.definitions
                               if item.definition_id in {row.definition_id for row in base.definitions}), base.definitions)
        self.assertEqual((self.catalog.claims, self.catalog.source_documents), (base.claims, base.source_documents))

    def test_E2_02_both_synthetic_passive_bodies_are_distinct(self):
        parts = {item.instance_id: item for item in self.instances}
        self.assertNotEqual(parts["r-top"].definition_digest, parts["r-bottom"].definition_digest)
        added = tuple(item for item in self.catalog.definitions if item.identity.synthetic_test_data)
        self.assertEqual(len(added), 2)
        self.assertTrue(all(item.device_class == "passive_resistor"
                            and {term.terminal_id for term in item.terminals} == {"high", "low"}
                            for item in added))

    def test_E2_03_exact_independent_net_partition(self):
        observed = {net.net_id: net.members for net in self.match.observed_nets}
        ids = self.match.net_ids
        self.assertEqual(len({ids.source, ids.midpoint, ids.ground}), 3)
        self.assertEqual((observed[ids.source], observed[ids.midpoint], observed[ids.ground]), (SOURCE, MID, GROUND))

    def test_E2_04_resistor_is_not_an_ideal_wire(self):
        locations = dict(compute_nets(self.catalog, self.snapshot).terminal_to_net)
        for resistor in ("r-top", "r-bottom"):
            self.assertNotEqual(locations[f"T:{resistor}/high"], locations[f"T:{resistor}/low"])
        self.assertTrue(all(not device.internal_ideal_ties for device in self.catalog.definitions
                            if device.device_class == "passive_resistor"))

    def test_E2_05_virtual_success_keeps_separate_evidence_limits(self):
        report = self.match
        self.assertEqual(report.motif_state, "CANONICAL_MOTIF_MATCHED")
        self.assertTrue(report.model_values_are_assumptions)
        self.assertTrue(report.actual_component_value_not_admitted)
        self.assertEqual(report.hardware_qualification, "HARDWARE_COMPATIBILITY_NOT_PROVEN")
        self.assertEqual(report.model_report.physical_network_provenance, "NOT_ESTABLISHED")
        self.assertEqual({row.rule_id: row.status for row in report.checks[-5:]},
                         {"ACTUAL_RESISTOR_VALUES": "INDETERMINATE", "RECEIVER_LOADING": "INDETERMINATE",
                          "SOURCE_DRIVE": "NOT_EVALUATED", "POWER_OFF": "NOT_EVALUATED", "TRANSIENT": "NOT_EVALUATED"})

    def test_E2_06_conditional_model_is_the_unchanged_e1_report(self):
        with patch("inventor_edu.divider_topology.evaluate_ideal_divider", wraps=evaluate_ideal_divider) as engine:
            actual = self.evaluate(self.snapshot, self.binding)
        engine.assert_called_once_with(self.model)
        self.assertEqual(actual.model_report, evaluate_ideal_divider(self.model))
        voltage = actual.model_report.calculation.output_voltage.lower
        self.assertEqual(Fraction(voltage.numerator, voltage.denominator), Fraction(125, 42))
        self.assertEqual(actual.math_state, "MATH_EXECUTED_CONDITIONALLY")

    def test_E2_07_two_miswired_endpoints_yield_real_rejected_nets(self):
        cases = (
            ("mid-receiver", "endpoint_a", "r_top_hi", "MID_NET_OPEN_OR_MISROUTED",
             ("T:board/J3.8", "T:r-top/high", "T:sensor/Echo")),
            ("ground-return", "endpoint_b", "source_out", "GROUND_NET_OPEN_OR_MISROUTED",
             ("T:r-bottom/low", "T:r-top/high", "T:sensor/Echo")),
        )
        with patch("inventor_edu.divider_topology.evaluate_ideal_divider") as engine:
            for key, endpoint, target, reason, expected in cases:
                snapshot = self.graph(rewire(self.wires, key, endpoint, self.roles[target]))
                report = self.evaluate(snapshot)
                row = self.assert_withheld(report, reason)
                self.assertNotEqual(report.snapshot_digest, self.match.snapshot_digest)
                net = next(item for item in report.observed_nets if item.members == expected)
                self.assertIn(net.net_id, row.affected_net_ids)
                self.assertIn(key, net.connection_ids)
        engine.assert_not_called()

    def test_E2_08_three_bypass_types_cannot_admit_math(self):
        for a, b, reason in (
            ("r_top_hi", "r_top_lo", "RESISTOR_TERMINALS_SHORTED"),
            ("r_bottom_hi", "r_bottom_lo", "RESISTOR_TERMINALS_SHORTED"),
            ("source_out", "reference_ground", "MOTIF_NETS_MERGED"),
        ):
            with self.subTest(a=a, b=b):
                graph = self.graph((*self.wires, wire("bypass", self.roles[a], self.roles[b])))
                report = self.evaluate(graph)
                failure = self.assert_withheld(report, reason)
                self.assertTrue(any("bypass" in net.connection_ids for net in report.observed_nets
                                    if net.net_id in failure.affected_net_ids))

    def test_E2_09_missing_ground_and_power_contact_fail(self):
        open_graph = self.graph(tuple(item for item in self.wires if item.connection_id != "ground-return"))
        self.assert_withheld(self.evaluate(open_graph), "GROUND_NET_OPEN_OR_MISROUTED")
        bad = self.binding.reference_ground.model_copy(update={"ref": contact("board", "J2.1")})
        self.assert_withheld(self.evaluate(self.snapshot, self.binding.model_copy(update={"reference_ground": bad})),
                             "INVALID_REFERENCE_GROUND")

    def test_E2_10_missing_or_duplicate_instances_and_bad_anchor_pins_fail(self):
        for field, anchor, reason in (
            ("r_top_hi", self.binding.r_top_hi.model_copy(update={"ref": contact("missing-r", "high")}),
             "INSTANCE_NOT_IN_SNAPSHOT"),
            ("r_top_lo", self.binding.r_top_lo.model_copy(update={"ref": contact("r-top", "absent")}),
             "TERMINAL_NOT_IN_SNAPSHOT"),
            ("r_top_lo", self.binding.r_top_lo.model_copy(update={"definition_digest": ZERO}),
             "DEFINITION_DIGEST_MISMATCH"),
            ("r_bottom_hi", self.binding.r_top_hi, "RESISTOR_INSTANCES_NOT_DISTINCT"),
        ):
            with self.subTest(field=field, reason=reason):
                self.assert_withheld(self.evaluate(self.snapshot, self.binding.model_copy(update={field: anchor})), reason)
        with self.assertRaises(EngineeringModelError) as caught:
            duplicate = self.snapshot.model_copy(update={"instances": (*self.instances, self.instances[-1])})
            self.evaluate(duplicate, self.binding)
        self.assertEqual(caught.exception.code, "DUPLICATE_ID")
        # Split one declared arm across two real instances while retaining unique role refs.
        crossed = self.binding.model_copy(update={"r_bottom_lo": self.binding.r_top_lo,
                                                  "r_top_lo": self.binding.r_bottom_lo})
        self.assert_withheld(self.evaluate(self.snapshot, crossed), "NOT_AN_ADMITTED_TWO_TERMINAL_RESISTOR_BODY")

    def test_E2_11_bad_digest_or_absent_stale_model_never_attaches_math(self):
        for digest in ("catalog_digest", "snapshot_digest"):
            self.assert_withheld(self.evaluate(self.snapshot, self.binding.model_copy(update={digest: ZERO})),
                                 "STALE_TOPOLOGY_BINDING")
        for association, reason in ((None, "MODEL_ASSOCIATION_MISSING"),
                                    (self.model.association.model_copy(update={"snapshot_digest": ZERO}), "STALE_MODEL_ASSOCIATION")):
            self.assert_withheld(self.evaluate(self.snapshot, self.binding, self.model.model_copy(update={"association": association})),
                                 reason, "MODEL_SCOPE_UNRESOLVED")
        correlated = self.model.model_copy(update={"parameter_relationship": "CORRELATED"})
        self.assert_withheld(self.evaluate(self.snapshot, self.binding, correlated), "JOINT_ENVELOPE_REQUIRED",
                             "MODEL_SCOPE_UNRESOLVED")

    def test_E2_12_extra_midpoint_power_or_load_is_unresolved(self):
        for terminal in ("Trig", "Vcc"):
            graph = self.graph((*self.wires[:-1], wire("mid-load", self.roles["r_top_lo"], contact("sensor", terminal))))
            report = self.evaluate(graph)
            failure = self.assert_withheld(report, "UNREVIEWED_MID_NET_MEMBERS", "MODEL_SCOPE_UNRESOLVED")
            self.assertEqual(failure.unexpected_members, (f"T:sensor/{terminal}",))
            self.assertIn("mid-load", next(item.connection_ids for item in report.observed_nets
                                          if item.net_id == report.net_ids.midpoint))

    def test_E2_13_extra_source_and_ground_contacts_are_unresolved(self):
        for role, branch, reason in (
            ("source_out", contact("sensor", "Vcc"), "UNREVIEWED_SOURCE_NET_MEMBERS"),
            ("reference_ground", contact("sensor", "Gnd"), "UNREVIEWED_GROUND_NET_MEMBERS"),
        ):
            graph = self.graph((*self.wires, wire("extra-contact", self.roles[role], branch)))
            report = self.evaluate(graph)
            failure = self.assert_withheld(report, reason, "MODEL_SCOPE_UNRESOLVED")
            self.assertEqual(failure.unexpected_members, (f"T:{branch.instance_id}/{branch.terminal_id}",))

    def test_E2_14_reordered_endpoints_and_conductors_are_canonical(self):
        reversed_wires = tuple(wire(item.connection_id, item.endpoint_b, item.endpoint_a)
                               for item in reversed(self.wires))
        self.assertEqual(self.evaluate(self.graph(reversed_wires)), self.match)
        # A CORE junction routes the midpoint without adding an electrical terminal.
        tee = JunctionRef(junction_id="test-tee")
        tee_graph = self.graph((*self.wires[:1], *self.wires[3:],
                                wire("mid-top", self.roles["r_top_lo"], tee),
                                wire("mid-bottom", self.roles["r_bottom_hi"], tee),
                                wire("mid-receiver", self.roles["receiver_input"], tee)),
                               junctions=(Junction(junction_id="test-tee"),))
        with_tee = self.evaluate(tee_graph)
        self.assertEqual(with_tee.net_ids, self.match.net_ids)
        self.assertEqual(with_tee.motif_state, "CANONICAL_MOTIF_MATCHED")
        self.assertNotEqual(with_tee.snapshot_digest, self.match.snapshot_digest)

    def test_E2_15_new_wire_invalidates_old_association_and_revert_recovers(self):
        wrong = rewire(self.wires, "mid-receiver", "endpoint_a", self.roles["r_top_hi"])
        bad = self.graph(wrong)
        self.assert_withheld(self.evaluate(bad, self.binding), "STALE_TOPOLOGY_BINDING")
        self.assert_withheld(self.evaluate(bad, model=self.model), "MID_NET_OPEN_OR_MISROUTED")
        restored = rewire(wrong, "mid-receiver", "endpoint_a", self.roles["r_bottom_hi"])
        self.assertEqual(self.evaluate(self.graph(restored)), self.match)

    def test_E2_16_changed_assumptions_change_e1_digest_not_authority(self):
        top = self.model.r_top.model_copy(update={"lower": self.model.r_bottom.lower, "upper": self.model.r_bottom.upper})
        changed = self.evaluate(self.snapshot, self.binding, self.model.model_copy(update={"r_top": top}))
        self.assertNotEqual(changed.model_digest, self.match.model_digest)
        value = changed.model_report.calculation.output_voltage.lower
        self.assertEqual(Fraction(value.numerator, value.denominator), Fraction(5, 2))
        self.assertTrue(changed.actual_component_value_not_admitted)

    def test_E2_17_synthetic_non_esp32_motif_runs_same_adapter(self):
        defs = (
            synthetic_definition("test-pulse", "pulse_source", (("Q", "output"),)),
            synthetic_definition("test-receiver", "sample_input", (("I", "input"), ("G", "ground"))),
            synthetic_definition("test-upper", "passive_resistor", (("a", "other"), ("b", "other"))),
            synthetic_definition("test-lower", "passive_resistor", (("a", "other"), ("b", "other"))),
        )
        catalog = admit_test_catalog(defs)
        instances = tuple(ComponentInstance(instance_id=key, definition_id=item.definition_id,
                                            definition_digest=item.definition_digest)
                          for key, item in zip(("pulse", "meter", "upper", "lower"), defs, strict=True))
        roles = dict(zip(self.roles, (contact("pulse", "Q"), contact("meter", "I"), contact("meter", "G"),
                                     contact("upper", "a"), contact("upper", "b"), contact("lower", "a"),
                                     contact("lower", "b")), strict=True))
        graph = create_snapshot(catalog, instances=instances, junctions=(), conductors=(
            wire("x", roles["source_out"], roles["r_top_hi"]),
            wire("y", roles["r_top_lo"], roles["receiver_input"]),
            wire("z", roles["receiver_input"], roles["r_bottom_hi"]),
            wire("w", roles["r_bottom_lo"], roles["reference_ground"]),
        ))
        binding, model = bind_fixture(catalog, graph, roles, hypothesis())
        result = bind_ideal_divider_to_snapshot(catalog, graph, binding, model)
        self.assertEqual(result.motif_state, "CANONICAL_MOTIF_MATCHED")
        self.assertEqual({net.members for net in result.observed_nets},
                         {("T:pulse/Q", "T:upper/a"), ("T:lower/a", "T:meter/I", "T:upper/b"),
                          ("T:lower/b", "T:meter/G")})

    def test_E2_18_old_gpio_pins_are_not_authority_for_composite(self):
        _, facts, _ = load_fixture()
        self.assertNotEqual(self.catalog.catalog_digest, CATALOG_PIN)
        self.assertEqual(facts.catalog_digest, CATALOG_PIN)
        for pin, code in ((CATALOG_PIN, "TRUSTED_CATALOG_PIN_MISMATCH"),
                          (self.catalog.catalog_digest, "FACTSET_CATALOG_MISMATCH")):
            with self.assertRaises(GpioVerificationError) as caught:
                verify_gpio_requirements(self.catalog, self.snapshot, facts, (), pin, FACTSET_PIN)
            self.assertEqual(caught.exception.code, code)

    def test_E2_19_rejected_cases_have_no_stale_numeric_or_hardware_verdict(self):
        reports = dict(run_cases())
        for name in ("B1-receiver-on-source", "B2-return-on-source"):
            report = reports[name]
            self.assertIsNone(report.model_report)
            payload = report.model_dump_json()
            for forbidden in ('"SAFE"', '"ELECTRICAL_COMPATIBLE"', '"HARDWARE_HIGH"', '"PHYSICALLY_VERIFIED"',
                              '"PASS"', "2.976190476190"):
                self.assertNotIn(forbidden, payload)

    def test_E2_20_cli_json_deterministic_across_two_processes(self):
        cmd = [sys.executable, "-X", "utf8", "-B", "-m", "examples.core001c_e2_divider_topology", "--json"]
        first, second = (subprocess.run(cmd, cwd=ROOT, capture_output=True, check=True, timeout=10) for _ in range(2))
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual((first.stderr, second.stderr), (b"", b""))
        self.assertIn(b"MATH_EXECUTED_CONDITIONALLY", first.stdout)
        self.assertIn(b"MATH_WITHHELD", first.stdout)
