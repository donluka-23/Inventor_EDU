import json
import unittest
from itertools import combinations

import networkx as nx
from hypothesis import given, seed, settings, strategies as st

from inventor_edu import (
    CircuitSnapshot, ComponentInstance, EngineeringModelError, Junction, JunctionRef,
    compute_nets, create_snapshot, load_catalog, resolve_terminal, restore_snapshot,
    serialize_snapshot, serialize_topology,
)
from tests.core001a_fixtures import (
    BOARD, MODULE, PASSIVE, SENSOR, ZERO, encode, fixture_data, part, seal, synthetic, t, wire,
)


def partition(result):
    return {frozenset(net.members) for net in result.nets}


class CoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = seal(*fixture_data())
        cls.catalog = load_catalog(cls.payload)

    def snapshot(self, wires=(), junctions=(), instances=None):
        if instances is None:
            instances = (part(self.catalog, "a"), part(self.catalog, "b"))
        return create_snapshot(self.catalog, instances=instances, conductors=tuple(wires),
                               junctions=tuple(Junction(junction_id=key) for key in junctions))

    def error(self, code, call, *args, **kwargs):
        with self.assertRaises(EngineeringModelError) as caught:
            call(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def test_three_terminals_junction_and_reordering(self):
        j, k = JunctionRef(junction_id="j"), JunctionRef(junction_id="k")
        a, b, c = t("a", "A"), t("a", "B"), t("b", "A")
        wires = (wire("1", a, j), wire("2", b, j), wire("3", j, k), wire("4", k, c))
        first = self.snapshot(wires, ("j", "k"))
        second = self.snapshot(tuple(wire(w.connection_id, w.endpoint_b, w.endpoint_a) for w in reversed(wires)),
                               ("k", "j"), first.instances[::-1])
        result = compute_nets(self.catalog, first)
        self.assertEqual(partition(result), {frozenset(("T:a/A", "T:a/B", "T:b/A")), frozenset(("T:b/B",))})
        self.assertEqual(result.isolated_terminals, ("T:b/B",))
        self.assertEqual(serialize_snapshot(first), serialize_snapshot(second))
        self.assertEqual(result, compute_nets(self.catalog, second))

    def test_deletion_duplicate_and_hash_vector(self):
        a, b, c = t("a", "A"), t("a", "B"), t("b", "A")
        first, second, duplicate = wire("1", a, b), wire("2", b, c), wire("3", c, b)
        original = compute_nets(self.catalog, self.snapshot((first, second, duplicate)))
        retained = compute_nets(self.catalog, self.snapshot((first, duplicate)))
        split = compute_nets(self.catalog, self.snapshot((first,)))
        self.assertEqual(original.terminal_to_net, retained.terminal_to_net)
        self.assertEqual(set(dict(original.connection_to_net)), {"1", "2", "3"})
        self.assertNotEqual(original.snapshot_sha256, retained.snapshot_sha256)
        self.assertEqual(partition(split), {frozenset(("T:a/A", "T:a/B")), frozenset(("T:b/A",)),
                                           frozenset(("T:b/B",))})
        self.assertEqual(dict(split.terminal_to_net)["T:a/A"],
                         "net:sha256:c226830ef614b43a85d20b6eae3117e59ee5ddb472638cc6f9e59d413e015735")

    def test_crossings_and_geometry_independence(self):
        snapshot = self.snapshot((wire("1", t("a", "A"), t("a", "B")),
                                  wire("2", t("b", "A"), t("b", "B"))))
        views = [{"snapshot": snapshot, "geometry": segments} for segments in (
            (((-1, 0), (1, 0)), ((0, -1), (0, 1))),
            (((-1, 0), (1, 0)), ((-1, 2), (1, 2))),
        )]
        first, second = [serialize_topology(compute_nets(self.catalog, view["snapshot"])) for view in views]
        self.assertEqual(first, second)
        self.assertEqual(json.loads(first)["nets"][0]["members"], ["T:a/A", "T:a/B"])
        self.assertEqual(json.loads(first)["nets"][1]["members"], ["T:b/A", "T:b/B"])

    def test_junction_only_and_singleton_with_stub(self):
        j, k, stub = [JunctionRef(junction_id=key) for key in ("j", "k", "stub")]
        snapshot = self.snapshot((wire("orphan", k, j), wire("stub", stub, t("a", "A"))),
                                 ("z", "j", "k", "stub"))
        data = json.loads(serialize_topology(compute_nets(self.catalog, snapshot)))
        self.assertEqual(len(data["nets"]), 4)
        self.assertEqual(data["isolated_terminals"], ["T:a/A", "T:a/B", "T:b/A", "T:b/B"])
        self.assertEqual(data["connection_to_net"], {"orphan": None, "stub": data["terminal_to_net"]["T:a/A"]})
        self.assertEqual(data["diagnostics"], [
            {"code": "JUNCTION_ONLY_GROUP", "junction_ids": ["j", "k"], "conductor_ids": ["orphan"]},
            {"code": "JUNCTION_ONLY_GROUP", "junction_ids": ["z"], "conductor_ids": []},
        ])

    def test_reference_profiles_and_generalization(self):
        choices = (("brd", BOARD), ("brd2", BOARD), ("sensor", SENSOR), ("resistor", PASSIVE), ("chip", MODULE))
        snapshot = self.snapshot(instances=tuple(part(self.catalog, a, b) for a, b in choices))
        result = compute_nets(self.catalog, snapshot)
        memberships = partition(result)
        for board in ("brd", "brd2"):
            self.assertIn(frozenset(f"T:{board}/{key}" for key in ("J2.14", "J3.1", "J3.7")), memberships)
        for key in ("brd/J2.19", "brd/J2.1", "sensor/Gnd", "resistor/A", "resistor/B",
                    "chip/P1", "chip/P2", "chip/P3"):
            self.assertIn(frozenset((f"T:{key}",)), memberships)
        joined = self.snapshot((wire("direct", t("resistor", "A"), t("chip", "P2")),), instances=snapshot.instances)
        self.assertIn(frozenset(("T:resistor/A", "T:chip/P2")), partition(compute_nets(self.catalog, joined)))
        pin = resolve_terminal(self.catalog, snapshot, t("brd", "J3.9")).terminal
        self.assertEqual((pin.terminal_id, pin.signal_ref.target_id), ("J3.9", "GPIO18"))

    def test_evidence_admission(self):
        for changes in ({"value": ["J2.14", "J3.1"]}, {"scope": "Different assembly"},
                        {"review_status": "unverified"}, {"locator": None}, {"source_class": "retailer"},
                        {"review_status": "conflicting"}):
            with self.subTest(changes=changes):
                definitions, sources, claims = fixture_data()
                next(item for item in claims if item["claim_id"] == "board-ground").update(changes)
                self.error("INVALID_IDEAL_TIE", load_catalog, seal(definitions, sources, claims))
        definitions, sources, claims = fixture_data()
        self.error("INVALID_IDEAL_TIE", load_catalog, seal(definitions, sources,
                   [item for item in claims if item["claim_id"] != "board-ground"]))
        disputed = next(item for item in claims if item["claim_id"] == "board-ground")
        claims.append({**disputed, "claim_id": "disputed-ground", "review_status": "conflicting"})
        self.error("INVALID_IDEAL_TIE", load_catalog, seal(definitions, sources, claims))
        opaque = synthetic("synthetic-tie", "test_fixture", ("A", "B"), "lead")
        opaque["internal_ideal_ties"] = [{"evidence_claim_id": "test-tie", "terminal_ids": ["A", "B"]}]
        claim = dict(claim_id="test-tie", claim_type="internal_ideal_tie", subject_definition_id="synthetic-tie",
                     value=["A", "B"], source_class="synthetic", scope="Synthetic topology fixture",
                     qualification="Artificial equivalence for a graph test", review_status="approved")
        catalog = load_catalog(seal([opaque], claims=[claim]))
        snapshot = create_snapshot(catalog, instances=(part(catalog, "a", "synthetic-tie"),),
                                   conductors=(), junctions=())
        self.assertEqual(partition(compute_nets(catalog, snapshot)), {frozenset(("T:a/A", "T:a/B"))})

    def test_invalid_endpoints_ids_and_identity(self):
        a, b = t("a", "A"), t("a", "B")
        for code, endpoint in (("UNKNOWN_INSTANCE", t("missing", "A")), ("UNKNOWN_TERMINAL", t("a", "P9")),
                               ("INVALID_ENDPOINT", JunctionRef(junction_id="missing")), ("SELF_LOOP", a)):
            self.error(code, self.snapshot, (wire("w", a, endpoint),))
        self.error("DUPLICATE_ID", self.snapshot, (wire("w", a, b), wire("w", b, a)))
        self.error("DUPLICATE_ID", self.snapshot, instances=(part(self.catalog, "a"),) * 2)
        self.error("DUPLICATE_ID", self.snapshot, junctions=("j", "j"))
        for key in ("generic-clone-hcsr04", "ESP32-DevKitC"):
            instance = ComponentInstance(instance_id="a", definition_id=key, definition_digest=ZERO)
            self.error("UNKNOWN_DEFINITION", self.snapshot, instances=(instance,))

    def test_canonical_round_trip_and_digest_mismatches(self):
        snapshot = self.snapshot((wire("w", t("b", "B"), t("a", "A")),))
        payload = serialize_snapshot(snapshot)
        raw = json.loads(payload)
        raw["instances"].reverse()
        self.assertEqual(serialize_snapshot(restore_snapshot(json.dumps(raw).encode(), self.catalog)), payload)
        self.assertEqual(serialize_snapshot(restore_snapshot(payload, self.catalog)), payload)
        self.error("CATALOG_MISMATCH", restore_snapshot, encode({**raw, "catalog_digest": ZERO}), self.catalog)
        raw["instances"][0]["definition_digest"] = ZERO
        self.error("CATALOG_DIGEST_MISMATCH", restore_snapshot, encode(raw), self.catalog)
        self.error("CATALOG_DIGEST_MISMATCH", load_catalog, self.payload, expected_sha256=ZERO)
        catalog_json = json.loads(self.payload)
        catalog_json["definitions"].reverse()
        catalog_json["source_documents"].reverse()
        catalog_json["claims"].reverse()
        self.assertEqual(load_catalog(encode(catalog_json)), self.catalog)
        board = next(d for d in catalog_json["definitions"] if d["definition_id"] == BOARD)
        next(p for p in board["terminals"] if p["terminal_id"] == "J3.9")["signal_ref"]["target_id"] = "GPIO19"
        self.error("CATALOG_DIGEST_MISMATCH", load_catalog, encode(catalog_json))

    def test_literal_canonical_snapshot_vector(self):
        expected = (b'{"catalog_digest":"' + ZERO.encode() +
                    b'","conductors":[],"instances":[],"junctions":[],"schema_version":"1.0"}')
        record = CircuitSnapshot(schema_version="1.0", catalog_digest=ZERO, conductors=(),
                                 instances=(), junctions=())
        self.assertEqual(serialize_snapshot(record), expected)

    def test_strict_schema_and_resource_limits(self):
        raw = json.loads(serialize_snapshot(self.snapshot()))
        self.error("SCHEMA_UNSUPPORTED", restore_snapshot, encode({**raw, "schema_version": "2.0"}), self.catalog)
        self.error("INVALID_SNAPSHOT", restore_snapshot, encode({**raw, "geometry": []}), self.catalog)
        self.assertIn("endpoint_a", type(wire("w", t("a", "A"), t("a", "B"))).model_json_schema()["properties"])
        self.error("MALFORMED_JSON", restore_snapshot, b'{"a":1,"a":2}', self.catalog)
        self.error("MALFORMED_JSON", restore_snapshot, b'{"x":0.1}', self.catalog)
        self.error("INVALID_ENDPOINT", restore_snapshot, encode({**raw, "conductors": [
            {"connection_id": "unfinished", "endpoint_a": {"kind": "terminal", "instance_id": "a", "terminal_id": "A"}}
        ]}), self.catalog)
        oversized = b" " * (4 * 1024 * 1024 + 1)
        for call, args in ((load_catalog, (oversized,)), (restore_snapshot, (oversized, self.catalog))):
            self.assertEqual(self.error("RESOURCE_LIMIT_EXCEEDED", call, *args).path, ("json_bytes",))
        make = ((("instances",), {"instances": (part(self.catalog, "a"),) * 129}),
                (("junctions",), {"junctions": ("j",) * 8193}),
                (("conductors",), {"wires": (wire("w", t("a", "A"), t("a", "B")),) * 16385}))
        for path, kwargs in make:
            self.assertEqual(self.error("RESOURCE_LIMIT_EXCEEDED", self.snapshot, **kwargs).path, path)
        catalog = load_catalog(seal([synthetic("many", "test", [f"p{i}" for i in range(65)], "pad")]))
        instances = tuple(part(catalog, f"a{i}", "many") for i in range(127))
        self.assertEqual(self.error("RESOURCE_LIMIT_EXCEEDED", create_snapshot, catalog, instances=instances,
                                    junctions=(), conductors=()).path, ("terminals",))

    @seed(1001)
    @settings(max_examples=80, database=None, deadline=None)
    @given(st.lists(st.sampled_from(list(combinations(range(6), 2))), max_size=15), st.data())
    def test_networkx_oracle_permutation_partition_and_single_edge_deletion(self, edges, data):
        nodes = [t("a", "A"), t("a", "B"), t("b", "A"), t("b", "B"),
                 JunctionRef(junction_id="j"), JunctionRef(junction_id="k")]
        keys = ["T:a/A", "T:a/B", "T:b/A", "T:b/B"]
        wires = [wire(f"w{i}", nodes[a], nodes[b]) for i, (a, b) in enumerate(edges)]

        def expected(selected):
            graph = nx.Graph()
            graph.add_nodes_from(range(6))
            graph.add_edges_from(selected)
            return {frozenset(keys[i] for i in group if i < 4)
                    for group in nx.connected_components(graph) if any(i < 4 for i in group)}

        original = self.snapshot(wires, ("j", "k"))
        result = compute_nets(self.catalog, original)
        shuffled = data.draw(st.permutations(wires))
        permuted = self.snapshot([wire(w.connection_id, w.endpoint_b, w.endpoint_a) for w in shuffled],
                                 ("k", "j"), original.instances[::-1])
        self.assertEqual(serialize_snapshot(original), serialize_snapshot(permuted))
        self.assertEqual(result, compute_nets(self.catalog, permuted))
        self.assertEqual(partition(result), expected(edges))
        self.assertEqual(sorted(key for n in result.nets for key in n.members), keys)
        if edges:
            i = data.draw(st.integers(min_value=0, max_value=len(edges) - 1))
            reduced = compute_nets(self.catalog, self.snapshot(wires[:i] + wires[i + 1:], ("j", "k")))
            self.assertEqual(partition(reduced), expected(edges[:i] + edges[i + 1:]))
            self.assertIn(len(reduced.nets) - len(result.nets), (0, 1))
        i = data.draw(st.integers(min_value=0, max_value=3))
        invalid = data.draw(st.sampled_from(("instance", "terminal")))
        invalid_ref = t("absent", "A") if invalid == "instance" else t(nodes[i].instance_id, "absent")
        self.error("UNKNOWN_" + invalid.upper(), self.snapshot,
                   wires + [wire("invalid", nodes[i], invalid_ref)], ("j", "k"))

    def test_mapping_rejects_resealed_mismatched_or_unapproved_evidence(self):
        cases = (
            ("wrong target ID", {"value": "GPIO19"}),
            ("wrong physical contact", {"condition": "J3.8"}),
            ("wrong definition", {"subject_definition_id": SENSOR}),
            ("wrong profile", {"scope": "Different assembly"}),
            ("missing document", {"source_document_id": None}),
            ("conflicting approval", {"review_status": "conflicting"}),
            ("unapproved", {"review_status": "unverified"}),
            ("missing claim", None),
        )
        for name, change in cases:
            with self.subTest(name=name):
                definitions, sources, claims = fixture_data()
                claim = next(item for item in claims if item["claim_id"] == "board-J3.9")
                if change is None:
                    claims.remove(claim)
                else:
                    claim.update(change)
                # A fresh digest isolates the semantic evidence check.
                self.error("AMBIGUOUS_MAPPING", load_catalog, seal(definitions, sources, claims))

    def test_source_edition_changes_catalog_pin_without_changing_connectivity(self):
        definitions, sources, claims = fixture_data()
        next(source for source in sources if source["source_document_id"] == "S18")["edition"] = "R1 test edition"
        payload = seal(definitions, sources, claims)
        self.error("CATALOG_DIGEST_MISMATCH", load_catalog, payload, expected_sha256=self.catalog.catalog_digest)
        updated = load_catalog(payload)
        self.assertNotEqual(self.catalog.catalog_digest, updated.catalog_digest)

        def board_snapshot(catalog):
            return create_snapshot(catalog, instances=(part(catalog, "board", BOARD),),
                                   junctions=(), conductors=())

        original, revised = board_snapshot(self.catalog), board_snapshot(updated)
        self.assertEqual(original.instances[0].definition_digest, revised.instances[0].definition_digest)
        mapping = resolve_terminal(updated, revised, t("board", "J3.9")).terminal.signal_ref
        self.assertEqual((mapping.mapping_status, mapping.target_kind, mapping.target_id),
                         ("unknown", "soc_gpio", "GPIO18"))
        encoded = serialize_snapshot(revised)
        self.assertEqual(serialize_snapshot(restore_snapshot(encoded, updated)), encoded)
        self.error("CATALOG_MISMATCH", restore_snapshot, encoded, self.catalog)
        self.assertEqual(compute_nets(self.catalog, original).nets, compute_nets(updated, revised).nets)
