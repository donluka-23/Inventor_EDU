"""Immutable records for the version 1 connectivity profile."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Identifier = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")]
Digest = Annotated[str, StringConstraints(pattern=r"^sha256:[a-f0-9]{64}$")]
Nonempty = Annotated[str, StringConstraints(min_length=1, pattern=r"\S")]
Version = Literal["1.0"]
CatalogVersion = Literal["1.0", "1.1"]
KnownStatus = Literal["verified", "unverified", "not_applicable"]
MappingTargetKind = Literal["soc_gpio", "power_domain", "signal"]


class EngineeringModelError(ValueError):
    def __init__(self, code: str, path: tuple[str | int, ...] = (),
                 context_ids: tuple[str, ...] = ()):
        self.code = code
        self.path = path
        self.context_ids = context_ids
        super().__init__(f"{code} at {path!r}: {context_ids!r}")


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True, revalidate_instances="always")


class DeviceIdentity(Record):
    brand_or_distributor: Nonempty
    manufacturer_status: KnownStatus
    manufacturer_name: Nonempty | None = None
    orderable_part_or_sku: Nonempty
    hardware_family: Nonempty
    hardware_revision_status: KnownStatus
    hardware_revision: Nonempty | None = None
    assembled_module: Nonempty | None = None
    silicon_revision_status: KnownStatus
    profile_scope: Nonempty
    synthetic_test_data: bool = False


class SourceDocument(Record):
    source_document_id: Identifier
    url: Annotated[str, StringConstraints(pattern=r"^https?://[^\s]+$")]
    publisher: Nonempty
    title: Nonempty
    edition: Nonempty
    accessed_at_utc: Nonempty
    media_type: Nonempty
    publication_date: Nonempty | None = None
    download_sha256: Digest | None = None
    rights_state: Literal["verified_reusable", "link_only", "permission_required", "unverified"]


class SignalMappingEvidence(Record):
    terminal_id: Identifier
    target_kind: MappingTargetKind
    target_id: Identifier


class EvidenceClaim(Record):
    claim_id: Identifier
    claim_type: Identifier
    subject_definition_id: Identifier
    value: Nonempty | tuple[Identifier, ...] | SignalMappingEvidence | None
    unit: Nonempty | None = None
    source_class: Literal["manufacturer", "retailer", "user_assumption", "derived", "measurement", "synthetic"]
    source_document_id: Identifier | None = None
    locator: Nonempty | None = None
    condition: Nonempty | None = None
    scope: Nonempty
    qualification: Nonempty
    review_status: Literal["approved", "unverified", "conflicting", "missing"]
    conflict_claim_ids: tuple[Identifier, ...] = ()


class SignalMapping(Record):
    terminal_id: Identifier
    target_kind: MappingTargetKind | Literal["unknown"]
    target_id: Identifier | None = None
    source_claim_id: Identifier | None = None
    mapping_status: Literal["verified", "unknown"]


class TerminalDefinition(Record):
    terminal_id: Identifier
    contact_type: Identifier
    connector_id: Identifier | None = None
    contact_position: Identifier | None = None
    printed_label: str
    electrical_role: Literal["power", "ground", "io", "input", "output", "other", "unknown"]
    signal_ref: SignalMapping | None = None
    capability_claim_ids: tuple[Identifier, ...] = ()


class InternalIdealTie(Record):
    terminal_ids: tuple[Identifier, ...]
    evidence_claim_id: Identifier


class DeviceDefinition(Record):
    definition_schema_version: Version
    definition_id: Identifier
    definition_digest: Digest
    device_class: Identifier
    identity: DeviceIdentity
    terminals: Annotated[tuple[TerminalDefinition, ...], Field(min_length=1)]
    internal_ideal_ties: tuple[InternalIdealTie, ...] = ()
    evidence_claim_ids: tuple[Identifier, ...] = ()


class CatalogSnapshot(Record):
    catalog_schema_version: CatalogVersion
    definitions: tuple[DeviceDefinition, ...]
    source_documents: tuple[SourceDocument, ...]
    claims: tuple[EvidenceClaim, ...]
    catalog_digest: Digest


class ComponentInstance(Record):
    instance_id: Identifier
    definition_id: Identifier
    definition_digest: Digest
    user_label: str | None = None


class TerminalRef(Record):
    kind: Literal["terminal"] = "terminal"
    instance_id: Identifier
    terminal_id: Identifier


class JunctionRef(Record):
    kind: Literal["junction"] = "junction"
    junction_id: Identifier


class Junction(Record):
    junction_id: Identifier


VertexRef = Annotated[TerminalRef | JunctionRef, Field(discriminator="kind")]


class Conductor(Record):
    connection_id: Identifier
    kind: Literal["ideal_wire"] = "ideal_wire"
    endpoint_a: VertexRef
    endpoint_b: VertexRef


class CircuitSnapshot(Record):
    schema_version: Version
    catalog_digest: Digest
    instances: tuple[ComponentInstance, ...]
    junctions: tuple[Junction, ...]
    conductors: tuple[Conductor, ...]


class ResolvedTerminal(Record):
    ref: TerminalRef
    definition_id: Identifier
    terminal: TerminalDefinition
    evidence_claim_ids: tuple[Identifier, ...]


class Net(Record):
    net_id: str
    members: tuple[str, ...]


class EditingDiagnostic(Record):
    code: Literal["JUNCTION_ONLY_GROUP"] = "JUNCTION_ONLY_GROUP"
    junction_ids: tuple[Identifier, ...]
    conductor_ids: tuple[Identifier, ...]


class TopologyResult(Record):
    topology_schema_version: Version = "1.0"
    snapshot_sha256: Digest
    nets: tuple[Net, ...]
    terminal_to_net: tuple[tuple[str, str], ...]
    connection_to_net: tuple[tuple[Identifier, str | None], ...]
    isolated_terminals: tuple[str, ...]
    diagnostics: tuple[EditingDiagnostic, ...]
