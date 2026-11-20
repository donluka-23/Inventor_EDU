"""One independent test-only GPIO transfer item using existing engineering engines."""

from hashlib import sha256
from hmac import compare_digest, digest
from typing import Literal

from .capability_discovery import CapabilityQuery, discover_gpio_terminals
from .core import compute_nets
from .gpio_facts import canonical_json, digest_bytes, validate_factset
from .gpio_verify import GpioRequirement, verify_gpio_requirements
from .learning_session import LearningAction, LearningSessionState, LessonFixture, apply_learning_action
from .models import Digest, Identifier, Nonempty, Record, TerminalRef
from .synthesis import CHECKS, HARD_CHECKS, SynthesisCandidate, SynthesisRequest, generate_candidates

ScopeAnswer = Literal["NO", "YES"]


class TransferValidationError(ValueError):
    pass


class TransferItem(Record):
    item_id: Literal["edu-t1-echo-direction"] = "edu-t1-echo-direction"
    version: Literal["1.0"] = "1.0"
    fixed_trig: TerminalRef
    options: tuple[TerminalRef, TerminalRef]


class TransferSource(Record):
    claim_id: Identifier
    source_id: Identifier
    url: Nonempty
    revision: Nonempty
    locator: Nonempty


class TransferResult(Record):
    schema_version: Literal["1.0"] = "1.0"
    restriction: Literal["TEST_ONLY_NOT_PRODUCTION"] = "TEST_ONLY_NOT_PRODUCTION"
    localization_review: Literal["PENDING_HUMAN_REVIEW"] = "PENDING_HUMAN_REVIEW"
    source_review: Literal["TEST_ONLY_SOURCE_REVIEWED"] = "TEST_ONLY_SOURCE_REVIEWED"
    electrical_acceptance: Literal["NOT_ESTABLISHED"] = "NOT_ESTABLISHED"
    item: TransferItem
    training_revision: int
    training_snapshot_digest: Digest
    context_fingerprint: Digest
    outcome: Literal["TRANSFER_CORRECT_IN_SCOPE", "TRANSFER_INCORRECT"]
    selected: TerminalRef
    scope_answer: ScopeAnswer
    choice_supported_in_scope: bool
    scope_answer_correct: bool
    echo_requirement_id: Identifier
    evidence: tuple[TransferSource, ...]
    candidate: SynthesisCandidate
    result_digest: Digest


class TransferAttempt(Record):
    schema_version: Literal["1.0"] = "1.0"
    item: TransferItem
    training_revision: int
    training_snapshot_digest: Digest
    context_fingerprint: Digest
    catalog_digest: Digest
    factset_digest: Digest
    result: TransferResult | None = None

    @property
    def answered(self) -> bool:
        return self.result is not None


def _item(fixture: LessonFixture) -> TransferItem:
    board = fixture.board_instance_id
    return TransferItem(
        fixed_trig=TerminalRef(instance_id=board, terminal_id="J3.9"),
        options=tuple(TerminalRef(instance_id=board, terminal_id=key) for key in ("J2.5", "J3.19")),
    )


def _role_findings(candidate: SynthesisCandidate, requirement_id: str):
    return {row.rule_id: row for row in candidate.gpio_report.findings if row.requirement_id == requirement_id}


def can_start_transfer(fixture: LessonFixture, state: LearningSessionState) -> bool:
    """Presentation gate over the authoritative, server-owned practice state."""
    previous = state.previous_reference
    transition = state.last_transition
    if state.revision < 1 or previous is None or transition is None:
        return False
    pin = state.candidate.topology.snapshot_sha256
    key = fixture.anchor_requirement_id
    rows = _role_findings(state.candidate, key)
    direction = rows.get("PHYSICAL_CAPABILITY")
    return (
        previous.terminal == fixture.initial_terminal
        and (previous.requirement_id, previous.rule_id, previous.status, previous.reason_code)
        == (key, "PHYSICAL_CAPABILITY", "FAIL", "OUTPUT_NOT_CAPABLE")
        and previous.snapshot_digest == transition.old_snapshot_digest != pin
        and transition.new_snapshot_digest == pin
        and any(hint.reference == previous for hint in transition.current.withdrawn_hints)
        and direction is not None and direction.terminal == _item(fixture).fixed_trig
        and direction.requested_function == "GPIO_OUT" and direction.status == "PASS"
        and not any(row.rule_id in HARD_CHECKS and row.status == "FAIL" for row in rows.values())
    )


def _verified_report(fixture: LessonFixture, request: SynthesisRequest, candidate: SynthesisCandidate):
    if len(request.roles) != 2 or any(len(role.domain) != 1 for role in request.roles):
        raise TransferValidationError("TRANSFER_UNAVAILABLE")
    topology = compute_nets(fixture.catalog, candidate.snapshot)
    expected = {frozenset((role.source_terminal, role.domain[0])) for role in request.roles}
    actual = {frozenset((wire.endpoint_a, wire.endpoint_b)) for wire in candidate.snapshot.conductors}
    if (topology != candidate.topology or set(candidate.snapshot.instances) != set(request.instances)
            or len(expected) != 2 or len(candidate.snapshot.conductors) != 2
            or actual != expected or candidate.snapshot.junctions):
        raise TransferValidationError("TRANSFER_UNAVAILABLE")
    requirements = tuple(GpioRequirement(
        requirement_id=role.requirement_id, terminal=role.domain[0], requested_function=role.function,
        checks=CHECKS, operating_state="ACTIVE",
    ) for role in request.roles)
    replay = verify_gpio_requirements(
        fixture.catalog, candidate.snapshot, fixture.fact_set, requirements,
        fixture.trusted_catalog_sha256, fixture.trusted_factset_sha256,
    )
    if candidate.gpio_report != replay:
        raise TransferValidationError("TRANSFER_UNAVAILABLE")
    return replay


def _context(fixture: LessonFixture, state: LearningSessionState, item: TransferItem) -> tuple[str, str]:
    if apply_learning_action(fixture, state, LearningAction(revision=state.revision, action="WHY_CURRENT")).error:
        raise TransferValidationError("STALE_TRANSFER_CONTEXT")
    facts = validate_factset(fixture.fact_set)
    if (facts.review != "TEST_ONLY_SOURCE_REVIEWED" or fixture.catalog.catalog_digest != fixture.trusted_catalog_sha256
            or facts.factset_digest != fixture.trusted_factset_sha256 or facts.catalog_digest != fixture.trusted_catalog_sha256
            or not can_start_transfer(fixture, state)):
        raise TransferValidationError("TRANSFER_UNAVAILABLE")
    pin = state.candidate.topology.snapshot_sha256
    return pin, digest_bytes(canonical_json({
        "item": item.model_dump(mode="json"), "revision": state.revision, "snapshot": pin,
        "previous_snapshot": state.previous_reference.snapshot_digest, "requirements": state.request.requirements_digest,
        "catalog": fixture.trusted_catalog_sha256, "facts": fixture.trusted_factset_sha256,
        "ruleset": state.candidate.gpio_report.ruleset_version,
    }))


def start_transfer(fixture: LessonFixture, state: LearningSessionState) -> TransferAttempt:
    item = _item(fixture)
    pin, fingerprint = _context(fixture, state, item)
    _verified_report(fixture, state.request, state.candidate)
    return TransferAttempt(
        item=item, training_revision=state.revision, training_snapshot_digest=pin, context_fingerprint=fingerprint,
        catalog_digest=fixture.trusted_catalog_sha256, factset_digest=fixture.trusted_factset_sha256,
    )


def transfer_choices(attempt: TransferAttempt, key: bytes) -> tuple[tuple[TerminalRef, str], ...]:
    """Opaque, process-keyed tokens reveal no engineering verdict or digest."""
    return tuple((ref, digest(key, canonical_json(
        (attempt.context_fingerprint, ref.model_dump(mode="json"))
    ), sha256).hex()) for ref in attempt.item.options)


def _generate_transfer(fixture: LessonFixture, item: TransferItem, selected: TerminalRef):
    board = next(part for part in fixture.request.instances if part.instance_id == fixture.board_instance_id)
    roles = []
    for role in fixture.request.roles:
        if (role.role, role.function) not in {("TRIG_OUTPUT", "GPIO_OUT"), ("ECHO_INPUT", "GPIO_IN")}:
            raise TransferValidationError("TRANSFER_UNAVAILABLE")
        target = item.fixed_trig if role.role == "TRIG_OUTPUT" else selected
        query = CapabilityQuery(
            query_id=role.requirement_id, requirement_id=role.requirement_id, board_instance_id=board.instance_id,
            definition_id=board.definition_id, definition_digest=board.definition_digest,
            requested_function=role.function, operating_state="ACTIVE", catalog_digest=fixture.trusted_catalog_sha256,
            factset_digest=fixture.trusted_factset_sha256, evidence_scope="TEST_ONLY_SOURCE_REVIEWED",
        )
        discovery = discover_gpio_terminals(
            query, fixture.catalog, board, fixture.fact_set,
            trusted_catalog_sha256=fixture.trusted_catalog_sha256,
            trusted_factset_sha256=fixture.trusted_factset_sha256,
        )
        if target not in discovery.terminal_domain:
            raise TransferValidationError("TRANSFER_UNAVAILABLE")
        roles.append(role.model_copy(update={"domain": (target,)}))
    request = fixture.request.model_copy(update={"roles": tuple(roles), "request_id": "edu-t1-transfer"})
    search = generate_candidates(
        request, fixture.catalog, fixture.fact_set, trusted_catalog_sha256=fixture.trusted_catalog_sha256,
        trusted_factset_sha256=fixture.trusted_factset_sha256,
    )
    if search.termination != "EXHAUSTED_REVIEWED_DOMAIN" or len(search.candidates) != 1:
        raise TransferValidationError("TRANSFER_UNAVAILABLE")
    return request, search.candidates[0]


def _sources(fixture: LessonFixture, claim_ids: set[str]) -> tuple[TransferSource, ...]:
    facts = fixture.fact_set
    claims = {claim.claim_id: claim for claim in fixture.catalog.claims if claim.review_status == "approved"}
    docs = {doc.source_document_id: doc for doc in fixture.catalog.source_documents}
    knowledge = {row.claim_id: row for row in (*facts.mappings, *facts.silicon, *facts.resources, *facts.straps)
                 if row.review == "approved"}
    fact_sources = {source.source_id: source for source in facts.sources}
    bindings = []
    for key in sorted(claim_ids):
        claim = claims.get(key)
        fact = knowledge.get(key)
        doc = docs.get(claim.source_document_id) if claim is not None else None
        if doc is not None and claim.locator and fact is None:
            bindings.append(TransferSource(claim_id=key, source_id=doc.source_document_id, url=doc.url,
                                           revision=doc.edition, locator=claim.locator))
        elif fact is not None and claim is None:
            for sid in sorted(fact.source_ids):
                source = fact_sources[sid]
                bindings.append(TransferSource(claim_id=key, source_id=sid, url=source.url,
                                               revision=source.revision, locator=fact.locator))
        else:
            raise TransferValidationError("TRANSFER_UNAVAILABLE")
    return tuple(bindings)


def submit_transfer(
    fixture: LessonFixture, state: LearningSessionState, attempt: TransferAttempt,
    key: bytes, token: str, scope_answer: ScopeAnswer,
) -> TransferAttempt:
    if attempt.answered:
        raise TransferValidationError("TRANSFER_ALREADY_ANSWERED")
    if scope_answer not in ("NO", "YES") or len(token) != 64 or not token.isascii():
        raise TransferValidationError("INVALID_TRANSFER_RESPONSE")
    pin, context = _context(fixture, state, _item(fixture))
    if (attempt.item != _item(fixture) or attempt.training_revision != state.revision
            or attempt.training_snapshot_digest != pin or attempt.context_fingerprint != context
            or attempt.catalog_digest != fixture.trusted_catalog_sha256 or attempt.factset_digest != fixture.trusted_factset_sha256):
        raise TransferValidationError("STALE_TRANSFER_CONTEXT")
    selected = next((ref for ref, expected in transfer_choices(attempt, key) if compare_digest(token, expected)), None)
    if selected is None:
        raise TransferValidationError("INVALID_TRANSFER_CHOICE")
    request, candidate = _generate_transfer(fixture, attempt.item, selected)
    report = _verified_report(fixture, request, candidate)
    if report.snapshot_digest == pin:
        raise TransferValidationError("TRANSFER_UNAVAILABLE")
    echo = next(role for role in request.roles if role.role == "ECHO_INPUT")
    rows = _role_findings(candidate, echo.requirement_id)
    coverage = [row for row in report.coverage if row.requirement_id == echo.requirement_id]
    if (rows.keys() != set(CHECKS) - {"ELECTRICAL_COMPATIBILITY"}
            or [(row.rule_id, row.coverage) for row in coverage] != [("ELECTRICAL_COMPATIBILITY", "NOT_EVALUATED")]
            or rows["PIN_MAPPING"].status != "PASS" or rows["PHYSICAL_CAPABILITY"].status not in {"PASS", "FAIL"}
            or not rows["PHYSICAL_CAPABILITY"].evidence_claims
            or rows["BOARD_AVAILABILITY"].status not in {"PASS", "FAIL", "UNKNOWN"}
            or rows["BOARD_AVAILABILITY"].reason_code in {"EVIDENCE_CONFLICT", "UNTRUSTED_CATALOG", "UNTRUSTED_FACTSET"}):
        raise TransferValidationError("TRANSFER_UNAVAILABLE")
    supported = rows["PHYSICAL_CAPABILITY"].status == "PASS" and all(rows[rule].status != "FAIL" for rule in HARD_CHECKS)
    bindings = _sources(fixture, {claim for row in rows.values() for claim in row.evidence_claims})
    result = TransferResult(
        item=attempt.item, training_revision=state.revision, training_snapshot_digest=pin, context_fingerprint=context,
        outcome="TRANSFER_CORRECT_IN_SCOPE" if supported and scope_answer == "NO" else "TRANSFER_INCORRECT",
        selected=selected, scope_answer=scope_answer, choice_supported_in_scope=supported,
        scope_answer_correct=scope_answer == "NO", echo_requirement_id=echo.requirement_id, evidence=bindings,
        candidate=candidate, result_digest="sha256:" + "0" * 64,
    )
    result = result.model_copy(update={
        "result_digest": digest_bytes(canonical_json(result.model_dump(mode="json", exclude={"result_digest"}))),
    })
    return attempt.model_copy(update={"result": result})
