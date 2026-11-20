# EDU-001 Georgian feedback contract

The read-only adapter teaches one anchored requirement of the existing two-role SYN-001 pattern. The caller provides the current `SynthesisRequest`, its selected snapshot SHA and external catalog and fact-set pins in `LearningContext`. A caller proposing a different assignment supplies its physical contact and can supply the alternate candidate for replay. Connective and GPIO authorities remain CORE-001A/B.

```python
build_educational_feedback(
    candidate: SynthesisCandidate, catalog: CatalogSnapshot, fact_set: GpioFactSet, context: LearningContext, *,
    proposed_terminal: TerminalRef | None = None, alternative: SynthesisCandidate | None = None,
) -> EducationalFeedbackReport
transition_feedback(
    previous: EducationalFeedbackReport, candidate: SynthesisCandidate, catalog: CatalogSnapshot,
    fact_set: GpioFactSet, context: LearningContext,
) -> FeedbackTransition
```

The adapter recomputes CORE topology and matches the two actual conductors against the typed roles, assigned contacts and CORE net membership. It replays the existing B verifier on the candidate snapshot and checks both raw finding and coverage collections against the candidate report. Record order is immaterial. A mismatch rejects the input before rendering. Synthesis domain membership is a bound for proposed actions. The candidate's report alone confers no new engineering authority.

A deterministic ka-GE template selected by exact rule, status and reason can use factual placeholders only from physical anchors and independently joined reviewed source rows. Source records carry claim and source IDs, locator, revision and scope. Typed catalog mappings and separate GPIO facts retain distinct provenance. Missing or unqualified bindings leave neutral evidence requests with reason codes and no inferred values. Coverage uses its own origin and raw coverage ID. Soft language never turns UNKNOWN, NOT_APPLICABLE or NOT_EVALUATED into PASS.

One primary hint prioritizes a proven failure or the selected role's physical capability result. Additional hints expose board availability, firmware configuration, electrical coverage and eligible boot context. Proposals are `CANDIDATE_ACTION`, with a direction claim only when a separately replayed alternative supplies qualified evidence. When the caller requests `RESET` and a reviewed strap fact covers the exact trusted mapping, the adapter makes a separate B `BOOT_STRAP_CONTEXT` call on the current snapshot. The raw result and open prerequisites remain separate. An absent check is represented as `NOT_REQUESTED` or `NOT_ESTABLISHED`.

Hint fingerprints include the snapshot, catalog and fact-set digests, requirements digest, ruleset and template versions, physical anchors, source bindings, raw record reference, rendered text and uncertainties. Transition recomputes feedback, moves obsolete active hints to WITHDRAWN, and lists newly generated IDs. It never changes raw B statuses.

## Headless preview

The authored wording is a draft pending independent human review and owner approval. The API fails closed unless the caller explicitly sets `preview_unreviewed_ka=True`. Preview output includes `PENDING_HUMAN_REVIEW` and `TEST_ONLY_NOT_PRODUCTION`. Reproduce the transcript and the structured evidence from the repository root with the pinned Python environment.

```powershell
python -X utf8 -B -m examples.edu001_learning_cycle --preview
python -X utf8 -B -m examples.edu001_learning_cycle --preview --json
```

The example simulates an explicit learner choice by narrowing a new SYN request to the selected assignment. It reads the ledger-pinned fixtures and invokes generation and verification again. The example writes no trace files and makes no online calls.
