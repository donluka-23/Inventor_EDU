# DS-002B visual contact audit

## Source identity and orientation

The prototype shows a CC0 **nominal DevKitC V4 CAD** shell. Espressif documents an ESP32-DevKitC-32E order option with ESP32-WROOM-32E. The selected STEP contains `WROOM_module`, a generic shield and an explicitly illustrative antenna. It does not identify the soldered module as 32E. Exact variant and physical fit remain `V4_ASSET_GATE_PENDING`. [Espressif guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html) · [Innerscene source](https://www.innerscene.com/tools/library/3d-parts/esp32-devkitc-v4-layout-1ab70892)

The actual mesh has 19 square contact solids on each row. Their centers are x = 1.27 and 26.67 mm, y = 1.27 through 46.99 mm at 2.54 mm intervals. The carrier spans 27.94 × 48.26 mm, and the micro-USB projects 1.20 mm past its lower end. Pitch in the downloaded file is more specific than the nominal 2.5 mm given on the landing page. Wokwi's V4 JSON instead gives 27.9 × 56.628 units with 2.54 row increments. Its length, origin and image shape are different. No Wokwi position entered the renderer.

With the STEP's micro-USB at screen bottom and the antenna at screen top, the manufacturer's Pin Layout figure places 3V3 at the first left contact and GND at the first right contact. The J2 and J3 tables identify these as their respective contact 1. Each row counts towards USB. The CAD's native ordinal increases towards the antenna, so the visual ordinal is `20 - native ordinal`. `Header_0_pin_n` is J2 and `Header_1_pin_n` is J3. The shipped JSON retains the native mesh name for each of the 38 rows. [Pinned pinout figure](https://github.com/espressif/esp-dev-kits/blob/da43a78cfdd2a1122047bb5617ca79e09fd687b2/docs/_static/esp32-devkitc/esp32_devkitC_v4_pinlayout.png) · [Pinned guide](https://github.com/espressif/esp-dev-kits/blob/da43a78cfdd2a1122047bb5617ca79e09fd687b2/docs/en/esp32-devkitc/user_guide.rst#header-block)

| Visual source → contact | Visual status | Engineering projection |
| --- | --- | --- |
| `innerscene-v4-nominal-wroom` / `Header_0_pin_15` → `board/J2.5` | VISUAL_MATCHED on the nominal shell | CANONICAL_MAPPING_UNAVAILABLE. The catalog fixture has J2.5 / IO34, but the asset is generic WROOM. |
| Same asset / `Header_1_pin_11` → `board/J3.9` | VISUAL_MATCHED on the nominal shell | CANONICAL_MAPPING_UNAVAILABLE. The catalog fixture has J3.9 / IO18, but the asset is generic WROOM. |
| Same asset / all other rows in `src/assets/devkitc-v4.json` | VISUAL_MATCHED on the nominal shell | CANONICAL_MAPPING_UNAVAILABLE. |
| Exact `ESP32-DevKitC-32E` assembled-module fit | VISUAL_UNRESOLVED | No projection table admitted. |
| Wokwi Elements generic HC-SR04 / VCC, TRIG, ECHO, GND | VISUAL_MATCHED via mounted pinInfo | CANONICAL_MAPPING_UNAVAILABLE. Renderer does not identify Adafruit retail SKU 3942. |
| Wokwi Elements LED / A, C and resistor / 1, 2 | VISUAL_MATCHED via mounted pinInfo | CANONICAL_MAPPING_UNAVAILABLE. |

The existing catalog is `sha256:356732040b6bd762e8c604ae63c3600df5da225cc938af6dff688b25aad4c57b`. Its board definition `esp32-devkitc-32e-v4` has ten contacts: J2.1, J2.5, J2.14, J2.19, J3.1, J3.7, J3.8, J3.9, J3.14 and J3.19. Its sensor definition `adafruit-3942-profile` has Vcc, Trig, Echo and Gnd. These records stay read-only. No use of the documented flash, strap or power labels generates a capability verdict. [Reviewed catalog](../../data/gpio/devkitc_32e_catalog.json) · [Source and rule ledger](../../reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md)

## Coordinate system

- `project-cad.py` projects the reviewed STEP meshes onto 29 × 51 mm at 20 raster pixels/mm. Screen y reverses model y. Coordinate offsets are 0.53 mm in x and 49 mm in y. The raster SHA-256 is `9efc931ec7ba77f772ff381334eb9ca009b38076a4793805ce9eb47a35058896`. The LF-normalized contact JSON SHA-256 is `fae65c6a77d2e6c7ffceab8fa3effe87a20c93e6af5e9cdbdd6aeda71dedad23`. Browser verification checks both digests and the decoded raster dimensions before exposing board handles.
- Each installed Wokwi element is read after Lit update. Its native `pinInfo` coordinates are in SVG CSS pixels. The local transforms scale the element and its pin list together. The observer catches element size, attribute and shadow subtree changes. On invalid geometry, handles disappear and affected wires hide until the geometry recovers. The React Flow node internals update after the handle list changes.
- Handles and paths share React Flow's translated and zoomed transform. Pointer coordinates and measured DOM rectangles are client CSS pixels. Pan, scroll and browser zoom affect both in the same transform. A browser's device pixel ratio affects rasterization. Rotation is unsupported and the strict import schema rejects extra transform fields.
- Hit boxes are 11 local CSS pixels wide. Board contacts are roughly 13.14 local CSS pixels apart longitudinally. A focusable inspector locator centers the selected contact and zooms to at least 1×. The custom edge shifts the React Flow left-side endpoint to the center of each hit box.

## Mechanical and electrical scope

No CAD-to-real-board tolerance is claimed. The on-screen alignment measurements compare handles to the displayed artwork and paths. The rendering omits fine details such as exact Espressif silkscreen and exact switch/antenna markings. No visual wire is engineering verified.
