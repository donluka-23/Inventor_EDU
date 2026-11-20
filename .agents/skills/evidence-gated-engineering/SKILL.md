---
name: evidence-gated-engineering
description: Use only when an approved execution plan requires implementing a defined engineering contract and verifying its real behavior.
---

# Execute authorized engineering contracts, do not design them
1. Read `AGENTS.md`, `docs/DECISION_AUTHORITY.md`, applicable accepted ADRs, the exact authorized plan and `docs/VERIFICATION_POLICY.md`.
2. Implement only the externally approved contract for named component/board variants, units, operating conditions and `UNKNOWN` states.
3. Use exact authorized fixtures/independent oracles; never invent a test oracle or change a physical constant to pass a test.
4. If a new mathematical model, unapproved dependency or changed architecture is needed, STOP and file a BLOCKED report.
5. Record actual tests, exact file manifest and limits in `reports/<TASK_ID>-REPORT.md`. No self-approval or next-task selection.
