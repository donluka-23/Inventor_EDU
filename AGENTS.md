# Codex execution rules — INVENTOR EDU

## Authority boundary (MANDATORY)
This repository builds a Georgian-first, novice-facing educational electronics workspace. Codex is an **implementation agent only**. Product discovery, scientific research, architecture, standards/model selection, license-policy decisions, technical trade-off decisions, and next-stage prioritization are made by the product owner with their separate architecture/research conversation; they are **not delegated to Codex**.

Codex MUST NOT independently:
- create, accept, amend or supersede architecture decisions (ADRs);
- choose/replace an engineering data model, simulator, solver, front-end framework, language, database or deployment approach;
- research competitors, define product strategy, determine requirements, or pick next development tasks;
- install/copy/add third-party source, artifacts, models, datasets or dependencies without explicit approved task scope and OSS approval;
- change the task scope or redesign a flawed assignment to make it executable;
- silently fix a missing engineering assumption with guessed data, AI-generated electrical constants, mocked simulator outputs, or unsupported claims.

Codex MAY make low-level local implementation choices (naming, formatting, internal decomposition) **only if** they remain within the authorized plan, accepted ADRs and acceptance tests. If an engineering or architecture question blocks safe execution, stop the affected work and produce a BLOCKED report; do not invent a solution.

## Each session — mandatory preflight
1. Read this file, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, and `docs/SESSION_PROTOCOL.md`.
2. Read the **single task plan explicitly authorized by the user's latest Codex message**, plus the named documents/files in that plan. `tasks/NEXT.md` is advisory and **is not authorization**.
3. Before editing, display a short BOOT BRIEF: task ID/revision, allowed/forbidden paths, required tests, referenced accepted ADRs, unresolved blockers. Confirm the task matches current repository state. Without an explicit authorized task, stop after the BOOT BRIEF.
4. Never treat provisional reference documentation or a PROPOSED ADR as permission to implement it. In case of conflict, follow the stop-and-report procedure.
5. Follow the mandatory Git and documentation lifecycle in `docs/SESSION_PROTOCOL.md`, including reviewing relevant prior reports, preserving existing work, and verifying synchronization.

## Execution discipline
- One authorized task per session; no opportunistic refactor or speculative feature.
- Honor the plan's file allowlist, non-goals, inputs/outputs, error semantics, time/model assumptions, acceptance oracles, and license gate.
- Before a potentially destructive command, check its explicit authorization. Never delete/change files outside the plan's allowlist. No secrets in Git.
- Engineering findings distinguish `PASS`, `FAIL`, `UNKNOWN`, `NOT_APPLICABLE`; absence of evidence never means `PASS`. ERC success does not imply physical safety. Full MCU or physics simulation is not implied by visual wiring.
- When a plan authorizes electrical work: pin/board variant, units, operating conditions, source revision and supported range must be traceable. No unverified hardware-limit substitutions.
- Tests must check real behavior. Avoid output hardcoding, false green tests and inflated demo claims. Run only tests/commands appropriate to the authorized plan.

## Mandatory end-of-session output
- Write a **single complete report** to `reports/<TASK_ID>-REPORT.md`, using `reports/REPORT_TEMPLATE.md`. Report must include scope and actual file changes, commands and observed results, acceptance-by-criterion PASS/FAIL/NOT_RUN/BLOCKED, evidence, model/coverage limitations, unexpected issues, and decision requests.
- Do not change `docs/DECISIONS.md`, ADR status, `tasks/NEXT.md`, `docs/PRODUCT.md`, `docs/REFERENCE_ARCHITECTURE.md`, `docs/OSS_POLICY.md` or other policy/architecture documents unless that exact change is specifically prescribed in the authorized plan and approved by the product owner.
- Update `docs/STATUS.md` and `tasks/WORK_LOG.md` **only if explicitly allowlisted in the authorized plan**; record verified facts only, never forecasts or presumed acceptance.
- In the final Codex response, give the exact report path and include its full Markdown content (or explicitly instruct the owner to attach/paste that report in their architecture conversation). Codex cannot automatically upload a local report into a separate conversation.
- A report documents execution; it does **not** approve the outcome or authorize the next task. The owner/research conversation reviews it before a new plan is issued.
- Before committing, reconcile permitted tracking documents with the evidence and record any factual updates that require separate authorization. Commit and push reviewed task changes under the session protocol.

## Project safety & product boundary
First promise: a carefully bounded, source-grounded interactive wiring checker with Georgian explanations for supported beginner electronics components. The engineering core precedes UI embellishment. No mains-power use cases; no unsupported claims of safety, accuracy, emulator coverage or commercial superiority.
