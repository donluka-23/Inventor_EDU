# Authority note
Only the owner/architecture conversation may approve OSS intake; Codex verifies pre-approved entries and stops if rights differ.

# Open-source and third-party material intake — blocking policy

**Status: ACCEPTED governance. Product release license: UNDECIDED.**

## Separate five artifact classes
1. Source code/library/runtime dependency.
2. Official component library or symbol/footprint data.
3. Semiconductor/board manufacturer numeric facts and docs.
4. Device simulation models (SPICE, firmware, binary).
5. UI icons, images, teaching illustrations, translations.

Each class has separate copyright, trademark, attribution, modification and redistribution questions. Free download ≠ open-source license ≠ right to rehost/redistribute.

## Mandatory hard gates BEFORE adoption
- Exact upstream owner, version/commit, primary URL, artifact type, official SPDX/license text, obligations and subdependency implications documented.
- Compatibility with intended distribution (web SaaS, possible self-hosted/mobile), modifications, source disclosure, attributions and data reuse. GPL/AGPL/CC-BY-SA/proprietary/NC/unknown require explicit separate legal review; do not assume prohibited or automatically compatible.
- Security and maintenance assessment, source integrity, update plan and model correctness or testing relevance.
- A named feature requirement and baseline showing why dependency is needed.
- No compliance gate can be overridden by weighted score.

## Weighted technical fit AFTER hard gates
Correctness/model fitness 35%; task coverage 25%; API/interoperability 15%; maintainability/security 15%; implementation burden 10%. A score is a screening aid, not proof.

## Decision states
`CANDIDATE`, `REVIEW`, `APPROVED`, `REJECTED`, `REPLACE` — record in `governance/OSS_REGISTER.csv` with date and reviewer. CANDIDATE does not authorize install, copy, import or redistribution.

## File-level provenance and SBOM
When source code is created or imported, adopt SPDX identifiers and REUSE conventions where applicable, generate a dependency inventory/SBOM for actual releases, preserve notice files and license texts. Record exact model/variant/version for any component data. Do not commit vendor PDFs or diagrams by default; store links and properly attributed extracted facts in a reviewed structured format.

## Product license
Do not write a `LICENSE` file selecting a distribution model without an explicit decision. Internal prototype code is not automatically licensed for third-party reuse. Seek legal review before commercial distribution involving copyleft, redistributed CAD libraries or vendor assets.

References: https://spdx.org/licenses/ ; https://reuse.software/spec/ ; https://spdx.dev/about/overview/
