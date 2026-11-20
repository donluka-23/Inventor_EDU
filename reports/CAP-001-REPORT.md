# CAP-001 revision 2 execution report

- Date — 2026-11-20, Asia/Tbilisi.
- Frozen plan — [CAP-001 revision 2](../tasks/CAP-001.md).
- Recommendation — **PASS** for independent owner review of the bounded experiment and research archive.
- Verified predecessor — `origin/codex/syn-001-candidate-generation` at `c0f3fd83f045ed3b8f2cb6be0060474ddcbb9d43`.
- Task branch — `codex/cap-001-terminal-discovery`.

## A. BOOT BRIEF

Verified the repository root and authorized origin `https://github.com/donluka-23/Inventor_EDU.git`, fetched origin, checked the live predecessor against the frozen SHA, and inventoried local work. The working tree contained the four original untracked Research F–I files. The remote task branch was absent. No preflight blocker was open.

Reviewed `AGENTS.md`, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, `docs/SESSION_PROTOCOL.md`, `docs/OSS_POLICY.md`, `docs/VERIFICATION_POLICY.md`, `docs/adr/ADR-0001-product-scope.md`, the evidence-gated-engineering skill, the frozen task, report template, master plan, and SYN-001 execution report. Inspected the existing CORE-001A, CORE-001B and SYN-001 interfaces and reviewed fixture tests. Accepted ADR-0001 applies. ADR-0002 remains on hold.

Allowed writes covered the four archive files as exact copies, the discovery module, independent tests, contract, task, report, three tracking files and the master-plan revision. Existing engines, catalogs, tests, ADRs, licensing, frontend, firmware and electrical work were outside scope. The gates were archival integrity, the 18 acceptance criteria, full regression, authentic GPIO source admission and headless replay.

## B. Research archival

Ran `git status --short --untracked-files=all`. Each expected document had one original at its existing path. All four decoded as nonempty UTF-8, had no NUL bytes, and had distinct SHA-256 digests. Their title and status metadata identified historical Research F, G, H and I documents. No individual authorship was established from the heading metadata. Credential, private-key, token, email and phone screening raised no credential or private-contact blocker. The seven email occurrences in Research F were reviewed in their context as cited organization contact listings. The review was limited to identity, provenance, integrity and archival screening. Research conclusions were neither interpreted for implementation nor changed.

| Original repository-relative path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/research/raw/RESEARCH_F_GEORGIAN_MARKET_COMPETITION_AND_PARTNERSHIPS.md` | 168456 | `2eb62e01ac952bd459a633b60ffbb32899e60c28b6e6b878be99e0e70a8da04f` |
| `docs/research/raw/RESEARCH_G_WOKWI_UX_ARCHITECTURE_AND_DEMO_STRATEGY.md` | 90718 | `9f105057c613e9111ec472f16f9655ee26fc777a9331350e922eb34f6a8f4d22` |
| `docs/research/raw/RESEARCH_H_INTENT_REQUIREMENTS_AND_EDUCATIONAL_FEEDBACK.md` | 196407 | `ee046362876c1a439c420abdee545bb116b45de5deb264d81978859bcf6f0714` |
| `docs/research/raw/RESEARCH_I_COMPONENT_CAPABILITY_MATCHING_AND_EDUCATIONAL_KNOWLEDGE.md` | 130529 | `6ea36ff9aed4365edfc0e2fdbcbaa2c08ad4ab11e0e61dd70df0a07032e0b4c7` |

Staged only those paths. The staged manifest had exactly four additions. For each path `git hash-object --no-filters <path>` equaled `git rev-parse :<path>`, proving the original bytes matched the staged blobs. The dedicated `docs(research): archive owner-provided Research F-I` commit is `f66d9af3db5fad3de878fbad3d45b06ee77c4ea4`. It precedes implementation and contains only those four originals. Research J and other artifacts were outside its manifest.

## C. Engineering execution and file manifest

`CapabilityQuery` is a strict, frozen version 1.0 record with query and originating requirement IDs, exact board instance and definition IDs and definition digest, `GPIO_IN` or `GPIO_OUT`, `ACTIVE`, catalog and fact-set digests, and evidence scope. `discover_gpio_terminals(query, catalog, board, fact_set, *, trusted_catalog_sha256, trusted_factset_sha256)` returns a frozen `CapabilityDiscoveryReport` with the query, board-only snapshot digest, ruleset version and candidates. Each frozen `TerminalCandidate` exposes the real terminal ref, resolved mapping, raw B findings, separate coverage, evidence claim IDs, limitation reason codes and bounded qualification.

The adapter validates the query, uses CORE-001A to create the board snapshot and checks declared evidence references. It enumerates the exact catalog definition's contacts in ID order. Typed GPIO or unknown mappings, matching-scope GPIO fact contacts, and undeclared input/output/I/O contacts enter evaluation. The last group remains provisional until B confirms the mapping. The adapter does not interpret labels. B validates external pins and fact-set binding and evaluates pin mapping, physical capability, board availability, active configuration and electrical compatibility for all contacts in one batch. A known FAIL yields `KNOWN_UNSUITABLE`. Mapping and direction PASS with no finding FAIL yield `FUNCTION_CONFIRMED_FOR_STATED_CHECK`. Other cases yield `UNRESOLVED_EVIDENCE`.

| Path | Change |
| --- | --- |
| `inventor_edu/capability_discovery.py` | Added immutable query/result types and discovery adapter |
| `tests/test_cap001_discovery.py` | Added 17 independent methods and the headless replay |
| `docs/prototype/CAPABILITY_DISCOVERY_CONTRACT.md` | Added API, scope, qualification and replay contract |
| `tasks/CAP-001.md` | Added frozen owner task |
| `reports/CAP-001-REPORT.md` | Added this execution and archival evidence |
| `docs/STATUS.md`, `tasks/NEXT.md`, `tasks/WORK_LOG.md` | Updated factual tracking and pending owner review |
| `docs/prototype/MASTER_PLAN.md` | Increased version to 1.2 and recorded CAP-001 as authorized |

The master-plan diff retains previous milestone authorizations, fixed non-goals, deferred opportunities, risk register and integration sequence. Task, status, pointer, work log and report were reconciled. Historical reports, decisions, ADRs and OSS records needed no updates. No dependencies, third-party code or license changes were introduced.

## D. Headless integration and acceptance

The documented ESP32-DevKitC-32E V4 case discovered the same five physical contacts for both roles. The caller passes the complete investigated domains into the existing SYN-001 request, including negative cases, and supplies the existing independently pinned catalog and facts. The replay sets the two sensor terminal roles and does not supply a list of board contacts.

| Physical contact | GPIO_OUT qualification | GPIO_IN qualification |
| --- | --- | --- |
| J2.5 / GPIO34 | KNOWN_UNSUITABLE, output fails | FUNCTION_CONFIRMED_FOR_STATED_CHECK |
| J3.14 / GPIO0 | FUNCTION_CONFIRMED_FOR_STATED_CHECK | FUNCTION_CONFIRMED_FOR_STATED_CHECK |
| J3.19 / GPIO6 | KNOWN_UNSUITABLE, board reservation | KNOWN_UNSUITABLE, board reservation |
| J3.8 / GPIO19 | FUNCTION_CONFIRMED_FOR_STATED_CHECK | FUNCTION_CONFIRMED_FOR_STATED_CHECK |
| J3.9 / GPIO18 | FUNCTION_CONFIRMED_FOR_STATED_CHECK | FUNCTION_CONFIRMED_FOR_STATED_CHECK |

SYN-001 exhausted the domain in 30 nodes with 5 exclusivity prunes, 20 evaluated assignments, 20 verifier calls, and 11 known hard rejections. All 9 remaining assignments retained unresolved obligations. The `sensor/Trig ↔ board/J3.9` and `sensor/Echo ↔ board/J3.8` alternative has two actual conductors, separate CORE nets with the expected members, and canonical snapshot digest `sha256:6fe1964503bdc98e1c3f82bd6c817ed92d0cef800b73734c7c11518d10a1a230`. It remains `INCOMPLETE_WITH_EXPLICIT_OBLIGATIONS`. Board availability and firmware evidence were UNKNOWN. Electrical compatibility was NOT_EVALUATED. The two engines retain distinct snapshot-specific verifier outputs.

| Criterion | Independent observation | Result |
| --- | --- | --- |
| 1 | Exact board and catalog binding. Mismatched IDs, digests and scope reject. | PASS |
| 2 | Five catalog contacts identified in stable physical ID order. Power and ground excluded. | PASS |
| 3 | GPIO34 input passes. | PASS |
| 4 | GPIO18 output passes. Its findings and coverage match a direct B call. | PASS |
| 5 | GPIO34 output fails with `OUTPUT_NOT_CAPABLE`. | PASS |
| 6 | GPIO6 direction PASS retains `RESERVED_RESOURCE` FAIL and unsuitable qualification. | PASS |
| 7 | Missing, conflicting and mismatched mapping facts stay unresolved. | PASS |
| 8 | Wrong external catalog and fact-set pins raise B mismatch errors. | PASS |
| 9 | Absent pins and unreviewed facts produce no confirmed qualification. | PASS |
| 10 | Catalog/fact ordering changes preserve equal results. Records are immutable. | PASS |
| 11 | Equal display labels preserve distinct instance identity. | PASS |
| 12 | Source revision changes invalidate stale digests and row IDs. Changed capability is reevaluated. | PASS |
| 13 | Unsupported function and operating context raise validation errors. | PASS |
| 14 | Distinct fictitious MCU fixture runs through the same algorithm and verifier. | PASS |
| 15 | Dynamically discovered domains feed SYN-001 and yield real canonical conductors and nets. | PASS |
| 16 | UNKNOWN and NOT_EVALUATED remain distinct from PASS. | PASS |
| 17 | Exposed classifications remain bounded to this experiment. | PASS |
| 18 | Existing CORE, DATA, DEMO and SYN regressions pass. | PASS |
| Archive | Four distinct original byte sequences in the dedicated commit. | PASS |

## E. Commands and observed outputs

Ran from `D:\Inventor_EDU` using the installed environment pinned by `requirements-core001a.txt` and `requirements-core001a-test.txt`.

```powershell
$exe=Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$src=Join-Path $env:TEMP 'InventorEDU-CORE-001B-01-sources'
$env:INVENTOR_EDU_DATA001_SOURCE_DIR=Join-Path $env:TEMP 'InventorEDU-DATA-001-dc037a238eb5efcc034dd9d62e5775d5c21e90e4'
$env:HYPOTHESIS_STORAGE_DIRECTORY=Join-Path $env:TEMP 'InventorEDU-CAP-001-hypothesis'
& $exe --version
& $exe -m pip list --format=freeze
& $exe -B -m tests.gpio_source_acceptance $src
& $exe -B -m unittest tests.test_cap001_discovery -v
& $exe -B -m unittest discover -s tests -v
& $exe -B -m tests.test_cap001_discovery
```

Python 3.12.8 and the installed locked dependencies were confirmed. The authentic gate, targeted tests and full suite exited 0:

```text
PASS: five authentic artifacts matched pins; masks, pull-up, header, flash, strap and -32E scope checked
Ran 17 tests in 0.263s
OK
Ran 89 tests in 1.751s
OK
```

Full discovery passed all 89 methods, including 17 new CAP tests, 18 SYN tests, 10 DEMO tests and four authentic DATA-001 tests. Zero failures, skips or blocked tests. Two separate headless replay processes emitted identical JSON. Both exited 0.

## F. Trust, scope and owner review

Positive GPIO findings are confined to the documented hardware and operating context, with caller-supplied test trust pins. Discovery works on a board-only snapshot and exposes the full explored domain, including negative and unresolved contacts, for subsequent synthesis. No physical hardware validation or electrical or firmware verification was performed. The synthetic MCU test uses fictitious evidence separately from the reviewed fixture. All results remain `TEST_ONLY_NOT_PRODUCTION`.

`OWNER_DECISION_REQUIRED` — no architectural or archival blocker was identified. Owner acceptance is pending. To replay use the commands above. The predecessor branch provides the pre-CAP configuration. No new task or merge is authorized.

## G. Git publication

The implementation commit `c7defd2b68011385b47953e30ccf152e0ffabc6a` was pushed with `git push -u origin codex/cap-001-terminal-discovery`. The live `git ls-remote --heads origin refs/heads/codex/cap-001-terminal-discovery refs/heads/main` returned that exact task branch SHA. The fetched ref matched the live SHA. `git merge-base --is-ancestor` verified the archival commit in the fetched branch history, and all four archived blobs at the fetched head matched the original local bytes. The local task branch tracks its same-named origin branch. Remote `main` remained at `b1db3e947d04508ca22d4ba55e3172616620bad2`. The implementation staging checks confirmed the frozen attachment, the nine authorized paths, whitespace and the targeted credential scan. This report-only follow-up records the verified publication.
