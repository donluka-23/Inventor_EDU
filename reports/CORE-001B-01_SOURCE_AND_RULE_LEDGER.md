# CORE-001B-01 source and rule ledger

Review: 2026-11-20 (Asia/Tbilisi). Scope: ESP32 target, documented ESP32-DevKitC V4 orderable `ESP32-DevKitC-32E` with module `ESP32-WROOM-32E`. No specific physical unit, assembly or silicon ECO was inspected.

## Exact sources and rights

`git ls-remote https://github.com/espressif/esp-idf.git 'refs/tags/v5.5.6*'` returned annotated tag object `28871d80f730e6976c9bdc9c4cbff1c916e905a9` and peeled commit `880a203ae603d08a94d06aa01e0d6761958e5e9e`. The official DevKitC guide's GitHub source resolves to `da43a78cfdd2a1122047bb5617ca79e09fd687b2`. Rendered documentation was cross-checked against the pinned source files. No v6.0.3 data was used.

| Local acceptance filename | Pinned source and locator | SHA-256 |
| --- | --- | --- |
| `soc_caps.h` | [ESP-IDF ESP32 header](https://raw.githubusercontent.com/espressif/esp-idf/880a203ae603d08a94d06aa01e0d6761958e5e9e/components/soc/esp32/include/soc/soc_caps.h), lines 182–184, `SOC_GPIO_VALID_GPIO_MASK` and `SOC_GPIO_VALID_OUTPUT_GPIO_MASK` | `adfe725856bd8e8453c867038ee03a1845d7fa4ed43acc73ffb1038e9010e713` |
| `gpio.rst` | [ESP-IDF GPIO reference source](https://raw.githubusercontent.com/espressif/esp-idf/880a203ae603d08a94d06aa01e0d6761958e5e9e/docs/en/api-reference/peripherals/gpio.rst), GPIO Summary target include and IO Configuration sections | `3c6d01f004ad68879fb8fbba513f97ca6887931ec02110e1351f998409ff9a74` |
| `esp32.inc` | [ESP32 GPIO Summary include](https://raw.githubusercontent.com/espressif/esp-idf/880a203ae603d08a94d06aa01e0d6761958e5e9e/docs/en/api-reference/peripherals/gpio/esp32.inc), GPIO34 row and GPI/SPI0/1/strapping notes (lines 165 and 197–200) | `cdacf70a69b8cb2bfe4f4abb3e9b37e9ca06509e71922e72c05982d4332fd66b` |
| `board.rst` | [Board source](https://raw.githubusercontent.com/espressif/esp-dev-kits/da43a78cfdd2a1122047bb5617ca79e09fd687b2/docs/en/esp32-devkitc/user_guide.rst), J2/J3 Header Block lines 130, 232, 236, 256, 276 and note 2 (279) | `a6e89080a3a5f9b99f33e63e7a0d9788fa858ad11cd25feffbb9e4df15229f1b` |
| `ordering.inc` | [Board ordering table](https://raw.githubusercontent.com/espressif/esp-dev-kits/da43a78cfdd2a1122047bb5617ca79e09fd687b2/docs/en/esp32-devkitc/ordering-info.inc), lines 20–21, exact orderable and module | `673ce22fc37b60afe6286a28d3bd1bb617b0fb2812609e086ba3577f72987e8b` |

The header carries an Apache-2.0 SPDX identifier and Espressif copyright notice. This pilot independently curates facts from the header and documentation. No SDK source or documentation bytes, PDFs, diagrams or libraries are distributed in this task. Documentation is linked and described in original words. No general redistribution clearance was established. [Published ESP-IDF GPIO reference](https://docs.espressif.com/projects/esp-idf/en/v5.5.6/esp32/api-reference/peripherals/gpio.html) · [Published board guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html)

## Curated facts and authority layers

| Board terminal | Board target | SDK target capability: input / output / pull-up | Module and board qualification |
| --- | --- | --- | --- |
| J2.5, IO34 | GPIO34 | true / false / false | Silicon validity and output exclusion from the two masks. Software pull-up exclusion from ESP32 GPIO Summary GPI note. Module identity from the exact orderable row. |
| J3.9, IO18 | GPIO18 | true / true / unknown | Ordinary ACTIVE digital capability from masks. Exact board availability, configured runtime state and pull-up support are outside the admitted facts. |
| J3.8, IO19 | GPIO19 | true / true / unknown | Same authority as J3.9. No Echo compatibility claim. |
| J3.19, CLK | GPIO6 | true / true / unknown | Silicon masks permit output. Board header note 2 documents flash-clock reservation on this profile, corroborated by the ESP32 SPI0/1 note. ACTIVE general-purpose use fails the separate board rule. |
| J3.14, IO0 | GPIO0 | true / true / unknown | Board table identifies this exact contact. The SDK note identifies GPIO0 as strapping. Reset level, external pull and sampling evidence remain missing. |

GPIO2, GPIO5, GPIO12 and GPIO15 also appear in the same strapping note. The bounded fixture admits a GPIO0 strap case only. No pinmux or flash release assumption is made. R2's existing board ground ties and sensor interface identities remain unchanged in meaning. The B catalog pins the board guide and adds typed J3.14 and J3.19 mappings, so its new catalog and definition pins are explicit.

## Rule traceability

All rule implementation is in `inventor_edu/gpio_verify.py`. Rules compare fixed typed values and exact identifiers. Device-specific facts reside in `data/gpio/devkitc_32e_facts.json`. The synthetic MCU-X scenario is a test assumption, not hardware evidence.

| Rule | Research basis | Required predicates and coverage | Independent positive, negative and missing oracle |
| --- | --- | --- | --- |
| PIN_MAPPING | B §2 R-B01/02, §6 B-G01 | Exact profile and pins, validated physical terminal, typed v1.1 `soc_gpio`, independently reviewed board-target agreement. `_mapping` and `verify_gpio_requirements`. | `test_pin_mapping_and_literal_canonical_report_hashes`: verified GPIO18. `test_resealed_wrong_mapping_legacy_and_missing_kind`: wrong target is ambiguous, legacy and unverified mapping unknown, malformed kind fails ingestion. |
| PHYSICAL_CAPABILITY | B §2 R-B03/04, §6 B-G02 and B-G08 | `_check`: supported requested function, ACTIVE state, approved and nonconflicting boolean for the mapped target. | `test_B01_to_B05_source_reviewed_direction_and_pullup`: GPIO18 out, GPIO19/GPIO34 in pass, GPIO34 out fails. `test_B13_conflicting_capability_claims_are_unknown` and `test_B18_B23_missing_conditions_board_and_capability_are_unknown` prove unknown behavior. |
| BOARD_AVAILABILITY | B §2 R-B05, §6 B-G03 | Scoped board fact for requested state, separate from mask. Explicit availability can pass, explicit reservation fails, missing record unknown. No source-backed ordinary availability record was admitted for this pilot. | `test_B06_board_reservation_is_separate_from_silicon`: GPIO6 silicon PASS, board FAIL. `test_B18_B23_missing_conditions_board_and_capability_are_unknown`: unrelated GPIO18 availability unknown. |
| INTERNAL_PULLUP_CAPABILITY | Task §6D, Research B §5 GPI note and §11 B05 | Explicit GPIO_IN_PULLUP request and approved ACTIVE pull-up fact. Input capability is a separate rule. | GPIO34 fails in `test_B01_to_B05_source_reviewed_direction_and_pullup`; `test_B18_B23_missing_conditions_board_and_capability_are_unknown` checks unknown and demonstrated inapplicability. No reviewed true pull-up fact is supplied. |
| BOOT_STRAP_CONTEXT | B §6 B-G06 | Known strapping definition at RESET produces a scoped unknown if required observations are missing. Explicitly sourced nonstrap would be not applicable. | `test_B07_B08_boot_and_active_require_separate_evidence`: GPIO0 missing reset prerequisites is UNKNOWN. No boot success or failure rule implemented. |
| ACTIVE_CONFIGURATION | B §2 R-B06, §6 B-G07 | `_check` preserves observation ref and declaration, neither constitutes validated telemetry. | Same test: capability passes and active state is UNKNOWN even with a declaration or an unvalidated reference. Active PASS and FAIL deferred. |
| Coverage and result replay | B §2 R-B07/08/09/10, §§7–8 | Separate coverage records for electrical/deferred and unsupported operations. Core errors and malformed ingestion propagate separately. Deterministic IDs plus fact, catalog, snapshot and ruleset pins. | `test_B16_B24_electrical_and_simulation_coverage_is_explicit`, `test_B15_B22_canonical_order_and_label_free_repetition` and pins/ingestion tests. |

## Trust and authentic-source acceptance

Catalog pin `sha256:356732040b6bd762e8c604ae63c3600df5da225cc938af6dff688b25aad4c57b`. Exact definition pin `sha256:8fadb7e6b1c95df25e43a4bd7aaeafd721fd05cc4415e715c5c1ffb60a10d2a9`. Fact-set pin `sha256:890f608028990e8f80f9ee48cd4388e58df1d160acc7edf2bf61445df8556d16`. All are test acceptance references. The profile is `TEST_ONLY_SOURCE_REVIEWED`; local ingestion cannot prove who controlled an expected pin.

Fetch the five linked artifacts to a temporary directory using the local filenames above. The required offline command is `python -B -m tests.gpio_source_acceptance <source-dir>`. It checks actual file bytes, extracts the bounded bit masks and compares their decisions, checks exact header rows and module, flash and GPI/strapping notes, and compares the candidate facts and typed catalog mappings. A missing file is BLOCKED and produces exit 1. Runtime evaluation performs no downloads.
