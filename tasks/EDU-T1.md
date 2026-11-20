INVENTOR EDU — EDU-T1
Independent GPIO Transfer Check in the Existing Georgian Learning Preview
Task: EDU-T1
Revision: 1 — OWNER-FROZEN UPON OWNER SUBMISSION TO CODEX
Authority: Owner and research conversation decide; Codex executes one task only.
Repository: D:\Inventor_EDU
Remote: https://github.com/donluka-23/Inventor_EDU.git
Required predecessor: origin/codex/core-001c-e2-divider-topology
Expected predecessor HEAD at task preparation: 486af81b4c38253927ba0bfe2572fb0fa43785f9
New task branch: codex/edu-t1-independent-transfer
Output: One real interactive, source-grounded, independent near-transfer exercise in the existing loopback lesson; a reproducible test run and an exhaustive Markdown report.
Authorization: This document authorizes no separate architecture decisions, general curriculum rewrite or subsequent task. Stop with OWNER_DECISION_REQUIRED if an exact conflict cannot be handled within the frozen scope.
1. Why this is the next bounded product capability
Currently the local CHAT-001 preview lets a learner fix the known sensor/Trig → board/J2.5 GPIO output-direction failure by selecting board/J3.9; EDU explains the current rule, shows provenance, and withdraws stale guidance. That is a guided correction, not evidence that the learner can transfer the concept independently. EDU-T1 adds one fresh assessment of the learner's ability to reason about input vs output and the difference between scoped direction support and complete electrical safety.

It must create observable learner value, not merely add an assessment model or more tests. The user must be able to complete the exercise in the existing browser-based loopback preview without manually editing source code or calling a separate CLI.

Research authority: Research K identified unhinted near-transfer, worked-example fading and clear separation of learner evidence from engineering verification as bounded educational options. This task adopts only an independent near-transfer check. The wider independent Research K2 investigation is unfinished for implementation purposes: do not infer, build or approve three learning routes, universal lesson architecture, mastery scoring or knowledge tracing. Engineering source and evidence remain as currently admitted by CORE/B; pedagogical research never becomes a device fact.
2. Precisely bounded experience
Practice stage — existing UI unchanged:
1. Learner sees Trig → board/J2.5 with real PHYSICAL_CAPABILITY=FAIL/OUTPUT_NOT_CAPABLE, and a Georgian, preview-only explanation.
2. Learner chooses board/J3.9 through the existing server-issued current option. CHAT/CAP/SYN/CORE/B/EDU perform their existing recomputation. Only Trig direction PASS is established; other scopes remain UNKNOWN/NOT_EVALUATED.
3. Only after this new, real role-correction transition and a current actual Trig PHYSICAL_CAPABILITY=PASS with no hard FAIL for that Trig role does a control appear to start „დამოუკიდებელი შემოწმება“. Do not treat a passive page load, hints viewed, an incorrect training choice, or a user-supplied flag as completing practice.
Independent transfer stage — new:
4. The learner receives a distinct prompt: „ახლა დაფამ სენსორის Echo სიგნალი უნდა წაიკითხოს (GPIO_IN). მოცემული ორი კონტაქტიდან რომელს არ აქვს ცნობილი აკრძალვა ამ როლისთვის მიმდინარე შემოწმებებში?“
5. Present exactly two neutral selectable physical contacts, board/J2.5 and board/J3.19, in one fixed documented ordering; no qualification, PASS, FAIL, reserved-resource explanation, highlighted recommended choice or underlying report may appear before submission. Hide the training-stage sidebar/option descriptions, prior source panel, and current practice findings while the transfer screen is active; otherwise the existing practice UI leaks the reserved-contact answer. The former Trig exercise has already taught that J2.5 cannot output: transfer assesses whether the learner understands that an input demand differs. J3.19 is a reserved resource even if silicon direction is supported.
6. Ask one explicit scope-calibration question before feedback: „თუ GPIO_IN ფუნქციის შემოწმება გავლილია, ამტკიცებს ეს Echo-ს ელექტრულ თავსებადობას?“ Allowed answers: არა or დიახ. Both answers are required before submission.
7. On submit, use real CORE/CAP/SYN/B outputs on a fresh transfer circuit, not display strings, to establish the exact check statuses. The transfer circuit has the same exact reviewed catalog/factset, sensor/Trig fixed to board/J3.9 and sensor/Echo assigned to the user's chosen physical input contact. The accepted roles remain TRIG_OUTPUT/`ECHO_INPUT`, GPIO_OUT/`GPIO_IN`, ACTIVE. No new circuit engine is authorized.
8. Result shows: the learner's selected contact, actual evaluated rule statuses and physical anchor, an explanation of whether the scoped choice was supported, and the continuing BOARD_AVAILABILITY=UNKNOWN, ACTIVE_CONFIGURATION=UNKNOWN, ELECTRICAL_COMPATIBILITY=NOT_EVALUATED or applicable FAIL/coverage, with actual source bindings where already available. It explicitly distinguishes the independent learning result from hardware acceptance.
9. A single attempt receives one assessment outcome and cannot be silently regraded after viewing the answer. Resetting the whole lesson starts a new local attempt without persisting learner answers. Repeated submissions and stale forms must reject without changing the stored result.

Freeze exactly one assessment item. Do not create a quiz bank, random quiz generator, user model, three-entry navigation or general Georgian natural-language parser.
3. Engineering and scoring authority
- No hardcoded engineering truth: J2.5 and J3.19 are explicit test fixture options, not general rules of GPIO. The scoring algorithm must determine suitability by freshly evaluated B findings for GPIO_IN, rather than if selected == "J2.5": correct.
- The expected fixture result is: board/J2.5 / GPIO34 is an input-capable contact with a scoped PHYSICAL_CAPABILITY=PASS; it has no known hard FAIL in the selected checked scope, but further obligations remain open. board/J3.19 / GPIO6 has BOARD_AVAILABILITY=FAIL/RESERVED_RESOURCE, even though its direction check may PASS.
- Compute the transfer on an exact current CircuitSnapshot with real sensor/Echo → selected board contact and sensor/Trig → board/J3.9 conductors and real topology. The fixed Trig role must stay distinct; no terminal reuse and no forged findings.
- The answer to the second question is არა, because the GPIO direction result cannot establish 5 V Echo electrical compatibility, source drive, supply or full system safety.
- TRANSFER_CORRECT_IN_SCOPE is permitted only if the learner selected a candidate with actual direction PASS, no known hard FAIL for that role, and answered the scope question არა. TRANSFER_INCORRECT covers the opposite case. Any mismatched catalog/factset pins, stale source versions, unsupported role, missing checker coverage or incomplete input must yield TRANSFER_UNAVAILABLE or explicit validation error without awarding correctness.
- Return structured assessment evidence including the current catalog, factset and snapshot digests; exact chosen TerminalRef; raw B reference IDs/statuses and separate coverage; actual assessment item/version; result and TEST_ONLY_NOT_PRODUCTION; Georgian text remains PENDING_HUMAN_REVIEW.
- Assessment correctness is learner evidence, never a new GpioFinding, manufacturer EvidenceClaim, SAFE, whole-project PASS, skill MASTERED or psychometric probability. Do not write learner responses into engineering knowledge stores.
- Before answer submission do not expose an answer-key, debug hints, source-linked correctness badges or selectable list filtered to only the correct contact. Prevent source/status leakage via any browser-visible HTML field.
4. Frozen architecture and interfaces
The implementation may add an isolated, read-only assessment adapter that consumes the already existing public LessonFixture, LearningSessionState, SynthesisRequest, CAP-001, SYN-001 and B/CORE outputs. Keep a typed, immutable assessment item/state/result with explicit context fingerprint, training session revision, current fixture digests, an attempt/answered marker and separate academic/electrical statuses.

Codex may choose internal function names only within the new adapter. The externally observable contract and stated DTO fields, not internal method names, are frozen. Use existing Pydantic Record, TerminalRef, Digest and public verifier/model APIs. No new external library, database, router framework, JS runtime, LLM, simulator or generalized course ontology.

The local LessonServer may keep the new assessment state in memory only and extend the existing GET / / POST / forms. Preserve existing exact loopback Host/Origin, CSRF, server-issued selection token, revision guard, strict form grammar, payload limit, HTML escaping, no external assets and CSP policy. A new assessment submission must never be allowed to send client-controlled raw engineering findings, arbitrary source claims, net IDs, catalog digests, GPIO capabilities or rule statuses. Use server-issued current choice IDs with constant-time comparison where appropriate. If a user changes the practice snapshot or resets the lesson, discard/invalidate the pending transfer attempt.

Existing ordinary text aliases and commands must keep their current behavior. Unsupported free text remains UNSUPPORTED_INTENT and is not stored. The assessment renders with TEST_ONLY_NOT_PRODUCTION and PENDING_HUMAN_REVIEW on initial, in-progress and result screens. No sign-off may be fabricated.

Special condition: This change must not accidentally run the current EDU tutoring hints for the transfer case and expose them pre-answer. It is fine to compute B internally; it is not fine to render raw truth before scoring.
5. Allowlisted changes
New:
- inventor_edu/transfer_assessment.py — immutable, grounded independent-assessment DTOs, preparation and scoring.
- tests/test_edu_t1_transfer.py — independent positive, negative, adversarial, and real HTTP acceptance tests.
- docs/prototype/INDEPENDENT_TRANSFER_T1_CONTRACT.md — exact interaction, API, assessment/scope semantics and reproduction.
- tasks/EDU-T1.md — exact owner-frozen task.
- reports/EDU-T1-REPORT.md — exhaustive execution report.
Modify only for necessary integration:
- examples/chat001_local_preview.py — small extensions to the existing loopback page and form handler for launch, submission and evidence-backed outcome.
- docs/STATUS.md, tasks/NEXT.md, tasks/WORK_LOG.md — strictly factual status and task tracking.
- docs/prototype/MASTER_PLAN.md — narrowly append EDU-T1 authorized test-only milestone and bump to 1.7; preserve all existing gates, deferred milestones and restrictions.
Read-only / forbidden: inventor_edu/models.py, core.py, gpio_facts.py, gpio_verify.py, synthesis.py, capability_discovery.py, educational_feedback.py, learning_session.py, demo_bridge.py, divider_topology.py, voltage_model.py, all existing tests, catalog/evidence files, Research F–I, Research J/K/K2, existing reports and ADRs, requirements/locks, OSS policies and the legacy main branch. Research K/K2 may be used as context but does not authorize implementation beyond this task. In particular, never invent or commit a missing local research file.

If the observable experience cannot be implemented without editing a protected module or expanding this allowlist, stop with OWNER_DECISION_REQUIRED; do not implement a workaround that duplicates verification authority.
6. Mandatory independent acceptance gates (T1-01 through T1-20)
1. Preflight: exact predecessor branch/SHA, origin, clean working tree, F–I archival ancestry and correct source pins checked; no silent local overwrite.
2. Browser starts on existing GPIO34 Trig failure, existing Georgian preview hint and both restrictions; original CHAT functionality remains.
3. Assessment cannot start just by visiting the page or inventing an action; require a real recorded training correction through the CHAT engine.
4. Start transfer produces the distinct ECHO_INPUT role demand and fixed TRIG_OUTPUT on J3.9; exact reviewed catalog/factset and source pins reused without modification.
5. Before submission, HTML contains the two neutral physical contact labels but no B qualification, answer key, PASS/FAIL, reserved-resource reason or source disclosure for the transfer case; the previous practice/sidebar panes must not leak the answer into the assessment HTML, including collapsed/hidden HTML sections or attributes.
6. Server-issued choice token binds the training revision, source/current snapshot, item version and exact option, and rejects forged/stale/duplicate tokens.
7. Both questions are required, with explicit limited allowed answer values. Missing/extra/duplicate form fields and malformed encoding reject.
8. Submitting J2.5 plus არა yields TRANSFER_CORRECT_IN_SCOPE from real ECHO_INPUT B results; no invented global safety.
9. Submitting J3.19 plus არა yields TRANSFER_INCORRECT and exposes actual reserved-resource FAIL only after submission.
10. Submitting J2.5 plus დიახ yields TRANSFER_INCORRECT despite a direction PASS; the scope failure is explained.
11. The scored circuit has real new CORE CircuitSnapshot, conductor/net membership and current B finding/coverage IDs; correct and incorrect examples are independently checked.
12. BOARD_AVAILABILITY, ACTIVE_CONFIGURATION, ELECTRICAL_COMPATIBILITY statuses remain separate and honest after scoring; GpioCoverage is not converted to GpioFinding.
13. A training reset, training rewire, altered revision or changed source/factset/catalog invalidates pending assessment and cannot reuse an old score.
14. A repeated score submission cannot mutate a finished result or create a second successful attempt in the same training state.
15. Wrong external pin, unreviewed evidence, mismatched report/source identity, unsupported role or unavailable B result cannot yield correct learning score.
16. Assessment output is an immutable, deterministic, versioned record; repeated identical fixtures/responses yield equal result bytes/digests, reordering unrelated records does not change outcomes.
17. The assessment never claims skill mastery, cognitive diagnosis, safety, real hardware compatibility, production readiness, physical-resistor validation or powered firmware behavior.
18. 127.0.0.1 only, Host/Origin/CSRF/form-size/CSP/escaping and existing HTTP adversarial controls remain unchanged or tighter. No JS, remote provider, cookies or persistent learner data.
19. Human-language approval remains pending; separate source-evidence and language review gating visible, no fabricated reviewer signature. Current EDU-001 wording packet unchanged.
20. Execute targeted tests, standalone full regression, authentic GPIO source admission and an end-to-end actual loopback HTTP sequence (practice fix → start assessment → submit both answers → view result → stale/replay rejection). Report actual counts, command logs, hashes, measured times and any failures. A browser visual/manual check is reported separately as DONE with actual evidence or NOT_PERFORMED; never substitute HTTP form tests for visual usability testing.
A successful test count alone is not a product gate. The HTTP transcript must demonstrate a new independent learner decision with separate academic and engineering verdicts.
7. Known baseline and restrictions
- Latest reported E2 test baseline: 165 tests on an isolated standalone run, with 20 E2 methods. One concurrent complete run failed with pre-existing Windows WinError 10053 on CHAT HTTP negative-body test, then the same full command passed standalone. Report any recurrence verbatim; do not silently suppress it or edit protected CHAT tests.
- CORE-001C-E1 and E2 are conditional, test-only mathematical/virtual topology experiments, not accepted electrical safety verification. Do not integrate their results into this assessment; this task is only GPIO input/output near-transfer.
- Reported CHAT and EDU localization remains PENDING_HUMAN_REVIEW, never claim user-ready production curriculum.
- Prior Research K's three routes are an interesting unapproved navigation hypothesis. No Project-first/Idea-first/Concept-first implementation in EDU-T1; independent Research K2's conclusion must be assessed by the owner separately.
- Keep main unchanged. Do not merge the new branch into main or previously published task branches.
8. Session steps and report
1. Fetch origin, verify the exact E2 predecessor and history, inspect protected modules only to understand existing public APIs, then create codex/edu-t1-independent-transfer from the checked SHA.
2. Implement only the frozen independent transfer adapter, minimal existing loopback integration and new tests. Preserve all old implementation bytes outside allowlist.
3. Run targeted tests; then sequentially, not concurrently, run the full test suite and authentic GPIO admission. Capture all commands, exit statuses, warnings, failed runs and retests.
4. Run the local HTTP scenario as a real process with the browser-equivalent form route, including adversarial/stale attempts. Log expected and observed source/assessment snapshots. Never record reusable secrets or CSRF token values in the report.
5. Commit authorized code/tests/docs as feat(edu-t1): add bounded independent GPIO transfer check. Include reports/EDU-T1-REPORT.md with commit manifest, actual suite counts, test-specific and usability gaps, network conditions, source integrity and PASS/PARTIAL/BLOCKED recommendation.
6. Push only codex/edu-t1-independent-transfer. Verify git ls-remote SHA, published commit ancestry and clean local state. If report needs a publication-only follow-up commit, record both exact SHAs and verify final remote HEAD.
7. Stop. No automatic architectural expansion, Research K2 adoption, UI framework decision, implementation of 3 routes or next Codex task. The owner reviews the report and decides what happens next.
Acceptance semantics
ENGINEERING_GATE_PASS requires actual fresh CORE/B verification, correct statuses, source/factset pins and all adversarial tests.
LEARNING_INTERACTION_PASS requires a complete browser-route transfer submission and honest independent-scoring behavior.
LOCALIZATION_PREVIEW_ONLY remains until a qualified independent Georgian reviewer and the owner explicitly approve exact text.
OVERALL: PASS_TEST_ONLY_PREVIEW only if both engineering and learning-interaction gates pass and localization restriction remains prominent. Any missing gate ⇒ PARTIAL or BLOCKED. This must not be reported as educational efficacy or production release.