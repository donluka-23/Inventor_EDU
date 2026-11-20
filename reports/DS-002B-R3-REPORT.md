# Execution report — DS-002B-R3

- Session date — 2026-11-21, Asia/Tbilisi.
- Frozen plan — [DS-002B-R3](../tasks/DS-002B-R3.md).
- Outcome — **OWNER_DECISION_REQUIRED**. The verified manufacturer photo of the exact assembly has baked-in callouts covering the J2.8 contact center and other target hardware details. No clean exact-variant asset with verified redistribution rights and sufficient visual detail was established. The asset gate stopped renderer and geometry implementation.
- Live baseline — `origin/codex/ds-002b-exact-component-canvas-r2` at `72df4ea34169ab10a59810b22c50e1fbbc81188f`. It includes the reported R2 implementation checkpoint `3c1081c0e250f0278d70b13866f279e3b63a7d88`.
- Task branch — `codex/ds-002b-r3-exact-hardware-visual`, created at the verified live R2 head. Protected `main` at preflight was `b1db3e947d04508ca22d4ba55e3172616620bad2`.

## A. Boot brief and scope

Read `AGENTS.md`, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, `docs/SESSION_PROTOCOL.md`, `docs/VERIFICATION_POLICY.md`, `docs/OSS_POLICY.md`, `governance/OSS_REGISTER.csv`, and accepted `docs/adr/ADR-0001-product-scope.md`. Read the R3 handoff and the R2 handoff, execution report, asset ledger, and pin audit. Consulted the R2 fixture links and existing application test configuration. Applied the OSS intake and evidence-gated engineering skills to the conditional asset gate.

The only permitted implementation work was within `prototypes/ds-002b/` after asset qualification. This checkpoint records the blocked gate and baseline regression evidence. `docs/research/raw/INVENTOR_EDU_SCREEN_ARCHITECTURE_PHASE_PLAN.md` was untracked before the branch switch and stayed outside staging.

## B. Exact manufacturer source and smallest reproducible blocker

| Check | Direct evidence | Result |
| --- | --- | --- |
| Source identity | Espressif `esp-dev-kits` revision `da43a78cfdd2a1122047bb5617ca79e09fd687b2`, `docs/_static/esp32-devkitc/esp32-devkitc-v4-functional-overview.png`. The raw file and live guide image had identical SHA-256 `e078f94904c5396ac7475c1e2349b368b31db7bb4d2716954bc3f72fdad7ab3c`. | PASS |
| Variant | The guide caption and order table identify `ESP32-DevKitC V4`, product `ESP32-DevKitC-32E`, and module `ESP32-WROOM-32E`. The photo's shield carries the 32E marking. | PASS for source identity |
| Resolution and orientation | 1738 × 751 RGB raster. The board occupies roughly 820 × 410 source pixels including antenna and USB. It is nearly top-down and horizontal, with USB left and antenna right. Rotating counterclockwise would place the antenna above and USB below. | Measured original, no upscaling |
| Clean visual extraction | Cropping the annotation text leaves seven callout dots or leads on the hardware. At the J2.8 contact center, source pixel `(854, 208)` is `(255, 0, 0)`. EN `(475, 278)`, BOOT `(475, 514)`, USB `(431, 395)`, the regulator-area LED callout `(604, 277)`, USB–UART bridge `(574, 407)`, and part of the module shield `(1086, 322)` also have opaque red at the marked location. | FAIL |
| Contact geometry | Espressif's connector tables and diagram establish row order and pin names. The opaque J2.8 mark removes the contact pixels needed to independently compare that physical center against the proposed artwork. Neighbor extrapolation would predict a position without restoring or validating the original feature. | BLOCKED for complete image correspondence |

Open the exact PNG at native resolution and inspect the upper row near the `33` marking, eighth contact from the antenna end. The guide's J2 table identifies that position as J2.8. The PNG is a flattened RGB raster. Crop, rotation, rectification, and transparent background processing cannot recover its overwritten pixels. A generated or hand-reconstructed contact would lack source evidence. No board artwork was selected or transformed for distribution. [Pinned PNG](https://raw.githubusercontent.com/espressif/esp-dev-kits/da43a78cfdd2a1122047bb5617ca79e09fd687b2/docs/_static/esp32-devkitc/esp32-devkitc-v4-functional-overview.png) · [Manufacturer guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html)

The pinned GitHub README documents CC BY-SA 4.0 International for repository documentation and its images. The pinned license file SHA-256 is `2003829cf643d61b00a76088dd31bb11b8029546f24c56b39fd492adb9281483`, and the README SHA-256 is `e7bbfd8b1066fcf2b018da3c50f47dd75a9893ecf0b73ca3056c81d3f5de4e9a`. No narrower notice was found for the inspected repository image. Reuse would require attribution to Espressif, source and license links, an indication of changes, retention of applicable notices, and CC BY-SA terms for distributed adaptations. Repository OSS policy separately requires explicit review of ShareAlike intake. No applicable approval was found in the OSS register. No license conclusion about another Espressif site follows from this repository grant. [Pinned README](https://github.com/espressif/esp-dev-kits/blob/da43a78cfdd2a1122047bb5617ca79e09fd687b2/README.md#open-source-licensing) · [Pinned license](https://github.com/espressif/esp-dev-kits/blob/da43a78cfdd2a1122047bb5617ca79e09fd687b2/LICENSE-CC-BY-SA) · [Legal code](https://creativecommons.org/licenses/by-sa/4.0/legalcode) · [Project OSS policy](../docs/OSS_POLICY.md)

## C. Alternatives submitted for owner review

| Candidate | Observed variant and visual evidence | Rights and disposition |
| --- | --- | --- |
| [Espressif product page 32E column](https://www.espressif.com/en/products/devkits/esp32-devkitc#compare) and [direct 32E PNG](https://www.espressif.com/sites/all/themes/espressif/images/esp32-devkitc/esp32-devkitc-32e.png) | Exact 32E column. The file is a 160 × 286 simplified rendering with generic shield detail and no contact silkscreen. SHA-256 `477e8e9f17b268215b5b27028473550f212e77fd4811f4df230bb9d12cb346b8`. | Commercial site. No file-specific reuse grant was located. Visual detail fails the R3 gate. |
| [Espressif unannotated board photo](https://github.com/espressif/esp-dev-kits/blob/da43a78cfdd2a1122047bb5617ca79e09fd687b2/docs/_static/esp32-devkitc/esp32-devkitc-board.png) | Clear silkscreen and connector detail. Its shield visibly reads `ESP32-WROVER-E`. SHA-256 `abe35074205aa38256d25fafcdb35c9eb5720c1eb40b3127db6889dc710a4ff7`. The repository's rear dimensions figure and C15 illustration do not supply a clean matching front. | Repository documentation grant applies. The assembly fails exact identity. |
| [DigiKey exact MPN listing](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-DEVKITC-32E/12091810) and [Mouser exact MPN listing](https://www.mouser.co.uk/en/ProductDetail/Espressif-Systems/ESP32-DevKitC-32E?qs=GedFDFLaBXFpgD0kAZWDrQ%3D%3D) | Listing metadata identifies the correct orderable model. Direct product page retrieval returned HTTP 403 during inspection, which left the original image bytes, photographed variant, and contact visibility unverified. | No file-specific permission established. [DigiKey terms](https://www.digikey.com/en/terms-and-conditions) |
| [Devan Metz 32E reference](https://devanmetz.com/boards/esp32-devkitc-v4/) | Credits the same Espressif annotated overview and describes its WebP conversion and resizing. The lineage does not provide an independent clean original. | Published attribution and CC BY-SA 4.0 label. Kept as a reference. |
| [Wokwi V4 reference](https://github.com/wokwi/wokwi-boards/tree/962b19d5636756537a93bb5337ac99abd775eae0/boards/esp32-devkit-c-v4) | V4 arrangement and 38 positions, with generic `ESP32` shield art. Exact 32E assembly identity is unestablished. Re-fetched SVG SHA-256 `002cb0eb5e33b926728bd0d3744e1c37830a82fa1f331434080e6f16cbad6763` and JSON SHA-256 `6377990e1317d929ac164570ba5adc0a32ccfaf10d66300526c6a132a2a5f885` match R2. | Pinned root `LICENSE` request returned HTTP 404. File-specific terms remain unestablished. Inspection reference only. |

## D. Official 38-contact inventory and R3 mapping status

Published names below come from the [pinned J2/J3 tables](https://github.com/espressif/esp-dev-kits/blob/da43a78cfdd2a1122047bb5617ca79e09fd687b2/docs/en/esp32-devkitc/user_guide.rst#header-block), SHA-256 `a6e89080a3a5f9b99f33e63e7a0d9788fa858ad11cd25feffbb9e4df15229f1b`. The [manufacturer pin layout](https://github.com/espressif/esp-dev-kits/blob/da43a78cfdd2a1122047bb5617ca79e09fd687b2/docs/_static/esp32-devkitc/esp32_devkitC_v4_pinlayout.png), SHA-256 `e3217229b995ec7e1b5c525ffd93eced3b3a17827806907dd25a1609667283e2`, independently shows the orientation. With antenna up and USB down, J2 is left, J3 is right, and both rows count towards USB. Each row has 19 unique ordinals.

“Present in fixture” means the existing exact-variant catalog contains that terminal. The catalog covers ten positions. This table adds zero canonical bindings. All visual-to-engineering projections remain `CANONICAL_MAPPING_UNAVAILABLE`. A dash means there was no admitted R3 image, rendered handle, or observed geometric deviation. [Existing catalog](../data/gpio/devkitc_32e_catalog.json)

| Visual terminal | Official position | Published name | Source | R3 image coordinate | R3 DOM coordinate | Deviation | Mapping status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `board/J2.1` | J2 1 | 3V3 | J2 table | — | — | — | R3 uncalibrated, present in fixture |
| `board/J2.2` | J2 2 | EN | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.3` | J2 3 | VP | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.4` | J2 4 | VN | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.5` | J2 5 | IO34 | J2 table | — | — | — | R3 uncalibrated, present in fixture |
| `board/J2.6` | J2 6 | IO35 | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.7` | J2 7 | IO32 | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.8` | J2 8 | IO33 | J2 table | — | — | — | Source contact obscured |
| `board/J2.9` | J2 9 | IO25 | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.10` | J2 10 | IO26 | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.11` | J2 11 | IO27 | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.12` | J2 12 | IO14 | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.13` | J2 13 | IO12 | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.14` | J2 14 | GND | J2 table | — | — | — | R3 uncalibrated, present in fixture |
| `board/J2.15` | J2 15 | IO13 | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.16` | J2 16 | D2 | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.17` | J2 17 | D3 | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.18` | J2 18 | CMD | J2 table | — | — | — | R3 uncalibrated |
| `board/J2.19` | J2 19 | 5V | J2 table | — | — | — | R3 uncalibrated, present in fixture |
| `board/J3.1` | J3 1 | GND | J3 table | — | — | — | R3 uncalibrated, present in fixture |
| `board/J3.2` | J3 2 | IO23 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.3` | J3 3 | IO22 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.4` | J3 4 | TX | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.5` | J3 5 | RX | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.6` | J3 6 | IO21 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.7` | J3 7 | GND | J3 table | — | — | — | R3 uncalibrated, present in fixture |
| `board/J3.8` | J3 8 | IO19 | J3 table | — | — | — | R3 uncalibrated, present in fixture |
| `board/J3.9` | J3 9 | IO18 | J3 table | — | — | — | R3 uncalibrated, present in fixture |
| `board/J3.10` | J3 10 | IO5 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.11` | J3 11 | IO17 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.12` | J3 12 | IO16 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.13` | J3 13 | IO4 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.14` | J3 14 | IO0 | J3 table | — | — | — | R3 uncalibrated, present in fixture |
| `board/J3.15` | J3 15 | IO2 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.16` | J3 16 | IO15 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.17` | J3 17 | D1 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.18` | J3 18 | D0 | J3 table | — | — | — | R3 uncalibrated |
| `board/J3.19` | J3 19 | CLK | J3 table | — | — | — | R3 uncalibrated, present in fixture |

## E. Acceptance and commands

| Scenario | Outcome | Scope of evidence |
| --- | --- | --- |
| A — Visual identity | BLOCKED | Exact identity confirmed in the source photo. The clean-art gate failed. |
| B — 38 contacts | PARTIAL | All official contact IDs and names inventoried. Replacement image and DOM calibration were blocked. |
| C — Real wiring | BASELINE ONLY | R2 regression used real Chromium. Replacement scenario was blocked. |
| D — Geometry | BASELINE ONLY | R2 0.5×, 1×, 2× and DPR 1 and 2 regression. No exact-asset geometric result. |
| E — Negative cases | BASELINE ONLY | R2 malformed asset, pin registry, import, keyboard, and nearby contact checks were exercised. Replacement orientation and photo tests were blocked. |
| Owner visual acceptance | BLOCKED | R2 board art was rejected by the owner. R3 has no replacement to review. |

Baseline validation used a temporary archive of the verified R2 head. Frontend commands ran in `%TEMP%/InventorEDU-DS002B-R3/baseline/prototypes/ds-002b` with Node 24.16.0, npm 11.13.0 and Chromium 151.0.7922.34 through Playwright 1.65.1. The existing lockfile SHA-256 is `6a876584f986914801e5010ba9d4a67571a4b66159c4041269dfc37d48df26fd`.

| Command | Exit | Observed output |
| --- | ---: | --- |
| `git archive --format=tar --output="$archive" 72df4ea34169ab10a59810b22c50e1fbbc81188f prototypes/ds-002b` and `tar -xf "$archive" -C "$trial"` | 0 | Isolated current R2 application and checked-in tests. |
| `npm ci --no-audit --no-fund` | 0 | Added 54 packages. |
| `npm run typecheck` | 0 | `tsc --noEmit` completed. |
| `npm run build` | 0 | Vite 8.3.8 built 60 modules. The existing React Flow `use client` bundle warning remained. |
| `npm run test` | 0 | 3 passed, 0 failed, 0 skipped. |
| `npm run test:e2e`, first attempt | 1 | Playwright stopped before tests because loopback port 4173 was already in use. |
| `npm run test:e2e`, rerun | 0 | 5 passed in 22.1 s. A literal port replacement from 4173 to 4183 was made only in the temporary copy of `playwright.config.ts` and `tests/canvas.spec.ts`. The original service was left alone and all assertions were preserved. |
| `node "$previousSmoke" "$env:DS002B_CHROMIUM"` | 0 | Previous local R2 smoke harness ran Vite preview on port 4174 with off-origin traffic blocked. Output: `Built preview: 46 contacts, pointer wire visible, runtime notices served, 0 off-origin requests`. |
| `curl.exe -fsSL` for the source assets and `Get-FileHash` | 0 for the recorded files | Pinned and live exact photo hashes matched. The first attempt at upstream `LICENSE` got HTTP 404, and retrieval of the actual `LICENSE-CC-BY-SA` succeeded. Wokwi's root `LICENSE` returned HTTP 404 separately. |

```powershell
$exe = Join-Path $env:TEMP 'InventorEDU-CORE-001A-8155c25ec54d40d8ba68e4f93c6f8d7a/Scripts/python.exe'
$env:HYPOTHESIS_STORAGE_DIRECTORY = Join-Path $env:TEMP 'InventorEDU-DS002B-R3-hypothesis'
& $exe -B -m unittest tests.test_core001a tests.test_core001a_r2 tests.test_gpio_capability tests.test_edu_t1_transfer -q
```

Python 3.12.8, repository root, exit 0. Observed `Ran 56 tests in 17.123s` and `OK`.

The R2 Chromium rerun exercised the original TRIG-to-J2.5 wire, rewire to J3.9 with independent ECHO at J3.8, both component moves, pan, resize, undo/redo, export/reload/import, stale or missing images, and keyboard paths. It measured wire-to-handle offset at 0 CSS px at all three zoom levels. For the nominal R2 asset, J3.9 handle-to-artwork deviations were 0.049, 0.098 and 0.197 CSS px at 0.5×, 1× and 2×. At 1× the all-contact maximum was 0.116 CSS px. These are baseline results against the rejected artwork.

## F. Screenshot evidence

R3 `workspace-1440x900.png`, `workspace-1024x768.png`, `board-closeup-1x.png`, `board-closeup-2x.png`, `pin-interaction.png` and `reference-vs-rendered.png` are **NOT_RUN** for a replacement asset. R2 captures remain historical evidence of the existing nominal renderer and interaction behavior. The official source link in §B shows the actual 32E and the opaque callouts. [R2 1440×900 capture](../prototypes/ds-002b/evidence/workspace-1440x900.png) · [R2 1024×768 capture](../prototypes/ds-002b/evidence/workspace-1024x768.png)

## G. File manifest and limits

| Path | Change |
| --- | --- |
| `tasks/DS-002B-R3.md` | Exact owner-frozen task attachment. |
| `reports/DS-002B-R3-REPORT.md` | Asset gate, pin inventory, observed tests, and checkpoint evidence. |
| `docs/STATUS.md` | Factual R3 and R2 visual-review status. |
| `tasks/NEXT.md` | Advisory pointer to the blocked gate and owner decision. |
| `tasks/WORK_LOG.md` | R3 chronology. |

The blocked gate left the existing prototype, source assets, lockfile, engineering contracts and catalogs at the R2 baseline. Downloaded candidate artwork and temporary Chromium outputs stayed outside Git. No new component library, renderer dependency or asset was admitted.

## H. Owner decision

Provide or approve a clean, near-top-down photo of a documented `ESP32-DevKitC-32E` with its visible `ESP32-WROOM-32E` shield, readable silkscreen and all 38 unobstructed contacts. Record file-specific modification and redistribution rights or arrange an owner-controlled photograph with an approved license. If a ShareAlike asset is selected, complete the separate review required by the OSS policy before artwork integration. Re-run exact-asset geometry, screenshots and owner visual review after source admission.
