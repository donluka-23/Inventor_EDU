"""Independent behavior and live loopback oracles for the one T1 item."""

from dataclasses import dataclass
from html.parser import HTMLParser
from threading import Thread
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

from examples.chat001_local_preview import CSP, LessonServer, NOTICE, reviewed_lesson
from inventor_edu.core import compute_nets
from inventor_edu.gpio_verify import GpioCoverage
from inventor_edu.learning_session import LearningAction, apply_learning_action, start_learning_session
from inventor_edu.transfer_assessment import (
    TransferValidationError, can_start_transfer, start_transfer, submit_transfer, transfer_choices,
)
from tests.test_chat001_learning_session import AFTER, BEFORE, PageForms, wire_request
from tests.test_gpio_capability import reseal

KEY = b"deterministic test key"
START = "დამოუკიდებელი შემოწმება"
SUBMIT = "პასუხების შემოწმება"
RESET = "თავიდან დაწყება"
CHOICE = "შეამოწმე board/J3.9"
PIN = "sha256:5090495849e1af8021bf83701328ea51831c63f3fcf9c1bcc8f50e6e88194f3e"
RESERVED_PIN = "sha256:c0b62b89933cdce52ff189342cfab603f902f217c1d1eb78797de0c40afaeca0"
ZERO = "sha256:" + "0" * 64


def corrected(fixture, state=None, contact="J3.9"):
    if state is None:
        state = start_learning_session(fixture, preview=True)
    choice = next(item.selection_id for item in state.options
                  if item.discovered.terminal.terminal_id == contact)
    return apply_learning_action(fixture, state, LearningAction(
        revision=state.revision, action="TRY_TERMINAL", selection_id=choice,
    )).state


def echo_rows(result):
    return {row.rule_id: row for row in result.candidate.gpio_report.findings
            if row.requirement_id == result.echo_requirement_id}


class Radios(HTMLParser):
    def __init__(self, html, name):
        super().__init__()
        self.values = []
        self.name = name
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "input" and attrs.get("type") == "radio" and attrs.get("name") == self.name:
            self.values.append(attrs["value"])


@dataclass
class Forms:
    port: int

    def get(self):
        return wire_request(self.port)[2]

    def post(self, page, label):
        return wire_request(self.port, "POST", fields=PageForms(page).forms[label])

    def pending(self):
        practice = self.get()
        fix = self.post(practice, CHOICE)[2]
        return self.post(fix, START)[2]

    def answers(self, pending, option=0, scope="NO"):
        return PageForms(pending).forms[SUBMIT] | {
            "terminal": Radios(pending, "terminal").values[option], "scope": scope,
        }


class TransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = reviewed_lesson()
        cls.initial = start_learning_session(cls.fixture, preview=True)
        cls.trained = corrected(cls.fixture, cls.initial)
        cls.attempt = start_transfer(cls.fixture, cls.trained)
        cls.tokens = tuple(token for _, token in transfer_choices(cls.attempt, KEY))

    def score(self, index=0, answer="NO"):
        return submit_transfer(self.fixture, self.trained, self.attempt, KEY, self.tokens[index], answer).result

    def test_T1_01_uses_original_independent_pins(self):
        self.assertEqual(self.fixture.trusted_catalog_sha256,
                         "sha256:356732040b6bd762e8c604ae63c3600df5da225cc938af6dff688b25aad4c57b")
        self.assertEqual(self.fixture.trusted_factset_sha256,
                         "sha256:890f608028990e8f80f9ee48cd4388e58df1d160acc7edf2bf61445df8556d16")
        self.assertEqual(self.attempt.factset_digest, self.fixture.fact_set.factset_digest)

    def test_T1_03_practice_cannot_be_skipped_or_wrong(self):
        for state in (self.initial, corrected(self.fixture, self.initial, "J3.19")):
            self.assertFalse(can_start_transfer(self.fixture, state))
            with self.assertRaisesRegex(TransferValidationError, "TRANSFER_UNAVAILABLE"):
                start_transfer(self.fixture, state)
        self.assertTrue(can_start_transfer(self.fixture, self.trained))

    def test_T1_04_selected_contact_is_evaluated_as_input_and_trig_stays_output(self):
        result = self.score()
        self.assertEqual(result.item.item_id, "edu-t1-echo-direction")
        traces = {item.role: item for item in result.candidate.traces}
        self.assertEqual(traces["TRIG_OUTPUT"].assigned_terminal.terminal_id, "J3.9")
        self.assertEqual(traces["ECHO_INPUT"].assigned_terminal.terminal_id, "J2.5")
        self.assertEqual({row.requested_function for row in echo_rows(result).values()}, {"GPIO_IN"})
        self.assertEqual(result.candidate.gpio_report.catalog_digest, self.fixture.trusted_catalog_sha256)

    def test_T1_06_tokens_are_process_revision_context_and_option_bound(self):
        self.assertNotEqual(*self.tokens)
        self.assertNotEqual(transfer_choices(self.attempt, b"another process"), transfer_choices(self.attempt, KEY))
        for option in ("0" * 64, self.tokens[0][:-1] + "g", "é" * 64):
            with self.assertRaises(TransferValidationError):
                submit_transfer(self.fixture, self.trained, self.attempt, KEY, option, "NO")
        for update in ({"training_revision": 2}, {"context_fingerprint": ZERO}, {"training_snapshot_digest": ZERO},
                       {"item": self.attempt.item.model_copy(update={"options": tuple(reversed(self.attempt.item.options))})}):
            with self.assertRaisesRegex(TransferValidationError, "STALE_TRANSFER_CONTEXT"):
                submit_transfer(self.fixture, self.trained, self.attempt.model_copy(update=update), KEY, self.tokens[0], "NO")

    def test_T1_08_input_and_no_are_correct_only_in_scope(self):
        result = self.score()
        self.assertEqual((result.outcome, result.electrical_acceptance),
                         ("TRANSFER_CORRECT_IN_SCOPE", "NOT_ESTABLISHED"))
        self.assertEqual(echo_rows(result)["PHYSICAL_CAPABILITY"].status, "PASS")
        self.assertIn("silicon-GPIO34", {source.claim_id for source in result.evidence})

    def test_T1_09_reserved_contact_is_incorrect_even_with_direction_pass(self):
        result = self.score(1)
        rows = echo_rows(result)
        self.assertEqual((result.outcome, rows["PHYSICAL_CAPABILITY"].status,
                          rows["BOARD_AVAILABILITY"].status, rows["BOARD_AVAILABILITY"].reason_code),
                         ("TRANSFER_INCORRECT", "PASS", "FAIL", "RESERVED_RESOURCE"))
        self.assertFalse(result.choice_supported_in_scope)

    def test_T1_10_electrical_overclaim_is_incorrect_even_with_correct_contact(self):
        result = self.score(answer="YES")
        self.assertTrue(result.choice_supported_in_scope)
        self.assertFalse(result.scope_answer_correct)
        self.assertEqual(result.outcome, "TRANSFER_INCORRECT")
        self.assertEqual(echo_rows(result)["PHYSICAL_CAPABILITY"].status, "PASS")

    def test_T1_11_exact_core_snapshots_and_verifier_pins(self):
        for index, contact, pin in ((0, "J2.5", PIN), (1, "J3.19", RESERVED_PIN)):
            result = self.score(index)
            candidate = result.candidate
            actual = compute_nets(self.fixture.catalog, candidate.snapshot)
            self.assertEqual((actual.snapshot_sha256, result.training_snapshot_digest), (pin, AFTER))
            self.assertIn((f"T:board/{contact}", "T:sensor/Echo"), {net.members for net in actual.nets})
            self.assertIn(("T:board/J3.9", "T:sensor/Trig"), {net.members for net in actual.nets})
            raw = candidate.gpio_report
            ratings = (*raw.findings, *raw.coverage)
            self.assertTrue(all(row.snapshot_digest == pin for row in ratings))
            self.assertEqual(len({row.finding_id for row in ratings}), 10)

    def test_T1_12_open_checks_are_distinct_raw_types(self):
        result = self.score()
        rows = echo_rows(result)
        coverage = next(row for row in result.candidate.gpio_report.coverage if row.requirement_id == "listen")
        self.assertIsInstance(coverage, GpioCoverage)
        self.assertEqual((coverage.rule_id, coverage.coverage), ("ELECTRICAL_COMPATIBILITY", "NOT_EVALUATED"))
        self.assertEqual((rows["BOARD_AVAILABILITY"].status, rows["ACTIVE_CONFIGURATION"].status), ("UNKNOWN", "UNKNOWN"))
        self.assertNotIn(coverage.rule_id, rows)

    def test_T1_15_source_role_and_report_fail_closed(self):
        bad_facts = self.fixture.fact_set.model_copy(update={"review": "UNREVIEWED"})
        wrong_roles = tuple(role.model_copy(update={"function": "GPIO_OUT"}) if role.role == "ECHO_INPUT" else role
                            for role in self.fixture.request.roles)
        for updates in ({"trusted_factset_sha256": ZERO}, {"trusted_catalog_sha256": ZERO},
                        {"fact_set": bad_facts}, {"request": self.fixture.request.model_copy(update={"roles": wrong_roles})}):
            with self.assertRaisesRegex(TransferValidationError, "STALE_TRANSFER_CONTEXT"):
                submit_transfer(self.fixture.model_copy(update=updates), self.trained, self.attempt, KEY, self.tokens[0], "NO")
        raw = self.score().candidate
        from inventor_edu.transfer_assessment import _generate_transfer
        request, _ = _generate_transfer(self.fixture, self.attempt.item, self.attempt.item.options[0])
        report = raw.gpio_report.model_copy(update={"coverage": ()})
        with patch("inventor_edu.transfer_assessment._generate_transfer",
                   return_value=(request, raw.model_copy(update={"gpio_report": report}))):
            with self.assertRaisesRegex(TransferValidationError, "TRANSFER_UNAVAILABLE"):
                self.score()
        body = self.fixture.fact_set.model_dump(mode="json")
        next(row for row in body["silicon"] if row["target"] == "GPIO34")["review"] = "unverified"
        facts = reseal(body)
        changed = self.fixture.model_copy(update={"fact_set": facts, "trusted_factset_sha256": facts.factset_digest})
        # The missing source also withdraws the original practice FAIL that gates assessment.
        with self.assertRaises(TransferValidationError):
            start_transfer(changed, corrected(changed))

    def test_T1_16_semantic_replay_and_unrelated_source_order_preserve_bytes(self):
        reorder = self.fixture.fact_set.model_copy(update={"sources": tuple(reversed(self.fixture.fact_set.sources))})
        changed = self.fixture.model_copy(update={"fact_set": reorder})
        state = corrected(changed)
        attempt = start_transfer(changed, state)
        result = submit_transfer(changed, state, attempt, KEY, self.tokens[0], "NO").result
        self.assertEqual(result.model_dump_json(), self.score().model_dump_json())
        with self.assertRaises(ValueError):
            result.outcome = "TRANSFER_INCORRECT"

    def test_T1_17_and_19_scoped_results_keep_approval_pending(self):
        result = self.score()
        self.assertEqual((result.restriction, result.localization_review, result.source_review),
                         ("TEST_ONLY_NOT_PRODUCTION", "PENDING_HUMAN_REVIEW", "TEST_ONLY_SOURCE_REVIEWED"))
        for forbidden in ('"SAFE"', '"MASTERED"', '"HARDWARE_COMPATIBLE"', '"READY_TO_BUILD"'):
            self.assertNotIn(forbidden, result.model_dump_json())


class TransferHttpTests(unittest.TestCase):
    def setUp(self):
        self.server = LessonServer(reviewed_lesson(), 0, preview=True)
        thread = Thread(target=self.server.serve_forever, kwargs={"poll_interval": .03}, daemon=True)
        thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(thread.join, 5)
        self.addCleanup(self.server.shutdown)
        self.forms = Forms(self.server.server_port)

    def test_T1_02_and_03_initial_preview_no_advance_by_get_or_forged_start(self):
        page = self.forms.get()
        for value in (NOTICE, BEFORE, "OUTPUT_NOT_CAPABLE", "GPIO34"):
            self.assertIn(value, page)
        self.assertNotIn(START, page)
        form = PageForms(page).forms[CHOICE]
        fields = {key: form[key] for key in ("csrf", "revision")} | {"action": "START_TRANSFER"}
        self.assertEqual(wire_request(self.forms.port, "POST", fields=fields)[0], 409)
        self.assertIsNone(self.server.transfer)

    def test_T1_05_pending_page_has_no_answer_or_hints_in_html(self):
        pending = self.forms.pending()
        self.assertIn(NOTICE, pending)
        self.assertIn("GPIO_IN", pending)
        self.assertEqual(len(Radios(pending, "terminal").values), 2)
        self.assertLess(pending.index("board/J2.5"), pending.index("board/J3.19"))
        self.assertEqual(Radios(pending, "scope").values, ["NO", "YES"])
        for forbidden in ("PASS", "FAIL", "RESERVED_RESOURCE", "GPIO34", "GPIO6", "href", "current-hint", AFTER, "კონტაქტები"):
            self.assertNotIn(forbidden, pending)
        self.assertEqual(pending, self.forms.get())

    def test_T1_07_missing_extra_duplicate_and_malformed_fields_reject(self):
        pending = self.forms.pending()
        valid = self.forms.answers(pending)
        for fields in (dict((k, v) for k, v in valid.items() if k != "scope"),
                       dict((k, v) for k, v in valid.items() if k != "terminal"),
                       valid | {"scope": "MAYBE"}, valid | {"finding": "PASS"}):
            self.assertEqual(wire_request(self.forms.port, "POST", fields=fields)[0], 400)
        raw = urlencode(valid).encode()
        for body in (raw + b"&scope=YES", raw.replace(b"scope=NO", b"scope=%FF"),
                     raw.replace(b"scope=NO", b"scope=%q1")):
            self.assertEqual(wire_request(self.forms.port, "POST", raw=body)[0], 400)
        self.assertFalse(self.server.transfer.answered)

    def test_T1_13_reset_and_rewire_invalidate_pending_and_tokens(self):
        pending = self.forms.pending()
        fields = self.forms.answers(pending)
        self.assertEqual(self.forms.post(pending, RESET)[0], 200)
        self.assertIsNone(self.server.transfer)
        self.assertEqual(wire_request(self.forms.port, "POST", fields=fields)[0], 409)
        practice = self.forms.get()
        practice = self.forms.post(practice, CHOICE)[2]
        pending = self.forms.post(practice, START)[2]
        old = self.forms.answers(pending)
        rewire = PageForms(practice).forms["შეამოწმე board/J3.19"]
        self.assertEqual(wire_request(self.forms.port, "POST", fields=rewire)[0], 200)
        self.assertIsNone(self.server.transfer)
        self.assertEqual(wire_request(self.forms.port, "POST", fields=old)[0], 409)

    def test_T1_14and20_browser_form_scores_once_and_replay_rejects(self):
        pending = self.forms.pending()
        fields = self.forms.answers(pending)
        status, _, result = wire_request(self.forms.port, "POST", fields=fields)
        self.assertEqual(status, 200)
        self.assertIn("TRANSFER_CORRECT_IN_SCOPE", result)
        self.assertIn("COVERAGE · ELECTRICAL_COMPATIBILITY=NOT_EVALUATED", result)
        self.assertIn(PIN, result)
        self.assertIn("silicon-GPIO34", result)
        self.assertEqual(result, self.forms.get())
        first = self.server.transfer
        for answer in ("NO", "YES"):
            status, _, response = wire_request(self.forms.port, "POST", fields=fields | {"scope": answer})
            self.assertEqual(status, 409)
            self.assertIn("TRANSFER_ALREADY_ANSWERED", response)
        restart = {key: fields[key] for key in ("csrf", "revision")} | {"action": "START_TRANSFER"}
        self.assertEqual(wire_request(self.forms.port, "POST", fields=restart)[0], 409)
        self.assertIs(self.server.transfer, first)

    def test_T1_09_and_10_incorrect_browser_cases_disclose_actual_reason_after(self):
        pending = self.forms.pending()
        for option, answer, expected in ((1, "NO", "BOARD_AVAILABILITY=FAIL/RESERVED_RESOURCE"),
                                         (0, "YES", "BOARD_AVAILABILITY=UNKNOWN")):
            status, _, page = wire_request(self.forms.port, "POST", fields=self.forms.answers(pending, option, answer))
            self.assertEqual(status, 200)
            self.assertIn("TRANSFER_INCORRECT", page)
            self.assertIn(expected, page)
            if answer == "YES":
                self.assertIn("პასუხი „დიახ“ არასწორია.", page)
            self.forms.post(page, RESET)
            pending = self.forms.pending()

    def test_T1_18_existing_transport_controls_guard_transfer(self):
        fields = self.forms.answers(self.forms.pending())
        self.assertEqual(self.server.server_address[0], "127.0.0.1")
        for headers in ({"Host": "test.invalid"}, {"Origin": "https://test.invalid"}, {"Origin": ""}):
            self.assertEqual(wire_request(self.forms.port, "POST", fields=fields, headers=headers)[0], 403)
        self.assertEqual(wire_request(self.forms.port, "POST", fields=fields | {"csrf": "bad"})[0], 403)
        self.assertEqual(wire_request(self.forms.port, "GET", "/?action=SUBMIT_TRANSFER")[0], 404)
        self.assertEqual(wire_request(self.forms.port, "POST", fields=fields | {"terminal": "f" * 64})[0], 400)
        status, headers, page = wire_request(self.forms.port)
        self.assertEqual((status, headers["Content-Security-Policy"], headers["Cache-Control"]), (200, CSP, "no-store"))
        self.assertNotIn("Set-Cookie", headers)
        self.assertNotIn("<script", page)
