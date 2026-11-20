# DS-002B revision 2

An isolated visual electronics workspace. The board is the Innerscene nominal ESP32-DevKitC V4 shell with 38 separately selectable contact positions. Exact ESP32-WROOM-32E fit and canonical terminal binding remain pending. The sensor, LED, and resistor are mounted Wokwi Elements.

## Run

From `prototypes/ds-002b/` with Node 24 and npm 11.

```sh
npm ci
npm run dev -- --host 127.0.0.1
```

Open the loopback URL printed by Vite. The running workspace needs no external services. Package and Chromium setup may need internet access.

```sh
npm run typecheck
npm run build
npm run test
npx playwright install chromium
npm run test:e2e
```

With an already installed compatible Chromium, set `DS002B_CHROMIUM` to the full executable path instead of installing a browser. The Playwright server uses loopback port 4173. Browser evidence is written to `evidence/`.

## Edit a visual workspace

- Press or click a contact to start, then choose another contact to make a wire. A self-connection or a duplicate unordered endpoint pair is rejected. Esc cancels the draft. Both contacts remain selectable after an invalid attempt.
- Select a wire in the inspector or on the canvas. Rewire destination keeps the wire ID and its first contact. Delete removes the selected wire. Undo and redo affect wire edits.
- Drag a part by its artwork or label. Drag open canvas to pan. Use wheel, zoom buttons or Fit view to reframe.
- Tab through pins and use Enter or Space to choose them. The contact selector and Focus button also center and focus a named physical contact. Ctrl+Z undoes and Ctrl+Shift+Z redoes.
- Open Visual workspace JSON and use Export. Copy the text to save it. To restore, paste the JSON and choose Import. The exchange preserves the four instance positions and exact visual endpoints. Asset revisions are mandatory, and visual-only data cannot be imported as a CORE snapshot.

## Reproduce the board asset

Download the STEP from the [Innerscene source](https://www.innerscene.com/tools/library/3d-parts/esp32-devkitc-v4-layout-1ab70892) and compare its digest with the [asset ledger](ASSET_AND_LICENSE_LEDGER.md). Run the converter from a separate tooling directory with `occt-import-js@0.0.23`. Use Python with Pillow 12.3.0 for the projection. The prototype's npm install does not include the converter.

```sh
node tools/project-step.cjs path/to/source.step path/to/mesh.json path/to/converter/node_modules/occt-import-js
python tools/project-cad.py path/to/source.step path/to/mesh.json src/assets
python tools/inventory-licenses.py
```

See the [pin geometry and mapping audit](PIN_GEOMETRY_AND_MAPPING_AUDIT.md), [dependency and asset ledger](ASSET_AND_LICENSE_LEDGER.md) and [execution report](../../reports/DS-002B-REV2-REPORT.md).
