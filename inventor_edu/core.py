"""Canonical persistence, catalog admission, and full snapshot connectivity."""

import hashlib
import json
from collections import deque, defaultdict
from operator import attrgetter

from pydantic import ValidationError

from .models import (
    CatalogSnapshot, CircuitSnapshot, ComponentInstance, Conductor, DeviceDefinition,
    EditingDiagnostic, EngineeringModelError, Junction, Net, Record, ResolvedTerminal,
    SignalMappingEvidence, TerminalRef, TopologyResult, VertexRef,
)

MAX_JSON_BYTES = 4 * 1024 * 1024
LIMITS = {"instances": 128, "terminals": 8192, "conductors": 16384, "junctions": 8192}


def _canonical(data: object) -> bytes:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def _digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def _reject_number(value):
    raise ValueError(f"Non-integer JSON number: {value}")


def _validate(model: type[Record], value, code: str, *, json_input: bool = False):
    try:
        if json_input:
            return model.model_validate_json(value)
        return model.model_validate(value)
    except ValidationError as error:
        details = error.errors(include_input=False)[0]
        path = details["loc"]
        if path[-1:] in {
            ("schema_version",), ("catalog_schema_version",), ("definition_schema_version",),
            ("topology_schema_version",),
        } and details["type"] == "literal_error":
            code = "SCHEMA_UNSUPPORTED"
        elif len(path) >= 3 and path[0] == "conductors" and path[2] in {"endpoint_a", "endpoint_b"}:
            code = "INVALID_ENDPOINT"
        raise EngineeringModelError(code, path) from error


def _decode(model: type[Record], payload: bytes, code: str):
    if type(payload) is not bytes:
        raise EngineeringModelError("MALFORMED_JSON")
    if len(payload) > MAX_JSON_BYTES:
        raise EngineeringModelError("RESOURCE_LIMIT_EXCEEDED", ("json_bytes",))
    try:
        decoded = json.loads(payload.decode("utf-8"), object_pairs_hook=_unique_object,
                             parse_float=_reject_number, parse_constant=_reject_number)
        # Reject escaped lone surrogates, which have no UTF-8 canonical representation.
        _canonical(decoded)
    except (ValueError, RecursionError) as error:
        raise EngineeringModelError("MALFORMED_JSON") from error
    if model is CircuitSnapshot and isinstance(decoded, dict):
        for field in ("instances", "junctions", "conductors"):
            records = decoded.get(field)
            if isinstance(records, list):
                _bound(field, len(records))
    return _validate(model, payload, code, json_input=True)


def _index(records, key: str, field: str):
    result = {}
    for record in records:
        identity = getattr(record, key)
        if identity in result:
            raise EngineeringModelError("DUPLICATE_ID", (field,), (identity,))
        result[identity] = record
    return result


def _sorted(records, key: str):
    return tuple(sorted(records, key=attrgetter(key)))


def _definition_payload(definition: DeviceDefinition) -> dict:
    item = definition.model_dump(mode="json")
    item.pop("definition_digest")
    item["terminals"].sort(key=lambda record: record["terminal_id"])
    for terminal in item["terminals"]:
        terminal["capability_claim_ids"].sort()
    item["evidence_claim_ids"].sort()
    for tie in item["internal_ideal_ties"]:
        tie["terminal_ids"].sort()
    item["internal_ideal_ties"].sort(key=lambda tie: (tie["terminal_ids"], tie["evidence_claim_id"]))
    return item


def _catalog_payload(catalog: CatalogSnapshot) -> dict:
    claims = []
    for claim in _sorted(catalog.claims, "claim_id"):
        item = claim.model_dump(mode="json")
        item["conflict_claim_ids"].sort()
        if isinstance(claim.value, tuple):
            item["value"].sort()
        claims.append(item)
    return {
        "catalog_schema_version": catalog.catalog_schema_version,
        "definitions": [
            {**_definition_payload(item), "definition_digest": item.definition_digest}
            for item in _sorted(catalog.definitions, "definition_id")
        ],
        "source_documents": [
            item.model_dump(mode="json") for item in _sorted(catalog.source_documents, "source_document_id")
        ],
        "claims": claims,
    }


def _typed_mapping_matches(mapping, claim, terminal_id, identity, source) -> bool:
    value = claim.value
    if not isinstance(value, SignalMappingEvidence) or (
        value.terminal_id, value.target_kind, value.target_id
    ) != (terminal_id, mapping.target_kind, mapping.target_id):
        return False
    if identity.synthetic_test_data:
        return False
    if claim.source_class == "manufacturer":
        return identity.manufacturer_status == "verified" and source.publisher == identity.manufacturer_name
    # Retail evidence establishes an external signal for a retail profile, not a SoC or rail mapping.
    return (claim.source_class == "retailer" and value.target_kind == "signal"
            and source.publisher == identity.brand_or_distributor)


def _admit_catalog(catalog: CatalogSnapshot):
    definitions = _index(catalog.definitions, "definition_id", "definitions")
    sources = _index(catalog.source_documents, "source_document_id", "source_documents")
    claims = _index(catalog.claims, "claim_id", "claims")
    conflicted = set()
    disputed_ties = set()
    disputed_mappings = set()
    approved_mapping_targets = {}
    legacy = catalog.catalog_schema_version == "1.0"
    for claim in claims.values():
        typed = isinstance(claim.value, SignalMappingEvidence)
        if (claim.subject_definition_id not in definitions
                or (claim.source_document_id is not None and claim.source_document_id not in sources)
                or not set(claim.conflict_claim_ids) <= claims.keys()
                or (typed and (legacy or claim.claim_type != "signal_mapping"))):
            raise EngineeringModelError("INVALID_CATALOG", ("claims",), (claim.claim_id,))
        conflicted.update(claim.conflict_claim_ids)
        if claim.review_status == "conflicting" or claim.conflict_claim_ids:
            conflicted.add(claim.claim_id)
            if claim.claim_type == "internal_ideal_tie" and isinstance(claim.value, tuple):
                disputed_ties.add((claim.subject_definition_id, claim.scope, frozenset(claim.value)))
        if typed and claim.review_status == "approved":
            key = (claim.subject_definition_id, claim.scope, claim.value.terminal_id)
            target = (claim.value.target_kind, claim.value.target_id)
            if approved_mapping_targets.setdefault(key, target) != target:
                disputed_mappings.add(key)
    for claim_id in conflicted:
        claim = claims[claim_id]
        if isinstance(claim.value, SignalMappingEvidence):
            disputed_mappings.add((claim.subject_definition_id, claim.scope, claim.value.terminal_id))

    terminals_by_definition = {}
    for definition_id, definition in definitions.items():
        path = ("definitions", definition_id)
        if definition.definition_digest != _digest(_canonical(_definition_payload(definition))):
            raise EngineeringModelError("CATALOG_DIGEST_MISMATCH", (*path, "definition_digest"))
        terminals = _index(definition.terminals, "terminal_id", "terminals")
        terminals_by_definition[definition_id] = terminals
        if (definition.identity.manufacturer_status == "verified") != bool(definition.identity.manufacturer_name):
            raise EngineeringModelError("INVALID_CATALOG", (*path, "identity", "manufacturer_name"))

        def scoped_claim(claim_id):
            claim = claims.get(claim_id)
            if (claim is not None and claim.subject_definition_id == definition_id
                    and claim.scope == definition.identity.profile_scope):
                return claim
            return None

        if any(scoped_claim(key) is None for key in definition.evidence_claim_ids):
            raise EngineeringModelError("INVALID_CATALOG", (*path, "evidence_claim_ids"))
        contacts = set()
        for terminal in terminals.values():
            if terminal.connector_id is not None and terminal.contact_position is not None:
                contact = (terminal.connector_id, terminal.contact_position)
                if contact in contacts:
                    raise EngineeringModelError("AMBIGUOUS_MAPPING", (*path, "terminals"), contact)
                contacts.add(contact)
            if any(scoped_claim(key) is None for key in terminal.capability_claim_ids):
                raise EngineeringModelError("INVALID_CATALOG", (*path, "terminals", terminal.terminal_id))
            mapping = terminal.signal_ref
            if mapping is not None:
                claim = scoped_claim(mapping.source_claim_id)
                mapping_path = (*path, "terminals", terminal.terminal_id)
                if (mapping.terminal_id != terminal.terminal_id
                        or (mapping.source_claim_id is not None and claim is None)):
                    raise EngineeringModelError("AMBIGUOUS_MAPPING", mapping_path)
                if mapping.mapping_status != "verified":
                    continue
                if (mapping.target_kind == "unknown" or mapping.target_id is None or claim is None
                        or claim.review_status != "approved" or claim.claim_id in conflicted
                        or claim.claim_type != "signal_mapping" or not claim.source_document_id or not claim.locator):
                    raise EngineeringModelError("AMBIGUOUS_MAPPING", mapping_path)
                if legacy:
                    matches = claim.value == mapping.target_id and claim.condition == terminal.terminal_id
                else:
                    scope_key = (definition_id, claim.scope, terminal.terminal_id)
                    matches = scope_key not in disputed_mappings and _typed_mapping_matches(
                        mapping, claim, terminal.terminal_id, definition.identity, sources[claim.source_document_id]
                    )
                if not matches:
                    raise EngineeringModelError("AMBIGUOUS_MAPPING", mapping_path)
        for tie in definition.internal_ideal_ties:
            members = set(tie.terminal_ids)
            claim = scoped_claim(tie.evidence_claim_id)
            source_class = "synthetic" if definition.identity.synthetic_test_data else "manufacturer"
            if (len(members) < 2 or len(members) != len(tie.terminal_ids)
                    or not members <= terminals.keys() or claim is None
                    or claim.claim_type != "internal_ideal_tie" or claim.review_status != "approved"
                    or claim.claim_id in conflicted or claim.source_class != source_class
                    or (definition_id, claim.scope, frozenset(members)) in disputed_ties
                    or not isinstance(claim.value, tuple) or sorted(claim.value) != sorted(tie.terminal_ids)
                    or (source_class == "manufacturer" and (
                        not claim.source_document_id or not claim.locator
                        or definition.identity.manufacturer_status != "verified"
                        or sources[claim.source_document_id].publisher != definition.identity.manufacturer_name
                    ))):
                raise EngineeringModelError("INVALID_IDEAL_TIE", (*path, "internal_ideal_ties"),
                                            (tie.evidence_claim_id,))
    if catalog.catalog_digest != _digest(_canonical(_catalog_payload(catalog))):
        raise EngineeringModelError("CATALOG_DIGEST_MISMATCH", ("catalog_digest",))
    return definitions, terminals_by_definition


def load_catalog(payload: bytes, *, expected_sha256: str | None = None) -> CatalogSnapshot:
    """Validate internal consistency and optionally compare an externally supplied catalog pin."""
    catalog = _decode(CatalogSnapshot, payload, "INVALID_CATALOG")
    _admit_catalog(catalog)
    if expected_sha256 is not None and expected_sha256 != catalog.catalog_digest:
        raise EngineeringModelError("CATALOG_DIGEST_MISMATCH", ("catalog_digest",))
    return CatalogSnapshot.model_validate_json(
        _canonical({**_catalog_payload(catalog), "catalog_digest": catalog.catalog_digest})
    )


def _vertex(ref: VertexRef) -> str:
    if isinstance(ref, TerminalRef):
        return f"T:{ref.instance_id}/{ref.terminal_id}"
    return f"J:{ref.junction_id}"


def _bound(field: str, size: int):
    if size > LIMITS[field]:
        raise EngineeringModelError("RESOURCE_LIMIT_EXCEEDED", (field,))


def _resolve(instances, terminals, ref: TerminalRef, path=()):
    instance = instances.get(ref.instance_id)
    if instance is None:
        raise EngineeringModelError("UNKNOWN_INSTANCE", path, (ref.instance_id,))
    terminal = terminals[instance.definition_id].get(ref.terminal_id)
    if terminal is None:
        raise EngineeringModelError("UNKNOWN_TERMINAL", path, (ref.instance_id, ref.terminal_id))
    return instance, terminal


def _bind(catalog: CatalogSnapshot, snapshot: CircuitSnapshot):
    catalog = _validate(CatalogSnapshot, catalog, "INVALID_CATALOG")
    definitions, terminals = _admit_catalog(catalog)
    if snapshot.catalog_digest != catalog.catalog_digest:
        raise EngineeringModelError("CATALOG_MISMATCH", ("catalog_digest",))
    for field in ("instances", "junctions", "conductors"):
        _bound(field, len(getattr(snapshot, field)))
    instances = _index(snapshot.instances, "instance_id", "instances")
    junctions = _index(snapshot.junctions, "junction_id", "junctions")
    _index(snapshot.conductors, "connection_id", "conductors")
    count = 0
    for instance in instances.values():
        definition = definitions.get(instance.definition_id)
        if definition is None:
            raise EngineeringModelError("UNKNOWN_DEFINITION", ("instances",), (instance.definition_id,))
        if definition.definition_digest != instance.definition_digest:
            raise EngineeringModelError("CATALOG_DIGEST_MISMATCH", ("instances", "definition_digest"),
                                        (instance.instance_id, instance.definition_id))
        count += len(terminals[instance.definition_id])
    _bound("terminals", count)
    for wire in snapshot.conductors:
        path = ("conductors", wire.connection_id)
        for field in ("endpoint_a", "endpoint_b"):
            endpoint = getattr(wire, field)
            if isinstance(endpoint, TerminalRef):
                _resolve(instances, terminals, endpoint, (*path, field))
            elif endpoint.junction_id not in junctions:
                raise EngineeringModelError("INVALID_ENDPOINT", (*path, field), (endpoint.junction_id,))
        if _vertex(wire.endpoint_a) == _vertex(wire.endpoint_b):
            raise EngineeringModelError("SELF_LOOP", path)
    return definitions, instances, terminals


def _normalize(snapshot: CircuitSnapshot) -> CircuitSnapshot:
    conductors = []
    for wire in _sorted(snapshot.conductors, "connection_id"):
        a, b = sorted((wire.endpoint_a, wire.endpoint_b), key=_vertex)
        conductors.append(wire.model_copy(update={"endpoint_a": a, "endpoint_b": b}))
    return snapshot.model_copy(update={
        "instances": _sorted(snapshot.instances, "instance_id"),
        "junctions": _sorted(snapshot.junctions, "junction_id"),
        "conductors": tuple(conductors),
    })


def create_snapshot(catalog: CatalogSnapshot, *, instances: tuple[ComponentInstance, ...],
                    junctions: tuple[Junction, ...], conductors: tuple[Conductor, ...]) -> CircuitSnapshot:
    catalog = _validate(CatalogSnapshot, catalog, "INVALID_CATALOG")
    for field, records in (("instances", instances), ("junctions", junctions), ("conductors", conductors)):
        if isinstance(records, tuple):
            _bound(field, len(records))
    snapshot = _validate(CircuitSnapshot, dict(schema_version="1.0", catalog_digest=catalog.catalog_digest,
                         instances=instances, junctions=junctions, conductors=conductors), "INVALID_SNAPSHOT")
    _bind(catalog, snapshot)
    return _normalize(snapshot)


def resolve_terminal(catalog: CatalogSnapshot, snapshot: CircuitSnapshot, ref: TerminalRef) -> ResolvedTerminal:
    """Resolve a contact. Legacy mapping declarations are returned as unverified hints."""
    snapshot = _validate(CircuitSnapshot, snapshot, "INVALID_SNAPSHOT")
    definitions, instances, terminals = _bind(catalog, snapshot)
    ref = _validate(TerminalRef, ref, "INVALID_ENDPOINT")
    instance, terminal = _resolve(instances, terminals, ref)
    evidence = set(definitions[instance.definition_id].evidence_claim_ids) | set(terminal.capability_claim_ids)
    mapping = terminal.signal_ref
    if mapping is not None:
        if mapping.source_claim_id is not None:
            evidence.add(mapping.source_claim_id)
        if catalog.catalog_schema_version == "1.0" and mapping.mapping_status == "verified":
            # Preserve the catalog's historical declaration and digest; downgrade only the resolved view.
            terminal = terminal.model_copy(update={"signal_ref": mapping.model_copy(update={"mapping_status": "unknown"})})
    return ResolvedTerminal(ref=ref, definition_id=instance.definition_id, terminal=terminal,
                            evidence_claim_ids=tuple(sorted(evidence)))


def _encode(data: dict) -> bytes:
    try:
        return _canonical(data)
    except (ValueError, TypeError) as error:
        raise EngineeringModelError("SERIALIZATION_ERROR") from error


def serialize_snapshot(snapshot: CircuitSnapshot) -> bytes:
    snapshot = _validate(CircuitSnapshot, snapshot, "SERIALIZATION_ERROR")
    for field in ("instances", "junctions", "conductors"):
        _bound(field, len(getattr(snapshot, field)))
    payload = _encode(_normalize(snapshot).model_dump(mode="json"))
    if len(payload) > MAX_JSON_BYTES:
        raise EngineeringModelError("RESOURCE_LIMIT_EXCEEDED", ("json_bytes",))
    return payload


def restore_snapshot(payload: bytes, catalog: CatalogSnapshot) -> CircuitSnapshot:
    snapshot = _decode(CircuitSnapshot, payload, "INVALID_SNAPSHOT")
    _bind(catalog, snapshot)
    return _normalize(snapshot)


def compute_nets(catalog: CatalogSnapshot, snapshot: CircuitSnapshot) -> TopologyResult:
    snapshot = _validate(CircuitSnapshot, snapshot, "INVALID_SNAPSHOT")
    definitions, instances, terminals = _bind(catalog, snapshot)
    adjacency = {f"J:{junction.junction_id}": set() for junction in snapshot.junctions}
    for instance_id, instance in instances.items():
        adjacency.update({f"T:{instance_id}/{key}": set() for key in terminals[instance.definition_id]})

    def add_edge(a, b):
        adjacency[a].add(b)
        adjacency[b].add(a)

    wires_at_vertex = defaultdict(list)
    for wire in snapshot.conductors:
        a, b = _vertex(wire.endpoint_a), _vertex(wire.endpoint_b)
        add_edge(a, b)
        wires_at_vertex[a].append(wire.connection_id)
    for instance_id, instance in instances.items():
        for tie in definitions[instance.definition_id].internal_ideal_ties:
            root, *others = sorted(tie.terminal_ids)
            for other in others:
                add_edge(f"T:{instance_id}/{root}", f"T:{instance_id}/{other}")

    visited = set()
    nets, isolated, diagnostics = [], [], []
    terminal_to_net, connection_to_net = {}, {}
    for start in sorted(adjacency):
        if start in visited:
            continue
        component = []
        queue = deque([start])
        visited.add(start)
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for neighbor in sorted(adjacency[vertex]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        members = tuple(sorted(key for key in component if key.startswith("T:")))
        connections = tuple(sorted(key for vertex in component for key in wires_at_vertex.get(vertex, ())))
        net_id = None
        if members:
            preimage = ("INVENTOR-EDU-NET-V1\n" + "\n".join(members)).encode("utf-8")
            net_id = "net:" + _digest(preimage)
            nets.append(Net(net_id=net_id, members=members))
            terminal_to_net.update(dict.fromkeys(members, net_id))
            if len(members) == 1:
                isolated.append(members[0])
        else:
            diagnostics.append(EditingDiagnostic(
                junction_ids=tuple(sorted(key[2:] for key in component)), conductor_ids=connections
            ))
        connection_to_net.update(dict.fromkeys(connections, net_id))
    return TopologyResult(
        snapshot_sha256=_digest(serialize_snapshot(snapshot)),
        nets=tuple(sorted(nets, key=lambda net: net.members[0])),
        terminal_to_net=tuple(sorted(terminal_to_net.items())),
        connection_to_net=tuple(sorted(connection_to_net.items())),
        isolated_terminals=tuple(sorted(isolated)),
        diagnostics=tuple(sorted(diagnostics, key=lambda item: item.junction_ids)),
    )


def serialize_topology(result: TopologyResult) -> bytes:
    result = _validate(TopologyResult, result, "SERIALIZATION_ERROR")
    data = result.model_dump(mode="json")
    data["terminal_to_net"] = dict(result.terminal_to_net)
    data["connection_to_net"] = dict(result.connection_to_net)
    data["nets"].sort(key=lambda net: min(net["members"], default=""))
    for net in data["nets"]:
        net["members"].sort()
    data["isolated_terminals"].sort()
    for diagnostic in data["diagnostics"]:
        diagnostic["junction_ids"].sort()
        diagnostic["conductor_ids"].sort()
    data["diagnostics"].sort(key=lambda item: (item["junction_ids"], item["conductor_ids"]))
    return _encode(data)
