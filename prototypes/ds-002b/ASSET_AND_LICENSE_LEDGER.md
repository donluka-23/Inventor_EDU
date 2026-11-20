# DS-002B assets and licenses

Reviewed 2026-11-21 (Asia/Tbilisi). Scope is the isolated, local prototype.

| Artifact | Exact identification and license | Disposition |
| --- | --- | --- |
| Innerscene ESP32 DevKitC V4 Layout | Innerscene Corp., STEP timestamp 2026-10-05T08:17:08, product `esp32_devkitc_v4`. The publisher page and actual STEP header explicitly dedicate it under CC0-1.0 for reuse, modification and redistribution. Source SHA-256 `7d6580aaa58a8d3e4b5bb237e6d2d10f8330891ba063873430379542e0b2ed01`. [Publisher page](https://www.innerscene.com/tools/library/3d-parts/esp32-devkitc-v4-layout-1ab70892) · [CC0 terms](https://creativecommons.org/publicdomain/zero/1.0/) | Admitted for nominal visualization. WROOM-32E variant and exact mechanical fit remain unqualified. Only derived raster and contact-center data shipped. |
| Wokwi Elements sensor, LED and resistor | Uri Shaked / Wokwi Elements contributors, installed npm `@wokwi/elements@1.9.2`, MIT in the package and at inspected upstream commit `5178c0cc1b455719fdf562169293797e29d73dac`. npm integrity `sha512-bommouWNrBl6bQqxi8ZT/Keh1MbGpL7bl2pVf4DxbrngXw3G7iejt5XA2990q9i5tidGoxMYJxoP11Ai6xuQdg==`. [Pinned upstream source and license](https://github.com/wokwi/wokwi-elements/tree/5178c0cc1b455719fdf562169293797e29d73dac) | The renderer modules are imported directly. Installed package notice is retained. The generic HC-SR04 artwork supplies visual contact names, without device-specific retail provenance. |
| Wokwi Boards V4 artwork and JSON | Marc Endtricht, board directory at `962b19d5636756537a93bb5337ac99abd775eae0`. SVG SHA-256 `002cb0eb5e33b926728bd0d3744e1c37830a82fa1f331434080e6f16cbad6763`; JSON SHA-256 `6377990e1317d929ac164570ba5adc0a32ccfaf10d66300526c6a132a2a5f885`. Root LICENSE request returned 404 and the SVG contained no license statement found in the raw file. [Exact source directory](https://github.com/wokwi/wokwi-boards/tree/962b19d5636756537a93bb5337ac99abd775eae0/boards/esp32-devkit-c-v4) | Inspection and comparison only. No artwork, visual geometry, or embedded Wokwi simulator. |
| Espressif KiCad Libraries alternative | Espressif, `footprints/Espressif.pretty/ESP32-DevKitC.kicad_mod` at `d5b68fd9269c639b3a60681e00b91df33b4db4a3`. CC-BY-SA-4.0 with an electronic-design exception. The inspected tree had a footprint and module models, without a matching whole-board STEP. [Footprint source](https://github.com/espressif/kicad-libraries/blob/d5b68fd9269c639b3a60681e00b91df33b4db4a3/footprints/Espressif.pretty/ESP32-DevKitC.kicad_mod) · [License](https://github.com/espressif/kicad-libraries/blob/d5b68fd9269c639b3a60681e00b91df33b4db4a3/LICENSE.md) | No library assets distributed. This candidate did not supply the whole-board renderer. |
| FreeSVG ESP32 DevKitC | FreeSVG attributes entry 197014 to matasoy, published 2022-10-21, marked CC0-1.0. The download endpoint returned an empty SVG response. The published PNG, `1666364456Esp32_devkitc_v4.png`, SHA-256 `8fd43f607a10480f72c5861800c80dcf99771d18f012a27a52aedafae48eb336`, shows 38 contacts and explicitly reads ESP-WROOM-32. [Asset page](https://freesvg.org/esp32-devkitc) · [Inspected preview](https://freesvg.org/img/1666364456Esp32_devkitc_v4.png) | The preview depicts a different module marking from ESP32-WROOM-32E. No FreeSVG assets distributed. |
| Espressif official guide and pinout | Guide S18, `da43a78cfdd2a1122047bb5617ca79e09fd687b2`, raw RST SHA-256 `a6e89080a3a5f9b99f33e63e7a0d9788fa858ad11cd25feffbb9e4df15229f1b`. [Manufacturer guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html) | Source for header order and documented hardware identity. Text and illustrations remain link-only. |

The only component artwork in the browser is the Innerscene STEP derivative and the three Wokwi Elements renderers. System fonts and CSS provide the editor chrome. Screenshots in `evidence/` are generated from this local workspace. The source hierarchy and comparisons are recorded in the [geometry audit](PIN_GEOMETRY_AND_MAPPING_AUDIT.md).

## Tool and notice evidence

- React Flow custom handles, naming and dynamic geometry were checked against its official docs and installed 12.10.0 implementation. [React Flow handles](https://reactflow.dev/learn/customization/handles)
- One-time CAD conversion used `occt-import-js 0.0.23` (npm license field LGPL-2.1, integrity `sha512-RFfYQXYFX5C1mB1Aywm0ShcUKzXOr/VzTnlzhBSDJOR6YCAPt1HYCzeXWg1vwwjn/cUxwqRNhhtf1dlewoZYCQ==`) and Pillow 12.3.0 (MIT-CMU). They were executed locally. No converter code, binaries or transitive dependency were vendored in the application. [Converter source](https://github.com/kovacsv/occt-import-js) · [Pillow license](https://github.com/python-pillow/Pillow/blob/12.3.0/LICENSE)
- `public/THIRD_PARTY_NOTICES.txt` retains the installed runtime package notices and is copied by Vite into builds. Development and platform-specific packages are installed from their registries, with integrity hashes in the lock. The Playwright Chromium executable remains in the local Playwright cache. No `node_modules`, browser binary, or built `dist/` is tracked.
- The npm tarball for `@lit-labs/ssr-dom-shim 1.6.0` has Google LLC BSD-3-Clause source headers and omits a separate LICENSE. Its pinned upstream repository LICENSE has SHA-256 `45d31799d0db956cc3eb5469346abbd9b7025babc5ff29fab10d7095da992ef1`, confirmed byte-identical to the LICENSE shipped with the installed Lit package and retained in the notice bundle. [Pinned Lit license](https://github.com/lit/lit/blob/20afabd3c5bfd49fdcdf1b8518e05c7f99a46db6/LICENSE)

## Locked npm packages

Each entry's full registry URL and integrity hash is in [package-lock.json](package-lock.json).

| Package path | Version | License | Scope |
| --- | --- | --- | --- |
| `node_modules/@emnapi/core` | 2.0.0-beta.2 | MIT | dev optional |
| `node_modules/@emnapi/runtime` | 2.0.0-beta.2 | MIT | dev optional |
| `node_modules/@emnapi/wasi-threads` | 2.2.0 | MIT | dev optional |
| `node_modules/@lit-labs/ssr-dom-shim` | 1.6.0 | BSD-3-Clause | runtime |
| `node_modules/@lit/reactive-element` | 2.1.2 | BSD-3-Clause | runtime |
| `node_modules/@napi-rs/wasm-runtime` | 1.2.6 | MIT | dev optional |
| `node_modules/@oxc-project/types` | 0.156.0 | MIT | dev |
| `node_modules/@playwright/test` | 1.65.1 | Apache-2.0 | dev |
| `node_modules/@rolldown/binding-android-arm-eabi` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-android-arm64` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-darwin-arm64` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-darwin-x64` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-freebsd-x64` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-linux-arm-gnueabihf` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-linux-arm64-gnu` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-linux-arm64-musl` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-linux-ppc64-gnu` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-linux-s390x-gnu` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-linux-x64-gnu` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-linux-x64-musl` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-openharmony-arm64` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-wasm32-wasi` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-win32-arm64-msvc` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/binding-win32-x64-msvc` | 1.2.19 | MIT | dev optional |
| `node_modules/@rolldown/pluginutils` | 1.1.1 | MIT | dev |
| `node_modules/@tybys/wasm-util` | 0.10.5 | MIT | dev optional |
| `node_modules/@types/d3-color` | 3.1.3 | MIT | runtime |
| `node_modules/@types/d3-drag` | 3.0.7 | MIT | runtime |
| `node_modules/@types/d3-interpolate` | 3.0.4 | MIT | runtime |
| `node_modules/@types/d3-selection` | 3.0.12 | MIT | runtime |
| `node_modules/@types/d3-transition` | 3.0.9 | MIT | runtime |
| `node_modules/@types/d3-zoom` | 3.0.9 | MIT | runtime |
| `node_modules/@types/node` | 24.10.1 | MIT | dev |
| `node_modules/@types/react` | 19.2.14 | MIT | runtime |
| `node_modules/@types/react-dom` | 19.2.3 | MIT | dev |
| `node_modules/@types/trusted-types` | 2.0.7 | MIT | runtime |
| `node_modules/@wokwi/elements` | 1.9.2 | MIT | runtime |
| `node_modules/@xyflow/react` | 12.10.0 | MIT | runtime |
| `node_modules/@xyflow/system` | 0.0.74 | MIT | runtime |
| `node_modules/classcat` | 5.0.5 | MIT | runtime |
| `node_modules/csstype` | 3.2.4 | MIT | runtime |
| `node_modules/d3-color` | 3.1.1 | ISC | runtime |
| `node_modules/d3-dispatch` | 3.0.2 | ISC | runtime |
| `node_modules/d3-drag` | 3.0.1 | ISC | runtime |
| `node_modules/d3-ease` | 3.0.2 | BSD-3-Clause | runtime |
| `node_modules/d3-interpolate` | 3.0.2 | ISC | runtime |
| `node_modules/d3-selection` | 3.0.1 | ISC | runtime |
| `node_modules/d3-timer` | 3.0.2 | ISC | runtime |
| `node_modules/d3-transition` | 3.0.2 | ISC | runtime |
| `node_modules/d3-zoom` | 3.0.1 | ISC | runtime |
| `node_modules/detect-libc` | 2.1.2 | Apache-2.0 | dev |
| `node_modules/fdir` | 6.5.0 | MIT | dev |
| `node_modules/fsevents` | 2.3.3 | MIT | dev optional |
| `node_modules/lightningcss` | 1.33.0 | MPL-2.0 | dev |
| `node_modules/lightningcss-android-arm64` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lightningcss-darwin-arm64` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lightningcss-darwin-x64` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lightningcss-freebsd-x64` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lightningcss-linux-arm-gnueabihf` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lightningcss-linux-arm64-gnu` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lightningcss-linux-arm64-musl` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lightningcss-linux-x64-gnu` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lightningcss-linux-x64-musl` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lightningcss-win32-arm64-msvc` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lightningcss-win32-x64-msvc` | 1.33.0 | MPL-2.0 | dev optional |
| `node_modules/lit` | 3.3.3 | BSD-3-Clause | runtime |
| `node_modules/lit-element` | 4.2.2 | BSD-3-Clause | runtime |
| `node_modules/lit-html` | 3.3.3 | BSD-3-Clause | runtime |
| `node_modules/nanoid` | 3.3.20 | MIT | dev |
| `node_modules/picocolors` | 1.1.1 | ISC | dev |
| `node_modules/picomatch` | 4.0.7 | MIT | dev |
| `node_modules/playwright` | 1.65.1 | Apache-2.0 | dev |
| `node_modules/playwright-core` | 1.65.1 | Apache-2.0 | dev |
| `node_modules/postcss` | 8.5.33 | MIT | dev |
| `node_modules/react` | 19.2.4 | MIT | runtime |
| `node_modules/react-dom` | 19.2.4 | MIT | runtime |
| `node_modules/rolldown` | 1.2.19 | MIT | dev |
| `node_modules/scheduler` | 0.27.0 | MIT | runtime |
| `node_modules/source-map-js` | 1.2.4 | BSD-3-Clause | dev |
| `node_modules/tinyglobby` | 0.2.17 | MIT | dev |
| `node_modules/tslib` | 2.9.1 | 0BSD | dev optional |
| `node_modules/typescript` | 5.9.3 | Apache-2.0 | dev |
| `node_modules/undici-types` | 7.16.0 | MIT | dev |
| `node_modules/use-sync-external-store` | 1.7.0 | MIT | runtime |
| `node_modules/vite` | 8.3.8 | MIT | dev |
| `node_modules/zustand` | 4.5.7 | MIT | runtime |
