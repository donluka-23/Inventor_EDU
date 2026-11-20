"""Discover test-scope physical GPIO domains using CORE-001A and CORE-001B."""

from collections import defaultdict
from typing import Literal

from .core import create_snapshot, resolve_terminal
from .gpio_facts import GpioFactSet, validate_factset
from .gpio_verify import GpioCoverage, GpioFinding, GpioRequirement, verify_gpio_requirements
from .models import CatalogSnapshot, ComponentInstance, Digest, Identifier, Record, SignalMapping, TerminalRef

Qualification = Literal[
    "FUNCTION_CONFIRMED_FOR_STATED_CHECK", "KNOWN_UNSUITABLE", "UNRESOLVED_EVIDENCE",
]
CHECKS = (
    "PIN_MAPPING", "PHYSICAL_CAPABILITY", "BOARD_AVAILABILITY",
    "ACTIVE_CONFIGURATION", "ELECTRICAL_COMPATIBILITY",
)


class DiscoveryInputError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class CapabilityQuery(Record):
    schema_version: Literal["1.0"] = "1.0"
    query_id: Identifier
    requirement_id: Identifier
    board_instance_id: Identifier
    definition_id: Identifier
    definition_digest: Digest
    requested_function: Literal["GPIO_OUT", "GPIO_IN"]
    operating_state: Literal["ACTIVE"]
    catalog_digest: Digest
    factset_digest: Digest
    evidence_scope: Literal["TEST_ONLY_SOURCE_REVIEWED", "TEST_ONLY_SYNTHETIC", "UNREVIEWED"]


class TerminalCandidate(Record):
    terminal: TerminalRef
    signal_mapping: SignalMapping | None
    findings: tuple[GpioFinding, ...]
    coverage: tuple[GpioCoverage, ...]
    evidence_claim_ids: tuple[Identifier, ...]
    limitations: tuple[Identifier, ...]
    qualification: Qualification


class CapabilityDiscoveryReport(Record):
    schema_version: Literal["1.0"] = "1.0"
    restriction: Literal["TEST_ONLY_NOT_PRODUCTION"] = "TEST_ONLY_NOT_PRODUCTION"
    query: CapabilityQuery
    snapshot_digest: Digest
    ruleset_version: Identifier
    candidates: tuple[TerminalCandidate, ...]

    @property
    def terminal_domain(self) -> tuple[TerminalRef, ...]:
        """Expose the explored contact domain, including negative and unresolved cases."""
        return tuple(candidate.terminal for candidate in self.candidates)


def _qualify(findings: tuple[GpioFinding, ...]) -> Qualification:
    if any(row.status == "FAIL" for row in findings):
        return "KNOWN_UNSUITABLE"
    passes = {row.rule_id for row in findings if row.status == "PASS"}
    if {"PIN_MAPPING", "PHYSICAL_CAPABILITY"} <= passes:
        return "FUNCTION_CONFIRMED_FOR_STATED_CHECK"
    return "UNRESOLVED_EVIDENCE"


def discover_gpio_terminals(
    query: CapabilityQuery, catalog: CatalogSnapshot, board: ComponentInstance, fact_set: GpioFactSet, *,
    trusted_catalog_sha256: str | None, trusted_factset_sha256: str | None,
) -> CapabilityDiscoveryReport:
    """Evaluate the exact board's GPIO candidates in a canonical board-only snapshot."""
    query = CapabilityQuery.model_validate(query)
    catalog = CatalogSnapshot.model_validate(catalog)
    board = ComponentInstance.model_validate(board)
    facts = validate_factset(fact_set)
    snapshot = create_snapshot(catalog, instances=(board,), junctions=(), conductors=())
    if (query.board_instance_id, query.definition_id, query.definition_digest) != (
        board.instance_id, board.definition_id, board.definition_digest,
    ):
        raise DiscoveryInputError("BOARD_REFERENCE_MISMATCH")
    if query.catalog_digest != snapshot.catalog_digest or query.factset_digest != facts.factset_digest:
        raise DiscoveryInputError("EVIDENCE_REFERENCE_MISMATCH")
    if query.evidence_scope != facts.review:
        raise DiscoveryInputError("EVIDENCE_SCOPE_MISMATCH")

    device = next(item for item in catalog.definitions if item.definition_id == board.definition_id)
    fact_contacts = {row.terminal_id for row in facts.mappings
                     if (facts.scope.definition_id, facts.scope.definition_digest)
                     == (board.definition_id, board.definition_digest)}
    refs = []
    for terminal in sorted(device.terminals, key=lambda item: item.terminal_id):
        mapping = terminal.signal_ref
        if (terminal.terminal_id in fact_contacts
                or (mapping is not None and mapping.target_kind in {"soc_gpio", "unknown"})
                or (mapping is None and terminal.electrical_role in {"io", "input", "output"})):
            refs.append(TerminalRef(instance_id=board.instance_id, terminal_id=terminal.terminal_id))

    # The originating requirement stays in the query. Physical contact IDs uniquely key the B batch.
    requests = tuple(GpioRequirement(
        requirement_id=ref.terminal_id, terminal=ref, requested_function=query.requested_function,
        operating_state=query.operating_state, checks=CHECKS,
    ) for ref in refs)
    report = verify_gpio_requirements(
        catalog, snapshot, facts, requests, trusted_catalog_sha256, trusted_factset_sha256,
    )
    findings_by_contact = defaultdict(list)
    coverage_by_contact = defaultdict(list)
    for finding in report.findings:
        findings_by_contact[finding.terminal].append(finding)
    for item in report.coverage:
        coverage_by_contact[item.terminal].append(item)

    candidates = []
    for ref in refs:
        findings = tuple(findings_by_contact[ref])
        coverage = tuple(coverage_by_contact[ref])
        limitations = {row.reason_code for row in findings if row.status != "PASS"}
        limitations.update(row.reason_code for row in coverage)
        candidates.append(TerminalCandidate(
            terminal=ref, signal_mapping=resolve_terminal(catalog, snapshot, ref).terminal.signal_ref,
            findings=findings, coverage=coverage, qualification=_qualify(findings),
            evidence_claim_ids=tuple(sorted({claim for row in (*findings, *coverage) for claim in row.evidence_claims})),
            limitations=tuple(sorted(limitations)),
        ))
    return CapabilityDiscoveryReport(
        query=query, snapshot_digest=report.snapshot_digest, ruleset_version=report.ruleset_version,
        candidates=tuple(candidates),
    )
