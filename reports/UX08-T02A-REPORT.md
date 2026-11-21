# Execution report — UX08-T02A Rev 1.0

- Date — 2026-11-21, Asia/Tbilisi
- Plan — [historical frozen Rev 1.0 handoff](https://github.com/donluka-23/Inventor_EDU/blob/8c1ce0e70144858044b93a6c8f60f0e60ab93562/tasks/UX08-T02A.md)
- Outcome — **BLOCKED / OWNER_DECISION_REQUIRED**
- Verified base — `codex/ds-002b-r3-exact-hardware-visual` at `78168099a649887dfd8f874d7953fff9428fe76c`
- Task branch — `codex/ux08-t02a-source-native-gpio-projection`

## A. Preflight and supporting audit

Read `AGENTS.md`, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, `docs/SESSION_PROTOCOL.md`, `docs/VERIFICATION_POLICY.md`, `docs/adr/ADR-0001-product-scope.md`, `reports/REPORT_TEMPLATE.md`, `reports/CORE-001B-01-REPORT.md`, and `reports/DEMO-001-REPORT.md`. Reviewed the archived `docs/RESEARCH_UX08_R2/` package, from `00_INPUT_MANIFEST_AND_AUTHORITY.md` through `10_EXECUTIVE_DECISION.md`, with its README and checksum manifest. All 12 listed hashes matched. The archive supplied technical context. Rev 1.0 supplied execution authority.

ADR-0001 is accepted. ADR-0002 remains proposed/on hold, and ADR-0003 and ADR-0004 remain undecided. Origin was `https://github.com/donluka-23/Inventor_EDU.git`. After fetching, the local and live base refs matched the pinned SHA, and `git diff --exit-code 78168099a649887dfd8f874d7953fff9428fe76c -- inventor_edu tests data` exited 0. The untracked archive and screen architecture file were outside the allowlist and staging scope.

## B. Reproduced stop condition

Section 5 assigns `PROJECTION_INVALID_INPUT` to any argument that fails strict Pydantic revalidation. The same section and T02A-08 assign `PROJECTION_INCONSISTENT_NATIVE_RECORD` to a record whose ruleset version differs from its report. Both native fields accept only `Literal["gpio-capability-v1"]`. Any nested ruleset value that differs from a valid report therefore also fails strict revalidation. The handoff leaves error precedence unspecified for this required case. [Ruleset literals](../inventor_edu/gpio_verify.py#L50) · [Record configuration](../inventor_edu/models.py#L25)

From the actual `DemoBridgeTests` fixture, generated `two_wires()` topology and the real GPIO report. The snapshot digests matched. On separate negative copies, changed only the first finding's or coverage record's `ruleset_version` to `gpio-capability-v2`, then called `GpioVerificationReport.model_validate(forged, strict=True)`. Both versions disagreed with the parent, and both triggered Pydantic `literal_error`. Stopped before writing projection code.

## C. Changed files

| Path | Change |
| --- | --- |
| `tasks/UX08-T02A.md` | Created by copying the exact attachment bytes. |
| `reports/UX08-T02A-REPORT.md` | Created the blocked checkpoint report. |

## D. Acceptance by criterion

| Criterion | Status | Evidence |
| --- | --- | --- |
| T02A-01, 02, 03, 04 | NOT_RUN | Projection implementation stopped during preflight. |
| T02A-05, 06, 07 | NOT_RUN | Projection implementation stopped during preflight. |
| T02A-08 | BLOCKED | The ruleset perturbation hit both frozen error conditions on the native report. The remaining projection subtests were not run. |
| T02A-09, 10, 11, 12 | NOT_RUN | Projection implementation stopped during preflight. |
| T02A-13, 14 | NOT_RUN | Projection implementation stopped during preflight. |

## E. Commands and observed results

Commands ran from `D:/Inventor_EDU` with the existing locked CPython 3.12.8 and Pydantic 2.14.4 environment. Used its existing DATA-001 fixture cache and a task-specific temporary Hypothesis cache.

| Command | Exit | Observed result |
| --- | --- | --- |
| `git fetch --prune origin`, `git ls-remote --heads origin` with task and base refs | 0 | Live base matched the local pinned commit. The task ref was absent. |
| `python -X utf8 -B -` with the in-memory repro in §B | 0 | `snapshot match: True`. Both record/report mismatch comparisons returned `True`. Errors were `(('findings', 0, 'ruleset_version'), 'literal_error')` and `(('coverage', 0, 'ruleset_version'), 'literal_error')`. |
| `python -X utf8 -B -m unittest tests.test_ui_projection -v` | NOT_RUN | The new test module was not created after the stop. |
| `python -X utf8 -B -m unittest discover -s tests -p 'test_*.py'` | 0 | `Ran 184 tests in 12.715s`, `OK`. Zero failures, errors or skips. Existing baseline only. |
| `git diff --check` | 0 | No whitespace diagnostics. |

## F–J. Boundaries, owner decision, OSS, and rollback

The native probe verifies only the reported input contradiction. It establishes no electrical compatibility, deployment trust, report currentness, or hardware safety. No dependencies, external source material, engineering implementations, or assets were introduced. Browser, simulator, network experiment, and UI validation were outside the task.

Owner decision required before implementation. Specify the required error for a native-shaped nested ruleset mismatch that also fails strict validation, or revise the T02A-08 ruleset oracle. The checkpoint has two Markdown files and its parent is the pinned baseline. Review this report in the architecture conversation before authorizing further implementation.

## Git publication

`git diff --cached --check` exited 0. The staged scope contained the two listed Markdown files. The staged handoff matched the attachment byte for byte, with SHA-256 `a8153cb39dc9b01470cffc5b9c1d9c56b51ec3fe69a40603c3e40551f28d86e3`. The credential-pattern scan found no matches.

`git push -u origin codex/ux08-t02a-source-native-gpio-projection` exited 0. Independent `git ls-remote --heads origin` and fetch verified the blocked checkpoint at `c1b273c0686dadc3d80c87366acc799d5a80a615`, the pinned predecessor at `78168099a649887dfd8f874d7953fff9428fe76c`, and `main` at `b1db3e947d04508ca22d4ba55e3172616620bad2`. This report follow-up records the observed publication.

# Continuation — UX08-T02A Rev 1.1

- Date — 2026-11-21, Asia/Tbilisi
- Plan — [verbatim frozen Rev 1.1 handoff](../tasks/UX08-T02A.md)
- Outcome — **PASS for the authorized projection and regression tests**
- Engineering base — `78168099a649887dfd8f874d7953fff9428fe76c`
- Verified continuation head — `8c1ce0e70144858044b93a6c8f60f0e60ab93562`
- Task branch — `codex/ux08-t02a-source-native-gpio-projection`

## A. Preflight and authority

Rechecked the governance and reports listed in Rev 1.0 §A, the Rev 1.1 handoff, the native ruleset literals, the canonical net computation and the DEMO-001/GPIO fixtures. Applied the evidence-gated engineering skill. The local and live branch refs matched the expected SHAs. The only commits between the engineering base and continuation head were the Rev 1.0 blocked checkpoint and its publication appendix. Their changes were confined to the handoff and report. The native source and fixture comparison against the engineering base exited 0. The task continued on the existing branch. The untracked audit archive and screen architecture file stayed outside staging.

ADR-0001 applies. ADR-0002 remains proposed/on hold and ADR-0003/0004 remain undecided. Owner decision UX08-T02A-D01 resolves the earlier blocker by putting strict native schema validation first. A forged nested ruleset now yields `PROJECTION_INVALID_INPUT`. Structurally valid digest and affected-net disagreements yield `PROJECTION_INCONSISTENT_NATIVE_RECORD`.

## B. Implementation

Added the six approved public names in `inventor_edu.ui_projection`. The projection strictly revalidates all inputs, checks the selected net and nets referenced by report terminals, and checks the complete report for record consistency and duplicate IDs before filtering. It returns the native net ID and membership tuple. Finding and coverage wrappers retain the original native payloads and use deterministic ordering. Serialization reuses the existing canonical JSON function.

## C. Changed files

| Path | Action |
| --- | --- |
| `inventor_edu/ui_projection.py` | Added the immutable projection API, validation and serializer. |
| `tests/test_ui_projection.py` | Added the 14 unittest acceptance cases using the real CORE and GPIO engines. |
| `docs/prototype/UX08_T02A_GPIO_PROJECTION_CONTRACT.md` | Documented the frozen API, precedence and evidence limits. |
| `tasks/UX08-T02A.md` | Replaced the handoff with the exact Rev 1.1 attachment bytes. |
| `reports/UX08-T02A-REPORT.md` | Added the continuation and preserved the Rev 1.0 blocker. |

## D. Acceptance matrix

| ID | Result | Observed |
| --- | --- | --- |
| T02A-01 | PASS | J2.5 was `FAIL / OUTPUT_NOT_CAPABLE`. Delegated electrical coverage was separate and unevaluated. |
| T02A-02 | PASS | J3.9 was `PASS / CAPABILITY_CONFIRMED`. Electrical coverage stayed unevaluated and board availability stayed unknown. |
| T02A-03 | PASS | Native serialized payloads matched field for field. Coverage kept `finding_id` and had no `status` or `severity`. |
| T02A-04 | PASS | Copied the CORE net containing `T:board/J2.5` and `T:sensor/Trig`. |
| T02A-05 | PASS | Absent selection raised `PROJECTION_TERMINAL_NOT_IN_TOPOLOGY`. |
| T02A-06 | PASS | The sensor terminal had native topology and an empty record tuple. |
| T02A-07 | PASS | Digest disagreement raised `PROJECTION_SNAPSHOT_MISMATCH`, including with an absent selection. |
| T02A-08 | PASS | Eight separate, structurally valid digest or net mutations across both record types returned `PROJECTION_INCONSISTENT_NATIVE_RECORD`. Two nested ruleset mutations returned `PROJECTION_INVALID_INPUT`. |
| T02A-09 | PASS | Broken net/member associations and missing or wrong report terminals returned their designated errors. |
| T02A-10 | PASS | Duplicates within findings, within coverage, and across kinds were rejected, including an unselected terminal. |
| T02A-11 | PASS | Repeated calls, partition reversal, independent canonical encoding and strict JSON round-trip produced identical bytes. |
| T02A-12 | PASS | Native bytes and digests were preserved. The result was frozen and rejected extra fields. Exact-type and schema errors returned `PROJECTION_INVALID_INPUT`. |
| T02A-13 | PASS | Native unknown findings and separate coverage were preserved when either trust pin was absent. |
| T02A-14 | PASS | Evidence claim IDs matched the native payloads. No source URL or citation was introduced. |

## E. Commands and observed results

Commands ran from `D:/Inventor_EDU` with the existing locked CPython 3.12.8 and Pydantic 2.14.4 environment. The existing DATA-001 source cache and a temporary Hypothesis directory were used.

| Command | Exit | Observed output |
| --- | --- | --- |
| `python -X utf8 -B -m unittest tests.test_ui_projection -v`, first run | 1 | `Ran 14 tests in 0.017s`, `FAILED (errors=15)`. The new fixture helper omitted the required `junctions` argument. Fixed the helper with `junctions=()`, matching DEMO-001. |
| `python -X utf8 -B -m unittest tests.test_ui_projection -v`, rerun | 0 | `Ran 14 tests in 0.171s`, `OK`. All 14 acceptance methods and their subtests passed, with zero skips. |
| `python -X utf8 -B -m unittest discover -s tests -p 'test_*.py'`, first run | 1 | `Ran 198 tests in 46.435s`, `FAILED (errors=1)`. The existing CHAT-001 HTTP test `test_negative_bodies_and_repeated_forms` raised `ConnectionAbortedError: [WinError 10053]` while reading a loopback response. |
| Same full suite, second run | 1 | `Ran 198 tests in 38.520s`, `FAILED (errors=1)`. The same HTTP test raised the same socket error. |
| Same full suite, preimplementation control from a temporary `git archive` of `8c1ce0e` | 0 | `Ran 184 tests in 32.800s`, `OK`. The archived control had neither the projection module nor its tests. |
| Same full suite, third Rev 1.1 run | 0 | `Ran 198 tests in 34.405s`, `OK`. Zero failures, errors or skips. The third run used the same sources and tests as the preceding run. |
| `git diff --check` | 0 | No whitespace diagnostics. Git printed its working-copy line-ending warning for the frozen handoff. |
| `python -X utf8 -B -`, in-memory fixture inspection | 0 | The module exposed exactly its six declared public names. Both real fixture results printed the net, membership and native capability/coverage pairs recorded below. All 12 archived audit files matched their checksum manifest after implementation. |

| Selection | Native net | Native capability | Electrical coverage |
| --- | --- | --- | --- |
| `board/J2.5` | `net:sha256:47d13c5a6c7d312b246fe22dde761476f8530f62eb3293d0c73068fe63633b44` | `FAIL / OUTPUT_NOT_CAPABLE` | `NOT_EVALUATED / ELECTRICAL_CHECK_DELEGATED` |
| `board/J3.9` | `net:sha256:2c9d5e8a7f486a3114cc6737d1363c90147ef602c0490e70f96822919212ee31` | `PASS / CAPABILITY_CONFIRMED` | `NOT_EVALUATED / ELECTRICAL_CHECK_DELEGATED` |

Both nets contained the selected board terminal and `T:sensor/Trig`.

## F–J. Evidence limits, OSS, rollback and review

The native results are test-only. Snapshot digests establish agreement between the supplied topology and report. Catalog and fact-set digests establish agreement between each report record and its parent. The topology has no independent catalog digest. The projection performs internal consistency checks and supplies no authority about hardware safety, source trust, currentness, or electrical behavior. The output preserves native evidence IDs and the exception message contains only the error code. No dependencies, new assets, network experiments, UI, or new engineering rules were introduced.

The implementation can be reviewed using the pinned continuation head and the five-path diff. Rollback is available through an owner-authorized revert of the Rev 1.1 commits. The Rev 1.0 blocked history remains in Git. Submitting this report for owner review does not authorize another task.

## Rev 1.1 Git publication

Both working and staged whitespace checks exited 0. The staged review confirmed the five allowlisted paths, verified the Rev 1.1 handoff SHA-256 `28a749a5c34cb283dfb607c73d8f194bce0a0c7332349a77f9cc7fe08fd436cf` against the exact attachment bytes, checked local links, and found no credential signatures.

`git push origin codex/ux08-t02a-source-native-gpio-projection` exited 0. Independent `git ls-remote --heads origin` and fetch verified implementation commit `8c735640c9a94265465f7659b01cda6a7b9c50e7` on the existing task branch, the engineering baseline ref at `78168099a649887dfd8f874d7953fff9428fe76c`, and `main` at `b1db3e947d04508ca22d4ba55e3172616620bad2`. This report-only follow-up records the observed implementation publication.
