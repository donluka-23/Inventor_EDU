"""Independent scenario acceptance over actual CORE-001A and B implementations."""

import json
import unittest
from unittest.mock import patch

from inventor_edu import (
    EngineeringModelError, GpioVerificationError, Junction, JunctionRef, compute_nets,
    create_snapshot, load_catalog, load_gpio_factset, restore_snapshot, serialize_gpio_report,
    serialize_snapshot, verify_gpio_requirements,
)
from inventor_edu.demo_bridge import DemoWiringReport, analyze_hcsr04_wiring
from tests.core001a_fixtures import BOARD, SENSOR, part, t, wire
from tests.test_gpio_capability import CATALOG_PIN, DATA, FACT_PIN

CHECKS = {
    "PIN_MAPPING", "PHYSICAL_CAPABILITY", "BOARD_AVAILABILITY",
    "ACTIVE_CONFIGURATION", "ELECTRICAL_COMPATIBILITY",
}


def two_wires(trigger="J2.5"):
    return (wire("trigger", t("board", trigger), t("sensor", "Trig")),
            wire("echo", t("board", "J3.8"), t("sensor", "Echo")))


class DemoBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog((DATA / "devkitc_32e_catalog.json").read_bytes(), expected_sha256=CATALOG_PIN)
        cls.facts = load_gpio_factset((DATA / "devkitc_32e_facts.json").read_bytes())
        cls.parts = (part(cls.catalog, "board", BOARD), part(cls.catalog, "sensor", SENSOR))

    def snapshot(self, conductors=(), *, parts=None, junctions=()):
        return create_snapshot(self.catalog, instances=self.parts if parts is None else parts,
                               junctions=junctions, conductors=conductors)

    def analyze(self, snapshot, catalog_pin=CATALOG_PIN, fact_pin=FACT_PIN):
        return analyze_hcsr04_wiring(self.catalog, snapshot, self.facts, catalog_pin, fact_pin)

    @staticmethod
    def decisions(report, role):
        return {
            f.rule_id: (f.status, f.reason_code) for f in report.gpio_report.findings if f.requirement_id == role
        }

    def test_A01_catalog_physical_refs_and_actual_verifier_receives_every_check(self):
        snapshot = self.snapshot(two_wires())
        with patch("inventor_edu.demo_bridge.verify_gpio_requirements", wraps=verify_gpio_requirements) as verify:
            report = self.analyze(snapshot)
        verify.assert_called_once()
        catalog, circuit, facts, requests, catalog_pin, fact_pin = verify.call_args.args
        self.assertEqual((catalog, circuit, facts, catalog_pin, fact_pin),
                         (self.catalog, snapshot, self.facts, CATALOG_PIN, FACT_PIN))
        self.assertEqual([(r.requirement_id, r.terminal, r.requested_function) for r in requests], [
            ("TRIG_OUTPUT", t("board", "J2.5"), "GPIO_OUT"),
            ("ECHO_INPUT", t("board", "J3.8"), "GPIO_IN"),
        ])
        for request in requests:
            self.assertEqual(len(request.checks), 5)
            self.assertEqual(set(request.checks), CHECKS)
            self.assertEqual(request.operating_state, "ACTIVE")
        expected = verify_gpio_requirements(catalog, circuit, facts, requests, CATALOG_PIN, FACT_PIN)
        self.assertEqual(serialize_gpio_report(report.gpio_report), serialize_gpio_report(expected))
        topology = compute_nets(self.catalog, snapshot)
        self.assertEqual((report.catalog_digest, report.snapshot_digest, report.factset_digest),
                         (CATALOG_PIN, topology.snapshot_sha256, FACT_PIN))
        self.assertEqual(report.authorization_scope, "TEST_ONLY_NOT_PRODUCTION")
        self.assertEqual(tuple(link.sensor_terminal for link in report.links), (t("sensor", "Trig"), t("sensor", "Echo")))
        self.assertEqual(DemoWiringReport.model_validate_json(report.model_dump_json()), report)
        self.assertEqual(set(json.loads(report.model_dump_json())), {
            "scenario_id", "scenario_version", "catalog_digest", "snapshot_digest",
            "factset_digest", "links", "gpio_report", "authorization_scope",
        })

    def test_A02_A03_A04_correction_changes_net_and_replaces_output_failure(self):
        before = self.analyze(self.snapshot(two_wires()))
        after = self.analyze(self.snapshot(two_wires("J3.9")))
        self.assertEqual(before.links[0].board_terminal, t("board", "J2.5"))
        self.assertEqual(after.links[0].board_terminal, t("board", "J3.9"))
        self.assertEqual([link.state for link in before.links + after.links], ["CONNECTED_UNIQUE"] * 4)
        self.assertNotEqual(before.links[0].net_id, after.links[0].net_id)
        self.assertEqual(before.links[1], after.links[1])
        base = {
            "PIN_MAPPING": ("PASS", "MAPPING_CONFIRMED"),
            "BOARD_AVAILABILITY": ("UNKNOWN", "EVIDENCE_MISSING"),
            "ACTIVE_CONFIGURATION": ("UNKNOWN", "ACTIVE_CONFIG_UNKNOWN"),
        }
        self.assertEqual(self.decisions(before, "TRIG_OUTPUT"), base | {
            "PHYSICAL_CAPABILITY": ("FAIL", "OUTPUT_NOT_CAPABLE"),
        })
        expected = base | {"PHYSICAL_CAPABILITY": ("PASS", "CAPABILITY_CONFIRMED")}
        self.assertEqual(self.decisions(after, "TRIG_OUTPUT"), expected)
        self.assertEqual(self.decisions(before, "ECHO_INPUT"), expected)
        self.assertEqual(self.decisions(after, "ECHO_INPUT"), expected)
        self.assertEqual({(c.requirement_id, c.rule_id, c.coverage, c.reason_code) for c in after.gpio_report.coverage}, {
            (role, "ELECTRICAL_COMPATIBILITY", "NOT_EVALUATED", "ELECTRICAL_CHECK_DELEGATED")
            for role in ("TRIG_OUTPUT", "ECHO_INPUT")
        })
        self.assertFalse(any(f.reason_code == "OUTPUT_NOT_CAPABLE" for f in after.gpio_report.findings))

    def test_A05_A06_removing_or_ambiguously_wiring_trig_does_not_evaluate_it(self):
        before = self.analyze(self.snapshot(two_wires()))
        self.assertTrue(self.decisions(before, "TRIG_OUTPUT"))
        missing = self.analyze(self.snapshot(two_wires()[1:]))
        ambiguous = self.analyze(self.snapshot((*two_wires(), wire("extra", t("board", "J3.9"), t("sensor", "Trig")))))
        for report, state in ((missing, "MISSING"), (ambiguous, "AMBIGUOUS")):
            self.assertEqual(report.links[0].state, state)
            self.assertIsNone(report.links[0].board_terminal)
            self.assertEqual(self.decisions(report, "TRIG_OUTPUT"), {})
            self.assertEqual(self.decisions(report, "ECHO_INPUT")["PHYSICAL_CAPABILITY"],
                             ("PASS", "CAPABILITY_CONFIRMED"))
            self.assertEqual({x.requirement_id for x in report.gpio_report.coverage}, {"ECHO_INPUT"})

    def test_A07_shared_signals_on_same_net_are_unresolved(self):
        short = wire("shared", t("sensor", "Trig"), t("sensor", "Echo"))
        for conductors in ((short,), (*two_wires(), short)):
            report = self.analyze(self.snapshot(conductors))
            self.assertEqual(tuple(x.state for x in report.links), ("SHARED_SIGNAL_NET", "SHARED_SIGNAL_NET"))
            self.assertEqual(report.links[0].net_id, report.links[1].net_id)
            self.assertTrue(all(x.board_terminal is None for x in report.links))
            self.assertIsNone(report.gpio_report)

    def test_A08_ground_and_mixed_ground_net_do_not_resolve_to_gpio(self):
        ground = wire("ground", t("board", "J2.14"), t("sensor", "Trig"))
        for conductors in ((ground, two_wires()[1]), (*two_wires("J3.9"), ground)):
            report = self.analyze(self.snapshot(conductors))
            self.assertEqual(report.links[0].state, "NON_GPIO")
            self.assertIsNone(report.links[0].board_terminal)
            self.assertEqual(self.decisions(report, "TRIG_OUTPUT"), {})

    def test_A09_unvalidated_snapshot_with_invalid_contact_raises_core_error(self):
        invalid = self.snapshot().model_copy(update={"conductors": (
            wire("bad", t("board", "J3.99"), t("sensor", "Trig")),
        )})
        with self.assertRaises(EngineeringModelError) as caught:
            self.analyze(invalid)
        self.assertEqual(caught.exception.code, "UNKNOWN_TERMINAL")

    def test_A10_missing_or_wrong_pins_follow_existing_verifier(self):
        snapshot = self.snapshot(two_wires("J3.9"))
        for catalog_pin, fact_pin, reason in (
            (None, FACT_PIN, "UNTRUSTED_CATALOG"), (CATALOG_PIN, None, "UNTRUSTED_FACTSET"),
        ):
            report = self.analyze(snapshot, catalog_pin, fact_pin)
            self.assertTrue(report.gpio_report.findings)
            self.assertEqual({(x.status, x.reason_code) for x in report.gpio_report.findings}, {("UNKNOWN", reason)})
        wrong = "sha256:" + "0" * 64
        for snapshot in (snapshot, self.snapshot()):
            for catalog_pin, fact_pin, code in (
                (wrong, FACT_PIN, "TRUSTED_CATALOG_PIN_MISMATCH"),
                (CATALOG_PIN, wrong, "TRUSTED_FACTSET_PIN_MISMATCH"),
            ):
                with self.assertRaisesRegex(GpioVerificationError, code):
                    self.analyze(snapshot, catalog_pin, fact_pin)

    def test_A11_junction_net_and_reordered_reversed_snapshot_replay(self):
        j, jr = Junction(junction_id="join"), JunctionRef(junction_id="join")
        conductors = (
            wire("segment-a", t("sensor", "Trig"), jr), wire("segment-b", jr, t("board", "J3.9")), two_wires()[1],
        )
        first = self.snapshot(conductors, junctions=(j,))
        second = self.snapshot(tuple(wire(w.connection_id, w.endpoint_b, w.endpoint_a) for w in conductors[::-1]),
                               parts=self.parts[::-1], junctions=(j,))
        raw = serialize_snapshot(first)
        self.assertEqual(raw, serialize_snapshot(second))
        report = self.analyze(second)
        self.assertEqual(report, self.analyze(restore_snapshot(raw, self.catalog)))
        self.assertEqual(report.links[0].board_terminal, t("board", "J3.9"))
        self.assertEqual(report.links[0].net_id,
                         "net:sha256:2c9d5e8a7f486a3114cc6737d1363c90147ef602c0490e70f96822919212ee31")
        self.assertEqual(self.analyze(first).model_dump_json(), report.model_dump_json())

    def test_A12_identical_labels_do_not_change_physical_instance_resolution(self):
        parts = tuple(p.model_copy(update={"user_label": "ერთი სახელი"}) for p in self.parts)
        report = self.analyze(self.snapshot(two_wires(), parts=parts))
        self.assertEqual(report.links[0].sensor_terminal.instance_id, "sensor")
        self.assertEqual(report.links[0].board_terminal.instance_id, "board")
        self.assertEqual({f.terminal.instance_id for f in report.gpio_report.findings}, {"board"})

    def test_exact_profile_is_required_for_each_named_instance(self):
        wrong_sensor = part(self.catalog, "sensor", BOARD)
        with self.assertRaisesRegex(EngineeringModelError, "UNSUPPORTED_DEMO_PROFILE"):
            self.analyze(self.snapshot(parts=(self.parts[0], wrong_sensor)))
        with self.assertRaisesRegex(EngineeringModelError, "UNKNOWN_INSTANCE"):
            self.analyze(self.snapshot(parts=(self.parts[0],)))
