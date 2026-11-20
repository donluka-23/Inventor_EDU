# Decision rights and escalation — approved governance rule

## Roles
- **Owner + research/architecture conversation:** research, product scope, data-model comparison, mathematics/physics choices, dependency/license acceptance, architecture and API contracts, milestones, risk acceptance, task plan preparation, task approval, and report adjudication.
- **Codex:** execute one frozen approved task; run checks; document factual findings; report blockers. No product or architectural discretion.

## Decision classes
| Class | Examples | Codex action |
| --- | --- | --- |
| A — Owner/architect decision | Canonical circuit schema, solver selection, UI framework, electrical correctness policy, third-party license acceptance, expanded scope | STOP and report a decision request; never self-approve |
| B — Plan-level technical detail | Exact API type, algorithm, validation behavior or allowed dependency specified in authorized plan | Implement exactly and test |
| C — Local implementation detail | Local variable names, file-internal helpers, non-semantic refactoring within allowlist | May decide, document material details |
| D — Discovery during implementation | Undocumented board variant, conflicting datasheet, incompatible library license, model cannot express scenario | Mark BLOCKED/UNKNOWN, preserve evidence, no scope expansion |

## Binding authority order
1. Explicit latest owner instruction authorizing **one** task ID and revision.
2. This file and `AGENTS.md`, which Codex cannot weaken itself.
3. Accepted ADRs and product boundary documents.
4. Authorized task execution plan.
5. Provisional/reference documentation and task backlog (non-binding without approval).

Conflicts or ambiguity: stop affected work, do not infer an override. A new decision must be made in the architecture conversation, approved by owner, and then transcribed in a separately authorized documentation task or the next plan.

## Definition of 'architecture change'
Any new externally visible behavior, persistent data semantics, physical model class, source/license dependence, framework/deployment decision, contract change, or modification of verification authority. Such changes require a new approved plan or explicit change to the current one from the owner. Codex must not propose a replacement implementation as if it were adopted.
