# Execution report — CORE-001A-R1

- Session date: 2026-11-20 (Asia/Tbilisi).
- Authority: phase A–F and §§9–15 of the owner-supplied CORE-001A-R1 handoff. The original and revised CORE-001A contracts were available locally. ADR-0001 applies. ADR-0002 remains proposed.
- **Outcome: PARTIAL.** Completed conformance and OSS audit, project tracking reconciliation, and v1 supplemental acceptance tests. Mapping-kind correction requires `SCHEMA_DECISION_REQUIRED`.
- Initial branch: `codex/core-001a-acceptance-audit` at `1808e2942ad306af6c103f86f376d586ba806ad6`, initially clean. Reviewed that branch's audit without merging it.
- Verified baseline: `origin/main` at `b1db3e947d04508ca22d4ba55e3172616620bad2`. Task branch: `codex/core-001a-r1-research-conformance`.

## A. BOOT BRIEF and required reads

Reviewed AGENTS, PRODUCT, DECISION_AUTHORITY, DECISIONS, STATUS, NEXT, WORK_LOG, SESSION_PROTOCOL, VERIFICATION_POLICY, OSS_POLICY, ADR-0001/0002, OSS register, both skills, prior execution and independent audit reports, both prior contracts, all six named raw research inputs (01–03 and A–C), runtime and test files, and pinned dependency manifests. The [standalone research audit](CORE-001A-RESEARCH_CONFORMANCE_AUDIT.md) records source-level authority and conformance. The Research E file appeared untracked after the initial clean check and was left outside the R1 changes.

## B–C. Execution and file manifest

Audited the existing source, identified the v1 schema boundary, reran the baseline and probed the invariant before applying any corrective test change. The permissible additions exercise contract behavior already supported by v1. Production code, fixtures, manifests, raw research, decisions and rule vocabulary remained as in the baseline.

| Path | Change | Purpose |
| --- | --- | --- |
| `tests/test_core001a.py` | Modified | Two independent evidence and catalog-revision regression tests |
| `docs/STATUS.md` | Modified | Factual implementation/audit status and unresolved work |
| `tasks/NEXT.md` | Modified | Advisory owner-adjudication pointer |
| `tasks/WORK_LOG.md` | Appended | Audit and test record |
| `governance/OSS_REGISTER.csv` | Appended | Eight observed dependencies, with `REVIEW` status and distribution pending |
| `reports/CORE-001A-R1-REPORT.md` | Created | Execution and observed verification |
| `reports/CORE-001A-RESEARCH_CONFORMANCE_AUDIT.md` | Created | Standalone Georgian executive findings, detailed traceability and options |

## D. Acceptance by criterion

| Criterion | Observed result | Status |
| --- | --- | --- |
| Research A requirements, F-A01–15, T01–20, P1–10 and AM-01–04 | 71 individually traceable matrix rows with source, oracle, restrictions and remedies | PASS for required audit |
| Actual OSS/API classification and registry reconciliation | Pinned versions and installed license metadata matched, five transitives identified; eight `REVIEW` rows | PASS for factual audit |
| Independent reproduction | Same target ID with changed mapping kind returned verified | PASS for reproduction; implementation invariant FAIL |
| Existing tests | 11/11 passed before test changes | PASS |
| Supplemental v1 regressions | Two new tests passed, including eight invalid evidence subcases | PASS |
| Source-edition pin and topology stability | Old external pin rejects updated catalog. Definition digest stable for edition-only edit. Canonical snapshot round-trips, same net partition. | PASS |
| Unknown evidence | Unverified approval rejected for positive mapping; declared unknown remains unknown | PASS for exercised boundary |
| Trust of unpinned external approval | Self-issued approval can be internally consistent. Trusted expected pin is a separate input. | RESTRICTED |
| New mapping-kind negative regression after correction | Independent kind is absent from the v1 claim, and no corrected schema is approved | BLOCKED |
| Hardware measurements and future GPIO/electrical checks | Outside A/R1 scope | NOT_RUN |
| Tracking reconciliation and branch publication | Recorded path changes and Git evidence below | See publication record |

## E. Commands and observed outputs

Ran from repository root with the existing Windows x64 virtual environment:

```powershell
$exe = Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$env:HYPOTHESIS_STORAGE_DIRECTORY = Join-Path $env:TEMP 'inventor-edu-r1-hypothesis'
& $exe --version
& $exe -m pip check
& $exe -m pip list --format=freeze
& $exe -B -m unittest discover -v
```

Python 3.12.8 and pip 24.3.1. `pip check` printed `No broken requirements found.` The initial suite reported `Ran 11 tests in 0.670s` and `OK`. The final invocation of the same discovery command exited 0 with the following output:

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

----------------------------------------------------------------------
Ran 13 tests in 0.693s

OK
```

Final count 13 passed, 0 failed, 0 skipped. New functions in `tests/test_core001a.py` start at lines 229 and 251. Existing graph and passive participation tests remained in discovery.

Exact reproduction and adjacent source probes were run by piping this Python input to `& $exe -B -` from PowerShell. They operated on fresh in-memory copies of approved fixtures.

```python
from hashlib import sha256
import json
from inventor_edu import *
from tests.core001a_fixtures import BOARD, fixture_data, seal, part, t
def make(change=lambda *a: None):
    defs, docs, claims = fixture_data()
    board = next(x for x in defs if x["definition_id"] == BOARD)
    mapping = next(x["signal_ref"] for x in board["terminals"] if x["terminal_id"] == "J3.9")
    claim = next(x for x in claims if x["claim_id"] == "board-J3.9")
    change(mapping, claim, defs, docs, claims)
    return seal(defs, docs, claims)
def show(label, payload, **kw):
    try:
        catalog = load_catalog(payload, **kw)
        snap = create_snapshot(catalog, instances=(part(catalog,"board",BOARD),), junctions=(), conductors=())
        signal = resolve_terminal(catalog, snap, t("board","J3.9")).terminal.signal_ref
        print(label, signal.mapping_status, signal.target_kind, signal.target_id)
        return catalog, snap
    except EngineeringModelError as exc:
        print(label, exc.code)
base,snap = show("valid", make())
for field,value in [("target_kind","power_domain"),("target_id","GPIO19")]:
    show(field, make(lambda m,c,*_:m.update({field:value})))
for field,value in [("condition","J3.8"),("scope","Other revision"),("subject_definition_id","adafruit-3942-profile"),
                    ("source_document_id",None),("review_status","conflicting"),("review_status","unverified")]:
    show(f"claim:{field}={value}",make(lambda m,c,*_:c.update({field:value})))
show("missing_claim", make(lambda m,c,d,s,cs:cs.remove(c)))
show("declared_unknown", make(lambda m,c,*_: (m.update(mapping_status="unknown"),c.update(review_status="unverified"))))
revised = make(lambda m,c,d,s,cs:next(x for x in s if x["source_document_id"]=="S18").update(edition="R1 probe edition"))
new,new_snap = show("resealed_source_edition", revised)
show("external_old_pin", revised, expected_sha256=base.catalog_digest)
print("edition", base.catalog_digest != new.catalog_digest, snap.instances[0].definition_digest == new_snap.instances[0].definition_digest)
print("canonical", serialize_snapshot(restore_snapshot(serialize_snapshot(new_snap),new)) == serialize_snapshot(new_snap))
print("graph_partition_unchanged", compute_nets(base,snap).nets == compute_nets(new,new_snap).nets)
print("snapshot_sha256", compute_nets(new,new_snap).snapshot_sha256 == "sha256:" + sha256(serialize_snapshot(new_snap)).hexdigest())
for label,payload in [("catalog_duplicate_key",b'{"x":1,"x":2}'),("catalog_bad_utf8",bytes([255])),("catalog_array",b'[]')]:
    show(label,payload)
try:
    direct = CircuitSnapshot(schema_version="1.0", catalog_digest=base.catalog_digest, instances=(), junctions=(),
        conductors=(Conductor(connection_id="w",endpoint_a=t("missing","A"),endpoint_b=t("missing","B")),))
    raw = serialize_snapshot(direct)
    print("unbound_serializer_bytes",len(raw))
    restore_snapshot(raw,base)
except EngineeringModelError as exc:
    print("unbound_restore",exc.code)
```

Observed output, exit 0:

```text
valid verified soc_gpio GPIO18
target_kind verified power_domain GPIO18
target_id AMBIGUOUS_MAPPING
claim:condition=J3.8 AMBIGUOUS_MAPPING
claim:scope=Other revision AMBIGUOUS_MAPPING
claim:subject_definition_id=adafruit-3942-profile AMBIGUOUS_MAPPING
claim:source_document_id=None AMBIGUOUS_MAPPING
claim:review_status=conflicting AMBIGUOUS_MAPPING
claim:review_status=unverified AMBIGUOUS_MAPPING
missing_claim AMBIGUOUS_MAPPING
declared_unknown unknown soc_gpio GPIO18
resealed_source_edition verified soc_gpio GPIO18
external_old_pin CATALOG_DIGEST_MISMATCH
edition True True
canonical True
graph_partition_unchanged True
snapshot_sha256 True
catalog_duplicate_key MALFORMED_JSON
catalog_bad_utf8 MALFORMED_JSON
catalog_array INVALID_CATALOG
unbound_serializer_bytes 352
unbound_restore UNKNOWN_INSTANCE
```

## F–I. Findings, schema decision, licensing and rollback

The mapping record stores `target_kind`, but v1's evidence claim stores the target ID as text and uses a condition for contact identity. It contains no independent type assertion. A versioned typed claim payload is the recommended minimum correction. The conformance audit compares it with a versioned kind field and a separately pinned typed sidecar, including how each affects digest inputs and what must be reverified. Require an owner decision about versioning, how legacy v1 mappings are consumed, catalog trust and explicit migration. Until then, positive kind-dependent evaluation remains blocked. The independent runtime boundary probe also confirmed that direct object construction can produce serializer output that fails restoration.

Installed package metadata was read using `importlib.metadata.distribution` under the same interpreter, checking version, license expression or declared license, non-extra requirements and license files. The eight observed packages are Pydantic 2.14.4, pydantic-core 2.50.5, annotated-types 0.8.0, typing-extensions 4.16.0, typing-inspection 0.4.5, NetworkX 3.7, Hypothesis 6.170.17 and sortedcontainers 2.4.0. No new package or third-party asset was installed. All eight license files were found locally. The factual register additions do not authorize redistribution.

Git preflight used `git fetch origin`, `git branch -avv`, `git ls-remote --symref origin`, and status inspection. Created this branch from the verified baseline with `git switch -c codex/core-001a-r1-research-conformance origin/main --no-track`. A checkpoint can be reverted with a new owner-authorized commit. The v1 data and deployment are unaffected by the test and documentation changes.

## J. Owner review

Attach both standalone reports to the architecture conversation. The minimum decision is the approved independent mapping kind representation, catalog version and migration policy, and external provenance admission. Positive mapping-dependent CORE-001B findings remain on hold. Separate authorization is required for CORE-001B and CORE-001C.
