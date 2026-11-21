"""Acceptance checks for the terminal projection using native engine fixtures."""

import json
import unittest

from pydantic import ValidationError

from inventor_edu.core import compute_nets, create_snapshot, load_catalog, serialize_snapshot, serialize_topology
from inventor_edu.demo_bridge import analyze_hcsr04_wiring
from inventor_edu.gpio_facts import load_gpio_factset
from inventor_edu.gpio_verify import GpioVerificationReport, serialize_gpio_report
from inventor_edu.models import TerminalRef
from inventor_edu.ui_projection import (
    GpioCoverageProjectionItem, GpioFindingProjectionItem, GpioTerminalInspection,
    ProjectionInputError, project_gpio_terminal, serialize_gpio_terminal_inspection,
)
from tests.core001a_fixtures import BOARD, SENSOR, ZERO, encode, part, t
from tests.test_demo001_bridge import two_wires
from tests.test_gpio_capability import CATALOG_PIN, DATA, FACT_PIN


class GpioTerminalProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(
            (DATA / "devkitc_32e_catalog.json").read_bytes(), expected_sha256=CATALOG_PIN,
        )
        cls.facts = load_gpio_factset((DATA / "devkitc_32e_facts.json").read_bytes())
        cls.parts = (part(cls.catalog, "board", BOARD), part(cls.catalog, "sensor", SENSOR))

    def native_case(self, contact="J2.5", *, catalog_pin=CATALOG_PIN, fact_pin=FACT_PIN):
        snapshot = create_snapshot(self.catalog, instances=self.parts, junctions=(), conductors=two_wires(contact))
        topology = compute_nets(self.catalog, snapshot)
        report = analyze_hcsr04_wiring(self.catalog, snapshot, self.facts, catalog_pin, fact_pin).gpio_report
        self.assertIsInstance(report, GpioVerificationReport)
        return snapshot, topology, report

    def assert_projection_error(self, code, topology, report, terminal):
        with self.assertRaises(ProjectionInputError) as caught:
            project_gpio_terminal(topology, report, terminal)
        self.assertEqual(caught.exception.code, code)
        self.assertEqual(str(caught.exception), code)

    def test_T02A_01_real_output_failure_and_separate_electrical_coverage(self):
        _, topology, report = self.native_case()
        terminal = t("board", "J2.5")
        items = {item.record.rule_id: item for item in project_gpio_terminal(topology, report, terminal).records}
        capability = items["PHYSICAL_CAPABILITY"]
        coverage = items["ELECTRICAL_COMPATIBILITY"]
        self.assertIs(type(capability), GpioFindingProjectionItem)
        self.assertEqual((capability.kind, capability.record.coverage, capability.record.status,
                          capability.record.reason_code),
                         ("GPIO_FINDING", "EVALUATED", "FAIL", "OUTPUT_NOT_CAPABLE"))
        self.assertIs(type(coverage), GpioCoverageProjectionItem)
        self.assertEqual((coverage.kind, coverage.record.coverage, coverage.record.reason_code),
                         ("GPIO_COVERAGE", "NOT_EVALUATED", "ELECTRICAL_CHECK_DELEGATED"))
        self.assertTrue(all(item.record.terminal == terminal for item in items.values()))

    def test_T02A_02_corrected_output_pass_stays_scoped(self):
        _, topology, report = self.native_case("J3.9")
        result = project_gpio_terminal(topology, report, t("board", "J3.9"))
        rows = {item.record.rule_id: item.record for item in result.records}
        capability = rows["PHYSICAL_CAPABILITY"]
        self.assertEqual((capability.status, capability.reason_code), ("PASS", "CAPABILITY_CONFIRMED"))
        self.assertEqual(rows["ELECTRICAL_COMPATIBILITY"].coverage, "NOT_EVALUATED")
        self.assertEqual(rows["BOARD_AVAILABILITY"].status, "UNKNOWN")
        self.assertNotIn(b"SAFE", serialize_gpio_terminal_inspection(result))

    def test_T02A_03_exact_payloads_and_native_coverage_id(self):
        _, topology, report = self.native_case()
        terminal = t("board", "J2.5")
        result = project_gpio_terminal(topology, report, terminal)
        native = {record.finding_id: record for record in report.findings + report.coverage
                  if record.terminal == terminal}
        serialized = json.loads(serialize_gpio_terminal_inspection(result))
        self.assertEqual({item["record"]["finding_id"] for item in serialized["records"]}, set(native))
        self.assertEqual(len(serialized["records"]), len(native))
        for item in serialized["records"]:
            payload = item["record"]
            self.assertEqual(payload, native[payload["finding_id"]].model_dump(mode="json"))
            if item["kind"] == "GPIO_COVERAGE":
                self.assertIn("finding_id", payload)
                self.assertNotIn("status", payload)
                self.assertNotIn("severity", payload)

    def test_T02A_04_copies_native_net_and_members(self):
        _, topology, report = self.native_case()
        result = project_gpio_terminal(topology, report, t("board", "J2.5"))
        mapping = dict(topology.terminal_to_net)
        self.assertEqual(result.net_id, mapping["T:board/J2.5"])
        self.assertEqual(result.net_id, mapping["T:sensor/Trig"])
        self.assertEqual(result.net_members, next(net.members for net in topology.nets if net.net_id == result.net_id))
        self.assertEqual(set(result.net_members), {"T:board/J2.5", "T:sensor/Trig"})

    def test_T02A_05_terminal_absent_from_topology(self):
        _, topology, report = self.native_case()
        self.assert_projection_error("PROJECTION_TERMINAL_NOT_IN_TOPOLOGY", topology, report, t("board", "J2.99"))

    def test_T02A_06_terminal_with_no_records(self):
        _, topology, report = self.native_case()
        result = project_gpio_terminal(topology, report, t("sensor", "Trig"))
        self.assertEqual(result.net_id, dict(topology.terminal_to_net)["T:sensor/Trig"])
        self.assertEqual(result.records, ())
        self.assertEqual(json.loads(serialize_gpio_terminal_inspection(result))["records"], [])

    def test_T02A_07_mismatched_snapshot_precedes_missing_selection(self):
        _, topology, report = self.native_case()
        forged = topology.model_copy(update={"snapshot_sha256": ZERO})
        for terminal in (t("board", "J2.5"), t("absent", "contact")):
            with self.subTest(terminal=terminal):
                self.assert_projection_error("PROJECTION_SNAPSHOT_MISMATCH", forged, report, terminal)

    def test_T02A_08_structural_and_semantic_record_errors(self):
        _, topology, report = self.native_case()
        selection = t("board", "J2.5")
        for field in ("findings", "coverage"):
            records = getattr(report, field)
            index = next(i for i, record in enumerate(records) if record.terminal == t("board", "J3.8"))
            original = records[index]
            for name, value in (
                ("snapshot_digest", ZERO), ("catalog_digest", ZERO), ("factset_digest", ZERO),
                ("affected_net", dict(topology.terminal_to_net)["T:board/J2.5"]),
                ("ruleset_version", "gpio-capability-v2"),
            ):
                with self.subTest(collection=field, field=name):
                    altered = original.model_copy(update={name: value})
                    forged = report.model_copy(update={field: records[:index] + (altered,) + records[index + 1:]})
                    if name == "ruleset_version":
                        self.assert_projection_error("PROJECTION_INVALID_INPUT", topology, forged, selection)
                    else:
                        GpioVerificationReport.model_validate(forged, strict=True)
                        self.assert_projection_error(
                            "PROJECTION_INCONSISTENT_NATIVE_RECORD", topology, forged, selection,
                        )

    def test_T02A_09_inconsistent_membership_and_missing_record_terminal(self):
        _, topology, report = self.native_case()
        terminal = t("board", "J2.5")
        selected_net_id = dict(topology.terminal_to_net)["T:board/J2.5"]
        native_net = next(net for net in topology.nets if net.net_id == selected_net_id)
        other_nets = tuple(net for net in topology.nets if net is not native_net)
        for changes in (
            {"nets": other_nets},
            {"nets": (*other_nets, native_net.model_copy(update={"members": ("T:sensor/Trig",)}))},
            {"nets": (*topology.nets, native_net)},
            {"terminal_to_net": (*topology.terminal_to_net, ("T:board/J2.5", selected_net_id))},
            {"terminal_to_net": tuple(pair for pair in topology.terminal_to_net if pair[0] != "T:sensor/Trig")},
            {"nets": tuple(net for net in topology.nets
                           if net.net_id != dict(topology.terminal_to_net)["T:board/J3.8"])},
        ):
            with self.subTest(changed_fields=tuple(changes)):
                forged = topology.model_copy(update=changes)
                self.assert_projection_error("PROJECTION_INCONSISTENT_TOPOLOGY", forged, report, terminal)

        original = report.coverage[0]
        for wrong_terminal in (t("board", "J3.99"), t("board", "J2.19")):
            with self.subTest(record_terminal=wrong_terminal):
                altered = original.model_copy(update={"terminal": wrong_terminal})
                forged = report.model_copy(update={"coverage": (altered, *report.coverage[1:])})
                self.assert_projection_error("PROJECTION_INCONSISTENT_NATIVE_RECORD", topology, forged, terminal)

    def test_T02A_10_record_id_duplicates_include_other_terminals(self):
        _, topology, report = self.native_case()
        selection = t("board", "J2.5")
        echo_coverage = next(coverage for coverage in report.coverage if coverage.terminal == t("board", "J3.8"))
        cross_kind_duplicate = echo_coverage.model_copy(update={"finding_id": report.findings[0].finding_id})
        for changes in (
            {"coverage": (report.coverage[0], *report.coverage)},
            {"findings": (report.findings[0], *report.findings)},
            {"coverage": tuple(cross_kind_duplicate if row is echo_coverage else row for row in report.coverage)},
        ):
            with self.subTest(changed_fields=tuple(changes)):
                forged = report.model_copy(update=changes)
                self.assert_projection_error("PROJECTION_DUPLICATE_RECORD_ID", topology, forged, selection)

    def test_T02A_11_canonical_bytes_and_native_round_trip(self):
        _, topology, report = self.native_case()
        selection = t("board", "J2.5")
        inspection = project_gpio_terminal(topology, report, selection)
        raw = serialize_gpio_terminal_inspection(inspection)
        keys = [(row.record.requirement_id, row.record.rule_id, row.kind, row.record.finding_id)
                for row in inspection.records]
        self.assertEqual(keys, sorted(keys))
        self.assertEqual(raw, encode(json.loads(raw)))
        self.assertEqual(raw, serialize_gpio_terminal_inspection(project_gpio_terminal(topology, report, selection)))
        reversed_report = GpioVerificationReport.model_validate({
            **report.model_dump(), "findings": report.findings[::-1], "coverage": report.coverage[::-1],
        }, strict=True)
        self.assertEqual(raw, serialize_gpio_terminal_inspection(
            project_gpio_terminal(topology, reversed_report, selection),
        ))
        restored = GpioTerminalInspection.model_validate_json(raw, strict=True)
        self.assertEqual(restored, inspection)
        self.assertEqual(raw, serialize_gpio_terminal_inspection(restored))

    def test_T02A_12_read_only_exact_native_types_and_precedence(self):
        snapshot, topology, report = self.native_case()
        terminal = t("board", "J2.5")
        sources = (serialize_snapshot(snapshot), serialize_topology(topology), serialize_gpio_report(report))
        digests = (report.snapshot_digest, report.catalog_digest, report.factset_digest)
        result = project_gpio_terminal(topology, report, terminal)
        self.assertEqual(sources, (serialize_snapshot(snapshot), serialize_topology(topology), serialize_gpio_report(report)))
        self.assertEqual((result.snapshot_digest, result.catalog_digest, result.factset_digest), digests)
        self.assertEqual(set(result.model_dump()), {
            "schema_version", "terminal", "net_id", "net_members", "snapshot_digest",
            "catalog_digest", "factset_digest", "ruleset_version", "records",
        })
        with self.assertRaises(ValidationError):
            result.net_id = "different"
        with self.assertRaises(ValidationError):
            GpioTerminalInspection.model_validate({**result.model_dump(), "extra": False})

        class TerminalSubclass(TerminalRef):
            pass

        for args in (
            (topology.model_dump(), report, terminal), (topology, report.model_dump(), terminal),
            (topology, report, terminal.model_dump()),
            (topology, report, TerminalSubclass(instance_id="board", terminal_id="J2.5")),
            (topology, report, terminal.model_copy(update={"terminal_id": "unsafe input"})),
            (topology, report.model_copy(update={"catalog_digest": "invalid digest"}), terminal),
            (topology.model_copy(update={"snapshot_sha256": ZERO}),
             report.model_copy(update={"ruleset_version": "wrong"}), terminal),
        ):
            with self.subTest(types=tuple(type(value).__name__ for value in args)):
                self.assert_projection_error("PROJECTION_INVALID_INPUT", *args)

    def test_T02A_13_preserves_native_unknown_and_coverage_without_pins(self):
        terminal = t("board", "J3.9")
        for kwargs, reason in (
            ({"catalog_pin": None}, "UNTRUSTED_CATALOG"),
            ({"fact_pin": None}, "UNTRUSTED_FACTSET"),
        ):
            with self.subTest(reason=reason):
                _, topology, report = self.native_case("J3.9", **kwargs)
                result = project_gpio_terminal(topology, report, terminal)
                findings = [item.record for item in result.records if item.kind == "GPIO_FINDING"]
                self.assertTrue(findings)
                self.assertEqual({(row.status, row.reason_code) for row in findings}, {("UNKNOWN", reason)})
                coverage = [item.record for item in result.records if item.kind == "GPIO_COVERAGE"]
                self.assertEqual(coverage, [row for row in report.coverage if row.terminal == terminal])
                self.assertTrue(coverage)
                self.assertTrue(all(row.coverage == "NOT_EVALUATED" for row in coverage))

    def test_T02A_14_copies_evidence_ids_without_resolving_urls(self):
        _, topology, report = self.native_case("J3.9")
        terminal = t("board", "J3.9")
        result = project_gpio_terminal(topology, report, terminal)
        expected = {row.finding_id: row.evidence_claims
                    for row in report.findings + report.coverage if row.terminal == terminal}
        self.assertTrue(any(expected.values()))
        self.assertEqual({row.record.finding_id: row.record.evidence_claims for row in result.records}, expected)
        raw = serialize_gpio_terminal_inspection(result)
        for marker in (b"http://", b"https://", b'"source_url"', b'"citation"'):
            self.assertNotIn(marker, raw)
