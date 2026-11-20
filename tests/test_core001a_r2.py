"""Independent R2 mapping evidence and persistence acceptance tests."""

import json
from hashlib import sha256
import unittest

from inventor_edu import (
    EngineeringModelError, Junction, JunctionRef, SignalMappingEvidence, compute_nets, create_snapshot,
    load_catalog, resolve_terminal, restore_snapshot, serialize_snapshot, serialize_topology,
)
from tests.core001a_fixtures import BOARD, PASSIVE, SENSOR, encode, fixture_data, part, reviewed_mapping_fixture_data, seal, t, wire

LEGACY_PIN = "sha256:6b2f1c33f43a7c7d02ab9e3b1d5b73466cb9ade6dc235e3f5a3af98782de1934"
BOARD_DEFINITION_PIN = "sha256:7884e0799a118c95709e2a871107871c428b03aeb11c436cf9befd32733b751f"
CLAIM = "board-J3.9"


class TypedMappingEvidenceTests(unittest.TestCase):
    def error(self, code, action, *args, **kwargs):
        with self.assertRaises(EngineeringModelError) as caught:
            action(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def typed_data(self):
        definitions, sources, claims = reviewed_mapping_fixture_data()
        board = next(d for d in definitions if d["definition_id"] == BOARD)
        mapping = next(p["signal_ref"] for p in board["terminals"] if p["terminal_id"] == "J3.9")
        claim = next(c for c in claims if c["claim_id"] == CLAIM)
        return definitions, sources, claims, mapping, claim

    def board_mapping(self, catalog):
        snapshot = create_snapshot(catalog, instances=(part(catalog, "board", BOARD),),
                                   junctions=(), conductors=())
        return resolve_terminal(catalog, snapshot, t("board", "J3.9")).terminal.signal_ref

    def test_verified_typed_mapping_uses_independent_contact_kind_and_target(self):
        catalog = load_catalog(seal(*reviewed_mapping_fixture_data(), version="1.1"))
        mapping = self.board_mapping(catalog)
        evidence = next(claim.value for claim in catalog.claims if claim.claim_id == CLAIM)
        self.assertIsInstance(evidence, SignalMappingEvidence)
        self.assertEqual((evidence.terminal_id, evidence.target_kind, evidence.target_id),
                         ("J3.9", "soc_gpio", "GPIO18"))
        self.assertEqual((mapping.mapping_status, mapping.target_kind, mapping.target_id),
                         ("verified", "soc_gpio", "GPIO18"))

    def test_resealed_wrong_kind_same_target_and_other_pair_mismatches_reject(self):
        for field, value in (("target_kind", "power_domain"), ("target_id", "GPIO19"), ("terminal_id", "J3.8")):
            for evidence_side in (False, True):
                with self.subTest(field=field, evidence_side=evidence_side):
                    definitions, sources, claims, mapping, claim = self.typed_data()
                    (claim["value"] if evidence_side else mapping)[field] = value
                    payload = seal(definitions, sources, claims, version="1.1")
                    self.error("AMBIGUOUS_MAPPING", load_catalog, payload)

    def test_typed_claim_requires_scope_review_and_qualified_source(self):
        cases = (
            ("wrong definition", {"subject_definition_id": SENSOR}, "AMBIGUOUS_MAPPING"),
            ("wrong profile", {"scope": "different hardware"}, "AMBIGUOUS_MAPPING"),
            ("missing claim", None, "AMBIGUOUS_MAPPING"),
            ("unapproved", {"review_status": "unverified"}, "AMBIGUOUS_MAPPING"),
            ("conflicting", {"review_status": "conflicting"}, "AMBIGUOUS_MAPPING"),
            ("missing document", {"source_document_id": None}, "AMBIGUOUS_MAPPING"),
            ("invalid document", {"source_document_id": "absent"}, "INVALID_CATALOG"),
            ("missing locator", {"locator": None}, "AMBIGUOUS_MAPPING"),
            ("manufacturer mismatch", {"source_document_id": "S23"}, "AMBIGUOUS_MAPPING"),
            ("unqualified class", {"source_class": "derived"}, "AMBIGUOUS_MAPPING"),
            ("retailer cannot establish SoC", {"source_class": "retailer"}, "AMBIGUOUS_MAPPING"),
            ("legacy string", {"value": "GPIO18"}, "AMBIGUOUS_MAPPING"),
            ("no evidence value", {"value": None}, "AMBIGUOUS_MAPPING"),
        )
        for name, update, code in cases:
            with self.subTest(name=name):
                definitions, sources, claims, _, claim = self.typed_data()
                if update is None:
                    claims.remove(claim)
                else:
                    claim.update(update)
                self.error(code, load_catalog, seal(definitions, sources, claims, version="1.1"))

    def test_conflicting_typed_claim_cannot_be_bypassed_by_selecting_another_claim(self):
        for status in ("approved", "conflicting"):
            with self.subTest(status=status):
                definitions, sources, claims, _, claim = self.typed_data()
                claims.append({**claim, "claim_id": "other-mapping", "review_status": status,
                               "value": {**claim["value"], "target_kind": "power_domain"}})
                self.error("AMBIGUOUS_MAPPING", load_catalog, seal(definitions, sources, claims, version="1.1"))

    def test_legacy_cannot_carry_typed_evidence_and_incomplete_mapping_stays_unknown(self):
        definitions, sources, claims, mapping, claim = self.typed_data()
        self.error("INVALID_CATALOG", load_catalog, seal(definitions, sources, claims))
        malformed = json.loads(seal(definitions, sources, claims, version="1.1"))
        typed = next(item["value"] for item in malformed["claims"] if item["claim_id"] == CLAIM)
        del typed["target_kind"]
        self.error("INVALID_CATALOG", load_catalog, encode(malformed))
        mapping.update(mapping_status="unknown", source_claim_id=None)
        claims.remove(claim)
        incomplete = load_catalog(seal(definitions, sources, claims, version="1.1"))
        self.assertEqual(self.board_mapping(incomplete).mapping_status, "unknown")

    def test_legacy_wrong_kind_declaration_has_no_positive_resolved_authority(self):
        definitions, sources, claims = fixture_data()
        board = next(d for d in definitions if d["definition_id"] == BOARD)
        mapping = next(p["signal_ref"] for p in board["terminals"] if p["terminal_id"] == "J3.9")
        mapping["target_kind"] = "power_domain"
        catalog = load_catalog(seal(definitions, sources, claims))
        self.assertEqual(self.board_mapping(catalog).mapping_status, "unknown")

    def test_legacy_snapshot_restore_and_explicit_migration_keep_electrical_membership(self):
        legacy_bytes = seal(*fixture_data())
        old = load_catalog(legacy_bytes, expected_sha256=LEGACY_PIN)
        new = load_catalog(seal(*reviewed_mapping_fixture_data(), version="1.1"))
        self.assertEqual(encode(old.model_dump(mode="json")), legacy_bytes)
        self.assertEqual(self.board_mapping(old).mapping_status, "unknown")
        raw_board = next(item for item in old.definitions if item.definition_id == BOARD)
        raw_pin = next(pin for pin in raw_board.terminals if pin.terminal_id == "J3.9")
        self.assertEqual(raw_pin.signal_ref.mapping_status, "verified")
        self.assertEqual(self.board_mapping(new).mapping_status, "verified")
        self.assertNotEqual(old.catalog_digest, new.catalog_digest)
        self.assertEqual(raw_board.definition_digest, BOARD_DEFINITION_PIN)
        self.assertEqual(old.definitions, new.definitions)

        junction = JunctionRef(junction_id="j")

        def make_snapshot(catalog):
            parts = (part(catalog, "board", BOARD), part(catalog, "sensor", SENSOR),
                     part(catalog, "resistor", PASSIVE))
            return create_snapshot(catalog, instances=parts, junctions=(Junction(junction_id="j"),),
                conductors=(wire("a", t("board", "J3.9"), junction), wire("b", junction, t("sensor", "Trig"))))

        legacy_snapshot = make_snapshot(old)
        new_snapshot = make_snapshot(new)
        self.assertEqual(sha256(serialize_snapshot(legacy_snapshot)).hexdigest(),
                         "2eda9446614581287eff52d1bbe5e7e60140146e46303b97319531c3e73c6b23")
        for snapshot, catalog, other in ((legacy_snapshot, old, new), (new_snapshot, new, old)):
            data = serialize_snapshot(snapshot)
            self.assertEqual(serialize_snapshot(restore_snapshot(data, catalog)), data)
            self.error("CATALOG_MISMATCH", restore_snapshot, data, other)
        before = json.loads(serialize_topology(compute_nets(old, legacy_snapshot)))
        after = json.loads(serialize_topology(compute_nets(new, new_snapshot)))
        self.assertNotEqual(before.pop("snapshot_sha256"), after.pop("snapshot_sha256"))
        self.assertEqual(before, after)
        net = after["terminal_to_net"]["T:board/J3.9"]
        self.assertEqual(net, "net:sha256:2c9d5e8a7f486a3114cc6737d1363c90147ef602c0490e70f96822919212ee31")
        self.assertEqual(net, after["terminal_to_net"]["T:sensor/Trig"])
        self.assertNotEqual(after["terminal_to_net"]["T:resistor/A"], after["terminal_to_net"]["T:resistor/B"])

    def test_source_revision_requires_new_external_pin(self):
        definitions, sources, claims = reviewed_mapping_fixture_data()
        original = load_catalog(seal(definitions, sources, claims, version="1.1"))
        next(s for s in sources if s["source_document_id"] == "S18")["edition"] = "R2 pin-control edition"
        changed = seal(definitions, sources, claims, version="1.1")
        self.error("CATALOG_DIGEST_MISMATCH", load_catalog, changed, expected_sha256=original.catalog_digest)
        unpinned = load_catalog(changed)
        self.assertEqual(self.board_mapping(unpinned).mapping_status, "verified")
        self.assertNotEqual(unpinned.catalog_digest, original.catalog_digest)
        self.assertEqual(unpinned.definitions, original.definitions)
        # A digest supplied by the same input author does not establish external trust.
        self.assertEqual(load_catalog(changed, expected_sha256=unpinned.catalog_digest), unpinned)

    def test_literal_typed_catalog_vector(self):
        # Hand-authored sorted JSON with fixed digests calculated using only hashlib over literal bytes.
        # This miniature invented record is a serialization vector, not hardware evidence.
        definition = (
            b'{"definition_id":"b","definition_schema_version":"1.0","device_class":"dev_board","evidence_claim_ids":[]'
            b',"identity":{"assembled_module":null,"brand_or_distributor":"Maker","hardware_family":"Synthetic vector","hardware_revision":null,"hardware_revision_status":"unverified","manufacturer_name":"Maker","manufacturer_status":"verified","orderable_part_or_sku":"b","profile_scope":"fixture","silicon_revision_status":"unverified","synthetic_test_data":false}'
            b',"internal_ideal_ties":[],"terminals":[{"capability_claim_ids":[],"connector_id":null,"contact_position":null,"contact_type":"pad","electrical_role":"io","printed_label":"P","signal_ref":{"mapping_status":"verified","source_claim_id":"m","target_id":"GPIO18","target_kind":"soc_gpio","terminal_id":"p"},"terminal_id":"p"}]}'
        )
        claim = b'{"claim_id":"m","claim_type":"signal_mapping","condition":null,"conflict_claim_ids":[],"locator":"row 1","qualification":"Synthetic canonical vector only","review_status":"approved","scope":"fixture","source_class":"manufacturer","source_document_id":"s","subject_definition_id":"b","unit":null,"value":{"target_id":"GPIO18","target_kind":"soc_gpio","terminal_id":"p"}}'
        source = b'{"accessed_at_utc":"2026-11-20","download_sha256":null,"edition":"1","media_type":"text/html","publication_date":null,"publisher":"Maker","rights_state":"link_only","source_document_id":"s","title":"Vector","url":"https://example.invalid/vector"}'
        catalog_pin = b"sha256:18975dcdc4a645f586820d8d16c8c4b0f2a44438e9cd6f31615a19dc27b42a62"
        definition_pin = b"sha256:0cbfb905aa8c3773ea5e7edc27efee448c78d6d3fdd8d8a6fdf7bf9030afc8ce"
        payload = (
            b'{"catalog_digest":"' + catalog_pin + b'","catalog_schema_version":"1.1","claims":[' + claim
            + b'],"definitions":[{"definition_digest":"' + definition_pin + b'",' + definition[1:]
            + b'],"source_documents":[' + source + b']}'
        )
        admitted = load_catalog(payload, expected_sha256=catalog_pin.decode())
        self.assertEqual(encode(admitted.model_dump(mode="json")), payload)
        self.assertEqual(admitted.definitions[0].definition_digest, definition_pin.decode())
        self.error("SCHEMA_UNSUPPORTED", load_catalog, payload.replace(b'"1.1"', b'"1.2"', 1))
