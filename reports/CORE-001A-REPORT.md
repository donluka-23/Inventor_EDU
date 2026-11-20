# Execution report — CORE-001A / Baseline v0.1

- Session date: 2026-11-20 (Asia/Tbilisi).
- Authorized plan: `C:/Users/Lenovo/.codex/attachments/4cb4c9df-14ea-4c9d-8bf9-29198b629d95/Pasted text.txt`, titled CORE-001A — Executable Engineering Model & Connectivity; Baseline v0.1, amendments AM-01–AM-04. No separate task revision was supplied.
- Outcome: **BLOCKED** at contract preflight. No implementation or acceptance tests executed.
- Git state: `D:/Inventor_EDU` is not recognized as a Git working tree. No commit or clean/dirty status can be reported.

## A. BOOT BRIEF / evidence of required reads

Read:

- The attached authorized plan above.
- `AGENTS.md`
- `docs/PRODUCT.md`
- `docs/DECISION_AUTHORITY.md`
- `docs/DECISIONS.md`
- `docs/STATUS.md`
- `tasks/NEXT.md`
- `docs/SESSION_PROTOCOL.md`
- `docs/research/raw/RESEARCH_A_ENGINEERING_MODEL_EXECUTION_CONTRACT.md` (including the authorized sections 2, 5–9 and 15).
- `docs/adr/ADR-0001-product-scope.md`
- `docs/adr/ADR-0002-data-model-proposed.md`
- `docs/VERIFICATION_POLICY.md`
- `docs/OSS_POLICY.md`
- `governance/OSS_REGISTER.csv`
- `reports/REPORT_TEMPLATE.md`
- `.agents/skills/evidence-gated-engineering/SKILL.md`
- `.agents/skills/oss-intake/SKILL.md`

Applicable accepted ADR: ADR-0001. ADR-0002 remains PROPOSED / HOLD; it was not promoted or used as implementation authority. The latest attached plan explicitly authorizes the selected Research A baseline and supersedes its conflicting recommendations through AM-01–AM-04. Stale task/status pointers were not treated as revoking this authorization.

Allowed writes: necessary Python package files, focused tests, minimal dependency configuration, and this report. Excluded: governance, raw research, architecture/ADR changes, status/work-log changes, unrelated tasks, UI, electrical rules, simulation and CORE-001B.

Repository inspection found a documentation starter, consistent with beginning a first implementation. CPython 3.12.8 is available. Required tests are Research A's applicable T01–T20 and P1–P10 plus the four-category generalization and AM-03 editing cases. Contract blockers below prevent committing the persistent schema/API without owner decisions.

## B. Actions executed (chronological, factual)

1. Read the attached authorization and mandatory governance files.
2. Read the relevant research contract, ADRs, report template, verification policy and OSS material.
3. Inventoried files and checked Git and Python availability.
4. Re-read bounded contract sections and searched for internal-tie, evidence, diagnostic and size-limit definitions.
5. Displayed the BOOT BRIEF before editing.
6. Created this report. No packages were installed, source artifacts imported, or implementation files created.

## C. Changed files (complete manifest)

| Path | Change | Reason |
| --- | --- | --- |
| `reports/CORE-001A-REPORT.md` | Created | Required standalone execution/blocker report |

This is the agent's write manifest, not a Git-derived diff. No pre-existing report at this path was found.

## D. Acceptance by criterion

All functional tests below are **NOT_RUN**, because implementation is blocked by B1–B2. These are not failing test results and provide no positive correctness evidence.

| Criterion | Required behavior | Result |
| --- | --- | --- |
| T01 | Three terminals share one net | NOT_RUN |
| T02 | Reordering preserves membership and canonical bytes | NOT_RUN |
| T03 | Duplicate/reversed conductors preserve membership; deleting one duplicate preserves connectivity | NOT_RUN |
| T04 | Disconnected terminals produce singleton nets | NOT_RUN |
| T05 | Edge deletion splits a net | NOT_RUN |
| T06 | Crossings without a junction do not connect | NOT_RUN |
| T07 | Multiple wires share an explicit junction | NOT_RUN |
| T08 | Unknown definition rejected | NOT_RUN |
| T09 | Ambiguous device identity rejected | NOT_RUN |
| T10 | Geometry-independent engineering output | NOT_RUN |
| T11 | Exact canonical JSON round-trip | NOT_RUN |
| T12 | Invalid terminal rejected | NOT_RUN |
| T13 | Missing instance rejected | NOT_RUN |
| T14 | Self-loop rejected | NOT_RUN |
| T15 | Duplicate IDs rejected | NOT_RUN |
| T16 | Source-qualified internal ties, within documented scope | NOT_RUN |
| T17 | Board 5V/3V3 remain separate absent ideal conductor | NOT_RUN |
| T18 | Source redistribution rights enforced | NOT_RUN; no third-party material imported |
| T19 | Extra schema fields rejected | NOT_RUN |
| T20 | Stale definition/catalog digest rejected | NOT_RUN |
| P1–P6 | Permutation, reversal, redundancy, add/delete bounds and partition properties | NOT_RUN |
| P7 | Independent NetworkX comparison | NOT_RUN |
| P8–P10 | View invariance, generated invalid-reference rejection and independent hash vectors | NOT_RUN |
| AM-01/02/04 | Board, sensor, synthetic passive and other multi-terminal category; generalized physical contacts | NOT_RUN |
| Passive isolation | Resistor terminals stay separate absent external ideal conductor | NOT_RUN |
| AM-03 | Junction-only groups are diagnostics, not physical-terminal nets; unfinished wires are not committed conductors | NOT_RUN |
| Contract readiness | Required semantics can be implemented without architecture decisions | BLOCKED: B1–B2 |

## E. Commands and actual terminal outputs

Working directory for shell commands: `D:/Inventor_EDU`.

- `Get-Content` read the paths in section A; `rg --files` inventoried the workspace. Initial default-encoding output displayed Georgian/punctuation incorrectly; subsequent relevant reads used `-Encoding UTF8`. Large combined output was truncated; bounded section reads were used for the implementation baseline.
- `rg --files -g AGENTS.md -g '*CORE*' -g '*requirements*' -g pyproject.toml` returned `AGENTS.md` before report creation. No existing CORE task/package configuration was found by that search.
- `rg -n 'SourceDocument|source_document|internal_ideal_ties|mapping_status|review_status|max bytes|limit|diagnostic' docs/research/raw/RESEARCH_A_ENGINEERING_MODEL_EXECUTION_CONTRACT.md` located the contract fields and requirements referenced in section G.
- `py -0p` failed: `The term 'py' is not recognized`. This is a missing launcher, not a missing Python runtime.
- `Get-Command python, python3, uv -ErrorAction SilentlyContinue` found `python.exe` at `C:\Users\Lenovo\anaconda3\python.exe`.
- `python --version` returned `Python 3.12.8`.
- `python -m pip show pydantic networkx hypothesis` reported Pydantic `2.13.4`, NetworkX `3.3`, and `WARNING: Package(s) not found: hypothesis`.
- A follow-up Python metadata check confirmed:

```text
3.12.8
C:\Users\Lenovo\anaconda3\python.exe
pydantic==2.13.4
networkx==3.3
hypothesis: NOT_INSTALLED
```

- Standalone `git status --short` exited 1:

```text
fatal: not a git repository (or any of the parent directories): .git
```

- `Test-Path reports/CORE-001A-REPORT.md` returned `False` before creation.
- `apply_patch` created this report. No implementation, installation, test or example command was run. Read-only compound PowerShell commands do not provide isolated exit codes for each constituent command; none are inferred here.

## F. Engineering facts, boundaries and UNKNOWN results

| Dependency | Authorized | Observed in current Python environment | Installation outcome |
| --- | --- | --- | --- |
| CPython | 3.12.x | 3.12.8 | Existing runtime; no installation |
| Pydantic | 2.14.4 | 2.13.4 | NOT_ATTEMPTED |
| NetworkX, test-only | 3.7 | 3.3 | NOT_ATTEMPTED |
| Hypothesis, test-only | 6.170.17 | Not installed | NOT_ATTEMPTED |

Availability of the exact approved packages was not checked online. Existing mismatched versions were not substituted or used to claim validation. The current environment was not modified.

Actual implemented data models/public APIs: **NONE**. Actual graph algorithm, canonical serializer and machine-readable topology output: **NONE**. Generalization results and reproducible terminal-to-net example: **NOT_RUN / unavailable**.

The approved algorithm remains full-snapshot deterministic BFS with `collections.deque`. The contract prescribes sorted canonical JSON, excluded self-digest fields, and terminal-membership-derived net IDs. These are requirements, not observed behavior.

Research A limits the board to its source-qualified ESP32-DevKitC V4/-32E profile and the sensor to Adafruit retail PID3942. Actual board assembly/silicon revision and the sensor OEM/PCB revision remain UNVERIFIED. No hardware evidence was independently upgraded, no numeric electrical facts added, and no electrical-safety or simulation claim made.

## G. Deviations, blockers and architectural decision requests

### B1 — Internal-tie serialization and admission contract is incomplete

Research A §5.1 lists `internal_ideal_ties` but does not define an element's fields or its binding to evidence. Sections 2 (I07), 6.1–6.2 and 8.3 require source-verified, scope-qualified ties and prohibit edges from incomplete evidence. They do not specify the exact machine-checkable admission predicate or how a tie references a claim identifying its precise terminal group. Generic definition-level evidence IDs alone do not specify that relationship.

Decision required: supply the serialized internal-tie record and the required claim/status/scope checks that admit it as an edge, including the behavior for incomplete or mismatched evidence. This determines persistent catalog bytes/digests and which terminals become electrically equivalent; it is not merely helper naming or internal decomposition.

### B2 — AM-03 leaves junction-only conductor output unspecified

AM-03 correctly supersedes rejection of orphan junction groups and forbids creating physical-terminal nets for them. Research A §6.2 step 6 nevertheless defines `connection_to_net` as mapping conductors to a net ID, and §5.1 has no diagnostic output structure. A valid conductor between two orphan junctions has no physical-terminal net ID.

Decision required: define the serialized result for this conductor (including whether its mapping is absent or explicitly has no net) and the diagnostic representation/ordering. This is externally visible API/serialization behavior. No option was selected by Codex.

### Additional details to freeze with the same contract clarification

- §5.1 `EvidenceClaim` and §8.3 fact-register fields differ; specify their relationship and the canonical `value` type, so strict restoration and evidence validation have one schema.
- §7.1 requires catalog/snapshot byte limits but provides no numerical bounds or limit-exceeded error contract.
- The OSS register has no entries for the newly authorized packages. The attached plan is explicit dependency authorization; the stale register alone was not treated as canceling it. Transitive versions, integrity hashes and distribution notices remain unverified; no registry edit was authorized or made.

No replacement architecture was adopted. Package implementation and tests were stopped rather than embedding guessed persistent semantics. The missing Git repository is an observation, not an engineering blocker; Git initialization was not performed.

## H. OSS/license changes

**NONE.** No installation, dependency import into project code, vendor document copying, artwork, models or dataset intake occurred. Research A reports MIT for Pydantic, BSD-3-Clause for NetworkX and MPL-2.0 for Hypothesis; these are supplied research statements, not an artifact/license audit completed during this session. No release license or OSS decision was changed.

## I. Rollback/reproducibility and residual risks

Only this report was created. No runtime or engineering state requires rollback. Repeat the read-only environment checks to reproduce the environment observations. Tests and an example cannot be reproduced because no implementation was produced. Resolving the contract details remains necessary before claiming canonical compatibility or evidence-qualified connectivity.

## J. Owner review request

This blocked execution report is ready for architecture-owner review; the requested implementation is not delivered. Please attach or paste this complete report in the architecture conversation and resolve B1–B2 and the associated schema details in a clarified CORE-001A contract. This report neither accepts an ADR nor authorizes another task. CORE-001B was not started.

---

# Resumed execution — CORE-001A revised contract, baseline v0.1

**Final status: PASS within the revised CORE-001A acceptance scope.** All 11 tests passed under the authorized interpreter and exact dependency versions. The earlier BLOCKED section records the prior session. The revised contract resolved its implementation blockers.

## A. Authority and scope

- Session date: 2026-11-20 (Asia/Tbilisi).
- Revised plan: `C:/Users/Lenovo/.codex/attachments/3f7ec696-9028-40a8-8477-8253b9adc9d4/Pasted text.txt`.
- Reviewed the original authorization, Research A, the previous execution report and the governance files listed in the historical preflight. Also reviewed `docs/REFERENCE_ARCHITECTURE.md` for the separation between view and engineering state.
- ADR-0001 applies. The revised owner authorization supplied the implementation contract. ADR-0002 remains PROPOSED / HOLD.
- Scope covered the Python connectivity package, test fixtures, executable demonstration, two dependency files and this report. GPIO capability checks, electronic calculations, visual editing, simulation and follow-up tasks were outside the authorized scope.

## B. Actions and file manifest

Checked package metadata, created an isolated CPython environment under the temporary directory, resolved the exact package wheels, checked their licenses, and installed with wheel hashes enforced. Checked primary documentation for fixture provenance, implemented the package and fixtures, ran the test suite and demonstration, and appended this report.

| Path | Change | Purpose |
| --- | --- | --- |
| `inventor_edu/__init__.py` | Created | Public models and functions |
| `inventor_edu/models.py` | Created | Strict immutable records and structured domain errors |
| `inventor_edu/core.py` | Created | Catalog admission, snapshot binding, canonical JSON and deterministic BFS |
| `tests/__init__.py` | Created | Standard-library test discovery and executable fixture module |
| `tests/core001a_fixtures.py` | Created | Four component profiles and executable terminal-to-net demonstration |
| `tests/test_core001a.py` | Created | Deterministic tests and bounded NetworkX/Hypothesis comparison |
| `requirements-core001a.txt` | Created | Hash-pinned Windows x64 runtime dependency set |
| `requirements-core001a-test.txt` | Created | Hash-pinned test dependencies layered over the runtime set |
| `reports/CORE-001A-REPORT.md` | Appended | Preserve the prior audit and record resumed results |

Git verification returned exit code 1 with `fatal: not a git repository (or any of the parent directories): .git`. The table records the execution write manifest.

## C. Implementation and serialization

- `load_catalog(payload, expected_sha256=...)` admits an immutable catalog with strict schema, unique IDs, normalized definitions and evidence, verified definition/catalog digests and an optional external catalog pin. `resolve_terminal(catalog, snapshot, ref)` returns the physical contact, any declared mapping with its status, and relevant claim IDs.
- `create_snapshot` and `restore_snapshot` validate catalog and per-instance definition pins, required endpoints, unique IDs and the v1 resource limits. `EngineeringModelError` carries a code, path and relevant context IDs. The limits are 4 MiB of JSON, 128 instances, 8192 instantiated terminals, 16384 conductors and 8192 junctions.
- `compute_nets` reconstructs a graph using disjoint `T:<instance>/<terminal>` and `J:<junction>` keys. Explicit wires and admitted ties create undirected edges. Each multi-terminal internal tie uses a star with one edge per non-root member. Sorted traversal with `collections.deque` yields physical-terminal partitions. Duplicate wires share adjacency and keep separate connection IDs. BFS traversal is linear in graph size before ordering.
- `InternalIdealTie` references a claim for the complete terminal set, which must contain at least two distinct exposed contacts. Claim identity, definition, scope, terminal membership, approval and source qualification are checked. Manufacturer ties require a manufacturer claim, its source document and locator, and a publisher matching the definition's verified manufacturer. A synthetic tie requires separately labeled synthetic data and a synthetic claim. Missing, unapproved, disputed or mismatched ties raise `INVALID_IDEAL_TIE` for a well-formed tie declaration. A payload that fails structural validation can be rejected before tie admission.
- Junction-only components emit `JUNCTION_ONLY_GROUP` diagnostics with sorted junction and conductor IDs, ordered by their junction IDs. Their conductors map to JSON `null`. A component with one physical terminal contributes a singleton net and an isolated-terminal entry even if it contains attached junctions.
- `serialize_snapshot` and `serialize_topology` emit compact UTF-8 JSON with sorted keys and normalized identity arrays. Endpoint pairs are sorted by vertex key. The profile rejects floating-point inputs, duplicate JSON keys, unsupported versions and geometry fields. Digests use canonical SHA-256 with self-digest fields absent from their own preimages. A net ID hashes the domain prefix `INVENTOR-EDU-NET-V1`, one LF, and the LF-joined sorted physical-terminal keys, without a trailing LF. The topology serializer converts immutable mapping tuples to JSON objects.
- These persistence bytes implement INVENTOR v1 as authorized. No KiCad or LibrePCB interchange adapter is provided. The runtime validates consistency of the supplied evidence and approvals. Catalog digests detect substitution relative to a trusted pin and do not authenticate who supplied or approved a claim.

## D. Reuse-versus-Custom Decision Register

| Requirement | Reuse or minimal custom selection | Rationale, maintenance and interoperability |
| --- | --- | --- |
| Physical contacts, logical targets and device identity | Reused LibrePCB's documented distinction as a convention. Typed `DeviceIdentity`, `DeviceDefinition`, `TerminalDefinition` and `SignalMapping` bind the project's evidence and contact IDs. | Preserves contact and function identity without a schematic or footprint library parser. No LibrePCB code or data incorporated. No file compatibility is claimed. [LibrePCB component documentation](https://librepcb.org/docs/quickstart/create-library-elements/component/) |
| Explicit junctions, stable instances and independent conductor records | Reused KiCad's explicit-junction convention. `ComponentInstance`, `TerminalRef`, `JunctionRef`, `Junction` and `Conductor` encode the approved, geometry-free snapshot semantics. | Keeps duplicate conductor IDs and junction-only editing state. Avoids EDA application integration, net-label inference and vendor format parsing. [KiCad wire junction documentation](https://docs.kicad.org/9.0/en/eeschema/eeschema.html#wire-junctions) |
| Evidence and tie admission | Small `SourceDocument`, `EvidenceClaim` and `InternalIdealTie` records, plus `ResolvedTerminal` for contact lookup. | A literal text or terminal-set value suffices for this task. Unknown values can be null. Rights and source locations stay traceable without a generic evidence framework or vendor asset redistribution. |
| Validation and canonical persistence | Reused Pydantic `BaseModel`, `ConfigDict`, `Field`, `StringConstraints`, `model_validate`, `model_validate_json`, `model_dump`, `model_copy` and its JSON Schema generation. Reused stdlib JSON and SHA-256. Added the `CatalogSnapshot` and `CircuitSnapshot` envelopes and cross-record validation. | Pydantic owns typed validation, while application code enforces identity and evidence references. No general JSON/schema engine required. The duplicate-key check uses the stdlib JSON parser hook. Pydantic is MIT. [Pydantic configuration](https://pydantic.dev/docs/validation/latest/api/pydantic/config/) |
| Electrical nets, editing diagnostics and independent oracle | Reused the established BFS algorithm and stdlib `deque`. `Net`, `TopologyResult` and `EditingDiagnostic` expose the required machine-readable output. Reused NetworkX `Graph` and `connected_components` in tests, with Hypothesis strategies and standard-library `unittest`. | No production graph-library dependency or custom graph framework. NetworkX and Hypothesis stay in the test environment. |

## E. Fixture evidence and coverage

- The ESP32 fixture covers eight selected header contacts. Espressif's V4 guide identifies the `ESP32-DevKitC-32E` orderable variant and `ESP32-WROOM-32E` module. The J2/J3 tables identify the fixture's contacts and their primary mappings, including `J3.9 → GPIO18`. [Espressif V4 guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html)
- The board ground tie uses Research A S18–S19. The revised run rechecked the header table and retrieved the original schematic. The schematic's text and connector layout were inspected in memory using the already installed local PDF reader. The guide and Research A's visual schematic review supply the exact J2.14/J3.1/J3.7 group. The schematic provides connector ground and separate `EXT_5V`/`VDD33` references. No live firing or measurement of hardware took place. [Espressif V4 reference schematic, sheet 1](https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_sch.pdf)
- The sensor evidence comes from Adafruit's PID3942 retail listing and its HC-SR04 pinout. The four exposed contacts in the fixture are Vcc, Trig, Echo and Gnd. Adafruit is recorded as the retailer. The sensor OEM, PCB revision, lot equivalence and applicable electrical limits remain unverified. [Adafruit PID3942](https://www.adafruit.com/product/3942) · [Adafruit pinout](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/pinouts)
- Physical PCB, assembly and silicon revisions of any particular ESP32 unit remain unverified. The board fixture is a documented subset. The two synthetic profiles are an opaque passive with two leads and an opaque integrated-circuit fixture with three pads. Both use explicit test-data markers. Neither has an implicit tie.
- The implementation supplies topology only. No voltage, current, GPIO compatibility, firmware behavior, electrical safety or physical validation result follows from these tests.

## F. Acceptance and actual test results

| Test or criterion | Observation | Result |
| --- | --- | --- |
| `test_three_terminals_junction_and_reordering` | Three terminals joined through junctions, one singleton, equal bytes and topology on reversed/reordered inputs | PASS |
| `test_deletion_duplicate_and_hash_vector` | Parallel wire preserves membership, deletion splits, independent net checksum matches | PASS |
| `test_crossings_and_geometry_independence` | Crossing and noncrossing view data give two unchanged engineering partitions | PASS |
| `test_junction_only_and_singleton_with_stub` | Orphan groups emit diagnostics and a null wire association. Stub keeps its singleton net. | PASS |
| `test_reference_profiles_and_generalization` | Scoped ground ties stay within each board instance. Sensor ground, distinct rails and passive leads stay separate. Passive lead and synthetic IC pad join through an explicit wire. | PASS |
| `test_evidence_admission` | Valid source tie and separately marked synthetic tie work. Missing, mismatched, unapproved, incorrectly sourced and disputed claims reject. | PASS |
| `test_invalid_endpoints_ids_and_identity` | Missing instance/contact/junction, self-loops, duplicate IDs and ambiguous/generic profiles reject | PASS |
| `test_canonical_round_trip_and_digest_mismatches` | Exact canonical round-trip, normalized catalog order and stale/tampered digest rejection | PASS |
| `test_literal_canonical_snapshot_vector` | Snapshot bytes match a literal, independently specified expected vector | PASS |
| `test_strict_schema_and_resource_limits` | Extra fields, unknown version, duplicate JSON keys, floats, uncommitted wire and each of five resource limits reject | PASS |
| `test_networkx_oracle_permutation_partition_and_single_edge_deletion` | Fixed seed 1001, up to 80 generated examples, six vertices and up to 15 input edges. NetworkX independently supplies the full and post-deletion partitions. Also checks ordering invariance and rejects generated bad references. | PASS |
| T18 redistribution behavior | Export or redistribution of manufacturer documents is outside this core. Fixture stores factual records and source links. | NOT_RUN |
| Executable demonstration | Nine nets printed, including the three board ground contacts and the explicit board-to-sensor net | PASS |

## G. Commands and observed outputs

Ran from `D:/Inventor_EDU` on CPython 3.12.8, Windows x64. The isolated interpreter was at `%TEMP%/InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe`. Use a fresh venv or point `$exe` to the existing one:

```powershell
$coreEnv = Join-Path $env:TEMP ('InventorEDU-CORE-001A-' + [guid]::NewGuid().ToString('N'))
python -m venv $coreEnv
$exe = Join-Path $coreEnv 'Scripts/python.exe'
& $exe -m pip --isolated install --index-url https://pypi.org/simple --only-binary=:all: --require-hashes -r requirements-core001a-test.txt
& $exe -m pip check
& $exe -B -m unittest discover -v
& $exe -B -m tests.core001a_fixtures
```

The dry run used the same PyPI index with `--dry-run --only-binary=:all: --report` and the three authorized direct pins. PyPI's versioned JSON metadata supplied SPDX identifiers or license names. The final installation exited 0 and printed:

```text
Successfully installed annotated-types-0.8.0 hypothesis-6.170.17 networkx-3.7 pydantic-2.14.4 pydantic-core-2.50.5 sortedcontainers-2.4.0 typing-extensions-4.16.0 typing-inspection-0.4.5
No broken requirements found.
```

The final discovery run and demonstration exited 0. All individual cases in section F printed `ok`. Relevant observed output:

```text
Ran 11 tests in 0.735s

OK
net:sha256:9f9e42e9ec60938f3c315593521e49b1dbd47e23960d97a7302dfb21ce800ef6 T:board/J2.14, T:board/J3.1, T:board/J3.7
net:sha256:2c9d5e8a7f486a3114cc6737d1363c90147ef602c0490e70f96822919212ee31 T:board/J3.9, T:sensor/Trig
```

An independent Python SHA-256 calculation over the literal net preimage produced `c226830ef614b43a85d20b6eae3117e59ee5ddb472638cc6f9e59d413e015735`, which is pinned in the deletion test.

## H. Dependency, licenses and operational requirements

| Use | Exact installed artifact | License from upstream |
| --- | --- | --- |
| Runtime validation | [pydantic 2.14.4](https://pypi.org/project/pydantic/2.14.4/) | MIT |
| Required runtime transitive | [pydantic-core 2.50.5](https://pypi.org/project/pydantic-core/2.50.5/) | MIT |
| Required runtime transitive | [annotated-types 0.8.0](https://pypi.org/project/annotated-types/0.8.0/) | MIT |
| Required runtime transitive | [typing-extensions 4.16.0](https://pypi.org/project/typing-extensions/4.16.0/) | PSF-2.0 |
| Required runtime transitive | [typing-inspection 0.4.5](https://pypi.org/project/typing-inspection/0.4.5/) | MIT |
| Test oracle | [networkx 3.7](https://pypi.org/project/networkx/3.7/) | BSD-3-Clause |
| Property tests | [hypothesis 6.170.17](https://pypi.org/project/hypothesis/6.170.17/) | MPL-2.0 |
| Required test transitive | [sortedcontainers 2.4.0](https://pypi.org/project/sortedcontainers/2.4.0/) | Apache-2.0 |

The eight installed code artifacts have license files in their wheel metadata directories. These licenses permit commercial use subject to their terms. Distribution needs the applicable copyright/license notices, including BSD non-endorsement and Apache notices where applicable. MPL obligations apply to distribution of covered files. CPython is the existing PSF-licensed runtime. The venv's bundled pip was 24.3.1 and served as an installer only. The Windows x64 binary wheels were used for the approved Pydantic core and Hypothesis dependencies. Hashes in the requirement files identify the exact verified wheels. There are no paid services or credentials in the implementation.

The revised plan explicitly approved the direct versions and bounded local use. The existing OSS register has no entries for these packages. Owner reconciliation is pending under the repository's governance process, which this task did not authorize editing. No vendor PDF or application/library source is bundled. The schematic was fetched for inspection. This execution records local dependency intake, not a release audit or approval of distribution packaging.

## I. Limitations and rollback

The Windows x64 CPython 3.12 wheel lock was exercised on 3.12.8. Other wheel platforms and Python patch versions were not exercised. The bounded random tests use small graphs and supplement the fixture tests. Performance at production scale was not benchmarked. Canonical catalog digest authoring for the demonstration lives in the fixture module, while catalog validation is a public runtime API. The reference fixtures are for this task's engineering scope, not a full hardware catalog.

Reverting the resumed execution consists of removing the eight created files listed in section B and restoring the report to the historical section above. The isolated environment is outside the workspace. The global Anaconda install was not modified.

## J. Architecture-owner review

The revised CORE-001A package, observed tests and executable demonstration are ready for owner review. Attach or paste this full Markdown file in the architecture conversation for adjudication. The report records execution within CORE-001A.
