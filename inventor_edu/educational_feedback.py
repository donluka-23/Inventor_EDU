"""Read-only, test-only Georgian feedback grounded in current CORE and B records."""

from dataclasses import dataclass
from typing import Literal

from .core import compute_nets, resolve_terminal
from .gpio_facts import GpioFactSet, canonical_json, digest_bytes, validate_factset
from .gpio_verify import GpioCoverage, GpioFinding, GpioRequirement, GpioVerificationReport, verify_gpio_requirements
from .models import CatalogSnapshot, Digest, Identifier, Record, ResolvedTerminal, TerminalRef
from .synthesis import CHECKS, ROLE_FUNCTIONS, RoleTrace, SynthesisCandidate, SynthesisRequest

TEMPLATE_VERSION = "ka-GE/edu-001-v1"
Category = Literal[
    "ERROR_CAUSE", "SCOPED_CONFIRMATION", "MISSING_EVIDENCE", "NOT_EVALUATED_EXPLANATION",
    "CONTEXTUAL_CAUTION", "NEXT_ACTION_CANDIDATE",
]
RawResult = GpioFinding | GpioCoverage


class FeedbackInputError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class LearningContext(Record):
    request: SynthesisRequest
    anchor_requirement_id: Identifier
    current_snapshot_sha256: Digest
    trusted_catalog_sha256: Digest | None
    trusted_factset_sha256: Digest | None
    boot_state: Literal["RESET"] | None = None
    preview_unreviewed_ka: bool = False


class EngineeringReference(Record):
    origin: Literal["FINDING", "COVERAGE"]
    record_id: Digest
    snapshot_digest: Digest
    requirement_id: Identifier
    terminal: TerminalRef
    net_id: str
    rule_id: Identifier
    reason_code: Identifier
    operating_state: Identifier
    status: Literal["PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE", "NOT_EVALUATED"]


class SourceBinding(Record):
    origin: Literal["CATALOG_CLAIM", "GPIO_FACT"]
    claim_id: Identifier
    source_id: Identifier
    url: str
    revision: str
    locator: str
    scope: str
    recorded_review: Literal["approved"] = "approved"
    source_digest: Digest | None = None


class EducationalHint(Record):
    hint_id: Digest
    category: Category
    learning_concept: Identifier
    template_key: Identifier
    template_version: str
    text_ka: str
    requirement_id: Identifier
    source_terminal: TerminalRef
    terminal: TerminalRef
    net_id: str | None
    reference: EngineeringReference | None
    evidence: tuple[SourceBinding, ...]
    unresolved_scopes: tuple[EngineeringReference, ...]
    limitations: tuple[Identifier, ...]
    action_qualification: Literal["CANDIDATE_ACTION"] | None = None
    dependency_fingerprint: Digest
    validity: Literal["ACTIVE", "WITHDRAWN"] = "ACTIVE"


class EducationalFeedbackReport(Record):
    schema_version: Literal["1.0"] = "1.0"
    restriction: Literal["TEST_ONLY_NOT_PRODUCTION"] = "TEST_ONLY_NOT_PRODUCTION"
    localization_review: Literal["PENDING_HUMAN_REVIEW"] = "PENDING_HUMAN_REVIEW"
    snapshot_digest: Digest
    catalog_digest: Digest
    factset_digest: Digest
    requirements_digest: Digest
    evidence_scope: Literal["TEST_ONLY_SOURCE_REVIEWED", "TEST_ONLY_SYNTHETIC"]
    ruleset_version: Identifier
    template_version: str
    primary_hint: EducationalHint
    additional_hints: tuple[EducationalHint, ...]
    next_action: EducationalHint | None
    boot_context: Literal["NOT_REQUESTED", "NOT_ESTABLISHED", "CHECKED"]
    contextual_finding: GpioFinding | None
    contextual_coverage: GpioCoverage | None
    withdrawn_hints: tuple[EducationalHint, ...] = ()

    @property
    def active_hints(self) -> tuple[EducationalHint, ...]:
        tail = () if self.next_action is None else (self.next_action,)
        return (self.primary_hint, *self.additional_hints, *tail)


class FeedbackTransition(Record):
    old_snapshot_digest: Digest
    new_snapshot_digest: Digest
    withdrawn_hint_ids: tuple[Digest, ...]
    new_hint_ids: tuple[Digest, ...]
    current: EducationalFeedbackReport


@dataclass(frozen=True)
class _Grounding:
    trace: RoleTrace
    report: GpioVerificationReport
    resolved: ResolvedTerminal


def _reference(row: RawResult) -> EngineeringReference:
    evaluated = isinstance(row, GpioFinding)
    return EngineeringReference(
        origin="FINDING" if evaluated else "COVERAGE", record_id=row.finding_id,
        snapshot_digest=row.snapshot_digest, requirement_id=row.requirement_id, terminal=row.terminal,
        net_id=row.affected_net, rule_id=row.rule_id, reason_code=row.reason_code,
        operating_state=row.operating_state, status=row.status if evaluated else "NOT_EVALUATED",
    )


def _verified(
    candidate: SynthesisCandidate, catalog: CatalogSnapshot, facts: GpioFactSet,
    context: LearningContext, expected_snapshot: str | None,
) -> _Grounding:
    snapshot = candidate.snapshot
    topology = compute_nets(catalog, snapshot)
    request = context.request
    if expected_snapshot is not None and topology.snapshot_sha256 != expected_snapshot:
        raise FeedbackInputError("STALE_SNAPSHOT")
    if candidate.topology != topology:
        raise FeedbackInputError("TOPOLOGY_MISMATCH")
    if (request.catalog_digest != snapshot.catalog_digest or request.evidence_scope != facts.review
            or set(request.instances) != set(snapshot.instances)):
        raise FeedbackInputError("REQUEST_CONTEXT_MISMATCH")
    roles = {role.requirement_id: role for role in request.roles}
    traces = {trace.requirement_id: trace for trace in candidate.traces}
    if (len(roles) != 2 or len(traces) != 2 or len(candidate.traces) != 2 or roles.keys() != traces.keys()
            or {role.role for role in roles.values()} != ROLE_FUNCTIONS.keys()
            or context.anchor_requirement_id not in roles):
        raise FeedbackInputError("REQUIREMENT_ANCHOR_MISMATCH")
    if len({trace.assigned_terminal for trace in traces.values()}) != 2:
        raise FeedbackInputError("EXCLUSIVE_TERMINAL_MISMATCH")
    sources = {role.source_terminal for role in roles.values()}
    if len(sources) != 2 or len({ref.instance_id for ref in sources}) != 1:
        raise FeedbackInputError("REQUIREMENT_ANCHOR_MISMATCH")
    net_ids = dict(topology.terminal_to_net)
    actual_pairs = {frozenset((wire.endpoint_a, wire.endpoint_b)) for wire in snapshot.conductors}
    expected_pairs = set()
    requirements = []
    for key, role in roles.items():
        trace = traces[key]
        source, target = role.source_terminal, trace.assigned_terminal
        source_net = net_ids.get(f"T:{source.instance_id}/{source.terminal_id}")
        target_net = net_ids.get(f"T:{target.instance_id}/{target.terminal_id}")
        if (trace.role != role.role or source != trace.source_terminal or target not in role.domain
                or source.instance_id == target.instance_id
                or source_net is None or source_net != target_net or trace.net_id != target_net
                or trace.requirements_digest != request.requirements_digest
                or (trace.snapshot_digest, trace.catalog_digest, trace.factset_digest)
                != (topology.snapshot_sha256, snapshot.catalog_digest, facts.factset_digest)
                or trace.evidence_scope != facts.review or trace.operating_state != "ACTIVE"
                or ROLE_FUNCTIONS[role.role] != role.function):
            raise FeedbackInputError("ROLE_TRACE_MISMATCH")
        expected_pairs.add(frozenset((source, target)))
        requirements.append(GpioRequirement(requirement_id=key, terminal=target, requested_function=role.function,
                                            checks=CHECKS, operating_state="ACTIVE"))
    if (actual_pairs != expected_pairs or len(snapshot.conductors) != len(expected_pairs) or snapshot.junctions):
        raise FeedbackInputError("PHYSICAL_WIRING_MISMATCH")
    replay = verify_gpio_requirements(catalog, snapshot, facts, tuple(requirements),
                                      context.trusted_catalog_sha256, context.trusted_factset_sha256)
    supplied = candidate.gpio_report
    if (supplied.model_dump(exclude={"findings", "coverage"}) != replay.model_dump(exclude={"findings", "coverage"})
            or sorted(supplied.findings, key=lambda row: row.finding_id) != sorted(replay.findings, key=lambda row: row.finding_id)
            or sorted(supplied.coverage, key=lambda row: row.finding_id) != sorted(replay.coverage, key=lambda row: row.finding_id)):
        raise FeedbackInputError("UNVERIFIED_GPIO_REPORT")
    for trace in traces.values():
        if (set(trace.finding_ids) != {row.finding_id for row in replay.findings
                                     if row.requirement_id == trace.requirement_id}
                or set(trace.coverage_ids) != {row.finding_id for row in replay.coverage
                                             if row.requirement_id == trace.requirement_id}):
            raise FeedbackInputError("TRACE_REFERENCE_MISMATCH")
    trace = traces[context.anchor_requirement_id]
    return _Grounding(trace, replay, resolve_terminal(catalog, snapshot, trace.assigned_terminal))


def _source_bindings(
    row: RawResult, resolved: ResolvedTerminal, catalog: CatalogSnapshot, facts: GpioFactSet,
) -> tuple[tuple[SourceBinding, ...], tuple[str, ...]]:
    result, missing = [], []
    mapping = resolved.terminal.signal_ref
    catalog_claims = {claim.claim_id: claim for claim in catalog.claims}
    documents = {doc.source_document_id: doc for doc in catalog.source_documents}
    gpio_claims = {claim.claim_id: claim for claim in (*facts.mappings, *facts.silicon, *facts.resources, *facts.straps)}
    sources = {source.source_id: source for source in facts.sources}
    definitions = {item.definition_id: item for item in catalog.definitions}
    device = definitions[resolved.definition_id]
    exact_gpio_scope = row.hardware_scope == facts.scope and (
        facts.scope.definition_id, facts.scope.definition_digest, facts.scope.profile_scope,
    ) == (device.definition_id, device.definition_digest, device.identity.profile_scope)
    for claim_id in row.evidence_claims:
        claim = catalog_claims.get(claim_id)
        fact = gpio_claims.get(claim_id)
        if claim is not None and fact is None:
            doc = documents.get(claim.source_document_id)
            if (doc is not None and claim.review_status == "approved" and claim.locator
                    and claim.subject_definition_id == device.definition_id
                    and claim.scope == device.identity.profile_scope):
                result.append(SourceBinding(origin="CATALOG_CLAIM", claim_id=claim_id,
                    source_id=doc.source_document_id, url=doc.url, revision=doc.edition,
                    locator=claim.locator, scope=claim.scope, source_digest=doc.download_sha256))
                continue
        elif (fact is not None and claim is None and exact_gpio_scope and fact.review == "approved"
              and mapping is not None and mapping.target_kind == "soc_gpio" and mapping.target_id == fact.target
              and all(source_id in sources for source_id in fact.source_ids)):
            for source_id in sorted(set(fact.source_ids)):
                source = sources[source_id]
                result.append(SourceBinding(origin="GPIO_FACT", claim_id=claim_id,
                    source_id=source_id, url=source.url, revision=source.revision,
                    locator=fact.locator, scope=facts.scope.profile_scope, source_digest=source.artifact_sha256))
            continue
        missing.append(claim_id)
    return tuple(result), tuple(missing)


def _contact(ref: TerminalRef) -> str:
    return f"{ref.instance_id}/{ref.terminal_id}"


def _guidance(
    reference: EngineeringReference, trace: RoleTrace, target_gpio: str | None,
) -> tuple[Category, str, str, str]:
    source, contact = _contact(trace.source_terminal), _contact(trace.assigned_terminal)
    key = reference.rule_id, reference.status, reference.reason_code
    if target_gpio is not None:
        basis = ("ამ საცდელი ჩანაწერის მიხედვით" if trace.evidence_scope == "TEST_ONLY_SYNTHETIC"
                 else "დოკუმენტირებული ვარიანტის მიხედვით")
        if key == ("PHYSICAL_CAPABILITY", "FAIL", "OUTPUT_NOT_CAPABLE"):
            return ("ERROR_CAUSE", "gpio_direction", "output_not_capable",
                    f"სქემაში {source} უკავშირდება {contact} კონტაქტს ({target_gpio}). "
                    f"{trace.source_terminal.terminal_id} სიგნალის გასაგზავნად დაფას სჭირდება გამოსასვლელი "
                    f"(GPIO_OUT). {basis} {target_gpio} ამ ფუნქციას ვერ ასრულებს.")
        if key == ("PHYSICAL_CAPABILITY", "PASS", "CAPABILITY_CONFIRMED"):
            direction = "გამოსასვლელის" if trace.role == "TRIG_OUTPUT" else "შესასვლელის"
            return ("SCOPED_CONFIRMATION", "gpio_direction", "direction_pass",
                    f"სქემაში {source} უკავშირდება {contact} კონტაქტს ({target_gpio}). "
                    f"ACTIVE რეჟიმში {direction} ფუნქციის შემოწმება (PHYSICAL_CAPABILITY) გავლილია.")
        if key == ("BOARD_AVAILABILITY", "FAIL", "RESERVED_RESOURCE"):
            return ("ERROR_CAUSE", "board_availability", "reserved_resource",
                    f"{contact} ({target_gpio}) კონტაქტი დაფის რესურსისთვის არის დაკავებული. "
                    "მიმართულების მხარდაჭერა ამ შეზღუდვას არ ხსნის. "
                    "ამ დაფისთვის განიხილე სხვა კონტაქტი და ხელახლა გაუშვი შემოწმება.")
        if key == ("BOOT_STRAP_CONTEXT", "UNKNOWN", "BOOT_STRAP_CONDITIONS_UNKNOWN"):
            return ("CONTEXTUAL_CAUTION", "boot_context", "boot_conditions_unknown",
                    f"{contact} ({target_gpio}) კონტაქტისთვის ჩატვირთვის პირობები უცნობია (UNKNOWN). "
                    "GPIO-ის მიმართულების მხარდაჭერა ჩატვირთვის ქცევას ვერ ადგენს. "
                    "გადაამოწმე მტკიცებულების ჩანაწერში ჩამოთვლილი საწყისი პირობები.")
    if key == ("BOARD_AVAILABILITY", "UNKNOWN", "EVIDENCE_MISSING"):
        return ("MISSING_EVIDENCE", "board_availability", "board_unknown",
                f"{contact} კონტაქტის ხელმისაწვდომობა დაფაზე დაუდგენელია (BOARD_AVAILABILITY=UNKNOWN). "
                "გადაამოწმე ამ დაფის რესურსების დოკუმენტაცია.")
    if key == ("ACTIVE_CONFIGURATION", "UNKNOWN", "ACTIVE_CONFIG_UNKNOWN"):
        return ("MISSING_EVIDENCE", "firmware_configuration", "active_unknown",
                "პროგრამული კონფიგურაცია დაუდასტურებელია (ACTIVE_CONFIGURATION=UNKNOWN). "
                "ამის დასადგენად საჭიროა შემოწმებული დაკვირვება პროგრამის გაშვებაზე.")
    if key == ("ELECTRICAL_COMPATIBILITY", "NOT_EVALUATED", "ELECTRICAL_CHECK_DELEGATED"):
        return ("NOT_EVALUATED_EXPLANATION", "electrical_compatibility", "electrical_not_evaluated",
                "ელექტრული თავსებადობა არ შემოწმებულა (ELECTRICAL_COMPATIBILITY=NOT_EVALUATED).")
    return ("MISSING_EVIDENCE", "evidence_scope", "evidence_request",
            f"{contact} კონტაქტზე ამ შემოწმების შედეგის ასახსნელად საჭიროა შესაბამისი, გადამოწმებული მტკიცებულება.")


def _hint(
    anchor: _Grounding, reference: EngineeringReference | None, evidence: tuple[SourceBinding, ...],
    unresolved: tuple[EngineeringReference, ...], limitations: tuple[str, ...],
    guidance: tuple[Category, str, str, str], *, proposed: TerminalRef | None = None,
) -> EducationalHint:
    category, concept, key, wording = guidance
    trace, report = anchor.trace, anchor.report
    terminal = proposed if proposed is not None else trace.assigned_terminal
    net = None if reference is None else reference.net_id
    fingerprint = digest_bytes(canonical_json({
        "catalog": report.catalog_digest, "facts": report.factset_digest, "snapshot": report.snapshot_digest,
        "ruleset": report.ruleset_version, "requirements": trace.requirements_digest,
        "template_version": TEMPLATE_VERSION, "template_key": key, "text_ka": wording,
        "requirement_id": trace.requirement_id, "source": trace.source_terminal.model_dump(mode="json"),
        "terminal": terminal.model_dump(mode="json"),
        "reference": None if reference is None else reference.model_dump(mode="json"),
        "evidence": [item.model_dump(mode="json") for item in evidence],
        "unresolved": [item.model_dump(mode="json") for item in unresolved], "limitations": limitations,
    }))
    return EducationalHint(
        hint_id=fingerprint, category=category, learning_concept=concept, template_key=key,
        template_version=TEMPLATE_VERSION, text_ka=wording, requirement_id=trace.requirement_id,
        source_terminal=trace.source_terminal, terminal=terminal, net_id=net, reference=reference,
        evidence=evidence, unresolved_scopes=unresolved, limitations=limitations, dependency_fingerprint=fingerprint,
        action_qualification="CANDIDATE_ACTION" if category == "NEXT_ACTION_CANDIDATE" else None,
    )


def _grounded_mapping(
    anchor: _Grounding, evidence: tuple[SourceBinding, ...], missing: tuple[str, ...],
) -> str | None:
    mapping = anchor.resolved.terminal.signal_ref
    if (missing or mapping is None or mapping.mapping_status != "verified" or mapping.target_kind != "soc_gpio"
            or not any(item.origin == "CATALOG_CLAIM" and item.claim_id == mapping.source_claim_id
                       for item in evidence)
            or not any(item.origin == "GPIO_FACT" for item in evidence)):
        return None
    return mapping.target_id


def _render(row: RawResult, anchor: _Grounding, catalog, facts, unresolved) -> EducationalHint:
    reference = _reference(row)
    evidence, missing = _source_bindings(row, anchor.resolved, catalog, facts)
    target = _grounded_mapping(anchor, evidence, missing)
    guidance = _guidance(reference, anchor.trace, target)
    limits = set(row.missing_prerequisites)
    if guidance[2] == "evidence_request":
        limits.update(("EVIDENCE_REQUEST", row.reason_code))
    if missing:
        limits.add("EVIDENCE_REQUEST")
        limits.add("UNQUALIFIED_SOURCE_CLAIM")
        limits.update(missing)
    return _hint(anchor, reference, evidence, unresolved, tuple(sorted(limits)), guidance)


def _boot_check(candidate, catalog, facts, context, anchor) -> RawResult | None:
    if context.boot_state is None:
        return None
    mapping = anchor.resolved.terminal.signal_ref
    pin = next((row for row in anchor.report.findings if row.requirement_id == context.anchor_requirement_id
                and row.rule_id == "PIN_MAPPING" and row.status == "PASS"), None)
    if (pin is None or mapping is None or not any(
            row.review == "approved" and row.target == mapping.target_id and row.boot_state == context.boot_state
            for row in facts.straps)):
        return None
    check = GpioRequirement(requirement_id=pin.requirement_id, terminal=pin.terminal,
                            requested_function=pin.requested_function, checks=("BOOT_STRAP_CONTEXT",),
                            operating_state=context.boot_state)
    result = verify_gpio_requirements(catalog, candidate.snapshot, facts, (check,),
                                      context.trusted_catalog_sha256, context.trusted_factset_sha256)
    (row,) = (*result.findings, *result.coverage)
    return row


def _action(anchor, proposed, alternative, catalog, facts, context, unresolved):
    if proposed is None:
        if alternative is not None:
            raise FeedbackInputError("PROPOSED_TERMINAL_REQUIRED")
        return None
    proposed = TerminalRef.model_validate(proposed)
    role = next(role for role in context.request.roles if role.requirement_id == context.anchor_requirement_id)
    if proposed not in role.domain or proposed == anchor.trace.assigned_terminal:
        raise FeedbackInputError("PROPOSED_TERMINAL_OUTSIDE_ALTERNATIVES")
    prefix = f"შემდეგი ცდა: მოდელში შეამოწმე {_contact(proposed)} კონტაქტი "
    suffix = "და ხელახლა გაუშვი შემოწმება. ელექტრული თავსებადობა დაუდასტურებელია."
    guidance = ("NEXT_ACTION_CANDIDATE", "try_assignment", "try_candidate", prefix + suffix)
    if alternative is None:
        return _hint(anchor, None, (), unresolved, ("ALTERNATIVE_NOT_REPLAYED",), guidance, proposed=proposed)
    other = _verified(alternative, catalog, facts, context, expected_snapshot=None)
    if other.trace.assigned_terminal != proposed:
        raise FeedbackInputError("ALTERNATIVE_ANCHOR_MISMATCH")
    rows = tuple(row for row in other.report.findings if row.requirement_id == context.anchor_requirement_id)
    capability = next((row for row in rows if row.rule_id == "PHYSICAL_CAPABILITY" and row.status == "PASS"), None)
    if capability is not None and not any(row.status == "FAIL" for row in rows):
        evidence, missing = _source_bindings(capability, other.resolved, catalog, facts)
        if _grounded_mapping(other, evidence, missing) is not None:
            obligations = tuple(_reference(row) for row in (*rows, *other.report.coverage)
                                if row.requirement_id == context.anchor_requirement_id
                                and (isinstance(row, GpioCoverage) or row.status == "UNKNOWN"))
            source = _contact(anchor.trace.source_terminal)
            text = f"შემდეგი ცდა: მოდელში გადაიტანე {source} კავშირი {_contact(proposed)} კონტაქტზე " + suffix
            text += " ამ ალტერნატივაზე მიმართულების შემოწმება გავლილია."
            return _hint(other, _reference(capability), evidence, obligations, (),
                         ("NEXT_ACTION_CANDIDATE", "try_assignment", "try_scoped_alternative", text))
    return _hint(anchor, None, (), unresolved, ("ALTERNATIVE_NOT_QUALIFIED",), guidance, proposed=proposed)


def build_educational_feedback(
    candidate: SynthesisCandidate, catalog: CatalogSnapshot, fact_set: GpioFactSet, context: LearningContext, *,
    proposed_terminal: TerminalRef | None = None, alternative: SynthesisCandidate | None = None,
) -> EducationalFeedbackReport:
    """Replay B on the exact taught assignment, then render only source-qualified statements."""
    context = LearningContext.model_validate(context)
    if not context.preview_unreviewed_ka:
        raise FeedbackInputError("GEORGIAN_WORDING_REVIEW_REQUIRED")
    catalog = CatalogSnapshot.model_validate(catalog)
    facts = validate_factset(fact_set)
    anchor = _verified(candidate, catalog, facts, context, context.current_snapshot_sha256)
    report = anchor.report
    rows = tuple(row for row in (*report.findings, *report.coverage) if row.requirement_id == context.anchor_requirement_id)
    boot = _boot_check(candidate, catalog, facts, context, anchor)
    if boot is not None:
        rows = (*rows, boot)
    scopes = tuple(_reference(row) for row in rows if isinstance(row, GpioCoverage) or row.status == "UNKNOWN")
    physical = next(row for row in rows if row.rule_id == "PHYSICAL_CAPABILITY")
    primary = next((row for row in rows if isinstance(row, GpioFinding) and row.status == "FAIL"), physical)
    secondary = tuple(_render(row, anchor, catalog, facts, scopes) for row in rows
                      if row is not primary and (row is physical or isinstance(row, GpioCoverage) or row.status != "PASS"))
    return EducationalFeedbackReport(
        snapshot_digest=report.snapshot_digest, catalog_digest=report.catalog_digest, factset_digest=report.factset_digest,
        requirements_digest=context.request.requirements_digest, evidence_scope=context.request.evidence_scope,
        ruleset_version=report.ruleset_version,
        template_version=TEMPLATE_VERSION, primary_hint=_render(primary, anchor, catalog, facts, scopes),
        additional_hints=secondary, next_action=_action(anchor, proposed_terminal, alternative, catalog, facts, context, scopes),
        boot_context="CHECKED" if boot is not None else "NOT_ESTABLISHED" if context.boot_state else "NOT_REQUESTED",
        contextual_finding=boot if isinstance(boot, GpioFinding) else None,
        contextual_coverage=boot if isinstance(boot, GpioCoverage) else None,
    )


def transition_feedback(
    previous: EducationalFeedbackReport, candidate: SynthesisCandidate, catalog: CatalogSnapshot,
    fact_set: GpioFactSet, context: LearningContext,
) -> FeedbackTransition:
    """Rebuild current feedback and withdraw old active hints that no longer apply."""
    previous = EducationalFeedbackReport.model_validate(previous)
    current = build_educational_feedback(candidate, catalog, fact_set, context)
    old_ids = {hint.hint_id for hint in previous.active_hints}
    current_ids = {hint.hint_id for hint in current.active_hints}
    withdrawn = tuple(hint.model_copy(update={"validity": "WITHDRAWN"})
                      for hint in previous.active_hints if hint.hint_id not in current_ids)
    return FeedbackTransition(
        old_snapshot_digest=previous.snapshot_digest, new_snapshot_digest=current.snapshot_digest,
        withdrawn_hint_ids=tuple(hint.hint_id for hint in withdrawn),
        new_hint_ids=tuple(hint.hint_id for hint in current.active_hints if hint.hint_id not in old_ids),
        current=current.model_copy(update={"withdrawn_hints": withdrawn}),
    )
