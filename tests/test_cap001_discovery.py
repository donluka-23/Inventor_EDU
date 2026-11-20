"""Independent fixture oracles for capability discovery and CAP-to-SYN replay."""

import json
import unittest

from pydantic import ValidationError

from inventor_edu import EngineeringModelError, GpioVerificationError, create_snapshot, load_catalog, load_gpio_factset
from inventor_edu.capability_discovery import CapabilityQuery, DiscoveryInputError, discover_gpio_terminals
from inventor_edu.gpio_verify import GpioRequirement, verify_gpio_requirements
from inventor_edu.synthesis import SignalRole, SynthesisRequest, generate_candidates
from tests.core001a_fixtures import BOARD, SENSOR, ZERO, checksum, part, t
from tests.test_gpio_capability import CATALOG_PIN, DATA, FACT_PIN, reseal
from tests.test_syn001_generation import synthetic_fixture


def reviewed_inputs():
    catalog = load_catalog((DATA / "devkitc_32e_catalog.json").read_bytes(), expected_sha256=CATALOG_PIN)
    facts = load_gpio_factset((DATA / "devkitc_32e_facts.json").read_bytes())
    return catalog, part(catalog, "board", BOARD), facts


def make_query(catalog, board, facts, function="GPIO_OUT", requirement_id="drive"):
    return CapabilityQuery(query_id=f"discover-{requirement_id}", requirement_id=requirement_id,
                           board_instance_id=board.instance_id, definition_id=board.definition_id,
                           definition_digest=board.definition_digest, requested_function=function,
                           operating_state="ACTIVE", catalog_digest=catalog.catalog_digest,
                           factset_digest=facts.factset_digest, evidence_scope=facts.review)


def discover(query, inputs, catalog_pin=CATALOG_PIN, fact_pin=FACT_PIN):
    return discover_gpio_terminals(query, *inputs, trusted_catalog_sha256=catalog_pin,
                                   trusted_factset_sha256=fact_pin)


def finding(candidate, rule):
    return next(row for row in candidate.findings if row.rule_id == rule)


def by_contact(report):
    return {candidate.terminal.terminal_id: candidate for candidate in report.candidates}


def run_headless():
    catalog, board, facts = inputs = reviewed_inputs()
    specifications = (
        ("TRIG_OUTPUT", "drive", "Trig", "GPIO_OUT"),
        ("ECHO_INPUT", "listen", "Echo", "GPIO_IN"),
    )
    reports = tuple(discover(make_query(*inputs, function, requirement), inputs)
                    for _, requirement, _, function in specifications)
    roles = tuple(SignalRole(role=role, requirement_id=discovery.query.requirement_id,
                            source_terminal=t("sensor", terminal), function=discovery.query.requested_function,
                            domain=discovery.terminal_domain)
                  for (role, _, terminal, _), discovery in zip(specifications, reports, strict=True))
    request = SynthesisRequest(request_id="discover-ultrasonic",
        requirements_digest=checksum(specifications), catalog_digest=CATALOG_PIN,
        instances=(board, part(catalog, "sensor", SENSOR)), roles=roles, resource_constraint="AllDifferent",
        evidence_scope="TEST_ONLY_SOURCE_REVIEWED", max_nodes=30, max_candidates=20)
    result = generate_candidates(request, catalog, facts, trusted_catalog_sha256=CATALOG_PIN,
                                 trusted_factset_sha256=FACT_PIN)
    return reports, request, result


class CapabilityDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = reviewed_inputs()
        cls.query = make_query(*cls.inputs)
        cls.report = discover(cls.query, cls.inputs)
        cls.contacts = by_contact(cls.report)

    def test_01_exact_catalog_board_and_query(self):
        catalog, board, facts = self.inputs
        self.assertEqual(self.report.query, self.query)
        self.assertEqual((self.query.definition_id, self.query.board_instance_id, self.query.catalog_digest),
                         ("esp32-devkitc-32e-v4", "board", CATALOG_PIN))
        self.assertEqual(self.query.definition_digest, board.definition_digest)
        for field, value, code in (
            ("board_instance_id", "other", "BOARD_REFERENCE_MISMATCH"),
            ("definition_id", "other", "BOARD_REFERENCE_MISMATCH"),
            ("definition_digest", ZERO, "BOARD_REFERENCE_MISMATCH"),
            ("catalog_digest", ZERO, "EVIDENCE_REFERENCE_MISMATCH"),
            ("factset_digest", ZERO, "EVIDENCE_REFERENCE_MISMATCH"),
            ("evidence_scope", "TEST_ONLY_SYNTHETIC", "EVIDENCE_SCOPE_MISMATCH"),
        ):
            with self.subTest(field=field), self.assertRaises(DiscoveryInputError) as caught:
                discover(self.query.model_copy(update={field: value}), self.inputs)
            self.assertEqual(caught.exception.code, code)
        with self.assertRaises(EngineeringModelError) as caught:
            discover(self.query, (catalog, board.model_copy(update={"definition_digest": ZERO}), facts))
        self.assertEqual(caught.exception.code, "CATALOG_DIGEST_MISMATCH")

    def test_02_dynamic_physical_enumeration(self):
        self.assertEqual(self.report.terminal_domain, tuple(t("board", contact)
            for contact in ("J2.5", "J3.14", "J3.19", "J3.8", "J3.9")))
        self.assertEqual(self.contacts["J3.14"].signal_mapping.target_id, "GPIO0")
        self.assertNotIn("J2.14", self.contacts)
        self.assertNotIn("J2.1", self.contacts)

    def test_03_gpio_input_discovery(self):
        report = discover(make_query(*self.inputs, "GPIO_IN", "listen"), self.inputs)
        observed = by_contact(report)["J2.5"]
        self.assertEqual((observed.signal_mapping.target_id, observed.qualification),
                         ("GPIO34", "FUNCTION_CONFIRMED_FOR_STATED_CHECK"))
        self.assertEqual(finding(observed, "PHYSICAL_CAPABILITY").status, "PASS")
        self.assertEqual(finding(observed, "PHYSICAL_CAPABILITY").requested_function, "GPIO_IN")

    def test_04_gpio_output_discovery_and_raw_verifier_equality(self):
        catalog, board, facts = self.inputs
        observed = self.contacts["J3.9"]
        self.assertEqual((observed.qualification, observed.evidence_claim_ids),
                         ("FUNCTION_CONFIRMED_FOR_STATED_CHECK", ("board-J3.9", "map-J3.9", "silicon-GPIO18")))
        snapshot = create_snapshot(catalog, instances=(board,), junctions=(), conductors=())
        direct = verify_gpio_requirements(catalog, snapshot, facts, (GpioRequirement(
            requirement_id="J3.9", terminal=t("board", "J3.9"), requested_function="GPIO_OUT",
            operating_state="ACTIVE", checks=("PIN_MAPPING", "PHYSICAL_CAPABILITY", "BOARD_AVAILABILITY",
                                               "ACTIVE_CONFIGURATION", "ELECTRICAL_COMPATIBILITY"),
        ),), CATALOG_PIN, FACT_PIN)
        self.assertEqual((observed.findings, observed.coverage), (direct.findings, direct.coverage))

    def test_05_input_only_rejects_output(self):
        observed = self.contacts["J2.5"]
        rule = finding(observed, "PHYSICAL_CAPABILITY")
        self.assertEqual((rule.status, rule.reason_code, observed.qualification),
                         ("FAIL", "OUTPUT_NOT_CAPABLE", "KNOWN_UNSUITABLE"))

    def test_06_reserved_board_resource_stays_separate(self):
        observed = self.contacts["J3.19"]
        self.assertEqual(finding(observed, "PHYSICAL_CAPABILITY").status, "PASS")
        rule = finding(observed, "BOARD_AVAILABILITY")
        self.assertEqual((rule.status, rule.reason_code, observed.qualification),
                         ("FAIL", "RESERVED_RESOURCE", "KNOWN_UNSUITABLE"))

    def test_07_missing_conflicting_or_inconsistent_mapping(self):
        catalog, board, facts = self.inputs
        for status, expected in ((None, "MISSING_MAPPING"), ("conflicting", "EVIDENCE_CONFLICT"),
                                 ("mismatch", "AMBIGUOUS_MAPPING")):
            body = facts.model_dump(mode="json")
            for row in tuple(body["mappings"]):
                if row["terminal_id"] == "J3.9":
                    if status is None:
                        body["mappings"].remove(row)
                    elif status == "mismatch":
                        row["target"] = "GPIO19"
                    else:
                        row["review"] = status
            revised = reseal(body)
            inputs = catalog, board, revised
            observed = by_contact(discover(make_query(*inputs), inputs, CATALOG_PIN, revised.factset_digest))["J3.9"]
            with self.subTest(status=status):
                self.assertEqual(observed.qualification, "UNRESOLVED_EVIDENCE")
                self.assertEqual({(row.status, row.reason_code) for row in observed.findings}, {("UNKNOWN", expected)})

    def test_08_invalid_external_pins_raise_real_b_errors(self):
        for a, b, code in ((ZERO, FACT_PIN, "TRUSTED_CATALOG_PIN_MISMATCH"),
                           (CATALOG_PIN, ZERO, "TRUSTED_FACTSET_PIN_MISMATCH")):
            with self.subTest(code=code), self.assertRaises(GpioVerificationError) as caught:
                discover(self.query, self.inputs, a, b)
            self.assertEqual(caught.exception.code, code)

    def test_09_absent_pins_and_unreviewed_facts_never_confer_authority(self):
        for a, b, reason in ((None, FACT_PIN, "UNTRUSTED_CATALOG"), (CATALOG_PIN, None, "UNTRUSTED_FACTSET")):
            with self.subTest(reason=reason):
                report = discover(self.query, self.inputs, a, b)
                self.assertEqual(report.terminal_domain, self.report.terminal_domain)
                for row in report.candidates:
                    self.assertEqual(row.qualification, "UNRESOLVED_EVIDENCE")
                    self.assertEqual({(f.status, f.reason_code) for f in row.findings}, {("UNKNOWN", reason)})
                    self.assertEqual(row.evidence_claim_ids, ())
        catalog, board, facts = self.inputs
        unreviewed = reseal(facts.model_dump(mode="json") | {"review": "UNREVIEWED"})
        inputs = (catalog, board, unreviewed)
        report = discover(make_query(*inputs), inputs, CATALOG_PIN, unreviewed.factset_digest)
        self.assertEqual({candidate.qualification for candidate in report.candidates}, {"UNRESOLVED_EVIDENCE"})
        self.assertTrue(all("UNTRUSTED_FACTSET" in candidate.limitations for candidate in report.candidates))

    def test_10_ordering_and_immutability(self):
        catalog, board, facts = self.inputs
        reordered = tuple(item.model_copy(update={"terminals": tuple(reversed(item.terminals))})
                          for item in reversed(catalog.definitions))
        report = discover(self.query, (catalog.model_copy(update={"definitions": reordered}), board,
                                      facts.model_copy(update={"mappings": tuple(reversed(facts.mappings))})))
        self.assertEqual(report, self.report)
        with self.assertRaises(ValidationError):
            report.query.requested_function = "GPIO_IN"
        with self.assertRaises(ValidationError):
            report.candidates[0].terminal.terminal_id = "other"

    def test_11_display_label_does_not_establish_instance_identity(self):
        catalog, board, facts = self.inputs
        label = "Same board display label"
        first = board.model_copy(update={"user_label": label})
        second = board.model_copy(update={"user_label": label, "instance_id": "second-board"})
        one = discover(self.query, (catalog, first, facts))
        two = discover(make_query(catalog, second, facts), (catalog, second, facts))
        self.assertEqual({row.terminal.instance_id for row in one.candidates}, {"board"})
        self.assertEqual({row.terminal.instance_id for row in two.candidates}, {"second-board"})
        self.assertEqual([row.qualification for row in one.candidates], [row.qualification for row in two.candidates])
        self.assertNotEqual(one.snapshot_digest, two.snapshot_digest)

    def test_12_source_revision_and_fact_change_invalidate_stale_results(self):
        catalog, board, facts = self.inputs
        body = facts.model_dump(mode="json")
        body["sources"][0]["revision"] = "changed source revision for test"
        changed_source = reseal(body)
        changed_inputs = catalog, board, changed_source
        with self.assertRaises(DiscoveryInputError) as caught:
            discover(self.query, changed_inputs)
        self.assertEqual(caught.exception.code, "EVIDENCE_REFERENCE_MISMATCH")
        updated = make_query(*changed_inputs)
        with self.assertRaises(GpioVerificationError) as caught:
            discover(updated, changed_inputs)
        self.assertEqual(caught.exception.code, "TRUSTED_FACTSET_PIN_MISMATCH")
        refreshed = discover(updated, changed_inputs, CATALOG_PIN, changed_source.factset_digest)
        self.assertNotEqual(finding(by_contact(refreshed)["J3.9"], "PIN_MAPPING").finding_id,
                            finding(self.contacts["J3.9"], "PIN_MAPPING").finding_id)
        next(row for row in body["silicon"] if row["target"] == "GPIO18")["output_allowed"] = False
        denied = reseal(body)
        denied_inputs = catalog, board, denied
        observed = by_contact(discover(make_query(*denied_inputs), denied_inputs, CATALOG_PIN,
                                       denied.factset_digest))["J3.9"]
        self.assertEqual(finding(observed, "PHYSICAL_CAPABILITY").reason_code, "OUTPUT_NOT_CAPABLE")
        self.assertEqual(observed.qualification, "KNOWN_UNSUITABLE")

    def test_13_unsupported_capabilities_and_contexts_fail_explicitly(self):
        for key, value in (("requested_function", "GPIO_IN_PULLUP"), ("operating_state", "RESET")):
            with self.subTest(key=key), self.assertRaises(ValidationError):
                discover(self.query.model_copy(update={key: value}), self.inputs)

    def test_14_fictitious_mcu_uses_the_same_discovery(self):
        synthetic, catalog, facts = synthetic_fixture()
        inputs = catalog, synthetic.instances[0], facts
        report = discover(make_query(*inputs), inputs, catalog.catalog_digest, facts.factset_digest)
        self.assertEqual(report.terminal_domain, tuple(t("controller", contact) for contact in ("A", "B", "C")))
        observed = by_contact(report)
        self.assertEqual(observed["B"].qualification, "FUNCTION_CONFIRMED_FOR_STATED_CHECK")
        self.assertEqual(observed["A"].qualification, "KNOWN_UNSUITABLE")
        self.assertEqual(observed["B"].signal_mapping.target_id, "Port1")

    def test_15_discovered_domains_drive_real_syn_conductors_and_core_nets(self):
        reports, request, result = run_headless()
        self.assertEqual(tuple(role.domain for role in request.roles), tuple(report.terminal_domain for report in reports))
        self.assertEqual((result.termination, result.nodes_visited, result.uniqueness_prunes,
                          result.evaluated_candidates, result.verifier_calls, result.rejected_candidates),
                         ("EXHAUSTED_REVIEWED_DOMAIN", 30, 5, 20, 20, 11))
        candidate = next(row for row in result.candidates if {trace.assigned_terminal.terminal_id
            for trace in row.traces if trace.role == "TRIG_OUTPUT"} == {"J3.9"} and
            {trace.assigned_terminal.terminal_id for trace in row.traces if trace.role == "ECHO_INPUT"} == {"J3.8"})
        self.assertEqual({frozenset((wire.endpoint_a, wire.endpoint_b)) for wire in candidate.snapshot.conductors},
                         {frozenset((t("board", "J3.9"), t("sensor", "Trig"))),
                          frozenset((t("board", "J3.8"), t("sensor", "Echo")))})
        nets = {net.net_id: net.members for net in candidate.topology.nets}
        self.assertEqual({nets[trace.net_id] for trace in candidate.traces},
                         {("T:board/J3.9", "T:sensor/Trig"), ("T:board/J3.8", "T:sensor/Echo")})
        self.assertEqual(candidate.classification, "INCOMPLETE_WITH_EXPLICIT_OBLIGATIONS")
        self.assertEqual({row.reason_code for row in candidate.gpio_report.findings if row.status == "UNKNOWN"},
                         {"ACTIVE_CONFIG_UNKNOWN", "EVIDENCE_MISSING"})
        self.assertEqual({row.coverage for row in candidate.gpio_report.coverage}, {"NOT_EVALUATED"})
        self.assertIn("FIRMWARE", candidate.unresolved_obligations)
        self.assertTrue(any(row.reason_code == "OUTPUT_NOT_CAPABLE" and row.status == "FAIL"
                            for option in result.candidates for row in option.gpio_report.findings))
        self.assertNotEqual(reports[0].snapshot_digest, candidate.gpio_report.snapshot_digest)

    def test_16_unknown_and_unevaluated_never_become_pass(self):
        observed = self.contacts["J3.9"]
        self.assertEqual(finding(observed, "BOARD_AVAILABILITY").status, "UNKNOWN")
        self.assertEqual(finding(observed, "ACTIVE_CONFIGURATION").status, "UNKNOWN")
        self.assertEqual([(row.rule_id, row.coverage) for row in observed.coverage],
                         [("ELECTRICAL_COMPATIBILITY", "NOT_EVALUATED")])
        self.assertEqual(observed.limitations, ("ACTIVE_CONFIG_UNKNOWN", "ELECTRICAL_CHECK_DELEGATED",
                                                 "EVIDENCE_MISSING"))

    def test_17_only_bounded_qualifications_are_exposed(self):
        self.assertEqual(self.report.restriction, "TEST_ONLY_NOT_PRODUCTION")
        for forbidden in ('"SAFE"', '"FULLY_COMPATIBLE"', '"READY_TO_BUILD"'):
            self.assertNotIn(forbidden, self.report.model_dump_json())


if __name__ == "__main__":
    reports, request, result = run_headless()
    print(json.dumps({"discovery": [report.model_dump(mode="json") for report in reports],
                      "request": request.model_dump(mode="json"), "synthesis": result.model_dump(mode="json")},
                     sort_keys=True))
