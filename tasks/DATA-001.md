# DATA-001 — Source-Verified Component Data Integration Pilot

**Project:** INVENTOR EDU  
**Local repository:** `D:\Inventor_EDU`  
**GitHub:** `https://github.com/donluka-23/Inventor_EDU.git`  
**Task ID:** DATA-001  
**Revision:** 1  
**Execution type:** Bounded data acquisition, integration and independent acceptance testing  
**Authority:** Owner-supplied task, based on Research E and the implemented CORE-001A-R2

## 1. Mission

Demonstrate one complete, reproducible engineering-data integration workflow:

**Authorized external source → pinned source artifact → verified structure → exact component identity → CORE-001A catalog → deterministic topology → independent acceptance tests.**

Do not build another engineering model.

Do not implement CORE-001B GPIO rules or CORE-001C electrical computations.

Do not design a universal component database.

Do not build a generic EDA importer for every available library format.

The objective is to establish whether existing structured engineering data can be legally and reliably reused in INVENTOR EDU with minimal custom code and maintenance burden.

A successful implementation must use real source artifacts. Synthetic fixtures may support testing but cannot replace the actual external-source integration.

## 2. Approved engineering architecture

Preserve the existing CORE-001A-R2 architecture:

- Physical terminal identity.
- Logical signal mapping separately from physical terminals.
- Explicit terminal-to-net connectivity.
- Deterministic BFS.
- Validated internal ideal ties.
- Immutable Pydantic records.
- Catalog schema v1.1.
- Source and definition digests.
- Explicit unknown evidence.
- Existing canonical serialization.

The current connectivity engine is the source of truth for net membership.

No alternative connectivity graph, universal component ontology or parallel electrical truth model is authorized.

### Source-specific architecture

The pilot has two distinct input classes:

**Structural candidate data**

Official LibrePCB CC0 component/package/device files.

These may provide physical pads, logical signals and mappings after validation.

**Manufacturer engineering facts**

Official YAGEO component information.

These may provide exact manufacturer identity and independently reviewed electrical specifications.

Do not confuse structural library data with manufacturer electrical guarantees.

Do not use a CAD library's generic electrical pin type as proof of safe voltage compatibility.

## 3. Mandatory repository and research preflight

Before modifying files, read the current project governance and execution rules:

- `AGENTS.md`
- `docs/PRODUCT.md`
- `docs/DECISION_AUTHORITY.md`
- `docs/DECISIONS.md`
- `docs/STATUS.md`
- `docs/SESSION_PROTOCOL.md`
- `docs/VERIFICATION_POLICY.md`
- `docs/OSS_POLICY.md`
- `tasks/NEXT.md`
- `tasks/WORK_LOG.md`

Read the relevant accepted ADRs.

Read:

- `reports/CORE-001A-REPORT.md`
- `reports/CORE-001A-R1-REPORT.md`
- `reports/CORE-001A-RESEARCH_CONFORMANCE_AUDIT.md`
- `reports/CORE-001A-R2-REPORT.md`

Read the Research A, B and C documents.

Most importantly, read:

`RESEARCH_E_COMPONENT_DATA_AND_EVIDENCE_PIPELINE.md`

Research E may currently exist as an untracked local Markdown file rather than in the canonical research directory.

Locate it without deleting, overwriting or renaming unrelated files.

Verify its title, sections and content before using it as the source of this task.

If available, preserve an unchanged copy at:

`docs/research/raw/RESEARCH_E_COMPONENT_DATA_AND_EVIDENCE_PIPELINE.md`

Only create that canonical file if it does not already exist. Do not overwrite an existing version. Record its SHA-256 and provenance.

The Research E document remains research evidence, not authorization to implement all its recommendations.

Read its sections covering:

- Official LibrePCB libraries.
- Machine-readable data formats.
- License and commercial-use conditions.
- YAGEO exact component profile.
- Acquisition workflow.
- Independent admission gates E-01–E-18.
- Proposed minimal integration pilot.

Produce a concise BOOT BRIEF identifying existing APIs, exact scope, allowed files, dependencies, evidence gaps and required tests.

## 4. Git baseline and branch policy

Fetch remote metadata and inspect the complete local working tree.

Verify that the R2 predecessor branch exists:

`origin/codex/core-001a-r2-typed-mapping`

At handoff preparation, its verified HEAD was:

`095b06e39dc9a782453ac1e6894221cb706d94de`

Do not assume the branch has remained unchanged. Compare the live remote SHA with this reference and inspect any changes.

Create the task branch:

`codex/data-001-component-source-pilot`

Base it on the verified R2 implementation, preserving the R1/R2 history.

Do not begin from the outdated `main` baseline.

Do not merge the acceptance-audit branch, rewrite previous history, force-push or discard untracked files.

Keep the new task branch separate until its results have been reviewed.

The integration of accepted branches into `main` is a separate owner-controlled Git approval step, not part of this task.

## 5. External source A — LibrePCB CC0 structural data

**Authorized source family:**

`https://github.com/LibrePCB-Libraries/LibrePCB_Base.lplib`

The research identifies its official libraries as candidates for CC0 data reuse.

This task authorizes a narrowly scoped, read-only acquisition and import experiment using this official repository, conditional on verifying the exact artifact's rights.

It does not authorize installing the LibrePCB application, copying its GPL source code or redistributing an unreviewed dataset.

### Required evidence acquisition

1. Verify the official repository identity.
2. Retrieve its full Git commit SHA.
3. Review the actual `LICENSE.txt` and any relevant per-directory/per-file rights.
4. Locate one authentic two-terminal resistor-related library record.
5. Identify the exact component, package and device files needed.
6. Record each source-relative path and file SHA-256.
7. Record the applicable LibrePCB library format version.
8. Confirm whether the available data actually defines the required pad/signal relationships.
9. Inspect hidden pads, duplicate identifiers and unresolved references.
10. Preserve the source revision and license evidence in a reproducible ledger.

Use fixed commit references. Do not depend on floating `master`, `main` or `latest` URLs for an admitted artifact.

Download only what is necessary for the bounded experiment.

Do not copy vendor PDFs, artwork or unrelated third-party assets.

### Technical scope

Investigate the official LibrePCB representation of:

- Package.
- Physical pad.
- Component.
- Component signal.
- Device.
- Device pad-to-signal relationship.

The pilot must demonstrate a real, checked transformation of an eligible source record.

The chosen source file must actually exist. Do not invent a package UUID, signal mapping or component ID.

### Parser and integration requirements

Prefer existing approved parsing capabilities when they genuinely provide the required behavior.

Do not introduce a new third-party Python dependency without explicit approval under the OSS policy.

If a small project-specific reader is necessary:

- Support only the selected documented LibrePCB file subset.
- Handle nested S-expressions correctly.
- Reject malformed or unsupported source syntax.
- Preserve physical pad identity.
- Detect duplicate or unresolved references.
- Fail closed on ambiguous device/package joins.
- Enforce file size and parsing limits.
- Do not use broad regex matching as a substitute for correct nested-structure parsing.
- Do not claim general LibrePCB compatibility.

Use independently authored tests to demonstrate that the parser cannot silently change pad identity.

The official LibrePCB CLI `open-library --check` may be used as an optional external syntax/interoperability comparator only if already available and legally permitted.

Do not install or bundle the full application merely for this pilot.

If the source cannot be parsed safely within the approved constraints, stop the affected importer work and record the precise limitation instead of creating a plausible-looking substitute.

## 6. External source B — Exact manufacturer component

Use:

**Manufacturer:** YAGEO  
**Orderable part number:** `RC0603FR-0710KL`  
**Component:** 10 kΩ, 0603 resistor  
**Initial reference:** Research E, manufacturer source register S20

Official manufacturer reference:

`https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-0710KL`

### Required manufacturer review

Verify from the actual manufacturer material:

- Exact orderable MPN.
- Component family and package.
- Nominal resistance.
- Tolerance.
- Rated power.
- Rated-power temperature condition.
- Working-voltage condition.
- Any relevant derating limitations.
- Source edition or document generation date.
- Exact source sections/rows.
- Reuse and redistribution conditions.

Research E reports the following values as source-derived candidates:

- 10 kΩ nominal.
- ±1% resistance tolerance.
- 0.1 W rated power at 70°C.
- 0603 package.

Do not admit these as newly verified merely by copying the research summary.

Recheck the official manufacturer source and record exact applicability conditions.

If an authoritative source cannot be accessed or verified, label the affected properties `UNVERIFIED` and do not create a fabricated manufacturer-approved record.

### Critical representation rule

A resistor has two distinct physical contacts.

Its electrical resistance does not make those contacts an ideal conductive connection.

Do not create an `InternalIdealTie` between resistor terminals.

CORE-001A must represent the resistor's physical connectivity without computing or assuming its analog voltage/current behavior.

The numerical resistance, tolerance and ratings must not be forced into generic topology fields that do not represent such facts.

Keep quantitative electrical properties in a clearly identified external, source-qualified candidate fact record for later CORE-001C integration.

Do not introduce a new general-purpose electrical property ontology.

## 7. Structural mapping and source identity

The LibrePCB candidate may describe a generic two-terminal device or package.

The YAGEO record identifies a specific manufactured component.

**These are not automatically equivalent.**

Before linking them:

1. Verify whether the exact YAGEO MPN appears in the selected library record.
2. If it does not, classify the LibrePCB structure as a reusable generic candidate only.
3. Independently check the manufacturer's applicable physical package and contact correspondence.
4. Preserve the difference between generic pad structure and exact manufacturer identity.
5. Do not assert a verified MPN-to-package relationship without evidence.
6. Do not infer electrical ratings from the CAD record.
7. Do not copy unspecified internal connectivity into CORE-001A.

If the exact structural relationship cannot be established, the task may still complete a structural importer demonstration, but the YAGEO manufacturer-specific catalog must remain unapproved.

Report this as PARTIAL rather than manufacturing a false match.

## 8. Integration with CORE-001A-R2

Use the existing public interfaces wherever possible:

- `load_catalog`
- `create_snapshot`
- `restore_snapshot`
- `resolve_terminal`
- `compute_nets`
- `serialize_snapshot`
- `serialize_topology`

Use the existing typed records rather than inventing parallel domain classes.

The imported or curated structural candidate must be transformed into a valid, reproducible catalog representation compatible with catalog schema v1.1.

Do not fabricate GPIO or signal mappings for the resistor.

Do not create unverified internal ideal ties.

Maintain precise relationships between:

- The source repository and commit.
- The source artifact and digest.
- The selected generic package/device information.
- The exact manufacturer component, where independently established.
- The resulting canonical device definition.
- The resulting catalog digest.

Do not claim that source files have external trust merely because a catalog can calculate a valid SHA-256 digest.

A generated candidate catalog hash is an integrity reference, not an owner-approved deployment trust pin.

### External evidence boundary

The catalog importer must not independently award trusted engineering approval.

Generate candidates with explicit source references and unresolved review status where necessary.

The approved deployment/evidence trust gate remains outside the automated source import.

Do not add a new signing service, authentication infrastructure or certificate system.

## 9. Required topology demonstration

Construct a deterministic test using the imported two-terminal structural profile.

At minimum demonstrate:

**Case A — Isolated resistor**

A two-terminal resistor instance is placed in a circuit with no wires.

Expected behavior:

- Both physical terminals exist.
- They belong to separate singleton nets.
- No internal ideal short is inferred.
- No voltage, current or resistance computation is claimed.

**Case B — External connections**

Use the existing reviewed ESP32 board and sensor fixture identities.

Connect a board physical terminal to one resistor lead.

Connect the other resistor lead to a sensor physical terminal.

Expected behavior:

- The first resistor lead shares a net with its externally connected board terminal.
- The second resistor lead shares a different net with the externally connected sensor terminal.
- The two nets are not merged through the resistor.
- Unrelated board and sensor terminals preserve their existing connectivity.
- All wire and terminal IDs remain traceable.

These tests prove structural net membership only.

They do not imply that the circuit is electrically suitable or that the sensor would function.

**Case C — Deterministic replay**

Reorder component and conductor lists, reverse conductor endpoints and restore the same snapshot.

Expected behavior:

- Equivalent net partitions.
- Identical normalized outputs where the established canonical contract requires them.
- Stable net IDs for unchanged terminal membership.
- Source and catalog provenance remain identifiable.

## 10. Independent acceptance matrix

Implement tests with independent expected outcomes.

At minimum:

| ID | Required test |
|---|---|
| DATA-01 | Selected upstream repository, full commit and file hashes are recorded |
| DATA-02 | Exact file-level CC0 eligibility is verified or import is blocked |
| DATA-03 | Actual source file is parsed; synthetic fixtures alone are insufficient |
| DATA-04 | Selected two-terminal source has the expected independently reviewed pad identities |
| DATA-05 | Duplicate or dangling pad/signal references reject |
| DATA-06 | Invalid or unsupported nested source syntax fails closed |
| DATA-07 | Source modification invalidates the pinned file digest |
| DATA-08 | Exact manufacturer MPN is kept separate from generic library identity unless proven |
| DATA-09 | The candidate yields a valid CORE-001A catalog or reports a precise incompatibility |
| DATA-10 | Resistor leads are not joined by an ideal internal tie |
| DATA-11 | External wires generate correct independent net membership |
| DATA-12 | Reordering/reversal preserves deterministic topology |
| DATA-13 | Missing manufacturer electrical facts never become default numeric values |
| DATA-14 | Source edition or accepted catalog change requires new provenance review |
| DATA-15 | No existing CORE-001A regression is broken |
| DATA-16 | No unsupported electrical or safety PASS is emitted |
| DATA-17 | No third-party source is bundled beyond the reviewed rights and authorized scope |
| DATA-18 | Pilot outputs and claimed results are reproducible from recorded pinned inputs |

Do not create expected values by calling the same import function being tested.

Derive expected pad identifiers and relationships independently from the selected source files.

Keep malformed and negative fixtures separate from positive acceptance.

Report PASS, FAIL, BLOCKED and NOT_RUN per test.

For actual engineering-rule outcomes, preserve the repository's currently accepted result vocabulary. Do not silently resolve the separate B/C status terminology issue.

## 11. Quantitative development-efficiency assessment

The purpose of this pilot is not merely to show that an importer can be written.

Determine whether importing a permitted existing library actually reduces manual engineering work.

Record:

- Number of authentic source files inspected.
- Number of physical pads imported.
- Number of manual corrections required.
- Number of unresolved source relationships.
- Number of fields that required manufacturer review.
- Number of rejected mappings.
- New source lines and functions introduced.
- Additional runtime or test dependencies.
- Actual import and test runtime, if measured.
- Reproducibility after source reloading.
- Structural coverage of the selected exact component.
- Licensing and review tasks that remain manual.

If measurable, record actual engineering effort spent on source inspection, parser development, manual curation and review separately.

Do not present Research E's estimated engineering hours as measured savings.

Do not extrapolate one component's measured import cost to hundreds of components without explicitly labeling the assumption.

Conclude whether the demonstrated import path is preferable to preparing this exact component manually.

## 12. Allowed changes

The following paths are authorized, only where required:

- `tasks/DATA-001.md` — preserve this approved task specification.
- A narrowly scoped importer module under `inventor_edu/`.
- Tests and dedicated DATA-001 test fixtures.
- Small, independently authored normalized candidate data under `data/pilot/`.
- A source/evidence ledger under `reports/`.
- `docs/research/raw/RESEARCH_E_COMPONENT_DATA_AND_EVIDENCE_PIPELINE.md`, create-only from verified original.
- `docs/STATUS.md`.
- `tasks/NEXT.md`.
- `tasks/WORK_LOG.md`.
- `governance/OSS_REGISTER.csv` for factual candidate/intake reconciliation only.
- `reports/DATA-001-REPORT.md`.

Preserve the existing filename and project conventions where they already define these responsibilities.

Do not create duplicate sources of project status or architecture decisions.

Do not modify the CORE-001A graph algorithm, Pydantic model definitions or persistence contracts.

Do not add new dependencies.

Do not modify previous research and execution reports.

Do not alter ADR status.

Do not update the project product license.

Do not add a database, frontend or new runtime service.

Do not commit temporary bulk source clones or manufacturer PDFs.

## 13. OSS and rights gate

Before persisting any third-party data:

1. Verify the selected source's exact file-level license.
2. Record the upstream commit and file digest.
3. Identify copied versus independently authored data.
4. Record actual intended internal use and potential public distribution.
5. Preserve required notices.
6. Check for third-party files not covered by the repository's general license.
7. Evaluate source integrity and maintenance implications.
8. Record applicable conditions in the OSS register.

This task authorizes a bounded internal CC0-source evaluation, not unrestricted third-party ingestion or commercial redistribution.

Research E lists LibrePCB libraries as `APPROVED_CANDIDATE`. Do not silently promote the entire library ecosystem to `APPROVED`.

Only the exact evaluated files may become eligible for further owner consideration.

If the precise required permissions cannot be established, stop the affected import. Do not bypass the policy by changing the source.

Never automatically ingest electrical safety limits extracted by an LLM.

## 14. Deliverables

### Deliverable A — Source and evidence ledger

Create:

`reports/DATA-001_SOURCE_AND_EVIDENCE_LEDGER.md`

Include:

- Official source repositories.
- Selected pinned upstream commits.
- Actual selected files.
- File SHA-256 values.
- Relevant licenses.
- Exact component/package identifiers.
- Source locators.
- Imported versus manually curated facts.
- Unsupported or missing facts.
- Evidence review status.
- Manufacturer/source disagreements.
- Rights and redistribution restrictions.
- Reproducibility steps.

### Deliverable B — Actual import demonstration

Provide the minimal code and machine-readable artifacts necessary to:

- Read the selected authentic LibrePCB source files.
- Reproduce the selected structural candidate.
- Produce or validate an existing CORE-001A-compatible catalog.
- Demonstrate actual net computation.
- Detect the specified negative cases.

Do not claim an import demonstration if the input was only a manually invented stand-in.

If genuine integration cannot be completed without a new architectural decision, preserve the validated subset and mark the remaining stage BLOCKED.

### Deliverable C — Execution report

Create:

`reports/DATA-001-REPORT.md`

Required content:

1. Exact task and authority.
2. Baseline repository and Git SHA.
3. Selected real source artifacts.
4. Code/files changed.
5. Actual library/API reuse inventory.
6. Source and license admission findings.
7. Demonstrated import path.
8. Exact transformed component and terminal identities.
9. Independent test results.
10. Remaining manual review.
11. Measured effort and cost observations.
12. Engineering correctness limitations.
13. Comparison with manual curation.
14. Research E requirements implemented.
15. Deviations from research and reasons.
16. Remaining decisions needed from the owner.
17. Git branch, commit SHA and push verification.
18. Final recommendation: CONTINUE / NARROW / HOLD.

Conclude with execution status:

`PASS / PARTIAL / BLOCKED`.

Do not label the whole task PASS solely because existing CORE-001A tests remain green.

## 15. Existing regression suite

Run all existing CORE-001A tests, including R1 and R2.

The R2 execution report recorded 22 passing tests.

Treat this as the previous baseline, not an assumed current outcome.

Record the actual new result:

- Existing tests passed.
- DATA-001 tests passed.
- Total discovered tests.
- Failed tests.
- Skipped or blocked tests.
- Actual commands and environment.
- Any independent source-validation tool used.

Do not suppress failed tests.

Do not edit expected outputs merely to make the implementation pass.

## 16. Documentation and repository history

Follow the project session lifecycle.

Update authorized project tracking files with verified facts only.

Mark DATA-001 as a successful structural import only if actual pinned source data was parsed and correctly mapped.

If manufacturer or license evidence remains incomplete, record the actual limitation.

Do not mark CORE-001B or CORE-001C as implemented or authorized.

Before committing:

- Review all modified and untracked files.
- Inspect the staged diff.
- Check secrets and restricted artifacts.
- Confirm only authorized paths are included.
- Run the full relevant tests.
- Check documentation consistency.

Commit to:

`codex/data-001-component-source-pilot`

Push to:

`origin`

Verify the remote commit SHA.

Do not merge into `main`.

If partially blocked, commit and push the independently useful verified results and the factual blocker report.

## 17. Rollback and reproducibility

No destructive repository operations are authorized.

Keep the previously verified R2 state unchanged.

A rollback must be possible by returning to the verified R2 predecessor commit or using an owner-approved revert of the task branch.

Do not rewrite or invalidate existing v1.0/v1.1 catalogs or snapshots.

The import demonstration must be reproducible from the exact recorded upstream commit, local source integrity checks and existing dependency environment.

## 18. Completion gate

DATA-001 is successful only if:

1. At least one authentic eligible LibrePCB structural record was identified and pinned.
2. Its applicable reuse rights were verified.
3. Its structure was extracted without inventing physical pads or mapping relationships.
4. A correctly scoped candidate catalog was generated or validated against the existing CORE-001A API.
5. The resistor's two physical contacts remained electrically separate without an ideal short.
6. Wiring changes produced independently expected net partitions.
7. Invalid, altered or ambiguous source data failed closed.
8. The source/evidence ledger permits exact reproduction.
9. All relevant existing regressions passed.
10. No unsupported engineering or commercial-use claim was introduced.
11. The result was committed and pushed to the correct task branch.

If any critical gate fails, report PARTIAL or BLOCKED precisely.

Do not expand the task into a general component importer, voltage simulator, GPIO checker or frontend.

### Final response to owner

Return:

- Actual execution outcome.
- Exact selected upstream source files and revisions.
- Whether genuine reusable data integration was achieved.
- What remained manually curated.
- What was not independently verified.
- Test results.
- Development-efficiency findings.
- The two Markdown report paths.
- Git commit SHA and remote branch.
- Concrete decision needed before broader catalog integration.

**Execute DATA-001 as one bounded, source-first engineering integration experiment.**

**END OF AUTHORIZED HANDOFF.**