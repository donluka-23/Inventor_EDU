"""Finite GPIO checks over validated CORE-001A references and separately pinned facts."""

from typing import Literal

from pydantic import TypeAdapter, ValidationError

from .core import compute_nets, resolve_terminal
from .gpio_facts import (
    GpioFactSet, GpioVerificationError, HardwareScope, SourceFact, canonical_json, digest_bytes, validate_factset,
)
from .models import CatalogSnapshot, CircuitSnapshot, Digest, Identifier, Record, TerminalRef

RULESET = "gpio-capability-v1"
FUNCTIONS = frozenset({"GPIO_IN", "GPIO_OUT", "GPIO_IN_PULLUP"})
CHECKS = frozenset({
    "PIN_MAPPING", "PHYSICAL_CAPABILITY", "BOARD_AVAILABILITY", "INTERNAL_PULLUP_CAPABILITY",
    "BOOT_STRAP_CONTEXT", "ACTIVE_CONFIGURATION",
})
Status = Literal["PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE"]


class GpioRequirement(Record):
    requirement_id: Identifier
    terminal: TerminalRef
    requested_function: Identifier
    checks: tuple[Identifier, ...]
    operating_state: Identifier
    declared_configuration: Identifier | None = None
    firmware_observation_ref: Identifier | None = None


class _Result(Record):
    finding_id: Digest
    requirement_id: Identifier
    rule_id: Identifier
    rule_version: Literal["1.0"] = "1.0"
    terminal: TerminalRef
    affected_net: str
    requested_function: Identifier
    operating_state: Identifier
    declared_configuration: Identifier | None
    firmware_observation_ref: Identifier | None
    hardware_scope: HardwareScope
    evidence_claims: tuple[Identifier, ...]
    missing_prerequisites: tuple[Identifier, ...]
    reason_code: Identifier
    catalog_digest: Digest
    snapshot_digest: Digest
    factset_digest: Digest
    ruleset_version: Literal["gpio-capability-v1"] = RULESET


class GpioFinding(_Result):
    coverage: Literal["EVALUATED"] = "EVALUATED"
    status: Status
    severity: Literal["info", "warning", "error"]


class GpioCoverage(_Result):
    coverage: Literal["NOT_EVALUATED"] = "NOT_EVALUATED"


class GpioVerificationReport(Record):
    schema_version: Literal["1.0"] = "1.0"
    ruleset_version: Literal["gpio-capability-v1"] = RULESET
    catalog_digest: Digest
    snapshot_digest: Digest
    factset_digest: Digest
    findings: tuple[GpioFinding, ...]
    coverage: tuple[GpioCoverage, ...]


def serialize_gpio_report(report: GpioVerificationReport) -> bytes:
    return canonical_json(report.model_dump(mode="json"))


def _fact_value(rows: tuple[SourceFact, ...], field: str) -> tuple[object, str | None, tuple[str, ...]]:
    approved = tuple(row for row in rows if row.review == "approved")
    values = {getattr(row, field) for row in approved} - {None, "unknown"}
    if any(row.review == "conflicting" for row in rows) or len(values) > 1:
        return None, "EVIDENCE_CONFLICT", tuple(row.claim_id for row in rows)
    if not values:
        return None, "EVIDENCE_MISSING", tuple(row.claim_id for row in rows)
    return values.pop(), None, tuple(row.claim_id for row in approved)


def _mapping(facts, catalog, terminal):
    ref = terminal.signal_ref
    if (catalog.catalog_schema_version != "1.1" or ref is None
            or ref.mapping_status != "verified" or ref.target_kind != "soc_gpio"):
        return None, "MISSING_MAPPING", ()
    rows = tuple(row for row in facts.mappings if row.terminal_id == terminal.terminal_id)
    target, reason, evidence = _fact_value(rows, "target")
    if reason:
        return None, "MISSING_MAPPING" if reason == "EVIDENCE_MISSING" else reason, evidence
    if target != ref.target_id:
        return None, "AMBIGUOUS_MAPPING", evidence
    return target, None, (*evidence, ref.source_claim_id)


def _check(facts, req, rule, target):
    if rule == "PIN_MAPPING":
        return "PASS", "MAPPING_CONFIRMED", (), ()
    if rule == "ACTIVE_CONFIGURATION":
        return "UNKNOWN", "ACTIVE_CONFIG_UNKNOWN", (), ("validated_firmware_observation",)
    if rule == "BOOT_STRAP_CONTEXT":
        rows = tuple(row for row in facts.straps if row.target == target and row.boot_state == "RESET")
        value, reason, ids = _fact_value(rows, "is_strapping")
        if reason:
            return "UNKNOWN", reason, ids, ("boot_strap_fact",)
        if value is False:
            return "NOT_APPLICABLE", "NOT_A_STRAPPING_CONTACT", ids, ()
        missing = tuple(key for row in rows if row.review == "approved" for key in row.prerequisites)
        return "UNKNOWN", "BOOT_STRAP_CONDITIONS_UNKNOWN", ids, missing
    if rule == "BOARD_AVAILABILITY":
        rows = tuple(row for row in facts.resources if row.target == target
                     and row.operating_state == req.operating_state)
        value, reason, ids = _fact_value(rows, "reservation")
        if reason:
            return "UNKNOWN", reason, ids, ("board_resource_fact",)
        return (("FAIL", "RESERVED_RESOURCE", ids, ()) if value == "reserved"
                else ("PASS", "BOARD_RESOURCE_AVAILABLE", ids, ()))
    if rule == "INTERNAL_PULLUP_CAPABILITY" and req.requested_function != "GPIO_IN_PULLUP":
        return "NOT_APPLICABLE", "PULLUP_NOT_REQUESTED", (), ()
    if req.operating_state != "ACTIVE":
        return "UNKNOWN", "CAPABILITY_UNKNOWN", (), ("supported_operating_state",)
    rows = tuple(row for row in facts.silicon if row.target == target)
    if rule == "INTERNAL_PULLUP_CAPABILITY":
        field, rejected = "pullup_allowed", "PULLUP_NOT_CAPABLE"
    elif req.requested_function == "GPIO_OUT":
        field, rejected = "output_allowed", "OUTPUT_NOT_CAPABLE"
    else:
        field, rejected = "input_allowed", "INPUT_NOT_CAPABLE"
    value, reason, ids = _fact_value(rows, field)
    if reason:
        return "UNKNOWN", "CAPABILITY_UNKNOWN" if reason == "EVIDENCE_MISSING" else reason, ids, (field,)
    return (("PASS", "CAPABILITY_CONFIRMED", ids, ()) if value is True
            else ("FAIL", rejected, ids, ()))


def verify_gpio_requirements(
    catalog: CatalogSnapshot, snapshot: CircuitSnapshot, fact_set: GpioFactSet,
    requests: tuple[GpioRequirement, ...], trusted_catalog_sha256: str | None,
    trusted_factset_sha256: str | None,
) -> GpioVerificationReport:
    """Evaluate reviewed test-scope facts. The caller controls the provenance of expected pins."""
    topology = compute_nets(catalog, snapshot)  # CORE-001A validates catalog, snapshot and links.
    facts = validate_factset(fact_set)
    try:
        requests = TypeAdapter(tuple[GpioRequirement, ...]).validate_python(requests, strict=True)
    except ValidationError as exc:
        raise GpioVerificationError("INVALID_REQUIREMENTS") from exc
    if (len({req.requirement_id for req in requests}) != len(requests)
            or any(not req.checks or len(set(req.checks)) != len(req.checks) for req in requests)):
        raise GpioVerificationError("INVALID_REQUIREMENTS")
    for pin, actual, code in (
        (trusted_catalog_sha256, catalog.catalog_digest, "TRUSTED_CATALOG_PIN_MISMATCH"),
        (trusted_factset_sha256, facts.factset_digest, "TRUSTED_FACTSET_PIN_MISMATCH"),
    ):
        if pin is not None and pin != actual:
            raise GpioVerificationError(code)
    if facts.catalog_digest != catalog.catalog_digest:
        raise GpioVerificationError("FACTSET_CATALOG_MISMATCH")

    scope = facts.scope
    definitions = {item.definition_id: item for item in catalog.definitions}
    net_ids = dict(topology.terminal_to_net)
    findings, coverage = [], []
    pins = dict(catalog_digest=catalog.catalog_digest, snapshot_digest=topology.snapshot_sha256,
                factset_digest=facts.factset_digest)
    for req in requests:
        resolved = resolve_terminal(catalog, snapshot, req.terminal)
        device = definitions[resolved.definition_id]
        identity = device.identity
        scoped = (device.definition_id, device.definition_digest, identity.hardware_family,
                  identity.hardware_revision, identity.orderable_part_or_sku, identity.assembled_module,
                  identity.profile_scope) == (
            scope.definition_id, scope.definition_digest, scope.board_family, scope.board_revision,
            scope.orderable_part, scope.module, scope.profile_scope,
        )
        for rule in req.checks:
            status = None
            evidence = missing = ()
            if rule == "ELECTRICAL_COMPATIBILITY":
                reason = "ELECTRICAL_CHECK_DELEGATED"
            elif rule not in CHECKS or req.requested_function not in FUNCTIONS:
                reason = "OUT_OF_SCOPE"
            elif not scoped:
                reason = "UNSUPPORTED_DEVICE"
            elif trusted_catalog_sha256 is None:
                status, reason, missing = "UNKNOWN", "UNTRUSTED_CATALOG", ("trusted_catalog_pin",)
            elif trusted_factset_sha256 is None or facts.review == "UNREVIEWED":
                status, reason, missing = "UNKNOWN", "UNTRUSTED_FACTSET", ("reviewed_factset_pin",)
            else:
                target, reason, evidence = _mapping(facts, catalog, resolved.terminal)
                if reason is not None:
                    status, missing = "UNKNOWN", ("verified_soc_mapping",)
                else:
                    status, reason, rule_evidence, missing = _check(facts, req, rule, target)
                    evidence += rule_evidence
            attributes = dict(
                **pins, requirement_id=req.requirement_id, rule_id=rule, rule_version="1.0",
                ruleset_version=RULESET, hardware_scope=scope, terminal=req.terminal,
                affected_net=net_ids[f"T:{req.terminal.instance_id}/{req.terminal.terminal_id}"],
                requested_function=req.requested_function, operating_state=req.operating_state,
                declared_configuration=req.declared_configuration, firmware_observation_ref=req.firmware_observation_ref,
                reason_code=reason, evidence_claims=tuple(sorted(set(evidence))),
                missing_prerequisites=tuple(sorted(set(missing))),
            )
            if status is None:
                result = GpioCoverage(finding_id="sha256:" + "0" * 64, **attributes)
                output = coverage
            else:
                severity = {"FAIL": "error", "UNKNOWN": "warning"}.get(status, "info")
                result = GpioFinding(finding_id="sha256:" + "0" * 64, status=status, severity=severity, **attributes)
                output = findings
            preimage = canonical_json({"finding_schema_version": "1.0", **result.model_dump(
                mode="json", exclude={"finding_id"}
            )})
            output.append(result.model_copy(update={"finding_id": digest_bytes(preimage)}))

    def order(item):
        return (item.requirement_id, item.rule_id, item.terminal.instance_id, item.terminal.terminal_id, item.reason_code)

    return GpioVerificationReport(**pins, findings=tuple(sorted(findings, key=order)),
                                  coverage=tuple(sorted(coverage, key=order)))
