"""Deterministic, test-only synthesis of a two-role GPIO connection pattern."""

from typing import Annotated, Literal

from pydantic import Field

from .core import LIMITS, compute_nets, create_snapshot, resolve_terminal
from .gpio_facts import GpioFactSet, HardwareScope, canonical_json, digest_bytes, validate_factset
from .gpio_verify import GpioRequirement, GpioVerificationReport, verify_gpio_requirements
from .models import (
    CatalogSnapshot, CircuitSnapshot, ComponentInstance, Conductor, Digest, Identifier, Record,
    TerminalRef, TopologyResult,
)

Role = Literal["TRIG_OUTPUT", "ECHO_INPUT"]
Function = Literal["GPIO_OUT", "GPIO_IN"]
EvidenceScope = Literal["TEST_ONLY_SOURCE_REVIEWED", "TEST_ONLY_SYNTHETIC"]
Classification = Literal[
    "REJECTED_KNOWN_HARD_FAIL", "SCOPED_CHECKS_PASSED_WITH_OBLIGATIONS",
    "INCOMPLETE_WITH_EXPLICIT_OBLIGATIONS",
]
Termination = Literal["EXHAUSTED_REVIEWED_DOMAIN", "SEARCH_INCOMPLETE", "NO_REVIEWED_DOMAIN"]
GENERATOR = "finite-domain-v1"
PATTERN = "two-signal-gpio-v1"
ROLE_FUNCTIONS = {"TRIG_OUTPUT": "GPIO_OUT", "ECHO_INPUT": "GPIO_IN"}
HARD_CHECKS = ("PIN_MAPPING", "PHYSICAL_CAPABILITY", "BOARD_AVAILABILITY")
CHECKS = (*HARD_CHECKS, "ACTIVE_CONFIGURATION", "ELECTRICAL_COMPATIBILITY")
PATTERN_OBLIGATIONS = ("POWER", "LED", "CURRENT_LIMITING_RESISTORS", "VOLTAGE_ADAPTATION", "FIRMWARE")


class SynthesisInputError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class SignalRole(Record):
    role: Role
    requirement_id: Identifier
    source_terminal: TerminalRef
    function: Function
    domain: Annotated[tuple[TerminalRef, ...], Field(max_length=LIMITS["terminals"])]


class SynthesisRequest(Record):
    schema_version: Literal["1.0"] = "1.0"
    request_id: Identifier
    requirements_digest: Digest
    catalog_digest: Digest
    instances: tuple[ComponentInstance, ComponentInstance]
    roles: tuple[SignalRole, SignalRole]
    resource_constraint: Literal["AllDifferent"]
    evidence_scope: EvidenceScope
    max_nodes: Annotated[int, Field(gt=0)]
    max_candidates: Annotated[int, Field(gt=0)]


class RoleTrace(Record):
    role: Role
    requirement_id: Identifier
    requirements_digest: Digest
    assignment_id: Digest
    source_terminal: TerminalRef
    assigned_terminal: TerminalRef
    net_id: str
    finding_ids: tuple[Digest, ...]
    coverage_ids: tuple[Digest, ...]
    reason_codes: tuple[Identifier, ...]
    evidence_claim_ids: tuple[Identifier, ...]
    unresolved_rule_ids: tuple[Identifier, ...]
    missing_prerequisites: tuple[Identifier, ...]
    catalog_digest: Digest
    snapshot_digest: Digest
    factset_digest: Digest
    hardware_scope: HardwareScope
    evidence_scope: EvidenceScope
    operating_state: Literal["ACTIVE"] = "ACTIVE"
    restriction: Literal["TEST_ONLY_NOT_PRODUCTION"] = "TEST_ONLY_NOT_PRODUCTION"
    generator_version: Literal["finite-domain-v1"] = GENERATOR
    pattern_version: Literal["two-signal-gpio-v1"] = PATTERN


class SynthesisCandidate(Record):
    assignment_id: Digest
    classification: Classification
    snapshot: CircuitSnapshot
    topology: TopologyResult
    gpio_report: GpioVerificationReport
    traces: tuple[RoleTrace, ...]
    unresolved_obligations: tuple[Identifier, ...] = PATTERN_OBLIGATIONS


class SynthesisResult(Record):
    schema_version: Literal["1.0"] = "1.0"
    request_id: Identifier
    requirements_digest: Digest
    restriction: Literal["TEST_ONLY_NOT_PRODUCTION"] = "TEST_ONLY_NOT_PRODUCTION"
    termination: Termination
    nodes_visited: int
    uniqueness_prunes: int
    evaluated_candidates: int
    rejected_candidates: int
    verifier_calls: int
    candidates: tuple[SynthesisCandidate, ...]


def _terminal_key(ref: TerminalRef) -> tuple[str, str]:
    return ref.instance_id, ref.terminal_id


def _ordered_roles(
    request: SynthesisRequest, catalog: CatalogSnapshot, empty: CircuitSnapshot,
) -> tuple[SignalRole, ...]:
    if request.catalog_digest != empty.catalog_digest:
        raise SynthesisInputError("CATALOG_REFERENCE_MISMATCH")
    roles = tuple(sorted(request.roles, key=lambda role: role.role))
    if ({role.role for role in roles} != ROLE_FUNCTIONS.keys()
            or len({role.requirement_id for role in roles}) != len(roles)
            or any(role.function != ROLE_FUNCTIONS[role.role] for role in roles)):
        raise SynthesisInputError("INVALID_ROLE_REQUIREMENTS")
    sources = {_terminal_key(role.source_terminal) for role in roles}
    source_instances = {instance_id for instance_id, _ in sources}
    if len(sources) != len(roles) or len(source_instances) != 1:
        raise SynthesisInputError("INVALID_SOURCE_TERMINALS")
    for role in roles:
        resolve_terminal(catalog, empty, role.source_terminal)
        keys = {_terminal_key(ref) for ref in role.domain}
        if len(keys) != len(role.domain) or any(instance_id in source_instances for instance_id, _ in keys):
            raise SynthesisInputError("INVALID_PHYSICAL_DOMAIN")
        for ref in role.domain:
            resolve_terminal(catalog, empty, ref)
    return roles


def _classify(report: GpioVerificationReport, role_count: int) -> Classification:
    hard = [finding for finding in report.findings if finding.rule_id in HARD_CHECKS]
    if any(finding.status == "FAIL" for finding in hard):
        return "REJECTED_KNOWN_HARD_FAIL"
    if len(hard) == role_count * len(HARD_CHECKS) and all(f.status == "PASS" for f in hard):
        return "SCOPED_CHECKS_PASSED_WITH_OBLIGATIONS"
    return "INCOMPLETE_WITH_EXPLICIT_OBLIGATIONS"


def _trace(
    request: SynthesisRequest, role: SignalRole, target: TerminalRef, assignment_id: str,
    topology: TopologyResult, report: GpioVerificationReport, hardware_scope: HardwareScope, wire: Conductor,
) -> RoleTrace:
    findings = tuple(item for item in report.findings if item.requirement_id == role.requirement_id)
    coverage = tuple(item for item in report.coverage if item.requirement_id == role.requirement_id)
    unresolved = (*coverage, *(item for item in findings if item.status == "UNKNOWN"))
    return RoleTrace(
        role=role.role, requirement_id=role.requirement_id, requirements_digest=request.requirements_digest,
        assignment_id=assignment_id, source_terminal=role.source_terminal, assigned_terminal=target,
        net_id=dict(topology.connection_to_net)[wire.connection_id],
        finding_ids=tuple(item.finding_id for item in findings),
        coverage_ids=tuple(item.finding_id for item in coverage),
        reason_codes=tuple(sorted({item.reason_code for item in (*findings, *coverage)})),
        evidence_claim_ids=tuple(sorted({claim for item in (*findings, *coverage) for claim in item.evidence_claims})),
        unresolved_rule_ids=tuple(sorted({item.rule_id for item in unresolved})),
        missing_prerequisites=tuple(sorted({key for item in unresolved for key in item.missing_prerequisites})),
        catalog_digest=report.catalog_digest, snapshot_digest=topology.snapshot_sha256,
        factset_digest=report.factset_digest, hardware_scope=hardware_scope, evidence_scope=request.evidence_scope,
    )


def generate_candidates(
    request: SynthesisRequest, catalog: CatalogSnapshot, fact_set: GpioFactSet, *,
    trusted_catalog_sha256: str | None, trusted_factset_sha256: str | None,
) -> SynthesisResult:
    """Search the supplied fixture domains and retain up to max_candidates in traversal order."""
    request = SynthesisRequest.model_validate(request)
    empty = create_snapshot(catalog, instances=request.instances, junctions=(), conductors=())
    roles = _ordered_roles(request, catalog, empty)
    facts = validate_factset(fact_set)
    if facts.review != request.evidence_scope:
        raise SynthesisInputError("EVIDENCE_SCOPE_MISMATCH")

    def verify(snapshot: CircuitSnapshot, requirements: tuple[GpioRequirement, ...]) -> GpioVerificationReport:
        return verify_gpio_requirements(
            catalog, snapshot, facts, requirements, trusted_catalog_sha256, trusted_factset_sha256,
        )

    domains = tuple(tuple(sorted(role.domain, key=_terminal_key)) for role in roles)
    retained = []
    visited = pruned = evaluated = rejected = 0

    def evaluate(selected: tuple[TerminalRef, ...]) -> Classification:
        pairs = tuple(zip(roles, selected, strict=True))
        wires = tuple(Conductor(connection_id=f"syn-{role.role}", endpoint_a=role.source_terminal,
                                endpoint_b=target) for role, target in pairs)
        snapshot = create_snapshot(catalog, instances=request.instances, junctions=(), conductors=wires)
        topology = compute_nets(catalog, snapshot)
        requirements = tuple(GpioRequirement(requirement_id=role.requirement_id, terminal=target,
                            requested_function=role.function, checks=CHECKS, operating_state="ACTIVE")
                             for role, target in pairs)
        report = verify(snapshot, requirements)
        classification = _classify(report, len(roles))
        if len(retained) < request.max_candidates:
            assignment_id = digest_bytes(canonical_json({
                "generator": GENERATOR, "pattern": PATTERN, "request": request.request_id,
                "requirements": request.requirements_digest, "role_requirements": [
                    (role.role, role.requirement_id) for role in roles
                ], "snapshot": topology.snapshot_sha256, "factset": report.factset_digest,
            }))
            traces = tuple(_trace(request, role, target, assignment_id, topology, report, facts.scope, wire)
                           for (role, target), wire in zip(pairs, wires, strict=True))
            retained.append(SynthesisCandidate(assignment_id=assignment_id, classification=classification,
                            snapshot=snapshot, topology=topology, gpio_report=report, traces=traces))
        return classification

    def visit(selected: tuple[TerminalRef, ...]) -> bool:
        nonlocal visited, pruned, evaluated, rejected
        if len(selected) == len(roles):
            classification = evaluate(selected)
            evaluated += 1
            rejected += classification == "REJECTED_KNOWN_HARD_FAIL"
            return True
        for terminal in domains[len(selected)]:
            if visited == request.max_nodes:
                return False
            visited += 1
            if terminal in selected:
                pruned += 1
            elif not visit((*selected, terminal)):
                return False
        return True

    if not all(domains):
        termination = "NO_REVIEWED_DOMAIN"
    else:
        termination = "EXHAUSTED_REVIEWED_DOMAIN" if visit(()) else "SEARCH_INCOMPLETE"
    if evaluated == 0:
        # Preserve B's pin and catalog-binding error semantics even without complete assignments.
        verify(empty, ())
    return SynthesisResult(
        request_id=request.request_id, requirements_digest=request.requirements_digest, termination=termination,
        nodes_visited=visited, uniqueness_prunes=pruned, evaluated_candidates=evaluated,
        rejected_candidates=rejected, verifier_calls=max(1, evaluated), candidates=tuple(retained),
    )
