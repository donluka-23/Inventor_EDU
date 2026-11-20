# Execution report — CORE-001A-R2 / owner-selected Option A1

- Session date: 2026-11-20 (Asia/Tbilisi).
- Authorized plan: CORE-001A-R2 — Typed Mapping Evidence & Versioned Catalog Admission, attachment `bd1daa20-40a3-4959-8e14-a75b7fb1cf1f`.
- Engineering outcome: **PASS** for the authorized R2 scope. Owner review and future verification authorization remain separate.
- Starting branch: `codex/core-001a-r1-research-conformance`. The fetched and remote-verified predecessor was `9e9f20e54631822672ac8f849fce523534b5e70d`. Task branch: `codex/core-001a-r2-typed-mapping`. Origin: `https://github.com/donluka-23/Inventor_EDU.git`.

## A. BOOT BRIEF and authority

Reviewed repository instructions, product, decision authority and index, status, next pointer, session and verification protocols, applicable ADRs, the evidence-gated-engineering skill, the original and revised CORE-001A contracts, Research A and AM-01–AM-04, the implementation report, the separate audit from its remote branch, both R1 reports and the relevant B/C integration boundaries. Inspected the models, catalog admission, resolver, fixtures and existing tests. ADR-0001 applies. ADR-0002 remains proposed. R2 explicitly selected A1 and catalog v1.1 in the task handoff. The unrelated untracked Research E file was preserved and excluded.

## B–C. Changes executed and manifest

| File | Change |
| --- | --- |
| `inventor_edu/models.py` | Added strict immutable `SignalMappingEvidence` and the separate catalog version type. |
| `inventor_edu/core.py` | Added version-aware claim admission, typed mapping comparison, conflict checks, and a legacy resolver downgrade. |
| `inventor_edu/__init__.py` | Exported `SignalMappingEvidence`. |
| `tests/core001a_fixtures.py` | Added a separate v1.1 evidence fixture authored from reviewed source rows and a version argument to the fixture sealer. |
| `tests/test_core001a.py` | Changed one R1 expected legacy mapping status from `verified` to `unknown`, as required by R2. The contact, identifier and topology expectations remain the same. |
| `tests/test_core001a_r2.py` | Added nine tests for the two catalog versions, mapping evidence, external pins, migration, hash vectors and unchanged connectivity. |
| `docs/STATUS.md`, `tasks/NEXT.md`, `tasks/WORK_LOG.md` | Recorded factual R2 implementation, boundaries and owner review pointer. |
| `reports/CORE-001A-R2-REPORT.md` | Created this report. |

Previous reports, research, ADRs, OSS register and dependency manifests were preserved. No external dependency or third-party asset was added.

## D. Acceptance by criterion

| Criterion | Independent observation | Result |
| --- | --- | --- |
| 1, 12. Valid manufacturer/typed mapping | `test_verified_typed_mapping_uses_independent_contact_kind_and_target` asserts the literal reviewed J3.9, `soc_gpio`, `GPIO18` tuple and v1.1 `verified`. | PASS |
| 2. Wrong mapping kind with same identifier and fresh digests | `test_resealed_wrong_kind_same_target_and_other_pair_mismatches_reject` mutates only the mapping kind to `power_domain` with evidence unchanged and reseals the definition and catalog. Admission rejects with `AMBIGUOUS_MAPPING`. The inverse evidence-only mutation also rejects. | PASS |
| 3, 4. Wrong target identifier or terminal | Same test changes each field independently on both claim and mapping sides and asserts `AMBIGUOUS_MAPPING`. | PASS |
| 5–9. Definition/scope, missing claim, approval, conflict, source/locator | `test_typed_claim_requires_scope_review_and_qualified_source` asserts exact rejections for each negative. `test_conflicting_typed_claim_cannot_be_bypassed_by_selecting_another_claim` adds a separate conflicting or contradictory approved claim. | PASS |
| 10, 11. Legacy restoration and no positive typed authority | `test_legacy_snapshot_restore_and_explicit_migration_keep_electrical_membership` preserves legacy bytes/pins and restores with the original catalog. `test_legacy_wrong_kind_declaration_has_no_positive_resolved_authority` confirms the old false-positive input surfaces as `unknown`. | PASS |
| 13. Incomplete v1.1 evidence | Missing typed fields fail schema validation. A string/null claim cannot support a positive mapping. A mapping explicitly marked `unknown` without a claim remains unknown. A v1.0 envelope with a typed claim rejects. | PASS |
| 14. Source revision and external pin | `test_source_revision_requires_new_external_pin` rejects the old external pin, and observes that a matching self-supplied replacement pin proves consistency alone. The definition digest stays stable. | PASS |
| 15. Canonical byte/hash vectors | `test_literal_typed_catalog_vector` reads hand-authored v1.1 canonical JSON with fixed SHA-256 vectors computed via stdlib only. Migration test pins the v1 catalog, board definition and pre-R2 snapshot digest. Existing literal snapshot/net vectors still pass. | PASS |
| 16. Partition and IDs | Migration compares serialized topology apart from the snapshot SHA. The fixed board-to-sensor net ID and two separate passive leads match expectations. All earlier graph, editing, NetworkX and Hypothesis checks pass. | PASS |
| Physical conditions and future GPIO rules | No hardware measurement or later subsystem execution. | NOT_RUN |

## E. Commands and observed results

From the repository root, using the existing Windows x64 environment:

```powershell
$exe = Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$env:HYPOTHESIS_STORAGE_DIRECTORY = Join-Path $env:TEMP 'inventor-edu-r2-hypothesis'
& $exe --version
& $exe -m pip check
& $exe -m pip list --format=freeze
& $exe -B -m unittest discover -v
git diff --check
```

Before editing, discovery exited 0 with `Ran 13 tests in 0.682s` and `OK`. Final discovery exited 0. Python was 3.12.8, pip 24.3.1, Pydantic 2.14.4, pydantic-core 2.50.5, annotated-types 0.8.0, typing-extensions 4.16.0, typing-inspection 0.4.5, NetworkX 3.7, Hypothesis 6.170.17 and sortedcontainers 2.4.0. Pip reported `No broken requirements found.`

```text
test_canonical_round_trip_and_digest_mismatches (tests.test_core001a.CoreTests.test_canonical_round_trip_and_digest_mismatches) ... ok
test_crossings_and_geometry_independence (tests.test_core001a.CoreTests.test_crossings_and_geometry_independence) ... ok
test_deletion_duplicate_and_hash_vector (tests.test_core001a.CoreTests.test_deletion_duplicate_and_hash_vector) ... ok
test_evidence_admission (tests.test_core001a.CoreTests.test_evidence_admission) ... ok
test_invalid_endpoints_ids_and_identity (tests.test_core001a.CoreTests.test_invalid_endpoints_ids_and_identity) ... ok
test_junction_only_and_singleton_with_stub (tests.test_core001a.CoreTests.test_junction_only_and_singleton_with_stub) ... ok
test_literal_canonical_snapshot_vector (tests.test_core001a.CoreTests.test_literal_canonical_snapshot_vector) ... ok
test_mapping_rejects_resealed_mismatched_or_unapproved_evidence (tests.test_core001a.CoreTests.test_mapping_rejects_resealed_mismatched_or_unapproved_evidence) ... ok
test_networkx_oracle_permutation_partition_and_single_edge_deletion (tests.test_core001a.CoreTests.test_networkx_oracle_permutation_partition_and_single_edge_deletion) ... ok
test_reference_profiles_and_generalization (tests.test_core001a.CoreTests.test_reference_profiles_and_generalization) ... ok
test_source_edition_changes_catalog_pin_without_changing_connectivity (tests.test_core001a.CoreTests.test_source_edition_changes_catalog_pin_without_changing_connectivity) ... ok
test_strict_schema_and_resource_limits (tests.test_core001a.CoreTests.test_strict_schema_and_resource_limits) ... ok
test_three_terminals_junction_and_reordering (tests.test_core001a.CoreTests.test_three_terminals_junction_and_reordering) ... ok
test_conflicting_typed_claim_cannot_be_bypassed_by_selecting_another_claim (tests.test_core001a_r2.TypedMappingEvidenceTests.test_conflicting_typed_claim_cannot_be_bypassed_by_selecting_another_claim) ... ok
test_legacy_cannot_carry_typed_evidence_and_incomplete_mapping_stays_unknown (tests.test_core001a_r2.TypedMappingEvidenceTests.test_legacy_cannot_carry_typed_evidence_and_incomplete_mapping_stays_unknown) ... ok
test_legacy_snapshot_restore_and_explicit_migration_keep_electrical_membership (tests.test_core001a_r2.TypedMappingEvidenceTests.test_legacy_snapshot_restore_and_explicit_migration_keep_electrical_membership) ... ok
test_legacy_wrong_kind_declaration_has_no_positive_resolved_authority (tests.test_core001a_r2.TypedMappingEvidenceTests.test_legacy_wrong_kind_declaration_has_no_positive_resolved_authority) ... ok
test_literal_typed_catalog_vector (tests.test_core001a_r2.TypedMappingEvidenceTests.test_literal_typed_catalog_vector) ... ok
test_resealed_wrong_kind_same_target_and_other_pair_mismatches_reject (tests.test_core001a_r2.TypedMappingEvidenceTests.test_resealed_wrong_kind_same_target_and_other_pair_mismatches_reject) ... ok
test_source_revision_requires_new_external_pin (tests.test_core001a_r2.TypedMappingEvidenceTests.test_source_revision_requires_new_external_pin) ... ok
test_typed_claim_requires_scope_review_and_qualified_source (tests.test_core001a_r2.TypedMappingEvidenceTests.test_typed_claim_requires_scope_review_and_qualified_source) ... ok
test_verified_typed_mapping_uses_independent_contact_kind_and_target (tests.test_core001a_r2.TypedMappingEvidenceTests.test_verified_typed_mapping_uses_independent_contact_kind_and_target) ... ok
Ran 22 tests in 0.814s
OK
```

Independent compatibility controls:

- Ran `git archive --format=zip --output=$zipPath 9e9f20e54631822672ac8f849fce523534b5e70d inventor_edu tests` and `Expand-Archive -LiteralPath $zipPath -DestinationPath $legacyPath` in a temporary location. From that archived R1 runtime, piped the equivalent migration snapshot construction to `& $exe -B -`, then printed `sha256(serialize_snapshot(snapshot)).hexdigest()`. The archived board, sensor, resistor and two wires produced `2eda9446614581287eff52d1bbe5e7e60140146e46303b97319531c3e73c6b23`. R2 asserts that exact legacy byte hash.
- Before changing runtime, `load_catalog(seal(*fixture_data()))` produced catalog pin `sha256:6b2f1c33f43a7c7d02ab9e3b1d5b73466cb9ade6dc235e3f5a3af98782de1934` and board definition pin `sha256:7884e0799a118c95709e2a871107871c428b03aeb11c436cf9befd32733b751f`. Both pins are asserted by R2.
- The separate stdlib-only hash calculation over literal sorted JSON gave v1.1 catalog hash `18975dcdc4a645f586820d8d16c8c4b0f2a44438e9cd6f31615a19dc27b42a62` and definition hash `0cbfb905aa8c3773ea5e7edc27efee448c78d6d3fdd8d8a6fdf7bf9030afc8ce`. The test neither uses the production encoder nor the fixture sealer to construct that input. It then checks the full readback bytes.
- The reviewed v1.1 migration fixture was independently loadable and produced `sha256:26e5b04153a1ca249c764d9c7fc327f3e64d34e28a819bf2c4c7f3a111b0b05e`. This is a test fixture pin, not an owner-issued deployment trust pin.

## F. Schema, semantics and provenance

**Before, catalog schema 1.0:** a mapping claim uses `claim_type: "signal_mapping"`, string `value: "GPIO18"`, and `condition: "J3.9"`. The stored mapping declares its own kind. The admission rule retains the legacy validation and canonical digest for backward compatibility. Its historical catalog records are readable without mutation.

**After, catalog schema 1.1:** a mapping claim has a strict object value, for example `{"terminal_id":"J3.9","target_kind":"soc_gpio","target_id":"GPIO18"}`. The type accepts exactly the three required fields and no unknown target kind. Subject definition, profile scope, review, conflicts, source document and locator are checked separately. The typed tuple matches the mapping by exact equality without target ID prefix conventions. Nonmapping claims and internal ties keep their approved representation. A malformed claim fails schema validation and an incomplete or mismatched positive claim fails admission. Explicitly unknown mappings can omit evidence. Conflicting declarations, linked conflicts and distinct approved targets for the same scoped contact block positive admission. A version 1.0 envelope cannot carry the new object.

The documented source policy requires manufacturer-class evidence whose publisher matches the verified manufacturer to support a SoC or power-domain mapping. Retailer-class evidence whose publisher matches the declared distributor supports a scoped external signal only. Synthetic labels and other claim classes cannot confer positive mapping authority. A locator must exist and have nonblank text. Admission cannot validate the accuracy of free-form location content or authenticate the actual publisher.

The twelve migrated values were independently expressed from reviewed primary material. The Espressif V4 header tables identify J2 positions 1, 5, 14 and 19, J3 positions 1, 7, 8 and 9, and scope the board profile to ESP32-DevKitC-32E / ESP32-WROOM-32E. The Adafruit retail page and pinout identify PID3942 and the Vcc, Trig, Echo and Gnd external contacts. The migration fixture deliberately authors these typed values separately from the legacy mapping object. It keeps the documented-profile qualification and preserves the unknown OEM, PCB and individual hardware limitations. [Espressif V4 board guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html) · [Adafruit retail profile](https://www.adafruit.com/product/3942) · [Adafruit pinouts](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/pinouts)

## G. API, migration and compatibility

- `load_catalog(payload, expected_sha256=...)` keeps its signature and now admits versions 1.0 and 1.1 under their explicit rules. The pin parameter compares the canonical digest and carries no provenance on the origin of the expected value.
- `resolve_terminal` keeps its signature, physical contact identity, target hints and claim references. It returns a legacy declaration as `mapping_status="unknown"` on the resolved terminal. Raw v1.0 catalog records keep their historical flag for byte compatibility. Future consumers must not interpret that raw flag as kind-verified evidence. Valid v1.1 mapping resolution can return `verified` for internal admission. It is not an electrical or hardware verdict.
- `SignalMappingEvidence` is a new public immutable value type. `EvidenceClaim.value` adds that type with the catalog admission restrictions above. Definition, circuit and topology schemas stay at v1.0. `create_snapshot`, `restore_snapshot`, `compute_nets` and both serialization entry points keep their signatures and existing electrical semantics.
- Migration is explicit: keep the old reviewed catalog and its pinned snapshots, author and review typed evidence into a v1.1 catalog, obtain a new catalog pin and create a new snapshot from the previously validated engineering state with the new catalog. No automatic write-back or production migration utility was introduced. The new envelope and evidence change the catalog digest. Definitions in the migration fixture are byte-equivalent since the references and mapping payloads are unchanged. Existing definition digests therefore stay the same. Both snapshot bytes and snapshot hash change on rebinding because the catalog pin changes. Electrical membership and net IDs remain unchanged.
- Research A's source-qualified ties, strict typed records, canonical serialization, physical references, deterministic stdlib BFS and NetworkX/Hypothesis test boundary remain intact. No editor geometry, GPIO rule, voltage model or simulator was added.

## H–I. Remaining restrictions, licensing and rollback

Positive CORE-001B findings require **both** independently typed v1.1 evidence and an owner-controlled reviewed expected catalog digest. The API cannot prove how a caller obtained that digest. Matching one's own recomputed digest is not authentication. Real hardware and electrical behavior remain outside the scope of the migration fixture.

The serializer validation issue and difference between repository findings `PASS/FAIL/UNKNOWN/NOT_APPLICABLE` and the B/C proposed vocabulary stay open. Formal documentation of the catalog architecture decision remains an owner action. No OSS intake occurred. Rollback is a new owner-authorized revert on the task branch. Persisted v1 artifacts need no rollback or rewrite.

## J. Owner review

Review the R2 report and the verified branch. CORE-001B and CORE-001C still require their own authorization and evidence contracts. R2 acceptance is limited to the typed catalog admission and compatibility behavior tested here.

## Verified publication

The reviewed R2 implementation, tests and documentation were committed as `3e63368196f912fff1418c0a3bb45e6464d54f13` (`fix(core-001a-r2): require typed mapping evidence in catalog v1.1`). Staging matched the ten authorized paths, the staged whitespace check passed, and a staged credential-pattern scan returned no hits. The unrelated Research E file remained untracked.

`git push -u origin codex/core-001a-r2-typed-mapping` exited 0 and set upstream tracking. `git ls-remote --heads origin refs/heads/codex/core-001a-r2-typed-mapping` then returned `3e63368196f912fff1418c0a3bb45e6464d54f13` for the exact task ref. This follow-up report entry records the already-observed publication. The task history remains separate from `main`.

**Final R2 result: PASS.**
