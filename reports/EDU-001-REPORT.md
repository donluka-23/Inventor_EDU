# EDU-001 revision 1 execution report

- Session date — 2026-11-20, Asia/Tbilisi.
- Frozen task — [EDU-001 revision 1](../tasks/EDU-001.md).
- Recommendation — **PARTIAL**. Engineering, evidence, stale-state and CLI gates passed. The Georgian wording is an explicitly gated test preview pending independent human review and owner approval. The handoff supplied no reviewed template text or approval of the implemented wording.
- Branch — `codex/edu-001-grounded-feedback`.
- Verified predecessor — `origin/codex/cap-001-terminal-discovery` at `885311f3549cece97cfa2ef08f1db36d624d1df4`.

## A. BOOT BRIEF

Fetched `https://github.com/donluka-23/Inventor_EDU.git`, checked the live predecessor, inspected the clean worktree, verified that `f66d9af3db5fad3de878fbad3d45b06ee77c4ea4` remains an ancestor, and confirmed the four tracked Research F–I originals. Created the task branch from that exact predecessor. No source, baseline or API blocker was found.

Read `AGENTS.md`, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, `docs/SESSION_PROTOCOL.md`, `docs/OSS_POLICY.md`, `docs/VERIFICATION_POLICY.md`, accepted `docs/adr/ADR-0001-product-scope.md`, the evidence-gated-engineering skill and the frozen task. Inspected the required CORE models and public functions, B facts/verifier, DEMO bridge, SYN and CAP interfaces, relevant tests, fixture data, master plan, the CAP/SYN reports and CORE-001B source/rule ledger. ADR-0002 remains on hold.

The allowed writes were the feedback module, tests, CLI, contract, task copy, report, factual tracking files and bounded master-plan revision. The existing engines, tests, catalogs, research, ADRs, policies, UI and lock files were read-only. Gates were E01–E18, adversarial controls, authentic GPIO source admission, and deterministic CLI replay.

## B. Research decisions reused

Read Research H §§8–12 and 14–15 and Research I §§11–12 and 17.7–17.10 for the frozen boundary. The handoff selects constraint-based/model-tracing inspiration, one formative primary hint with a concrete next action, separate open issues, deterministic H1 templates, and the source claim → engineering record → physical anchor → educational claim chain. These are design choices for the bounded experiment. The H references on tutoring and feedback, cognitive load and PROV-O support the owner's design rationale. This session measures observable outputs. Research J was unavailable locally and no substitute was created. Research F–I were preserved unchanged.

## C. Implemented API and immutable DTOs

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

| DTO | Implemented fields |
| --- | --- |
| `LearningContext` | `request: SynthesisRequest`, `anchor_requirement_id: Identifier`, `current_snapshot_sha256: Digest`, `trusted_catalog_sha256: Digest \| None`, `trusted_factset_sha256: Digest \| None`, `boot_state: Literal["RESET"] \| None = None`, `preview_unreviewed_ka: bool = False` |
| `EngineeringReference` | `origin: FINDING \| COVERAGE`, `record_id` and `snapshot_digest: Digest`, `requirement_id`, `rule_id`, `reason_code` and `operating_state: Identifier`, `terminal: TerminalRef`, `net_id: str`, `status: PASS \| FAIL \| UNKNOWN \| NOT_APPLICABLE \| NOT_EVALUATED` |
| `SourceBinding` | `origin: CATALOG_CLAIM \| GPIO_FACT`, `claim_id` and `source_id: Identifier`, `url`, `revision`, `locator` and `scope: str`, `recorded_review: Literal["approved"]`, `source_digest: Digest \| None` |
| `EducationalHint` | `hint_id` and `dependency_fingerprint: Digest`, `category: Category`, `learning_concept`, `template_key` and `requirement_id: Identifier`, `template_version` and `text_ka: str`, `source_terminal` and `terminal: TerminalRef`, `net_id: str \| None`, `reference: EngineeringReference \| None`, `evidence: tuple[SourceBinding, ...]`, `unresolved_scopes: tuple[EngineeringReference, ...]`, `limitations: tuple[Identifier, ...]`, `action_qualification: Literal["CANDIDATE_ACTION"] \| None = None`, `validity: ACTIVE \| WITHDRAWN = ACTIVE` |
| `EducationalFeedbackReport` | `schema_version: "1.0"`, `restriction: "TEST_ONLY_NOT_PRODUCTION"`, `localization_review: "PENDING_HUMAN_REVIEW"`, `snapshot_digest`, `catalog_digest`, `factset_digest` and `requirements_digest: Digest`, `evidence_scope: TEST_ONLY_SOURCE_REVIEWED \| TEST_ONLY_SYNTHETIC`, `ruleset_version: Identifier`, `template_version: str`, `primary_hint: EducationalHint`, `additional_hints` and `withdrawn_hints: tuple[EducationalHint, ...]`, `next_action: EducationalHint \| None`, `boot_context: NOT_REQUESTED \| NOT_ESTABLISHED \| CHECKED`, `contextual_finding: GpioFinding \| None`, `contextual_coverage: GpioCoverage \| None`; derived `active_hints` property |
| `FeedbackTransition` | `old_snapshot_digest` and `new_snapshot_digest: Digest`, `withdrawn_hint_ids` and `new_hint_ids: tuple[Digest, ...]`, `current: EducationalFeedbackReport` |

`Category` admits `ERROR_CAUSE`, `SCOPED_CONFIRMATION`, `MISSING_EVIDENCE`, `NOT_EVALUATED_EXPLANATION`, `CONTEXTUAL_CAUTION` and `NEXT_ACTION_CANDIDATE`. `FeedbackInputError.code` identifies rejected educational inputs. Core and verifier validation errors continue to propagate.

For a current hint, the adapter recomputes CORE topology, compares the active snapshot pin, checks exact request instances, distinct role anchors, conductors and CORE net membership, and replays the existing verifier with external pins and the actual assignment. It compares the raw candidate report, both record collections and the role trace IDs against that replay. CAP board-only reports inform domain discovery. The generated circuit's B report anchors the tutoring output. Findings and coverage carry distinct origins. Candidate action references keep the alternative's own snapshot.

The versioned ka-GE preview uses exact rule/status/reason branches. Pin-specific claims require a typed scope-matched reviewed catalog mapping and the actual reviewed GPIO evidence B references. Each citation joins to its exact source ID, locator, revision, scope and available digest. Missing, ambiguous and unreviewed sources suppress pin-specific prose and leave a neutral evidence request. CORE topology, including net membership, is represented separately from those sources. A fingerprint covers the current snapshot, role requirements, catalog and fact-set versions, ruleset, template version and text, reference, source bindings, physical anchors and unresolved scopes. Transition rebuilds the current report and withdraws obsolete IDs. No raw report is modified.

## D. Observed correction transcript and T0 comparison

The CLI loads the acceptance pins published in the [CORE-001B source/rule ledger](CORE-001B-01_SOURCE_AND_RULE_LEDGER.md). CAP discovers the domains for Trig and Echo. SYN evaluates those assignments on CORE snapshots. The scripted choice narrows a fresh request and reruns SYN and B. The before/after excerpts below are from the actual CLI.

```text
EDU-001 | TEST_ONLY_NOT_PRODUCTION | PENDING_HUMAN_REVIEW
საწყისი შეერთება
sha256:b6ccc23eb87fe910d9127ec7dfdaef68e18aba243af4e9996c4b09abddbf2369
PHYSICAL_CAPABILITY=FAIL/OUTPUT_NOT_CAPABLE
სქემაში sensor/Trig უკავშირდება board/J2.5 კონტაქტს (GPIO34). Trig სიგნალის გასაგზავნად დაფას სჭირდება გამოსასვლელი (GPIO_OUT). დოკუმენტირებული ვარიანტის მიხედვით GPIO34 ამ ფუნქციას ვერ ასრულებს.
შემდეგი ცდა: მოდელში გადაიტანე sensor/Trig კავშირი board/J3.9 კონტაქტზე და ხელახლა გაუშვი შემოწმება. ელექტრული თავსებადობა დაუდასტურებელია. ამ ალტერნატივაზე მიმართულების შემოწმება გავლილია.
რა შეიცვალა და რატომ
მაგალითში მოსწავლე ირჩევს შეთავაზებულ კონტაქტს და შემოწმება თავიდან ეშვება.
წინა მინიშნება გაუქმდა (WITHDRAWN) | sha256:d3fe3cf60c3160d578c7face13dc20f43cf4b7c3c2f50ce63e014f9bf8af4e7c
sha256:6fe1964503bdc98e1c3f82bd6c817ed92d0cef800b73734c7c11518d10a1a230
PHYSICAL_CAPABILITY=PASS/CAPABILITY_CONFIRMED
სქემაში sensor/Trig უკავშირდება board/J3.9 კონტაქტს (GPIO18). ACTIVE რეჟიმში გამოსასვლელის ფუნქციის შემოწმება (PHYSICAL_CAPABILITY) გავლილია.
რა რჩება დაუდგენელი
პროგრამული კონფიგურაცია დაუდასტურებელია (ACTIVE_CONFIGURATION=UNKNOWN). ამის დასადგენად საჭიროა შემოწმებული დაკვირვება პროგრამის გაშვებაზე.
board/J3.9 კონტაქტის ხელმისაწვდომობა დაფაზე დაუდგენელია (BOARD_AVAILABILITY=UNKNOWN). გადაამოწმე ამ დაფის რესურსების დოკუმენტაცია.
ელექტრული თავსებადობა არ შემოწმებულა (ELECTRICAL_COMPATIBILITY=NOT_EVALUATED).
ცალკე შემოწმება ჩატვირთვისას
BOOT_STRAP_CONTEXT=UNKNOWN/BOOT_STRAP_CONDITIONS_UNKNOWN | external_pull, reset_level, sampling_timing
board/J3.14 (GPIO0) კონტაქტისთვის ჩატვირთვის პირობები უცნობია (UNKNOWN). GPIO-ის მიმართულების მხარდაჭერა ჩატვირთვის ქცევას ვერ ადგენს. გადაამოწმე მტკიცებულების ჩანაწერში ჩამოთვლილი საწყისი პირობები.
```

Before, finding `sha256:3f797ff0ed2bd36510d2f6c23e7262cc1c17f942da47b21283fbd57c386d4b33` cited `board-J2.5` at `Header Block, J2 row 5`, `map-J2.5` at `Header Block J2.5; ordering row -32E`, and `silicon-GPIO34` at the inherited `soc_caps.h` mask/GPIO summary locator. After, finding `sha256:0b4a491805ae97648c107dc6951a7a9bf7abc3a0116e31d8081b318b47078050` cited the corresponding `board-J3.9`, `map-J3.9` and `silicon-GPIO18` locators for J3 row 9 and the mask. JSON preserves exact revisions, unmodified locators and URLs. Five prior hints or actions were withdrawn and four new active hints were generated.

The optional boot check used the real B `BOOT_STRAP_CONTEXT` operation at `RESET` on the separate J3.14 candidate's own canonical snapshot. It retained `strap-gpio0` with the recorded locator `ESP32 GPIO Summary Strapping pin note; board J3 row 14` from `board-header` and `sdk-gpio`. The reviewed fact triggers the check. A synthetic Port1 case exercised the same path without an ESP32/GPIO0 name check. Missing reviewed evidence or an omitted context yielded no boot-safety conclusion.

| Scenario | T0 raw engineering result | Additional information emitted by T1 |
| --- | --- | --- |
| Before | `FAIL / OUTPUT_NOT_CAPABLE` at board/J2.5 | Links the physical sensor/Trig wire to the contact, explains why the required GPIO_OUT direction fails at GPIO34, binds the source locators, and proposes moving the simulated Trig wire to J3.9 and rerunning verification. |
| After | `PASS / CAPABILITY_CONFIRMED` at board/J3.9 | States the precise passed direction scope and marks the earlier hint withdrawn. Explains what still requires board-resource, firmware and electrical evidence. |
| Separate boot | `UNKNOWN / BOOT_STRAP_CONDITIONS_UNKNOWN` at board/J3.14 | Explains why direction support does not settle startup behavior and exposes the three recorded prerequisites as next evidence to check. |

No learner study, rate-of-error measurement or comparison of instructional effectiveness was performed. Research H benchmark overlaps exercised here were F01–F04, F06–F12, F19 and F23. The full research benchmark was not run. F05, F13–F18, F20–F22 and F24 are **NOT_IMPLEMENTED** in this adapter, covering unsupported states/functions, incomplete or ambiguous topology scenarios, a source STALE state, component selection, staged learner modeling and firmware thresholds.

## E. Acceptance and adversarial controls

| Gate | Observed result | Status |
| --- | --- | --- |
| E01 | Exact board/J2.5 and sensor/Trig causal Georgian direction explanation | PASS in preview |
| E02 | Exact finding, rule, requirement, snapshot, net, reviewed claim and locator joins | PASS |
| E03 | Scoped GPIO18 output and GPIO19/GPIO34 input confirmations in their respective scenarios | PASS in preview |
| E04 | Board and firmware UNKNOWN and electrical NOT_EVALUATED visible. Board reservation FAIL prioritized even with direction PASS. | PASS |
| E05 | Separate raw coverage origin and matching actual coverage ID | PASS |
| E06 | Missing either pin confers no authority, numeric assertion or invented ID | PASS |
| E07 | Three mismatched record digests and both wrong external pins rejected | PASS |
| E08 | Unreviewed, conflicting and removed capability fact all produce evidence requests | PASS |
| E09 | Equal instance labels and synthetic duplicate printed labels preserve exact anchors | PASS |
| E10 | Equivalent reordered records produce equal output | PASS |
| E11 | Fresh generated snapshot and B PASS withdraw old FAIL hint | PASS |
| E12 | Unreplayed proposal has no verifier reference and is only CANDIDATE_ACTION | PASS |
| E13 | Separate boot result equals a direct B call and preserves all prerequisites | PASS |
| E14 | Missing strap evidence/context creates no safety conclusion. Synthetic NOT_APPLICABLE stays distinct. | PASS |
| E15 | Source, requirements and template revisions invalidate fingerprints. Spoofed ruleset rejected. | PASS |
| E16 | Unknown injected rules and reasons rejected before rendering. Unmapped authentic rendering keys abstain. | PASS |
| E17 | CLI subprocesses emitted Georgian before/after text and structured evidence | PASS in preview |
| E18 | CORE, DATA, DEMO, SYN and CAP regressions all passed | PASS |
| A1 | Forged PASS on an actual failing input rejected as UNVERIFIED_GPIO_REPORT | PASS |
| A2 | Swapped physical anchor rejected as ROLE_TRACE_MISMATCH | PASS |
| A3 | Fabricated claim ID rejected as UNVERIFIED_GPIO_REPORT | PASS |
| A4 | Old candidate presented with a new current snapshot pin rejected as STALE_SNAPSHOT | PASS |
| Linguistic approval | No approval record or independently reviewed Georgian template text supplied | PENDING_HUMAN_REVIEW |

## F. Actual commands, results and replay hashes

Ran in `D:\Inventor_EDU` using Python 3.12.8. Installed versions matched the pinned Pydantic 2.14.4, pydantic-core 2.50.5, annotated-types 0.8.0, typing-extensions 4.16.0, typing-inspection 0.4.5, NetworkX 3.7, Hypothesis 6.170.17 and sortedcontainers 2.4.0. pip reported 24.3.1.

```powershell
$exe=Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$src=Join-Path $env:TEMP 'InventorEDU-CORE-001B-01-sources'
$env:INVENTOR_EDU_DATA001_SOURCE_DIR=Join-Path $env:TEMP 'InventorEDU-DATA-001-dc037a238eb5efcc034dd9d62e5775d5c21e90e4'
$env:HYPOTHESIS_STORAGE_DIRECTORY=Join-Path $env:TEMP 'InventorEDU-EDU-001-hypothesis'
& $exe --version
& $exe -m pip list --format=freeze
& $exe -B -m unittest tests.test_edu001_feedback -v
& $exe -B -m unittest discover -s tests -v
& $exe -B -m tests.gpio_source_acceptance $src
& $exe -X utf8 -B -m examples.edu001_learning_cycle --preview
& $exe -X utf8 -B -m examples.edu001_learning_cycle --preview --json
```

```text
Ran 21 tests in 1.921s
OK
Ran 110 tests in 9.476s
OK
PASS: five authentic artifacts matched pins; masks, pull-up, header, flash, strap and -32E scope checked
```

Targeted and full test exits were 0. The full process took 10874.2 ms including startup and terminal delivery. All 110 passed, with zero failures, skips or blocks, including the 21 EDU tests and four authentic DATA cases. Authentic GPIO admission exited 0 separately. No test or CLI warnings were observed.

A Python subprocess check ran the two CLI modes twice each and compared raw stdout bytes before computing SHA-256. Every process exited 0 with zero stderr bytes.

| Mode | Measured wall time | Exact bytes | SHA-256 |
| --- | --- | ---: | --- |
| Georgian transcript | 630.6 ms and 637.4 ms | 5582 | `13a1651278024a70d1bd6301921beed14d1e87ec02a0bb6f39a86745997d0e7d` |
| Structured JSON | 667.5 ms and 614.9 ms | 228901 | `62278a3b05ae7fd5b0cd318613cf0c625546b7b13293be98baca1b53bcbe82d9` |

## G. Changed files, limits and owner decision

| Path | Change |
| --- | --- |
| `inventor_edu/educational_feedback.py` | Added the immutable feedback adapter, source joins and transitions |
| `tests/test_edu001_feedback.py` | Added the acceptance, adversarial and CLI integration checks |
| `examples/edu001_learning_cycle.py` | Added the reproducible headless preview |
| `docs/prototype/EDUCATIONAL_FEEDBACK_CONTRACT.md` | Added the exact API, preview boundary and commands |
| `tasks/EDU-001.md` | Added the frozen task |
| `reports/EDU-001-REPORT.md` | Added this complete execution record |
| `docs/STATUS.md`, `tasks/NEXT.md`, `tasks/WORK_LOG.md` | Recorded factual verified progress and the outstanding gate |
| `docs/prototype/MASTER_PLAN.md` | Advanced 1.2 to 1.3 and recorded the authorized EDU milestone and wording-review state |

Existing milestone descriptions, downstream gates, fixed non-goals, deferred features and risks were preserved. Status, next-task pointer and execution report agree. The adapter adds zero dependencies or artifacts from outside the repository. Existing source and fact files, Research F–I, and accepted engines/tests remain unedited. H intent parsing, broader component matching, CORE-001C voltage/current analysis, firmware verification, user study and UI remain unimplemented in EDU-001.

`OWNER_DECISION_REQUIRED` — have a qualified Georgian reviewer review the exact ka-GE v1 wording and approve it or supply corrections. Default calls fail closed with `GEORGIAN_WORDING_REVIEW_REQUIRED`; only explicit preview renders the current draft, with its review status visible. The handoff provides engineering and template-method authorization. Linguistic acceptance remains open, and no change to the architecture or B API is needed to complete it. Owner acceptance of EDU-001 is pending.
