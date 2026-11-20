# CORE-001C-E1 revision 1 execution report

- Date — 2026-11-20, Asia/Tbilisi.
- Frozen task — [CORE-001C-E1 revision 1](../tasks/CORE-001C-E1.md).
- Recommendation — **PASS** for the isolated, test-only ideal divider and conditional HIGH margin calculation. Hardware compatibility and physical network provenance remain unestablished.
- Verified predecessor — `origin/codex/chat-001-local-learning-session` at `ebb373fef5d4506d4ffd382d421f4a4712a59a13`.
- Task branch — `codex/core-001c-e1-voltage-math` on `https://github.com/donluka-23/Inventor_EDU.git`.

## A. BOOT BRIEF

Confirmed the clean working tree, live predecessor SHA and correct origin. Verified Research F–I are tracked and archival commit `f66d9af3db5fad3de878fbad3d45b06ee77c4ea4` is in predecessor history. Accepted ADR-0001 applies. Examined repository governance, including AGENTS.md, decision authority, session protocol, OSS and verification policies, decision index, product/status/next-task records, master plan and evidence-gated-engineering skill. Read the existing CORE topology and fixture APIs, CORE-001B source/rule ledger and Research C sections covering the approved mathematical and evidence boundary. Independent fraction arithmetic agreed with the frozen interval oracle. No engineering blocker was open.

Allowed writes covered the isolated module, tests, example, contract, frozen task, report and specified tracking changes. Existing topology, GPIO, CAP/SYN/EDU/CHAT, tests, catalogs, source ledgers, research and locks were outside the write scope. The bounded API adds exact rational result records and an optional digest association through the existing CORE computation. Required gates were E1-01–18, full regression, authentic GPIO admission, two replay runs and measured runtime. The optional load model was omitted.

## B. Implemented model and provenance

`evaluate_ideal_divider(hypothesis: IdealDividerHypothesis) -> VoltageModelReport` is a stateless calculation. The immutable request carries the explicit unloaded DC model scope, parameter relationship, applied voltage range, ordered resistor ranges and tolerances, linked assumptions, optional HIGH requirement, and optional snapshot association. `SnapshotAssociation.from_core(catalog, snapshot)` obtains the two digests after real CORE validation and computation. Direct typed association fields express a reference. Neither path proves a model resistor is physically represented.

KCL gives equal resistor currents. KVL gives `I = Vin/(Rtop + Rbottom)` and `Vout = I × Rbottom`. For independent nonnegative voltage and positive resistance bounds, Vout increases with Vin and bottom resistance and decreases with top resistance. The required extreme values follow from those monotonicities. The independent test enumerates all eight corners using node conductances, `(Vin/Rtop)/(1/Rtop + 1/Rbottom)`. Declared correlations without an admitted joint envelope produce INDETERMINATE and omit both the output and margin. A missing threshold leaves the HIGH margin NOT_EVALUATED.

Explicit V/mV and ohm/kΩ units are converted exactly. Numeric inputs use finite bounded decimals, including explicit percentage tolerance. The calculation and comparison use reduced rational numbers. Display uses exact round-half-to-even at 12 decimal places. The test exercises ties, a negative margin whose display rounds to zero, exact equality and independence from the ambient Decimal precision. An exact zero satisfies the assumed inequality. Every result links to the declared inputs, provenance, ordered derivation, version and digest. Field and provenance order alone do not change the digest.

| Input or source | Role in this task |
| --- | --- |
| 5 V nominal and 4.5–5.25 V interval | Explicit applied-voltage hypotheses authorized by E1. The interval is not a manufacturer guarantee. |
| 10/10 kΩ or 6.8/10 kΩ, plus ±1% where specified | Proposed resistance inputs. No canonical resistor instances or actual resistor measurements were admitted. |
| 2.55 V required HIGH | Assumed model comparator from `0.75 × 3.4 V`. Applicability of a threshold formula at this supply condition is unestablished. |
| Adafruit #3942 description | Retail context only. Local catalog S22 identifies the Product 3942 listing and S23 identifies the pinout edition edited 2024-03-08. Research C S03 records the Echo seller description and locator. It provides no maker-guaranteed VOH_min or VOL_max envelope. |
| Espressif module supply entry | Research C S01 records ESP32-WROOM-32E/32UE datasheet v2.1, §6.1 Table 13. The module VDD33 supply entry is contextual and supplies no GPIO pin absolute limit. No electrical numeric datasheet value was imported as a device fact. |
| Existing CORE-001B ledger | Documents GPIO direction and source scope using ESP-IDF v5.5.6 at `880a203ae603d08a94d06aa01e0d6761958e5e9e` and board guide `da43a78cfdd2a1122047bb5617ca79e09fd687b2`. GPIO19 direction has no admitted Echo compatibility verdict. |

No new hardware source was admitted. Each numerical input requires a `MODEL_ASSUMPTION` binding. Manufacturer, retailer and measurement declarations are contextual and cannot confer electrical authority. The associated scenario used catalog `sha256:356732040b6bd762e8c604ae63c3600df5da225cc938af6dff688b25aad4c57b` and snapshot `sha256:6fe1964503bdc98e1c3f82bd6c817ed92d0cef800b73734c7c11518d10a1a230`. CORE computation confirmed the fixture contains only the board and sensor instances, with the existing Trig/Echo conductors. The sidecar emits `NETWORK_PHYSICALLY_REPRESENTED=NOT_ESTABLISHED` and asserts no canonical resistor net membership. B's existing `ELECTRICAL_COMPATIBILITY=NOT_EVALUATED` is unchanged.

## C. Demonstration and independent observations

| Model case | Exact Vout in V | Exact conditional margin in V | Rounded display |
| --- | --- | --- | --- |
| 5 V, 10 kΩ top, 10 kΩ bottom | 5/2 | −1/20 | 2.500000000000 V, −0.050000000000 V |
| 5 V, 6.8 kΩ top, 10 kΩ bottom | 125/42 | 179/420 | 2.976190476190 V, +0.426190476190 V |
| 4.5–5.25 V, 6.8/10 kΩ with both at ±1% | [22275/8384, 53025/16832] | 4479/41920 | [2.656846374046, 3.150249524715] V, +0.106846374046 V |

The swapped oracle produced 85/42 V. The synthetic non-ESP32 case produced exactly 8 V with a 1 V model margin and no board association. A negative modeled margin does not establish a real LOW. A positive modeled margin does not establish a hardware HIGH.

Each demo report emitted four INDETERMINATE scopes, three NOT_EVALUATED scopes and one NOT_ESTABLISHED scope. Across three cases this was **24 unclosed findings** and **zero false hardware PASS**. Hardware HIGH lacks maker VOH_min under load, applicable receiver VIH and exact board state. LOW lacks maker VOL_max and applicable VIL. Applicability lacks exact unit/variant, loading, configuration, supply and temperature evidence. Pin stress lacks pin-specific absolute input limits and clamp/injection limits. Source drive, power-off and transient physics remain unevaluated. Physical-network provenance requires verified resistor instances and terminal topology. The demonstration emits `NOT_PROVEN_HARDWARE_COMPATIBILITY` and lists these gaps.

| Gate | Observed result | Status |
| --- | --- | --- |
| E1-01 | Equal resistors yield exact 5/2 V. | PASS |
| E1-02 | 6.8 kΩ above 10 kΩ yields exact 125/42 V. | PASS |
| E1-03 | Swapping ordered resistances yields exact 85/42 V. | PASS |
| E1-04 | Both exact bounds match independent exhaustive KCL corner check. | PASS |
| E1-05 | Negative margin is exact −1/20 V and provides no real LOW evidence. | PASS |
| E1-06 | Positive margin uses the requirement's upper endpoint and stays conditional. | PASS |
| E1-07 | Exact zero, negative sub-display margin and half-even tie cases agree. | PASS |
| E1-08 | V/mV and ohm/kΩ equivalence. Cross-dimensional units reject. | PASS |
| E1-09 | Missing maker VOH_min keeps HIGH indeterminate. Retail-to-input promotion rejected. | PASS |
| E1-10 | VDD33 supply context cannot establish GPIO pin stress. | PASS |
| E1-11 | Malformed, nonfinite, negative, zero-resistance, wrong-scope and oversized inputs reject. | PASS |
| E1-12 | HIGH, LOW, applicability and unsupported physics remain distinct. | PASS |
| E1-13 | Correlation abstains from rectangular extrema. | PASS |
| E1-14 | Synthetic receiver reproduces independent 8 V and 1 V oracles. | PASS |
| E1-15 | Reordered input/metadata stable. A changed assumption alters the trace digest. | PASS |
| E1-16 | A different real CORE snapshot changes association and digest while preserving the math. | PASS |
| E1-17 | CORE fixture contains board and sensor only. Physical divider remains unestablished. | PASS |
| E1-18 | No electrical acceptance symbols, including with an unadmitted guarantee. Full regression passes. | PASS |

## D. Commands, replays and runtime

Run in `D:\Inventor_EDU` using the existing installed pinned environment. The observed interpreter was Python 3.12.8. Installed packages matched the locks, including Pydantic 2.14.4, pydantic-core 2.50.5, NetworkX 3.7 and Hypothesis 6.170.17.

```powershell
$exe=Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$src=Join-Path $env:TEMP 'InventorEDU-CORE-001B-01-sources'
$env:INVENTOR_EDU_DATA001_SOURCE_DIR=Join-Path $env:TEMP 'InventorEDU-DATA-001-dc037a238eb5efcc034dd9d62e5775d5c21e90e4'
$env:HYPOTHESIS_STORAGE_DIRECTORY=Join-Path $env:TEMP 'InventorEDU-E1-hypothesis'
& $exe --version
& $exe -m pip list --format=freeze
& $exe -B -m unittest tests.test_core001c_e1_voltage_model -v
& $exe -B -m unittest discover -s tests -v
& $exe -B -m tests.gpio_source_acceptance $src
& $exe -X utf8 -B -m examples.core001c_e1_voltage_cases
& $exe -X utf8 -B -m examples.core001c_e1_voltage_cases --json
```

```text
Ran 18 tests in 0.059s
OK
Ran 145 tests in 7.687s
OK
PASS: five authentic artifacts matched pins; masks, pull-up, header, flash, strap and -32E scope checked
```

All three acceptance commands exited 0. All 145 tests passed, including CHAT, EDU, SYN, CAP, both CORE fixtures and authentic DATA. There were zero test failures, skips or blocks. Authentic GPIO admission was a separate exit-0 gate.

A Python `subprocess.run` harness ran each CLI mode twice, asserted byte equality on stdout, measured with `perf_counter` and calculated SHA-256. All four subprocesses exited 0 with empty stderr.

| Mode | Observed times | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Summary | 485.3, 469.2 ms | 1,698 | `582bb25d6e452965331bf1b6d9357320bc3a180cd0cdb4befa4e09ac59952594` |
| JSON | 466.1, 447.2 ms | 23,019 | `e950ac622c987618996933136e7739012dfb8625b6d85d00b84afec012b4581d` |

With fixture loading excluded, `timeit.repeat(lambda: evaluate_ideal_divider(case), repeat=5, number=1000)` gave nominal batches of 0.433409, 0.489881, 0.418055, 0.441029 and 0.445674 s. The interval batches took 0.427698, 0.457104, 0.461813, 0.469310 and 0.503561 s. The observed medians were 0.441 ms per nominal call and 0.462 ms per interval call. These measurements include per-call validation, exact arithmetic, packaging and hashing on this Windows host.

## E. File manifest and remaining scope

| Path | Change |
| --- | --- |
| `inventor_edu/voltage_model.py` | Added isolated immutable request, exact arithmetic and scoped evidence outputs |
| `tests/test_core001c_e1_voltage_model.py` | Added 18 independent oracle methods |
| `examples/core001c_e1_voltage_cases.py` | Added deterministic neutral summary and UTF-8 JSON |
| `docs/prototype/VOLTAGE_MODEL_E1_CONTRACT.md` | Added typed contract, precision and replay |
| `tasks/CORE-001C-E1.md` | Added frozen task |
| `reports/CORE-001C-E1-REPORT.md` | Added execution evidence |
| `docs/STATUS.md`, `tasks/NEXT.md`, `tasks/WORK_LOG.md` | Recorded observed progress and pending review |
| `docs/prototype/MASTER_PLAN.md` | Advanced 1.4 to 1.5 and added the model-only substep |

Preserved the full CORE-001C gate and all deferred UI, review and downstream restrictions. No locks, engines, old tests, policy, source or language records changed. No dependency, vendor asset or new electrical data was added. CHAT visual/browser automation and Georgian language review retain their previous status. Full electrical acceptance, loading, correlated joint envelopes, pin stress, source drive, power-off, transient analysis and real hardware validation remain outside this E1 task. No implementation contradiction requires an owner decision. Owner acceptance of this bounded result is pending.

## F. Git publication

Pushed implementation commit `e1d23b75307bf627d16a8c71d6f10ba66d118f8a` with `git push -u origin codex/core-001c-e1-voltage-math`. The live `git ls-remote` and fetched task branch matched that exact SHA. The fetched history contained the CHAT predecessor and research archival commit. The four research blobs matched the archived originals. Remote `main` remained at `b1db3e947d04508ca22d4ba55e3172616620bad2`. Verified the ten-path allowlist, frozen task bytes, staged whitespace and credential patterns, documentation links and the protected master-plan content. This report-only follow-up records the publication.
