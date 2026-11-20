# CAP-001 GPIO terminal discovery contract

Call `inventor_edu.capability_discovery.discover_gpio_terminals(query, catalog, board, fact_set, *, trusted_catalog_sha256, trusted_factset_sha256)`. This read-only test adapter handles `GPIO_IN` and `GPIO_OUT` at `ACTIVE` on one exact board instance. `CapabilityQuery` version 1.0 records the query and originating requirement IDs, the board instance and definition IDs and definition digest, function, operating state, catalog and fact-set digests, and evidence scope.

The adapter builds a canonical board-only snapshot using CORE-001A. It walks the catalog's physical terminals in terminal ID order. Typed GPIO and unknown mappings, exact-scope GPIO fact entries, and contacts with an input, output, or I/O role and no mapping declaration enter evaluation. Explicit alternate mapping kinds without a GPIO fact entry stay outside this domain. A missing declaration with an I/O role is a provisional contact that still requires verified mapping evidence. Display labels have no effect on membership.

CORE-001B checks `PIN_MAPPING`, `PHYSICAL_CAPABILITY`, `BOARD_AVAILABILITY`, `ACTIVE_CONFIGURATION`, and `ELECTRICAL_COMPATIBILITY` in one batch. The originating requirement stays in the query and the verifier batch keys rows by physical terminal ID. Wrong external pins raise verifier errors. Missing pins or unreviewed facts leave findings unresolved. The resolved catalog mapping is exposed alongside the actual B checks and requires a supported, trusted B result to confer qualification.

Each frozen candidate exposes its `TerminalRef`, resolved mapping, raw findings, separate coverage, evidence claim IDs, and limitation reason codes. A reported FAIL yields `KNOWN_UNSUITABLE`. Positive mapping and physical capability with no known FAIL yield `FUNCTION_CONFIRMED_FOR_STATED_CHECK`. Other candidates are `UNRESOLVED_EVIDENCE`. Direction qualification can coexist with unknown board availability and active configuration. Electrical compatibility remains unevaluated.

The report's `terminal_domain` exposes every investigated contact in order, including unsuitable and unresolved contacts. This lets a caller pass the full domain into SYN-001 and preserve real negative and uncertain results. CORE-001B runs again on each generated canonical circuit with caller pins. Discovery findings refer to the board-only snapshot.

Run the end-to-end JSON example with the pinned Python environment from the repository root.

```powershell
python -B -m tests.test_cap001_discovery
```

The example declares the two sensor roles, discovers both board contact domains, and feeds them to SYN-001. The JSON contains the discovery reports, request, canonical circuits, and verifier traces. All results remain `TEST_ONLY_NOT_PRODUCTION`.
