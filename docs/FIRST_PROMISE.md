# First promise / engineering contract (candidate)

**Status: PROPOSED technical scope, validate exact part variants before implementation.**

## Reference lesson
A novice wires a specific ESP32 development board variant to a specific HC-SR04 module variant in a 2D workspace.

## Input
- Explicit board manufacturer, model and revision; exact GPIO/pad mapping.
- Explicit sensor manufacturer/model/revision; electrical input/output specifications.
- Circuit instances, pin IDs, electrical nets, and optional intermediary components.
- Operating conditions (power supply rail, logic level, resistor tolerances, intended signal direction).

## Expected output
- Editable 2D wiring topology with stable identity between visual handles and physical pins.
- Deterministic `PASS` / `FAIL` / `UNKNOWN` findings for **supported rules**, each with affected pin/net IDs and source metadata.
- Plain Georgian explanation, evidence link and correction suggestion **only if justified**.
- Changing a connection recomputes findings; stale warnings disappear, unknown states stay visible.

## Initial engineering questions
- Is output required where the selected GPIO is input-only?
- Does output signal exceed the receiving input's applicable electrical maximum?
- Is the required common-reference net present (as far as the documented topology establishes)?
- If a proposed resistor divider exists, is the relevant voltage under *stated* source/load/tolerance assumptions compliant? If load data is missing, label UNKNOWN.

## Acceptance rule
A passing test for a supported rule does not mean the whole circuit is safe or operational. Unknown variant, unspecified voltage conditions, missing datasheet or absent physical model must produce UNKNOWN, not PASS.

## First deliverable is NOT an app
The first milestone is an evidence-backed data-model fit report and a falsifiable contract. Only after approval should code, interaction design, and simulations proceed.
