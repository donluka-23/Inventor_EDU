# BOOT-001 (revision 1) — new-repository governance verification

**Type:** execution-only, no feature code. **Owner authorization required:** user must explicitly instruct Codex to execute `BOOT-001 rev 1`. The existence of this file is NOT authorization.

## Exact result
Produce a factual repository boot report proving the governance scaffold is readable and structurally valid. No research, design choice, code architecture or dependency installation.

## Read these
`AGENTS.md`, `README.md`, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/SESSION_PROTOCOL.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, `tasks/BOOT-001.md`, `reports/REPORT_TEMPLATE.md`, `scripts/preflight.py`.

## Allowed writes
- `reports/BOOT-001-REPORT.md` ONLY.

## Prohibited
Application code creation; library installation; external research; ADR changes; editing any other file; proposing new architecture; changing roadmap/status/backlog; git commit or remote operations.

## Steps
1. Emit BOOT BRIEF with task ID/revision and no-code scope.
2. Run `python scripts/preflight.py` (use equivalent `py -3` only if `python` unavailable; record exact invocation).
3. Run `git status --short` only if repo is initialized; record observation. Do not initialize Git.
4. Verify from actual files that the initial product is Georgian-first educational wiring verification and that no implementation has been claimed.
5. Write report using specified template, include preflight output and any missing/inconsistent files.

## Acceptance
- Report file exists with every required section populated.
- Verbatim preflight terminal outcome recorded, whether PASS or FAIL.
- No file changed other than `reports/BOOT-001-REPORT.md`.
- No dependency or new design chosen.

## If blocked
Stop and report missing source files or failed preflight; do not fix without new authorized task.
