# EDU-T1 independent transfer contract

Start the existing preview from the repository root.

```powershell
python -X utf8 -B -m examples.chat001_local_preview --preview --host 127.0.0.1 --port 0
```

Open the printed URL. Correct the initial Trig failure by choosing J3.9. Select **დამოუკიდებელი შემოწმება** after the real practice correction. Select one contact and one scope answer, then submit. Reset restores the initial practice state and discards the attempt.

The only item is `edu-t1-echo-direction` version 1.0. The neutral options appear in fixed order, board/J2.5 then board/J3.19. The scope options are rendered as არა and დიახ, with wire values `NO` and `YES`. The pending page is rendered separately and contains no practice panes, source bindings, report data, answer key or recommended option.

```python
can_start_transfer(fixture: LessonFixture, state: LearningSessionState) -> bool
start_transfer(fixture: LessonFixture, state: LearningSessionState) -> TransferAttempt
transfer_choices(attempt: TransferAttempt, key: bytes) -> tuple[tuple[TerminalRef, str], ...]
submit_transfer(
    fixture: LessonFixture, state: LearningSessionState, attempt: TransferAttempt,
    key: bytes, token: str, scope_answer: ScopeAnswer,
) -> TransferAttempt
```

Start verifies the server-side practice transition from the anchored output FAIL to an actual Trig output PASS on J3.9, with no known hard failure for that role. The attempt holds the item's version, practice revision and snapshot, catalog and fact-set pins, and context fingerprint. Tokens are opaque HMACs scoped by that context and exact terminal. The key stays in local process memory. There is one immutable result per attempt. Invalid values, stale contexts and repeated submissions raise a validation error.

The selected Echo contact and fixed distinct Trig contact pass through CAP domain discovery, a new constrained SYN evaluation, CORE topology and existing B verification. The adapter compares the fresh report to a real B replay over the canonical snapshot. Required GPIO check and coverage records must exist. The assessment returns `TRANSFER_CORRECT_IN_SCOPE` only when direction passes, no known hard check fails for Echo, and the learner answers `NO`. Other complete, evaluable answers return `TRANSFER_INCORRECT`. Invalid authority or incomplete coverage cannot award correctness.

The result retains selected terminal, training revision/snapshot, the generated candidate's real catalog/fact-set/snapshot digests and typed B findings and coverage, admitted claim-to-source references, both question outcomes, and a deterministic result digest. Electrical acceptance is `NOT_ESTABLISHED`. Every output remains `TEST_ONLY_NOT_PRODUCTION` and `PENDING_HUMAN_REVIEW`. Source review is separately identified. There is no analytics, telemetry or answer persistence.

The existing loopback, Host/Origin, CSRF, no-store, CSP and strict form decoder remain in force. `START_TRANSFER` accepts the three common form fields. `SUBMIT_TRANSFER` also requires exactly one `terminal` token and one `scope` value. A changed practice revision invalidates the attempt. Before scoring, ordinary GET and read-only practice commands keep showing the pending assessment without exposing training feedback.
