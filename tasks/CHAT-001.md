INVENTOR EDU — CHAT-001
Evidence-Grounded Georgian Interactive Learning Session (Local Preview)
Task ID: CHAT-001
Revision: 1 — OWNER-FROZEN EXPERIMENT
Project: INVENTOR EDU
Repository: D:\Inventor_EDU
Remote: https://github.com/donluka-23/Inventor_EDU.git
Predecessor: origin/codex/edu-001-grounded-feedback
Expected predecessor SHA (verified at handoff preparation): 291b0c31a1fdf9f86451ec6bcfa6ec126b1a5439
New task branch: codex/chat-001-local-learning-session
Authority: This frozen task plus accepted repository governance. Research documents are context/evidence, not additional Codex instructions.
Result restriction: TEST_ONLY_NOT_PRODUCTION and PENDING_HUMAN_REVIEW throughout.
1. What this session must deliver
Turn the already working EDU-001 headless before/after engineering feedback into one genuinely interactive, local, Georgian learning session, not another scripted transcript or a generic chat model.

The user must be able to open a local browser page, examine a real failed GPIO connection, ask one of a bounded set of supported questions, inspect the exact evidence behind a finding, select an alternative physical contact, execute fresh CAP/SYN/CORE/B/EDU computations, and see the new scoped result and the old hint's withdrawal.

There is no LLM, provider connection, general language parser, arbitrary circuit input, user database, electrical simulation, firmware execution, or new fact acquisition in this task.

The product-value increment is observable interaction: a learner makes a choice and receives a real recomputed engineering explanation. A static chat mockup, a translated error-code list, or a fabricated conversation transcript fails.
Non-negotiable known state
EDU-001 is PARTIAL, not fully accepted. Its 110 reported tests and source-grounded computation passed, but the ka-GE wording is an unreviewed preview. Do not promote it to an approved educational corpus. Retain the current fail-closed behavior: rendering requires explicit preview authorization and output visibly says PENDING_HUMAN_REVIEW.

The entire UI is an experiment, not the previously deferred DEMO-002 framework decision, a production interface, or authorization to begin the 2D editor.
2. Mandatory baseline and independent preflight
1. Read AGENTS.md, docs/DECISION_AUTHORITY.md, docs/SESSION_PROTOCOL.md, docs/OSS_POLICY.md, docs/VERIFICATION_POLICY.md, docs/DECISIONS.md, docs/STATUS.md, tasks/NEXT.md and docs/prototype/MASTER_PLAN.md.
2. Fetch the exact predecessor branch and verify SHA. If it differs, identify the delta; do not silently rebase onto main.
3. Confirm the four archived Research F–I files remain tracked and unchanged; do not reinterpret or restage them. Research J is not automatically present in this branch; do not generate a substitute.
4. Read actual public APIs and tests in:
   - inventor_edu/models.py, core.py, gpio_facts.py, gpio_verify.py;
   - inventor_edu/capability_discovery.py, synthesis.py, educational_feedback.py;
   - examples/edu001_learning_cycle.py;
   - docs/prototype/EDUCATIONAL_FEEDBACK_CONTRACT.md;
   - reports/EDU-001-REPORT.md, reports/CAP-001-REPORT.md, reports/SYN-001-REPORT.md;
   - reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md.
5. Inspect the actual Georgian TEMPLATE_VERSION = 'ka-GE/edu-001-v1', current build_educational_feedback/`transition_feedback` signatures, and the preview gate. Read only the necessary sections of Research H and I to confirm already-approved boundaries; do not derive new architectural decisions from them.
6. Produce a short BOOT BRIEF with observed facts and contradictions before writing code.
No hidden approvals
The repository's master plan 1.3 currently lists DEMO-002 as deferred and EDU-001 as ENGINEERING VERIFIED / GEORGIAN WORDING REVIEW PENDING.

This handoff grants a single explicit exception for a disposable local learning-chat preview, using Python standard library and a tiny embedded HTML/CSS view. It does not authorize adoption of a frontend framework or changes to the long-term interactive editor architecture. Record this narrow exception in master plan revision 1.4, and nothing more.
3. Exact functionality
3.1 Scenario
Use the documented test-only ESP32-DevKitC-32E V4 / Adafruit #3942 HC-SR04 profile, with the existing independent catalog and GPIO fact-set pins.

Initial fixture state:
- sensor/Trig → board/J2.5 (GPIO34), known OUTPUT_NOT_CAPABLE failure.
- sensor/Echo → board/J3.8 (GPIO19), supported input-direction scope; electrical compatibility NOT_EVALUATED.
The initial exact contacts are permitted as scenario fixture data only, not in a generic engine or hardcoded explanatory text.

Show the real primary educational hint. Every engineering sentence must come from the current EducationalFeedbackReport or its explicitly linked immutable source bindings and raw verifier records.
3.2 Supported chat-like interactions
Provide visible Georgian quick actions corresponding to exact, typed intent/action IDs:
- WHY_CURRENT — display the current primary hint and the exact applicable rule/status.
- SHOW_EVIDENCE — show the real claim/source URL, edition/revision, locator, rule, terminal and snapshot references; do not invent citations.
- SHOW_UNVERIFIED — show active UNKNOWN / NOT_EVALUATED findings/coverage, including electrical, board-resource and firmware limitations.
- LIST_TERMINALS — display CAP-discovered, physically referenced candidates and their scoped status (KNOWN_UNSUITABLE, UNRESOLVED_EVIDENCE, FUNCTION_CONFIRMED_FOR_STATED_CHECK). Do not call any candidate globally safe.
- TRY_TERMINAL — select an existing, explicitly shown physical terminal candidate, construct a new constrained SYN request, actually rerun synthesis/CORE/B, then use transition_feedback to update current hints. Never merely change the displayed label.
- WHY_CHANGED — explain the actual difference between old and new outcomes from old/new immutable reports and withdrawn hint IDs. If no successful transition exists, state that clearly.
- SHOW_BOOT_CONTEXT — show a true BOOT_STRAP_CONTEXT finding only if existing EDU/B behavior has explicitly invoked the check for the selected terminal, its source facts and operating conditions; otherwise state NOT_REQUESTED / NOT_ESTABLISHED and make no boot-safety claim. Do not infer boot behavior from a GPIO number or pin name.
- RESET_LESSON — restore the initial fixture state with a fresh deterministic state transition.
A limited chat-text input may recognize only an explicitly listed handful of exact Georgian commands/aliases mapping to these IDs. Unsupported free text receives a neutral UNSUPPORTED_INTENT message with available actions. No LLM fallback, semantic similarity, or claim that arbitrary engineering questions are understood. The buttons alone must offer a complete usable path.
3.3 Candidate selection must be real
Derive the selection choices from actual CAP discovery and actual SYN candidate enumeration. An allowed choice must belong to the current, pinned, reviewed fixture's domain; server must independently validate the selected exact terminal/assignment reference.

For TRY_TERMINAL, do not trust an HTTP-provided verdict, finding ID, snapshot hash, evidence claim or source text. Resolve the user-selected terminal against current server-owned state, build a new request and run the existing methods. Reject stale or forged choices.

A PHYSICAL_CAPABILITY=PASS for GPIO18 is only a function-specific PASS. Keep BOARD_AVAILABILITY=UNKNOWN, ACTIVE_CONFIGURATION=UNKNOWN and ELECTRICAL_COMPATIBILITY=NOT_EVALUATED. If a user selects GPIO0, do not label startup behavior safe; the applicable, separately invoked existing BOOT_STRAP rule must be disclosed when evaluated, otherwise boot context remains unestablished.
3.4 Chat-facing data model
Introduce the fewest immutable application-level DTOs needed for a session view, for example:
- LearningSessionState: session revision, current request/assignment and snapshot digest, current feedback report, optional last transition, test-only scope.
- LearningAction: an allowed action ID plus optional selected canonical terminal reference; no freeform technical claims.
- LearningMessage: role (learner/`system`), message kind (explanation/`evidence`/`qualification`/`error`), linked current snapshot and raw engineering refs, Georgian text reused from EDU-001 where factual.
- LearningActionResult: updated state, rendered transcript messages, recognized action, validation/error status, and explicit preview restriction.
These are conceptual responsibilities, not permission for a broad ontology. Reuse existing EducationalFeedbackReport, FeedbackTransition, GpioFinding, GpioCoverage, RoleTrace, SourceBinding, TerminalRef, and the existing CORE/SYN/CAP types. Do not serialize duplicate engineering truth.
3.5 Human-language review boundary
EDU-001 Georgian wording remains PENDING_HUMAN_REVIEW.
- The browser must display a prominent persistent TEST_ONLY_NOT_PRODUCTION · ქართული ტექსტი დაუმტკიცებელია marker.
- The preview must require explicit --preview opt-in; without it the process must fail closed with a clear explanation rather than silently enabling unreviewed text.
- Do not change localization_review, TEMPLATE_VERSION, or the existing preview_unreviewed_ka gate.
- Codex may compose neutral interaction labels (e.g., „მაჩვენე წყაროები“, „სხვა კონტაქტის შემოწმება“), but must not invent engineering statements or modify EDU-001 technical claims.
- Prepare a separate review packet listing every currently reachable ka-GE template key, exact draft text, allowed rule/status/reason, example grounded bindings, uncertainty wording, and reviewer decision fields (APPROVE / CORRECT / REJECT, reviewer/date/notes).
- Leave all reviewer fields blank and all approval status pending. Codex cannot self-certify independent human review or fabricate an owner signature.
- Production use remains blocked until the owner separately approves an actual qualified-language review and a dedicated implementation task applies it.
4. UI implementation boundary (only this experiment)
Build a minimal browser-accessible, local-only preview with no new pip/npm dependencies:
- Use Python 3.12 standard library, e.g. one small http.server-based adapter and an HTML/CSS template stored within the allowed new preview module or a separate explicitly allowed local static template.
- Bind only 127.0.0.1, on an ephemeral or explicit loopback port. Do not bind to 0.0.0.0, publish to a cloud host, or add deployment configs.
- Keep session state in memory for one local demonstration. No account creation, cookies holding engineering claims, external analytics, telemetry, database or user-data persistence.
- Render Georgian text as actual UTF-8, with escaping for all dynamic fields, including source labels, original text and URLs. URL links must be derived unchanged from trusted source bindings and checked as http(s); never interpolate raw HTML.
- Require exact whitelisted action IDs, small bounded request bodies and server-controlled candidate IDs; reject malformed/unknown actions, query strings and fake PASS claims.
- For browser POSTs, enforce loopback Host / allowed Origin, a per-process CSRF token, and no cross-origin resource access; use Cache-Control: no-store and a restrictive Content-Security-Policy compatible with the minimal static page. This is still a local test utility, not audited web security.
- Do not use dynamic evaluation, script CDNs, web APIs, network search or external services.
- Prefer server-rendered forms/requests and straightforward keyboard-accessible controls. A page reload after each action is acceptable if current state, focus and errors remain clear.
- No 2D editor, drag/drop wiring, chart, tool calling or general chat framework.
- Visual clarity matters: distinguish FAIL, PASS FOR STATED CHECK, UNKNOWN, and NOT_EVALUATED in words, not color alone. Evidence/unknowns remain expandable and never hidden behind an overall green badge.
If safe use of the standard library local HTTP path cannot meet these minimal requirements, mark LOCAL_UI_BLOCKED, still deliver and test the deterministic headless action controller, and document the precise blocker. Do not install a frontend dependency or choose a permanent UI architecture.
5. Scientific and engineering guardrails
The educational mechanism is the already selected Research H limited constraint-based / model-tracing and formative-feedback approach: one primary anchored hint, a concrete user action, source evidence, remaining unknowns, and an independent recomputation. Research I supplies exact component/evidence constraints. Do not treat these references as empirical proof of improved learning outcomes in INVENTOR EDU.

Must not happen:
1. A UI message claims a circuit is safe or build-ready based on GPIO direction.
2. An unknown/missing rule appears as a valid engineering PASS.
3. A GpioCoverage(NOT_EVALUATED) becomes a GpioFinding(PASS).
4. The UI treats the CAP board-only snapshot's B findings as the generated two-component circuit's findings.
5. An old hint is displayed as active after a terminal change.
6. A user-supplied finding/source/snapshot digest becomes trusted without server-side regeneration.
7. An unreviewed Georgian template becomes APPROVED by code/default.
8. An absent manufacturer fact is replaced by a plausible statement or a textbook rule without provenance.
9. Code name-specific checks (gpio34, gpio18, esp32) are embedded in the generic session controller. Such names are permitted in pinned fixtures and tests only.
10. A successful demo is described as successful learning transfer, physical safety, or full firmware/electrical validation.
No CORE, B, CAP, SYN, EDU rule/DTO/validator modification is authorized. If the existing EDU contract is insufficient for safe action transitions, report the exact contradiction and ask for an owner decision instead of changing the verifier or silently weakening its gates.
6. Acceptance tests: pre-registered, independent oracles
Implement targeted tests with real CORE/CAP/SYN/EDU fixture calls; no mocked PASS/finding oracle as sole success measure.
ID	Acceptance condition
C01	Local preview starts only when --preview explicitly supplied; without it no UI exposing unreviewed template text starts.
C02	Initial learner view displays actual GPIO34 OUTPUT_NOT_CAPABLE finding and current snapshot ID.
C03	WHY_CURRENT displays EDU-001 real source-backed primary hint, not a new hardcoded hardware explanation.
C04	SHOW_EVIDENCE lists the actual GPIO claim IDs, source URLs, editions/locators and referenced current snapshot.
C05	SHOW_UNVERIFIED retains board availability/active configuration UNKNOWN and electrical NOT_EVALUATED.
C06	LIST_TERMINALS gets options from CAP and SYN; GPIO6 reserved and GPIO34 output-ineligible are distinguished.
C07	TRY_TERMINAL with J3.9 produces a fresh SYN/CORE/B evaluation, new snapshot and scoped output PASS; old failure hint is withdrawn.
C08	Changing to another allowed terminal updates current state and explains the actual observed result; no silent promotion to SAFE.
C09	Invalid, forged, stale or off-domain terminal IDs fail closed without mutating session state.
C10	WHY_CHANGED exposes old/new finding and snapshot references, never invents a correction if no transition exists.
C11	SHOW_BOOT_CONTEXT preserves genuine B BOOT_STRAP_CONTEXT statuses/prerequisites when applicable; never asserts boot safety from identity alone.
C12	RESET_LESSON restores the exact fixture and yields the same initial engineering verdict.
C13	Unsupported free text/command produces UNSUPPORTED_INTENT without engineering speculation or API calls.
C14	Changing source/factset/requirements/template pin makes old context stale or fails validation; no old hint is current.
C15	Forged PASS, swapped physical contact, fabricated claim ID, and stale snapshot from EDU-001 adversarial suite still fail.
C16	All user-originated strings are escaped; no arbitrary HTML/script insertion or arbitrary URL invocation.
C17	HTTP binds only loopback, rejects wrong Host/Origin and missing/invalid CSRF; state-changing actions require POST.
C18	All UI and controller results expose TEST_ONLY_NOT_PRODUCTION and PENDING_HUMAN_REVIEW, including JSON if one exists.
C19	The review packet includes every reachable template exactly, with no false review approvals.
C20	All pre-existing tests including EDU-001 and authentic GPIO source admission remain green.


Also run: deterministic same-event replay in two fresh processes; invalid UTF-8, very long body, duplicate action parameters, unknown action keys, repeated/stale submissions; browser GET/POST negative controls. Report measured runtime and resource use without fabricating targets or claiming broad performance.

Evidence standard: Show an actual 4-step captured interaction (initial failure → why/evidence → candidate selection → fresh result/withdrawal), exact current vs previous snapshot digests and corresponding raw B statuses. A scripted terminal output alone does not meet C07; demonstrate actual action-driven state transition through the local interface/controller.
7. Allowlist / forbidden modifications
Add only
- inventor_edu/learning_session.py — pure bounded, test-only chat-action controller.
- examples/chat001_local_preview.py — local-only HTTP/HTML preview entrypoint; HTML/CSS may be embedded or stored in examples/chat001_preview_template.html only if genuinely necessary.
- tests/test_chat001_learning_session.py — controller, adapter and HTTP acceptance tests.
- docs/prototype/CHAT001_LEARNING_SESSION_CONTRACT.md — exact APIs, statuses, local usage, no-safety guarantee.
- docs/reviews/EDU001_KA_WORDING_REVIEW_PACKET.md — unapproved textual review package, no signoff.
- tasks/CHAT-001.md — exact frozen handoff.
- reports/CHAT-001-REPORT.md — actual execution evidence.
Factual modifications only
- docs/STATUS.md
- tasks/NEXT.md
- tasks/WORK_LOG.md
- docs/prototype/MASTER_PLAN.md only to version 1.4 and to add CHAT-001 | local-only interactive learning preview | AUTHORIZED / TEST_ONLY / LANGUAGE_REVIEW_PENDING, while leaving DEMO-002/003/004/005 and all existing scopes NOT_AUTHORIZED. Preserve all fixed non-goals, opportunity register, risks, and change-control rules verbatim.
Strictly forbidden
- inventor_edu/models.py, core.py, gpio_verify.py, gpio_facts.py.
- inventor_edu/synthesis.py, capability_discovery.py, educational_feedback.py.
- Existing verified tests, catalogs, facts, source ledgers, upstream reports.
- Research F–I originals; inventing/mutating Research J.
- ADR acceptance, license/rights changes, dependencies/lock files, deployment and permanent frontend directories.
- Any general user-account, database, scraping, dataset ingestion, knowledge-base build or personal-history learning functionality.
If an existing interface requires a change to complete the task, do not touch it; report OWNER_DECISION_REQUIRED, preserve all functioning prior capabilities and deliver the safe subset with a PARTIAL classification.
8. Run and acceptance handoff
Propose a simple no-install Windows run command (actual CLI syntax must match source):
cd D:\Inventor_EDU
python -X utf8 -B -m examples.chat001_local_preview --preview --host 127.0.0.1 --port 0
The program must print the exact local URL/assigned port, then serve the interactive lesson until stopped. --port 0 requests a kernel-assigned ephemeral loopback port; never treat 0 as the user-visible final port.

A tester must be able to:
1. Open the URL.
2. Read the actual GPIO34 failure as a Georgian preview.
3. Click რატომ? and წყაროები to inspect the computation and provenance.
4. Inspect actual alternative contacts and select J3.9.
5. Observe new snapshot and scoped GPIO18 PASS, the original hint marked withdrawn, and the continuing UNKNOWN/NOT_EVALUATED obligations.
6. Return to the initial fixture with თავიდან დაწყება.
The demo may begin in a controlled failing state; never fabricate the actual subsequent engineering verdicts.
9. Required report and Git closure
reports/CHAT-001-REPORT.md must contain:
1. BOOT BRIEF, exact predecessor and task branch.
2. Verified existing APIs, baseline limitations and confirmation of the archived F–I research commits.
3. Exact added files and absence of unauthorized changes/dependencies.
4. Pure action-controller state machine and supported intent grammar.
5. Browser preview operation, loopback/CSRF/escaping controls, launch command.
6. Real generated chat transcript with before/after snapshot, raw B findings, source bindings, withdrawn hint IDs, and test-scope warning.
7. Named source of every factual statement in the interface; unsupported/question fallback.
8. Review packet manifest with PENDING_HUMAN_REVIEW retained; no claim of human approval.
9. C01–C20 independent acceptance and negative test results, exact commands and process exit codes.
10. Full regression and GPIO source-admission outputs.
11. Measurement method, latency and warnings, if any.
12. Remaining electrical, firmware, exact hardware revision, broader catalog, Georgian NLP and frontend limitations.
13. Architectural contradictions and narrowly scoped owner requests (if any).
14. Master-plan 1.4 diff limited to CHAT-001 and unchanged deferred frontend gates.
15. Git implementation commit SHA, push, and verified remote HEAD.
16. Final PASS_TEST_ONLY_PREVIEW / PARTIAL / BLOCKED recommendation. Never report the Georgian educational wording as fully accepted without independent review evidence.
Use git add with an explicit file allowlist; do not stage everything. Follow required repository session controls. Push only codex/chat-001-local-learning-session and verify remote SHA. Do not merge to main or start any further task.
Fail-fast criteria
STOP and report an owner decision if the UI can show forged or stale PASS, report unsupported electrical safety, bypass the pending language gate, require an upstream schema rewrite, or expose the local HTTP preview beyond loopback. A technically unsafe shortcut is not a successful prototype.
Final success condition
CHAT-001 is successful only if a real learner action through a local Georgian chat-style preview causes fresh existing-engine computations, produces a source-grounded and scoped explanation, visibly withdraws obsolete feedback, preserves all open obligations, and keeps both scientific/engineering trust and linguistic-approval boundaries intact.

Execute CHAT-001 only.