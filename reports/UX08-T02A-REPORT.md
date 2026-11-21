# Execution report — UX08-T02A Rev 1.0

- Date — 2026-11-21, Asia/Tbilisi
- Plan — [verbatim frozen handoff](../tasks/UX08-T02A.md)
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
