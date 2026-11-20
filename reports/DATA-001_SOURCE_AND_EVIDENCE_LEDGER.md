# DATA-001 source and evidence ledger

- Review date: 2026-11-20 (Asia/Tbilisi). Scope: internal structural evaluation and manufacturer facts for review. No deployment or engineering-rule approval.
- Research E provenance: the owner's pre-existing untracked canonical Markdown file at `docs/research/raw/RESEARCH_E_COMPONENT_DATA_AND_EVIDENCE_PIPELINE.md`. Its title and sections 2/4/6/8/10/13/15 were checked. Original bytes preserved, SHA-256 `80a935dc06cf2289a8918101110559f5020a1c95d07fb534ba87d9eee6ad97d6`. No upstream URL or independent author attestation for that local research input was supplied.
- Authoritative LibrePCB repository: [LibrePCB-Libraries/LibrePCB_Base.lplib](https://github.com/LibrePCB-Libraries/LibrePCB_Base.lplib), verified by GitHub repository metadata and `git ls-remote --symref ... HEAD`. [Pinned commit dc037a238eb5efcc034dd9d62e5775d5c21e90e4](https://github.com/LibrePCB-Libraries/LibrePCB_Base.lplib/tree/dc037a238eb5efcc034dd9d62e5775d5c21e90e4). Branch name was discovered only to identify this revision. All read artifact URLs use the complete commit.

## LibrePCB artifacts

The three selected structural files are ordinary Git blobs (mode 100644). The GitHub recursive tree was complete and had one license file, the pinned root `LICENSE.txt`. No nested license, notice, copying, copyright or REUSE/DEP5 override was found. The selected files do not declare incompatible terms. The generic package/device records attribute their generation to LibrePCB's parts generator. The selected data does not contain or require generator code, symbol artwork, or referenced 3D asset bytes.

| File relative to pin | SHA-256 of fetched bytes | Evidence |
| --- | --- | --- |
| `LICENSE.txt` | `36ffd9dc085d529a7e60e1276d73ae5a030b020313e6c5408593a6ae2af39673` | Repository CC0 1.0 Universal waiver and fallback |
| `README.md` | `619212a20dd4d83914a890d64dceda8f9d36d764ec91ce49c818c17d6f61ccb3` | The official base library identifies its content as CC0-1.0 and links the root license |
| `.librepcb-lib`, `cmp/ef80cd5e-2689-47ee-8888-31d04fc99174/.librepcb-cmp`, `pkg/5d9abd1b-cf0b-4cf7-8666-20a1add9971e/.librepcb-pkg`, `dev/483a71eb-318e-448e-82ff-f02efc4821aa/.librepcb-dev` | Each `53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3` | Library and element file format 2, literal bytes `2\n` |
| `cmp/ef80cd5e-2689-47ee-8888-31d04fc99174/component.lp` | `8e76dc4bfaf40f56e6856883b4dee5af0f2c368633c3e3c9a7031fcdf1b17b07` | Generic Resistor, element version 0.2, root signal entries. Git blob `b8d32584a1deda738240f9a25dc819a602b3968a`. |
| `pkg/5d9abd1b-cf0b-4cf7-8666-20a1add9971e/package.lp` | `61ee014c8bb7200eaf4c523b044dbc8090d8074c923059cfba46d601c98900c8` | Generic RESC1608 (0603), element version 0.5, root pad names and each footprint's package-pad references. Git blob `b7784bd30eb3572398007c2c161f16a003b3b521`. |
| `dev/483a71eb-318e-448e-82ff-f02efc4821aa/device.lp` | `3c4cce7d485a1260ac5980bb0ad1d5c9c292f384a49a9a920e95912092431a80` | Generic Resistor 1608 (0603), element version 0.3.1, root component/package UUIDs and two pad-to-signal children. No vendor part records. Git blob `370f242f5ef651559a417aa61adadbe09fec9b51`. |

`git hash-object --no-filters` reproduced all three Git blob IDs against the API tree. The [pinned license](https://github.com/LibrePCB-Libraries/LibrePCB_Base.lplib/blob/dc037a238eb5efcc034dd9d62e5775d5c21e90e4/LICENSE.txt) and [official license explanation](https://librepcb.org/license/) state the library rights separately from the application. CC0 covers the affirmer's applicable rights, with a fallback license. It provides no warranty and does not waive patents or trademarks or clear third-party rights. The task permits this bounded internal evaluation. Only independently authored normalized records and factual identifiers are published on the task branch; no raw library file, application source, symbol, artwork or PDF is bundled. Pinning the license alongside the data prevents silent intake after an upstream change. Broader ingestion or distribution review remains an owner decision.

| Pad label | Canonical terminal ID (original package-pad UUID) | Component signal UUID from device join |
| --- | --- | --- |
| 1 | `ad768910-1573-409f-81d4-d4c7692ab494` | `3452d36e-1ce8-4b7c-8e5b-90c2e4929ed8` |
| 2 | `65ab6c75-b264-4fed-b445-d3d98c956008` | `ad623f98-9e73-49c3-9404-f7cfa99d17cd` |

The root package pads, both footprints and the two device rows agree on the same two package-pad identities. Neither footprint exposed any extra, hidden or unlinked pad. Both component signals are required, passive and have no forced net. All joins are one-to-one. The three-way pad/signal relationship is recorded as derived candidate evidence, not promoted to an externally trusted signal mapping. The source's no-parts marker and absence of part records mean there is no exact YAGEO join. The library's empty generic resistance attribute supplies no default.

Catalog `1.1`, definition `librepcb-483a71eb-318e-448e-82ff-f02efc4821aa`, definition digest `sha256:0b17c8ec095f5c1f843353277917a7a88cf95e8b4277bc5b7874d272b4865ae3`, catalog digest `sha256:1d0094e60730c9daea083fcf63170e24cef90bd27d22af789cab628064002057`, canonical file SHA-256 `891405396e2e8e2210ca4847cc11d2488354647dee8f451f42e5e1e88f602558`. These are integrity references, not trusted deployment pins.

## YAGEO evidence kept outside the catalog

The [exact MPN sheet](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-0710KL) returned a one-page PDF. The retrieved bytes had SHA-256 `1c105e7b4dd7b447e996030d423850cb19acf219f05bb8ffbe38a6934d0eddbc` and footer **Generated 2026-11-20**. The web preview showed November 19, and Research E cites December 23, 2025. Those are different observed editions of a dynamic endpoint. This ledger pins the locally inspected bytes. A later download with a different hash requires review rather than silently replacing the evidence. The [series specification](https://yageogroup.com/content/datasheet/asset/file/PYU-RC_GROUP_51_ROHS_L) was **2025-11-14 V.14**, 11 pages, SHA-256 `7b6f0ae72708ca4b38126f84b5407a3e970a94cb60bc1a0afdaeb25a23d839bb`.

| Fact | Source locator and conditions |
| --- | --- |
| Exact orderable `RC0603FR-0710KL`, YAGEO RC thick-film SMD chip, 0603 EIA / 1608 metric | Part sheet p. 1 heading and General Information. Series document p. 2 order-code table distinguishes standard power and higher-power options. |
| Two end terminations, nominal body 1.6 mm by 0.8 mm | Part sheet p. 1 Dimensions, including B1 and B2. Series p. 4 Construction and Fig. 9. This supports two physical contacts and dimensional class, but no exact LibrePCB UUID, pin numbering or land-pattern approval. |
| 10,000 Ω nominal, ±1% | Part sheet p. 1 Specifications, Resistance and Resistance Tolerance. |
| 0.1 W at 70 °C ambient | Part sheet p. 1 Specifications, Power. Series p. 5 Table 2 and p. 7 Power Rating. |
| 75 V DC ceiling in the full-rated-power row | Part sheet p. 1 Specifications, Voltage DC. Series p. 7 Rated Voltage further limits continuous voltage to the lesser of the working voltage ceiling and the voltage corresponding to resistance and rated power. No unconditional 75 V rating or circuit calculation is claimed. |
| Derating above 70 °C | Series p. 7 Fig. 10-1 covers RC0603 family range: full rated power through 70 °C and falling to zero at 155 °C. No assembly-specific thermal model supplied or admitted. |

The sheet carries a copyright and application-suitability disclaimer. No redistribution grant for either PDF, illustrations or manufacturer 3D models was established. Only URLs, source metadata and independently expressed facts are retained. A second qualified engineer and an exact footprint/contact match are pending. The machine-readable candidate is `data/pilot/yageo_rc0603fr_0710kl_candidate.json`, with `catalog_admission: HOLD`, null LibrePCB device match and null admitted electrical limits. The importer never reads it.

## Exact replay

Use the existing CPython 3.12 Windows x64 environment and hash-pinned project requirements. Run from the repository root. The following downloads only the nine LibrePCB artifacts into a local temporary directory, then validates and parses the same files offline. The YAGEO evidence is intentionally outside the import path. Acquire a fresh YAGEO sheet only for review and compare its bytes and edition to the recorded evidence.

```powershell
$exe = 'PATH_TO_EXISTING_CORE_001A_ENV/Scripts/python.exe'
$sourceDir = Join-Path $env:TEMP 'InventorEDU-DATA-001-dc037a238eb5efcc034dd9d62e5775d5c21e90e4'
$base = 'https://raw.githubusercontent.com/LibrePCB-Libraries/LibrePCB_Base.lplib/dc037a238eb5efcc034dd9d62e5775d5c21e90e4/'
$paths = & $exe -B -c 'from inventor_edu.librepcb_pilot import PINNED_FILES; print("\n".join(p for p, _ in PINNED_FILES))'
if ($LASTEXITCODE -ne 0) { throw 'Could not enumerate pinned paths' }
foreach ($relative in $paths) {
    $local = Join-Path $sourceDir $relative
    New-Item -ItemType Directory -Path (Split-Path $local) -Force | Out-Null
    Invoke-WebRequest -UseBasicParsing "$base$relative" -OutFile $local
}
$env:INVENTOR_EDU_DATA001_SOURCE_DIR = $sourceDir
$env:HYPOTHESIS_STORAGE_DIRECTORY = Join-Path $env:TEMP 'inventor-edu-data001-hypothesis'
& $exe -B -m inventor_edu.librepcb_pilot $sourceDir --output (Join-Path $sourceDir 'candidate.json')
if ($LASTEXITCODE -ne 0) { throw 'Import did not pass' }
& $exe -B -m unittest discover -v
```

LibrePCB CLI was unavailable and was not installed. The file format reference documents S-expressions and major versioning. This reader implements only the selected nested subset and only admits the reviewed pin. It does not validate irrelevant artwork, symbolic variants or full footprint geometry. [LibrePCB file format](https://librepcb.org/features/file-format/)
