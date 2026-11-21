INVENTOR EDU — Source-grounded UX readiness decision and one Codex implementation handoff
Date: 2026-11-21. Status: RESEARCH_ASSESSED / VISUAL_DESIGN_NOT_APPROVED / SINGLE_FUNCTIONAL_TASK_READY_FOR_OWNER_AUTHORIZATION.
1. Source assessment (not a new Codex audit)
Directly inspected the user-provided UX08-R2 ZIP (00–`10`, README), the prior UX03 and UX07 independent audit records, the v0.2 Screen Architecture plan, and live GitHub source at donluka-23/Inventor_EDU ref 771b45a6215fb32d8ba326ec9debe5c857adadcd.
Domain	Supported by research	Not supplied as approved build instruction
One canonical project and distinct Learn/Create presentation policies	UX08-R2 03, 04, 05; Screen Architecture v0.2	Unified client/backend mutation gateway or product-wide persistence
Entry and component discovery	UX03 original report + audit; UX08-R2 03	Accepted entry-route winner, final URL/screen layout, real Recent/`Saved` data
Canvas interaction	R2 verified code + UX02, UX08-R2 04	Exact variant board art and approved physical terminal binding to CORE
Rule-scoped inspection	UX04 + UX08-R2 04; UX08-T02A Rev 1.1 implemented	Source-qualified, fresh, integrated UI API and whole-circuit safety
Learn and assistant semantics	UX05/UX06 proposals, UX08-R2 05	Approved character design, reviewed Georgian learner-facing copy or production LLM action gateway
Visual system	UX07 visual study, UX07 audit, UX08-R2 06 D0–D6 process	A signed/owner-approved D4 design implementation contract: exact layout, token values, typography, movement, breakpoints and approved screenshot targets. Generated mocks explicitly rejected.


Assessment: The research adequately supports a small behavioral implementation and explicit negative cases. It does not support recreating a final highly polished Rodin-like visual UI without designer/owner-authored visual decisions. Codex must not fill that gap. The Rodin reference is a later owner-supplied interaction inspiration, not a frozen layout in these research reports. Architectural claims like no full safety, visual-only, one graph remain hard boundaries.
2. Frozen single-task handoff candidate
Task ID: UX-NAV-001A
Revision: 1.0
Name: SEMANTIC_COMPONENT_ENTRY_AND_ON_DEMAND_SHELF
Authorization: only after owner explicitly provides this exact handoff as the single Codex task.
Base: 771b45a6215fb32d8ba326ec9debe5c857adadcd (existing UX08-T02A continuation branch).
New task branch: codex/ux-nav-001a-semantic-component-entry.
Non-negotiable product output
Add a runnable, visually neutral, explicitly TEST_ONLY entry-to-component-shelf experiment to the existing React Flow browser program. It must let a person open the experiment, find a library-rendered component, place a single instance in the existing visual canvas, inspect/select a real renderer pin, add another supported part and visually connect two actual contacts. This is the first working user-entry interaction, not a designed production shell. No source-generated hardware artwork, no new style/theme/branding, no fabricated engineering data or saved-project promise.

Keep the legacy R2 canvas at the current / entry entirely usable and regression-compatible. Access the new experiment only through /?ux=entry. Do not alter routing infrastructure or add dependencies. This explicit experimental URL avoids making a visually unapproved shell the product default.
Exact source and supported asset set
Read the existing governance files required by AGENTS.md, the current UX08-T02A report and the v0.2 Screen Architecture plan, plus these existing files:
- prototypes/ds-002b/src/{main.tsx,Workspace.tsx,DeviceNode.tsx,model.ts,style.css};
- prototypes/ds-002b/tests/canvas.spec.ts;
- prototypes/ds-002b/package.json and prototypes/ds-002b/ASSET_AND_LICENSE_LEDGER.md.
Use only pinned, already present @wokwi/elements@1.9.2 renderers for sensor, led, resistor. They remain VISUAL_ONLY_NOT_ENGINEERING_VERIFIED; do not claim a specific retail revision or exact board identity. The already-present board nominal R2 art is not offered or rendered in /?ux=entry, because the owner rejected it; the legacy / route is preserved solely for historical tests. The experimental shelf must show an informational disabled ESP32-DevKitC-32E — ვიზუალი დაუმტკიცებელია entry with no Add action. No new asset/source or icon/package installation.
Exact visible semantic controls / behavior
The new experimental route has only these new controls, using semantic native HTML. Do not create a marketing landing page, a styled dashboard, fake projects, persona avatar, chat window, animation system, new palette, themed cards, tool icons or other navigation. Preserve the existing ReactFlow canvas implementation and its internal geometry/handle rendering.
1. On open, the visual experiment has an empty node set, with an accessible main heading INVENTOR EDU — ვიზუალური ექსპერიმენტი, a persistent qualification text VISUAL_ONLY_NOT_ENGINEERING_VERIFIED, a button კომპონენტის დამატება, and the existing canvas. Do not show the rejected nominal board.
2. კომპონენტის დამატება opens a native modal <dialog> titled კომპონენტების ბიბლიოთეკა with an input labeled ძებნა. Focus enters that input. Escape closes and focus returns to the opener. Closing must not change canvas, wires or selection.
3. List the four static candidates using the existing assets metadata. The three already-installed Wokwi renderers offer მოთავსება while not already present. Search is case-insensitive over the existing name/ID; empty result shows შედეგი ვერ მოიძებნა. Only exact known IDs are accepted; never admit arbitrary typed devices or a generated catalog.
4. Selecting მოთავსება for sensor, led or resistor adds the existing DeviceNode component to the ReactFlow layout at its already-declared initialPositions[device]; the device appears exactly once. It closes the dialog, leaves current other positions, wires, zoom and user selection intact, and returns focus to the opener. On reopening, an already-added item is non-addable and says უკვე დამატებულია.
5. The existing DeviceNode real Wokwi pinInfo validation and named contact pointer/keyboard flow must continue to work for newly added nodes. Users can add sensor + LED, choose sensor/TRIG then led/A, and create a visual-only wire. Existing move, pan, zoom and undo/redo wire behavior must work.
6. On this route, do not expose the legacy visual-only JSON import/export controls because that schema assumes a fixed four-node layout. Show neither Save nor Saved/Recent/Recover. No native CircuitSnapshot mutation, T02A fake bridge, GPIO result, assistant or lesson.
7. Selection-none, no added parts and no search results are distinct states. A failed renderer must fail closed: no usable pins on that part; the shelf continues to function for unaffected parts. No visual pin mapping may be treated as a reviewed canonical terminal binding.
8. Absolutely no new themed CSS. The only permitted additions to style.css are minimal structural rules needed to make the native dialog and existing canvas usable and focusable at 1440×900 and 1024×768. Reuse existing system font, CSS variables and native focus outlines; don't create a design system. Label screenshots SEMANTIC_EXPERIMENT_NOT_VISUAL_DESIGN.
Files allowed for writes (exact)
1. prototypes/ds-002b/src/main.tsx — exact URL switch only.
2. prototypes/ds-002b/src/Workspace.tsx — existing canvas with an opt-in ux=entry semantic mode, no rewrite of normal route.
3. prototypes/ds-002b/src/ComponentShelf.tsx — new native dialog with controlled search and supported items.
4. prototypes/ds-002b/src/style.css — only minimal structural layout/focus support described above.
5. prototypes/ds-002b/tests/entry-shelf.spec.ts — new Playwright acceptance tests.
6. prototypes/ds-002b/evidence/ux-nav-001a-entry-1440x900.png — real Chromium screenshot, with experiment qualification visible.
7. prototypes/ds-002b/evidence/ux-nav-001a-entry-1024x768.png — real Chromium screenshot, with experiment qualification visible.
8. tasks/UX-NAV-001A.md — exact handoff copied verbatim.
9. reports/UX-NAV-001A-REPORT.md — complete task report.
Forbidden: edit model.ts, DeviceNode.tsx, existing tests, catalogs, CORE, existing engineering interfaces, governance, ADRs, source or asset files, npm lock/manifest, dependencies, or the rejected existing board image. If the above cannot be implemented without a forbidden edit or architectural change, stop with OWNER_DECISION_REQUIRED and give the exact conflict. Do not expand the allowlist.
Must-pass acceptance tests
- UXN-01: / retains prior all-component canvas behavior and existing tests still run.
- UXN-02: /?ux=entry starts with zero components, qualified label, real canvas and one Add button; no board image/handles.
- UXN-03: Open dialog, focus input, filter by sensor/`HC-SR04`, no-results, Escape and focus return; no side effects on close.
- UXN-04: Add HC-SR04, then LED, one instance per candidate; Wokwi renderer is present and validated pins usable; attempted duplicate cannot add.
- UXN-05: sensor/TRIG→`led/A` creates only visual wire; wire changes with actual moving part and remains aligned at 0.5×, 1× and 2×; undo/redo work.
- UXN-06: Default board cannot be added in this new mode; no replaced/AI-generated image, no claims about exact 32E artwork.
- UXN-07: No Save/Recent, no enabled inspector electrical PASS, no unreviewed lesson/chat, no visual-only legacy JSON export on entry route.
- UXN-08: 1440×900 and 1024×768 screenshots from real Chromium, keyboard-only open/search/add/close, Escape and focus assertions, no runtime exceptions or off-origin network requests.
Commands from prototypes/ds-002b: npm run typecheck, npm run build, npm test, npm run test:e2e, git diff --check. Report exits, case counts, failures, environment and screenshots. Preserve the original Playwright suite and do not weaken tests to make the new mode pass. Keep the existing npm lock unchanged. Do not claim user experience superiority from Playwright alone.
Mandatory preflight, failure and publication
1. Verify remote origin, the exact base ref/SHA, ancestry, clean tracked working tree, and task branch absent. Do not silently choose main, rebase or merge.
2. Read mandatory governance/owner design authority rules, the task and listed source. Print BOOT BRIEF with base, nine-file allowlist, tests, and scope.
3. Implement the exact behavior. Do not infer a full design from UX01–08 research or use UX07/Figma-generated screenshots as visual reference. None is a signed D4 design implementation contract.
4. Write the complete reports/UX-NAV-001A-REPORT.md with acceptance table, real Chromium screen captures, regressions, negative/error cases, limitations and all actual code changes. Label visual experiment status, no canonical bridge and no artwork approval.
5. Stage only these nine paths, review full diff and secrets, commit/push the task branch and verify remote SHA per docs/SESSION_PROTOCOL.md. No merges. If blocked, publish a minimal truthful checkpoint only.
6. End with full Markdown report and branch/commit info. No next task, design choice or ADR is authorized.
Owner interpretation
A PASS proves only a small working interaction and the ability to reuse a third-party renderer inside the existing browser editor. It does not prove the final user experience, visual design, educational effect, engineered circuit accuracy, or a mature component catalog. Full styling waits for an owner/human-authored D4 contract; the experiment deliberately does not invite Codex to improvise it.