INVENTOR EDU — UX-NAV-001B Rev 1.1
Contextual Workspace: Test-Oracle Migration and Implementation Continuation
Status: FROZEN_HANDOFF_CANDIDATE / REQUIRES_EXPLICIT_OWNER_AUTHORIZATION
Task: Continue the same UX-NAV-001B task, not a new UX task or a new design exploration.
Authority: This amendment supersedes only the conflicting implementation/test lifecycle details of tasks/UX-NAV-001B.md Rev 1.0. Everything not explicitly amended remains binding. The original Rev 1.0 handoff is retained for provenance and read-only reference.
Repository: D:\Inventor_EDU · donluka-23/Inventor_EDU
Existing task branch: codex/ux-nav-001b-contextual-workspace
Required live branch HEAD at authorization preflight: 9ddcfa3dd31fb9e89d0f0903585f8c374c13720f
Ancestry: The branch descends from the original UX-NAV-001A baseline 561b33f8339c3f9985ba75667650e5c1cb4b4d77, and already contains the published UX-NAV-001B blocked checkpoint 0c7331a0a4b3bb90a92f2507b911a77433f65601.
Target route: /?ux=entry · Preserve: / legacy behavior and its unmodified tests/canvas.spec.ts.
A. Owner decision UXB-D01 — migrate superseded entry-route oracles
The existing prototypes/ds-002b/tests/entry-shelf.spec.ts is allowed to be edited only to migrate checks that assert obsolete Rev 1.0 UX-NAV-001A entry-route presentation, while preserving or strengthening every real behavioral/engineering invariant. tests/canvas.spec.ts MUST remain byte-identical. The original UX-NAV-001A tests are historical regression oracles for the old interface: they do not veto an explicitly authorized replacement of that very interface on the same route.

Conflict precedence: On /?ux=entry, the owner-authorized UX-NAV-001B Rev 1.0 contextual interaction contract takes precedence over obsolete UX-NAV-001A presentation expectations. The Rev 1.1 migration below replaces these expectations explicitly. For behavior unaffected by the replacement, preserve the old assertions or replace them with at least equally strict observations; do not delete entire tests or narrow coverage to make a failure disappear.
A1. Replace initial empty state assertions
In entry-shelf.spec.ts, the test formerly titled UXN-02, 06, 07 exact entry starts empty and keeps unsupported features absent:
- Preserve assertions for /?ux=entry route, heading, VISUAL_ONLY_NOT_ENGINEERING_VERIFIED, visible React Flow canvas, exactly one Add button, zero initial nodes/handles/board images, and absence of fabricated Save/Recent/Recover/Assistant/Lesson/PASS controls.
- Supersede the old კომპონენტები ჯერ არ არის დამატებული and კონტაქტი არ არის არჩეული visible assertions (the previous text lived in the permanent Inspector).
- Require exact visible დაიწყე კომპონენტის დამატებით when empty.
- Require no visible contextual Inspector before selection. Do not require that hidden DOM content be absent if the implementation uses semantically correct hidden/unmounted state.
- After one supported placement, require the empty prompt to disappear.
- Preserve the existing disabled ESP32 label and its inability to be placed.
A2. Replace the zero-button-in-empty-shelf assertion
In entry-shelf.spec.ts formerly UXN-03, preserve search-by-ID/name, case-insensitive matches, real no-results state (შედეგი ვერ მოიძებნა), non-placement of unknown typed items, Enter-no-creation, Escape dismissal, focus restoration, intact draft, selection, zoom, positions and wire state.

Replace the obsolete assertion shelf(page).getByRole('button') count zero with all of:
- No მოთავსება action exists for no matches;
- Exactly one available in-panel button labeled დახურვა remains;
- Clicking დახურვა closes only the shelf and returns focus appropriately;
- Escape closes the shelf even when type="search" has text, without canceling a canvas wire draft or changing selection/zoom/position.
Do not drop the negative-case assertion or treat the always-available close button as a placement action.
A3. Freeze the non-modal panel's accessible semantics
For /?ux=entry, implement the Component Shelf as an in-page, non-modal <section role="region" aria-labelledby="shelf-title"> with visible heading კომპონენტების ბიბლიოთეკა and a text-search control labeled ძებნა.
- Do not use showModal(), <dialog open> as a blocking modal, aria-modal="true", a full-screen backdrop, focus trapping, or global canvas inertness.
- Update the existing test helper from getByRole('dialog', { name: 'კომპონენტების ბიბლიოთეკა' }) to getByRole('region', { name: 'კომპონენტების ბიბლიოთეკა' }) in entry-shelf.spec.ts. Apply the same semantic locator to new contextual-workspace.spec.ts tests.
- The shelf may be conditionally mounted or correctly hidden. On open, focus enters the search; explicit close and Escape return focus to the opener; interactions outside the panel remain possible. No implicit collapse or dismissal is required upon outside clicks unless Rev 1.0 already specified it.
- The panel's visible close control is named exactly დახურვა; Georgian copy remains experimental and not human-reviewed production text.
A4. Preserve other UX-NAV-001A tests with semantic adaptations only
Retain coverage for:
1. Existing / and non-exact URL four-part legacy canvas, 46 physical handles and legacy visual JSON, with no Add button;
2. All supported Wokwi Elements (HC-SR04 / LED / resistor), one instance each; real pinInfo, registration, duplicate prevention and fixed positions;
3. Sensor sensor/TRIG → led/A real visual wiring, wire list, changes upon drag and pan, 0.5×/1×/2× geometry error < 2 CSS px, and Undo/Redo;
4. Corrupted pinInfo fails closed only for affected renderer, unaffected shelf still works;
5. Keyboard-only placement and wiring at both 1440×900 and 1024×768, no off-origin network requests, no errors and no rejected devkitc-v4 image fetch;
6. CANONICAL_MAPPING_UNAVAILABLE, distinct no-selection/no-findings cases, and prohibition on false electrical verdicts.
Adapt old .contact-readout, .draft, .wire-list visibility checks to reflect contextual Inspector open on relevant contact/wire selection, rather than demanding permanently visible Inspector content. Do not remove the underlying factual assertions or loosen the geometry bounds. Preserve keyboard focus continuity when a panel is open/closed. The old UXN-08 test still must perform the same real keyboard journey and capture its prior evidence in a throwaway test archive, not overwrite tracked historical screenshots in the repository.
A5. Explicit acceptance labeling
Document the migrated assertions as UX-NAV-001A_PREVIOUS_PRESENTATION_SUPERSEDED_BY_UXB_REV1_1. The seven historical UX-NAV-001A cases must still execute and pass for preserved behavior, with outdated UI assertions replaced by Rev 1.1 checks. No "12 original tests unchanged" claim is allowed: the correct claim is 5 unchanged legacy canvas cases + 7 migrated entry cases + new UXB cases, with exact actual counts recorded. The original task history and its former 12/12 result must not be rewritten.
B. Additional small clarification for Rev 1.0 layout
All Rev 1.0 requirements continue: contextual non-modal shelf on the left; canvas-dominant workspace; contextual Inspector in lower-right; 56 px header; precise shelf/Inspector dimensions and offsets; real Wokwi renderer and React Flow behavior; 120–160ms restrained transitions and prefers-reduced-motion; no approved final design claim; no additional icons/themes/frameworks/assets; old / unchanged.
- Rev 1.0's Inspect phrase is not authority to add a permanent global Inspector trigger. Implement the required selection-driven Inspector; any explicitly exposed inspect affordance must be limited to the selected object and must not invent a broader feature.
- For the revised route use .ux-entry as the CSS scope. The legacy / must be unaffected. Do not use the old screenshot as a visual target.
- After a contact/wire is selected, opening and closing the Inspector is presentation state only; it cannot change visual wiring or claim canonical CircuitSnapshot mutation.
- Do not invent any new device art or enable the ESP32.
C. Exact write allowlist — Rev 1.1
Only these 9 paths are writable:
1. prototypes/ds-002b/src/Workspace.tsx
2. prototypes/ds-002b/src/ComponentShelf.tsx
3. prototypes/ds-002b/src/style.css
4. prototypes/ds-002b/tests/contextual-workspace.spec.ts (new)
5. prototypes/ds-002b/tests/entry-shelf.spec.ts (newly authorized, constrained migration only)
6. prototypes/ds-002b/evidence/ux-nav-001b-workspace-1440x900.png (actual Chromium, new)
7. prototypes/ds-002b/evidence/ux-nav-001b-workspace-1024x768.png (actual Chromium, new)
8. tasks/UX-NAV-001B-REV1_1.md (new; copy this attachment verbatim, preserve Rev 1.0 task)
9. reports/UX-NAV-001B-REPORT.md (append Rev 1.1 continuation, preserve prior BLOCKED checkpoint chronology; update current outcome only with actual new evidence)
Read-only: tasks/UX-NAV-001B.md (Rev 1.0), prototypes/ds-002b/tests/canvas.spec.ts, src/main.tsx, src/model.ts, src/DeviceNode.tsx, all prior evidence screenshots, package files, lockfile, catalogs, CORE, T02A native projection, research, governance, docs/STATUS.md and tasks/NEXT.md. Preserve both pre-existing untracked research directories/files. No new dependency. No changes to main. No new branch.
D. Continuation, preflight and source alignment
1. Stay on existing codex/ux-nav-001b-contextual-workspace branch. Verify origin and the exact expected current remote HEAD 9ddcfa3dd31fb9e89d0f0903585f8c374c13720f. Confirm the ancestor 561b33f8339c3f9985ba75667650e5c1cb4b4d77. If the branch moved or the tracked worktree is dirty, STOP with BASELINE_DRIFT / OWNER_DECISION_REQUIRED. Do not rebase/reset/force-push, recreate the branch, or switch to another baseline.
2. Read required governance documents, the pre-existing Rev 1.0 task, prior Rev 1.0 BLOCKED report, this Rev 1.1 amendment, source and tests. BOOT BRIEF must state 9 writable paths and exact precedence of new UI over obsolete entry test oracles.
3. First migrate only affected test semantics per section A; do not delete entire tests or reduce retained assertions. Then implement the Rev 1.0 contextual workspace and run actual Chromium tests.
4. Testing in a temporary archive/copy is preferred because old entry-shelf.spec.ts writes legacy ux-nav-001a-entry-*.png screenshots. Those prior evidence files are not editable under this task. Keep normal runtime output (dist, test-results) outside tracked staging. Author new UXB screenshot evidence only at the two allowlisted new paths.
5. Run exactly documented verification: npm run typecheck, npm run build, npm test, npm run test:e2e, git diff --check. Verify all 5 unchanged legacy tests, all 7 migrated entry tests, and all added UXB tests. Record every real failure and rerun. Do not claim PASS from prior baseline runs.
6. Playwright assertions MUST test that /?ux=entry materially differs from the old route: no permanent Inspector column, no centered modal/backdrop, context panel geometry matches frozen dimensions, both panels overlay without shifting React Flow viewport, real wire alignment holds, keyboard/focus/reduced-motion and error states work. Capture and inspect real Chromium screenshots at 1440×900 and 1024×768.
7. Report each UXB-01..08 outcome, retain original blocked history, document migrated old assertions by line/behavior, exact test counts, screenshots, sources, changed files, SHA, and whether visual criteria are fulfilled. Do not mislabel experimental visual compliance as final owner UX acceptance.
8. Stage only the nine paths, review staged diff/secrets/rights, commit, push without rewriting history and verify remote. If genuinely blocked for another specific reason, commit an honest checkpoint and report, without unauthorized changes. Do not merge or begin another task.
E. Rev 1.1 success condition
The task is complete only if the existing UI on /?ux=entry is visibly replaced with the owner-specified contextual layout and preserved UX-NAV-001A behaviors, migrated tests, unchanged legacy tests, new UXB tests, and real screenshots pass. No full product-wide visual design is approved by this experimental contract. PASS is impossible if the task only modifies test expectations, leaves the old Inspector/modal unchanged, or suppresses assertions to make tests green.