# Execution report — CORE-001B-01 rev 1

- Session date: 2026-11-20, Asia/Tbilisi.
- Authorized task: [tasks/CORE-001B-01.md](../tasks/CORE-001B-01.md), owner-supplied frozen revision 1.
- **Outcome: PASS** for the bounded source-reviewed, test-only acceptance contract. Recommended owner disposition: accept the tested capability behavior for this scope, subject to independent pin review and deployment authorization.
- Repository: `D:/Inventor_EDU`, origin `https://github.com/donluka-23/Inventor_EDU.git`. Clean initial working tree on DATA-001. Fetched/live DATA-001 predecessor `360a0fc18c450e9f9d0c11172b51db0ecc5fa554`. Task branch `codex/core-001b-01-gpio-capability`.

## A. BOOT BRIEF and authority

Reviewed AGENTS, product, decision authority and index, status, session/verification/OSS policies, task pointer and work log, ADR-0001, the engineering skill, Research 01–03 and A/B/C/E, the A implementation, independent audit, R1/R2 reports and DATA-001 report/ledger. Research B §§2–8 and 11 drive the bounded verification traceability. Existing A runtime, R2 typed mappings, public APIs and test fixtures were inspected. ADR-0001 applies and ADR-0002 remains proposed. No changes to the A graph, model definitions, persistence contracts, previous tests, importer, policy or raw research were authorized.

## B–C. Actions and changed files

After fetching and inspecting local and remote state, created the task branch directly from DATA-001. Resolved the ESP-IDF tag to the exact approved commit. Resolved the DevKitC guide into immutable source with its associated ordering table. Retrieved only five source files into a temporary cache, checked their bytes and curated the small fact and test catalog fixtures. Implemented the typed finite checks, external pin boundary and explicit source acceptance entry point. Tested with both authentic caches present and reconciled project tracking.

| Path | Change |
| --- | --- |
| `tasks/CORE-001B-01.md` | Exact owner handoff preserved |
| `inventor_edu/gpio_facts.py` | Immutable typed fact records, source/canonical validation and digest binding |
| `inventor_edu/gpio_verify.py` | Fixed finite GPIO semantics and deterministic report/coverage serialization |
| `inventor_edu/__init__.py` | Exported public fact loader, verifier, serializer and result/request types |
| `data/gpio/devkitc_32e_catalog.json` | Test-only catalog derived from R2, with a pinned board source and independently sourced J3.19 and J3.14 typed mappings |
| `data/gpio/devkitc_32e_facts.json` | Separately pinned source-reviewed facts |
| `tests/test_gpio_capability.py` | Fixed oracles, synthetic MCU, trust/invalid cases, replay and golden hashes |
| `tests/gpio_source_acceptance.py` | Explicit authentic-source admission, nonzero on missing input |
| `docs/STATUS.md`, `tasks/NEXT.md`, `tasks/WORK_LOG.md` | Verified status and review queue updated |
| `reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md` | Source pins and per-rule evidence, revisions and test traceability |
| `reports/CORE-001B-01-REPORT.md` | This execution report |

No new dependencies or licensed bytes were added. No OSS register edit was needed for fact-only linking and an unchanged dependency set.

## D. B01–B24 disposition

| Case | Expected and verified result | Acceptance |
| --- | --- | --- |
| B01 | GPIO34 output false → `FAIL / OUTPUT_NOT_CAPABLE` | PASS |
| B02 | GPIO18 ordinary output true → capability `PASS / CAPABILITY_CONFIRMED` | PASS |
| B03 | GPIO19 input true → capability `PASS / CAPABILITY_CONFIRMED` | PASS |
| B04 | GPIO34 input true → capability `PASS / CAPABILITY_CONFIRMED` | PASS |
| B05 | GPIO34 software pull-up false → `FAIL / PULLUP_NOT_CAPABLE` | PASS |
| B06 | J3.19/GPIO6 silicon output PASS and separate board `FAIL / RESERVED_RESOURCE` | PASS |
| B07 | Optional mapped GPIO0 case implemented. Without reset level, external pull or timing, `UNKNOWN / BOOT_STRAP_CONDITIONS_UNKNOWN`. | PASS for missing-evidence classification |
| B08 | GPIO18 output capability PASS with separate `UNKNOWN / ACTIVE_CONFIG_UNKNOWN`, including an unvalidated observation reference | PASS |
| B09 | Observed mismatch needs trusted real firmware observation and timing | NOT_RUN |
| B10 | Exclusive output ownership needs a sourced ownership contract | NOT_RUN |
| B11 | PWM plus input sharing needs validated dual-use peripheral/mode facts | NOT_RUN |
| B12 | Other definition or mismatched module/orderable does not inherit the profile | PASS |
| B13 | Opposing resealed same-scope output claims → `UNKNOWN / EVIDENCE_CONFLICT` | PASS |
| B14 | Unknown physical contact → CORE-001A `UNKNOWN_TERMINAL` ingestion error | PASS |
| B15 | Permuted requests/fact records yield identical canonical bytes. View-only localization cannot enter the interface. Persisted user-label changes preserve semantic decisions/anchors but change the A snapshot hash and finding IDs. | PASS within existing A hash semantics |
| B16 | GPIO19 works as input capability only. Electrical coverage `NOT_EVALUATED / ELECTRICAL_CHECK_DELEGATED`. | PASS |
| B17 | UART/ownership needs pinmux and resource contracts | NOT_RUN |
| B18 | Optional ACTIVE/SLEEP contrast checked. ACTIVE capability passes and SLEEP gives `UNKNOWN`, based on absence of SLEEP scope. No sleep operation was verified. | PASS for missing-evidence classification |
| B19 | Same evaluator on a fictitious MCU-X gives P0 output PASS and P1 output FAIL | PASS |
| B20 | I2C/mode and open-drain rule need separately approved facts and rule | NOT_RUN |
| B21 | Dynamic serial/GPIO contention and ownership changes need timed state facts | NOT_RUN |
| B22 | 100 repeated evaluations with reversed requirements and fact/source rows yield byte-identical reports | PASS |
| B23 | Missing applicable capability stays `UNKNOWN / CAPABILITY_UNKNOWN` | PASS |
| B24 | Unsupported analog-noise request yields `NOT_EVALUATED / OUT_OF_SCOPE` | PASS |

All mandatory negative controls ran. Wrong orderable or module has no matching scope. A wrong supplied catalog or fact-set pin fails typed ingestion. Old pins reject a resealed source-edition change. Missing trusted catalog/factset pins or an unreviewed set produce scoped UNKNOWN. A well-formed fact set cannot claim a different catalog. Legacy and unverified mappings stay unknown. Dropped typed kind is a CORE-001A ingestion error. Missing board-resource facts stay unknown. Two instances with the same display label keep distinct physical references and nets. Unknown state cannot establish active capability. Malformed fact data and missing source references fail separately as typed ingestion errors.

## E. Actual commands and results

Git: `git fetch origin`, `git branch -avv`, `git ls-remote --heads origin`, `git status --porcelain`, and `git switch -c codex/core-001b-01-gpio-capability origin/codex/data-001-component-source-pilot --no-track`.

SDK tag query: `git ls-remote https://github.com/espressif/esp-idf.git 'refs/tags/v5.5.6*'`. The peeled SHA was `880a203ae603d08a94d06aa01e0d6761958e5e9e`. Board artifacts use `da43a78cfdd2a1122047bb5617ca79e09fd687b2`. `Invoke-WebRequest -UseBasicParsing <pinned-URL> -OutFile <temporary-file>` and `Get-FileHash` retrieved and checked the five files listed in the [source and rule ledger](CORE-001B-01_SOURCE_AND_RULE_LEDGER.md). The authoritative GPIO reference and board guide were also reviewed in rendered form.

```powershell
$exe = Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$src = Join-Path $env:TEMP 'InventorEDU-CORE-001B-01-sources'
$env:INVENTOR_EDU_DATA001_SOURCE_DIR = Join-Path $env:TEMP 'InventorEDU-DATA-001-dc037a238eb5efcc034dd9d62e5775d5c21e90e4'
$env:HYPOTHESIS_STORAGE_DIRECTORY = Join-Path $env:TEMP 'inventor-edu-b01-hypothesis'
& $exe --version
& $exe -m pip check
& $exe -B -m tests.gpio_source_acceptance $src
& $exe -B -m tests.gpio_source_acceptance (Join-Path $src 'absent')
& $exe -B -m unittest discover -v
```

CPython 3.12.8, existing hash-pinned environment, Pydantic 2.14.4, NetworkX 3.7 and Hypothesis 6.170.17. `pip check`: `No broken requirements found.` The existing DATA-001 cache contained the nine pinned artifacts and its authentic-source tests actually ran. The explicit GPIO acceptance exited 0 and printed `PASS: five authentic artifacts matched pins; masks, pull-up, header, flash, strap and -32E scope checked`. The missing-source control printed `BLOCKED: GPIO source admission: [Errno 2] No such file or directory` and exited 1. The authentic-source command is separate from regular discovery and never treats missing files as passing acceptance.

Discovery exited 0. **44 passed, 0 failed, 0 skipped**: 29 preceding CORE-001A/R1/R2/DATA-001 methods and 15 GPIO methods. Offline unit tests used pinned factual fixtures. The authentic-source check above verified the independent source bytes and fact content.

```text
test_B01_to_B05_source_reviewed_direction_and_pullup (tests.test_gpio_capability.GpioAcceptanceTests.test_B01_to_B05_source_reviewed_direction_and_pullup) ... ok
test_B06_board_reservation_is_separate_from_silicon (tests.test_gpio_capability.GpioAcceptanceTests.test_B06_board_reservation_is_separate_from_silicon) ... ok
test_B07_B08_boot_and_active_require_separate_evidence (tests.test_gpio_capability.GpioAcceptanceTests.test_B07_B08_boot_and_active_require_separate_evidence) ... ok
test_B12_wrong_device_and_module_and_board_variant_never_inherit_scope (tests.test_gpio_capability.GpioAcceptanceTests.test_B12_wrong_device_and_module_and_board_variant_never_inherit_scope) ... ok
test_B13_conflicting_capability_claims_are_unknown (tests.test_gpio_capability.GpioAcceptanceTests.test_B13_conflicting_capability_claims_are_unknown) ... ok
test_B14_bad_physical_contact_propagates_core_error (tests.test_gpio_capability.GpioAcceptanceTests.test_B14_bad_physical_contact_propagates_core_error) ... ok
test_B15_B22_canonical_order_and_label_free_repetition (tests.test_gpio_capability.GpioAcceptanceTests.test_B15_B22_canonical_order_and_label_free_repetition) ... ok
test_B16_B24_electrical_and_simulation_coverage_is_explicit (tests.test_gpio_capability.GpioAcceptanceTests.test_B16_B24_electrical_and_simulation_coverage_is_explicit) ... ok
test_B18_B23_missing_conditions_board_and_capability_are_unknown (tests.test_gpio_capability.GpioAcceptanceTests.test_B18_B23_missing_conditions_board_and_capability_are_unknown) ... ok
test_B19_synthetic_mcu_facts_use_same_evaluator (tests.test_gpio_capability.GpioAcceptanceTests.test_B19_synthetic_mcu_facts_use_same_evaluator) ... ok
test_malformed_factsets_and_required_source_references_are_ingestion_errors (tests.test_gpio_capability.GpioAcceptanceTests.test_malformed_factsets_and_required_source_references_are_ingestion_errors) ... ok
test_pin_mapping_and_literal_canonical_report_hashes (tests.test_gpio_capability.GpioAcceptanceTests.test_pin_mapping_and_literal_canonical_report_hashes) ... ok
test_resealed_wrong_mapping_legacy_and_missing_kind (tests.test_gpio_capability.GpioAcceptanceTests.test_resealed_wrong_mapping_legacy_and_missing_kind) ... ok
test_same_display_label_preserves_instance_and_net_identity (tests.test_gpio_capability.GpioAcceptanceTests.test_same_display_label_preserves_instance_and_net_identity) ... ok
test_untrusted_missing_pins_and_wrong_pins (tests.test_gpio_capability.GpioAcceptanceTests.test_untrusted_missing_pins_and_wrong_pins) ... ok
Ran 44 tests in 1.613s
OK
```

## F. Rule semantics, API and deterministic evidence

`verify_gpio_requirements(catalog, snapshot, fact_set, requests, trusted_catalog_sha256, trusted_factset_sha256)` returns a typed `GpioVerificationReport`. `load_gpio_factset` loads strict JSON and enforces source references and canonical identity. `compute_nets` validates the actual A snapshot and provides the snapshot hash and physical net anchors. `resolve_terminal` supplies the validated contact and typed mapping. The tests construct using `create_snapshot`, round-trip through `restore_snapshot` and load actual canonical catalogs using `load_catalog`. No A graph or persistence reimplementation is present.

Narrow supported functions are `GPIO_IN`, `GPIO_OUT` and `GPIO_IN_PULLUP`. The six direct checks use fixed membership and Boolean comparisons, with no ESP32 or GPIO-number branches. Explicitly requested internal pull-up is independent of input direction. Board availability uses a scoped reservation fact. Missing nonreservation proof stays UNKNOWN. Active config and boot timing are evaluated only as evidence bounds. See the ledger's Research B requirement-to-code matrix and exact authoritative fact values. GPIO matrix routing, ownership, buses, analog behavior, electrical compatibility and live runtime configuration remain out of scope.

Repository engineering statuses remain `PASS/FAIL/UNKNOWN/NOT_APPLICABLE`. B's applicable `INDETERMINATE` maps to evaluated `UNKNOWN`. Unsupported/future checks map to separate `NOT_EVALUATED` coverage records with no invented engineering status. `NOT_APPLICABLE` means a supported rule demonstrably does not apply, such as the pull-up check when pull-up is not requested. Severity is separate. Malformed input, invalid A links, wrong supplied pins and invalid snapshots raise typed errors instead of engineering findings.

Fact-set preimage: compact sorted UTF-8 JSON, exclude the root digest and sort source/fact tables, source IDs and prerequisite arrays. Finding IDs hash canonical result content plus the finding schema version, excluding the ID itself. The report sorts each result partition by requirement, rule, terminal and reason. No user-display labels are used for device identity or rule decisions. A persisted label changes the A snapshot hash by existing contract. Exact identity anchors and semantics remain stable.

- Catalog: `sha256:356732040b6bd762e8c604ae63c3600df5da225cc938af6dff688b25aad4c57b`.
- Board definition: `sha256:8fadb7e6b1c95df25e43a4bd7aaeafd721fd05cc4415e715c5c1ffb60a10d2a9`.
- Fact set: `sha256:890f608028990e8f80f9ee48cd4388e58df1d160acc7edf2bf61445df8556d16`.
- Golden GPIO18 physical-output vector: A snapshot hash `ed5f9ed4f834f2c8549f346fc470eec2e415435b95b50b28665ae45be1017eec`; finding SHA-256 `71549f4eb0d8d875789b55f91565661df24f85e68981e4b816d66e65789141f6`; report byte SHA-256 `f2c8d9434c54886427ec3fe8f142828f0d49b74e1984807557a9a980cdb16430`. These were independently calculated from literal expected result fields and Python stdlib JSON/SHA-256, using the existing A snapshot bytes and documented net preimage.

## G–I. Acceptance boundaries and rollback

| Dimension | Result and limit |
| --- | --- |
| ALGORITHM_CORRECTNESS | PASS for tested deterministic finite rules and negative controls. No device-name checks in evaluator. |
| SOURCE_FACT_VERIFICATION | PASS for location- and revision-pinned documented facts and explicit authentic acceptance, not a physical-unit check. |
| CATALOG_TRUST | Test pins verified. Production trust NOT ESTABLISHED. A checksum cannot prove the provenance of the caller's expected pins. |
| REGRESSION_COMPATIBILITY | PASS, 29 unchanged predecessor methods including authentic DATA-001. |
| FUNCTIONAL_SCOPE_COVERAGE | PASS for authorized bounded checks. Full B01–B24 suite not claimed. |
| PHYSICAL_HARDWARE_VALIDATION | NOT_RUN. No board, reset telemetry or live pin inspected. |
| DISTRIBUTION_RIGHTS | Link and independently curated facts only. SDK header's metadata is Apache-2.0. No external artifact packaged and redistribution of manufacturer materials not approved. |

Keep independently reviewed expected catalog and factset pins, explicit producer/scope approval and hardware revision controls before deployment. A supplied test fact-set pin does not promote the fixture into a production-approved catalog. Real board fit, electrical limits and active firmware remain outside these results. Reproduction steps and per-fact licensing are in the ledger. Rollback is the untouched DATA-001 predecessor or a new owner-authorized revert. No unrelated history was merged, and no CORE-001C work was begun.

## J. Owner review

Review the bounded algorithm and source facts with the ledger, then independently authorize trusted deployment pins and applicability limits if needed. Keep firmware observation, GPIO electrical checks and any new board or SDK version behind separate task authority.

## Verified publication

The reviewed implementation was committed as `96d6f4838b5cd2dc044f6b6db764be280a6863a5` (`feat(core-001b-01): verify source-backed GPIO capability`). The staged scope matched the thirteen authorized paths. Whitespace checks passed for new work, and the exact handoff bytes were preserved. Credential-pattern and binary-artifact checks returned no findings.

`git push -u origin codex/core-001b-01-gpio-capability` exited 0 and set upstream tracking. `git ls-remote --heads origin refs/heads/codex/core-001b-01-gpio-capability` then returned `96d6f4838b5cd2dc044f6b6db764be280a6863a5` for the exact branch. This report records the already-observed publication in a follow-up commit. The task remains separate from `main`.

**Final result: PASS in the authorized test scope.**
