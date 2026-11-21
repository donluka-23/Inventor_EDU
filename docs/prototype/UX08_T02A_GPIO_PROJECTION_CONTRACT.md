# UX08-T02A GPIO terminal projection contract

Authority is the frozen [UX08-T02A Rev 1.1 handoff](../../tasks/UX08-T02A.md). See the [execution report](../../reports/UX08-T02A-REPORT.md) for acceptance evidence.

## Public interface

Import `project_gpio_terminal(topology, report, terminal)` and `serialize_gpio_terminal_inspection(value)` from `inventor_edu.ui_projection`. The inputs are the exact native `TopologyResult`, `GpioVerificationReport`, and `TerminalRef` classes. The returned `GpioTerminalInspection` is a frozen `Record` with schema version `ux08-t02a-v1`, the selected terminal, the native net ID and member tuple, the report's snapshot/catalog/fact-set digests and ruleset version, and a tuple of tagged records.

Each `GpioFindingProjectionItem` has kind `GPIO_FINDING` and wraps a complete native `GpioFinding`. Each `GpioCoverageProjectionItem` has kind `GPIO_COVERAGE` and wraps a complete native `GpioCoverage`. Both retain `finding_id`. Only the finding payload carries `status` and `severity`. Claim IDs, prerequisites, operating state, scope, and rule metadata stay native. Selection uses exact terminal equality. Ordering uses `(requirement_id, rule_id, kind, finding_id)`.

`net_id` and `net_members` are copied from the supplied topology. An empty `records` means the supplied report has no rows for the selected terminal. Serialization calls the existing `canonical_json(value.model_dump(mode="json"))` and returns UTF-8 bytes. `GpioTerminalInspection.model_validate_json` can read those bytes for canonical reserialization.

## Error precedence

`ProjectionInputError.code` carries the first applicable error. The exception message is the code alone.

| Order | Code | Condition |
| --- | --- | --- |
| 1 | `PROJECTION_INVALID_INPUT` | Wrong exact input type or strict native validation failure, including a forged nested ruleset. |
| 2 | `PROJECTION_SNAPSHOT_MISMATCH` | Native topology and report snapshot digests differ. |
| 3 | `PROJECTION_TERMINAL_NOT_IN_TOPOLOGY` | The selected key is absent from the native terminal-to-net mapping. |
| 4 | `PROJECTION_INCONSISTENT_TOPOLOGY` | An inspected net or its terminal membership is missing, inconsistent, or ambiguous. |
| 5 | `PROJECTION_INCONSISTENT_NATIVE_RECORD` | A structurally valid record disagrees with the report digests, names a missing topology terminal, or gives the wrong affected net. |
| 6 | `PROJECTION_DUPLICATE_RECORD_ID` | A record ID repeats anywhere across native findings and coverage. |

Consistency checks include all report records before selection. Topology checks cover the selected net and the nets of mapped report terminals. Strict revalidation is recursive. The current native ruleset literal accepts only `gpio-capability-v1`.

## Evidence boundary

The source-backed DEMO-001 fixture is test-only. A GPIO direction finding is scoped to the native requirement. Electrical compatibility stays a separate coverage record. The projection checks agreement within the given inputs. Independent catalog trust, report authenticity, freshness, electrical or firmware behavior, and physical safety are outside this contract. `TopologyResult` supplies a snapshot digest and has no catalog digest. Source claim IDs are preserved without lookup.
