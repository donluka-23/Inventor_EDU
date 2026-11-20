"""Replay two real canonical wiring failures and recovery of the tested E2 divider."""

import argparse
import json

from examples.core001c_e1_voltage_cases import fixture_cases
from examples.edu001_learning_cycle import load_fixture
from inventor_edu.core import create_snapshot, load_catalog
from inventor_edu.divider_topology import DividerTopologyBinding, TerminalAnchor, bind_ideal_divider_to_snapshot
from inventor_edu.gpio_facts import canonical_json, digest_bytes
from inventor_edu.models import CatalogSnapshot, ComponentInstance, Conductor, DeviceDefinition, DeviceIdentity
from inventor_edu.models import TerminalDefinition, TerminalRef
from inventor_edu.voltage_model import SnapshotAssociation


def synthetic_definition(key, device_class, contacts):
    definition = DeviceDefinition(
        definition_schema_version="1.0", definition_id=key, device_class=device_class,
        definition_digest="sha256:" + "0" * 64,
        identity=DeviceIdentity(
            brand_or_distributor="E2 synthetic", manufacturer_status="unverified", orderable_part_or_sku=key,
            hardware_family="E2 fixture", hardware_revision_status="unverified",
            silicon_revision_status="unverified", profile_scope="Test-only virtual topology", synthetic_test_data=True,
        ),
        terminals=tuple(TerminalDefinition(terminal_id=contact, contact_type="fixture_contact",
                                           printed_label=contact, electrical_role=role)
                        for contact, role in sorted(contacts)),
    )
    body = definition.model_dump(mode="json", exclude={"definition_digest"})
    return definition.model_copy(update={"definition_digest": digest_bytes(canonical_json(body))})


def admit_test_catalog(definitions, base: CatalogSnapshot | None = None) -> CatalogSnapshot:
    """Derive a local test pin, then pass the composite through public CORE admission."""
    if base is None:
        body = {"catalog_schema_version": "1.1", "definitions": [], "source_documents": [], "claims": []}
    else:
        body = base.model_dump(mode="json", exclude={"catalog_digest"})
        if digest_bytes(canonical_json(body)) != base.catalog_digest:
            raise ValueError("BASE_FIXTURE_NOT_IN_CANONICAL_ORDER")
    body["definitions"].extend(item.model_dump(mode="json") for item in definitions)
    body["definitions"].sort(key=lambda item: item["definition_id"])
    pin = digest_bytes(canonical_json(body))
    return load_catalog(canonical_json(dict(body, catalog_digest=pin)), expected_sha256=pin)


def contact(instance_id, terminal_id):
    return TerminalRef(instance_id=instance_id, terminal_id=terminal_id)


def wire(key, first, second):
    return Conductor(connection_id=key, endpoint_a=first, endpoint_b=second)


def primary_fixture():
    reviewed, _, existing_instances = load_fixture()
    resistors = tuple(synthetic_definition(key, "passive_resistor", (("high", "other"), ("low", "other")))
                      for key in ("e2-top-resistor", "e2-bottom-resistor"))
    catalog = admit_test_catalog(resistors, reviewed)
    instances = (*existing_instances, *(ComponentInstance(
        instance_id=key, definition_id=definition.definition_id, definition_digest=definition.definition_digest,
    ) for key, definition in zip(("r-top", "r-bottom"), resistors, strict=True)))
    roles = {
        "source_out": contact("sensor", "Echo"), "receiver_input": contact("board", "J3.8"),
        "reference_ground": contact("board", "J2.14"), "r_top_hi": contact("r-top", "high"),
        "r_top_lo": contact("r-top", "low"), "r_bottom_hi": contact("r-bottom", "high"),
        "r_bottom_lo": contact("r-bottom", "low"),
    }
    wires = (
        wire("source-wire", roles["source_out"], roles["r_top_hi"]),
        wire("mid-series", roles["r_top_lo"], roles["r_bottom_hi"]),
        wire("mid-receiver", roles["r_bottom_hi"], roles["receiver_input"]),
        wire("ground-return", roles["r_bottom_lo"], roles["reference_ground"]),
        wire("trig-wire", contact("board", "J3.9"), contact("sensor", "Trig")),
    )
    return catalog, instances, roles, wires


def bind_fixture(catalog, snapshot, roles, hypothesis):
    association = SnapshotAssociation.from_core(catalog, snapshot)
    instances = {item.instance_id: item for item in snapshot.instances}
    binding = DividerTopologyBinding(
        **association.model_dump(), qualification="TEST_ONLY_MODEL_ASSUMPTIONS",
        **{role: TerminalAnchor(ref=ref, definition_digest=instances[ref.instance_id].definition_digest)
           for role, ref in roles.items()},
    )
    return binding, hypothesis.model_copy(update={"association": association})


def rewire(wires, key, endpoint, target):
    return tuple(item.model_copy(update={endpoint: target}) if item.connection_id == key else item for item in wires)


def run_cases():
    catalog, instances, roles, correct = primary_fixture()
    hypothesis = fixture_cases()[1]
    receiver_on_source = rewire(correct, "mid-receiver", "endpoint_a", roles["r_top_hi"])
    return_on_source = rewire(correct, "ground-return", "endpoint_b", roles["source_out"])
    restored = rewire(receiver_on_source, "mid-receiver", "endpoint_a", roles["r_bottom_hi"])
    results = []
    for label, wires in (("A-correct", correct), ("B1-receiver-on-source", receiver_on_source),
                         ("B2-return-on-source", return_on_source), ("A-restored", restored)):
        snapshot = create_snapshot(catalog, instances=instances, junctions=(), conductors=wires)
        binding, current_hypothesis = bind_fixture(catalog, snapshot, roles, hypothesis)
        results.append((label, bind_ideal_divider_to_snapshot(catalog, snapshot, binding, current_hypothesis)))
    return tuple(results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit deterministic UTF-8 JSON")
    args = parser.parse_args()
    cases = run_cases()
    if args.json:
        print(json.dumps({key: report.model_dump(mode="json") for key, report in cases},
                         ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return
    for name, report in cases:
        print(f"{name} | {report.restriction} | {report.hardware_qualification}")
        print(f"  {report.snapshot_digest} | {report.motif_state} | {report.math_state}")
        for net in report.observed_nets:
            print(f"  {net.net_id} | {', '.join(net.members)} | wires={','.join(net.connection_ids)}")
        for row in report.checks:
            if row.status in {"REJECTED", "UNRESOLVED"}:
                print(f"  {row.rule_id} | {row.reason_code} | affected={','.join(row.affected_net_ids)}")
        if report.model_report is not None:
            math = report.model_report.calculation
            print(f"  Vout={math.output_voltage.lower.decimal_12dp} V | "
                  f"conditional HIGH margin={math.high_margin.decimal_12dp} V | {report.model_digest}")
    print("Test-only resistor bodies and assumed model values. Actual component values and hardware conditions are unestablished.")


if __name__ == "__main__":
    main()
