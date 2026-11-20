"""Independent structural, integrity and topology checks for the selected DATA-001 records."""

from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
import unittest

from inventor_edu import (
    Junction, JunctionRef, compute_nets, create_snapshot, load_catalog, resolve_terminal,
    restore_snapshot, serialize_snapshot, serialize_topology,
)
from inventor_edu.librepcb_pilot import (
    COMPONENT, DEVICE, PACKAGE, PINNED_FILES, PilotSourceError, _extract, _parse, build_candidate,
)
from tests.core001a_fixtures import BOARD, SENSOR, part, reviewed_mapping_fixture_data, seal, t, wire

P1 = "ad768910-1573-409f-81d4-d4c7692ab494"
P2 = "65ab6c75-b264-4fed-b445-d3d98c956008"
S1 = "3452d36e-1ce8-4b7c-8e5b-90c2e4929ed8"
S2 = "ad623f98-9e73-49c3-9404-f7cfa99d17cd"
CATALOG = "sha256:1d0094e60730c9daea083fcf63170e24cef90bd27d22af789cab628064002057"
DEF = "librepcb-483a71eb-318e-448e-82ff-f02efc4821aa"
DATA = Path(__file__).resolve().parents[1] / "data" / "pilot"


def synthetic_structure():
    """Minimal scaffolding for negative join tests, independent of the downloaded records."""
    signals = "".join(
        f'(signal {key} (name "{name}") (role passive) (required true) '
        '(negated false) (clock false) (forced_net ""))'
        for key, name in ((S1, "one"), (S2, "two"))
    )
    contacts = f'(pad {P1} (name "1")) (pad {P2} (name "2"))'
    layout = "".join(f"(pad {key} (side top) (function standard) (package_pad {key}))" for key in (P1, P2))
    joins = f"(pad {P1} (optional false) (signal {S1})) (pad {P2} (optional false) (signal {S2}))"
    return (
        f"(librepcb_component {COMPONENT} (deprecated false) (schematic_only false) {signals})".encode(),
        f"(librepcb_package {PACKAGE} (deprecated false) (assembly_type smt) {contacts} "
        f"(footprint {PACKAGE} {layout}))".encode(),
        f"(librepcb_device {DEVICE} (deprecated false) (component {COMPONENT}) (package {PACKAGE}) "
        f"(approved no_parts) {joins})".encode(),
    )


class ParserNegativeTests(unittest.TestCase):
    def test_parser_rejects_unsupported_or_unbounded_syntax(self):
        for bad in (b"(a (b)", b"(a) (b)", b'(a "b"c)', b'(a ("quoted-head" 1))',
                    b'(a (b "\\q"))', b"(a (b ; comment))", b"\xff",
                    b"(a " * 25 + b")" * 25, b"(a " + b"x " * 12001 + b")",
                    b" " * 65537):
            with self.subTest(prefix=bad[:24]):
                with self.assertRaises(PilotSourceError):
                    _parse(bad)

    def test_join_rejects_duplicates_and_dangling_relationships(self):
        cmp, pkg, dev = synthetic_structure()
        for changed in (
            (cmp.replace(S2.encode(), S1.encode()), pkg, dev),
            (cmp, pkg.replace(P2.encode(), P1.encode()), dev),
            (cmp, pkg, dev.replace(P2.encode(), P1.encode())),
            (cmp, pkg, dev.replace(S2.encode(), DEVICE.encode())),
            (cmp, pkg, dev.replace(S2.encode(), S1.encode())),
            (cmp, pkg, dev.replace(f"(package {PACKAGE})".encode(), f"(package {COMPONENT})".encode())),
            (cmp, pkg.replace(f"(package_pad {P2})".encode(), f"(package_pad {DEVICE})".encode()), dev),
            (cmp, pkg.replace(b'(name "2")', b'(name "1")'), dev),
            (cmp, pkg, dev.replace(b"(optional false)", b"(optional true)", 1)),
            (cmp, pkg, dev.replace(b"(approved no_parts)", b'(part "unreviewed")')),
        ):
            with self.subTest(changed=changed):
                with self.assertRaises(PilotSourceError):
                    _extract(*changed)

    def test_yageo_claims_are_separate_candidates_and_unknowns_are_null(self):
        facts = json.loads((DATA / "yageo_rc0603fr_0710kl_candidate.json").read_bytes())
        self.assertEqual((facts["manufacturer"], facts["mpn"]), ("YAGEO", "RC0603FR-0710KL"))
        self.assertEqual(facts["catalog_admission"], "HOLD")
        for key in ("independent_engineering_approval", "librepcb_device_match", "admitted_electrical_limits"):
            self.assertIsNone(facts[key])


class AuthenticSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = os.getenv("INVENTOR_EDU_DATA001_SOURCE_DIR")
        if source is None:
            raise unittest.SkipTest("Set INVENTOR_EDU_DATA001_SOURCE_DIR using the DATA-001 ledger")
        cls.source = Path(source)
        cls.payload = build_candidate(cls.source)
        cls.catalog = load_catalog(cls.payload, expected_sha256=CATALOG)

    def test_actual_sources_preserve_independently_reviewed_pad_and_signal_identities(self):
        (device,) = self.catalog.definitions
        self.assertEqual(device.definition_id, DEF)
        self.assertEqual(device.identity.manufacturer_status, "unverified")
        self.assertIsNone(device.identity.manufacturer_name)
        self.assertNotIn(b"RC0603FR-0710KL", self.payload)
        self.assertEqual({(p.terminal_id, p.printed_label) for p in device.terminals}, {(P1, "1"), (P2, "2")})
        self.assertEqual({(c.condition, c.value) for c in self.catalog.claims}, {(P1, S1), (P2, S2)})
        self.assertTrue(all(c.review_status == "unverified" for c in self.catalog.claims))
        self.assertEqual({(s.source_document_id, s.download_sha256) for s in self.catalog.source_documents}, {
            ("component", "sha256:8e76dc4bfaf40f56e6856883b4dee5af0f2c368633c3e3c9a7031fcdf1b17b07"),
            ("package", "sha256:61ee014c8bb7200eaf4c523b044dbc8090d8074c923059cfba46d601c98900c8"),
            ("device", "sha256:3c4cce7d485a1260ac5980bb0ad1d5c9c292f384a49a9a920e95912092431a80"),
        })
        self.assertTrue(all("/dc037a238eb5efcc034dd9d62e5775d5c21e90e4/" in s.url
                            for s in self.catalog.source_documents))
        self.assertEqual(device.internal_ideal_ties, ())
        self.assertTrue(all(p.signal_ref is None and p.electrical_role == "unknown" for p in device.terminals))
        self.assertEqual(self.payload, (DATA / "librepcb_resistor_catalog.json").read_bytes())
        self.assertEqual(build_candidate(self.source), self.payload)
        self.assertEqual(sha256(self.payload).hexdigest(),
                         "891405396e2e8e2210ca4847cc11d2488354647dee8f451f42e5e1e88f602558")

    def test_modified_data_license_or_format_never_reuses_pins(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative, _ in PINNED_FILES:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((self.source / relative).read_bytes())
            for suffix in ("device.lp", "LICENSE.txt", ".librepcb-pkg"):
                relative = next(path for path, _ in PINNED_FILES if path.endswith(suffix))
                file = root / relative
                original = file.read_bytes()
                with self.subTest(relative=relative):
                    file.write_bytes(original + b" ")
                    with self.assertRaisesRegex(PilotSourceError, "pinned digest mismatch"):
                        build_candidate(root)
                    file.write_bytes(original)
            self.assertEqual(build_candidate(root), self.payload)

    def test_isolated_candidate_has_two_singleton_nets(self):
        snapshot = create_snapshot(self.catalog, instances=(part(self.catalog, "r", DEF),),
                                   junctions=(), conductors=())
        topology = compute_nets(self.catalog, snapshot)
        self.assertEqual({n.members for n in topology.nets}, {(f"T:r/{P1}",), (f"T:r/{P2}",)})
        self.assertEqual(resolve_terminal(self.catalog, snapshot, t("r", P1)).terminal.printed_label, "1")
        self.assertEqual(resolve_terminal(self.catalog, snapshot, t("r", P2)).terminal.printed_label, "2")
        self.assertEqual(set(json.loads(serialize_topology(topology))), {
            "topology_schema_version", "snapshot_sha256", "nets", "terminal_to_net",
            "connection_to_net", "isolated_terminals", "diagnostics",
        })

    def test_real_import_wired_into_reviewed_fixture_and_deterministic_replay(self):
        defs, docs, claims = reviewed_mapping_fixture_data()
        defs = [d for d in defs if d["definition_id"] in {BOARD, SENSOR}]
        other = load_catalog(seal(defs, docs, claims, version="1.1"))
        imported = json.loads(self.payload)
        mixed = load_catalog(seal(defs + imported["definitions"], docs + imported["source_documents"],
                                  claims + imported["claims"], version="1.1"))
        self.assertEqual(next(d for d in mixed.definitions if d.definition_id == DEF),
                         self.catalog.definitions[0])
        initial = (part(other, "board", BOARD), part(other, "sensor", SENSOR))
        baseline = create_snapshot(other, instances=initial, junctions=(), conductors=())
        unrelated = {
            ("T:board/J2.1",), ("T:board/J2.5",), ("T:board/J2.19",), ("T:board/J3.8",),
            ("T:board/J2.14", "T:board/J3.1", "T:board/J3.7"),
            ("T:sensor/Echo",), ("T:sensor/Gnd",), ("T:sensor/Vcc",),
        }
        self.assertEqual({n.members for n in compute_nets(other, baseline).nets},
                         unrelated | {("T:board/J3.9",), ("T:sensor/Trig",)})
        parts = (*initial, part(mixed, "r", DEF))
        j = Junction(junction_id="j")
        jr = JunctionRef(junction_id="j")
        wires = (wire("a", t("board", "J3.9"), jr), wire("b", jr, t("r", P1)),
                 wire("c", t("r", P2), t("sensor", "Trig")))
        snapshot = create_snapshot(mixed, instances=parts, junctions=(j,), conductors=wires)
        topology = compute_nets(mixed, snapshot)
        self.assertEqual({n.members for n in topology.nets}, unrelated | {
            ("T:board/J3.9", f"T:r/{P1}"), (f"T:r/{P2}", "T:sensor/Trig"),
        })
        connections = dict(topology.connection_to_net)
        self.assertEqual(set(connections), {"a", "b", "c"})
        self.assertEqual(connections["a"], connections["b"])
        self.assertNotEqual(connections["a"], connections["c"])
        reordered = create_snapshot(mixed, instances=parts[::-1], junctions=(j,),
            conductors=tuple(wire(w.connection_id, w.endpoint_b, w.endpoint_a) for w in reversed(wires)))
        raw = serialize_snapshot(snapshot)
        self.assertEqual(serialize_snapshot(reordered), raw)
        restored = restore_snapshot(raw, mixed)
        self.assertEqual(restored.catalog_digest, mixed.catalog_digest)
        for case in (reordered, restored):
            self.assertEqual(serialize_topology(compute_nets(mixed, case)), serialize_topology(topology))
