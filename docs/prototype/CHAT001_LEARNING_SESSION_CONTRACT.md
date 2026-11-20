# CHAT-001 local learning session contract

The preview serves the owner-frozen ESP32-DevKitC-32E V4 and Adafruit #3942 fixture. The learner can change the Trig contact. The Echo contact stays fixed. All output is `TEST_ONLY_NOT_PRODUCTION` and `PENDING_HUMAN_REVIEW`. GPIO direction results apply to the stated check at the documented contact. Board-resource, firmware, electrical and startup scope retain their individual records.

## Launch

From the repository root with the existing pinned Python environment:

```powershell
cd D:\Inventor_EDU
python -X utf8 -B -m examples.chat001_local_preview --preview --host 127.0.0.1 --port 0
```

Open the printed loopback URL. Use **რატომ?** for the scoped result, **წყაროები** for sources, **შეამოწმე board/J3.9** for a fresh choice, **რა შეიცვალა?** for the transition and **თავიდან დაწყება** to reset. Stop the server with Ctrl+C. Omitting `--preview` fails before binding.

## Controller

```python
start_learning_session(fixture: LessonFixture, *, preview: bool = False) -> LearningSessionState
apply_learning_action(
    fixture: LessonFixture, state: LearningSessionState, action: LearningAction,
) -> LearningActionResult
apply_exact_alias(
    fixture: LessonFixture, state: LearningSessionState, revision: int, text: str,
) -> LearningActionResult
```

`LessonFixture` holds the existing catalog, fact set, typed request, anchored requirement, board identity, fixed and initial contacts, and independent pins. `LearningAction` carries a revision, an allowed intent, and at most one server-issued selection digest. `LearningSessionState` carries the narrowed request, actual SYN candidate, CAP-backed options, current EDU feedback, optional prior transition and reference, and the input-fingerprint guard. `LearningActionResult` carries the recognized action, error and optional state. Raw findings and coverage keep their existing types. With stale fixture, ruleset or template context, the controller withholds state.

| Intent | Exact Georgian alias | Operation |
| --- | --- | --- |
| WHY_CURRENT | რატომ? | Show the active primary EDU hint and rule |
| SHOW_EVIDENCE | წყაროები | Show the active record and its source bindings |
| SHOW_UNVERIFIED | რა არ ვიცით? | Show open checks, with each role bound to the current circuit |
| LIST_TERMINALS | კონტაქტები | Show CAP qualifications with current SYN-backed selection controls |
| TRY_TERMINAL | — | Select a server-issued current option and recompute |
| WHY_CHANGED | რა შეიცვალა? | Show previous and current references and withdrawn IDs |
| SHOW_BOOT_CONTEXT | ჩატვირთვა | Show the separate EDU/B RESET result or its unestablished state |
| RESET_LESSON | თავიდან დაწყება | Recompute the frozen initial assignment through a new transition |

Unknown text returns `UNSUPPORTED_INTENT` and is discarded. An off-domain option returns `INVALID_CHOICE`. Old form revisions return `STALE_SUBMISSION`. Invalid action shapes return `INVALID_ACTION`. A changed fixture, rule version or template version returns `STALE_CONTEXT` without active feedback.

For a new choice or reset the controller reruns CAP, enumerates actual SYN choices with the other role fixed, regenerates the selected assignment in a narrowed request, and calls EDU transition, which checks CORE topology and the current B report again. A displayed CAP qualification describes its board-only snapshot. The active EDU finding and Echo rows describe the current two-component snapshot.

## Loopback transport

`GET /` reads the current state. `POST /` accepts a single exact form action or a short exact text alias. Form values are limited to 2,048 bytes and five unique fields, with strict UTF-8 percent decoding. Host must match the bound numeric loopback authority. POST requires the matching Origin and a per-process CSRF token. Selection IDs are tied to the current revision, active snapshot and server-enumerated assignment. Sensitive engineering fields are absent from the accepted form grammar.

The server renders UTF-8 HTML with escaped dynamic values, HTTP(S) links from current source bindings, `Cache-Control: no-store` and a CSP with a pinned stylesheet hash. It exposes no CORS permission, script, API route or persistent user state. This is an unaudited local utility. The [Georgian wording review packet](../reviews/EDU001_KA_WORDING_REVIEW_PACKET.md) remains pending human review.
