"""Serve the explicit CHAT-001 test preview on IPv4 loopback."""

import argparse
from base64 import b64encode
from hashlib import sha256
from hmac import compare_digest
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
from secrets import token_urlsafe
from urllib.parse import parse_qsl, urlsplit

from examples.edu001_learning_cycle import ANCHOR, CATALOG_PIN, FACTSET_PIN, load_fixture
from inventor_edu.gpio_facts import canonical_json, digest_bytes
from inventor_edu.learning_session import (
    ALIASES, LearningAction, LearningActionResult, LessonFixture, apply_exact_alias, apply_learning_action,
    start_learning_session,
)
from inventor_edu.models import TerminalRef
from inventor_edu.synthesis import SignalRole, SynthesisRequest
from pydantic import ValidationError

HOST = "127.0.0.1"
MAX_BODY_BYTES = 2048
NOTICE = "TEST_ONLY_NOT_PRODUCTION · ქართული ტექსტი დაუმტკიცებელია · PENDING_HUMAN_REVIEW"
LABELS = {
    "WHY_CURRENT": "რატომ?",
    "SHOW_EVIDENCE": "წყაროები",
    "SHOW_UNVERIFIED": "რა არ ვიცით?",
    "LIST_TERMINALS": "კონტაქტები",
    "TRY_TERMINAL": "სხვა კონტაქტის შემოწმება",
    "WHY_CHANGED": "რა შეიცვალა?",
    "SHOW_BOOT_CONTEXT": "ჩატვირთვა",
    "RESET_LESSON": "თავიდან დაწყება",
}
ERROR_TEXT = {
    "UNSUPPORTED_INTENT": "გამოიყენე ჩამოთვლილი მოქმედებებიდან ერთ-ერთი.",
    "INVALID_ACTION": "მოქმედების ფორმა არასწორია.",
    "INVALID_CHOICE": "ეს არჩევანი მიმდინარე სიაში ხელმისაწვდომი არ არის.",
    "STALE_SUBMISSION": "ფორმა ძველია. გამოიყენე მიმდინარე გვერდის მოქმედებები.",
    "STALE_CONTEXT": "გაკვეთილის კონტექსტი შეიცვალა. თავიდან გაუშვი ადგილობრივი გაკვეთილი.",
}
STATUS_TEXT = {
    "PASS": "PASS · გაიარა მხოლოდ მითითებულმა შემოწმებამ",
    "FAIL": "FAIL · ვერ გაიარა",
    "UNKNOWN": "UNKNOWN · დაუდგენელია",
    "NOT_APPLICABLE": "NOT_APPLICABLE · არ ვრცელდება",
    "NOT_EVALUATED": "NOT_EVALUATED · არ შემოწმებულა",
}
CSS = """
:root{color-scheme:light;background:#edf2f1;color:#172c2d;font:16px/1.65 "Segoe UI",system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0}main{max-width:72rem;margin:auto;padding:1.4rem}
header{background:#163837;color:#fff;padding:1.5rem;border-radius:1rem}h1,h2,h3,p{margin:0 0 .7rem}
h1{font-size:clamp(1.5rem,4vw,2.3rem)}h2{font-size:1.25rem}h3{font-size:1.05rem}
.notice{background:#ffe9ad;color:#3c2d00;padding:.65rem .8rem;border-radius:.4rem;font-weight:700}
.layout{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:1rem;margin-top:1rem}
article,aside section{background:#fff;padding:1.25rem;border-radius:.75rem;border:1px solid #cad7d5;margin-bottom:1rem}
.actions{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:.8rem}.actions form{margin:0}
button,input{font:inherit;border-radius:.4rem;padding:.45rem .7rem;border:1px solid #537572}
button{background:#e1f0ee;color:#183e3b;cursor:pointer;font-weight:600}button:hover{background:#cde8e4}
button:focus-visible,input:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid #985500;outline-offset:2px}
input{width:100%;margin:.35rem 0}code{overflow-wrap:anywhere;font-size:.91em}
li{margin:.45rem 0}ul{padding-left:1.25rem}a{color:#16574f;overflow-wrap:anywhere}
.status{display:inline-block;padding:.15rem .45rem;border-radius:.25rem;background:#e4efed;font-weight:700}
.fail,.error{background:#ffe2d9;color:#702d1e}.muted{color:#405d5b}.withdrawn{border-left:4px solid #9c7057;padding-left:.7rem}
details{margin:.65rem 0}summary{cursor:pointer;font-weight:650}.option{border-bottom:1px solid #dae4e3;padding:.55rem 0}
@media(max-width:47rem){.layout{grid-template-columns:1fr}main{padding:.65rem}}
"""
CSP = ("default-src 'none'; style-src 'sha256-" + b64encode(sha256(CSS.encode()).digest()).decode()
       + "'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'; object-src 'none'")


def reviewed_lesson() -> LessonFixture:
    """Bind lesson contacts and independent pins from the reviewed EDU fixture."""
    catalog, facts, instances = load_fixture()
    specs = (("TRIG_OUTPUT", ANCHOR, "Trig", "GPIO_OUT"), ("ECHO_INPUT", "listen", "Echo", "GPIO_IN"))
    roles = tuple(SignalRole(role=role, requirement_id=requirement, function=function,
                             source_terminal=TerminalRef(instance_id="sensor", terminal_id=terminal), domain=())
                  for role, requirement, terminal, function in specs)
    request = SynthesisRequest(
        request_id="chat-lesson", requirements_digest=digest_bytes(canonical_json(specs)), catalog_digest=CATALOG_PIN,
        instances=instances, roles=roles, resource_constraint="AllDifferent", evidence_scope="TEST_ONLY_SOURCE_REVIEWED",
        max_nodes=30, max_candidates=20,
    )
    return LessonFixture(
        catalog=catalog, fact_set=facts, request=request, anchor_requirement_id=ANCHOR, board_instance_id="board",
        initial_terminal=TerminalRef(instance_id="board", terminal_id="J2.5"),
        fixed_terminal=TerminalRef(instance_id="board", terminal_id="J3.8"),
        trusted_catalog_sha256=CATALOG_PIN, trusted_factset_sha256=FACTSET_PIN,
    )


def _e(value) -> str:
    return escape(str(value), quote=True)


def _contact(terminal: TerminalRef) -> str:
    return f"{terminal.instance_id}/{terminal.terminal_id}"


def _safe_source_link(url: str) -> str:
    if re.search(r"[\x00-\x20\x7f\\]", url):
        return _e(url)
    try:
        parts = urlsplit(url)
        allowed = parts.scheme in {"http", "https"} and bool(parts.hostname) and parts.username is None
    except ValueError:
        allowed = False
    if not allowed:
        return _e(url)
    return f'<a href="{_e(url)}" rel="noreferrer noopener">{_e(url)}</a>'


def _hidden(name: str, value) -> str:
    return f'<input type="hidden" name="{_e(name)}" value="{_e(value)}">'


def _button(common: str, action: str, selection_id: str | None = None, label: str | None = None) -> str:
    selected = "" if selection_id is None else _hidden("terminal", selection_id)
    return (f'<form action="/" method="post">{common}{_hidden("action", action)}{selected}'
            f'<button type="submit">{_e(label or LABELS[action])}</button></form>')


def _reference(ref) -> str:
    if ref is None:
        return "<p>შემოწმების ჩანაწერი მიუწვდომელია.</p>"
    status_css = "status fail" if ref.status == "FAIL" else "status"
    return (f'<p><span class="{status_css}">{_e(STATUS_TEXT[ref.status])}</span> '
            f'<code>{_e(ref.rule_id)} = {_e(ref.status)} / {_e(ref.reason_code)}</code></p>'
            f'<p><code>{_e(_contact(ref.terminal))} · {_e(ref.operating_state)}</code></p>'
            f'<p><code>{_e(ref.origin)} · {_e(ref.record_id)}<br>Snapshot · {_e(ref.snapshot_digest)}'
            f'<br>Net · {_e(ref.net_id)} · {_e(ref.requirement_id)}</code></p>')


def _evidence(hint) -> str:
    items = "".join(
        f'<li><code>{_e(item.origin)} · {_e(item.claim_id)} · {_e(item.source_id)}</code>'
        f'<br>{_e(item.locator)}<br><code>{_e(item.revision)} · {_e(item.recorded_review)}</code>'
        f'<br>{_safe_source_link(item.url)}</li>' for item in hint.evidence
    )
    return "<ul>" + items + "</ul>" if items else "<p>წყაროს ჩანაწერი მიუწვდომელია.</p>"


def _options(state, common: str) -> str:
    rows = []
    for option in state.options:
        item = option.discovered
        contact = _contact(item.terminal)
        observed = " · ".join(f"{row.rule_id}={row.status}/{row.reason_code}" for row in item.findings
                              if row.rule_id in {"PHYSICAL_CAPABILITY", "BOARD_AVAILABILITY"})
        select = (_button(common, "TRY_TERMINAL", option.selection_id, f"შეამოწმე {contact}")
                  if option.selection_id else "<p>ამ დავალებაში ეს კონტაქტი უკვე სხვა როლისთვისაა არჩეული.</p>")
        rows.append(f'<div class="option"><p><strong>{_e(contact)}</strong><br><code>{_e(item.qualification)}'
                    f'<br>{_e(observed)}</code></p>{select}</div>')
    return "".join(rows)


def _change(state) -> str:
    transition = state.last_transition
    if transition is None:
        return "<p>არჩევანის შემდეგ გადასვლა აქ გამოჩნდება.</p>"
    withdrawn = "".join(f'<li><code>WITHDRAWN · {_e(key)}</code></li>' for key in transition.withdrawn_hint_ids)
    prev = _reference(state.previous_reference)
    current = _reference(transition.current.primary_hint.reference)
    return (f'<h3>წინა შედეგი</h3>{prev}<h3>მიმდინარე შედეგი</h3>{current}'
            + (f'<div class="withdrawn"><h3>გაუქმებული მინიშნებები</h3><ul>{withdrawn}</ul></div>'
               if withdrawn else "<p>გაუქმებული მინიშნებები არ არის.</p>"))


def _boot(state) -> str:
    report = state.feedback
    row = report.contextual_finding or report.contextual_coverage
    if row is None:
        return f'<p><code>{_e(report.boot_context)}</code></p>'
    hints = tuple(item for item in report.additional_hints
                  if item.reference is not None and item.reference.record_id == row.finding_id)
    return (f'<p><code>{_e(report.boot_context)} · {_e(", ".join(row.missing_prerequisites))}</code></p>'
            + "".join(_reference(item.reference) + f"<p>{_e(item.text_ka)}</p>" + _evidence(item) for item in hints))


def _other_role(state) -> str:
    """Expose the second role from this circuit's report, separately from the primary hint."""
    anchor = state.feedback.primary_hint.requirement_id
    raw = state.candidate.gpio_report
    trace = next(item for item in state.candidate.traces if item.requirement_id != anchor)
    findings = [f"{row.rule_id}={row.status}/{row.reason_code}" for row in raw.findings
                if row.requirement_id == trace.requirement_id
                and (row.rule_id == "PHYSICAL_CAPABILITY" or row.status == "UNKNOWN")]
    coverage = [f"{row.rule_id}={row.coverage}/{row.reason_code}" for row in raw.coverage
                if row.requirement_id == trace.requirement_id]
    checks = "".join(f"<li><code>{_e(item)}</code></li>" for item in (*findings, *coverage))
    return (f'<h3>მეორე სიგნალი</h3><p><code>{_e(_contact(trace.source_terminal))} → '
            f'{_e(_contact(trace.assigned_terminal))}</code></p><ul>{checks}</ul>')


def render_page(result: LearningActionResult, csrf: str) -> str:
    state = result.state
    opening = ('<!doctype html><html lang="ka"><head><meta charset="utf-8">'
               '<meta name="viewport" content="width=device-width, initial-scale=1">'
               f'<title>INVENTOR EDU · ადგილობრივი გაკვეთილი</title><style>{CSS}</style></head><body><main>'
               f'<header><h1>INVENTOR EDU</h1><p>ადგილობრივი სასწავლო სესია</p>'
               f'<div class="notice">{_e(NOTICE)}</div></header>')
    ending = "</main></body></html>"
    error = (f'<p class="error" role="alert"><code>{_e(result.error)}</code> · {_e(ERROR_TEXT[result.error])}</p>'
             if result.error else "")
    if state is None:
        return opening + error + ending
    report = state.feedback
    common = _hidden("csrf", csrf) + _hidden("revision", state.revision)
    actions = "".join(_button(common, key) for key in LABELS if key != "TRY_TERMINAL")
    aliases = " · ".join(ALIASES)
    prompt = (f'<details><summary>ზუსტი ტექსტური ბრძანებები</summary><p class="muted">{_e(aliases)}</p>'
              f'<form action="/" method="post">{common}<label for="command">ბრძანება</label>'
              '<input id="command" name="text" maxlength="80" required autocomplete="off">'
              '<button type="submit">გაგზავნა</button></form></details>')
    recognized = f'<p class="muted">მოქმედება · {_e(LABELS[result.recognized_action])}</p>' if result.recognized_action else ""
    hint = report.primary_hint
    unknown = "".join(f'<li><code>{_e(item.reference.rule_id)}={_e(item.reference.status)}</code>'
                      f'<br>{_e(item.text_ka)}</li>' for item in report.additional_hints
                      if item.reference is not None and item.reference.status in {"UNKNOWN", "NOT_EVALUATED"})
    withdrawal = (f'<p class="withdrawn"><code>WITHDRAWN · {_e(state.last_transition.withdrawn_hint_ids[0])}</code></p>'
                  if state.last_transition and state.last_transition.withdrawn_hint_ids else "")
    open_for = lambda *ids: " open" if result.recognized_action in ids else ""
    return (opening + '<div class="layout"><div><article><h2>მიმდინარე მინიშნება</h2>' + error + recognized
            + f'<p id="current-hint">{_e(hint.text_ka)}</p>{_reference(hint.reference)}{withdrawal}'
            + f'<details{open_for("SHOW_EVIDENCE")}><summary>წყაროები</summary>{_evidence(hint)}</details>'
            + f'<details{open_for("SHOW_UNVERIFIED", "TRY_TERMINAL", "RESET_LESSON")}><summary>რა რჩება დაუდგენელი</summary>'
              f'<ul>{unknown}</ul>{_other_role(state)}</details>'
            + f'<details{open_for("WHY_CHANGED", "TRY_TERMINAL", "RESET_LESSON")}><summary>რა შეიცვალა?</summary>'
              f'{_change(state)}</details>'
            + f'<details{open_for("SHOW_BOOT_CONTEXT")}><summary>ჩატვირთვა</summary>{_boot(state)}</details></article>'
            + f'<article><h2>მოქმედებები</h2><div class="actions">{actions}</div>{prompt}</article></div>'
            + '<aside><section><h2>დაფის კონტაქტები</h2><p class="muted">CAP · დაფის ცალკე შემოწმება</p>'
            + _options(state, common) + '</section></aside></div>' + ending)


class LessonServer(HTTPServer):
    def __init__(self, fixture: LessonFixture, port: int, *, preview: bool = False):
        self.fixture = fixture
        self.state = start_learning_session(fixture, preview=preview)
        self.csrf = token_urlsafe(32)
        super().__init__((HOST, port), LessonHandler)
        self.authority = f"{HOST}:{self.server_port}"
        self.origin = f"http://{self.authority}"


class LessonHandler(BaseHTTPRequestHandler):
    server: LessonServer
    server_version = "InventorEDU-Preview"
    sys_version = ""

    def setup(self):
        self.request.settimeout(4)
        super().setup()

    def log_message(self, format, *args):
        # Do not collect request paths, free text or request metadata.
        return

    def _send(self, status: int, body: str, content_type: str = "text/plain; charset=utf-8"):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def send_error(self, code, message=None, explain=None):
        self._send(code, f"{NOTICE}\nREQUEST_REJECTED")

    def _body_length(self) -> int | None:
        lengths = self.headers.get_all("Content-Length", [])
        if (len(lengths) != 1 or re.fullmatch(r"[0-9]{1,10}", lengths[0]) is None
                or self.headers.get_all("Transfer-Encoding", [])):
            return None
        return int(lengths[0])

    def _discard_small_body(self):
        # Windows may reset a closing socket with unread data before delivering a rejection.
        # Never drain an oversized, ambiguously framed or indefinitely delayed request.
        size = self._body_length()
        if size is not None and 0 < size <= MAX_BODY_BYTES:
            try:
                self.rfile.read(size)
            except OSError:
                pass

    def _authorized(self, *, post: bool) -> bool:
        host = self.headers.get_all("Host", [])
        origin = self.headers.get_all("Origin", [])
        if host != [self.server.authority] or (origin != [self.server.origin] and (post or origin)):
            if post:
                self._discard_small_body()
            self.send_error(403)
            return False
        if self.path != "/":
            if post:
                self._discard_small_body()
            self.send_error(404)
            return False
        return True

    def _page(self, result: LearningActionResult):
        status = 409 if result.error in {"STALE_CONTEXT", "STALE_SUBMISSION"} else 400 if result.error else 200
        self._send(status, render_page(result, self.server.csrf), "text/html; charset=utf-8")

    def do_GET(self):
        if self._authorized(post=False):
            state = self.server.state
            result = apply_learning_action(self.server.fixture, state,
                                           LearningAction(action="WHY_CURRENT", revision=state.revision))
            self._page(result.model_copy(update={"recognized_action": None}))

    def _form(self) -> dict[str, str] | None:
        length = self._body_length()
        if length is None:
            self.send_error(400)
            return None
        if length > MAX_BODY_BYTES:
            self.send_error(413)
            return None
        if self.headers.get_all("Content-Type", []) != ["application/x-www-form-urlencoded"]:
            self._discard_small_body()
            self.send_error(415)
            return None
        try:
            data = self.rfile.read(length)
            if len(data) != length or re.search(rb"%(?![0-9A-Fa-f]{2})", data):
                raise ValueError("INVALID_FORM")
            items = parse_qsl(data.decode("ascii"), keep_blank_values=True, strict_parsing=True,
                              encoding="utf-8", errors="strict", max_num_fields=5)
            form = dict(items)
            if len(form) != len(items):
                raise ValueError("AMBIGUOUS_FORM")
        except (ValueError, TimeoutError):
            self.send_error(400)
            return None
        if not compare_digest(form.get("csrf", "").encode("utf-8"), self.server.csrf.encode("ascii")):
            self.send_error(403)
            return None
        return form

    def do_POST(self):
        if not self._authorized(post=True):
            return
        form = self._form()
        if form is None:
            return
        revision = form.get("revision", "")
        if re.fullmatch(r"[0-9]{1,10}", revision) is None:
            self.send_error(400)
            return
        fixture, state = self.server.fixture, self.server.state
        try:
            if form.keys() == {"csrf", "revision", "text"} and len(form["text"]) <= 80:
                result = apply_exact_alias(fixture, state, int(revision), form["text"])
            elif (form.keys() == {"csrf", "revision", "action"}
                  or (form.keys() == {"csrf", "revision", "action", "terminal"} and form["action"] == "TRY_TERMINAL")):
                action = LearningAction(revision=int(revision), action=form["action"], selection_id=form.get("terminal"))
                result = apply_learning_action(fixture, state, action)
            else:
                self.send_error(400)
                return
        except ValidationError:
            self.send_error(400)
            return
        except ValueError:
            self._send(409, f"{NOTICE}\nPREVIEW_CONTEXT_REJECTED")
            return
        if result.state is not None and result.error is None:
            self.server.state = result.state
        self._page(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="explicitly opt in to unreviewed Georgian wording")
    parser.add_argument("--host", choices=(HOST,), default=HOST)
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args()
    if not args.preview:
        parser.error("--preview is required for the PENDING_HUMAN_REVIEW wording")
    if not 0 <= args.port <= 65535:
        parser.error("--port must be between 0 and 65535")
    with LessonServer(reviewed_lesson(), args.port, preview=args.preview) as server:
        print(f"{server.origin}/", flush=True)
        print(NOTICE, flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
