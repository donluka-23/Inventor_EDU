# CORE-001C-E2 revision 1 execution report

- Date — 2026-11-21, Asia/Tbilisi.
- Frozen task — [CORE-001C-E2 revision 1](../tasks/CORE-001C-E2.md).
- Recommendation — **PASS** for the isolated, test-only virtual motif and conditional model binding. Hardware compatibility and actual component values remain unproven.
- Verified predecessor — `origin/codex/core-001c-e1-voltage-math` at `7d60e6e8143030c4ec32ad69ae3c19225f474546`.
- Task branch — `codex/core-001c-e2-divider-topology`.

## A. BOOT BRIEF

Fetched the authorized origin `https://github.com/donluka-23/Inventor_EDU.git`, verified live predecessor HEAD, inspected the clean worktree, and verified that Research F–I matched the blobs in archival ancestor `f66d9af3db5fad3de878fbad3d45b06ee77c4ea4`. Created one branch from that predecessor. Accepted ADR-0001 applies. No CORE schema or source-admissibility contradiction was identified. The archived research stayed read-only.

Read AGENTS.md, product/status/next-task records, decision authority/index, session protocol, OSS policy, verification policy, ADR-0001, master plan 1.5 and the evidence-gated-engineering skill. Inspected CORE models and APIs, the actual `DeviceDefinition.device_class` identifier, the E1 implementation, fixtures and report, DATA-001 report, CORE-001B source/rule ledger and Research C §4, §§9–10.2 and §17.1. The plan allowed the isolated adapter, fixture in the example, tests, contract, frozen task, report and specified tracking changes. Existing implementations, tests, catalogs, ledgers, research, policies and locks were outside the write scope.

## B. API, authority and evidence

```python
bind_ideal_divider_to_snapshot(
    catalog: CatalogSnapshot, snapshot: CircuitSnapshot,
    binding: DividerTopologyBinding, hypothesis: IdealDividerHypothesis,
) -> DividerTopologyReport
```

The versioned immutable binding carries the catalog and snapshot digests, test-only qualification and seven `TerminalAnchor` fields. Each pins a physical `TerminalRef` and the exact owner definition digest. The report contains observed anchor identity, CORE net IDs, complete members and connection IDs on the role nets, per-rule reason codes, prerequisites and separate binding/hypothesis hashes. Its optional `model_report` and `model_digest` come from E1 only after the structural checks and current E1 association pass. Invalid typed records or invalid CORE graphs raise existing validation errors.

| Authority | Evidence used | Claim boundary |
| --- | --- | --- |
| CORE | Catalog admission, real snapshot, actual conductors and junctions, qualified internal ideal ties, `compute_nets(catalog, snapshot)` | Canonical virtual net membership |
| E2 | Seven exact role bindings, two distinct synthetic resistor instances and the three-net partition | The bounded motif exists in the virtual graph |
| E1 | Explicit ideal unloaded DC hypotheses and exact association | Conditional arithmetic. Its own physical network provenance stays NOT_ESTABLISHED. |
| Existing B GPIO sources | Original pinned board/sensor catalog and fact set only | No authority for the recomposed catalog. The test rejected both original-pin reuse and composite-pin substitution with the old fact set. |
| DATA-001 | Independent generic LibrePCB two-terminal structural precedent | The held manufacturer-specific YAGEO match was neither imported nor used as evidence. |

The admitted in-memory catalog `sha256:b99c6082d3f3eaea7d21828f569fda4577073275634a50db225cfb99c947d419` preserves the exact reviewed DevKitC-32E and Adafruit #3942 definitions, claims and sources. Its only additional definitions are synthetic `e2-top-resistor` at `sha256:ee44701ef6a678388799d87e706f788794e05f320d2033814e3eb7260883f607` and `e2-bottom-resistor` at `sha256:e5b1150ad701cb03426d7fe29d6d7fec5260c464cf736a079bc51f7809a3e193`. The existing catalog's canonical payload matched its original digest before composition. The new digest was derived locally and checked through public CORE admission. It is a test fixture pin. No fallback was needed for the primary demo.

Each resistor is an ordinary virtual component with two contacts, no ideal tie, and synthetic identity. The 5 V applied input, 6.8 kΩ top, 10 kΩ bottom, ideal unloaded behavior and 2.55 V threshold are inherited E1 assumptions. Actual resistance, tolerance, material and receiver leakage/pulls were not admitted. Source drive, power-off and transient behavior remain separate NOT_EVALUATED obligations. Hardware qualification is `HARDWARE_COMPATIBILITY_NOT_PROVEN` throughout.

| E2 check | Positive and independent oracle | Counterexample or uncertainty |
| --- | --- | --- |
| BINDING_IDENTITY | Current catalog and CORE snapshot pin | Stale catalog or snapshot rejects |
| ROLE_IDENTITIES | Exact bound instance, definition digest and physical terminal IDs | Missing instance, wrong digest, nonexistent terminal, duplicate anchoring or inappropriate ground rejects |
| RESISTOR_BODIES | Two different, two-terminal test bodies with endpoints on different CORE nets | One arm split across instances, shared body, or resistor terminals shorted rejects |
| VIRTUAL_NET_PARTITION | Explicit three-member-set oracles below | Receiver or return moved to source rejects. Three bypass paths reject. |
| UNLOADED_NET_SCOPE | Only specified contacts plus the receiver's CORE-established internal ground aliases | Extra source, midpoint or ground contact leaves scope unresolved, including a midpoint rail |
| E1_MODEL_BINDING | Current CORE association and valid independent E1 hypothesis | Missing/stale association and correlated input leave math withheld |

## C. Observed wiring changes and recovery

The independently specified and observed Case A member sets were:

| Role group | CORE net SHA-256 | Exact terminal members | Connection IDs |
| --- | --- | --- | --- |
| Source | `9271e79c9df2dddace5c3fef6a2ab6fb5d48aebe807eab93f10d9ea259ce745b` | `T:r-top/high`, `T:sensor/Echo` | `source-wire` |
| Midpoint | `065b3aa7947eecc1dfef44f9838d7e20cb8231ef1b2c969148eed08c8b259eb2` | `T:board/J3.8`, `T:r-bottom/high`, `T:r-top/low` | `mid-receiver`, `mid-series` |
| Ground | `a96c83888da87bcaf70b871e4a3645e6a4ad4e3fb1220b17dcdfcbceb37ae3af` | `T:board/J2.14`, `T:board/J3.1`, `T:board/J3.7`, `T:r-bottom/low` | `ground-return` |

The ground aliases remained connected in a receiver-only CORE snapshot with no external conductors. The additional Trig wire is on a separate net. An explicit CORE junction in a test preserved the midpoint terminal set. Reversing conductor endpoints and order preserved the entire E2 report.

| Demo | Snapshot SHA-256 | Actual outcome |
| --- | --- | --- |
| A correct | `90aba65d17694a237b64c5d2f368f2113345b0fcf3cd1f05f04f47c886fcc59f` | CANONICAL_MOTIF_MATCHED, MATH_EXECUTED_CONDITIONALLY |
| B1 receiver on source | `2ed8438866ee71d3a3caa3f9840a59279806ee8314683fe0299fab6e23c8bbd2` | MID_NET_OPEN_OR_MISROUTED, MATH_WITHHELD |
| B2 return on source | `6c87634f41df19d0ac5be19e71248359c9e76bfa1e673d1b8a0d96bca501ff94` | GROUND_NET_OPEN_OR_MISROUTED, MATH_WITHHELD |
| A restored | `90aba65d17694a237b64c5d2f368f2113345b0fcf3cd1f05f04f47c886fcc59f` | The full original report and E1 model digest recovered |

B1 moved `mid-receiver` to the source. CORE observed source members `T:board/J3.8`, `T:r-top/high`, `T:sensor/Echo` and midpoint members `T:r-bottom/high`, `T:r-top/low`. B2 moved `ground-return` to the source. CORE observed source members `T:r-bottom/low`, `T:r-top/high`, `T:sensor/Echo` and the board-only internal ground group `T:board/J2.14`, `T:board/J3.1`, `T:board/J3.7`. Both reports listed the affected net IDs and their real conductor IDs. Neither called E1 or retained Case A's result. Old topology tokens also failed against new wiring.

At A and A restored, unchanged E1 returned exact **125/42 V** and a conditional HIGH margin of **179/420 V**, displayed as 2.976190476190 V and +0.426190476190 V. Calculation digest `sha256:fe5a9daa4fbe2934f2f32f9329f2d022091897656180bf05024100ed68a52aa2` was identical after restore. The synthetic non-ESP32 fixture independently matched using differently named instances and terminals. Hardware compatibility remained unproven in every case.

## D. Independent acceptance

| Gate | Observation | Result |
| --- | --- | --- |
| E2-01 | Seven exact physical identities with verified owner definition pins | PASS |
| E2-02 | Two distinct synthetic two-terminal resistor bodies | PASS |
| E2-03 | Three distinct canonical net IDs and explicit expected member sets | PASS |
| E2-04 | Resistor ends remain on separate CORE nets | PASS |
| E2-05 | Virtual motif success leaves material, actual values and hardware unproven | PASS |
| E2-06 | E1 is called once with the same hypothesis and returned unchanged | PASS |
| E2-07 | Two true endpoint mutations reject and never call E1 | PASS |
| E2-08 | Source-mid, mid-ground and source-ground bypasses reject | PASS |
| E2-09 | Missing return and non-ground reference reject | PASS |
| E2-10 | Missing, duplicate, cross-instance or wrong-pin anchors/graph reject | PASS |
| E2-11 | Wrong topology digests and missing/stale model association cannot attach math | PASS |
| E2-12 | Unreviewed midpoint load and powered contact withhold math | PASS |
| E2-13 | Unknown source and extra ground contacts withhold math | PASS |
| E2-14 | Wire order and endpoint reversal stable. Benign junction accepted. | PASS |
| E2-15 | Changed wire rejects stale association. Real restoration recovers results. | PASS |
| E2-16 | Changed resistance assumption changes E1 digest and preserves evidence limits | PASS |
| E2-17 | Differently named synthetic source/receiver/passives run the same adapter | PASS |
| E2-18 | Original GPIO fact set refuses mismatched composite catalog | PASS |
| E2-19 | Negative cases serialize no stale numeric result or hardware acceptance | PASS |
| E2-20 | Final full regression, authentic GPIO admission and deterministic replay pass | PASS on standalone rerun |

## E. Commands, output and elapsed time

Ran from `D:\Inventor_EDU` using the existing pinned environment. Python 3.12.8, Pydantic 2.14.4, pydantic-core 2.50.5, Hypothesis 6.170.17 and NetworkX 3.7 matched the baseline.

```powershell
$exe=Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$src=Join-Path $env:TEMP 'InventorEDU-CORE-001B-01-sources'
$env:INVENTOR_EDU_DATA001_SOURCE_DIR=Join-Path $env:TEMP 'InventorEDU-DATA-001-dc037a238eb5efcc034dd9d62e5775d5c21e90e4'
$env:HYPOTHESIS_STORAGE_DIRECTORY=Join-Path $env:TEMP 'InventorEDU-E2-hypothesis'
& $exe --version
& $exe -m pip list --format=freeze
& $exe -B -m unittest tests.test_core001c_e2_divider_topology -v
& $exe -B -m unittest discover -s tests -v
& $exe -B -m tests.gpio_source_acceptance $src
& $exe -X utf8 -B -m examples.core001c_e2_divider_topology
& $exe -X utf8 -B -m examples.core001c_e2_divider_topology --json
```

```text
Ran 20 tests in 1.190s
OK
Ran 165 tests in 8.678s
OK
PASS: five authentic artifacts matched pins; masks, pull-up, header, flash, strap and -32E scope checked
```

Targeted, standalone full regression and authentic GPIO admission exited 0. The standalone full run had zero failures or skips. The first full run, concurrent with the replay and targeted runs, exited 1 after 20.418 s with one `WinError 10053` socket abort in the pre-existing `HttpTests.test_negative_bodies_and_repeated_forms`. No E2 test failed. Only the identical full-suite command was rerun standalone. The CHAT test and HTTP implementation were outside scope and were left unchanged.

A Python `subprocess.run` harness measured the command in each output mode twice with `perf_counter` and compared raw bytes. All four processes exited 0 with empty stderr.

| Mode | Wall times | Bytes per run | Identical SHA-256 |
| --- | --- | ---: | --- |
| Summary | 530.5, 457.2 ms | 3,429 | `f879b4a341f6e1f4a5e499745cf157fd1c4333c29709a355b0dce43458578c15` |
| JSON | 552.8, 528.3 ms | 44,333 | `5de2f6fa4a5b201a9cb135e6803e23d8104b3a195d7cc350ef851a301f5489ef` |

With the typed inputs prebuilt, five `timeit.repeat` batches of 100 calls took 0.437965, 0.397525, 0.413689, 0.410583 and 0.456987 s for the matched case, and 0.157180, 0.154462, 0.174648, 0.165687 and 0.187486 s for B1. Medians were approximately 4.14 and 1.66 ms per call, respectively, including topology recomputation and result construction. These are local fixture timings.

## F. Manifest and remaining scope

| Path | Change |
| --- | --- |
| `inventor_edu/divider_topology.py` | Added the strict read-only motif adapter |
| `tests/test_core001c_e2_divider_topology.py` | Added 20 independent acceptance methods |
| `examples/core001c_e2_divider_topology.py` | Added in-memory fixture, live endpoint mutations and replay |
| `docs/prototype/DIVIDER_TOPOLOGY_E2_CONTRACT.md` | Added the scoped API and method |
| `tasks/CORE-001C-E2.md` | Added the frozen owner handoff |
| `reports/CORE-001C-E2-REPORT.md` | Added execution evidence |
| `docs/STATUS.md`, `tasks/NEXT.md`, `tasks/WORK_LOG.md` | Updated factual status and pending owner review |
| `docs/prototype/MASTER_PLAN.md` | Advanced 1.5 to 1.6 and added only the E2 row |

Full CORE-001C authorization, prior milestones, fixed non-goals, opportunities and risks remain as recorded. No existing engine, test, source material, dependency, license, local UI or multilingual review record changed. No architecture decision is required for the bounded result. Exact hardware identities beyond the reviewed context, actual resistor data, approved source drive and receiver conditions, electrical acceptance, powered-off behavior and transients remain unverified or outside scope. Owner acceptance is pending.
