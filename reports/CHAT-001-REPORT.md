# CHAT-001 revision 1 execution report

- Session date — 2026-11-20, Asia/Tbilisi.
- Frozen task — [CHAT-001 revision 1](../tasks/CHAT-001.md).
- Recommendation — **PASS_TEST_ONLY_PREVIEW**. Actual loopback form interactions and engineering gates passed. Visual browser automation could not complete. The wording remains **PENDING_HUMAN_REVIEW**.
- Remote — `https://github.com/donluka-23/Inventor_EDU.git`.
- Verified predecessor — `origin/codex/edu-001-grounded-feedback` at `291b0c31a1fdf9f86451ec6bcfa6ec126b1a5439`.
- Task branch — `codex/chat-001-local-learning-session`.

## A. BOOT BRIEF and baseline

Fetched origin, verified the live predecessor SHA and clean worktree, then created the task branch. Verified `f66d9af3db5fad3de878fbad3d45b06ee77c4ea4` as an ancestor and matched all four tracked Research F–I blobs to the archival commit. Research J was unavailable locally. No substitute was created. Master plan 1.3 deferred DEMO-002. EDU-001 was PARTIAL with unapproved wording. Accepted ADR-0001 applies. ADR-0002 remains on hold. No upstream API change was required.

Read `AGENTS.md`, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/SESSION_PROTOCOL.md`, `docs/OSS_POLICY.md`, `docs/VERIFICATION_POLICY.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, `docs/prototype/MASTER_PLAN.md`, ADR-0001 and the evidence-gated-engineering skill. Inspected CORE, B, CAP, SYN, EDU, the EDU CLI, relevant existing tests, the EDU contract, EDU/CAP/SYN reports and the CORE-001B source/rule ledger. Read the relevant H/I feedback and evidence-boundary sections without adopting new research proposals.

The original `ka-GE/edu-001-v1` constant, `LearningContext.preview_unreviewed_ka`, `build_educational_feedback` and `transition_feedback` remained intact. The task's authorized writes covered the local controller and view, their tests and documentation, the frozen plan, and the specified factual tracking. The evidence gates were C01–C20, HTTP negative controls, full regression, authentic GPIO admission, and two real loopback form replays.

## B. Controller and local view

The public entry points are `start_learning_session(fixture, *, preview=False)`, `apply_learning_action(fixture, state, action)`, and `apply_exact_alias(fixture, state, revision, text)`. `LessonFixture` holds the catalog, facts, typed request, board/requirement identity, initial and fixed contacts, and independent pins. Frozen state holds the current narrowed request, actual SYN candidate, CAP-backed options, initial EDU report or last transition, prior reference, revision and context fingerprint. The typed result includes the recognized intent, error, and current state when available. Engineering findings, coverage, topology and source bindings use the existing types.

The controller recognizes WHY_CURRENT, SHOW_EVIDENCE, SHOW_UNVERIFIED, LIST_TERMINALS, TRY_TERMINAL, WHY_CHANGED, SHOW_BOOT_CONTEXT and RESET_LESSON. Exact text aliases are `რატომ?`, `წყაროები`, `რა არ ვიცით?`, `კონტაქტები`, `რა შეიცვალა?`, `ჩატვირთვა` and `თავიდან დაწყება`. All other text returns `UNSUPPORTED_INTENT` with the allowed actions still available. The text is discarded. TRY requires a server-owned selection ID. No engine runs for unsupported text or read-only views.

TRY and RESET rerun CAP discovery for the two roles, enumerate actual SYN assignments with Echo held fixed, and regenerate the selected assignment from a narrowed SYN request. CORE and B run in that path. EDU validates the current topology and replays B before producing the transition. A selection ID binds a session revision, the active snapshot and the server-enumerated assignment. Old revisions and old choice IDs reject. The context fingerprint covers the fixture records, pins, requirements, ruleset and template version. Context mismatches withhold active feedback.

The source of every engineering display is explicit. The primary Georgian explanation is the current EDU hint. Its provenance panel shows the corresponding finding/coverage reference and EDU-reviewed evidence bindings. The uncertainty panel uses active EDU hints and current raw B rows for the fixed Echo role. The contact list is labelled as the CAP board-only evaluation. Its controls exist only for contacts with enumerated SYN options. The change panel reads old and current engineering references and EDU withdrawal IDs. The boot panel reads EDU's separately invoked B result and prerequisites or the unestablished state.

The HTTP server binds only `127.0.0.1`, prints the assigned port, and keeps one session in memory. It serves `GET /` and exact form `POST /` requests. POST requires the exact loopback Host and Origin, the per-process CSRF token, a current revision, and whitelisted fields. The decoder accepts at most 2,048 bytes, five unique fields and strict UTF-8 form data. Dynamic HTML fields are escaped. Links come from source bindings and are eligible only with an HTTP(S) URL. Responses use `Cache-Control: no-store` and a restrictive CSP with a hashed stylesheet. There is no CORS permission, external resource loading, user persistence or network provider. Windows socket tests exposed resets when rejecting a small request while its body was arriving. Known-length small bodies on rejected Host/Origin, paths or content types are now discarded within the existing size and socket timeout bounds before sending the rejection. Oversized or ambiguously framed requests are rejected without draining their body.

## C. Captured interaction

The local server was launched as a real process. The capture made an initial GET and submitted the page's own forms over loopback, using its current CSRF and revision fields. Each response below was HTTP 200. This exercised the same route, form validation, controller and rendered response used by a browser. Browser automation could not complete. The in-app browser access host was unavailable and native automation stopped because the browser URL could not be established with sufficient confidence. No visual browser or human usability result is claimed.

| Event | Actual result |
| --- | --- |
| 1. GET initial page | `sensor/Trig → board/J2.5`, `PHYSICAL_CAPABILITY = FAIL / OUTPUT_NOT_CAPABLE`. Restriction marker included both `TEST_ONLY_NOT_PRODUCTION` and `PENDING_HUMAN_REVIEW`. |
| 2. POST **რატომ?**, then **წყაროები** | The same EDU failure and snapshot remained active. The source panel opened and displayed `board-J2.5`, `map-J2.5` and `silicon-GPIO34` with their original links and locators. |
| 3. POST **შეამოწმე board/J3.9** | The emitted option ID resolved to the enumerated candidate. The server regenerated the assignment and returned `PHYSICAL_CAPABILITY = PASS / CAPABILITY_CONFIRMED` for board/J3.9. |
| 4. Read fresh result and POST **რა შეიცვალა?** | The new snapshot and scoped hint remained current. The previous finding and snapshot appeared in the change panel with four `WITHDRAWN` hint IDs. Board availability and active configuration stayed UNKNOWN. Electrical compatibility stayed NOT_EVALUATED. |
| Reset | POST **თავიდან დაწყება** recomputed the initial fixture and returned its original canonical snapshot and output-direction failure. |

Actual primary Georgian responses:

> სქემაში sensor/Trig უკავშირდება board/J2.5 კონტაქტს (GPIO34). Trig სიგნალის გასაგზავნად დაფას სჭირდება გამოსასვლელი (GPIO_OUT). დოკუმენტირებული ვარიანტის მიხედვით GPIO34 ამ ფუნქციას ვერ ასრულებს.

> სქემაში sensor/Trig უკავშირდება board/J3.9 კონტაქტს (GPIO18). ACTIVE რეჟიმში გამოსასვლელის ფუნქციის შემოწმება (PHYSICAL_CAPABILITY) გავლილია.

| Field | Before | After |
| --- | --- | --- |
| Canonical snapshot SHA-256 | `b6ccc23eb87fe910d9127ec7dfdaef68e18aba243af4e9996c4b09abddbf2369` | `6fe1964503bdc98e1c3f82bd6c817ed92d0cef800b73734c7c11518d10a1a230` |
| Raw B physical capability finding SHA-256 | `3f797ff0ed2bd36510d2f6c23e7262cc1c17f942da47b21283fbd57c386d4b33` | `0b4a491805ae97648c107dc6951a7a9bf7abc3a0116e31d8081b318b47078050` |
| Board availability | UNKNOWN / EVIDENCE_MISSING | UNKNOWN / EVIDENCE_MISSING |
| Active configuration | UNKNOWN / ACTIVE_CONFIG_UNKNOWN | UNKNOWN / ACTIVE_CONFIG_UNKNOWN |
| Electrical compatibility | NOT_EVALUATED / ELECTRICAL_CHECK_DELEGATED | NOT_EVALUATED / ELECTRICAL_CHECK_DELEGATED |

The captured withdrawn SHA-256 IDs were `d3fe3cf60c3160d578c7face13dc20f43cf4b7c3c2f50ce63e014f9bf8af4e7c` (primary), `7b35a7195aa371b47f34c64d2ded117bdf7a79e560996bc4002f4bd9f41aa1b7`, `b897a90ae53330bc1aa71cd97ad78a322d91f58ed07e18b642ba34dba90d90d1` and `f2d44b18dd228bca63e7914d25a40fa354deccc0b04dd4ee3c355c926259ec9e`.

The source panel used S18 at `Header Block, J2 row 5`, B's `map-J2.5` at `Header Block J2.5; ordering row -32E`, and `silicon-GPIO34` at its inherited mask/summary locator. The result for J3.9 bound `board-J3.9`, `map-J3.9`, and `silicon-GPIO18` to its new report. The source editions, revisions and URLs were taken from the existing bindings. The controller also exercised J3.19, retaining its real board reservation FAIL and distinct physical direction PASS. J3.14 produced a separate `BOOT_STRAP_CONTEXT / UNKNOWN / BOOT_STRAP_CONDITIONS_UNKNOWN` at RESET with `strap-gpio0` and the three recorded prerequisites. The ordinary J2.5 state had `NOT_ESTABLISHED` boot context.

## D. Acceptance and negative controls

| ID | Independent evidence | Result |
| --- | --- | --- |
| C01 | CLI without preview and CLI with non-loopback host both exit 2 before binding. Direct preview constructor also requires opt-in. | PASS |
| C02 | Initial HTTP page contains the known raw failure, actual snapshot and restriction. | PASS |
| C03 | WHY_CURRENT returns the real EDU text and exact anchored reference. | PASS |
| C04 | Sources form opens the pane with actual claim IDs, URL, revisions, locator and snapshot. | PASS |
| C05 | Open statuses remain UNKNOWN or NOT_EVALUATED, including on Echo. | PASS |
| C06 | Five CAP contacts shown. Reservations and direction failure distinguished. The held Echo contact cannot be selected for Trig. | PASS |
| C07 | Submitted an actual generated J3.9 choice to the running local server. New canonical snapshot, current B PASS and withdrawn prior hint verified. | PASS via HTTP forms |
| C08 | J3.19 generated a distinct snapshot and real board reservation FAIL. | PASS |
| C09 | Forged token, off-domain contact and old revision/token reject without state mutation. | PASS |
| C10 | WHY_CHANGED shows both actual references after a transition and a neutral empty state before it. | PASS |
| C11 | Separate B RESET finding preserves UNKNOWN, exact prerequisites, scope and reviewed claim. | PASS |
| C12 | RESET submits a new revision and re-creates the original snapshot and verdict. | PASS |
| C13 | Exact aliases recognized. Unsupported text returns UNSUPPORTED_INTENT and makes no engine call. | PASS |
| C14 | Source edits, wrong pins, changed requirements, ruleset or template suppress stale context. | PASS |
| C15 | HTTP rejects spoofed engineering fields. All four predecessor EDU adversarial controls pass in the full suite. | PASS |
| C16 | Unsupported text is not reflected. Markup escapes and a non-HTTP(S) source produces no link. | PASS |
| C17 | Loopback socket, Origin, Host, token, GET/POST boundary and CSP verified over HTTP. | PASS |
| C18 | Both restrictions appear in responses and controller records. | PASS |
| C19 | Ten original EDU drafts verified against live generated strings. Decision, reviewer, date and notes fields are blank. | PASS |
| C20 | 127 tests passed and the independent source-admission gate passed. | PASS |

Malformed UTF-8 and percent escapes, oversized bodies, duplicate fields, unsupported actions and extra keys were rejected. Repeating the previously successful mutation returned `409 STALE_SUBMISSION`. Invalid Host/Origin, missing or bad CSRF, disallowed query strings and unsupported methods could not change the lesson.

## E. Reproduction and measurements

Commands ran in `D:\Inventor_EDU` with Python 3.12.8 and the existing locked runtime and test packages.

```powershell
$exe=Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$src=Join-Path $env:TEMP 'InventorEDU-CORE-001B-01-sources'
$env:INVENTOR_EDU_DATA001_SOURCE_DIR=Join-Path $env:TEMP 'InventorEDU-DATA-001-dc037a238eb5efcc034dd9d62e5775d5c21e90e4'
$env:HYPOTHESIS_STORAGE_DIRECTORY=Join-Path $env:TEMP 'InventorEDU-CHAT-001-hypothesis'
& $exe --version
& $exe -m pip list --format=freeze
& $exe -B -m unittest tests.test_chat001_learning_session -v
& $exe -B -m unittest discover -s tests -v
& $exe -B -m tests.gpio_source_acceptance $src
& $exe -X utf8 -B -m examples.chat001_local_preview --preview --host 127.0.0.1 --port 0
```

```text
Ran 17 tests in 3.369s
OK
Ran 127 tests in 7.598s
OK
PASS: five authentic artifacts matched pins; masks, pull-up, header, flash, strap and -32E scope checked
```

Targeted, full and authentic admission commands exited 0. The full suite had zero failures, skips or blocked methods, including all four authentic DATA tests. Earlier development runs surfaced three assertions that incorrectly required Pydantic object identity despite identical immutable values, and Windows socket aborts during rejecting unread requests. The tests now assert semantic equality and the server returns stable rejection for small unauthorized submissions. An initial capture pipeline also required explicit UTF-8 PowerShell input encoding for its Georgian form labels. The recorded final runs passed.

The replay harness launched the preview command in two fresh processes. It measured launch and loopback round trips using Python `perf_counter`, parsed the actual forms, and hashed a JSON sequence of all six response bodies with only the generated CSRF token normalized. Both processes produced SHA-256 `4237f48a61811c5f7e2a6bff4692369f3ba132a85d43a0c357fddf30d562d20c`. The kernel assigned ports 62438 and 62454. Startup took 555.1 ms and 502.8 ms. The J3.9 form took 94.7 ms and 89.7 ms. Reset took 96.2 ms and 81.2 ms. Response bodies ranged from 13,378 to 15,111 bytes. `tracemalloc` measured 433,553 current and 1,010,019 peak tracked Python heap bytes across separate in-process initialization and choice. This excludes native allocations and HTTP process baseline. The harness exited 0. It explicitly terminated each long-running child afterward, which returned exit 1 on this host with zero stderr bytes. These observations describe only the local fixture.

## F. Manifest, wording and limitations

| Path | Change |
| --- | --- |
| `inventor_edu/learning_session.py` | Added bounded immutable controller |
| `examples/chat001_local_preview.py` | Added loopback server and embedded static view |
| `tests/test_chat001_learning_session.py` | Added 17 controller/HTTP/wording methods covering the gates |
| `docs/prototype/CHAT001_LEARNING_SESSION_CONTRACT.md` | Added APIs, usage, statuses and scope |
| `docs/reviews/EDU001_KA_WORDING_REVIEW_PACKET.md` | Added ten original draft entries and blank review fields |
| `tasks/CHAT-001.md` | Added the frozen handoff byte-for-byte |
| `reports/CHAT-001-REPORT.md` | Added execution and publication evidence |
| `docs/STATUS.md`, `tasks/NEXT.md`, `tasks/WORK_LOG.md` | Updated factual status and pending review |
| `docs/prototype/MASTER_PLAN.md` | Changed 1.3 to 1.4 and added only the authorized CHAT row |

Verified all other master-plan content, including deferred frontend gates, fixed non-goals, opportunities, risks and change control, against the predecessor. Existing code, tests, catalogs, source ledgers, historic reports, research, governance and dependencies were preserved. There are no new dependencies and no terminal-specific checks in the session controller.

The [wording packet](../docs/reviews/EDU001_KA_WORDING_REVIEW_PACKET.md) preserves all ten inherited draft keys, exact template wording, allowed bindings and uncertainties. The method remains one anchored formative hint with evidence and a fresh recomputation. No empirical learning outcome or Georgian language approval was established. Independent qualified-language review and separate owner approval remain pending. Exact physical hardware revision, electrical compatibility, firmware behavior, wider catalogs, general Georgian NLP, and the permanent frontend remain outside this preview. No architecture or upstream contract decision was needed to publish the tested local subset. Owner review remains pending.
