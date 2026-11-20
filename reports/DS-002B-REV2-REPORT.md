# Execution report — DS-002B revision 2

- Session date — 2026-11-21, Asia/Tbilisi.
- Frozen plan — [DS-002B revision 2](../tasks/DS-002B-REV2.md).
- Outcome — **PARTIAL_V4_ASSET_PENDING**. The canvas works with a rights-cleared nominal V4 shell and three licensed Wokwi Elements. Exact ESP32-WROOM-32E asset fit and the canonical projection remain open. Owner visual acceptance remains pending.
- Task branch — `codex/ds-002b-exact-component-canvas-r2`. Predecessor on `origin/codex/edu-t1-independent-transfer`: `4e6daa0b60937e5863bb754b9293a6504174bb5a`. Preflight `origin/main`: `b1db3e947d04508ca22d4ba55e3172616620bad2`.

## A. Boot brief and evidence

Reviewed `AGENTS.md`, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, `docs/SESSION_PROTOCOL.md`, `docs/VERIFICATION_POLICY.md`, `docs/OSS_POLICY.md`, `docs/prototype/MASTER_PLAN.md` v1.7, accepted ADR-0001, and Research G in `docs/research/raw/RESEARCH_G_WOKWI_UX_ARCHITECTURE_AND_DEMO_STRATEGY.md`. Reviewed the CORE physical terminal model, the existing `data/gpio/devkitc_32e_catalog.json` and corresponding tests, the CORE-001B source and rule ledger, and recent acceptance evidence through EDU-T1. ADR-0002 remains proposed.

Fetched the authorized origin and queried live refs for the predecessor, main, and overlapping DS-002B/VIS-001 tasks. Created the task branch directly at the live predecessor. Preflight showed the untracked `prototypes/ds-002/` folder. That path was absent at final scope inspection. The task issued no edits or deletion against it. The untracked screen-architecture file `docs/research/raw/INVENTOR_EDU_SCREEN_ARCHITECTURE_PHASE_PLAN.md` also stayed outside the staged scope. Changes are confined to the new isolated app, exact task handoff, this report, and the three authorized project tracking files.

## B. Actions and observed results

1. Inspected the official Espressif guide, exact 32E fixture claims, Wokwi Elements source and npm package, Wokwi Boards V4 SVG and JSON, Innerscene STEP, and alternative assets. The FreeSVG preview showed ESP-WROOM-32 on its shield. Inspected the manufacturer figure and rendered the downloaded Wokwi SVG separately in local Chromium. Rights and exact source digests are recorded in the asset ledger.
2. Tessellated the CC0 STEP and rendered an orthographic raster. Extracted 38 centers from the STEP's own named solids. Reconciled the screen order with the official J2/J3 header tables. The generic WROOM shape left the exact assembly gate open.
3. Built an isolated React Flow editor with mounted Wokwi Elements, a validated runtime pin registry, focusable named handles, visual wire state and deterministic JSON interchange. Missing or changed asset geometry disables its own handles. Rewiring preserves the selected wire ID and its first endpoint.
4. Ran real Chromium pointer events for `sensor/TRIG → board/J2.5`, a separate `sensor/ECHO → board/J3.8`, and rewire of TRIG to `board/J3.9`. Verified the ECHO path was byte-identical during rewire. Exercised movement of both major devices, pan and zoom, keyboard selection and deletion, undo/redo, reset by reload plus import, and rejected stale or malformed data.

## C. Changed-file manifest

| Paths | Change and purpose |
| --- | --- |
| `prototypes/ds-002b/.gitattributes`, `.gitignore`, `index.html`, `package.json`, `package-lock.json`, `tsconfig.json`, `playwright.config.ts` | New isolated project and immutable byte handling for CAD contact data. |
| `prototypes/ds-002b/src/main.tsx`, `Workspace.tsx`, `DeviceNode.tsx`, `model.ts`, `style.css` | New browser entry, editor, adapter, registry and interchange logic. |
| `prototypes/ds-002b/src/assets/devkitc-v4.png`, `devkitc-v4.json` | New CC0 raster and pinned CAD contact centers. |
| `prototypes/ds-002b/tools/project-step.cjs`, `project-cad.py`, `inventory-licenses.py` | New reproducibility tools. |
| `prototypes/ds-002b/README.md`, `ASSET_AND_LICENSE_LEDGER.md`, `PIN_GEOMETRY_AND_MAPPING_AUDIT.md`, `public/THIRD_PARTY_NOTICES.txt` | New operator instructions, asset and package ledger, contact evidence, runtime notices. |
| `prototypes/ds-002b/tests/model.test.ts`, `canvas.spec.ts`, `evidence/*.png` | New unit and Chromium tests and actual browser screenshots named below. |
| `tasks/DS-002B-REV2.md`, `reports/DS-002B-REV2-REPORT.md` | New frozen handoff and execution record. |
| `docs/STATUS.md`, `tasks/NEXT.md`, `tasks/WORK_LOG.md` | Updated observed partial status, advisory owner review pointer, and execution chronology. |

Decision, ADR, OSS register, existing protocol, research, master plan, CORE code, source catalog and earlier reports were preserved. The isolated npm dependency and asset facts are recorded in the prototype ledger. Central OSS register reconciliation would require owner authorization of that file.

## D. Acceptance by criterion

| ID | Result | Evidence |
| --- | --- | --- |
| D2R-01 | PASS | Live predecessor SHA verified. Authorized files only. |
| D2R-02 | PASS | Shipped CC0 CAD projection and three actual MIT Wokwi renderers. |
| D2R-03 | V4_ASSET_GATE_PENDING | Candidate bytes and reuse rights verified. Exact WROOM-32E fit unavailable. |
| D2R-04 | PARTIAL | Espressif ordering reconciled to all 38 nominal solids. Exact variant remains unresolved. |
| D2R-05 | PASS, nominal shell | 38 unique focusable contacts. Tested all handle centers against raster pixels. |
| D2R-06 | BLOCKED | J2.5 and J3.9 are known catalog fixture contacts. No exact asset identity proof to enable canonical links. |
| D2R-07 | PASS | All contacts labeled independently of canonical evidence. |
| D2R-08 | PASS | Mounted HC-SR04 and four separate live contacts. |
| D2R-09 | PASS | Actual LED and resistor artwork and four independently operated leads. |
| D2R-10 | PASS | Mounted pinInfo is the coordinate source. Lit flip alters LED geometry. Corrupt pinInfo clears handles and suppresses affected rendered wires. |
| D2R-11 | PASS | Real pointer rewire changes TRIG geometry and retains ECHO. |
| D2R-12 | PASS | Esc, self and reversed duplicate attempts leave committed edges unchanged. |
| D2R-13 | PASS, browser geometry | Dragged both components, panned, changed zoom and resized. SVG edge endpoints stayed within the tested CSS-pixel tolerance of handles. |
| D2R-14 | PASS | Tab, Enter, Space, Delete and a visible contact locator. |
| D2R-15 | PASS | Undo and redo preserve wire records. Reimport after reload produced identical exported JSON. |
| D2R-16 | PASS | Visual-only schema. Extra fields, including invented canonical bindings, are rejected. |
| D2R-17 | PASS, tested cases | Missing raster, stale bytes, corrupted pin list, overlapping hit geometry, unrecognized variant, injected labels and stale import data rejected. |
| D2R-18 | PASS, measured page traffic | No external network request in development or in a built preview with off-origin requests blocked. |
| D2R-19 | PASS | Typecheck, build, unit and Chromium commands completed. Initial failed runs recorded below. |
| D2R-20 | PASS, capture and measurement | Native Chromium screenshots and observed measurements below. Owner aesthetic review is pending. |
| D2R-21 | PASS | Exact source rights and locked package integrities recorded. Wokwi Boards and Espressif illustrations remain inspection references. |
| D2R-22 | PASS | Reviewed the 31-file scope and published the implementation checkpoint. The live task, predecessor and main refs matched the expected SHAs in the verification below. |

## E. Commands and observed terminal results

Prototype commands ran from `D:/Inventor_EDU/prototypes/ds-002b` using Node 24.16.0, npm 11.13.0, Playwright 1.65.1, and real Chromium 151.0.7922.34. Playwright ran the local development server on `127.0.0.1:4173` with `DS002B_CHROMIUM` pointed at the installed Chromium.

| Command | Exit | Observed output |
| --- | --- | --- |
| `npm ci --no-audit --no-fund` | 0 | `added 54 packages in 3s` on Windows. |
| `npm run typecheck` | 0 | `tsc --noEmit` completed without diagnostics. |
| `npm run build` | 0 | Vite 8.3.8 emitted the page, CSS, JS and 7.41 kB CAD raster. Rolldown warned that React Flow's `use client` directive may not be preserved during bundling. |
| `npm run test` | 0 | 3 tests, 3 passed, 0 failed, 0 skipped. |
| `npm run test:e2e` | 0 | 5 Chromium tests using one worker, 5 passed. Lit printed its development-mode notice. |
| `node "$scratch/preview-smoke.cjs" "$chrome"` (temporary harness) | 0 | `Built preview: 46 contacts, pointer wire visible, runtime notices served, 0 off-origin requests`. Vite preview listened on loopback port 4174. Playwright blocked off-origin HTTP traffic. |
| `python tools/inventory-licenses.py` | 0 | Wrote the 86-package dependency ledger and runtime notice file. |
| `node tools/project-step.cjs …` and `python tools/project-cad.py …` | 0 | A second conversion in a temporary directory reproduced both checked-in SHA-256 digests. See the README for the argument order. |

The unchanged Python baseline was checked from `D:/Inventor_EDU` in the previously installed locked Python 3.12.8 environment. The initial `python -m pytest -q -p no:cacheprovider …` under the default shell interpreter gave four collection errors for missing `hypothesis` and `pydantic`. The pinned interpreter did not have pytest. The repository's documented runner then succeeded without any installation.

```powershell
$exe = Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$env:HYPOTHESIS_STORAGE_DIRECTORY = Join-Path $env:TEMP 'InventorEDU-DS002B-hypothesis'
& $exe -B -m unittest tests.test_core001a tests.test_core001a_r2 tests.test_gpio_capability tests.test_edu_t1_transfer -q
```

```text
Ran 56 tests in 5.275s
OK
```

Earlier runs exposed ES2023-only test syntax in the ES2022 typecheck, ambiguous test selectors, an SVG DOM point serialization difference, React Flow pointer and keyboard conflicts, and a drag warning caused by discarded dimension state. Corrected the tests, routed primary pointer presses through the custom handles, and retained React Flow dimension changes. Staging also exposed Windows line-ending normalization of the hashed JSON. The conversion tool now writes LF explicitly, and browser tests use the same digest as the staged bytes. The final checks passed.

## F. Alignment and visual review

Measurements are screen CSS pixels. Edge alignment compares the SVG path endpoints transformed by `getScreenCTM()` with actual DOM handle centers. Board artwork comparison uses gold pixel centroid from the loaded PNG. Sensor comparison uses the actual metal lead rectangle in the SVG shadow root. The maximum for all 38 board contacts at 1× was **0.116 CSS px**.

| React Flow scale | Max TRIG edge to handle | J3.9 handle to raster contact | TRIG handle to metal lead |
| --- | ---: | ---: | ---: |
| 0.5× | 0.000 | 0.049 | 0.048 |
| 1× | 0.000 | 0.098 | 0.096 |
| 2× | 0.000 | 0.197 | 0.192 |

The browser thresholds were 2 CSS px for wire-to-handle, 2 for the zoomed board raster comparison, and 3 for the metal lead. At 1× the all-contact raster gate was 1 CSS px. Adjacent J2.5 and J2.6 selected independently at 0.5× in a device-pixel-ratio 2 Chromium context. These numbers apply only to the displayed renderer geometry.

- [1440×900 workspace after rewire](../prototypes/ds-002b/evidence/workspace-1440x900.png)
- [1024×768 workspace after movement, pan, zoom and resize](../prototypes/ds-002b/evidence/workspace-1024x768.png)
- [2× hover and attachment close-up](../prototypes/ds-002b/evidence/contact-zoom-2x.png)

| Trait | Wokwi V4 reference inspected locally | DS-002B browser result |
| --- | --- | --- |
| Board readability | Printed signal labels, multiple visible surface components and detailed USB area. | Clear nominal board silhouette, 38 gold contacts and a hover/focus label. The STEP derivative has simplified components and no matching silkscreen. |
| Physical lead selection | Wokwi Boards supplies artwork and its own 38 contact coordinates. | CAD mesh centers drive board contacts. Mounted Wokwi Elements supply sensor, LED and resistor leads at runtime. |
| Artwork detail | The V4 SVG shows module branding and detailed terminals. | Wokwi Elements are retained as shipped for the three independent devices. The board artwork's generic module and difference in outline remain material. |

The comparison can be repeated with the [exact Wokwi source](https://github.com/wokwi/wokwi-boards/tree/962b19d5636756537a93bb5337ac99abd775eae0/boards/esp32-devkit-c-v4) and the local screenshots. The local reference capture was excluded from the repo because reuse rights for that artwork were unestablished.

## G. Open scope and owner decisions

Decide whether the nominal shell is acceptable for continued visual prototyping. Exact acceptance and a canonical board projection need separately supported 32E asset identity and physical fit. The generic Wokwi HC-SR04 renderer also lacks an exact link to the reviewed Adafruit PID 3942 profile. No electrical, firmware, or GPIO verification ran through this canvas, and no engineering data is exported. CORE integration remains a separate decision.

## H. Licensing and reproducibility

See the [asset and license ledger](../prototypes/ds-002b/ASSET_AND_LICENSE_LEDGER.md), [geometry audit](../prototypes/ds-002b/PIN_GEOMETRY_AND_MAPPING_AUDIT.md), and [run instructions](../prototypes/ds-002b/README.md). The raw sources used for inspection are referenced by URL and digest. Production and development package revisions are fixed by the lock. No project-wide dependency or governance change was made.

## I. Rollback and review handoff

This experiment is isolated to its task branch. The predecessor needs no new dependencies or migration. For architectural review, attach this Markdown report and the three browser evidence PNGs. The owner should inspect the running canvas and decide whether to keep or replace the nominal board shell.

## J. Git publication evidence

`git diff --cached --check` passed. The staged manifest contained 31 authorized files, all report links resolved, and the reviewed text contained no credential signatures. The projected raster, contact JSON and exact handoff also matched the reviewed bytes in the staging index. The pre-push live query found no overlapping task branch.

`git push --set-upstream origin codex/ds-002b-exact-component-canvas-r2` created and tracked the task branch. The follow-up live query and fetch verified the implementation checkpoint and its unchanged predecessor and main refs.

| Remote branch | Independently verified SHA |
| --- | --- |
| `codex/ds-002b-exact-component-canvas-r2` | `3c1081c0e250f0278d70b13866f279e3b63a7d88` (implementation checkpoint) |
| `codex/edu-t1-independent-transfer` | `4e6daa0b60937e5863bb754b9293a6504174bb5a` |
| `main` | `b1db3e947d04508ca22d4ba55e3172616620bad2` |

`git merge-base --is-ancestor` confirmed the verified EDU-T1 predecessor is an ancestor of the fetched task branch. This report records the implementation checkpoint's publication evidence in a documentation-only follow-up.
