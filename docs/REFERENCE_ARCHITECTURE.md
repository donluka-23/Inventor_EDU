# Authority note
Research reference only: this is not an accepted implementation design. Codex must not select modules or realize the diagram without a separately authorized task plan.

# Reference architecture — provisional boundaries

**Status: REFERENCE ONLY — implementation is not approved.**

```
2D editor (rendering, selections, learner actions)
      ⇅ stable component / terminal / net IDs
Canonical circuit topology (instances, terminals, nets, board pad mapping)
      + Component facts (versions, operating domains, provenance)
      → rule evaluator / optional physics adapter
      → typed findings (PASS | FAIL | UNKNOWN | NOT_APPLICABLE)
      → localised explanation + highlighted UI elements
```

## Required separation of concerns
1. **Presentation:** positions, rotation, path routing, SVG/canvas geometry, accessibility, interaction state.
2. **Connectivity:** electrical equivalence classes (nets), instances and terminal IDs; not merely individual drawn line pairs.
3. **Part metadata:** component, device, package/pad mapping and actual board revision; supported operating modes; sourced facts with units and bounds.
4. **Analysis:** domain-limited rules and calculations operating on the canonical model; no visual-coordinate interpretation.
5. **Evidence:** source and model revision, assumptions, computation trace and failure/unknown status.
6. **Education:** Georgian corrective text derived from typed findings, with novice-friendly explanations.

## Interface boundaries (candidate, not committed schema)
- `parse_editor_action → circuit_state`
- `evaluate(circuit_state, catalog_snapshot, conditions) → findings[]`
- `render(circuit_state, findings) → UI`
- Any future `simulate` adapter is **optional** and must explicitly declare supported component models, conditions and numerical accuracy.

## Design questions requiring experiments
How represent split signals, ERC rules, physical board headers vs MCU pads, multiple sensor variants, analog intermediate parts, and non-ideal sources? Compare existing open data semantics in `docs/MODEL_SELECTION.md` before accepting persistent schemas.

## Prohibited shortcuts
Do not encode physical facts only in frontend components; do not treat "drawn line = validated circuit"; no AI-inferred pin ratings without sources; no server architecture chosen without evidence of deployment needs.
