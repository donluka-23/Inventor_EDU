# Frozen execution plans — ONLY authored/approved outside Codex

A plan may be drafted in the separate architecture/research conversation and approved by the owner. Codex is **not authorized to prepare a new implementation architecture or plan**, replan it, or broaden it. `tasks/EXECPLAN_TEMPLATE.md` is an authoring template for the owner/architecture conversation, not an instruction to Codex to invent work.

A valid authorized plan names TASK_ID and REVISION, exact objective, file allowlist, read sources, prerequisites and accepted ADRs, fixed interfaces/algorithms/units, concrete acceptance fixtures and oracles, required test commands, forbidden modifications, external dependencies/license approvals, stop conditions, rollback, and report path.

If no approved plan is given in the user's Codex message, do not implement. If the task cannot meet its acceptance criteria as written, stop and produce a BLOCKED report. Codex may make local non-semantic implementation choices within the agreed boundaries only.
