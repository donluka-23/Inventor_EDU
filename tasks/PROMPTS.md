# Copy-ready Codex prompt — execution only

## First session: narrow bootstrap authorization
Execute only `BOOT-001 rev 1` from `tasks/BOOT-001.md`. First read `AGENTS.md` and the mandatory governance files and output a BOOT BRIEF. Follow the task's write allowlist. Do not research, propose architecture, create code, install dependencies, or edit any other file. Run the exact preflight checks, write `reports/BOOT-001-REPORT.md` using the template, then provide the report's full Markdown and exact path. If the plan conflicts with the repo, stop and report BLOCKED; do not improvise.

## For EVERY future task
Execute only `<TASK_ID> rev <REV>` described in `tasks/<TASK_ID>.md`, explicitly authorized in this message. Read `AGENTS.md`, all required governance documents, the approved task and referenced accepted ADRs; emit BOOT BRIEF, then implement only the approved scope. Treat missing architecture decisions, unexpected required dependencies, model uncertainty or scope conflict as STOP/BLOCKED, not as an invitation to design. Complete `reports/<TASK_ID>-REPORT.md` with exact changed files, observed tests and failures. Return the full report text so it can be reviewed in the separate architecture conversation. Do not choose or start the next task.
