# SYN-001 headless synthesis contract

The version 1.0 request covers a two-device test fixture with `TRIG_OUTPUT/GPIO_OUT` and `ECHO_INPUT/GPIO_IN`. The caller supplies exact component instances, sensor terminal references and finite domains of physical controller contacts. `SignalRole.requirement_id` links the role to its originating requirement. `SynthesisRequest.requirements_digest` preserves the caller's upstream requirements digest. Upstream serialization and the semantic review of the role bindings and domains remain with the fixture owner.

## Execution

Call `inventor_edu.synthesis.generate_candidates(request, catalog, fact_set, *, trusted_catalog_sha256, trusted_factset_sha256)`. Request and output records are strict and immutable. The caller supplies expected pins from an independent test authority. The evidence scope must match the supplied fact set's reviewed or synthetic test scope. Wrong pins raise the existing CORE-001B errors and absent pins leave applicable findings `UNKNOWN`. Invalid record fields raise Pydantic validation errors. Invalid catalog, component and terminal references use CORE errors, with `SynthesisInputError` for mismatched request catalog, evidence scope, role bindings or malformed domain structure.

Roles are ordered by role ID and domains by exact instance and terminal ID. Each attempted terminal consumes one search node, including any attempt pruned by the declared `AllDifferent` constraint. CORE-001A constructs each complete assignment and computes its topology. CORE-001B receives the full GPIO check scope at `ACTIVE`. Verifier calls count one per evaluated assignment, or one empty-request call to validate trust and catalog binding when no assignment is evaluated. Validation and per-assignment work are outside the node count. The candidate cap retains the first results in traversal order and leaves traversal and evaluation totals intact.

`EXHAUSTED_REVIEWED_DOMAIN` covers a fully visited finite search. `SEARCH_INCOMPLETE` covers an unvisited branch after the node limit. `NO_REVIEWED_DOMAIN` covers an empty role domain. Counts describe this run and its supplied domains.

## Result and replay

Each retained candidate contains the exact snapshot, real topology and unchanged GPIO report. A hard failure in pin mapping, physical capability or board availability rejects the candidate. Positive findings for every one of those checks on both roles yield `SCOPED_CHECKS_PASSED_WITH_OBLIGATIONS`. Other assignments are `INCOMPLETE_WITH_EXPLICIT_OBLIGATIONS`. The role traces preserve CORE net IDs, immutable source and assigned terminal references, separate finding and coverage IDs, source claim IDs, missing prerequisites, evidence scope, versions and digests. Power, LED, current-limiting resistors, voltage adaptation and firmware remain obligations.

With the project's pinned environment, run from the repository root:

```powershell
python -B -m tests.test_syn001_generation
```

This prints two JSON records with exact input, snapshots, topology, GPIO results and traces. The first run enumerates three Trig contacts and holds Echo at `J3.8`. The second restricts Trig to `J3.9` and runs its single assignment again, preserving the canonical snapshot and finding IDs for that assignment. Every output remains `TEST_ONLY_NOT_PRODUCTION`.
