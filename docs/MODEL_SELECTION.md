# Data model selection research protocol

**Status: OPEN — next experiment**

## Candidate semantics to compare
1. **KiCad:** pin/net connectivity, symbols, netlist, ERC and CLI export. Its ERC does not itself certify arbitrary component physical behaviour.
2. **LibrePCB:** component electrical signals, symbols, device-to-package mapping, exact part and visual representation separation.
3. **SPICE:** node/component constitutive behaviour with appropriate models, distinct from visual wiring and firmware.

## Evaluation cases
A. One controller rail feeding two sensors: multiple visual edges form a single net.
B. Input-only GPIO attached to an input requiring trigger generation: a logical function conflict.
C. Standard 5 V signal into a specified 3.3 V-limited input: distinguish actual relevant voltage domains and maximum from nominal data.
D. Add a two-resistor voltage divider: compute output with explicit assumptions; flag unknown with missing load/tolerance values.
E. Identical named controller models with different header or silicon revisions: stable identity and version isolation.

## Evaluation columns
| Criterion | Required evidence |
| --- | --- |
| Net semantics | Source format and example round trip |
| Logical pin function | Rule and required board-specific facts |
| Electrical bounds | Units, source, operating conditions and validity |
| Visual-to-electrical mapping | Identity stability under UI rearrangement |
| Cross-model integration | Loss analysis at import/export boundaries |
| Licensing | Code, library data, icons and vendor models separately |
| Unknown behaviour | Example of rejected or undecidable input |

## Decision rule
Choose the smallest representation that supports all critical first-lesson cases with inspectable derivations and no silent loss of identity or constraints. Prefer reuse/interoperability over implementing a broad custom standard. If no candidate fully fits, document the **minimal** adapter or extension and its loss tests.

## Resources
- https://docs.kicad.org/10.0/en/eeschema/eeschema.html
- https://docs.kicad.org/master/en/cli/cli.html
- https://librepcb.org/docs/quickstart/create-library-elements/component/
- https://librepcb.org/docs/quickstart/create-project/schematics/
- https://librepcb.org/license/
