"""Independent physical contacts, outcomes and search oracles for SYN-001."""

from hashlib import sha256
import json
import unittest
from unittest.mock import patch

from pydantic import ValidationError

from inventor_edu import EngineeringModelError, GpioVerificationError, load_catalog, load_gpio_factset
from inventor_edu.gpio_verify import verify_gpio_requirements
from inventor_edu.synthesis import SignalRole, SynthesisInputError, SynthesisRequest, generate_candidates
from tests.core001a_fixtures import (
    BOARD, SENSOR, ZERO, claim, definition, identity, part, seal, source, t, terminal,
)
from tests.test_gpio_capability import CATALOG_PIN, DATA, FACT_PIN, reseal


def reviewed_fixture(trig=("J3.9", "J2.5", "J3.19"), echo=("J3.8",), **overrides):
    catalog = load_catalog((DATA / "devkitc_32e_catalog.json").read_bytes(), expected_sha256=CATALOG_PIN)
    facts = load_gpio_factset((DATA / "devkitc_32e_facts.json").read_bytes())
    roles = (
        SignalRole(role="TRIG_OUTPUT", requirement_id="drive", source_terminal=t("sensor", "Trig"),
                   function="GPIO_OUT", domain=tuple(t("board", contact) for contact in trig)),
        SignalRole(role="ECHO_INPUT", requirement_id="listen", source_terminal=t("sensor", "Echo"),
                   function="GPIO_IN", domain=tuple(t("board", contact) for contact in echo)),
    )
    digest = sha256(b"drive:TRIG_OUTPUT:GPIO_OUT;listen:ECHO_INPUT:GPIO_IN").hexdigest()
    fields = dict(request_id="ultrasonic-example", requirements_digest="sha256:" + digest,
                  catalog_digest=CATALOG_PIN, instances=(part(catalog, "board", BOARD), part(catalog, "sensor", SENSOR)),
                  roles=roles, resource_constraint="AllDifferent", evidence_scope="TEST_ONLY_SOURCE_REVIEWED",
                  max_nodes=30, max_candidates=10)
    return SynthesisRequest(**(fields | overrides)), catalog, facts


def run(fixture, catalog_pin=CATALOG_PIN, fact_pin=FACT_PIN):
    return generate_candidates(*fixture, trusted_catalog_sha256=catalog_pin, trusted_factset_sha256=fact_pin)


def finding(candidate, requirement, rule="PHYSICAL_CAPABILITY"):
    return next(item for item in candidate.gpio_report.findings
                if (item.requirement_id, item.rule_id) == (requirement, rule))


def assigned_contact(candidate, requirement="drive"):
    return next(trace.assigned_terminal.terminal_id for trace in candidate.traces
                if trace.requirement_id == requirement)


def synthetic_fixture():
    scope = "Fictitious MCU and signal device"
    device = definition("fictional-controller", "test-mcu", identity("Fictional Lab", "Z-9", "MCU-Z", scope,
        manufacturer_status="verified", manufacturer_name="Fictional Lab", hardware_revision="prototype",
        assembled_module="module-z"), [])
    peer = definition("fictional-peer", "test-peer", identity("Fictional Lab", "P-9", "PEER-Z", scope), [
        terminal("stimulus", "SAME", "input"), terminal("response", "SAME", "output"),
    ])
    doc = source("fixture", "Fictional Lab", "https://example.invalid/syn-fixture", scope, "test-v1")
    claims, mappings, silicon, resources = [], [], [], []
    for contact, target, output in (("A", "Port0", False), ("B", "Port1", True), ("C", "Port2", False)):
        mapping = dict(terminal_id=contact, target_kind="soc_gpio", target_id=target)
        device["terminals"].append(terminal(contact, "SAME", "io",
            signal_ref=dict(**mapping, source_claim_id=f"catalog-{contact}", mapping_status="verified")))
        claims.append(claim(f"catalog-{contact}", "signal_mapping", device, mapping, "fixture", contact,
                            source_class="manufacturer", qualification="Fictitious test only"))
        basis = dict(target=target, source_ids=["fixture"], locator=contact, review="approved")
        mappings.append(dict(**basis, claim_id=f"map-{contact}", terminal_id=contact))
        silicon.append(dict(**basis, claim_id=f"cap-{contact}", silicon="MCU-Z", input_allowed=True,
                            output_allowed=output, pullup_allowed=None))
        resources.append(dict(**basis, claim_id=f"free-{contact}", operating_state="ACTIVE",
                              reservation="available", reason="Fictitious test assumption"))
    catalog = load_catalog(seal([device, peer], [doc], claims, version="1.1"))
    controller = part(catalog, "controller", "fictional-controller")
    facts = reseal(dict(schema_version="1.0", catalog_digest=catalog.catalog_digest,
        scope=dict(definition_id=controller.definition_id, definition_digest=controller.definition_digest,
                   board_family="MCU-Z", board_revision="prototype", orderable_part="Z-9", module="module-z",
                   silicon="MCU-Z", profile_scope=scope),
        review="TEST_ONLY_SYNTHETIC", mappings=mappings, silicon=silicon, resources=resources, straps=[],
        sources=[dict(source_id="fixture", url=doc["url"], revision="test-v1", artifact_sha256=ZERO,
                      rights="test only; fictitious")]))
    request = SynthesisRequest(request_id="synthetic", requirements_digest=ZERO, catalog_digest=catalog.catalog_digest,
        instances=(controller, part(catalog, "peer", "fictional-peer")), resource_constraint="AllDifferent",
        roles=(
            SignalRole(role="TRIG_OUTPUT", requirement_id="drive", function="GPIO_OUT",
                       source_terminal=t("peer", "stimulus"), domain=(t("controller", "B"), t("controller", "A"))),
            SignalRole(role="ECHO_INPUT", requirement_id="listen", function="GPIO_IN",
                       source_terminal=t("peer", "response"), domain=(t("controller", "C"),)),
        ), evidence_scope="TEST_ONLY_SYNTHETIC", max_nodes=10, max_candidates=10)
    return request, catalog, facts


class SynthesisAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = reviewed_fixture()
        cls.result = run(cls.fixture)
        cls.by_trig = {assigned_contact(candidate): candidate for candidate in cls.result.candidates}

    def test_S01_exact_fixture_and_invalid_contracts(self):
        request, catalog, facts = self.fixture
        self.assertEqual(tuple(item.definition_id for item in request.instances),
                         ("esp32-devkitc-32e-v4", "adafruit-3942-profile"))
        self.assertEqual(self.result.evaluated_candidates, 3)
        for updates, code in (
            (dict(catalog_digest=ZERO), "CATALOG_REFERENCE_MISMATCH"),
            (dict(evidence_scope="TEST_ONLY_SYNTHETIC"), "EVIDENCE_SCOPE_MISMATCH"),
            (dict(roles=(request.roles[0], request.roles[0])), "INVALID_ROLE_REQUIREMENTS"),
            (dict(roles=(request.roles[0].model_copy(update={"function": "GPIO_IN"}), request.roles[1])),
             "INVALID_ROLE_REQUIREMENTS"),
            (dict(roles=(request.roles[0].model_copy(update={"domain": (t("board", "J2.5"),) * 2}),
                         request.roles[1])), "INVALID_PHYSICAL_DOMAIN"),
        ):
            with self.subTest(code=code), self.assertRaises(SynthesisInputError) as caught:
                run((request.model_copy(update=updates), catalog, facts))
            self.assertEqual(caught.exception.code, code)
        wrong_part = request.instances[0].model_copy(update={"definition_digest": ZERO})
        with self.assertRaises(EngineeringModelError) as caught:
            run((request.model_copy(update={"instances": (wrong_part, request.instances[1])}), catalog, facts))
        self.assertEqual(caught.exception.code, "CATALOG_DIGEST_MISMATCH")
        for field, value in (("max_nodes", 0), ("max_candidates", True), ("resource_constraint", "guess")):
            with self.subTest(field=field), self.assertRaises(ValidationError):
                run((request.model_copy(update={field: value}), catalog, facts))

    def test_S02_gpio34_output_rejection(self):
        candidate = self.by_trig["J2.5"]
        result = finding(candidate, "drive")
        self.assertEqual((result.status, result.reason_code), ("FAIL", "OUTPUT_NOT_CAPABLE"))
        self.assertEqual(candidate.classification, "REJECTED_KNOWN_HARD_FAIL")

    def test_S03_gpio18_scoped_pass_unknown_board(self):
        candidate = self.by_trig["J3.9"]
        self.assertEqual(finding(candidate, "drive").status, "PASS")
        self.assertEqual(finding(candidate, "drive", "BOARD_AVAILABILITY").status, "UNKNOWN")
        self.assertEqual(candidate.classification, "INCOMPLETE_WITH_EXPLICIT_OBLIGATIONS")

    def test_S04_gpio19_echo_input_pass(self):
        for candidate in self.result.candidates:
            observed = finding(candidate, "listen")
            self.assertEqual((observed.status, observed.requested_function, observed.terminal),
                             ("PASS", "GPIO_IN", t("board", "J3.8")))

    def test_S05_flash_reservation_is_separate(self):
        candidate = self.by_trig["J3.19"]
        self.assertEqual(finding(candidate, "drive").status, "PASS")
        observed = finding(candidate, "drive", "BOARD_AVAILABILITY")
        self.assertEqual((observed.status, observed.reason_code), ("FAIL", "RESERVED_RESOURCE"))
        self.assertEqual(candidate.classification, "REJECTED_KNOWN_HARD_FAIL")

    def test_S06_exclusive_physical_contact(self):
        result = run(reviewed_fixture(trig=("J3.8", "J3.9")))
        self.assertEqual((result.nodes_visited, result.uniqueness_prunes, result.evaluated_candidates), (3, 1, 1))
        self.assertEqual(assigned_contact(result.candidates[0]), "J3.9")

    def test_S07_missing_mapping_and_bad_contact(self):
        candidate = run(reviewed_fixture(trig=("J2.14",))).candidates[0]
        result = finding(candidate, "drive", "PIN_MAPPING")
        self.assertEqual((result.status, result.reason_code), ("UNKNOWN", "MISSING_MAPPING"))
        self.assertFalse(any(item.status == "PASS" for item in candidate.gpio_report.findings
                             if item.requirement_id == "drive"))
        with self.assertRaises(EngineeringModelError) as caught:
            run(reviewed_fixture(trig=("IO18",)))
        self.assertEqual(caught.exception.code, "UNKNOWN_TERMINAL")

    def test_S08_actual_conductors_and_core_nets(self):
        candidate = self.by_trig["J3.9"]
        observed = {frozenset((wire.endpoint_a, wire.endpoint_b)) for wire in candidate.snapshot.conductors}
        self.assertEqual(observed, {frozenset((t("board", "J3.9"), t("sensor", "Trig"))),
                                    frozenset((t("board", "J3.8"), t("sensor", "Echo")))})
        members = {net.net_id: net.members for net in candidate.topology.nets}
        expected = {"drive": ("T:board/J3.9", "T:sensor/Trig"), "listen": ("T:board/J3.8", "T:sensor/Echo")}
        self.assertEqual({trace.requirement_id: members[trace.net_id] for trace in candidate.traces}, expected)
        self.assertEqual(len({trace.net_id for trace in candidate.traces}), 2)

    def test_S09_domain_change_calls_real_verifier_on_new_snapshot(self):
        with patch("inventor_edu.synthesis.verify_gpio_requirements", wraps=verify_gpio_requirements) as spy:
            old = run(reviewed_fixture(trig=("J2.5",))).candidates[0]
            new = run(reviewed_fixture(trig=("J3.9",))).candidates[0]
        self.assertEqual(spy.call_count, 2)
        self.assertEqual([call.args[1] for call in spy.call_args_list], [old.snapshot, new.snapshot])
        self.assertEqual([verify_gpio_requirements(*call.args) for call in spy.call_args_list],
                         [old.gpio_report, new.gpio_report])
        self.assertNotEqual(old.topology.snapshot_sha256, new.topology.snapshot_sha256)
        self.assertTrue({f.finding_id for f in old.gpio_report.findings}.isdisjoint(
            f.finding_id for f in new.gpio_report.findings))

    def test_S10_order_independence(self):
        request, catalog, facts = self.fixture
        reordered = request.model_copy(update={
            "instances": tuple(reversed(request.instances)),
            "roles": tuple(role.model_copy(update={"domain": tuple(reversed(role.domain))})
                           for role in reversed(request.roles)),
        })
        self.assertEqual(self.result, run((reordered, catalog, facts)))

    def test_S11_budget_and_retention_are_independent(self):
        partial = run(reviewed_fixture(max_nodes=2))
        self.assertEqual((partial.termination, partial.nodes_visited, partial.evaluated_candidates,
                          partial.rejected_candidates, partial.verifier_calls),
                         ("SEARCH_INCOMPLETE", 2, 1, 1, 1))
        self.assertEqual(partial.candidates, self.result.candidates[:1])
        capped = run(reviewed_fixture(max_nodes=4, max_candidates=1))
        self.assertEqual((capped.termination, capped.evaluated_candidates, capped.rejected_candidates,
                          capped.verifier_calls, len(capped.candidates)), ("EXHAUSTED_REVIEWED_DOMAIN", 3, 2, 3, 1))
        early = run(reviewed_fixture(max_nodes=1))
        self.assertEqual((early.termination, early.evaluated_candidates, early.candidates),
                         ("SEARCH_INCOMPLETE", 0, ()))

    def test_S12_empty_domain_differs_from_exhaustive_rejection(self):
        empty = run(reviewed_fixture(trig=()))
        rejected = run(reviewed_fixture(trig=("J2.5",)))
        self.assertEqual((empty.termination, empty.nodes_visited, empty.candidates, empty.verifier_calls),
                         ("NO_REVIEWED_DOMAIN", 0, (), 1))
        self.assertEqual((rejected.termination, rejected.evaluated_candidates, rejected.rejected_candidates),
                         ("EXHAUSTED_REVIEWED_DOMAIN", 1, 1))

    def test_S13_electrical_coverage_and_firmware_remain_open(self):
        for candidate in self.result.candidates:
            self.assertEqual(set(candidate.unresolved_obligations),
                             {"POWER", "LED", "CURRENT_LIMITING_RESISTORS", "VOLTAGE_ADAPTATION", "FIRMWARE"})
            self.assertEqual([(row.rule_id, row.coverage, row.reason_code) for row in candidate.gpio_report.coverage],
                             [("ELECTRICAL_COMPATIBILITY", "NOT_EVALUATED", "ELECTRICAL_CHECK_DELEGATED")] * 2)
            for trace in candidate.traces:
                self.assertIn("ELECTRICAL_COMPATIBILITY", trace.unresolved_rule_ids)
            self.assertIn("validated_firmware_observation", candidate.traces[0].missing_prerequisites)

    def test_S14_external_pins_preserve_verifier_restrictions(self):
        for pins, code in (((ZERO, FACT_PIN), "TRUSTED_CATALOG_PIN_MISMATCH"),
                           ((CATALOG_PIN, ZERO), "TRUSTED_FACTSET_PIN_MISMATCH")):
            for fixture in (self.fixture, reviewed_fixture(trig=())):
                with self.subTest(code=code), self.assertRaises(GpioVerificationError) as caught:
                    run(fixture, *pins)
                self.assertEqual(caught.exception.code, code)
        for pins, reason in (((None, FACT_PIN), "UNTRUSTED_CATALOG"),
                             ((CATALOG_PIN, None), "UNTRUSTED_FACTSET")):
            candidates = run(self.fixture, *pins).candidates
            self.assertTrue(candidates)
            for candidate in candidates:
                self.assertEqual(candidate.classification, "INCOMPLETE_WITH_EXPLICIT_OBLIGATIONS")
                self.assertEqual({(row.status, row.reason_code) for row in candidate.gpio_report.findings},
                                 {("UNKNOWN", reason)})

    def test_S15_immutable_trace_has_original_report_ids_and_scope(self):
        candidate = self.by_trig["J3.9"]
        for trace in candidate.traces:
            self.assertEqual(trace.requirements_digest, self.fixture[0].requirements_digest)
            self.assertEqual(trace.assignment_id, candidate.assignment_id)
            self.assertEqual((trace.catalog_digest, trace.snapshot_digest, trace.factset_digest),
                             (CATALOG_PIN, candidate.topology.snapshot_sha256, FACT_PIN))
            self.assertEqual((trace.restriction, trace.evidence_scope, trace.operating_state),
                             ("TEST_ONLY_NOT_PRODUCTION", "TEST_ONLY_SOURCE_REVIEWED", "ACTIVE"))
            self.assertEqual(trace.hardware_scope.orderable_part, "ESP32-DevKitC-32E")
            self.assertEqual(trace.finding_ids, tuple(row.finding_id for row in candidate.gpio_report.findings
                                                     if row.requirement_id == trace.requirement_id))
            self.assertEqual(trace.coverage_ids, tuple(row.finding_id for row in candidate.gpio_report.coverage
                                                      if row.requirement_id == trace.requirement_id))
            self.assertTrue(set(trace.finding_ids).isdisjoint(trace.coverage_ids))
            self.assertTrue(trace.evidence_claim_ids)
            self.assertEqual(trace.net_id, finding(candidate, trace.requirement_id).affected_net)
            with self.assertRaises(ValidationError):
                trace.source_terminal.terminal_id = "other"
            with self.assertRaises(ValidationError):
                trace.net_id = "other"

    def test_S16_alternate_fictitious_mcu_uses_same_b_rules(self):
        fixture = synthetic_fixture()
        rejected, scoped = run(fixture, fixture[1].catalog_digest, fixture[2].factset_digest).candidates
        self.assertEqual((assigned_contact(rejected), assigned_contact(scoped)), ("A", "B"))
        self.assertEqual(finding(rejected, "drive").reason_code, "OUTPUT_NOT_CAPABLE")
        self.assertEqual(finding(scoped, "drive", "BOARD_AVAILABILITY").status, "PASS")
        self.assertEqual(scoped.classification, "SCOPED_CHECKS_PASSED_WITH_OBLIGATIONS")
        self.assertTrue(all(claim_id.startswith(("map-", "cap-", "free-", "catalog-"))
                            for trace in scoped.traces for claim_id in trace.evidence_claim_ids))

    def test_S17_display_labels_do_not_select_or_merge_contacts(self):
        request, catalog, facts = synthetic_fixture()
        labeled = request.model_copy(update={"instances": tuple(
            instance.model_copy(update={"user_label": "Common display label"}) for instance in request.instances
        )})
        pins = (catalog.catalog_digest, facts.factset_digest)
        original = run((request, catalog, facts), *pins)
        changed = run((labeled, catalog, facts), *pins)
        self.assertEqual({term.printed_label for device in catalog.definitions for term in device.terminals}, {"SAME"})
        for before, after in zip(original.candidates, changed.candidates, strict=True):
            self.assertEqual(before.snapshot.conductors, after.snapshot.conductors)
            self.assertEqual(before.topology.nets, after.topology.nets)
            self.assertEqual(before.classification, after.classification)
            self.assertEqual(len({trace.net_id for trace in after.traces}), 2)

    def test_S18_only_scoped_verdict_vocabulary(self):
        self.assertEqual(self.result.restriction, "TEST_ONLY_NOT_PRODUCTION")
        self.assertEqual({candidate.classification for candidate in self.result.candidates},
                         {"REJECTED_KNOWN_HARD_FAIL", "INCOMPLETE_WITH_EXPLICIT_OBLIGATIONS"})
        exposed = self.result.model_dump_json()
        for forbidden in ('"SAFE"', '"FULLY_COMPATIBLE"', '"READY_TO_BUILD"'):
            self.assertNotIn(forbidden, exposed)


if __name__ == "__main__":
    # Headless example with the same reviewed fixture and independently fixed trusted pins.
    for contacts in (("J2.5", "J3.19", "J3.9"), ("J3.9",)):
        fixture = reviewed_fixture(trig=contacts)
        print(json.dumps({"request": fixture[0].model_dump(mode="json"),
                          "result": run(fixture).model_dump(mode="json")}, sort_keys=True))
