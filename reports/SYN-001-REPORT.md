# SYN-001 revision 1 execution report

- Session date — 2026-11-20, Asia/Tbilisi.
- Frozen task — [SYN-001 revision 1](../tasks/SYN-001.md).
- Recommendation — **PASS** for owner review of the bounded headless experiment.
- Live predecessor — `origin/codex/demo-001-scenario-bridge` at `2ece740bb49dfd330cbdecd4981204eb085821dd`.
- Task branch — `codex/syn-001-candidate-generation` on `https://github.com/donluka-23/Inventor_EDU.git`.

## A. BOOT BRIEF

Confirmed the live predecessor, tracking state, authorized origin, and four pre-existing untracked raw Research F–I files. Created the task branch from the verified predecessor. Preflight found no blocker.

Read `AGENTS.md`, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, `docs/SESSION_PROTOCOL.md`, `docs/OSS_POLICY.md`, `docs/VERIFICATION_POLICY.md`, `docs/adr/ADR-0001-product-scope.md`, and the evidence-gated-engineering skill. Read the frozen task, `inventor_edu/models.py`, `inventor_edu/core.py`, `inventor_edu/gpio_facts.py`, `inventor_edu/gpio_verify.py`, `inventor_edu/demo_bridge.py`, `tests/test_demo001_bridge.py`, `docs/prototype/MASTER_PLAN.md`, `reports/DEMO-001-REPORT.md`, and `reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md`. Accepted ADR-0001 and frozen SYN-DEC-01 through SYN-DEC-05 govern this task. ADR-0002 remains on hold.

The authorized write scope was the implementation, test, task copy, contract, report, three factual tracking updates and four specified master-plan edits. Existing engines, engine tests, evidence catalogs, raw research, architecture records, policy, licensing and frontend files were outside the write scope. The acceptance gates were S01–S18, full discovery with authentic DATA-001 inputs, authentic GPIO admission, and headless replay.

## B. Implementation and API compatibility

The public module `inventor_edu.synthesis` defines frozen `SignalRole`, `SynthesisRequest`, `RoleTrace`, `SynthesisCandidate` and `SynthesisResult` records, `SynthesisInputError`, and:

```python
generate_candidates(
    request: SynthesisRequest, catalog: CatalogSnapshot, fact_set: GpioFactSet, *,
    trusted_catalog_sha256: str | None, trusted_factset_sha256: str | None,
) -> SynthesisResult
```

The request carries schema 1.0, a request ID, requirements and catalog digests, two exact instances, two typed roles with originating IDs, functions, sensor refs and physical terminal domains, declared `AllDifferent`, test evidence scope and positive budgets. It uses CORE admission and `resolve_terminal(catalog, snapshot, ref)` to validate instances, definition digests and terminal references. The fixture owner reviews domain membership and source-role semantics. The caller's requirements digest is carried as provenance because the upstream requirements serialization is outside this scope.

Search branches sort by role ID then instance/contact ID. Each attempted terminal consumes one node, including exclusivity prunes. Exact budget use can still exhaust the domain. An unvisited branch yields `SEARCH_INCOMPLETE` and preserves completed evaluations. An empty role domain yields `NO_REVIEWED_DOMAIN`. `max_candidates` retains the first results in traversal order. Evaluation and counts continue after the retention cap. With zero evaluated assignments, a single empty B call validates pins and catalog binding and is included in the verifier count.

Each complete assignment constructs two ideal `Conductor` records. `create_snapshot(catalog, *, instances, junctions, conductors)` canonicalizes the circuit, and `compute_nets(catalog, snapshot)` supplies the snapshot digest and conductor net IDs. The generator invokes `verify_gpio_requirements(catalog, snapshot, fact_set, requests, trusted_catalog_sha256, trusted_factset_sha256)` directly. Each role requests `PIN_MAPPING`, `PHYSICAL_CAPABILITY`, `BOARD_AVAILABILITY`, `ACTIVE_CONFIGURATION` and `ELECTRICAL_COMPATIBILITY` at `ACTIVE`. The complete B report is retained unchanged. The existing DEMO bridge and both core APIs required zero changes.

Classification comes from the first three checks on both roles. Any known hard FAIL rejects. Positive findings for all six hard checks yield `SCOPED_CHECKS_PASSED_WITH_OBLIGATIONS`. Other candidates remain incomplete. Active configuration findings and electrical coverage remain independent of this classification. Power, LED, current-limiting resistors, voltage adaptation and firmware are explicit obligations on every candidate.

## C. Complete file manifest

| Path | Change | Purpose |
| --- | --- | --- |
| `inventor_edu/synthesis.py` | Added | Request, search, CORE/B integration and traces |
| `tests/test_syn001_generation.py` | Added | S01–S18 and reproducible JSON example |
| `tasks/SYN-001.md` | Added | Frozen owner task |
| `docs/prototype/SYNTHESIS_CONTRACT.md` | Added | Public surface, limitations and replay |
| `reports/SYN-001-REPORT.md` | Added | Execution evidence and publication |
| `docs/STATUS.md` | Updated | Verified result and pending owner acceptance |
| `tasks/NEXT.md` | Updated | Pending review and advisory pointer |
| `tasks/WORK_LOG.md` | Updated | Factual execution chronology |
| `docs/prototype/MASTER_PLAN.md` | Updated | 1.1, SYN-001 after DEMO-001, DEMO-002 deferred, approved integration sequence |

The master-plan diff preserves the fixed non-goals, deferred opportunities, risk register and other milestone authorizations. The documentation check aligned the task, status, pointer and report and verified links. Decisions, ADRs, historical reports and OSS records required no edits. The four pre-existing raw research files remained outside the task branch commit.

## D. Headless evidence and acceptance

The test caller explicitly supplies the previously pinned catalog and fact set for documented Espressif ESP32-DevKitC-32E V4 with ESP32-WROOM-32E and the Adafruit SKU 3942 HC-SR04 retail profile. The physical domains are `sensor/Trig → board/{J2.5,J3.19,J3.9}` for `drive/GPIO_OUT` and `sensor/Echo → board/{J3.8}` for `listen/GPIO_IN`. The fixture owner selects contacts from the existing catalog and evidence ledger, including known negative cases.

| Trig contact | Physical capability | Board availability | Candidate classification | Canonical snapshot SHA-256 |
| --- | --- | --- | --- | --- |
| J2.5 / GPIO34 | FAIL `OUTPUT_NOT_CAPABLE` | UNKNOWN | `REJECTED_KNOWN_HARD_FAIL` | `b6ccc23eb87fe910d9127ec7dfdaef68e18aba243af4e9996c4b09abddbf2369` |
| J3.19 / GPIO6 | PASS | FAIL `RESERVED_RESOURCE` | `REJECTED_KNOWN_HARD_FAIL` | `ab0df31ce408d0094e0cebe2d8955c656d9702de7bfb18905e1a2bfd8cce6ba9` |
| J3.9 / GPIO18 | PASS | UNKNOWN | `INCOMPLETE_WITH_EXPLICIT_OBLIGATIONS` | `6fe1964503bdc98e1c3f82bd6c817ed92d0cef800b73734c7c11518d10a1a230` |

J3.8 / GPIO19 passes Echo input direction in every assignment. The full domain exhausts with 4 nodes, 3 evaluations, 2 rejections and 3 verifier calls. Restricting Trig to J3.9 exhausts with 2 nodes, 1 evaluation, 0 rejections and 1 verifier call. It reproduces the same J3.9 snapshot. S09 compares disjoint one-contact domains and verifies distinct snapshots, freshly computed B reports, and disjoint finding IDs.

The J3.9 Trig trace preserves `drive`, `sensor/Trig`, `board/J3.9`, the CORE net `net:sha256:2c9d5e8a7f486a3114cc6737d1363c90147ef602c0490e70f96822919212ee31`, and assignment `sha256:bab11d6375bc79aaf00db3cdb6903365a79758894f5fcc9cabdfa888ba43a8d0`. It contains four original finding IDs, the separate electrical coverage ID `sha256:3fb7fc6d36df201a1ee66346cd104100c12bbad1143a1199081b1aca942b5344`, and claims `board-J3.9`, `map-J3.9` and `silicon-GPIO18`. The JSON also includes both terminal references, all digests, the documented board scope, `ACTIVE`, the generator and pattern versions and the `TEST_ONLY_NOT_PRODUCTION` restriction. B returns electrical compatibility as `NOT_EVALUATED/ELECTRICAL_CHECK_DELEGATED` and firmware context as `UNKNOWN/ACTIVE_CONFIG_UNKNOWN` on the mapped alternative.

| ID | Independent observation | Result |
| --- | --- | --- |
| S01 | Exact profile IDs, three evaluated assignments and rejection of invalid request data | PASS |
| S02 | GPIO34 output FAIL | PASS |
| S03 | GPIO18 output PASS with board availability UNKNOWN | PASS |
| S04 | GPIO19 input PASS | PASS |
| S05 | GPIO6 direction PASS and board reservation FAIL | PASS |
| S06 | Shared exclusive physical contact pruned | PASS |
| S07 | Non-GPIO contact reports missing mapping and label used as contact raises an error | PASS |
| S08 | Two actual wires and expected CORE net members | PASS |
| S09 | Changed assignment calls real B on new snapshot | PASS |
| S10 | Reordered inputs produce equal output | PASS |
| S11 | Budget cutoff retains evaluated results and candidate cap leaves counts intact | PASS |
| S12 | Empty domain distinct from exhausted rejection | PASS |
| S13 | Electrical and firmware remain open | PASS |
| S14 | Wrong pins raise B mismatch errors and absent pins produce B UNKNOWN | PASS |
| S15 | Frozen traces retain original IDs, scope and digest links | PASS |
| S16 | Fictitious MCU produces one rejected and one scoped passing alternative via real A/B with independent synthetic facts | PASS |
| S17 | Identical printed and user labels preserve physical contacts and separate nets | PASS |
| S18 | Only bounded test-scope classifications are exposed | PASS |

## E. Commands, observed output and timing

Commands ran in `D:\Inventor_EDU` with the existing pinned environment:

```powershell
$exe=Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$src=Join-Path $env:TEMP 'InventorEDU-CORE-001B-01-sources'
$env:INVENTOR_EDU_DATA001_SOURCE_DIR=Join-Path $env:TEMP 'InventorEDU-DATA-001-dc037a238eb5efcc034dd9d62e5775d5c21e90e4'
$env:HYPOTHESIS_STORAGE_DIRECTORY=Join-Path $env:TEMP 'InventorEDU-SYN-001-hypothesis'
& $exe --version
& $exe -m pip list --format=freeze
& $exe -B -m tests.gpio_source_acceptance $src
& $exe -B -m unittest discover -s tests -v
& $exe -B -m tests.test_syn001_generation
& $exe -B -c "from timeit import repeat; from tests.test_syn001_generation import reviewed_fixture,run; a=reviewed_fixture(); b=reviewed_fixture(trig=('J3.9',)); print('five 10-call batches, seconds', repeat(lambda:run(a),number=10,repeat=5), repeat(lambda:run(b),number=10,repeat=5))"
```

Python 3.12.8, Pydantic 2.14.4, pydantic-core 2.50.5, annotated-types 0.8.0, typing-extensions 4.16.0, typing-inspection 0.4.5, NetworkX 3.7, Hypothesis 6.170.17 and sortedcontainers 2.4.0 matched the repository locks. pip reported 24.3.1. The authentic GPIO admission and final discovery commands exited 0:

```text
PASS: five authentic artifacts matched pins; masks, pull-up, header, flash, strap and -32E scope checked
Ran 72 tests in 1.521s

OK
```

All 72 methods passed, including 18 SYN, 10 DEMO and four authentic DATA-001 methods. Zero failed, skipped or blocked. The first isolated `& $exe -B -m unittest tests.test_syn001_generation -v` run exited 1 with two `FACTSET_DIGEST_MISMATCH` errors (S16 and S17). The synthetic fixture then supplied its explicit null pull-up field before independent digesting. Final discovery verified both tests.

Two example processes emitted identical JSON, and the measured invocation exited 0 in 364.4 ms including interpreter startup and serialization. With preloaded inputs, five 10-call batches took 150.0–152.9 ms for the three-assignment domain and 63.7–68.6 ms for the one-assignment domain. These measurements describe this fixture and Windows session. Input validation and individual evaluations are outside the search-node count.

## F. Scope, OSS and owner review

The reviewed -32E profile is test-only. Synthetic MCU facts have their own fictitious source and exercise the existing checker without borrowing ESP32 claims. Pins are supplied by the authorized caller. A digest check confirms integrity against a pin and does not establish the pin's provenance. Positive GPIO direction is scoped to the documented hardware and operating state. Electrical compatibility, firmware, power and the physical hardware build remain unverified.

Research H/I parsing, general component matching, the H→I→J crosswalk, Georgian explanation generation, the broader J01–J16 benchmark, electrical analysis, firmware validation and interactive UI remain outside the delivered experiment. No architecture-level blocker was encountered. No dependencies, third-party artifacts or licenses were added. To discard the experiment locally, switch back to the verified predecessor branch and retain the task branch for review.

Owner acceptance is pending. Further milestones require a separately authorized task.

## G. Git publication

Implementation commit `36b3548855cbf90d80e8a6f2bc3e68deee27650e` was pushed with `git push -u origin codex/syn-001-candidate-generation`. A live `git ls-remote --heads origin refs/heads/codex/syn-001-candidate-generation refs/heads/main` verified the exact commit on the task branch. The local branch tracks its same-named origin branch. Remote `main` remained at `b1db3e947d04508ca22d4ba55e3172616620bad2`. The staged allowlist, whitespace and credential-pattern checks passed. The frozen task bytes matched the owner attachment locally and the staged blob matched after Git's line ending normalization. The four pre-existing untracked research files were preserved. This publication section is a report-only follow-up to the verified implementation commit.
