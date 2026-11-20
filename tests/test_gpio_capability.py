"""Fixed independent GPIO acceptance oracles and integrity controls."""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import unittest

from inventor_edu import (
    EngineeringModelError, GpioRequirement, GpioVerificationError, create_snapshot, load_catalog,
    load_gpio_factset, restore_snapshot, serialize_gpio_report, serialize_snapshot, verify_gpio_requirements,
)
from tests.core001a_fixtures import BOARD, SENSOR, encode, fixture_data, part, reviewed_mapping_fixture_data, seal, t, wire

DATA = Path(__file__).resolve().parents[1] / "data" / "gpio"
CATALOG_PIN = "sha256:356732040b6bd762e8c604ae63c3600df5da225cc938af6dff688b25aad4c57b"
FACT_PIN = "sha256:890f608028990e8f80f9ee48cd4388e58df1d160acc7edf2bf61445df8556d16"
CHECK = "PHYSICAL_CAPABILITY"


def reseal(body):
    """Compute a fresh independent checksum so mutations test semantics, not a stale hash."""
    body = deepcopy(body)
    body.pop("factset_digest", None)
    body["sources"].sort(key=lambda s: s["source_id"])
    for table in ("mappings", "silicon", "resources", "straps"):
        body[table].sort(key=lambda x: x["claim_id"])
        for row in body[table]:
            row["source_ids"] = sorted(row["source_ids"])
            if table == "straps":
                row["prerequisites"] = sorted(row["prerequisites"])
    body["factset_digest"] = "sha256:" + sha256(encode(body)).hexdigest()
    return load_gpio_factset(encode(body))


def request(contact="J3.9", function="GPIO_OUT", checks=(CHECK,), state="ACTIVE", key="req", instance="board"):
    return GpioRequirement(requirement_id=key, terminal=t(instance, contact), requested_function=function,
                           checks=checks, operating_state=state)


class GpioAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog((DATA / "devkitc_32e_catalog.json").read_bytes(), expected_sha256=CATALOG_PIN)
        cls.facts = load_gpio_factset((DATA / "devkitc_32e_facts.json").read_bytes())
        cls.body = cls.facts.model_dump(mode="json")
        cls.snapshot = cls.make_snapshot(cls.catalog)

    @staticmethod
    def make_snapshot(catalog):
        circuit = create_snapshot(catalog, instances=(part(catalog, "board", BOARD), part(catalog, "sensor", SENSOR)),
            junctions=(), conductors=(wire("echo", t("board", "J3.8"), t("sensor", "Echo")),))
        return restore_snapshot(serialize_snapshot(circuit), catalog)

    def check(self, *reqs, **overrides):
        args = dict(catalog=self.catalog, snapshot=self.snapshot, fact_set=self.facts, requests=reqs,
                    trusted_catalog_sha256=CATALOG_PIN, trusted_factset_sha256=FACT_PIN)
        return verify_gpio_requirements(**(args | overrides))

    def expect(self, result, expectations):
        self.assertEqual({item.rule_id: (item.status, item.reason_code) for item in result.findings}, expectations)
        self.assertTrue(all(item.coverage == "EVALUATED" for item in result.findings))

    def test_B01_to_B05_source_reviewed_direction_and_pullup(self):
        for contact, func, checks, expected in (
            ("J2.5", "GPIO_OUT", (CHECK,), {CHECK: ("FAIL", "OUTPUT_NOT_CAPABLE")}),
            ("J3.9", "GPIO_OUT", (CHECK,), {CHECK: ("PASS", "CAPABILITY_CONFIRMED")}),
            ("J3.8", "GPIO_IN", (CHECK,), {CHECK: ("PASS", "CAPABILITY_CONFIRMED")}),
            ("J2.5", "GPIO_IN", (CHECK,), {CHECK: ("PASS", "CAPABILITY_CONFIRMED")}),
            ("J2.5", "GPIO_IN_PULLUP", (CHECK, "INTERNAL_PULLUP_CAPABILITY"), {
                CHECK: ("PASS", "CAPABILITY_CONFIRMED"),
                "INTERNAL_PULLUP_CAPABILITY": ("FAIL", "PULLUP_NOT_CAPABLE"),
            }),
        ):
            with self.subTest(contact=contact, func=func):
                self.expect(self.check(request(contact, func, checks)), expected)

    def test_pin_mapping_and_literal_canonical_report_hashes(self):
        self.expect(self.check(request(checks=("PIN_MAPPING",))),
                    {"PIN_MAPPING": ("PASS", "MAPPING_CONFIRMED")})
        report = self.check(request())
        # Authored from the documented preimages, with a literal result and stdlib SHA-256.
        self.assertEqual(report.snapshot_digest,
                         "sha256:ed5f9ed4f834f2c8549f346fc470eec2e415435b95b50b28665ae45be1017eec")
        self.assertEqual(report.findings[0].finding_id,
                         "sha256:71549f4eb0d8d875789b55f91565661df24f85e68981e4b816d66e65789141f6")
        self.assertEqual(sha256(serialize_gpio_report(report)).hexdigest(),
                         "f2c8d9434c54886427ec3fe8f142828f0d49b74e1984807557a9a980cdb16430")

    def test_B06_board_reservation_is_separate_from_silicon(self):
        self.expect(self.check(request("J3.19", checks=(CHECK, "BOARD_AVAILABILITY"))), {
            CHECK: ("PASS", "CAPABILITY_CONFIRMED"),
            "BOARD_AVAILABILITY": ("FAIL", "RESERVED_RESOURCE"),
        })

    def test_B07_B08_boot_and_active_require_separate_evidence(self):
        self.expect(self.check(request("J3.14", checks=("BOOT_STRAP_CONTEXT",))), {
            "BOOT_STRAP_CONTEXT": ("UNKNOWN", "BOOT_STRAP_CONDITIONS_UNKNOWN"),
        })
        req = request(checks=(CHECK, "ACTIVE_CONFIGURATION")).model_copy(
            update={"declared_configuration": "OUTPUT", "firmware_observation_ref": "unvalidated"})
        self.expect(self.check(req), {
            CHECK: ("PASS", "CAPABILITY_CONFIRMED"), "ACTIVE_CONFIGURATION": ("UNKNOWN", "ACTIVE_CONFIG_UNKNOWN"),
        })

    def test_B12_wrong_device_and_module_and_board_variant_never_inherit_scope(self):
        unsupported = self.check(request("Echo", "GPIO_IN", instance="sensor"))
        self.assertEqual(unsupported.coverage[0].reason_code, "UNSUPPORTED_DEVICE")
        for field, wrong in (("orderable_part", "Generic ESP32"), ("module", "ESP32-WROOM-32UE")):
            body = deepcopy(self.body)
            body["scope"][field] = wrong
            facts = reseal(body)
            result = self.check(request(), fact_set=facts, trusted_factset_sha256=facts.factset_digest)
            self.assertEqual((), result.findings)
            self.assertEqual(result.coverage[0].reason_code, "UNSUPPORTED_DEVICE")

    def test_B13_conflicting_capability_claims_are_unknown(self):
        body = deepcopy(self.body)
        original = next(x for x in body["silicon"] if x["target"] == "GPIO18")
        body["silicon"].append(original | {"claim_id": "conflict", "output_allowed": False})
        facts = reseal(body)
        self.expect(self.check(request(), fact_set=facts, trusted_factset_sha256=facts.factset_digest),
                    {CHECK: ("UNKNOWN", "EVIDENCE_CONFLICT")})

    def test_B14_bad_physical_contact_propagates_core_error(self):
        with self.assertRaises(EngineeringModelError) as caught:
            self.check(request("J3.99"))
        self.assertEqual("UNKNOWN_TERMINAL", caught.exception.code)

    def test_B15_B22_canonical_order_and_label_free_repetition(self):
        a, b = request(key="a"), request("J2.5", key="b")
        original = serialize_gpio_report(self.check(a, b))
        reversed_facts = self.facts.model_copy(update={"silicon": self.facts.silicon[::-1],
                                                      "sources": self.facts.sources[::-1]})
        for _ in range(100):
            self.assertEqual(original, serialize_gpio_report(self.check(b, a, fact_set=reversed_facts)))
        snapshot = create_snapshot(self.catalog,
            instances=tuple(p.model_copy(update={"user_label": "ერთი სახელი"}) for p in self.snapshot.instances),
            conductors=self.snapshot.conductors, junctions=())
        localized = self.check(a, b, snapshot=snapshot)
        initial = self.check(a, b)
        self.assertEqual([(x.terminal, x.affected_net, x.status) for x in initial.findings],
                         [(x.terminal, x.affected_net, x.status) for x in localized.findings])
        self.assertNotEqual(initial.snapshot_digest, localized.snapshot_digest)
        # Snapshot-pinned IDs depend on canonical circuit bytes. View-only localization has no input API.
        self.assertEqual(original, serialize_gpio_report(self.check(a, b)))

    def test_B16_B24_electrical_and_simulation_coverage_is_explicit(self):
        result = self.check(request("J3.8", "GPIO_IN", (CHECK, "ELECTRICAL_COMPATIBILITY")),
                            request(function="SIMULATE_ANALOG_NOISE", key="simulation"))
        self.expect(result, {CHECK: ("PASS", "CAPABILITY_CONFIRMED")})
        self.assertEqual({(x.requirement_id, x.coverage, x.reason_code) for x in result.coverage}, {
            ("req", "NOT_EVALUATED", "ELECTRICAL_CHECK_DELEGATED"),
            ("simulation", "NOT_EVALUATED", "OUT_OF_SCOPE"),
        })

    def test_B18_B23_missing_conditions_board_and_capability_are_unknown(self):
        self.expect(self.check(request(checks=("BOARD_AVAILABILITY",))), {
            "BOARD_AVAILABILITY": ("UNKNOWN", "EVIDENCE_MISSING"),
        })
        self.expect(self.check(request(state="SLEEP")), {CHECK: ("UNKNOWN", "CAPABILITY_UNKNOWN")})
        self.expect(self.check(request(function="GPIO_IN_PULLUP", checks=("INTERNAL_PULLUP_CAPABILITY",))), {
            "INTERNAL_PULLUP_CAPABILITY": ("UNKNOWN", "CAPABILITY_UNKNOWN"),
        })
        self.expect(self.check(request(checks=("INTERNAL_PULLUP_CAPABILITY",))), {
            "INTERNAL_PULLUP_CAPABILITY": ("NOT_APPLICABLE", "PULLUP_NOT_REQUESTED"),
        })

    def test_untrusted_missing_pins_and_wrong_pins(self):
        self.expect(self.check(request(), trusted_catalog_sha256=None), {CHECK: ("UNKNOWN", "UNTRUSTED_CATALOG")})
        self.expect(self.check(request(), trusted_factset_sha256=None), {CHECK: ("UNKNOWN", "UNTRUSTED_FACTSET")})
        for field, code in (("trusted_catalog_sha256", "TRUSTED_CATALOG_PIN_MISMATCH"),
                            ("trusted_factset_sha256", "TRUSTED_FACTSET_PIN_MISMATCH")):
            with self.assertRaises(GpioVerificationError) as caught:
                self.check(request(), **{field: "sha256:" + "0" * 64})
            self.assertEqual(caught.exception.code, code)
        body = deepcopy(self.body)
        body["sources"][0]["revision"] = "other edition"
        changed = reseal(body)
        with self.assertRaisesRegex(GpioVerificationError, "TRUSTED_FACTSET_PIN_MISMATCH"):
            self.check(request(), fact_set=changed)
        body["review"] = "UNREVIEWED"
        unreviewed = reseal(body)
        self.expect(self.check(request(), fact_set=unreviewed, trusted_factset_sha256=unreviewed.factset_digest),
                    {CHECK: ("UNKNOWN", "UNTRUSTED_FACTSET")})

    def test_malformed_factsets_and_required_source_references_are_ingestion_errors(self):
        for malformed in (b'{"schema_version":"1.0","schema_version":"1.0"}', b"\xff", b"[]"):
            with self.subTest(malformed=malformed), self.assertRaisesRegex(GpioVerificationError, "INVALID_FACTSET"):
                load_gpio_factset(malformed)
        body = deepcopy(self.body)
        body["silicon"][0]["source_ids"] = ["missing-document"]
        with self.assertRaisesRegex(GpioVerificationError, "INVALID_FACTSET"):
            reseal(body)
        body = deepcopy(self.body)
        body["catalog_digest"] = "sha256:" + "f" * 64
        orphan = reseal(body)
        with self.assertRaisesRegex(GpioVerificationError, "FACTSET_CATALOG_MISMATCH"):
            self.check(request(), fact_set=orphan, trusted_factset_sha256=orphan.factset_digest)

    def test_resealed_wrong_mapping_legacy_and_missing_kind(self):
        body = deepcopy(self.body)
        next(row for row in body["mappings"] if row["terminal_id"] == "J3.9")["target"] = "GPIO19"
        facts = reseal(body)
        self.expect(self.check(request(), fact_set=facts, trusted_factset_sha256=facts.factset_digest),
                    {CHECK: ("UNKNOWN", "AMBIGUOUS_MAPPING")})
        for legacy in (True, False):
            definitions, sources, claims = fixture_data() if legacy else reviewed_mapping_fixture_data()
            board = next(d for d in definitions if d["definition_id"] == BOARD)
            if not legacy:
                pin = next(x for x in board["terminals"] if x["terminal_id"] == "J3.9")
                pin["signal_ref"]["mapping_status"] = "unknown"
            catalog = load_catalog(seal(definitions, sources, claims, version="1.0" if legacy else "1.1"))
            body = deepcopy(self.body)
            body["catalog_digest"] = catalog.catalog_digest
            body["scope"]["definition_digest"] = next(d.definition_digest for d in catalog.definitions
                                                        if d.definition_id == BOARD)
            facts = reseal(body)
            self.expect(self.check(request(), catalog=catalog, snapshot=self.make_snapshot(catalog), fact_set=facts,
                trusted_catalog_sha256=catalog.catalog_digest, trusted_factset_sha256=facts.factset_digest),
                {CHECK: ("UNKNOWN", "MISSING_MAPPING")})
        invalid = json.loads((DATA / "devkitc_32e_catalog.json").read_bytes())
        del next(row["value"] for row in invalid["claims"] if row["claim_id"] == "board-J3.9")["target_kind"]
        with self.assertRaises(EngineeringModelError):
            load_catalog(encode(invalid))

    def test_same_display_label_preserves_instance_and_net_identity(self):
        parts = tuple(part(self.catalog, key, BOARD).model_copy(update={"user_label": "Same"})
                      for key in ("first", "second"))
        snapshot = create_snapshot(self.catalog, instances=parts, junctions=(), conductors=())
        result = self.check(request(instance="first", key="a"), request(instance="second", key="b"), snapshot=snapshot)
        self.assertEqual([f.terminal.instance_id for f in result.findings], ["first", "second"])
        self.assertEqual(2, len({f.affected_net for f in result.findings}))

    def test_B19_synthetic_mcu_facts_use_same_evaluator(self):
        # The fictitious manufacturer record exercises A's positive mapping admission in a test only.
        # B explicitly marks the factset synthetic. None of these identities is hardware evidence.
        scope = "Synthetic test MCU X"
        profile = dict(definition_schema_version="1.0", definition_id="mcu-x", device_class="test-mcu",
            identity=dict(brand_or_distributor="Fictional test maker", manufacturer_status="verified",
                manufacturer_name="Fictional test maker", orderable_part_or_sku="X-1", hardware_family="MCU-X",
                hardware_revision="X1", hardware_revision_status="unverified", assembled_module="module-X",
                silicon_revision_status="unverified", profile_scope=scope), terminals=[])
        doc = dict(source_document_id="synthetic", url="https://example.invalid/mcu-x", publisher="Fictional test maker",
                   title=scope, edition="synthetic-v1", accessed_at_utc="2026-11-20", media_type="text/plain",
                   rights_state="link_only")
        claims, mappings, caps = [], [], []
        for contact, target, can_output in (("P0", "PortX", True), ("P1", "PortY", False)):
            profile["terminals"].append(dict(terminal_id=contact, contact_type="pad", printed_label=contact,
                electrical_role="io", signal_ref=dict(terminal_id=contact, target_kind="soc_gpio", target_id=target,
                source_claim_id=f"claim-{contact}", mapping_status="verified")))
            claims.append(dict(claim_id=f"claim-{contact}", claim_type="signal_mapping", subject_definition_id="mcu-x",
                value=dict(terminal_id=contact, target_kind="soc_gpio", target_id=target), source_class="manufacturer",
                source_document_id="synthetic", locator=contact, scope=scope, qualification="Test only", review_status="approved"))
            base = dict(target=target, source_ids=["synthetic"], locator=contact, review="approved")
            mappings.append(dict(**base, claim_id=f"map-{contact}", terminal_id=contact))
            caps.append(dict(**base, claim_id=f"cap-{contact}", silicon="MCU-X",
                             input_allowed=True, output_allowed=can_output, pullup_allowed=None))
        catalog = load_catalog(seal([profile], [doc], claims, version="1.1"))
        device = catalog.definitions[0]
        facts = reseal(dict(schema_version="1.0", catalog_digest=catalog.catalog_digest,
            scope=dict(definition_id="mcu-x", definition_digest=device.definition_digest, board_family="MCU-X",
                board_revision="X1", orderable_part="X-1", module="module-X", silicon="MCU-X", profile_scope=scope),
            review="TEST_ONLY_SYNTHETIC", mappings=mappings, silicon=caps, straps=[], resources=[],
            sources=[dict(source_id="synthetic", url=doc["url"], revision="synthetic-v1",
                          artifact_sha256="sha256:" + "0" * 64, rights="test only")]))
        snapshot = create_snapshot(catalog, instances=(part(catalog, "board", "mcu-x"),), conductors=(), junctions=())
        result = verify_gpio_requirements(catalog, snapshot, facts, (request("P0", key="a"), request("P1", key="b")),
                                          catalog.catalog_digest, facts.factset_digest)
        self.assertEqual([(f.status, f.reason_code) for f in result.findings],
                         [("PASS", "CAPABILITY_CONFIRMED"), ("FAIL", "OUTPUT_NOT_CAPABLE")])
