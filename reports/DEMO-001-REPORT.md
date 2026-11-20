# Execution report — DEMO-001 rev 1

- Date: 2026-11-20 (Asia/Tbilisi).
- Authority: [owner-frozen DEMO-001 handoff](../tasks/DEMO-001.md), revision 1.
- Outcome: **PASS for the test-only headless bridge.**
- Predecessor: `origin/codex/core-001b-01-gpio-capability` at `0cdec11db446a6ea77ac74ef02dec0c2f995a3d6`, verified locally and against the live remote. Task branch: `codex/demo-001-scenario-bridge`.

## A. BOOT BRIEF and reads

Read AGENTS, PRODUCT, DEMO, DECISION_AUTHORITY, DECISIONS, SESSION_PROTOCOL, VERIFICATION_POLICY, STATUS, NEXT, WORK_LOG and ADR-0001. Inspected the existing CORE-001A models and core, B GPIO facts and verifier, pinned board/sensor catalog and fact set, fixture and test implementations, and R2, DATA-001 and B execution reports and B source ledger. ADR-0001 applies. No semantic blocker was found. The allowed writes were the handoff, master plan, bridge, tests, report and tracking files. The untracked Research F/G documents were left untouched and were not used to change product decisions.

## B–C. Actions and changed files

Fetched origin, verified the predecessor, created the task branch, preserved the frozen plan, implemented the adapter, ran source admission and regression tests, and reviewed the authorized tracking updates.

| Path | Action |
| --- | --- |
| `tasks/DEMO-001.md` | Preserved exact handoff bytes. |
| `docs/prototype/MASTER_PLAN.md` | Created the owner-frozen roadmap. The prescribed section matches the handoff text, in order, under a document title. |
| `inventor_edu/demo_bridge.py` | Added the one public operation and immutable report and link DTOs. |
| `tests/test_demo001_bridge.py` | Added 10 integration tests covering all 12 acceptance IDs and exact profile validation. |
| `docs/STATUS.md`, `tasks/NEXT.md`, `tasks/WORK_LOG.md` | Recorded verified headless status and remaining gates. |
| `reports/DEMO-001-REPORT.md` | Created this report. |

## D. Acceptance

| Criterion | Observed result | Status |
| --- | --- | --- |
| A01 | Exact catalog loads and the real verifier receives all five checks for both physical contacts. Its report is returned unchanged. | PASS |
| A02–A04 | J2.5→Trig fails output capability; moving Trig to J3.9 changes its net and passes output capability; J3.8→Echo independently passes input capability. | PASS |
| A05–A06 | Removing or ambiguously wiring Trig removes its findings; Echo remains evaluable. | PASS |
| A07–A08 | Shared Trig/Echo nets and ground or mixed GPIO/ground nets remain unresolved. | PASS |
| A09–A10 | Invalid terminal propagates the A typed error; missing pins yield UNKNOWN and incorrect pins raise existing B errors, including when no role resolves. | PASS |
| A11–A12 | Reordering, reversing and restoring preserve canonical output; identical display labels preserve physical instance IDs. | PASS |

Topology integration, requirement completeness, and real verifier integration passed. Evidence trust restrictions were preserved. Regression status: PASS. Prototype feature completeness: headless milestone only. Full `docs/DEMO.md` acceptance remains unmet, including the interactive editor, Georgian feedback and real voltage case.

## E. Commands and observed results

Ran from `D:/Inventor_EDU`. Git preflight used `git fetch origin`, `git branch -avv`, `git ls-remote --heads origin` and `git status --short`. Created the branch with `git switch -c codex/demo-001-scenario-bridge origin/codex/core-001b-01-gpio-capability --no-track`.

```powershell
$exe = Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$src = Join-Path $env:TEMP 'InventorEDU-CORE-001B-01-sources'
$env:INVENTOR_EDU_DATA001_SOURCE_DIR = Join-Path $env:TEMP 'InventorEDU-DATA-001-dc037a238eb5efcc034dd9d62e5775d5c21e90e4'
$env:HYPOTHESIS_STORAGE_DIRECTORY = Join-Path $env:TEMP 'inventor-edu-demo001-hypothesis'
& $exe --version
& $exe -m pip check
& $exe -B -m tests.gpio_source_acceptance $src
& $exe -B -m unittest discover -v
```

All four Python commands exited 0. Exact outcome excerpts:

```text
Python 3.12.8
No broken requirements found.
PASS: five authentic artifacts matched pins; masks, pull-up, header, flash, strap and -32E scope checked
Ran 54 tests in 1.685s

OK
```

44 predecessor methods plus 10 new methods passed, with zero failures and skips. DATA-001's authentic-source cases ran. The roadmap text comparison printed `MASTER_PLAN_SECTION_TEXT_MATCH`.

## F. Engineering and trust boundaries

`analyze_hcsr04_wiring` returns `DemoWiringReport` with two ordered `DemoLinkResult` records and the original `GpioVerificationReport` when roles resolve. `compute_nets` validates the committed snapshot and supplies membership and its digest. The bridge scopes the named instances by exact definition ID and digest, then uses `resolve_terminal` to identify verified SoC GPIO contacts among actual board members. Shared signals take precedence. Multiple eligible contacts are ambiguous, no board contact means missing, and a non-GPIO board contact on the net keeps it unresolved. No engineering finding is synthesized for those links.

For each unique role the adapter requests `PIN_MAPPING`, `PHYSICAL_CAPABILITY`, `BOARD_AVAILABILITY`, `ACTIVE_CONFIGURATION` and `ELECTRICAL_COMPATIBILITY` in ACTIVE state. Corrected GPIO direction is a scoped PASS; ordinary board availability and runtime activity stay UNKNOWN in these fixtures. Electrical coverage is NOT_EVALUATED. Even an empty request list uses the existing verifier's pin validation. Expected pins pass through unchanged.

Test catalog pin: `sha256:356732040b6bd762e8c604ae63c3600df5da225cc938af6dff688b25aad4c57b`. Fact-set pin: `sha256:890f608028990e8f80f9ee48cd4388e58df1d160acc7edf2bf61445df8556d16`. These are acceptance references, not independently authorized production trust. No physical hardware or safety was verified.

## G–J. Deviations, OSS, rollback and owner review

No roadmap change requests or blockers were identified. Frontend, Georgian goal parsing, commercial validation, firmware observation and electrical computation were outside scope. No new source, OSS dependencies or assets were introduced. To roll back, use the preserved predecessor or an owner-authorized revert. Review the headless result and separately authorize any later milestone or deployment trust decision.
