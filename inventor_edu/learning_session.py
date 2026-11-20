"""Pure action controller for the pinned, local two-role learning preview."""

from typing import Literal

from pydantic import ValidationError

from . import educational_feedback as edu, gpio_verify
from .capability_discovery import CapabilityQuery, TerminalCandidate, discover_gpio_terminals
from .gpio_facts import GpioFactSet, canonical_json, digest_bytes
from .models import CatalogSnapshot, Digest, Identifier, Record, TerminalRef
from .synthesis import SynthesisCandidate, SynthesisRequest, generate_candidates

Intent = Literal[
    "WHY_CURRENT", "SHOW_EVIDENCE", "SHOW_UNVERIFIED", "LIST_TERMINALS",
    "TRY_TERMINAL", "WHY_CHANGED", "SHOW_BOOT_CONTEXT", "RESET_LESSON",
]
ALIASES: dict[str, Intent] = {
    "რატომ?": "WHY_CURRENT",
    "წყაროები": "SHOW_EVIDENCE",
    "რა არ ვიცით?": "SHOW_UNVERIFIED",
    "კონტაქტები": "LIST_TERMINALS",
    "რა შეიცვალა?": "WHY_CHANGED",
    "ჩატვირთვა": "SHOW_BOOT_CONTEXT",
    "თავიდან დაწყება": "RESET_LESSON",
}


class LessonFixture(Record):
    catalog: CatalogSnapshot
    fact_set: GpioFactSet
    request: SynthesisRequest
    anchor_requirement_id: Identifier
    board_instance_id: Identifier
    initial_terminal: TerminalRef
    fixed_terminal: TerminalRef
    trusted_catalog_sha256: Digest
    trusted_factset_sha256: Digest


class LearningAction(Record):
    revision: int
    action: Intent
    selection_id: Digest | None = None


class TerminalOption(Record):
    discovered: TerminalCandidate
    selection_id: Digest | None


class LearningSessionState(Record):
    restriction: Literal["TEST_ONLY_NOT_PRODUCTION"] = "TEST_ONLY_NOT_PRODUCTION"
    localization_review: Literal["PENDING_HUMAN_REVIEW"] = "PENDING_HUMAN_REVIEW"
    revision: int
    context_fingerprint: Digest
    request: SynthesisRequest
    candidate: SynthesisCandidate
    options: tuple[TerminalOption, ...]
    initial_feedback: edu.EducationalFeedbackReport | None
    last_transition: edu.FeedbackTransition | None
    previous_reference: edu.EngineeringReference | None

    @property
    def feedback(self) -> edu.EducationalFeedbackReport:
        if self.last_transition is not None:
            return self.last_transition.current
        if self.initial_feedback is None:
            raise ValueError("MISSING_FEEDBACK")
        return self.initial_feedback


class LearningActionResult(Record):
    restriction: Literal["TEST_ONLY_NOT_PRODUCTION"] = "TEST_ONLY_NOT_PRODUCTION"
    localization_review: Literal["PENDING_HUMAN_REVIEW"] = "PENDING_HUMAN_REVIEW"
    state: LearningSessionState | None
    recognized_action: Intent | None
    error: Literal[
        "UNSUPPORTED_INTENT", "INVALID_ACTION", "STALE_SUBMISSION", "INVALID_CHOICE", "STALE_CONTEXT",
    ] | None = None


def _context_fingerprint(fixture: LessonFixture) -> str:
    # Include input records as well as the pins so copied, unvalidated edits fail closed.
    return digest_bytes(canonical_json({
        "fixture": fixture.model_dump(mode="json"),
        "ruleset": gpio_verify.RULESET, "template": edu.TEMPLATE_VERSION,
    }))


def _generate(fixture: LessonFixture, request: SynthesisRequest) -> tuple[SynthesisCandidate, ...]:
    result = generate_candidates(
        request, fixture.catalog, fixture.fact_set,
        trusted_catalog_sha256=fixture.trusted_catalog_sha256, trusted_factset_sha256=fixture.trusted_factset_sha256,
    )
    if result.termination != "EXHAUSTED_REVIEWED_DOMAIN" or len(result.candidates) != result.evaluated_candidates:
        raise ValueError("LESSON_DOMAIN_NOT_EXHAUSTED")
    return result.candidates


def _domains(fixture: LessonFixture) -> tuple[SynthesisRequest, tuple[TerminalCandidate, ...]]:
    board = next(instance for instance in fixture.request.instances if instance.instance_id == fixture.board_instance_id)
    roles = []
    anchor_options = ()
    for role in fixture.request.roles:
        query = CapabilityQuery(
            query_id=role.requirement_id, requirement_id=role.requirement_id, board_instance_id=board.instance_id,
            definition_id=board.definition_id, definition_digest=board.definition_digest,
            requested_function=role.function, operating_state="ACTIVE", catalog_digest=fixture.request.catalog_digest,
            factset_digest=fixture.fact_set.factset_digest, evidence_scope=fixture.request.evidence_scope,
        )
        discovered = discover_gpio_terminals(
            query, fixture.catalog, board, fixture.fact_set,
            trusted_catalog_sha256=fixture.trusted_catalog_sha256,
            trusted_factset_sha256=fixture.trusted_factset_sha256,
        )
        if role.requirement_id == fixture.anchor_requirement_id:
            anchor_options = discovered.candidates
            domain = discovered.terminal_domain
        else:
            if fixture.fixed_terminal not in discovered.terminal_domain:
                raise ValueError("FIXED_CONTACT_OUTSIDE_DISCOVERY")
            domain = (fixture.fixed_terminal,)
        roles.append(role.model_copy(update={"domain": domain}))
    return fixture.request.model_copy(update={"roles": tuple(roles)}), anchor_options


def _contact(candidate: SynthesisCandidate, fixture: LessonFixture) -> TerminalRef:
    return next(trace.assigned_terminal for trace in candidate.traces
                if trace.requirement_id == fixture.anchor_requirement_id)


def _selection_id(candidate: SynthesisCandidate, revision: int, snapshot: str) -> str:
    return digest_bytes(canonical_json((revision, snapshot, candidate.assignment_id)))


def _recompute(
    fixture: LessonFixture, selected: TerminalRef, previous: LearningSessionState | None,
) -> LearningSessionState:
    discovered_request, discovered = _domains(fixture)
    enumerated = {_contact(option, fixture): option for option in _generate(fixture, discovered_request)}
    if selected not in enumerated:
        raise ValueError("CONTACT_OUTSIDE_CURRENT_ASSIGNMENTS")
    request = discovered_request.model_copy(update={
        "roles": tuple(role.model_copy(update={"domain": (selected,)})
                       if role.requirement_id == fixture.anchor_requirement_id else role
                       for role in discovered_request.roles),
    })
    (candidate,) = _generate(fixture, request)
    context = edu.LearningContext(
        request=request, anchor_requirement_id=fixture.anchor_requirement_id,
        current_snapshot_sha256=candidate.topology.snapshot_sha256,
        trusted_catalog_sha256=fixture.trusted_catalog_sha256,
        trusted_factset_sha256=fixture.trusted_factset_sha256, boot_state="RESET",
        preview_unreviewed_ka=True,
    )
    revision = 0 if previous is None else previous.revision + 1
    options = tuple(TerminalOption(
        discovered=contact, selection_id=_selection_id(enumerated[contact.terminal], revision, context.current_snapshot_sha256)
        if contact.terminal in enumerated else None,
    ) for contact in discovered)
    initial = None
    transition = None
    before = None
    if previous is None:
        initial = edu.build_educational_feedback(candidate, fixture.catalog, fixture.fact_set, context)
    else:
        before = previous.feedback.primary_hint.reference
        transition = edu.transition_feedback(previous.feedback, candidate, fixture.catalog, fixture.fact_set, context)
    return LearningSessionState(
        revision=revision, context_fingerprint=_context_fingerprint(fixture), request=request, candidate=candidate,
        options=options, initial_feedback=initial, last_transition=transition, previous_reference=before,
    )


def start_learning_session(fixture: LessonFixture, *, preview: bool = False) -> LearningSessionState:
    """Start only on explicit opt-in, with fresh discovery, synthesis and feedback."""
    if preview is not True:
        raise ValueError("PREVIEW_OPT_IN_REQUIRED")
    fixture = LessonFixture.model_validate(fixture)
    return _recompute(fixture, fixture.initial_terminal, None)


def apply_learning_action(
    fixture: LessonFixture, state: LearningSessionState, action: LearningAction,
) -> LearningActionResult:
    """Apply one action to server-owned state. Failed actions yield no state change."""
    if state.context_fingerprint != _context_fingerprint(fixture):
        return LearningActionResult(state=None, recognized_action=None, error="STALE_CONTEXT")
    try:
        action = LearningAction.model_validate(action)
    except ValidationError:
        return LearningActionResult(state=state, recognized_action=None, error="INVALID_ACTION")
    intent = action.action
    if action.revision != state.revision:
        return LearningActionResult(state=state, recognized_action=intent, error="STALE_SUBMISSION")
    if intent == "TRY_TERMINAL":
        choice = next((choice for choice in state.options if action.selection_id is not None
                       and choice.selection_id == action.selection_id), None)
        if choice is None:
            return LearningActionResult(state=state, recognized_action=intent, error="INVALID_CHOICE")
        state = _recompute(fixture, choice.discovered.terminal, state)
    elif action.selection_id is not None:
        return LearningActionResult(state=state, recognized_action=intent, error="INVALID_ACTION")
    elif intent == "RESET_LESSON":
        state = _recompute(fixture, fixture.initial_terminal, state)
    return LearningActionResult(state=state, recognized_action=intent)


def apply_exact_alias(
    fixture: LessonFixture, state: LearningSessionState, revision: int, text: str,
) -> LearningActionResult:
    """Recognize exact aliases only. No free-text inference or storage."""
    if state.context_fingerprint != _context_fingerprint(fixture):
        return LearningActionResult(state=None, recognized_action=None, error="STALE_CONTEXT")
    intent = ALIASES.get(text)
    if intent is None:
        return LearningActionResult(state=state, recognized_action=None, error="UNSUPPORTED_INTENT")
    return apply_learning_action(fixture, state, LearningAction(revision=revision, action=intent))
