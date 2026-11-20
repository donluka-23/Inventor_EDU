"""Replay the bounded Georgian tutoring preview using the published test fixture."""

import argparse
from pathlib import Path

from inventor_edu import load_catalog
from inventor_edu.capability_discovery import CapabilityQuery, discover_gpio_terminals
from inventor_edu.educational_feedback import LearningContext, build_educational_feedback, transition_feedback
from inventor_edu.gpio_facts import canonical_json, digest_bytes, load_gpio_factset
from inventor_edu.models import ComponentInstance, TerminalRef
from inventor_edu.synthesis import SignalRole, SynthesisRequest, generate_candidates

# Independent expected test pins from reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md.
CATALOG_PIN = "sha256:356732040b6bd762e8c604ae63c3600df5da225cc938af6dff688b25aad4c57b"
FACTSET_PIN = "sha256:890f608028990e8f80f9ee48cd4388e58df1d160acc7edf2bf61445df8556d16"
DATA = Path(__file__).resolve().parents[1] / "data" / "gpio"
ANCHOR = "drive"


def load_fixture():
    catalog = load_catalog((DATA / "devkitc_32e_catalog.json").read_bytes(), expected_sha256=CATALOG_PIN)
    facts = load_gpio_factset((DATA / "devkitc_32e_facts.json").read_bytes())
    definitions = {item.definition_id: item for item in catalog.definitions}
    return catalog, facts, tuple(
        ComponentInstance(instance_id=key, definition_id=device.definition_id, definition_digest=device.definition_digest)
        for key, device in (("board", definitions[facts.scope.definition_id]), ("sensor", definitions["adafruit-3942-profile"]))
    )


def discover_request(catalog, facts, instances):
    board, sensor = instances
    specifications = (("TRIG_OUTPUT", ANCHOR, "Trig", "GPIO_OUT"), ("ECHO_INPUT", "listen", "Echo", "GPIO_IN"))
    discovery, roles = [], []
    for role, requirement_id, source_contact, function in specifications:
        query = CapabilityQuery(
            query_id=f"edu-{requirement_id}", requirement_id=requirement_id, board_instance_id=board.instance_id,
            definition_id=board.definition_id, definition_digest=board.definition_digest, requested_function=function,
            operating_state="ACTIVE", catalog_digest=catalog.catalog_digest, factset_digest=facts.factset_digest,
            evidence_scope=facts.review,
        )
        report = discover_gpio_terminals(query, catalog, board, facts,
                                         trusted_catalog_sha256=CATALOG_PIN, trusted_factset_sha256=FACTSET_PIN)
        discovery.append(report)
        roles.append(SignalRole(role=role, requirement_id=requirement_id, function=function,
            source_terminal=TerminalRef(instance_id=sensor.instance_id, terminal_id=source_contact),
            domain=report.terminal_domain))
    return tuple(discovery), SynthesisRequest(
        request_id="edu-discovered", requirements_digest=digest_bytes(canonical_json(specifications)),
        catalog_digest=catalog.catalog_digest, instances=instances, roles=tuple(roles),
        resource_constraint="AllDifferent", evidence_scope=facts.review, max_nodes=30, max_candidates=20,
    )


def _select(candidates, terminal, expect):
    return next(candidate for candidate in candidates if any(
        trace.requirement_id == ANCHOR and trace.assigned_terminal.terminal_id == terminal
        for trace in candidate.traces) and expect(candidate))


def _learning_context(request, candidate, *, boot_state=None):
    return LearningContext(
        request=request, anchor_requirement_id=ANCHOR, current_snapshot_sha256=candidate.topology.snapshot_sha256,
        trusted_catalog_sha256=CATALOG_PIN, trusted_factset_sha256=FACTSET_PIN, boot_state=boot_state,
        preview_unreviewed_ka=True,
    )


def run_cycle():
    catalog, facts, instances = load_fixture()
    discovery, request = discover_request(catalog, facts, instances)

    def generate(synthesis_request):
        return generate_candidates(synthesis_request, catalog, facts,
                                  trusted_catalog_sha256=CATALOG_PIN, trusted_factset_sha256=FACTSET_PIN)

    def direction(candidate, status, reason):
        return any((row.requirement_id, row.rule_id, row.status, row.reason_code)
                   == (ANCHOR, "PHYSICAL_CAPABILITY", status, reason) for row in candidate.gpio_report.findings)

    def same_echo(candidate):
        return any(trace.role == "ECHO_INPUT" and trace.assigned_terminal.terminal_id == "J3.8"
                   for trace in candidate.traces)

    candidates = generate(request).candidates
    before = _select(candidates, "J2.5", lambda item: same_echo(item) and direction(item, "FAIL", "OUTPUT_NOT_CAPABLE"))
    proposed = _select(candidates, "J3.9", lambda item: same_echo(item) and direction(item, "PASS", "CAPABILITY_CONFIRMED"))
    proposed_contact = next(trace.assigned_terminal for trace in proposed.traces if trace.requirement_id == ANCHOR)
    initial = build_educational_feedback(
        before, catalog, facts, _learning_context(request, before),
        proposed_terminal=proposed_contact, alternative=proposed,
    )
    # Scripted learner choice narrows both roles, then invokes SYN and B again.
    learner_request = request.model_copy(update={
        "request_id": "edu-learner-choice",
        "roles": tuple(role.model_copy(update={"domain": tuple(trace.assigned_terminal for trace in proposed.traces
                    if trace.requirement_id == role.requirement_id)}) for role in request.roles),
    })
    fresh = generate(learner_request).candidates[0]
    transition = transition_feedback(initial, fresh, catalog, facts, _learning_context(learner_request, fresh))
    strap_candidate = _select(candidates, "J3.14", lambda item: same_echo(item))
    contextual = build_educational_feedback(
        strap_candidate, catalog, facts, _learning_context(request, strap_candidate, boot_state="RESET"),
    )
    return discovery, before, initial, learner_request, fresh, transition, strap_candidate, contextual


def transcript(initial, transition, contextual) -> str:
    def describe(report):
        reference = report.primary_hint.reference
        lines = [report.snapshot_digest, f"{reference.rule_id}={reference.status}/{reference.reason_code}",
                 report.primary_hint.text_ka]
        lines.extend(f"  {binding.claim_id} | {binding.source_id} | {binding.locator} | {binding.url}"
                     for binding in report.primary_hint.evidence)
        return lines

    boot = contextual.contextual_finding
    boot_line = (f"{boot.rule_id}={boot.status}/{boot.reason_code} | {', '.join(boot.missing_prerequisites)}"
                 if boot is not None else contextual.boot_context)
    return "\n".join((
        "EDU-001 | TEST_ONLY_NOT_PRODUCTION | PENDING_HUMAN_REVIEW",
        "საწყისი შეერთება", *describe(initial), initial.next_action.text_ka,
        "რა შეიცვალა და რატომ", "მაგალითში მოსწავლე ირჩევს შეთავაზებულ კონტაქტს და შემოწმება თავიდან ეშვება.",
        f"წინა მინიშნება გაუქმდა (WITHDRAWN) | {initial.primary_hint.hint_id}",
        *describe(transition.current), "რა რჩება დაუდგენელი",
        *(hint.text_ka for hint in transition.current.additional_hints),
        "ცალკე შემოწმება ჩატვირთვისას", boot_line,
        *(hint.text_ka for hint in contextual.additional_hints if hint.category == "CONTEXTUAL_CAUTION"),
        *(f"  {binding.claim_id} | {binding.source_id} | {binding.locator}" for hint in contextual.additional_hints
          if hint.category == "CONTEXTUAL_CAUTION" for binding in hint.evidence if binding.claim_id.startswith("strap-")),
    ))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", required=True, help="use unreviewed Georgian draft wording")
    parser.add_argument("--json", action="store_true", help="emit deterministic machine-readable evidence")
    args = parser.parse_args()
    discovery, before, initial, learner_request, fresh, transition, strap_candidate, contextual = run_cycle()
    if args.json:
        records = {"before_candidate": before, "before": initial, "learner_choice": learner_request,
                   "after_candidate": fresh, "transition": transition, "boot_candidate": strap_candidate, "boot": contextual}
        body = {key: value.model_dump(mode="json") for key, value in records.items()}
        body["restriction"] = "TEST_ONLY_NOT_PRODUCTION"
        body["discovery"] = [report.model_dump(mode="json") for report in discovery]
        print(canonical_json(body).decode("utf-8"))
    else:
        print(transcript(initial, transition, contextual))


if __name__ == "__main__":
    main()
