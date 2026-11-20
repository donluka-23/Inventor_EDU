# Work cycle: architecture conversation → Codex → report → review

## 0. Research and decision outside Codex
The separate research/architecture conversation: defines one testable engineering outcome, evaluates evidence and alternatives, selects approach, records accepted or proposed ADRs, identifies license rights and engineering limits, and writes a **frozen task execution plan**. The owner approves it.

## 1. Task handoff (exactly one)
Handoff includes: TASK_ID + REVISION, `tasks/<TASK_ID>.md`, allowed files, explicit exclusions, acceptance tests/oracles, necessary input artifacts, dependencies and OSS status, rollback. If any of these is missing in a way that changes design, STOP.

## 2. Codex session start
Read the mandatory files from `AGENTS.md`; produce BOOT BRIEF; verify allowed execution context. Do not launch research or self-generate plans. `NEXT.md` is a pointer only.

## 3. Implementation
Implement only the frozen plan. Report model gaps and architecture-level blockers instead of creating substitute requirements. No unapproved library installs, unexplained updates, or side quests.

## 4. Session report
Write `reports/<TASK_ID>-REPORT.md` based on `reports/REPORT_TEMPLATE.md`. Include actual command outputs and FAIL/UNKNOWN cases. The report must be standalone for review in a different chat. Preserve all relevant outcomes, including no-code/blocked sessions.

## 5. Transfer to architecture conversation
The owner **uploads the Markdown report or pastes its full content** into the architecture conversation. Codex cannot send the file to that conversation automatically. Assistant reviews outcomes, tests acceptance, chooses ACCEPT / REVISE / BLOCK, determines next architecture/work change with user approval, and issues the next frozen task plan.

## 6. Persistent knowledge
`docs/STATUS.md` is observed current state, `docs/DECISIONS.md` is approved decision index, `docs/adr/` has design rationale, `reports/` has execution evidence, `tasks/WORK_LOG.md` has short execution chronology. These must not be changed to make a failing task look complete. A report alone cannot elevate ADR or gate status.

## 7. Mandatory Git lifecycle

- **Start:** Confirm the local repository and expected `origin`. Fetch remote metadata and inspect the current branch, its tracking state and the working tree. Identify and preserve existing uncommitted work. Use a task-specific branch such as `codex/core-001a-acceptance-audit` unless the architecture owner explicitly authorizes another branch policy.
- **During the task:** Keep changes within the authorized scope. Run relevant tests, retain reproducibility evidence and record added, modified and removed files. Keep unrelated changes out of the task commit.
- **Finish with changes:** Record actual checks and outcomes. Inspect `git status` and the intended files for secrets, sensitive data and restricted materials. Stage only authorized changes, inspect the full staged diff and create a descriptive commit that identifies the task and result. Push the current task branch to `origin`, verify the remote ref points to the expected SHA, and report the branch, commit SHA, push status and test status.
- **PARTIAL or BLOCKED:** Commit and push a safe, reviewable checkpoint and factual report on the task branch. Label the incomplete work explicitly. If there are no changes to commit, verify synchronization and record that no commit was needed.
- **Push failure:** Preserve the local commit and report `PUSH_FAILED` with the actual cause and SHA. Claim synchronization only after checking the remote ref.
- **Protected development:** A branch push does not approve the work. Keep `main` at the approved baseline until owner review. Do not automatically merge task branches, bypass protections, force-push or rewrite history.

## 8. Mandatory documentation lifecycle

At session start, read `docs/STATUS.md`, `tasks/NEXT.md`, the authorized task, relevant decisions and previous execution reports. Apply the existing write allowlist and approval rules throughout the session.

At completion:

1. Create or update the task-specific report with actual commands, checks, evidence, limitations and results. Use explicit statuses such as `COMPLETED`, `PARTIAL`, `BLOCKED` and `NOT_RUN` where appropriate.
2. If the recorded state materially changed, update `docs/STATUS.md` and `tasks/NEXT.md` when the plan authorizes those exact writes. Otherwise, record the factual discrepancy and the pending update in the report. A next-task pointer stays advisory.
3. Update `docs/DECISIONS.md` or ADRs only for explicitly owner-approved decisions. Update the OSS register only when dependency or license facts change and governance authorizes the edit. Report any pending reconciliation.
4. Update other existing documents only when their defined responsibilities are affected and their paths are authorized. Preserve raw research, historical reports and decision provenance.
5. Before committing, compare the active task, canonical status, next-task pointer and report for consistency. Verify references and evidence, record unresolved discrepancies, and include all authorized tracking updates in the task commit and push. Never promote an implementation claim to a verified result without evidence.
