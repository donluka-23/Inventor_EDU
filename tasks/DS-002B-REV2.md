INVENTOR EDU — DS-002B / REVISION 2
Exact DevKitC V4 Component Canvas — Library-Based Implementation and Evidence-Qualified Pin Interaction
Owner decision: AUTHORIZED SINGLE CODEX TASK. This REVISION 2 supersedes the earlier DS-002B Rev 1 handoff. Do not implement both.
Project: donluka-23/Inventor_EDU
Baseline: origin/codex/edu-t1-independent-transfer @ 4e6daa0b60937e5863bb754b9293a6504174bb5a (revalidate live Git before acting).
New branch: codex/ds-002b-exact-component-canvas-r2
Status: owner-frozen implementation experiment; not production authorization or full app UI authorization.
Primary objective: A high-quality, usable, runnable, locally hosted electronics canvas with real, previously developed, reusable component graphics, interactive individual pins, wire lifecycle, and truthful board identity. It must include the documented ESP32-DevKitC V4 with ESP32-WROOM-32E and HC-SR04; LED and resistor are additional usable components. Do not default to an ESP32 DevKit V1 pretending to be the approved board.
0 — Mission and non-negotiable product outcome
The owner rejects previous AI-illustrated electronics and generic dashboard UI. The deliverable is not a prettier screenshot. It is a functional, device-faithful circuit-workspace foundation whose pin interaction quality is seriously comparable to the relevant portion of Wokwi. Use existing, professionally made renderer assets rather than AI-generated vector replacements.

On a single full-viewport workspace a user can:
1. Identify a realistic, correctly named ESP32-DevKitC V4 and HC-SR04 module; also display a real library LED and resistor.
2. Find both physical header rows on the DevKitC V4; zoom; hover/focus and select a particular physical terminal, not just a GPIO number.
3. Start a wire at sensor/TRIG, select the reviewed board physical terminal board/J2.5, see the actual wire, rewire to board/J3.9, and inspect the exact chosen visual endpoints. Other board terminals must be present as distinct interactive anchors, even if not yet covered by engineering facts.
4. Move either component and pan/zoom the canvas; existing wire endpoints stay attached to the rendered physical contacts, not their old screen coordinates.
5. Cancel a draft, delete a wire, undo and redo, navigate pins without a mouse, and export deterministic visual-only connection data.
6. Recognize the strict absence of full electrical/firmware simulation. There must be no invented PASS, SAFE, voltage verdict, GPIO capability verdict, or fabricated canonical proof.
Task output must feel like an electronics editor, not a flowchart or an LLM-designed dashboard. Wokwi's identical visual style is not mandatory; real device fidelity and actual pin interaction are mandatory. Judge with live screenshot, not prose.
Explicit owner scope resolution
- No artificial DevKit V1 limit. Target the actual V4 fixture first; preserve distinct hardware variants, no aliasing by matching printed labels.
- No limit to only five hardcoded GPIOs. Render, enumerate and individually address all 38 visual V4 header contacts if the board's reviewed layout supports them. Only reviewed terminals may obtain canonical engineering links; everything else is visually selectable but clearly ENGINEERING_COVERAGE_UNKNOWN until checked.
- No ban on legitimate off-the-shelf assets. Any traceable, clearly permissive board asset can be used, subject to exact variant alignment. Do not unnecessarily reject a technically and legally usable alternative simply because it was not named here.
- No artificial UI framework selection. React Flow is the strong default, but report measured unsuitability and request an owner choice before replacing a framework. Do not build a second unreviewed editor engine silently.
- No unrelated application scope. Sidebar system, chat, project gallery, Learn/Create modes, quiz architecture and user management are separate tasks, not added by loosening the visual component limitation.
1 — Preflight and authoritative evidence
1. Fetch https://github.com/donluka-23/Inventor_EDU.git, read AGENTS.md, governance, docs/prototype/MASTER_PLAN.md (known v1.7 at base), docs/STATUS.md, the frozen DS-002B instructions, Research G, CORE catalog/mappings, relevant tests, and current acceptance reports. Confirm expected baseline HEAD / working tree / permitted locations; log any discrepancy. Never infer main reflects current work.
2. Treat existing canonical semantics as immutable: exact DeviceDefinition, physical TerminalRef, CircuitSnapshot, catalog digest, GpioFinding vs GpioCoverage, B source pins, CAP/SYN and all existing Python verifiers.
3. Audit the exact physical hardware: Espressif ESP32-DevKitC V4 documentation for J2/J3 connector numbering, WROOM-32E variant, power/flash/strap notes. Use existing reviewed catalog for the canonical board/Jx.y associations. A rendered GPIO18 silkscreen is not enough for a J3.9 claim; both header row and numbered position must align with approved data.
4. Source-identity ledger must retain visual asset ID → graphical pin ID → verified physical header location → canonical TerminalRef (if proven). Distinguish VISUAL_MATCHED, VISUAL_UNRESOLVED, CANONICAL_MAPPING_REVIEWED, CANONICAL_MAPPING_UNAVAILABLE. Source approval cannot be generated by the UI.
5. Confirm no active overlapping DS-002B or VIS-001 task branch changes before proceeding. On an unexpected concurrent branch, stop and ask for owner reconciliation, not an invisible merge.
2 — Technology sources and asset acquisition order
A. Ready-to-use licensed component renderers
Required default: @wokwi/elements (Wokwi Elements, MIT license) for HC-SR04, LED, resistor. Inspect the actual installed package, its transitive dependencies and component pinInfo. The exported ESP32 Devkit V1 renderer is useful as a clearly labeled control/reference, not a surrogate for V4.

Sources and exact inspected upstream reference:
- https://github.com/wokwi/wokwi-elements @ 5178c0cc1b455719fdf562169293797e29d73dac (read LICENSE, src/hc-sr04-element.ts, src/led-element.ts, src/resistor-element.ts, src/pin.ts). Record exact npm version, dist integrity and actual package license.
- @xyflow/react / React Flow, MIT: https://reactflow.dev/learn/customization/handles. Multiple named handles, sourceHandle/targetHandle, ConnectionMode.Loose, custom handles, dynamic reposition (useUpdateNodeInternals). Record installed version.
- React + TypeScript + Vite for this isolated single-page workspace. Playwright for actual Chromium screenshots, mouse/keyboard tests, viewport calibration and regression.
B. Exact V4 visual asset — mandatory acquisition work, not an invented SVG
Evaluate at least the following distinct options in a reproducible asset review. Select the highest-fidelity legally usable V4 representation with a matching 38-pin header overlay:
1. Existing official-compatible CC0 model candidate: https://www.innerscene.com/tools/library/3d-parts/esp32-devkitc-v4-layout-1ab70892. The page states CC0, provides a STEP model, and describes 38 pins. It also explicitly states that some geometry and details are representative, with nominal pitches/spacing, not guaranteed mechanical accuracy. It is a visual candidate only, never source authority for header numbering, PCB revision, electrical limits or manufacturing geometry. Using an orthographic exported image/raster or browser-rendered model derived from verified CC0 material is permitted and is not AI art generation. Evaluate performance, fidelity and whether actual per-pin anchors can be reconciled with the documented V4.
2. Alternative properly licensed V4 asset: search established asset repositories (CC0, MIT, or compatible licensed graphics/3D) and record the exact original file, author, terms, revision, integrity hash, pin coverage and reproduction/derivative permission. Prior FreeSVG ESP32 DevKitC was noted as a CC0 candidate but needs identity and live URL verification; do not assume it is an exact V4 pin image.
3. Wokwi's already-published V4 reference: https://github.com/wokwi/wokwi-boards/tree/main/boards/esp32-devkit-c-v4 contains board.svg and board.json (current checked ref 962b19d5636756537a93bb5337ac99abd775eae0). The JSON lists 38 pins and visual x/y geometry. Use them for inspection and comparison. This repository has no repository-wide LICENSE detected. Establish rights for those exact files before embedding, modifying or distributing them. A library being MIT does not automatically MIT-license a separate repository; public GitHub visibility alone does not license reuse. This is an asset-specific issue, not permission for Codex to stop all implementation. If a valid explicit license, permission or alternative provenance is established, use the exact asset. Record evidence. Do not fake permission. Relevant GitHub policy: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository.
4. Official manufacturer geometry/pin labels: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html. Official J2/J3 pin tables, board revision and dimensions are technical evidence; do not assume that published manufacturer art or DXF grants unlimited copyright permissions. Derive machine-readable factual coordinate/terminal mappings from independently verified technical facts, never from a screenshot pixel guess. If exact external render material is not licensed, use a lawful independently licensed/CC0 V4 visualization as the shell and augment the interactive pin hit-map from verified technical information.
Geometry pitfall that must be checked: The CC0 3D-model page describes an overall length of about 49.5 mm and nominal pitch details, while the published Wokwi V4 board JSON describes 27.9 × 56.628 units and 2.54-mm row increments. These are not safely interchangeable. Do not simply scale one source's pin coordinates onto another source's image and call it precise. The authoritative physical header positions/row ordering must be reconciled with documented physical hardware. If they cannot be, mark V4 asset fit as PARTIAL and do not issue a false pin-alignment PASS.

Asset selection priorities: legal reuse; correct physical board identity; real pin hit-map; fidelity; browser performance; sustainable integration/maintenance. Prefer a verified existing library asset over drawing a board yourself. No generated substitute ESP32 artwork, fake photorealistic board, or mismatched V1-as-V4 fallback.
C. Technical and engineering independence
- Do not integrate the Wokwi proprietary simulator, hosted editor, runtime APIs, community projects or paid SDKs into the application.
- Do not use an AI-image tool for hardware artwork. Ordinary deterministic conversion/rendering of an appropriately licensed CAD/3D asset is allowed.
- Keep a standalone ASSET_AND_LICENSE_LEDGER.md for every graphical asset and every dependency. Retain required notices and redistribution conditions. Licenses apply per actual file/source, not per brand.
- Work should continue on all unaffected components while a specific asset license is being checked. Only the unapproved artwork is excluded from distribution, not the entire canvas or tests.
3 — Architecture: off-the-shelf canvas + device adapter + truth firewall
Application directory: prototypes/ds-002b/ inside the existing repository. Isolated npm project; does not overwrite the user's already-running prototypes/ds-002/ or other Vite scaffolds. npm ci, npm run dev -- --host 127.0.0.1, npm run build, npm run test, npm run test:e2e must be documented and runnable.

Recommended layered design:
React Flow viewport + custom device nodes + edges
             |
     DeviceVisualAdapter
     (Wokwi Elements or licensed V4 geometry)
             |
  VisualPinRegistry: per instance, every pin
             |
  Stable visual terminal reference (nodeId, visualPinId)
             |
  ExactMappingProjection (read-only explicit table)
             |
  Existing canonical TerminalRef (ONLY when independently proven)
For this task, the backend is not a write target. ExactMappingProjection is a small, audited, read-only visual-to-canonical adapter for reviewed fixture pins only, with nonmatching pins left unqualified. It is not a new engineering ontology or a substitute for B's fact set. Visual connection export is explicitly separate from canonical Conductor creation.

Example TypeScript contracts; adapt naming if required by existing repository conventions:
type PinMappingStatus = 'CANONICAL_MAPPING_REVIEWED' | 'CANONICAL_MAPPING_UNAVAILABLE';
interface DeviceVisualSpec {
  visualAssetId: string; assetSha256: string; provenanceId: string;
  deviceVariant: string; visualWidth: number; visualHeight: number;
  pinList: readonly VisualPinSpec[];
}
interface VisualPinSpec {
  visualPinId: string; displayLabel: string;
  localAnchor: { x: number; y: number; coordinateSystem: string };
  mappingStatus: PinMappingStatus;
  canonicalTerminal?: { instanceId: string; terminalId: string; catalogDigest: string };
}
interface VisualWire {
  edgeId: string;
  a: { instanceId: string; visualPinId: string };
  b: { instanceId: string; visualPinId: string };
}
interface VisualWorkspaceExport {
  schemaVersion: '1.0'; qualification: 'VISUAL_ONLY_NOT_ENGINEERING_VERIFIED';
  nodes: unknown[]; wires: VisualWire[]; visualAssetRevisions: string[];
}
Design invariant: CSS/viewport coordinates never grant a pin an electrical identity. Canonical binding is a separate exact key from reviewed records, pinned to catalog/board/asset revision; if uncertain, explicit UNAVAILABLE. Every supported visual terminal may be selected even if its engineering mapping is unknown, but UI must never falsely assert its capabilities.
The 38 pins and the 4 HC-SR04 pins
- V4: two actual header rows, correct J2/J3 order and explicit physical contact numbering. All 38 have individually distinguishable interactive controls and unique stable names. These controls are not necessarily all electrical-verification capable.
- HC-SR04: VCC, TRIG, ECHO, GND all hoverable/focusable, visually anchored; do not treat a visual color label as proof of voltage.
- LED: anode/cathode; resistor: both ends. Detect element-supplied pinInfo and any dynamic update from properties; do not fabricate another coordinate table when the library already provides one.
- Confirm that the visual board actually corresponds to the reviewed exact hardware revision, not just a similar pin count.
4 — Pin geometry and React Flow implementation contract
1. Register and mount actual @wokwi/elements Web Components as React custom-element nodes. Take pinInfo from the mounted element's actual runtime API. Be careful with Shadow DOM and component sizing.
2. For each visual V4 pin, use the selected asset's documented coordinate system and measured DOM bounds, pinned to its asset revision. If the V4 renderer is a licensed orthographic visual, attach React Flow handles as a separate deterministic overlay. Never derive a pin's identity from the current screenshot pixel color or OCR.
3. Browser coordinate transformation must explicitly account for asset intrinsic units, CSS scale, device pixel ratio, getBoundingClientRect, pan, zoom, scroll and any rotation. Use ResizeObserver/`useUpdateNodeInternals` or equivalent for dynamic handles, and cancel stale handles on asset/variant changes.
4. All interactive handles have stable unique IDs. sourceHandle and targetHandle must identify the actual visual pin. Use ConnectionMode.Loose if needed so electronics terminals can connect in either direction.
5. Selected/focused pins show unambiguous halo/label. Enlarge pointer hit target without visually moving the electrical connection anchor; for dense headers, offer zoom-on-focus and a keyboard pin list as fallback.
6. Do not use styling or a CSS pseudo-element as a second untracked electrical pin. For each visual handle one stable VisualPinSpec, and vice versa. No overlapping click maps that silently pick neighboring pins.
7. Use real library visuals without generic card frames around every part. Keep a neutral, instrumentation-like canvas, a small connection-debug strip, and scoped notices. Do not implement any application-wide product shell.
Wire lifecycle
IDLE → DRAFT(start visual pin) → COMMIT(end visual pin) → SELECT/REWIRE/DELETE; ESC cancels; UNDO/REDO restores exact recorded endpoints. A draft produces no committed edge. Duplicate/self-connection policy explicitly documented and enforced; never create an invalid phantom edge or a new electrical net from visual-only coordinates. Drag/zoom/pan change geometry, not endpoint IDs. Preserve identity across node moves, React state updates and reload from deterministic visual export.
UI semantics (not yet engineering assertions)
Use text labels, exact terminal IDs when reviewed, and the following separate statuses:
- VISUAL_PIN_AVAILABLE — physically selectable in renderer.
- CANONICAL_MAPPING_REVIEWED — matched to the exact reviewed fixture terminal and catalog digest.
- CANONICAL_MAPPING_UNAVAILABLE — exact source/pin proof absent.
- NOT_ENGINEERING_VERIFIED — all edited visual wires, until a separately authorized CORE integration.
No frontend PASS, FAIL, UNKNOWN claims may masquerade as Python verifier findings. It is okay to label the mapping as unresolved; it is not okay to infer an electrical conclusion from a successful wire draw.
5 — Concrete functional demonstration
Run, in the real browser:

A. Load the workspace at the V4 board and sensor; the board body is real, distinct from DevKit V1; all 38 V4 contacts are individually addressable. Display the asset's truthful provenance.

B. Hover/focus sensor/TRIG, then board/J2.5. Pin positions and labels match the actual selected physical contacts. Connect them; show edge from precisely the correct anchor. The export contains stable visual endpoint IDs and only an explicitly reviewed canonical binding if available.

C. Rewire TRIG from board/J2.5 to board/J3.9. The old edge must genuinely change. Do not switch a preprogrammed illustration. Verify a separate ECHO wire remains on its original endpoints.

D. Add or reposition resistor and LED from library components; mouse click and keyboard focus work on each real lead. This does not authorize a simulated circuit result.

E. Drag both large parts, zoom to 0.5×, 1×, 2×, pan, resize to 1024×768 and 1440×900, and verify that physical contact anchors and wire endpoints stay aligned. Measure observed offset in CSS px, save screenshots showing cursor, selected pin and edge endpoint alignment; set per-scale tolerance based on real measured geometry (e.g. ≤5 CSS px at normal zoom; explain any exception). Screenshots must use the actual browser, not generated mockups.

F. Undo, redo, delete and restore edges; export, reload and confirm deterministic IDs and the same endpoint graph. Confirm that malformed/unsupported variant mapping fails closed and that the client does not issue fake safety verdicts.

G. Compare visual quality side by side with the Wokwi user reference and actual shipped Wokwi Elements. Device readability, physical lead location and pin selection must meet the owner's acceptance; unit tests alone cannot approve aesthetics.
6 — Test gates (must be independently falsifiable)
ID	PASS requirement
D2R-01	Predecessor SHA and remote branch verified; research, core and policies unchanged.
D2R-02	Components actually loaded from external permissively licensed professional assets, no AI-drawn device replacements.
D2R-03	Exact V4 visual candidate and permissions/provenance documented; if not proven, specific V4_ASSET_GATE_PENDING, never mislabel V1.
D2R-04	V4 asset variant and J2/J3 38-contact ordering reconciled with reviewed Espressif/CORE facts.
D2R-05	Every V4 pin has unique visual ID, correct visual position and focusable handle.
D2R-06	Reviewed J2.5, J3.9, and other real fixture terminals map only under pinned existing catalog evidence.
D2R-07	All unreviewed pins are visually selectable but never falsely engineering-qualified.
D2R-08	Wokwi Elements HC-SR04 renders correctly; 4 real pins separately addressable.
D2R-09	Wokwi Elements LED and resistor renders correctly; both real leads interactive.
D2R-10	No hidden hardcoded duplicate pinInfo table for library components; geometry changes invalidate stale handles.
D2R-11	TRIG→J2.5 and rewire→J3.9 are genuine pointer events / state changes, not canned scenarios.
D2R-12	Draft connect/cancel and invalid edges have no committed effect.
D2R-13	Existing wires retain exact endpoint IDs and alignment across drag, pan, zoom and resize.
D2R-14	Keyboard-only pin discovery/connect/delete and visible focus/pin locator work.
D2R-15	Undo/redo and deterministic visual export + reimport preserve identity/edges.
D2R-16	Visual export contains no forged canonical CircuitSnapshot or engineering verifier outputs.
D2R-17	Proper error handling for missing asset, missing pin, wrong revision, duplicate anchors and stale asset hash.
D2R-18	Local offline runtime after dependency install; no Wokwi-hosted simulator/account/API/token.
D2R-19	Typecheck/build/unit/e2e scripts executed and output recorded with no concealed failures.
D2R-20	Real Chromium screenshots and alignment measurements attached to report; manual visual quality explicitly undecided until owner inspection.
D2R-21	All licences/asset rights and package integrity documented; uncertain V4 artwork excluded from distributable build, not silently promoted.
D2R-22	Scope diff reviewed, commit/push to task branch verified, main unchanged, next decision explicitly reported.


Adversarial tests: wrong J2/J3 row translation; V1 art relabeled as V4; disconnected visual pin after resize; two adjacent pins selecting the same ID; stale asset digest; tampered/missing pinInfo; switching board variants while wires exist; unusually small zoom; unauthorised JS HTML injection via labels; source license metadata missing; reimport after version change. Must not yield a fake success.
7 — Source rights: strict, practical, and non-blocking
The owner explicitly asks not to let avoidable restrictions cause an inaccurate board or poor UX. Implement this policy:
- If a high-fidelity exact V4 asset has verified compatible rights, use it; do not reject for arbitrary reasons.
- If a particular Wokwi wokwi-boards V4 SVG lacks reuse permission, do not distribute that file merely because Wokwi Elements is MIT. Search CC0/permissive variants and evaluate the CC0 STEP path. This is not a refusal to build the canvas.
- If legal/variant fit fails for an otherwise good V4 candidate, leave only that candidate unadmitted; complete licensed HC-SR04/LED/resistor, canvas, and all-independent pin interactions, and report PARTIAL_V4_ASSET_PENDING. Never solve it by saying the V1 art is the real V4 or by ignoring the problem.
- Keep asset license/provenance separate from hardware truth. CC0 means reuse rights, not correctness of physical geometry. No metadata such as resistor values or GPIO safety is inferred from a renderer.
- No external service or paywall required for a working local runtime.
8 — Allowed changes and expected files
Implement new prototypes/ds-002b/ containing package.json, lockfile, Vite/React/TS config, source, DeviceVisualAdapter, VisualPinRegistry, VisualWire management, V4 asset integration/ledger, minimal technical interface, and tests. Do not scatter generated files into unrelated repo directories or overwrite the existing local Vite project.

Additional authorized paths:
- tasks/DS-002B-REV2.md — copy of this exact handoff (do not silently edit instructions).
- reports/DS-002B-REV2-REPORT.md — factual run history, screenshots paths, source rights, pin alignment results, gaps.
- narrow factual updates to docs/STATUS.md, tasks/NEXT.md, tasks/WORK_LOG.md, respecting repo governance.
Do not modify existing CORE, CAP, SYN, E1/E2, EDU/CHAT, test fixtures, scientific research archives, existing source catalogs, policies, documentation of accepted previous reports or master plan without owner authorization. No merge into main. Do not assume VIS-001 exists or can be integrated.

Recommended file group, adjust only within the new directory as evidence requires:
prototypes/ds-002b/
  package.json / package-lock.json / vite.config.ts / tsconfig*.json
  index.html
  src/
    main.tsx
    App.tsx
    device/
      visual-types.ts
      visual-registry.ts
      wokwi-elements-adapter.tsx
      v4-asset-adapter.tsx
      visual-to-canonical-fixture.ts
    canvas/
      DeviceNode.tsx
      visual-connections.ts
      Workspace.tsx
    style.css
  tests/
    visual-registry.test.ts
    edge-lifecycle.test.ts
    browser-canvas.spec.ts
  evidence/
    *.png  # real browser screenshots only
  ASSET_AND_LICENSE_LEDGER.md
  PIN_GEOMETRY_AND_MAPPING_AUDIT.md
  README.md
Before any file generation, preserve existing hand-created / user-owned untracked work. Do not overwrite. The isolated app must run with actual package dependencies, not CDN script tags or a single embedded fake HTML screenshot.
9 — Development and owner handover
1. Run baseline checks; read exact code and source. Record installed Node, npm, browser versions.
2. Evaluate exact V4 licensed assets and reconcile source facts; select by evidence, not by aesthetic guess. Record fallback and any mismatch before implementation.
3. Implement Wokwi Elements adapters, React Flow handles and correctly anchored V4 pin overlay.
4. Add wire lifecycle, keyboard alternative, undo/redo and deterministic export.
5. Execute unit, browser and visual-alignment tests sequentially where necessary (prior Windows HTTP test had a transient socket abort under parallelism). Log failures and reruns honestly.
6. Capture 1440×900 and 1024×768 real browser screenshots (additional zoom/hover captures) and provide actual file paths in report.
7. Record one real user demonstration: V4 TRIG→J2.5→J3.9, plus movement and correction. Do not claim verified electrical compatibility.
8. Commit only authorized files, push task branch and independently re-fetch exact remote SHA. Report main unchanged.
9. Final status: ACCEPTANCE_CANDIDATE, PARTIAL_V4_ASSET_PENDING, BLOCKED_TECHNICAL_CONTRADICTION, or FAILED_QA. These are Codex reports, not owner acceptance.
10. If a material identity contradiction makes exact V4 mapping impossible without changing accepted CORE models, return OWNER_DECISION_REQUIRED with the smallest reproducible evidence; no self-authorized architecture change.
Next stage is a separate owner decision: visual canvas → canonical engineering UI integration; later separate design work for product shell, project entry, Create/Learn mode, hints, assessments and LLM interpretation chat. Do not implement them as hidden extras.
10 — Reference index checked during preparation
- Licensed renderer source (MIT): https://github.com/wokwi/wokwi-elements ; https://elements.wokwi.com/
- React Flow named handles/dynamic internals (MIT): https://reactflow.dev/learn/customization/handles
- Exact V4 upstream reference (not automatically reusable): https://github.com/wokwi/wokwi-boards/tree/main/boards/esp32-devkit-c-v4
- CC0 V4 CAD candidate with explicit nominal dimension caveats: https://www.innerscene.com/tools/library/3d-parts/esp32-devkitc-v4-layout-1ab70892
- Official manufacturer V4 technical identity and J2/J3 pin tables: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
- GitHub's license rule: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
- Repository research G: docs/research/raw/RESEARCH_G_WOKWI_UX_ARCHITECTURE_AND_DEMO_STRATEGY.md
- Superseded handoff: DS-002B REV 1 in the owner conversation; do not run two versions.
OWNER-FROZEN REVISION 2 — END.