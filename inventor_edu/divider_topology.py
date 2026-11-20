"""Bind E1 assumptions to a CORE-observed, test-only two-resistor motif."""

from typing import Literal

from .core import compute_nets, create_snapshot
from .gpio_facts import canonical_json, digest_bytes
from .models import CatalogSnapshot, CircuitSnapshot, Digest, Identifier, Record, TerminalRef
from .voltage_model import IdealDividerHypothesis, SnapshotAssociation, VoltageModelReport, evaluate_ideal_divider

ALGORITHM_VERSION = "divider-topology-e2-v1"
RESISTOR_CLASS = "passive_resistor"
Role = Literal[
    "source_out", "receiver_input", "reference_ground", "r_top_hi", "r_top_lo", "r_bottom_hi", "r_bottom_lo",
]
ROLES: tuple[Role, ...] = (
    "source_out", "receiver_input", "reference_ground", "r_top_hi", "r_top_lo", "r_bottom_hi", "r_bottom_lo",
)
MotifState = Literal["CANONICAL_MOTIF_MATCHED", "MOTIF_NOT_ADMITTED", "MODEL_SCOPE_UNRESOLVED"]


class TerminalAnchor(Record):
    ref: TerminalRef
    definition_digest: Digest


class DividerTopologyBinding(Record):
    schema_version: Literal["1.0"] = "1.0"
    qualification: Literal["TEST_ONLY_MODEL_ASSUMPTIONS"]
    catalog_digest: Digest
    snapshot_digest: Digest
    source_out: TerminalAnchor
    receiver_input: TerminalAnchor
    reference_ground: TerminalAnchor
    r_top_hi: TerminalAnchor
    r_top_lo: TerminalAnchor
    r_bottom_hi: TerminalAnchor
    r_bottom_lo: TerminalAnchor


class ObservedAnchor(Record):
    role: Role
    anchor: TerminalAnchor
    observed_definition_digest: Digest | None
    net_id: str | None
    status: Literal["MATCHED", "REJECTED"]


class MotifNetIds(Record):
    source: str | None
    midpoint: str | None
    ground: str | None


class ObservedNet(Record):
    net_id: str
    members: tuple[str, ...]
    connection_ids: tuple[Identifier, ...]


class MotifCheck(Record):
    rule_id: Identifier
    status: Literal["MATCHED", "REJECTED", "UNRESOLVED", "INDETERMINATE", "NOT_EVALUATED"]
    reason_code: Identifier
    affected_roles: tuple[Role, ...] = ()
    affected_net_ids: tuple[str, ...] = ()
    unexpected_members: tuple[str, ...] = ()
    missing_prerequisites: tuple[Identifier, ...] = ()


class DividerTopologyReport(Record):
    schema_version: Literal["1.0"] = "1.0"
    algorithm_version: Literal["divider-topology-e2-v1"] = ALGORITHM_VERSION
    restriction: Literal["TEST_ONLY_NOT_PRODUCTION"] = "TEST_ONLY_NOT_PRODUCTION"
    hardware_qualification: Literal["HARDWARE_COMPATIBILITY_NOT_PROVEN"] = "HARDWARE_COMPATIBILITY_NOT_PROVEN"
    motif_state: MotifState
    math_state: Literal["MATH_EXECUTED_CONDITIONALLY", "MATH_WITHHELD"]
    catalog_digest: Digest
    snapshot_digest: Digest
    binding_digest: Digest
    hypothesis_digest: Digest
    model_digest: Digest | None
    anchors: tuple[ObservedAnchor, ...]
    net_ids: MotifNetIds
    observed_nets: tuple[ObservedNet, ...]
    checks: tuple[MotifCheck, ...]
    model_values_are_assumptions: Literal[True] = True
    actual_component_value_not_admitted: Literal[True] = True
    model_report: VoltageModelReport | None


OBLIGATIONS = (
    MotifCheck(rule_id="ACTUAL_RESISTOR_VALUES", status="INDETERMINATE", reason_code="COMPONENT_VALUE_NOT_ADMITTED",
               missing_prerequisites=("actual_resistor_values_and_material",)),
    MotifCheck(rule_id="RECEIVER_LOADING", status="INDETERMINATE", reason_code="INPUT_LOADING_UNKNOWN",
               missing_prerequisites=("receiver_input_leakage_and_pull_configuration",)),
    MotifCheck(rule_id="SOURCE_DRIVE", status="NOT_EVALUATED", reason_code="SOURCE_DRIVE_OUT_OF_SCOPE",
               missing_prerequisites=("source_voltage_current_characteristic",)),
    MotifCheck(rule_id="POWER_OFF", status="NOT_EVALUATED", reason_code="POWER_OFF_OUT_OF_SCOPE",
               missing_prerequisites=("unpowered_pin_behavior",)),
    MotifCheck(rule_id="TRANSIENT", status="NOT_EVALUATED", reason_code="TRANSIENT_OUT_OF_SCOPE",
               missing_prerequisites=("capacitance_and_edge_timing",)),
)


def _vertex(ref: TerminalRef) -> str:
    return f"T:{ref.instance_id}/{ref.terminal_id}"


def _observations(topology, anchors: tuple[ObservedAnchor, ...]) -> tuple[ObservedNet, ...]:
    relevant = {row.net_id for row in anchors}
    connections = {}
    for wire_id, net_id in topology.connection_to_net:
        if net_id in relevant:
            connections.setdefault(net_id, []).append(wire_id)
    return tuple(ObservedNet(net_id=net.net_id, members=net.members,
                             connection_ids=tuple(connections.get(net.net_id, ())))
                 for net in topology.nets if net.net_id in relevant)


def _allowed_ground_members(catalog, receiver, ground: TerminalRef, definition) -> set[str]:
    # Ask CORE which contacts remain connected after removing all external conductors.
    isolated = create_snapshot(catalog, instances=(receiver,), junctions=(), conductors=())
    local = compute_nets(catalog, isolated)
    ground_net = dict(local.terminal_to_net)[_vertex(ground)]
    ground_vertices = {_vertex(TerminalRef(instance_id=receiver.instance_id, terminal_id=term.terminal_id))
                       for term in definition.terminals if term.electrical_role == "ground"}
    return set(next(net.members for net in local.nets if net.net_id == ground_net)) & ground_vertices


def bind_ideal_divider_to_snapshot(
    catalog: CatalogSnapshot,
    snapshot: CircuitSnapshot,
    binding: DividerTopologyBinding,
    hypothesis: IdealDividerHypothesis,
) -> DividerTopologyReport:
    """Verify an exact virtual motif before exposing an unchanged E1 report."""
    binding = DividerTopologyBinding.model_validate(binding)
    hypothesis = IdealDividerHypothesis.model_validate(hypothesis)
    topology = compute_nets(catalog, snapshot)
    current = SnapshotAssociation(catalog_digest=catalog.catalog_digest, snapshot_digest=topology.snapshot_sha256)
    instances = {row.instance_id: row for row in snapshot.instances}
    definitions = {row.definition_id: row for row in catalog.definitions}
    locations = dict(topology.terminal_to_net)
    anchors = []
    terminals = {}
    for role in ROLES:
        anchor = getattr(binding, role)
        ref = anchor.ref
        instance = instances.get(ref.instance_id)
        observed_digest = instance.definition_digest if instance is not None else None
        net_id = locations.get(_vertex(ref))
        matched = observed_digest == anchor.definition_digest and net_id is not None
        anchors.append(ObservedAnchor(role=role, anchor=anchor, observed_definition_digest=observed_digest,
                                      net_id=net_id, status="MATCHED" if matched else "REJECTED"))
        if matched:
            definition = definitions[instance.definition_id]
            terminals[role] = next(item for item in definition.terminals if item.terminal_id == ref.terminal_id)
    anchors = tuple(anchors)
    by_role = {row.role: row for row in anchors}
    observed = _observations(topology, anchors)
    members = {net.net_id: set(net.members) for net in observed}
    ids = MotifNetIds(source=by_role["source_out"].net_id, midpoint=by_role["r_top_lo"].net_id,
                      ground=by_role["reference_ground"].net_id)
    checks = []

    def check(rule, status, reason, roles=(), unexpected=(), missing=()):
        affected = {by_role[role].net_id for role in roles if by_role[role].net_id is not None}
        checks.append(MotifCheck(rule_id=rule, status=status, reason_code=reason, affected_roles=roles,
                                 affected_net_ids=tuple(sorted(affected)), unexpected_members=tuple(sorted(unexpected)),
                                 missing_prerequisites=missing))

    def report(state: MotifState, model: VoltageModelReport | None = None) -> DividerTopologyReport:
        preimage = hypothesis.model_dump(mode="json")
        preimage["assumptions"].sort(key=lambda item: item["record_id"])
        return DividerTopologyReport(
            motif_state=state, math_state="MATH_WITHHELD" if model is None else "MATH_EXECUTED_CONDITIONALLY",
            catalog_digest=current.catalog_digest, snapshot_digest=current.snapshot_digest,
            binding_digest=digest_bytes(canonical_json(binding.model_dump(mode="json"))),
            hypothesis_digest=digest_bytes(canonical_json(preimage)),
            model_digest=None if model is None else model.calculation_digest, anchors=anchors, net_ids=ids,
            observed_nets=observed, checks=(*checks, *OBLIGATIONS), model_report=model,
        )

    if (binding.catalog_digest, binding.snapshot_digest) != (current.catalog_digest, current.snapshot_digest):
        check("BINDING_IDENTITY", "REJECTED", "STALE_TOPOLOGY_BINDING", ROLES)
        return report("MOTIF_NOT_ADMITTED")
    check("BINDING_IDENTITY", "MATCHED", "CURRENT_CORE_DIGESTS")
    invalid = tuple(row.role for row in anchors if row.status == "REJECTED")
    if invalid:
        for role in invalid:
            row = by_role[role]
            reason = ("INSTANCE_NOT_IN_SNAPSHOT" if row.observed_definition_digest is None else
                      "DEFINITION_DIGEST_MISMATCH" if row.observed_definition_digest != row.anchor.definition_digest else
                      "TERMINAL_NOT_IN_SNAPSHOT")
            check("ROLE_IDENTITIES", "REJECTED", reason, (role,))
        return report("MOTIF_NOT_ADMITTED")

    refs = {role: row.anchor.ref for role, row in by_role.items()}
    receiver = instances[refs["receiver_input"].instance_id]
    receiver_definition = definitions[receiver.definition_id]
    ground = terminals["reference_ground"]
    ground_mapping = ground.signal_ref
    if (refs["reference_ground"].instance_id != receiver.instance_id or ground.electrical_role != "ground"
            or (not receiver_definition.identity.synthetic_test_data and (
                catalog.catalog_schema_version != "1.1" or ground_mapping is None
                or ground_mapping.mapping_status != "verified" or ground_mapping.target_kind != "power_domain"))):
        check("ROLE_IDENTITIES", "REJECTED", "INVALID_REFERENCE_GROUND", ("reference_ground", "receiver_input"))
        return report("MOTIF_NOT_ADMITTED")
    for role, allowed in (("source_out", {"output", "io"}), ("receiver_input", {"input", "io"})):
        term = terminals[role]
        if term.electrical_role not in allowed or (term.signal_ref is not None and term.signal_ref.target_kind == "power_domain"):
            check("ROLE_IDENTITIES", "REJECTED", "SIGNAL_ROLE_INVALID", (role,))
            return report("MOTIF_NOT_ADMITTED")
    top = ("r_top_hi", "r_top_lo")
    bottom = ("r_bottom_hi", "r_bottom_lo")
    top_id, bottom_id = refs[top[0]].instance_id, refs[bottom[0]].instance_id
    if top_id == bottom_id:
        check("RESISTOR_BODIES", "REJECTED", "RESISTOR_INSTANCES_NOT_DISTINCT", (*top, *bottom))
        return report("MOTIF_NOT_ADMITTED")
    if len(set(refs.values())) != len(ROLES) or refs["source_out"].instance_id == receiver.instance_id:
        check("ROLE_IDENTITIES", "REJECTED", "ROLE_ANCHORS_NOT_DISTINCT", ROLES)
        return report("MOTIF_NOT_ADMITTED")
    check("ROLE_IDENTITIES", "MATCHED", "EXACT_ROLE_ANCHORS")
    for pair in (top, bottom):
        hi, lo = (refs[role] for role in pair)
        definition = definitions[instances[hi.instance_id].definition_id]
        if (hi.instance_id != lo.instance_id or definition.device_class != RESISTOR_CLASS
                or not definition.identity.synthetic_test_data or len(definition.terminals) != 2
                or definition.internal_ideal_ties
                or any(term.electrical_role != "other" or term.signal_ref is not None for term in definition.terminals)):
            check("RESISTOR_BODIES", "REJECTED", "NOT_AN_ADMITTED_TWO_TERMINAL_RESISTOR_BODY", pair)
            return report("MOTIF_NOT_ADMITTED")
        if by_role[pair[0]].net_id == by_role[pair[1]].net_id:
            check("RESISTOR_BODIES", "REJECTED", "RESISTOR_TERMINALS_SHORTED", pair)
            return report("MOTIF_NOT_ADMITTED")
    check("RESISTOR_BODIES", "MATCHED", "SEPARATE_TEST_RESISTOR_BODIES", (*top, *bottom))

    groups = (
        ("SOURCE", ids.source, ("source_out", "r_top_hi")),
        ("MID", ids.midpoint, ("r_top_lo", "r_bottom_hi", "receiver_input")),
        ("GROUND", ids.ground, ("reference_ground", "r_bottom_lo")),
    )
    if len({ids.source, ids.midpoint, ids.ground}) != 3:
        check("VIRTUAL_NET_PARTITION", "REJECTED", "MOTIF_NETS_MERGED", ROLES)
        return report("MOTIF_NOT_ADMITTED")
    for label, net_id, roles in groups:
        if any(by_role[role].net_id != net_id for role in roles):
            check("VIRTUAL_NET_PARTITION", "REJECTED", f"{label}_NET_OPEN_OR_MISROUTED", roles)
            return report("MOTIF_NOT_ADMITTED")
    check("VIRTUAL_NET_PARTITION", "MATCHED", "THREE_DISTINCT_CORE_NETS", ROLES)

    for label, net_id, roles in groups:
        allowed = {_vertex(refs[role]) for role in roles}
        if label == "GROUND":
            allowed |= _allowed_ground_members(catalog, receiver, refs["reference_ground"], receiver_definition)
        extra = members[net_id] - allowed
        if extra:
            check("UNLOADED_NET_SCOPE", "UNRESOLVED", f"UNREVIEWED_{label}_NET_MEMBERS", roles, extra,
                  ("evidence_for_additional_net_branches",))
    if checks[-1].status == "UNRESOLVED":
        return report("MODEL_SCOPE_UNRESOLVED")
    check("UNLOADED_NET_SCOPE", "MATCHED", "EXACT_MOTIF_TERMINALS_AND_ADMITTED_GROUND_TIES", ROLES)

    if hypothesis.association != current:
        reason = "MODEL_ASSOCIATION_MISSING" if hypothesis.association is None else "STALE_MODEL_ASSOCIATION"
        check("E1_MODEL_BINDING", "UNRESOLVED", reason, missing=("current_core_model_association",))
        return report("MODEL_SCOPE_UNRESOLVED")
    if hypothesis.parameter_relationship != "INDEPENDENT":
        check("E1_MODEL_BINDING", "UNRESOLVED", "JOINT_ENVELOPE_REQUIRED", missing=("admitted_joint_envelope",))
        return report("MODEL_SCOPE_UNRESOLVED")
    check("E1_MODEL_BINDING", "MATCHED", "CURRENT_SNAPSHOT_AND_EXPLICIT_E1_ASSUMPTIONS")
    return report("CANONICAL_MOTIF_MATCHED", evaluate_ideal_divider(hypothesis))
