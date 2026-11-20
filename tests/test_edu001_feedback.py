"""Independent oracles for the test-only feedback cycle and evidence rejection."""

import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from inventor_edu import GpioVerificationError
from inventor_edu.educational_feedback import (
    FeedbackInputError, LearningContext, build_educational_feedback, transition_feedback,
)
from inventor_edu.gpio_verify import GpioCoverage, GpioFinding, GpioRequirement, verify_gpio_requirements
from inventor_edu.synthesis import generate_candidates
from tests.core001a_fixtures import ZERO, t
from tests.test_gpio_capability import CATALOG_PIN, FACT_PIN, reseal
from tests.test_syn001_generation import reviewed_fixture, synthetic_fixture

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-X", "utf8", "-B", "-m", "examples.edu001_learning_cycle", "--preview"]


def synthesis(request, catalog, facts, catalog_pin=CATALOG_PIN, fact_pin=FACT_PIN):
    return generate_candidates(request, catalog, facts, trusted_catalog_sha256=catalog_pin,
                               trusted_factset_sha256=fact_pin).candidates


def context(request, candidate, catalog_pin=CATALOG_PIN, fact_pin=FACT_PIN, **overrides):
    fields = dict(request=request, anchor_requirement_id="drive", current_snapshot_sha256=candidate.topology.snapshot_sha256,
                  trusted_catalog_sha256=catalog_pin, trusted_factset_sha256=fact_pin, preview_unreviewed_ka=True)
    return LearningContext(**(fields | overrides))


def select(candidates, contact):
    return next(candidate for candidate in candidates if any(
        trace.requirement_id == "drive" and trace.assigned_terminal.terminal_id == contact for trace in candidate.traces
    ))


def direction(row):
    return row.requirement_id == "drive" and row.rule_id == "PHYSICAL_CAPABILITY"


def replace_direction(candidate, **updates):
    report = candidate.gpio_report
    rows = tuple(row.model_copy(update=updates) if direction(row) else row for row in report.findings)
    return candidate.model_copy(update={"gpio_report": report.model_copy(update={"findings": rows})})


class EducationalFeedbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.request, cls.catalog, cls.facts = reviewed_fixture(trig=("J2.5", "J3.9", "J3.14", "J3.19"))
        candidates = synthesis(cls.request, cls.catalog, cls.facts)
        cls.before = select(candidates, "J2.5")
        cls.after = select(candidates, "J3.9")
        cls.strap = select(candidates, "J3.14")
        cls.reserved = select(candidates, "J3.19")
        cls.before_context = context(cls.request, cls.before)
        cls.after_context = context(cls.request, cls.after)
        cls.initial_report = build_educational_feedback(cls.before, cls.catalog, cls.facts, cls.before_context)
        cls.current_report = build_educational_feedback(cls.after, cls.catalog, cls.facts, cls.after_context)

    def assert_rejects(self, candidate, code, current=None):
        with self.assertRaises(FeedbackInputError) as caught:
            build_educational_feedback(candidate, self.catalog, self.facts, current or self.before_context)
        self.assertEqual(caught.exception.code, code)

    def test_E01_causal_georgian_failure_explains_requirement_and_terminal(self):
        hint = self.initial_report.primary_hint
        self.assertEqual((hint.category, hint.terminal, hint.source_terminal),
                         ("ERROR_CAUSE", t("board", "J2.5"), t("sensor", "Trig")))
        self.assertEqual((hint.reference.status, hint.reference.reason_code), ("FAIL", "OUTPUT_NOT_CAPABLE"))
        self.assertIn("Trig სიგნალის გასაგზავნად დაფას სჭირდება გამოსასვლელი", hint.text_ka)
        self.assertIn("GPIO34 ამ ფუნქციას ვერ ასრულებს", hint.text_ka)

    def test_E02_exact_finding_and_source_bindings(self):
        hint = self.initial_report.primary_hint
        observed = next(row for row in self.before.gpio_report.findings if direction(row))
        self.assertEqual((hint.reference.record_id, hint.reference.rule_id, hint.requirement_id,
                          hint.reference.snapshot_digest, hint.net_id, hint.terminal),
                         (observed.finding_id, "PHYSICAL_CAPABILITY", "drive", self.before.topology.snapshot_sha256,
                          observed.affected_net, observed.terminal))
        self.assertEqual({(row.origin, row.claim_id) for row in hint.evidence}, {
            ("CATALOG_CLAIM", "board-J2.5"), ("GPIO_FACT", "map-J2.5"), ("GPIO_FACT", "silicon-GPIO34"),
        })
        self.assertTrue(all(row.revision and row.recorded_review == "approved" for row in hint.evidence))
        locators = {(row.claim_id, row.source_id): row.locator for row in hint.evidence}
        self.assertEqual(locators["board-J2.5", "S18"], "Header Block, J2 row 5")
        self.assertIn("soc_caps.h", locators["silicon-GPIO34", "sdk-mask"])

    def test_E03_pass_is_scoped_to_direction(self):
        hint = self.current_report.primary_hint
        self.assertEqual((hint.category, hint.reference.rule_id, hint.reference.status),
                         ("SCOPED_CONFIRMATION", "PHYSICAL_CAPABILITY", "PASS"))
        self.assertIn("board/J3.9", hint.text_ka)
        self.assertIn("GPIO18", hint.text_ka)
        self.assertIn("გამოსასვლელის ფუნქციის შემოწმება", hint.text_ka)
        for forbidden in ("SAFE", "FULLY_COMPATIBLE", "სქემა სწორია", "უსაფრთხოა"):
            self.assertNotIn(forbidden, self.current_report.model_dump_json())
        self.assertEqual(self.current_report.localization_review, "PENDING_HUMAN_REVIEW")
        current = self.after_context.model_copy(update={"preview_unreviewed_ka": False})
        self.assert_rejects(self.after, "GEORGIAN_WORDING_REVIEW_REQUIRED", current)
        for contact, gpio in (("J3.8", "GPIO19"), ("J2.5", "GPIO34")):
            request, catalog, facts = reviewed_fixture(trig=("J3.9",), echo=(contact,))
            candidate = synthesis(request, catalog, facts)[0]
            report = build_educational_feedback(candidate, catalog, facts,
                context(request, candidate, anchor_requirement_id="listen"))
            self.assertEqual((report.primary_hint.terminal, report.primary_hint.reference.status),
                             (t("board", contact), "PASS"))
            self.assertIn(gpio, report.primary_hint.text_ka)
            self.assertIn("შესასვლელის", report.primary_hint.text_ka)

    def test_E04_prioritized_hint_keeps_three_open_scopes_visible(self):
        expected = {("BOARD_AVAILABILITY", "UNKNOWN"), ("ACTIVE_CONFIGURATION", "UNKNOWN"),
                    ("ELECTRICAL_COMPATIBILITY", "NOT_EVALUATED")}
        for report in (self.initial_report, self.current_report):
            self.assertEqual({(row.rule_id, row.status) for row in report.primary_hint.unresolved_scopes}, expected)
            self.assertEqual({(hint.reference.rule_id, hint.reference.status) for hint in report.additional_hints}, expected)
            for rule, status in expected:
                self.assertTrue(any(f"{rule}={status}" in hint.text_ka for hint in report.additional_hints))
        reserved = build_educational_feedback(self.reserved, self.catalog, self.facts,
                                               context(self.request, self.reserved))
        self.assertEqual((reserved.primary_hint.category, reserved.primary_hint.reference.reason_code),
                         ("ERROR_CAUSE", "RESERVED_RESOURCE"))
        self.assertTrue(any(hint.reference.rule_id == "PHYSICAL_CAPABILITY" and hint.reference.status == "PASS"
                            for hint in reserved.additional_hints))

    def test_E05_coverage_retains_its_actual_distinct_reference(self):
        raw = next(row for row in self.after.gpio_report.coverage if row.requirement_id == "drive")
        hint = next(hint for hint in self.current_report.additional_hints if hint.reference.origin == "COVERAGE")
        self.assertIsInstance(raw, GpioCoverage)
        self.assertEqual((hint.category, hint.reference.record_id, hint.reference.status),
                         ("NOT_EVALUATED_EXPLANATION", raw.finding_id, "NOT_EVALUATED"))
        self.assertNotIn(hint.reference.record_id, {row.finding_id for row in self.after.gpio_report.findings})

    def test_E06_missing_trust_cannot_create_hardware_details(self):
        for pins, reason in (((None, FACT_PIN), "UNTRUSTED_CATALOG"), ((CATALOG_PIN, None), "UNTRUSTED_FACTSET")):
            candidate = select(synthesis(self.request, self.catalog, self.facts, *pins), "J2.5")
            report = build_educational_feedback(candidate, self.catalog, self.facts,
                                                context(self.request, candidate, *pins))
            hint = report.primary_hint
            self.assertEqual((hint.category, hint.reference.status, hint.reference.reason_code, hint.evidence),
                             ("MISSING_EVIDENCE", "UNKNOWN", reason, ()))
            for forbidden in ("GPIO34", "Ω", "ვოლტ", "რეზისტორ"):
                self.assertNotIn(forbidden, hint.text_ka)
            raw_ids = {row.finding_id for row in (*candidate.gpio_report.findings, *candidate.gpio_report.coverage)}
            self.assertTrue(all(item.reference.record_id in raw_ids for item in report.active_hints))

    def test_E07_pin_mismatches_cannot_leave_hints_active(self):
        for field in ("catalog_digest", "snapshot_digest", "factset_digest"):
            with self.subTest(field=field):
                self.assert_rejects(replace_direction(self.before, **{field: ZERO}), "UNVERIFIED_GPIO_REPORT")
        for pins, code in (((ZERO, FACT_PIN), "TRUSTED_CATALOG_PIN_MISMATCH"),
                           ((CATALOG_PIN, ZERO), "TRUSTED_FACTSET_PIN_MISMATCH")):
            with self.subTest(code=code), self.assertRaises(GpioVerificationError) as caught:
                build_educational_feedback(self.before, self.catalog, self.facts,
                                            context(self.request, self.before, *pins))
            self.assertEqual(caught.exception.code, code)

    def test_E08_missing_unreviewed_or_conflicting_facts_abstain(self):
        for review in ("unverified", "conflicting", None):
            body = self.facts.model_dump(mode="json")
            claim = next(row for row in body["silicon"] if row["claim_id"] == "silicon-GPIO34")
            if review is None:
                body["silicon"].remove(claim)
            else:
                claim["review"] = review
            facts = reseal(body)
            candidate = select(synthesis(self.request, self.catalog, facts, CATALOG_PIN, facts.factset_digest), "J2.5")
            result = build_educational_feedback(candidate, self.catalog, facts,
                                                context(self.request, candidate, CATALOG_PIN, facts.factset_digest))
            with self.subTest(review=review):
                self.assertEqual(result.primary_hint.reference.status, "UNKNOWN")
                self.assertIn("EVIDENCE_REQUEST", result.primary_hint.limitations)
                self.assertNotIn("GPIO34", result.primary_hint.text_ka)

    def test_E09_identical_display_labels_do_not_move_hint(self):
        labeled = self.request.model_copy(update={"instances": tuple(
            item.model_copy(update={"user_label": "ერთი და იგივე სახელი"}) for item in self.request.instances
        )})
        candidate = select(synthesis(labeled, self.catalog, self.facts), "J2.5")
        report = build_educational_feedback(candidate, self.catalog, self.facts, context(labeled, candidate))
        self.assertEqual((report.primary_hint.terminal, report.primary_hint.source_terminal),
                         (t("board", "J2.5"), t("sensor", "Trig")))
        self.assertEqual(report.primary_hint.text_ka, self.initial_report.primary_hint.text_ka)
        self.assertNotEqual(report.snapshot_digest, self.initial_report.snapshot_digest)
        request, catalog, facts = synthetic_fixture()
        self.assertEqual({terminal.printed_label for device in catalog.definitions for terminal in device.terminals},
                         {"SAME"})
        pins = (catalog.catalog_digest, facts.factset_digest)
        candidate = select(synthesis(request, catalog, facts, *pins), "A")
        other = build_educational_feedback(candidate, catalog, facts, context(request, candidate, *pins))
        self.assertEqual((other.primary_hint.terminal, other.primary_hint.source_terminal),
                         (t("controller", "A"), t("peer", "stimulus")))
        self.assertNotIn("SAME", other.primary_hint.text_ka)

    def test_E10_semantic_order_and_repeat_are_stable(self):
        report = self.before.gpio_report
        candidate = self.before.model_copy(update={
            "traces": tuple(reversed(self.before.traces)),
            "gpio_report": report.model_copy(update={"findings": tuple(reversed(report.findings)),
                                                     "coverage": tuple(reversed(report.coverage))}),
        })
        reordered = self.request.model_copy(update={"roles": tuple(reversed(self.request.roles))})
        new_context = context(reordered, candidate)
        self.assertEqual(build_educational_feedback(candidate, self.catalog, self.facts, new_context),
                         self.initial_report)

    def test_E11_new_learner_assignment_withdraws_old_failure(self):
        narrowed = self.request.model_copy(update={"roles": tuple(
            role.model_copy(update={"domain": (t("board", "J3.9"),)}) if role.requirement_id == "drive" else role
            for role in self.request.roles)})
        fresh = synthesis(narrowed, self.catalog, self.facts)[0]
        transition = transition_feedback(self.initial_report, fresh, self.catalog, self.facts, context(narrowed, fresh))
        old = self.initial_report.primary_hint
        new = transition.current.primary_hint
        self.assertNotEqual(transition.old_snapshot_digest, transition.new_snapshot_digest)
        self.assertIn(old.hint_id, transition.withdrawn_hint_ids)
        self.assertEqual(transition.current.withdrawn_hints[0].validity, "WITHDRAWN")
        self.assertNotIn(old.hint_id, {hint.hint_id for hint in transition.current.active_hints})
        self.assertNotEqual(old.reference.record_id, new.reference.record_id)
        self.assertEqual((new.reference.status, new.terminal), ("PASS", t("board", "J3.9")))

    def test_E12_unverified_repair_is_only_a_candidate_action(self):
        proposal = t("board", "J3.9")
        result = build_educational_feedback(self.before, self.catalog, self.facts, self.before_context,
                                           proposed_terminal=proposal)
        self.assertEqual((result.next_action.action_qualification, result.next_action.reference, result.next_action.net_id),
                         ("CANDIDATE_ACTION", None, None))
        self.assertIn("ALTERNATIVE_NOT_REPLAYED", result.next_action.limitations)
        self.assertNotIn("VERIFIED_CORRECTION", result.model_dump_json())

    def test_E13_real_separate_boot_context_record_matches_direct_b(self):
        with patch("inventor_edu.educational_feedback.verify_gpio_requirements", wraps=verify_gpio_requirements) as spy:
            result = build_educational_feedback(self.strap, self.catalog, self.facts,
                                                context(self.request, self.strap, boot_state="RESET"))
        self.assertEqual(spy.call_count, 2)
        direct = verify_gpio_requirements(self.catalog, self.strap.snapshot, self.facts, (GpioRequirement(
            requirement_id="drive", terminal=t("board", "J3.14"), requested_function="GPIO_OUT",
            checks=("BOOT_STRAP_CONTEXT",), operating_state="RESET",
        ),), CATALOG_PIN, FACT_PIN)
        self.assertEqual((result.contextual_finding, result.contextual_coverage), (direct.findings[0], None))
        self.assertEqual((result.contextual_finding.status, result.contextual_finding.reason_code),
                         ("UNKNOWN", "BOOT_STRAP_CONDITIONS_UNKNOWN"))
        self.assertEqual(result.contextual_finding.missing_prerequisites, ("external_pull", "reset_level", "sampling_timing"))
        caution = next(hint for hint in result.additional_hints if hint.category == "CONTEXTUAL_CAUTION")
        self.assertIn("GPIO0", caution.text_ka)
        self.assertIn("ჩატვირთვის ქცევას ვერ ადგენს", caution.text_ka)
        self.assertIn("strap-gpio0", {binding.claim_id for binding in caution.evidence})

    def test_E14_missing_boot_fact_or_context_and_alternate_target(self):
        for candidate, state, expected in ((self.strap, None, "NOT_REQUESTED"),
                                            (self.after, "RESET", "NOT_ESTABLISHED")):
            report = build_educational_feedback(candidate, self.catalog, self.facts,
                                                context(self.request, candidate, boot_state=state))
            self.assertEqual(report.boot_context, expected)
            self.assertIsNone(report.contextual_finding)
        request, catalog, facts = synthetic_fixture()
        for strapping, status in ((True, "UNKNOWN"), (False, "NOT_APPLICABLE")):
            body = facts.model_dump(mode="json")
            body["straps"] = [dict(claim_id="synthetic-strap", target="Port1", source_ids=["fixture"], locator="B",
                                  review="approved", is_strapping=strapping, boot_state="RESET",
                                  condition="Fictitious start configuration", prerequisites=["test_condition"])]
            revised = reseal(body)
            candidate = select(synthesis(request, catalog, revised, catalog.catalog_digest, revised.factset_digest), "B")
            report = build_educational_feedback(candidate, catalog, revised,
                context(request, candidate, catalog.catalog_digest, revised.factset_digest, boot_state="RESET"))
            self.assertIsInstance(report.contextual_finding, GpioFinding)
            self.assertEqual(report.contextual_finding.status, status)
            self.assertEqual(report.contextual_finding.terminal, t("controller", "B"))
            caution = next(hint for hint in report.additional_hints if hint.reference.rule_id == "BOOT_STRAP_CONTEXT")
            self.assertEqual(caution.reference.status, status)
            self.assertNotIn("GPIO0", caution.text_ka)

    def test_E15_template_requirements_source_and_ruleset_invalidation(self):
        with patch("inventor_edu.educational_feedback.TEMPLATE_VERSION", "ka-GE/test-revision"):
            refreshed = transition_feedback(self.initial_report, self.before, self.catalog, self.facts, self.before_context)
        self.assertIn(self.initial_report.primary_hint.hint_id, refreshed.withdrawn_hint_ids)
        self.assertNotEqual(refreshed.current.primary_hint.hint_id, self.initial_report.primary_hint.hint_id)
        changed_requirements = self.request.model_copy(update={"requirements_digest": ZERO})
        self.assert_rejects(self.before, "ROLE_TRACE_MISMATCH", context(changed_requirements, self.before))
        req_changed = select(synthesis(changed_requirements, self.catalog, self.facts), "J2.5")
        req_hint = build_educational_feedback(req_changed, self.catalog, self.facts, context(changed_requirements, req_changed))
        self.assertNotEqual(req_hint.primary_hint.hint_id, self.initial_report.primary_hint.hint_id)
        body = self.facts.model_dump(mode="json")
        body["sources"][0]["revision"] = "separately pinned revised fixture"
        facts = reseal(body)
        candidate = select(synthesis(self.request, self.catalog, facts, CATALOG_PIN, facts.factset_digest), "J2.5")
        revised = build_educational_feedback(candidate, self.catalog, facts,
                                             context(self.request, candidate, CATALOG_PIN, facts.factset_digest))
        self.assertNotEqual(revised.primary_hint.hint_id, self.initial_report.primary_hint.hint_id)
        report = self.before.gpio_report.model_copy(update={"ruleset_version": "test-future-ruleset"})
        self.assert_rejects(self.before.model_copy(update={"gpio_report": report}), "UNVERIFIED_GPIO_REPORT")

    def test_E16_unrecognized_reason_or_rule_cannot_render(self):
        self.assert_rejects(replace_direction(self.before, reason_code="UNRECOGNIZED_REASON"), "UNVERIFIED_GPIO_REPORT")
        self.assert_rejects(replace_direction(self.before, rule_id="UNRECOGNIZED_RULE"), "UNVERIFIED_GPIO_REPORT")

    def test_E17_real_cli_georgian_transcript_and_structured_evidence(self):
        def run(args):
            return subprocess.run(args, cwd=ROOT, capture_output=True, check=True, encoding="utf-8").stdout
        transcript = run(CLI)
        for token in ("საწყისი შეერთება", "რა შეიცვალა და რატომ", "რა რჩება დაუდგენელი", "board/J2.5",
                      "board/J3.9", "WITHDRAWN", "PHYSICAL_CAPABILITY=PASS", "BOARD_AVAILABILITY=UNKNOWN",
                      "ACTIVE_CONFIGURATION=UNKNOWN", "ELECTRICAL_COMPATIBILITY=NOT_EVALUATED",
                      "BOOT_STRAP_CONDITIONS_UNKNOWN", "TEST_ONLY_NOT_PRODUCTION"):
            self.assertIn(token, transcript)
        trace = json.loads(run([*CLI, "--json"]))
        self.assertEqual(trace["transition"]["current"]["primary_hint"]["reference"]["status"], "PASS")
        self.assertEqual(trace["before"]["primary_hint"]["reference"]["status"], "FAIL")
        self.assertIn(trace["before"]["primary_hint"]["hint_id"], trace["transition"]["withdrawn_hint_ids"])
        self.assertEqual(trace["after_candidate"]["gpio_report"]["snapshot_digest"],
                         trace["transition"]["new_snapshot_digest"])

    def test_adversarial_forged_pass_is_rejected(self):
        self.assert_rejects(replace_direction(self.before, status="PASS", reason_code="CAPABILITY_CONFIRMED"),
                            "UNVERIFIED_GPIO_REPORT")

    def test_adversarial_swapped_physical_anchor_is_rejected(self):
        traces = tuple(trace.model_copy(update={"assigned_terminal": t("board", "J3.9")})
                       if trace.requirement_id == "drive" else trace for trace in self.before.traces)
        self.assert_rejects(self.before.model_copy(update={"traces": traces}), "ROLE_TRACE_MISMATCH")

    def test_adversarial_fabricated_source_claim_id_is_rejected(self):
        self.assert_rejects(replace_direction(self.before, evidence_claims=("fabricated-source",)), "UNVERIFIED_GPIO_REPORT")

    def test_adversarial_old_snapshot_cannot_become_current(self):
        self.assert_rejects(self.before, "STALE_SNAPSHOT", self.after_context)
