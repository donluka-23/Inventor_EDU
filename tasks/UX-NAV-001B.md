# INVENTOR EDU — UX-NAV-001B Rev 1.0
## CONTEXTUAL_WORKSPACE_INTERACTION_IMPLEMENTATION

**Execution mode:** IMPLEMENT, TEST, CAPTURE, REPORT

**Authorization:** This message explicitly authorizes only UX-NAV-001B Rev 1.0. Do not begin another task.

**Repository:** `D:\Inventor_EDU`

**Required baseline branch:** `codex/ux-nav-001a-semantic-component-entry`

**Required baseline HEAD:** `561b33f8339c3f9985ba75667650e5c1cb4b4d77`

**New task branch:** `codex/ux-nav-001b-contextual-workspace`

**Target URL:** `http://127.0.0.1:<actual-vite-port>/?ux=entry`

---

## 1. Objective — What must visibly change

Transform the existing `/?ux=entry` experiment from a conventional toolbar + permanent Inspector + modal dialog interface into a **contextual, non-blocking, canvas-centered interaction workspace**.

The result must be immediately distinguishable from the existing interface in actual Chromium screenshots.

This is a bounded implementation of an owner-specified interaction layout, not an invitation to design a new product.

The desired interaction principle is continuous direct manipulation: the user discovers a component, places it, selects a physical contact, sees relevant context and continues working without leaving the canvas.

Hyper3D Rodin is a reference for interaction continuity and contextual disclosure only. Do not copy its proprietary visuals, styling, assets, layout measurements or animations.

**Required user journey:**

`Open workspace → Open component shelf → Search → Place component → Inspect terminal → Close inspection → Continue editing`

All steps must function in the same browser workspace without page navigation or canvas reset.

---

## 2. Mandatory preflight

Before editing:

1. Read `AGENTS.md`, `docs/DECISION_AUTHORITY.md`, `docs/SESSION_PROTOCOL.md`, the accepted ADRs and the relevant current task report.
2. Verify repository origin, branch, exact baseline HEAD, tracked working-tree state and the existence of the required source files.
3. Preserve the two existing untracked research locations:
   - `docs/RESEARCH_UX08_R2/`
   - `docs/research/raw/INVENTOR_EDU_SCREEN_ARCHITECTURE_PHASE_PLAN.md`
4. Read the existing `ComponentShelf.tsx`, `Workspace.tsx`, `main.tsx`, `DeviceNode.tsx`, `model.ts`, `style.css`, and Playwright tests.
5. Confirm that `/?ux=entry` already supports adding HC-SR04, LED and resistor and that `/` is the historical legacy route.

If baseline verification fails, stop with `BASELINE_DRIFT`. Do not silently rebase, merge, reset or select another branch.

---

## 3. Frozen visual and interaction contract

The following layout and behavior are explicitly specified for this experimental route. Do not replace them with an independently designed alternative.

### 3.1 Workspace structure

For `/?ux=entry` only:

- Keep one full-size React Flow canvas as the dominant surface.
- Remove the permanent right-hand Inspector column from this experimental layout.
- Use the available width for the canvas; contextual interfaces overlay it only while needed.
- Preserve current component artwork, physical handles, wires, pan, zoom and undo/redo.
- Keep a compact 56px workspace header.
- The header contains: product label, `კომპონენტის დამატება`, Undo, Redo and Fit view.
- Do not add dashboards, sidebar navigation, project cards, analytics panels or decorative widgets.
- Retain the visual-only and test-only qualification, but make it subordinate to the primary interaction.

Do not change the legacy `/` layout.

### 3.2 Component Shelf — replace native modal

Replace the experimental route's existing blocking `<dialog>` with a **non-modal contextual component panel**.

Its required structure:

- Anchored inside the workspace, 16px from the left edge and below the header.
- Width: 320px at 1440px viewport, maximum `calc(100vw - 32px)` on narrower screens.
- Maximum height: 70vh; overflow scrolls within the panel.
- The panel opens from the existing `კომპონენტის დამატება` button.
- It must not create a full-screen backdrop or block interactions outside its own boundaries.
- Keep the underlying canvas visible and interactive outside the panel.
- Provide an explicit Close button and Escape handling.
- Focus moves to the search field on opening and returns appropriately on closing.
- Search remains case-insensitive.
- Maintain the existing exact component identities and disabled ESP32 state.
- Existing instances remain non-addable.
- Choosing `მოთავსება` places the component once and closes the panel.

Use existing fonts, CSS variables and controls. Do not introduce new visual themes or dependencies.

### 3.3 Contextual Inspector — replace permanent sidebar

In the experimental route, the Inspector is initially hidden.

Open it when the user:

- selects a physical terminal;
- selects an existing visual wire; or
- explicitly activates an `Inspect` control.

Presentation:

- Floating contextual panel anchored to the lower-right canvas region.
- Width: 296px.
- Bottom offset: 58px.
- Right offset: 16px.
- Maximum height: 60vh, with internal scrolling.
- It must not resize the canvas or change the viewport transform.
- Its close action must not delete, change or deselect engineering objects unless existing behavior explicitly requires it.

Content must reuse existing real information:

- selected visual terminal or wire ID;
- visual pin availability;
- `CANONICAL_MAPPING_UNAVAILABLE`;
- relevant existing wire actions.

Do not display fabricated electrical verdicts, sources, voltage measurements or manufacturing facts.

Preserve the existing terminal locator and accessible keyboard path.

### 3.4 Empty state and progressive disclosure

When no components are present:

- Canvas remains visible.
- Show a concise instruction: `დაიწყე კომპონენტის დამატებით`.
- Provide the existing component-add action.
- Do not show an empty permanent Inspector.
- Do not invent recent projects, tutorials, suggested AI projects or completion indicators.

After the first component is placed:

- Remove the empty-state instruction.
- Keep the component visible at its existing declared initial position.
- Preserve pan, zoom and any existing layout state.
- Avoid automatically opening unrelated panels.

### 3.5 Motion and interaction feedback

Use only restrained functional transitions:

- Contextual panel opening/closing: 120–160ms.
- Animate only opacity and a small position offset where appropriate.
- No bounce, decorative movement, parallax or large screen transitions.
- Respect `prefers-reduced-motion: reduce`.
- Avoid layout shifts when panels open and close.
- Never animate physical contact coordinates independently of React Flow geometry.

These transitions are presentation-only and must not change canonical or visual wiring data.

---

## 4. Engineering authority — non-negotiable

This task changes UI presentation and local interaction only.

Do not alter:

- `CircuitSnapshot`;
- canonical `TerminalRef`;
- `TopologyResult`;
- GPIO verification or coverage semantics;
- `UX08-T02A` projection behavior;
- component catalog facts;
- electrical rules or source evidence;
- device artwork or licensing metadata.

Continue using existing `@wokwi/elements@1.9.2` and `@xyflow/react@12.10.0`.

The supported component set remains HC-SR04, LED and resistor, one instance of each.

The ESP32 item remains unavailable in the experimental shelf because its exact artwork has not been approved.

Do not generate new device illustrations.

Do not build the assistant, chat system, Learn lessons, persistence or backend integration during this task.

---

## 5. Exact write allowlist

You may modify or create only:

1. `prototypes/ds-002b/src/Workspace.tsx`
2. `prototypes/ds-002b/src/ComponentShelf.tsx`
3. `prototypes/ds-002b/src/style.css`
4. `prototypes/ds-002b/tests/contextual-workspace.spec.ts`
5. `prototypes/ds-002b/evidence/ux-nav-001b-workspace-1440x900.png`
6. `prototypes/ds-002b/evidence/ux-nav-001b-workspace-1024x768.png`
7. `tasks/UX-NAV-001B.md`
8. `reports/UX-NAV-001B-REPORT.md`

All new experimental CSS must be scoped to `.ux-entry` so the legacy route remains visually unaffected.

Do not modify `model.ts`, `DeviceNode.tsx`, `main.tsx`, existing tests, dependencies, package-lock, source assets, engineering modules, ADRs or governance files.

If a required behavior genuinely cannot be implemented within this scope, return `OWNER_DECISION_REQUIRED` with the exact conflict. Do not silently expand the allowlist.

---

## 6. Required interaction tests

Create real Playwright tests covering:

**UXB-01 — Visual structure**
- No permanent Inspector column on `/?ux=entry`.
- Canvas occupies the underlying workspace width.
- Contextual panels overlay rather than resize the canvas.
- Legacy `/` retains its original structure.

**UXB-02 — Component discovery**
- Add button opens a non-modal panel.
- Focus enters search.
- Search filters supported items.
- Outside-panel canvas interaction is not blocked by a backdrop.
- Escape closes the panel and restores focus.

**UXB-03 — Component placement**
- Place HC-SR04.
- Reopen shelf.
- Place LED.
- Both real Wokwi renderers appear.
- Duplicate placement is blocked.
- Existing node positions, wire state and zoom survive shelf use.

**UXB-04 — Contextual inspection**
- No Inspector initially.
- Selecting `sensor/TRIG` opens the Inspector.
- Inspector displays the real visual terminal identity.
- Closing Inspector does not mutate any wire.
- Keyboard access and focus remain usable.

**UXB-05 — Wiring continuity**
- Connect `sensor/TRIG` to `led/A`.
- Move LED.
- Wire endpoint remains aligned with the real terminal.
- Verify at 0.5×, 1× and 2×.
- Existing undo/redo works.

**UXB-06 — Negative states**
- Unavailable ESP32 cannot be added.
- Missing renderer pin geometry fails closed.
- Invalid search gives an empty result.
- No fabricated engineering PASS or voltage verdict.
- No fake save, assistant or lesson state.

**UXB-07 — Motion/accessibility**
- `prefers-reduced-motion` is respected.
- No page-level horizontal overflow at 1024×768.
- Dialog/modal backdrop is absent.
- Focus indicators and keyboard closing behavior work.

**UXB-08 — Regression**
- Existing unit, build and legacy Playwright suites pass unchanged.
- No off-origin requests.
- No browser runtime exceptions.
- No unauthorized source files changed.

---

## 7. Visual acceptance is mandatory

Run the actual browser implementation.

At minimum capture:

**1440×900:** HC-SR04 and LED placed, their visual wire connected, contextual Inspector open, no permanent sidebar.

**1024×768:** Component Shelf open, with existing components identified and the resistor still available, canvas visible behind and alongside the panel.

Before accepting the result:

1. Inspect both screenshots.
2. Confirm the old permanent Inspector layout is absent from the experimental route.
3. Confirm the shelf is not a centered blocking native dialog.
4. Confirm both interactive panels match the specified dimensions and positions.
5. Confirm the underlying canvas is still usable.
6. Confirm Georgian labels remain legible without clipping.
7. Check actual behavior, not just screenshots.

If these conditions are not met, correct the implementation within the approved scope and rerun tests.

Do not mark a visual acceptance criterion PASS solely because TypeScript, Vite or Playwright functional tests pass.

Screenshots must be actual Chromium output, not AI-generated or hand-composited images.

---

## 8. Required execution commands

Run from `prototypes/ds-002b`:

- `npm run typecheck`
- `npm run build`
- `npm test`
- `npm run test:e2e`

Run `git diff --check` and inspect the complete staged diff.

Record the actual outputs. Never weaken existing tests to make the task pass.

---

## 9. Completion and reporting

Write a complete `reports/UX-NAV-001B-REPORT.md` containing:

- exact baseline and task branch;
- full file manifest;
- implemented behavior;
- visual changes compared with `UX-NAV-001A`;
- acceptance ID-by-ID PASS/FAIL/BLOCKED;
- real test commands and outcomes;
- screenshot references;
- browser interaction findings;
- limitations and unresolved decisions;
- implementation commit and verified remote SHA.

Commit and push only the authorized task branch.

Do not merge into `main`, change architectural decisions or start another task.

**Success means the browser visibly and functionally implements the specified new contextual interaction layout — not merely that an additional button or modal works.**

If successful, return `FUNCTIONAL_AND_EXPERIMENTAL_VISUAL_CONTRACT_PASS`.

Do not claim the entire INVENTOR EDU application or its final visual design has been accepted.