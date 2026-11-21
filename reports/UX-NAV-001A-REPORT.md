# Execution report — UX-NAV-001A Rev 1.0

- Session date — 2026-11-21, Asia/Tbilisi
- Plan — [frozen handoff](../tasks/UX-NAV-001A.md)
- Outcome — **PASS for the test-only semantic experiment**
- Experimental entry — `/?ux=entry`
- Base — `codex/ux08-t02a-source-native-gpio-projection` at `771b45a6215fb32d8ba326ec9debe5c857adadcd`
- Task branch — `codex/ux-nav-001a-semantic-component-entry`

## A. Preflight and scope

Read `AGENTS.md`, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, `docs/SESSION_PROTOCOL.md`, `docs/adr/ADR-0001-product-scope.md`, `reports/REPORT_TEMPLATE.md`, the pinned archived `reports/UX08-T02A-REPORT.md`, and the local Screen Architecture v0.2 plan. Read the five named prototype source files, `tests/canvas.spec.ts`, `package.json`, and the existing asset and license ledger. The standalone owner handoff supplied all execution authority.

Fetched origin and verified the exact local and live UX08-T02A base. Ancestry from R3 `7816809` was confirmed. The new task branch was absent locally and remotely, and the tracked worktree and index were clean. Created the branch at the pinned base. The untracked UX-08-R2 audit archive and screen architecture plan stayed outside staging. ADR-0001 applies. ADR-0002 remains proposed/on hold and ADR-0003/0004 remain undecided.

## B. Implementation and observed behavior

The exact entry URL starts with an empty React Flow layout. The native modal uses the existing device names and IDs. It offers placement for HC-SR04, LED and resistor. The ESP32-DevKitC-32E row is disabled and informational. A placement reuses the same node template and previously declared position and leaves existing state in place. The shelf checks presence from the current layout and the placement handler rejects duplicate or unsupported IDs.

Opening focuses the search field. Closing returns focus to the opener. The canvas hotkeys stay inactive while the modal is open. The first browser run exposed Chromium's Escape behavior in a filled native search field. It cleared the search while leaving the dialog open. The search field now closes its dialog on the first Escape and stops that event before it reaches the canvas.

The experiment retains real Wokwi handles and uses the existing visual edge, move, pan, zoom, and undo/redo behavior. The entry route omits the fixed-layout JSON controls and the nominal board's provenance text. It displays `VISUAL_ONLY_NOT_ENGINEERING_VERIFIED` and `TEST_ONLY · SEMANTIC_EXPERIMENT_NOT_VISUAL_DESIGN`. The existing root canvas still provides its original four-part layout and JSON controls.

## C. File manifest

| Path | Change |
| --- | --- |
| `prototypes/ds-002b/src/main.tsx` | Opt-in check for the exact URL. |
| `prototypes/ds-002b/src/Workspace.tsx` | Entry mode, single placement, modal hotkey isolation and entry-specific states. |
| `prototypes/ds-002b/src/ComponentShelf.tsx` | Native dialog, search, placement and focus behavior. |
| `prototypes/ds-002b/src/style.css` | One structural heading rule to fit the existing toolbar. |
| `prototypes/ds-002b/tests/entry-shelf.spec.ts` | Seven Playwright cases covering the eight handoff criteria. |
| `prototypes/ds-002b/evidence/ux-nav-001a-entry-1440x900.png` | Actual Chromium canvas with the keyboard-created wire. |
| `prototypes/ds-002b/evidence/ux-nav-001a-entry-1024x768.png` | Actual Chromium shelf showing two placed items, the disabled board and the available resistor. |
| `tasks/UX-NAV-001A.md` | Verbatim owner handoff. |
| `reports/UX-NAV-001A-REPORT.md` | Execution, verification and publication evidence. |

## D. Acceptance

| ID | Result | Observed |
| --- | --- | --- |
| UXN-01 | PASS | All five unchanged legacy Chromium tests passed. The root retained four nodes, 46 handles and JSON controls. A non-exact query stayed on the four-node legacy route. |
| UXN-02 | PASS | Exact entry displayed its heading, qualification, canvas and one Add button. Zero initial nodes, contacts, or board image. Empty canvas and no selection were distinct. |
| UXN-03 | PASS | Search focused on open. Mixed-case existing ID/name filtering worked. Arbitrary input yielded an explicit empty result. Escape returned focus and preserved an active draft, selection, zoom and position. |
| UXN-04 | PASS | Mounted actual HC-SR04, LED and resistor renderers. Sensor and LED appeared at the declared positions with validated handles. Reopened shelf marked placed entries and removed duplicate actions. An injected empty LED pin list withheld its handles and the resistor still placed with two handles. |
| UXN-05 | PASS | Connected `sensor/TRIG → led/A`. Adding a third part preserved the selected wire and zoom. Dragging the LED changed the actual path. Panning changed the viewport and undo/redo removed/restored the wire. The maximum measured SVG endpoint-to-handle error was 0.0000 CSS px at each of 0.5×, 1× and 2× against a 2 CSS px threshold. |
| UXN-06 | PASS | Disabled ESP32 row had no placement action. The experiment requested no ESP32 image in either capture run. |
| UXN-07 | PASS | Entry omitted fixed-layout JSON transfer and Save/Recent/Recover, assistant, lesson and engineering verdict controls. Contact inspection showed `CANONICAL_MAPPING_UNAVAILABLE`. |
| UXN-08 | PASS | Real Chromium keyboard open, search, place, focus return and terminal connection passed at both viewports. Escape and focus restoration passed. The capture runs saw zero page exceptions and zero off-origin requests. |

## E. Commands and observed results

Node 24.16.0, npm 11.13.0, Vite 8.3.8, Playwright 1.65.1 and the installed Chromium 151.0.7922.34 were used. Typecheck, build and unit commands ran in `D:/Inventor_EDU/prototypes/ds-002b`. The two Chromium runs used an archive of the pinned prototype in a temporary directory with the five current implementation/test files overlaid. A junction reused the already installed `node_modules`. `DS002B_CHROMIUM` selected the cached browser. The unchanged Playwright config used loopback port 4173. This kept the legacy tests' automatically regenerated screenshots outside the repository.

| Command | Exit | Observed output |
| --- | --- | --- |
| `npm run typecheck` | 0 | `tsc --noEmit` completed. |
| `npm run build` | 0 | `61 modules transformed`, `built in 137ms` on the final run. Rolldown retained its warning about React Flow's module-level `use client` directive. |
| `npm test` | 0 | Three passed, zero failed, canceled or skipped. |
| `npm run test:e2e`, first run | 1 | `2 failed`, `10 passed (40.8s)`. Both failures were Escape with a filled search field. All five legacy tests had passed. |
| `npm run test:e2e`, final run | 0 | `12 passed (13.0s)`, comprising five legacy and seven entry cases. Zero failures and skips. The test server printed Lit dev-mode and NO_COLOR/FORCE_COLOR notices. |
| `git diff --check` | 0 | No whitespace diagnostics. Git emitted its working-copy newline notice. |

## F. Chromium evidence

- [1440×900 — keyboard-created visual wire](../prototypes/ds-002b/evidence/ux-nav-001a-entry-1440x900.png)
- [1024×768 — open native shelf after placement](../prototypes/ds-002b/evidence/ux-nav-001a-entry-1024x768.png)

The captures are actual Chromium PNGs. The first shows the named wire and selected LED contact. The second shows the focused search field, disabled ESP32 item, placed status and remaining resistor action. Both show the experiment qualification.

## G–J. Limits, OSS, rollback and review

The observed alignment compares browser wire endpoints with real renderer handles. It supplies visual geometry evidence for this experiment. It supplies no physical board qualification, canonical engineering mapping, capability verdict or electrical safety evidence. The native dialog and existing editor styling are for behavioral review. Production visual design and user experience acceptance remain owner decisions.

OSS additions — `NONE`. The existing Wokwi Elements 1.9.2 and React Flow 12.10.0 installation was reused. The lockfile, assets and legacy tests were preserved. An owner-authorized revert of the task commits would restore the pinned baseline. Review this semantic experiment and its evidence in the architecture conversation.

## Git publication

The staged review found exactly nine authorized paths. The tested source and both actual Chromium PNGs matched the staged content. Local report links resolved, the credential-pattern scan found no matches, and both working and staged whitespace checks exited 0. The staged attachment matched the handoff byte for byte, SHA-256 `349d4b5cfffd155888e4baf7344bea8f12a0a79c6d4e2caec76d83dba7b0b36f`.

`git push -u origin codex/ux-nav-001a-semantic-component-entry` exited 0. A separate live ref query and fetch verified implementation commit `482e62164a47686f380d94fcb1e07180d8983a01`, the predecessor at `771b45a6215fb32d8ba326ec9debe5c857adadcd`, and remote `main` at `b1db3e947d04508ca22d4ba55e3172616620bad2`. This report-only follow-up records the verified implementation publication.
