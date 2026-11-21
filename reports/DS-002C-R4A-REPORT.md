# Execution report — DS-002C-R4A Rev 1.0

- Date — 2026-11-21, Asia/Tbilisi
- Plan — [frozen handoff](../tasks/DS-002C-R4A.md)
- Outcome — **BLOCKED / OWNER_DECISION_REQUIRED**. Adom's GLB is downloadable and the package carries a CC BY-SA 4.0 label. The rights review could not establish that the grant covers the manufacturer artwork Adom says it reproduced from Espressif's externally hosted PCB layout plot. The source-rights gate stopped rendering, integration, and screenshot production.
- Engineering base — `codex/ds-002b-r3-exact-hardware-visual` at `78168099a649887dfd8f874d7953fff9428fe76c`
- Task branch — `codex/ds-002c-r4a-external-32e-candidate`

## A. Preflight

Read `AGENTS.md`, `docs/PRODUCT.md`, `docs/DECISION_AUTHORITY.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `tasks/NEXT.md`, `docs/SESSION_PROTOCOL.md`, `docs/VERIFICATION_POLICY.md`, `docs/OSS_POLICY.md`, `governance/OSS_REGISTER.csv`, `docs/adr/ADR-0001-product-scope.md`, and `reports/REPORT_TEMPLATE.md`. Read the R3 handoff and report, R2 report, and the asset ledger, pin audit, `DeviceNode.tsx`, `model.ts`, `Workspace.tsx`, and `canvas.spec.ts` under `prototypes/ds-002b/`. Read the available `docs/research/raw/INVENTOR_EDU_SCREEN_ARCHITECTURE_PHASE_PLAN.md` v0.2 as context. Applied the OSS intake, evidence-gated engineering and Firecrawl skills.

The local and live R3 refs matched the pinned base, and no existing local or live R4A branch was present. The tracked working tree and index were clean. Created the R4A branch directly at the R3 commit. The untracked UX-08-R2 audit archive and screen architecture plan were preserved outside staging. ADR-0001 applies, ADR-0002 remains proposed/on hold, and ADR-0003 and ADR-0004 remain undecided.

## B. Source acquisition and revision

Downloaded the selected source into a temporary inspection directory outside the repository. The publisher identifies the package as `adom/esp32-devkitc`, ID `pg_4ebcczwyjc`, version `0.2.0`. The GLB file page lists the `Publish 0.2.0` commit `51763cce5bbc24369fdb3a879b9a56b5ea34cfc6` and the frozen `aa0351d279c7.b1` download URL. The footprint file page identifies its current file commit as `ff6bf07adfec243062c01558f8fc34a31933177a`, a datasheet-property update per the file list. The advertised GLB and current footprint are identified separately below. The footprint hash is for the current advertised byte stream and was not attributed to the GLB's release commit. [Adom component](https://wiki.adom.inc/adom/esp32-devkitc) · [Release commit](https://wiki.adom.inc/adom/esp32-devkitc/commit/51763cce5bbc24369fdb3a879b9a56b5ea34cfc6) · [GLB file page](https://wiki.adom.inc/adom/esp32-devkitc/files/esp32-devkitc.glb) · [Footprint file page](https://wiki.adom.inc/adom/esp32-devkitc/files/esp32-devkitc.kicad_mod)

| Retrieved source | SHA-256 | Observed |
| --- | --- | --- |
| [GLB, final resolved URL](https://wiki.adom.inc/api/pages/adom/esp32-devkitc/files/esp32-devkitc.glb?v=aa0351d279c7.b1) | `e966fe390c9260bd19b1dd0f9bea54b43819b328be964394343b001e46decdce` | HTTP 200, 2,884,924 bytes. |
| [KiCad footprint](https://wiki.adom.inc/api/pages/adom/esp32-devkitc/files/esp32-devkitc.kicad_mod?v=aa0351d279c7.b1) | `f46b2f3eb8d5fb4b4c8b8160bdfaa838e4ed20ba81c751efe08a0c5026cb367f` | HTTP 200, 6,666 bytes. |
| [Package manifest](https://wiki.adom.inc/api/pages/adom/esp32-devkitc/files/package.json?v=aa0351d279c7.b1) | `493c3cbcb366373c793baa28a0771ba48490894f63e7d9afa87373d6a3088d56` | HTTP 200, version 0.2.0 and MPN `ESP32-DEVKITC-32E`. |
| [Publisher README](https://wiki.adom.inc/api/pages/adom/esp32-devkitc/files/README.md?v=aa0351d279c7.b1) | `833d4447374610bbce5e92b32ce40c95637688627202a20b755ee294fa6dc89a` | HTTP 200. Records both source derivation and mechanical assumptions. |
| [Pinned Espressif guide](https://raw.githubusercontent.com/espressif/esp-dev-kits/da43a78cfdd2a1122047bb5617ca79e09fd687b2/docs/en/esp32-devkitc/user_guide.rst) | `a6e89080a3a5f9b99f33e63e7a0d9788fa858ad11cd25feffbb9e4df15229f1b` | Official J2/J3 tables and 32E assembly listing. |
| [Espressif layout plot cited by Adom](https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_pcb_layout.pdf) | `ae7473227cb26713534e70f311ad33b6c7b0a3a250bc2d99d31328456a7c967c` | HTTP 200, six pages, 745,906 bytes. |

A non-rendering binary inspection confirmed magic `glTF`, version 2, declared length 2,884,924, a 2,169,540-byte JSON chunk and a 715,356-byte BIN chunk. The JSON contains one scene, 859 nodes, 756 meshes, 30 materials, no image textures, and `KHR_mesh_quantization`. Named geometry references WROOM-32E, and the assembly declares J1, J2, J3, SW1 and SW2 nodes. This was a container and metadata check. GLTFLoader rendering and projected geometry were gated off.

## C. Rights and exact stop condition

**Adom's published license was verified.** The component page identifies Adom as publisher and says CC BY-SA 4.0. The README names Espressif's KiCad WROOM-32E model and official KiCad library components as upstream contributions. Both upstream libraries publish CC BY-SA 4.0 with electronic-design exceptions. The exceptions were not relied on to waive obligations for a republished visualization. [Adom component](https://wiki.adom.inc/adom/esp32-devkitc) · [Espressif KiCad library license](https://github.com/espressif/kicad-libraries/blob/d5b68fd9269c639b3a60681e00b91df33b4db4a3/LICENSE.md) · [KiCad libraries license](https://www.kicad.org/libraries/license/)

**The specific missing link is Espressif's reproduced PCB artwork.** Adom states that it rebuilt the board using the manufacturer's PCB layout plot, including the original silkscreen. The pinned Espressif guide links to the plot at `dl.espressif.com`. The exact PDF is absent from the non-truncated tree of the licensed `esp-dev-kits` repository. The repository README applies CC BY-SA to documentation in that repository. The plot had no license statement in extracted page text or metadata. Espressif's documentation disclaimer provides no express or implied IP grant of its own. The reference-design resource URL resolved to HTML; the tested direct and API paths returned a 404 or JSON, without an archive or license. No source reviewed established that Adom had authority to relicense the reproduced artwork, or that Espressif granted reuse of the plot artwork for the candidate render. This is an unresolved provenance finding under the frozen gate. [Adom derivation](https://wiki.adom.inc/adom/esp32-devkitc/files/README.md) · [Espressif repository licensing](https://github.com/espressif/esp-dev-kits/blob/da43a78cfdd2a1122047bb5617ca79e09fd687b2/README.md#open-source-licensing) · [Espressif disclaimer](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/disclaimer-and-copyright.html) · [Espressif reference design listing](https://www.espressif.com/en/products/devkits/esp32-devkitc-googlecloud-iot/resources)

If the rights holder confirms scope for this artwork, the disposition to review is asset-level attribution to Adom and the identified upstream contributors, retention of notices and links, clear labeling of the orthographic conversion and any modifications, and compatible ShareAlike terms for any shared adaptation. CC BY-SA extends only to rights the licensor has authority to grant and excludes trademark rights. No candidate license was applied to a distributed project file. [CC BY-SA 4.0 legal code](https://creativecommons.org/licenses/by-sa/4.0/legalcode) · [Project OSS policy](../docs/OSS_POLICY.md)

## D. Identity and nominal geometry

**IDENTITY_CONTRADICTION / PHYSICAL_DETAIL_NOT_METROLOGICALLY_VERIFIED.** Adom's package MPN and named module geometry indicate 32E, while its README calls the board orderable as 32D. The manufacturer's 32E listing identifies ESP32-WROOM-32E. The README also documents assumed header drill, switch height and USB jack modeling details. The contradiction remains open, as expected by this handoff. No exact assembly approval or pixel calibration was issued.

The pinned manufacturer's table names matched all 38 Adom package contact labels. Independent footprint parsing found 19 distinct positions on each row, 38 unique coordinates, and constant 2.54 mm adjacent pitch. In the footprint's mm coordinate system, J2 is at x = −12.70 and J3 at x = +12.70. Each row runs from y = −22.86 at ordinal 1 to y = +22.86 at ordinal 19. Each ordinal `n` advances by `2.54 × (n − 1)` mm from contact 1. The manufacturer numbers both rows from the antenna end. `J2.8` is `IO33` at `(−12.70, −5.08) mm`. Ground contacts retain distinct IDs `J2.14`, `J3.1`, and `J3.7`. The source-rights stop left model-to-raster orientation, projected coordinates, holdouts, pixel residuals, and visual click qualification untested.

## E. Commands and actual results

Commands ran from `D:/Inventor_EDU`. Source bytes were inspected in `%TEMP%/InventorEDU-DS002C-R4A`.

| Command or check | Result |
| --- | --- |
| `git fetch --prune origin`, `git ls-remote --heads origin` for R3, R4A, UX08-T02A and main, and `git show-ref` | Exit 0. Verified R3 and absence of an existing R4A branch before switching from the clean tracked worktree. |
| `curl.exe -sSL --max-time … <source URL> -o <temporary file> -w …` | Adom landing and files pages, exact GLB, footprint, manifest and README reached HTTP 200. Pinned Espressif guide and official plot were acquired. The final resolved GLB URL retained `v=aa0351d279c7.b1`. |
| `python -B -` on the temporary GLB, KiCad and manufacturer files | Exit 0. Checked container/version/chunks, file hashes, 38 pin labels and pad coordinates, 2.54 mm pitch and three separate GND locators. PDF inspection reported 6 pages and 0 license or copyright notice matches in extracted text. |
| `npm view three@0.187.0 version license dist.integrity --json` | Exit 0. Reported `0.187.0`, `MIT`, and `sha512-Qiu7R+Cmh8CstZsY1uJOSWnVlfo7ZtNLV7mF8Jltk3LB3AtDu9cRZlcnRKkAk8Y4z6KKw35z7Y7Urd7jWY8etA==`. No installation occurred. |
| `npm run typecheck`, `npm run build`, `npm test`, `npm run test:e2e` | NOT_RUN. The handoff makes these conditional on implementation code. The asset gate stopped before code and artwork changes. |

## F. Acceptance and screenshot evidence

| ID | Result | Observed |
| --- | --- | --- |
| A01 SOURCE | BLOCKED | Acquired and pinned actual files. Adom license verified, with rights for reproduced Espressif plot artwork unresolved. |
| A02 IDENTITY | PARTIAL | Source supports evaluation of a 32E candidate. 32D prose and unmeasured details remain unresolved. |
| A03 GEOMETRY | PARTIAL | Verified 38 nominal pad coordinates and manufacturer labels. Full rendered geometry and visual mapping remained gated. |
| A04 ART | NOT_RUN | No raster or browser asset was produced after the rights stop. |
| A05 INTERACTION | NOT_RUN | Chromium implementation tests required a runnable candidate. |
| A06 QUALITY | NOT_RUN | No new 1440×900, 1024×768, 1×, 2×, or comparison capture exists. Owner visual acceptance remains pending. |
| A07 GOVERNANCE | PASS for blocked checkpoint scope | Work was confined to the authorized Markdown checkpoint. Publication verification is recorded separately. |

## G–J. Manifest, limits, OSS, and owner review

| Path | Change |
| --- | --- |
| `tasks/DS-002C-R4A.md` | Added verbatim frozen handoff. |
| `reports/DS-002C-R4A-REPORT.md` | Added source, rights, geometry and blocked execution evidence. |

OSS additions — `NONE`. The candidate bytes stayed in the temporary inspection directory. There was no change to the prototype, its dependencies, editor interactions, Wokwi Elements, or canonical engineering files. The checkpoint can be set aside by returning to the pinned R3 branch.

**Owner decision required.** Provide file-specific confirmation covering the Espressif PCB artwork embodied in the pinned Adom GLB and its planned evaluation render and Git redistribution, or supply an owner-authorized amendment that resolves that scope. Once verified, the orthographic render and 38-contact pixel correspondence would still need execution and owner visual review.
