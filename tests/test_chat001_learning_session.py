"""Independent controller, loopback HTTP and wording packet acceptance oracles."""

from base64 import b64encode
from hashlib import sha256
from html.parser import HTMLParser
from http.client import HTTPConnection
from pathlib import Path
import re
import subprocess
import sys
from threading import Thread
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

from examples.chat001_local_preview import LessonServer, NOTICE, _evidence, reviewed_lesson
from inventor_edu.educational_feedback import build_educational_feedback
from inventor_edu.learning_session import LearningAction, apply_exact_alias, apply_learning_action, start_learning_session
from tests.core001a_fixtures import ZERO, t
from tests.test_edu001_feedback import context, select, synthesis
from tests.test_syn001_generation import reviewed_fixture

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-X", "utf8", "-B", "-m", "examples.chat001_local_preview"]
BEFORE = "sha256:b6ccc23eb87fe910d9127ec7dfdaef68e18aba243af4e9996c4b09abddbf2369"
AFTER = "sha256:6fe1964503bdc98e1c3f82bd6c817ed92d0cef800b73734c7c11518d10a1a230"
FAIL_ID = "sha256:3f797ff0ed2bd36510d2f6c23e7262cc1c17f942da47b21283fbd57c386d4b33"
PASS_ID = "sha256:0b4a491805ae97648c107dc6951a7a9bf7abc3a0116e31d8081b318b47078050"
OPEN_CHECKS = ("BOARD_AVAILABILITY=UNKNOWN", "ACTIVE_CONFIGURATION=UNKNOWN", "ELECTRICAL_COMPATIBILITY=NOT_EVALUATED")


class PageForms(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.forms = {}
        self.fields = None
        self.label = None
        self.feed(page)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form":
            self.fields = {}
        elif self.fields is not None and tag == "input" and attrs.get("type") == "hidden":
            self.fields[attrs["name"]] = attrs["value"]
        elif self.fields is not None and tag == "button":
            self.label = ""

    def handle_data(self, data):
        if self.label is not None:
            self.label += data

    def handle_endtag(self, tag):
        if tag == "form":
            self.forms[self.label] = self.fields
            self.fields = None
            self.label = None


def wire_request(port, method="GET", path="/", *, fields=None, raw=None, headers=None):
    request_headers = {}
    if method == "POST":
        request_headers = {"Content-Type": "application/x-www-form-urlencoded", "Origin": f"http://127.0.0.1:{port}"}
    request_headers.update(headers or {})
    connection = HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        body = raw if raw is not None else urlencode(fields).encode("ascii") if fields is not None else None
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        return response.status, dict(response.getheaders()), response.read().decode("utf-8")
    finally:
        connection.close()


class ControllerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = reviewed_lesson()
        cls.initial = start_learning_session(cls.fixture, preview=True)

    def choose(self, state, terminal):
        option = next(item for item in state.options if item.discovered.terminal == t("board", terminal))
        return apply_learning_action(self.fixture, state, LearningAction(
            action="TRY_TERMINAL", revision=state.revision, selection_id=option.selection_id,
        ))

    def test_C03_why_uses_actual_edu_hint(self):
        result = apply_learning_action(self.fixture, self.initial, LearningAction(action="WHY_CURRENT", revision=0))
        self.assertTrue(result.state == self.initial)
        hint = result.state.feedback.primary_hint
        self.assertEqual((hint.reference.record_id, hint.source_terminal, hint.terminal),
                         (FAIL_ID, t("sensor", "Trig"), t("board", "J2.5")))
        self.assertIn("Trig სიგნალის გასაგზავნად დაფას სჭირდება გამოსასვლელი", hint.text_ka)
        self.assertEqual(result.recognized_action, "WHY_CURRENT")

    def test_C06_discovery_and_enumeration_distinguish_contacts(self):
        options = {item.discovered.terminal.terminal_id: item for item in self.initial.options}
        self.assertEqual(tuple(options), ("J2.5", "J3.14", "J3.19", "J3.8", "J3.9"))
        for contact, reason in (("J2.5", "OUTPUT_NOT_CAPABLE"), ("J3.19", "RESERVED_RESOURCE")):
            self.assertEqual(options[contact].discovered.qualification, "KNOWN_UNSUITABLE")
            self.assertIn(reason, options[contact].discovered.limitations)
        self.assertIsNone(options["J3.8"].selection_id)
        self.assertEqual(options["J3.9"].discovered.qualification, "FUNCTION_CONFIRMED_FOR_STATED_CHECK")
        for item in options.values():
            self.assertTrue(all(row.snapshot_digest != BEFORE for row in item.discovered.findings))

    def test_C08_another_choice_yields_actual_board_failure(self):
        result = self.choose(self.initial, "J3.19")
        hint = result.state.feedback.primary_hint
        self.assertEqual((hint.reference.status, hint.reference.rule_id, hint.reference.reason_code),
                         ("FAIL", "BOARD_AVAILABILITY", "RESERVED_RESOURCE"))
        self.assertNotEqual(result.state.feedback.snapshot_digest, BEFORE)
        self.assertTrue(any((item.requirement_id, item.rule_id, item.status)
                            == ("drive", "PHYSICAL_CAPABILITY", "PASS") for item in result.state.candidate.gpio_report.findings))
        self.assertNotIn('"SAFE"', result.model_dump_json())

    def test_C09_forged_off_domain_and_stale_tokens_rejected(self):
        bad = apply_learning_action(self.fixture, self.initial,
                                    LearningAction(action="TRY_TERMINAL", revision=0, selection_id=ZERO))
        none = self.choose(self.initial, "J3.8")
        self.assertEqual((bad.error, none.error), ("INVALID_CHOICE", "INVALID_CHOICE"))
        self.assertTrue(bad.state == self.initial)
        self.assertTrue(none.state == self.initial)
        fresh = self.choose(self.initial, "J3.9").state
        for revision, error in ((0, "STALE_SUBMISSION"), (1, "INVALID_CHOICE")):
            attempt = apply_learning_action(self.fixture, fresh,
                LearningAction(action="TRY_TERMINAL", revision=revision, selection_id=self.initial.options[0].selection_id))
            self.assertEqual(attempt.error, error)
            self.assertTrue(attempt.state == fresh)

    def test_C11_boot_context_retains_raw_separate_check(self):
        self.assertEqual(self.initial.feedback.boot_context, "NOT_ESTABLISHED")
        self.assertIsNone(self.initial.feedback.contextual_finding)
        state = self.choose(self.initial, "J3.14").state
        result = apply_learning_action(self.fixture, state, LearningAction(action="SHOW_BOOT_CONTEXT", revision=1))
        row = result.state.feedback.contextual_finding
        self.assertEqual((row.rule_id, row.status, row.reason_code, row.operating_state),
                         ("BOOT_STRAP_CONTEXT", "UNKNOWN", "BOOT_STRAP_CONDITIONS_UNKNOWN", "RESET"))
        self.assertEqual(row.missing_prerequisites, ("external_pull", "reset_level", "sampling_timing"))
        self.assertEqual(row.snapshot_digest, state.feedback.snapshot_digest)
        self.assertIn("strap-gpio0", row.evidence_claims)
        self.assertFalse(any(item.rule_id == row.rule_id for item in state.candidate.gpio_report.findings))

    def test_C13_unsupported_text_is_neutral_without_engine_calls(self):
        with patch("inventor_edu.learning_session._recompute") as engine:
            self.assertEqual(apply_exact_alias(self.fixture, self.initial, 0, "რატომ?").recognized_action, "WHY_CURRENT")
            for unsupported in ("GPIO18 მუშაობს?", " რატომ?", "რატომ", "TRY_TERMINAL"):
                result = apply_exact_alias(self.fixture, self.initial, 0, unsupported)
                self.assertEqual(result.error, "UNSUPPORTED_INTENT")
                self.assertTrue(result.state == self.initial)
            engine.assert_not_called()

    def test_C14_changed_source_requirements_pins_template_or_ruleset_fail_closed(self):
        action = LearningAction(action="WHY_CURRENT", revision=0)
        request = self.fixture.request.model_copy(update={"requirements_digest": ZERO})
        altered = self.fixture.fact_set.sources[0].model_copy(update={"revision": "test-edited-revision"})
        fact_set = self.fixture.fact_set.model_copy(update={"sources": (altered, *self.fixture.fact_set.sources[1:])})
        for update in ({"trusted_catalog_sha256": ZERO}, {"trusted_factset_sha256": ZERO},
                       {"request": request}, {"fact_set": fact_set}):
            result = apply_learning_action(self.fixture.model_copy(update=update), self.initial, action)
            self.assertEqual((result.error, result.state), ("STALE_CONTEXT", None))
        for attr in ("educational_feedback.TEMPLATE_VERSION", "gpio_verify.RULESET"):
            with patch(f"inventor_edu.{attr}", "test-revision"):
                result = apply_learning_action(self.fixture, self.initial, action)
            self.assertEqual((result.error, result.state), ("STALE_CONTEXT", None))

    def test_C18_controller_keeps_preview_restrictions(self):
        state = self.choose(self.initial, "J3.9").state
        result = apply_exact_alias(self.fixture, state, 1, "არაარსებული ბრძანება")
        for row in (state, state.feedback, result):
            self.assertEqual((row.restriction, row.localization_review),
                             ("TEST_ONLY_NOT_PRODUCTION", "PENDING_HUMAN_REVIEW"))

    def test_C19_all_ten_packet_drafts_match_live_edu_templates(self):
        packet = (ROOT / "docs/reviews/EDU001_KA_WORDING_REVIEW_PACKET.md").read_text(encoding="utf-8")
        entries = dict(re.findall(r"## \x60([a-z_]+)\x60\n.*?\x60{3}text\n(.*?)\n\x60{3}", packet, re.DOTALL))
        self.assertEqual(set(entries), {
            "output_not_capable", "direction_pass", "reserved_resource", "boot_conditions_unknown", "board_unknown",
            "active_unknown", "electrical_not_evaluated", "evidence_request", "try_candidate", "try_scoped_alternative",
        })
        self.assertEqual(packet.count("Decision ____________________ Reviewer ____________________ Date ____________________"), 10)
        self.assertEqual(packet.count("Notes _______________________________________________________________________________"), 10)
        self.assertIn("PENDING_HUMAN_REVIEW", packet)
        self.assertNotIn("APPROVED", packet)
        for contact, gpio in (("J2.5", "GPIO34"), ("J3.9", "GPIO18"), ("J3.19", "GPIO6"), ("J3.14", "GPIO0")):
            state = self.choose(self.initial, contact).state
            for hint in state.feedback.active_hints:
                self.assertEqual(hint.text_ka, entries[hint.template_key].format(
                    source="sensor/Trig", source_terminal_id="Trig", contact=f"board/{contact}", target_gpio=gpio,
                    basis="დოკუმენტირებული ვარიანტის მიხედვით", direction="გამოსასვლელის",
                ))
        request, catalog, facts = reviewed_fixture()
        candidates = synthesis(request, catalog, facts)
        failing, alternative = select(candidates, "J2.5"), select(candidates, "J3.9")
        for candidate in (None, alternative):
            report = build_educational_feedback(failing, catalog, facts, context(request, failing),
                proposed_terminal=t("board", "J3.9"), alternative=candidate)
            hint = report.next_action
            self.assertEqual(hint.text_ka, entries[hint.template_key].format(source="sensor/Trig", proposed_contact="board/J3.9"))
        untrusted = select(synthesis(request, catalog, facts, None, self.fixture.trusted_factset_sha256), "J2.5")
        report = build_educational_feedback(untrusted, catalog, facts, context(request, untrusted, None))
        self.assertEqual(report.primary_hint.text_ka, entries["evidence_request"].format(contact="board/J2.5"))


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.server = LessonServer(reviewed_lesson(), 0, preview=True)
        thread = Thread(target=self.server.serve_forever, kwargs={"poll_interval": .03}, daemon=True)
        thread.start()
        self.port = self.server.server_port
        self.addCleanup(self.server.server_close)
        self.addCleanup(thread.join, 5)
        self.addCleanup(self.server.shutdown)

    def get(self):
        status, headers, page = wire_request(self.port)
        self.assertEqual(status, 200)
        return headers, page

    def post(self, page, label):
        status, _, response = wire_request(self.port, "POST", fields=PageForms(page).forms[label])
        self.assertEqual(status, 200)
        return response

    def test_C01_cli_without_preview_or_non_loopback_rejects(self):
        for args in (["--port", "0"], ["--preview", "--host", "0.0.0.0"]):
            run = subprocess.run(CLI + args, cwd=ROOT, capture_output=True, encoding="utf-8", timeout=5)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(run.stdout, "")
            self.assertIn("error:", run.stderr)
        with self.assertRaisesRegex(ValueError, "PREVIEW_OPT_IN_REQUIRED"):
            LessonServer(reviewed_lesson(), 0)

    def test_C02_initial_real_failure_on_page(self):
        headers, page = self.get()
        for token in (NOTICE, "GPIO34", "OUTPUT_NOT_CAPABLE", BEFORE, FAIL_ID):
            self.assertIn(token, page)
        self.assertEqual(headers["Content-Type"], "text/html; charset=utf-8")

    def test_C04_C05_evidence_and_open_checks(self):
        _, page = self.get()
        evidence = self.post(self.post(page, "რატომ?"), "წყაროები")
        self.assertIn('<details open><summary>წყაროები</summary>', evidence)
        for token in ("silicon-GPIO34", "map-J2.5", "Header Block, J2 row 5", BEFORE, FAIL_ID, "sdk-mask",
                      "880a203ae603d08a94d06aa01e0d6761958e5e9e"):
            self.assertIn(token, evidence)
        self.assertIn('href="https://raw.githubusercontent.com/espressif/esp-idf/', evidence)
        missing = self.post(evidence, "რა არ ვიცით?")
        self.assertIn('<details open><summary>რა რჩება დაუდგენელი</summary>', missing)
        self.assertIn("sensor/Echo → board/J3.8", missing)
        self.assertIn("PHYSICAL_CAPABILITY=PASS/CAPABILITY_CONFIRMED", missing)
        for check in OPEN_CHECKS:
            self.assertIn(check, missing)

    def test_C07_C10_C12_real_browser_forms_recompute_compare_reset(self):
        _, page = self.get()
        unchanged = self.post(page, "რა შეიცვალა?")
        self.assertIn("არჩევანის შემდეგ გადასვლა აქ გამოჩნდება", unchanged)
        options = self.post(unchanged, "კონტაქტები")
        old_hint = self.server.state.feedback.primary_hint.hint_id
        next_page = self.post(options, "შეამოწმე board/J3.9")
        state = self.server.state
        self.assertEqual((state.revision, state.candidate.topology.snapshot_sha256), (1, AFTER))
        self.assertEqual(state.feedback.primary_hint.reference.record_id, PASS_ID)
        self.assertIn(old_hint, state.last_transition.withdrawn_hint_ids)
        self.assertNotIn(old_hint, {hint.hint_id for hint in state.feedback.active_hints})
        for token in ("GPIO18", "CAPABILITY_CONFIRMED", "WITHDRAWN", old_hint, *OPEN_CHECKS):
            self.assertIn(token, next_page)
        difference = self.post(next_page, "რა შეიცვალა?")
        for token in (BEFORE, AFTER, FAIL_ID, PASS_ID):
            self.assertIn(token, difference)
        reset = self.post(difference, "თავიდან დაწყება")
        self.assertIn(FAIL_ID, reset)
        self.assertEqual((self.server.state.feedback.snapshot_digest, self.server.state.revision), (BEFORE, 2))
        self.assertEqual(self.server.state.feedback.primary_hint.reference.reason_code, "OUTPUT_NOT_CAPABLE")

    def test_C15_http_claim_spoofs_reject_before_engine(self):
        _, page = self.get()
        form = PageForms(page).forms["შეამოწმე board/J3.9"]
        initial = self.server.state
        for field in ("status", "finding_id", "terminal_ref", "claim_id", "snapshot_digest"):
            self.assertEqual(wire_request(self.port, "POST", fields=form | {field: "PASS"})[0], 400)
            self.assertIs(self.server.state, initial)

    def test_C16_no_html_or_uri_injection(self):
        _, page = self.get()
        form = PageForms(page).forms["გაგზავნა"]
        status, _, result = wire_request(self.port, "POST", fields=form | {"text": "<script>alert(31337)</script>"})
        self.assertEqual(status, 400)
        self.assertIn("UNSUPPORTED_INTENT", result)
        self.assertNotIn("<script>", result)
        self.assertNotIn("31337", result)
        hint = self.server.state.feedback.primary_hint
        crafted = hint.evidence[0].model_copy(update={"url": "javascript:alert(1)", "locator": "<img src=x onerror=x>"})
        html = _evidence(hint.model_copy(update={"evidence": (crafted,)}))
        self.assertNotIn('href="javascript:', html)
        self.assertNotIn("<img", html)
        self.assertIn("&lt;img", html)
        original = hint.evidence[0].model_copy(update={"url": "https://example.invalid/?a=1&b=two"})
        html = _evidence(hint.model_copy(update={"evidence": (original,)}))
        self.assertIn('href="https://example.invalid/?a=1&amp;b=two"', html)

    def test_C17_loopback_authority_origin_csrf_method_and_policy(self):
        self.assertEqual(self.server.socket.getsockname()[0], "127.0.0.1")
        headers, page = self.get()
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertIn("default-src 'none'", headers["Content-Security-Policy"])
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
        style = page.split("<style>", 1)[1].split("</style>", 1)[0]
        self.assertIn(b64encode(sha256(style.encode()).digest()).decode(), headers["Content-Security-Policy"])
        form = PageForms(page).forms["შეამოწმე board/J3.9"]
        for h in ({"Host": "evil.invalid"}, {"Origin": "https://evil.invalid"}, {"Origin": ""}):
            self.assertEqual(wire_request(self.port, "POST", fields=form, headers=h)[0], 403)
        self.assertEqual(wire_request(self.port, "GET", headers={"Host": "evil.invalid"})[0], 403)
        self.assertEqual(wire_request(self.port, "GET", headers={"Origin": "https://evil.invalid"})[0], 403)
        self.assertEqual(wire_request(self.port, "POST", fields=form | {"csrf": "invalid"})[0], 403)
        self.assertEqual(wire_request(self.port, "POST", fields={k: v for k, v in form.items() if k != "csrf"})[0], 403)
        self.assertEqual(wire_request(self.port, "GET", "/?action=TRY_TERMINAL")[0], 404)
        self.assertEqual(wire_request(self.port, "POST", "/?action=TRY_TERMINAL", fields=form)[0], 404)
        self.assertEqual(wire_request(self.port, "PUT")[0], 501)
        self.assertEqual(self.server.state.revision, 0)

    def test_negative_bodies_and_repeated_forms(self):
        _, page = self.get()
        form = PageForms(page).forms["შეამოწმე board/J3.9"]
        valid = urlencode(form).encode("ascii")
        for body, expected in ((valid + b"&action=WHY_CURRENT", 400), (valid + b"&bogus=x", 400),
                               (valid + b"&ignored=%FF", 400), (valid + b"&bad=%z1", 400),
                               (b"x" * 4096, 413)):
            self.assertEqual(wire_request(self.port, "POST", raw=body)[0], expected)
        self.assertEqual(wire_request(self.port, "POST", fields=form | {"action": "UNKNOWN_ACTION"})[0], 400)
        self.assertEqual(wire_request(self.port, "POST", fields=form | {"terminal": ZERO})[0], 400)
        self.assertEqual(self.server.state.revision, 0)
        self.assertEqual(wire_request(self.port, "POST", fields=form)[0], 200)
        status, _, response = wire_request(self.port, "POST", fields=form)
        self.assertEqual(status, 409)
        self.assertIn("STALE_SUBMISSION", response)
        self.assertEqual(self.server.state.revision, 1)
