# RESEARCH I — კომპონენტების მტკიცებულებაზე დაფუძნებული აღმოჩენა, ფუნქციური შესაბამისობა და საგანმანათლებლო ცოდნა

**პროექტი:** INVENTOR EDU  
**თარიღი:** 2026-11-20, Asia/Tbilisi  
**სტატუსი:** დამოუკიდებელი კვლევა და გადაწყვეტილების წინადადება — **არ არის** არქიტექტურის ცვლილების, პროგრამირების ან Codex-ის დავალების ნებართვა  
**საძიებო გადაწყვეტილება:** **SELECT B (ვიწრო სტრუქტურული იმპორტი + ხელით საინჟინრო მიღება); PILOT C მხოლოდ აღმოჩენისთვის; HOLD მულტიკომპონენტიან ავტომატურ სინთეზზე**  
**რეპოზიტორიის შემოწმების ობიექტი:** [`donluka-23/Inventor_EDU`](https://github.com/donluka-23/Inventor_EDU), commit [`2ece740bb49dfd330cbdecd4981204eb085821dd`](https://github.com/donluka-23/Inventor_EDU/tree/2ece740bb49dfd330cbdecd4981204eb085821dd), branch `codex/demo-001-scenario-bridge`  
**მასალის კლასები:** **[R]** რეპოზიტორიაში წაკითხული კოდი/ანგარიში; **[P]** პირველწყაროში დადასტურებული ფაქტი; **[E]** Research E-დან გადმოტანილი შეფასება; **[D]** ამ კვლევის დიზაინერული რეკომენდაცია; **[U]** დაუდასტურებელი ან დაკარგული ინფორმაცია; **[T]** სინთეზური სატესტო მონაცემი.

> **კრიტიკული შეზღუდვა:** კომპონენტის პოვნა ≠ მისი სწორი ფიზიკური იდენტიფიკაცია ≠ კონკრეტული პინის ფუნქციური დასაშვებობა ≠ კომბინირებული სქემის ელექტრული უსაფრთხოება ≠ firmware-ის მუშაობა. ყოველი საფეხური დამოუკიდებელი მტკიცებულებისა და ანგარიშის მფლობელია.

## 1. Executive summary — გადაწყვეტილება

**[D]** საუკეთესო პირველი არქიტექტურა არის *read-only Component Discovery & Matching* ფენა, რომელიც ქმნის აპლიკაციის დონეზე მცირე, ტიპიზებულ **capability index**-ს და **admission ledger**-ს; არ ცვლის `CORE-001A`-ის canonical `DeviceDefinition`/`TerminalRef`/`CircuitSnapshot`-ს, არ წერს მეორე GPIO-verifier-ს და არ ასკვნის უცნობ ელექტრულ ლიმიტებს. მისგან მიღებული `ComponentCandidate` არის *წინადადება შესამოწმებლად*, არა „უსაფრთხო კომპონენტი“.

**გამოყენების სამფაზიანი კონტროლი:**

1. **Discovery:** დასაშვები ლიცენზიის მქონე სტრუქტურული წყაროებიდან ან ტექსტური აღწერებიდან კომპონენტების აღმოჩენა; დაუდასტურებელი candidate რჩება საძიებო ინდექსში.
2. **Engineering admission:** მწარმოებლის exact scope-ის, წყაროს locator-ის, მოცულობის/ერთეულის/პირობის და დამოუკიდებელი review-ს შემდეგ მხოლოდ შესაბამისი ვიწრო claim შეიძლება გადავიდეს `ENGINEERING_ADMITTED` მდგომარეობაში. CORE-ის არსებული კატალოგური admission და GPIO ფაქტების ცალკე ვალიდაციაც კვლავ სავალდებულოა.
3. **Educational enrichment:** უკვე მიღებული ფაქტისა და რეალური verifier finding-ის ახსნა ქართულად, ზუსტი `reason_code`-ით, მოქმედების შემდეგი ნაბიჯით და გაურკვევლობის ღია აღნიშვნით. განმარტების ფენას არ შეუძლია finding-ის შეცვლა.

**[R] რეალურად არსებული საფუძველი:** `inventor_edu/models.py`, `core.py`, `gpio_facts.py`, `gpio_verify.py`, `librepcb_pilot.py`, `demo_bridge.py`; `data/gpio/*`, `data/pilot/*` და `reports/CORE-001A-R2-REPORT.md`, `CORE-001B-01-REPORT.md`, `DATA-001-REPORT.md`, `DEMO-001-REPORT.md`. DEMO-001-ის ანგარიშში აღწერილია **54 გავლილი ტესტი** (44 წინამორბედი + 10 ახალი); ეს არის **შემსრულებლის ანგარიშში დაფიქსირებული შედეგი**, ამ კვლევას ტესტები დამოუკიდებლად **არ გაუშვია**. ამჟამინდელი DEMO headless GPIO bridge-ია, არა ინტერაქტიული სქემა და არა ელექტრული verifier [R01–R07].

**მთავარი გადაწყვეტილების გეითები:** `exact identity`, `rights`, `hard-constraint evidence`, `independent verifier`, `revision pin`, `hint provenance`. ამ ექვსიდან რომელიმე აუცილებელი ელემენტის უქონლობა იძლევა `UNKNOWN/NEEDS_REVIEW`-ს, და არა ავტომატურ თავსებადობას.

## 2. არსებული CORE/DATA/DEMO კონტრაქტების ფაქტობრივი მდგომარეობა

| მოდული / წყარო | უკვე არსებული და გადამოწმებული კონტრაქტი | არ არსებობს / რისი პრეტენზია არ შეიძლება |
|---|---|---|
| `models.py`, `core.py` | `DeviceIdentity` (manufacturer status, SKU, revision status, scope, synthetic flag), `SourceDocument`, `EvidenceClaim`, `TerminalDefinition`, typed `SignalMapping`, `DeviceDefinition`, `CatalogSnapshot`, `ComponentInstance`, `TerminalRef`, `Conductor`, `CircuitSnapshot`, `TopologyResult`; pinned digests, canonical JSON და ზუსტი terminal→net | უნივერსალური შემადგენელი ნაწილის ანალოგიის ძრავი; თვითნებური numeric electrical inference; voltage checker |
| R2 / `models.py` | `CatalogVersion` 1.1, `SignalMapping` target `soc_gpio / power_domain / signal / unknown`, წყაროს/claim-ის იდენტიფიკატორები, verified/unknown mapping | label-ის მიხედვით იდენტობის მტკიცება; ავტომატური package pad→exact MPN join |
| `gpio_facts.py` | ცალკე `GpioFactSet`, `HardwareScope`, source/fact digest, mapping/silicon/resource/strap ფაქტები და conflict/review ველები | generic voltage-/I2C-/LED-compatibility rule set |
| `gpio_verify.py` | `GpioRequirement`, `GpioVerificationReport`, `GpioFinding`, `GpioCoverage`; `PASS/FAIL/UNKNOWN/NOT_APPLICABLE`; `PIN_MAPPING`, `PHYSICAL_CAPABILITY`, `BOARD_AVAILABILITY`, `INTERNAL_PULLUP_CAPABILITY`, `BOOT_STRAP_CONTEXT`, `ACTIVE_CONFIGURATION`; რეალური `finding_id/reason_code/snapshot_digest` | არ იღებს „ნებისმიერ GPIO-ს თავისუფალია“ ვარაუდს; `ACTIVE_CONFIGURATION` ძირითადად `UNKNOWN`-ის კონტრაქტს ასრულებს |
| DATA-001 | CC0 LibrePCB Base-ის პინირებულ generic 0603 resistor `component.lp`+`package.lp`+`device.lp` სტრუქტურული იმპორტი; ორი package pad და ორი signal-ის join; sample catalog 1.1 | **არ** არსებობს დამტკიცებული კავშირი generic 0603-სა და `YAGEO RC0603FR-0710KL`-ს შორის; არც კონკრეტული 10 kΩ ელექტრული მახასიათებელი generic catalog-ში |
| DEMO-001 | exact-profile HC-SR04 Trig/Echo ↔ ESP32 board wire/net matching და არსებული GPIO verifier-ის გამოძახება; `DemoWiringReport` | bridge hardcoded კონკრეტულ demo პროფილებზე — **არ ვაცხადებთ** general-purpose synthesizer-ად; voltage, LED, firmware **არ მოწმდება** |

**კონტრაქტული შეზღუდვა:** `EvidenceClaim.value` ამ ვერსიაში ზოგადი არათავსებადი რიცხვითი interval-სტრუქტურა არ არის; მასში arbitrary nested JSON/float დიაპაზონების ძალით ჩატენვა შეცდომაა. Engineering limit-ების structured interval-ები თავდაპირველად ცალკე versioned **sidecar**-ში რჩება, evidence claim-ებზე რეფერენციით. CORE-ის ცვლილება დასაშვებია მხოლოდ კონკრეტულად ნაჩვენები, ცალკე დამტკიცებული შეუთავსებლობის შემდეგ [R01].

**`CORE-001C`/Research C:** voltage compatibility შესწავლილია როგორც მომავალი დამოუკიდებელი გამოთვლითი საზღვარი; შემოწმებულ reference commit-ზე მისი დასრულებული, მწარმოებლით მხარდაჭერილი აპლიკაცია **არ დასტურდება**. იგივე ეხება H/J/L research შედეგების მომავალ ინტეგრაციებს. `RESEARCH H` ხელმისაწვდომია როგორც მოთხოვნების **დავალება**, არა აუცილებლად დასრულებული და მოწონებული განხორციელების სქემა [U].

## 3. Research E-ის ხელახალი გამოყენება და ახალი ამოცანის საზღვარი

Research E-ის განმეორება არ არის საჭირო. მისგან უცვლელად ვიღებთ [E01]:

- **CC0 official LibrePCB structure → exact, reviewer-curated manufacturer fact → existing CORE/GPIO boundary**;
- manufacturer PDF/diagram-ის არალიცენზირებული კოპირების, bulk scraping-ის, KiCad CC BY-SA library collection-ის უფლებების და Wokwi proprietary dependency-ის **ცალკე განხილვის** ვალდებულებას;
- საკითხებს `VIH/VIL/VOH/VOL`, absolute vs recommended bounds, `VCCA/VCCB`, firmware/operating mode და board/silicon revision scope;
- cost-ranges როგორც **შეფასებებს**, არა გაკეთებული ტაიმინგ-ექსპერიმენტების შედეგებს;
- დამატებით acceptance fixture-ებს Raspberry Pi Pico R3, TI level translator, YAGEO resistor.

**აქ ახალი კვლევითი წვლილია:** `RequiredCapabilityQuery` → typed retrieval, evidence-aware join, exact candidate identity gate, HARD/UNKNOWN semantics, rank without safety laundering, source→rule→hint impact graph, 16 test oracle და Georgian component-knowledge context. Research G-ის თვალსაზრისით, editor-ის visible label მხოლოდ ვიზუალურია, physical terminal key — engineering truth [E02].

**Research E-ის შემდეგ მიღებული ფაქტობრივი განახლება:** DATA-001-მა უკვე დააპინა LibrePCB Base-ის კონკრეტული commit `dc037a238eb5efcc034dd9d62e5775d5c21e90e4`, შემოიტანა generic resistor, მაგრამ **განზრახ არ მოახდინა** YAGEO-ის ელექტრული ფაქტების დაკავშირება [R05]. Research E-ს ძველი გამონათქვამი „კონკრეტული commit ჯერ არ არის“ ამ კონკრეტულ DATA-001 subset-ზე **აღარ მოქმედებს**. სხვა family-სა და vendor-ს ეს pin არ ფარავს.

## 4. კომპონენტის იდენტობის და შესაძლებლობის იერარქია

`Generic family` → `publisher/vendor listing` → `manufacturer exact MPN (+ package/orderable suffix)` → `board assembly/PCB revision` → `module/silicon variant/revision` → `physical connector/position/package pad` → `logical signal/function/peripheral` → `firmware/operating mode` → `electrical bound with conditions` → `source-reviewed claim` → `engineering verifier` → `educational hint`.

ეს არ არის ერთი `is-a` ხე: **რამდენიმე orthogonal graph edge** საჭიროა კონკრეტული join-ის დასადგენად. მინიმუმი:

| მიმართება | join-ის უსაფრთხო გასაღები | დასაშვები მტკიცებულება | არასაკმარისი პირობა |
|---|---|---|---|
| Retail SKU → assembled device | vendor product ID + actual received revision, optional batch/lot | orderable sheet, marked PCB/assembly + verified revision | „HC-SR04“, retailer ფოტოს მსგავსება |
| Board → header terminal | board exact profile + connector + contact position | manufacturer header table/board schematic | `IO18` label სხვა დაფაზე |
| Header terminal → SoC GPIO | verified typed `SignalMapping` + manufacturer claim + independent factset | R2 catalog + scoped board documentation | textual `GPIO18`/silicon pin name |
| Package pad → component signal | exact `device` UUID + `package` UUID + `component` UUID + expected footprint | reviewed LibrePCB structural triple | package geometry implies any MPN |
| Capability → function | canonical function predicate + mode + conditions + review | manufacturer/SDK fact as appropriate | category name, simulator pin name |
| Firmware driver → part profile | driver/compatible + SDK/OS version + pin/resource assumptions | source repository code + tested deployment where required | exists in GitHub alone |
| Visual → physical | presentation ID → `instance_id`+`terminal_id` explicit mapping | reviewed immutable mapping | same display string |

**მნიშვნელოვანი მაგალითები:**
- `generic_hc_sr04_family` არის **კლასი**; `Adafruit #3942` არის **retailer product**; ორიდან არცერთი არ ასახელებს დადასტურებულ OEM-სა და PCB revision-ს [P06].
- `ESP32-WROOM-32E` მოდული ≠ `ESP32-DevKitC-32E` board assembly ≠ თვითონ SoC GPIO. Header contact `J2.5`→ GPIO34-ს ამტკიცებს board profile და არა მხოლოდ SoC-ს განსახიერება [P05].
- `YAGEO RC0603FR-0710KL` არის manufacturer MPN; `RESC1608 (0603)` library footprint შეიძლება კანდიდატი იყოს, მაგრამ არ არის გამოკვლეული exact MPN-to-pad/land-pattern pairing [R05,P07].

**მოცულობა:** `identity_state = EXACT_VERIFIED | LISTING_ONLY | FAMILY_ONLY | CONFLICTING | UNKNOWN`; `hardware_revision_status` CORE-ის არსებული მნიშვნელობებით ინახება; ახალი მდგომარეობა მხოლოდ matching adapter-ში წარმოიქმნება. არ ვანიჭებთ „exact verified“-ს იმ ფაქტს, რომელსაც მხოლოდ logo/printed marking აქვს [D].

## 5. მანქანურად წასაკითხი მონაცემები, ტექნიკური სისრულე, უფლებები

`Machine-readable` აღწერს ფორმატს, **არა** factual correctness-ს. ქვემოთ `H` = შესაბამის ველში არსებობს სტრუქტურირებული metadata, `P` = ნაწილობრივი/რელიზზე ან კონკრეტულ მოწყობილობაზე დამოკიდებული, `–` = საჭირო ველი არ არის. **Commercial use** ნიშნავს მხოლოდ დადასტურებულ scope-ს, არა ზოგად იურიდიულ დასკვნას.

| წყარო / კონკრეტული არტეფაქტი | ფორმატი / ხელმისაწვდომობა | იდენტობა, პადები, ფუნქცია, electrical, firmware | უფლებები და გავრცელება | ოპერაციული გადაწყვეტილება |
|---|---|---|---|---|
| **LibrePCB Base** [`LibrePCB_Base.lplib`](https://github.com/LibrePCB-Libraries/LibrePCB_Base.lplib/tree/dc037a238eb5efcc034dd9d62e5775d5c21e90e4) `cmp/*/component.lp`, `pkg/*/package.lp`, `dev/*/device.lp` | S-expression; textual parser / optional LibrePCB CLI checker; pinned commit; `LICENSE.txt` | family P; pads H; pad↔signal H; electrical –; firmware – | official library **CC0-1.0**, original license checked in DATA-001; app itself **GPLv3** (separate!) [P01,R05] | **SELECT**, კონკრეტული subset და raw/derived rights ledger |
| **KiCad symbols** [`kicad-symbols`](https://gitlab.com/kicad/libraries/kicad-symbols) | `.kicad_sym` S-expression, symbol pins/name/type | identity P; pins H; functional P; electrical –; firmware – | **CC BY-SA 4.0 + KiCad libraries exception**; გამოყენება საკუთარ დიზაინში თავისუფალია, მაგრამ **redistributed library collection-ის გამონაკლისი არ ვრცელდება** [P02] | **CONDITIONAL**, არ დავაკოპიროთ proprietary საერთო catalog-ში review-ის გარეშე |
| **KiCad footprints** [`kicad-footprints`](https://gitlab.com/kicad/libraries/kicad-footprints) | `.kicad_mod`, pad numbering/geometry | exact MPN P; pads H; logical P; electrical – | იგივე collection share-alike/attribution რისკი; exact library artifact license საჭირო | **HOLD** initial bundled ingestion |
| **Espressif ESP-IDF** [`espressif/esp-idf`](https://github.com/espressif/esp-idf) GPIO SoC headers / per-target `soc_caps` | C macros/headers, compiled SDK/API; target/release-specific | SoC identity H; board pads –; GPIO function H/P; electrical limited; firmware H | repository **Apache-2.0** ძირითადად; file-level SPDX/third-party exceptions უნდა შემოწმდეს; SDK მონაცემები **სილიკონის ფუნქციის** მტკიცებულებაა [P03] | **SELECT** უკვე გამოყენებული source-reviewed GPIO facts; no duplicate checker |
| **Espressif DevKitC user guide / board schematic** [board guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html) | RST/HTML header tables; PDF schematic for independent cross-check | board identity H; header→GPIO H; electrical P; firmware – | ტექსტის/დიაგრამის **კოპირებაზე** უფლება ცალკე დადასტურდეს; numeric fact + locator ხელით | **SELECT** linked evidence, no mirrored schematics [P05] |
| **Module/SoC manufacturer datasheet** [ESP32-WROOM-32E v2.1](https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html) | versioned HTML/PDF table, manual/potential table extraction | exact module H; module pins H; functions P; rated electrical H; firmware – | დოკუმენტის შიგთავსის მონაცემად გადაბეჭდვა **არ ჩაითვალოს** ავტომატურად ლიცენზირებულად | **SELECT** manually curated per claim; source revision essential [P08] |
| **Zephyr Devicetree** [`hc-sr04.yaml`](https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/sensor/hc-sr04.yaml), DTS/overlay | YAML + DTS + `edtlib`/`dtlib` (reviewed source version) | compatible P; GPIO roles H; electrical –; firmware binding P | example binding `SPDX Apache-2.0`, მაგრამ სხვადასხვა ფაილს own SPDX; sensor compatible ≠ exact OEM [P09] | **SELECT cross-check**, no independent electrical truth |
| **CMSIS-SVD / CMSIS-Pack** [PDSC specification](https://arm-software.github.io/CMSIS_5/5.8.0/Pack/html/packFormat.html) | `.svd`, `.pdsc` XML, XSD, device/board/conditions | silicon devices H/P, package pads P, peripheral registers H, electrical –; software components H/P | schema/tools open; **ყოველ vendor pack-ს თავისი უფლებები**; არც ყველა SVD/pack-ს ერთიანი Apache license | **HOLD** until non-ESP MCU family requires and pack-specific rights verified [P10] |
| **Adafruit retailer #3942** [product listing](https://www.adafruit.com/product/3942), learning pages | HTML; human curation | SKU H; roles H; approximate voltage/trigger H at listing level; exact OEM revision –; firmware – | vendor page is **not** bulk licensed component DB; link + pinpoint factual attribution, not mass scraping [P06] | **SELECT retail-scope discovery**, **HOLD exact OEM engineering admission** |
| **YAGEO exact sheet** [RC0603FR-0710KL](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-0710KL) | manufacturer dynamic PDF endpoint; manually pin bytes/edition and table row | MPN H; rating H when reviewed; specific LibrePCB UUID matching – | no blanket PDF redistribution permission established | **HOLD** exact import until manufacturer-to-generic mapping reviewed [R05,P07] |
| **Wokwi reference / Custom Chips** [HC-SR04](https://docs.wokwi.com/parts/wokwi-hc-sr04), [Chips API](https://docs.wokwi.com/chips-api/getting-started) | simulator reference + JSON visual pinout + C/WASM model | simulated interface P; physical identity –; rated electrical –; firmware simulated P | documentation accessible; Wokwi production/API/embed rights **არ დასტურდება** მხოლოდ უფასო plan-ით [E02,P11] | **REFERENCE ONLY**, do not import simulator safety claims |
| **Distributor catalog/availability** | provider-dependent HTML/API; stock/price variable | procurement H/P; package P; compliance/rating sometimes P | provider terms, rate-limit, redistribution/APIs often restricted; individual review | **OPTIONAL procurement only**, no hard safety authority |

**ვერსიის გაფრთხილება [P08]:** 2026-11-20-ზე Espressif-ის ოფიციალურ HTML datasheet-ში ESP32-WROOM-32E ვერსია **v2.1** ჩანს; Research E-ის ძველი ტესტის source edition არ უნდა ჩაითვალოს ავტომატურად იგივე გამოცემად. DATA-001-ის ledger-ში YAGEO-ს ერთ URL-ზე სხვადასხვა დროს გენერირებული PDF edition/fingerprint დაფიქსირდა; საჭიროა **ფაქტის წყაროს ვერსიის** pin, არა მარტო მუდმივი URL. [R05]

**განსხვავებული უფლების მდგომარეობები:** `USE_AS_LINK`, `PARSE_LOCALLY`, `DISTRIBUTE_DERIVED_FACTS` (იურიდიული დასკვნის შემდეგ), `REDISTRIBUTE_SOURCE`, `RESTRICTED`, `UNKNOWN`. მათზე გადაწყვეტილება **artifact-specific**ა. SHA ამტკიცებს ბაიტების იგივეობას, არა მონაცემის ნამდვილობას, source authenticity-ს ან უფლებას.

**ტექნიკური სიფრთხილე:** I2C binding ნიშნავს software bus role-ს; pull-up resistor-ის არქონა/არსებობა, `VIL/VIH`, speed/clock-stretch/voltage tolerance სხვა მტკიცებულების საგანია. KiCad `pin_type=power_in` არის ERC metadata, არა 5 V tolerant-ის დადასტურება. Wokwi სიმულაციაში `VCC` სახელწოდება არაა PCB-ის სერტიფიცირებული აღწერა [P02,P09,P11].

## 6. Evidence acquisition — რეალური, მრავალჯერადი გამოყენების მექანიზმები

**რეკომენდებული წყარო→კატალოგი ბილიკი:** `Discovery → Rights → Exact identity → Structural extraction → Semantic normalization → Capability extraction → Constraint qualification → Evidence review → Versioned catalog → Regression → Admission → Reuse`. მონაცემთა დამუშავება არ გულისხმობს LLM-ისაგან ახალი ელექტრული ფაქტების ავტორიზებას.

| საფეხური | შესავალი → გამოსავალი | deterministic მეთოდი / არსებული OSS | უარყოფა, review, update და rollback |
|---|---|---|---|
| 1. Discovery | query / user request → URL/part candidates | exact-key search; LibrePCB S-expression indexes; manufacturer part search. Text retrieval მხოლოდ recall-ის ასამაღლებლად | გაურკვეველი part names რჩება `DISCOVERED_CANDIDATE`; reviewer არ საჭიროებს ჯერ |
| 2. Rights | URL + proposed use → permissions record | license file/ToS snapshot, SPDX, use-case matrix; no bulk scrape | permission unknown→ **link only**; policy downgrade immediately quarantine; human legal/product owner |
| 3. Identity | candidate + vendor order code → scoped `identity` | full MPN normalization **lossless** (suffix შენარჩუნებული), board/module/revision matching, source aliases evidence | mixed retailer/OEM→`NEEDS_REVIEW`; არ შეიძლება fuzzy merge |
| 4. Structure | pinned file → pads/signals/terminals | LibrePCB parser + three-way UUID join, optional upstream CLI syntax check; KiCad review-only fallback | duplicate/missing pad/mismatched UUID→`REJECTED`; rollback to prior pinned catalog |
| 5. Semantics | accepted structure → typed functional predicates | supported capability vocabulary, explicit interface/mode, unit semantics | undefined function→discoverable, not pass; reviewer for new synonym/capability |
| 6. Claim extraction | numbered official document locator → proposed fact | manual field extraction; compiler/header parser for SDK flags; LLM may suggest span **but not admit** | bound type `min/max/typ/abs`, unit, condition, scope missing→`NEEDS_REVIEW` |
| 7. Qualification | proposed claim + sources → status | source-class precedence **by claim type**, condition matching, conflict detection, provenance check | conflicting same-scope claims→`CONFLICTING`; no arbitrary last-write-wins |
| 8. Review | qualification package → signed decision/ledger | human review for safety critical; separate reviewer strongly recommended for positive electrical bounds | approve narrowly; review not inherited to neighboring variants; backout revokes claim |
| 9. Version | reviewed records → immutable catalog + index generation | stable IDs, canonical serialization, full version/digest, dependency keys | schema mismatch, stale IDs→fail closed; last admitted catalog retained |
| 10. Regression | version + frozen fixtures → oracle report | source-mapping, GPIO/B existing tests, independent evidence acceptance, electrical tests **when C exists** | delta break→not admitted; prior version still available read-only |
| 11. Admission | all independent gates passed → `ENGINEERING_ADMITTED` | ledger + external policy gate; for CORE/GPIO call their own validators | any missing gate→previous state, no silent transition |
| 12. Reuse/update | exact versioned claims→queries/verifiers/hints | composite source→claim→rule→finding→hint reverse index | source change invalidates dependent results; freeze/recheck before reactivation |

**სავალდებულო provenance tuple [D]:** `{publisher, source_class, canonical_url, document_id, edition, publication_or_retrieval_date, content_digest_if_permitted, locator(page/section/table/row or file:line), exact_subject_scope, extracted_property, declared_bound_kind, normalized_unit, original_unit, mode, environment, load/supply_conditions, source_license_state, review_state, reviewer_record, catalog_revision}`. **ცალკე** ინახება field provenance for derived formulas: upstream claim IDs + formula/version + rounding. Manual reviewer approves *claim scope*, not entire document.

**იდემპოტენტურობა:** same original artifact digest + same parser version + same normalization semantics → same candidate normalized record. *Different* edited source/digest → new version, never overwrite old claim. `digest` is integrity guard, not rights/authenticity oracle. External signed manufacturer authenticity is not assumed unless verifiable [D].

**დაშვების ორი დამოუკიდებელი უფლება:**

- **Search admission:** `DISCOVERED_CANDIDATE`, `STRUCTURALLY_VALIDATED`, `NEEDS_REVIEW`, `CONFLICTING` (მხოლოდ მკაფიო ნიშნით). `REJECTED` მხოლოდ აუდიტში, არა ჩვეულებრივ რეკომენდაციებში.
- **Engineering-positive admission:** მხოლოდ შესაბამისი `ENGINEERING_ADMITTED` claim + exact scope + compatible condition + independent rule invocation. `SEMANTICALLY_REVIEWED` საკმარისია UI-ს კონცეპტისთვის, მაგრამ არა უსაფრთხოების PASS-ისთვის.

`STRUCTURALLY_VALIDATED`-დან `SEMANTICALLY_REVIEWED`-ზე ტრანზიცია არ ნიშნავს ავტომატურ `ENGINEERING_ADMITTED`-ს. `CONFLICTING`, `NEEDS_REVIEW` და `REJECTED` მდგომარეობები მოითხოვს *ხელმოწერილ* review event-ს მდგომარეობის შეცვლისას. წინასწარ მიღებულ facts-ზე დაგვიანებულმა conflict-მა status უნდა დააქვეითოს, არ დატოვოს „კარგი“ badge.

## 7. Functional capability matching — ალგორითმების შედარება

| მეთოდი | რაში მუშაობს | საფრთხე/ზღვარი | გადაწყვეტილება |
|---|---|---|---|
| Indexed relational / typed attribute filtering | `measurement=distance`, `interface=pulse`, `gpio_out=true`, `package=0603` | არ ასრულებს კომბინირებულ circuit constraints-ს | **SELECT first** — მარტივი, აუდიტირებადი, უფასო embedded SQLite-ით |
| Deterministic rule matching | exact mode, voltage/source qualification, typed evidence | წესის დუბლირების რისკი CORE/B/C-ში | **SELECT only selection predicates**, GPIO/electrical verdict delegated |
| Finite-domain CSP / backtracking | ორი–რამდენიმე slot-ის resource assignment, must-not-share GPIO, unique output pin | combinatorial growth; insufficient electrical facts | **SELECT optional bounded, only after single-slot tests** |
| Bipartite graph matching | required signal/role ↔ eligible port/resource | ერთი პინის მრავალროლიანი mode და bus constraints ცალკე დასადებია | **SELECT for bounded distinct-assignment cases** |
| Knowledge graph | heterogeneous provenance exploration | ახალი store/ontology, consistency/maintenance | **HOLD** — flat join/index + reverse references საკმარისია |
| Semantic search / vector retrieval | ქართულ ფრაზიდან aliases/synonyms → discovery | similarity „safe“/„supported“ არ ნიშნავს | **HOLD vector DB**; optional full-text query expansion with human-review synonyms |
| Symbolic + semantic hybrid | high-recall discovery + exact final filtering | LLM hallucination, retrieval poisoning | **CONDITIONAL** only search stage; never proof stage |
| Multi-criteria optimization | compatible candidates-ის cost/complexity ranking | weight-based safety laundering | **SELECT lexicographic**, no probabilistic compatibility score |
| CP-SAT OR-Tools | larger discrete assignments and resource conflicts | solver integration/complexity, license/solver path | **HOLD** until bounded backtracking becomes inadequate; OR-Tools Apache-2.0 [P12] |

**მინიმალური მუშაობის ფორმულა [D]:**

1. `query.intent_capability` ემთხვევა დამტკიცებულ typed predicate-ს (მაგ., `MEASURE_DISTANCE`, `GPIO_OUT`, `PULSE_ECHO_INPUT`, `I2C_SENSOR`, `LED_INDICATION`), მაგრამ თავისუფალი ქართული ტექსტი არ გადაიქცევა engineering fact-ად.
2. exact identity guard აგროვებს MPN, revision, package/mode. თუ მოთხოვნა **generic component family**-ს უშვებს, `FAMILY_ONLY` შეიძლება მოხვდეს shortlist-ში; თუ exact MPN/PCB აუცილებელია, იგივე candidate `IDENTITY_UNRESOLVED`-ია.
3. hard predicates სამმნიშვნელოვანი ლოგიკით: `TRUE`, `FALSE`, `UNKNOWN` (+ separate `CONFLICT`). `FALSE→REJECTED`, `UNKNOWN→UNRESOLVED`; `CONFLICT→CONFLICTING/HOLD`. **არც ერთი UNKNOWN არ გარდაიქმნება TRUE-დ**.
4. component-level capability matching-ის შედეგი არის predicate-satisfaction-სა და evidence-სთან დაკავშირებული წინადადება. **Circuit-wide hardware rules** არ სრულდება ამ ეტაპზე: მას მფლობელი verifier უნდა შეასრულოს.
5. accepted candidate-ის შემდეგ მომხმარებლის მიერ არჩეული `terminal_id`+`instance_id` CORE-ისგან გამოითვლება; GPIO rule კი სრულდება **მხოლოდ** `gpio_verify.py`-ით.

**სასარგებლო კონტრ-მაგალითი:** სასურველია `GPIO_OUT` და candidate-ზე წერია `GPIO34`. კატეგორიულად მსგავსი label-ს მიუხედავად `PHYSICAL_CAPABILITY` source fact ამბობს `output_allowed=false` → B-verifier **FAIL**. Matching-ის ამოცანაა შესაბამის კანდიდატს verifier გადასცეს და არა საკუთარ დამოუკიდებელ GPIO truth-ს ენდოს [R03,P04].

## 8. Hard / soft constraints და uncertainty semantics

**Hard:** exact function/mode; strict physical identity; reviewed board contact→silicon mapping; source-supported voltage/logic/current constraints; package/connector/operating state; mandatory firmware support *თუ მოცემული მიზნისთვის აუცილებელია*; required supporting circuit elements. **Soft:** ფასი, ხელმისაწვდომობა, ზომა, პოპულარობა, დასწავლის სიმარტივე, examples, ნაწილების რაოდენობა.

**მნიშვნელოვანი განსხვავება:** „უნდა იყოს სენსორი, რომლის Echo პირდაპირ შეერთებადია ESP32-ზე“ არის *hard circuit-level requirement*; „სასურველია ხმის ტალღით გაზომვა“ შეიძლება soft preference. კანდიდატის ფუნქციური შესაბამისობა *არ* აკმაყოფილებს automatic direct-connection requirement-ს.

| ფაქტის მდგომარეობა | Matching selection | Engineering output | Georgian hint wording |
|---|---|---|---|
| reviewed mandatory fact TRUE, ყველა საჭირო check შესრულდა | `FUNCTIONALLY_ELIGIBLE`; optionally later verified | მხოლოდ exact verified check `PASS` | „ამ პირობებში X-ის მოთხოვნა დაკმაყოფილდა“ |
| reviewed mandatory fact FALSE | `REJECTED_HARD` | verifier-იდან `FAIL`, თუ verifier წესი არსებობს; სხვა შემთხვევაში `NOT_SELECTED` | „ამ ფუნქციისთვის ვერ გამოიყენება: …“ |
| required fact absent / unspecified mode | `UNRESOLVED_MISSING` | `UNKNOWN` ან `NOT_EVALUATED` — **არ** PASS | „ჯერ უცნობია …; საჭიროა …“ |
| same-scope claims disagree | `UNRESOLVED_CONFLICT` | `UNKNOWN` with source claim IDs | „წყაროები ერთმანეთს ეწინააღმდეგება“ |
| missing device mapping | `UNRESOLVED_IDENTITY` | GPIO `UNKNOWN`, source-mapping not established | „შერჩეული ფიზიკური კონტაქტი ვერ მიება სილიკონის პინს“ |
| clearly unsupported rule/mode | `UNSUPPORTED_SCOPE` | `NOT_EVALUATED`, არა `FAIL` | „ამ ტიპის შემოწმება ჯერ არ არის მხარდაჭერილი“ |
| only soft preference mismatched | keep eligible; note penalty | no change to engineering finding | „შეიძლება გამოყენება, მაგრამ ნაკლებად მოსახერხებელია …“ |

**ორი ცალკე boolean:** `capability_confirmed` და `circuit_verified` **არ არიან** synonyms. Candidate შეიძლება `capability_confirmed=true` და `circuit_verified=unknown` იყოს. „compatible“ UI-ს სიტყვა ვაწეროთ მხოლოდ ზუსტად დასახელებულ check-ს (`GPIO output supported in mode ACTIVE`), არა მთელ მოწყობილობას.

## 9. Candidate ranking — დაჯგუფება, არა ფუჭი ქულა

**შერჩევის წესი:** ჯერ safety/identity gate, მერე preference order; `UNKNOWN` არ უნდა გაერიოს დამტკიცებულებთან ერთიან რიცხვით „მაღალ ქულად“.

1. **Group 0: `REJECTED_HARD` ან `CONFLICTING`** — არ შედის რეკომენდებულ არჩევანში; შესაძლებელია troubleshooting list-ში.
2. **Group 1: `REVIEWED_FUNCTIONAL / circuit checks pending`** — დადასტურებული ფუნქცია, მაგრამ electrical/firmware/synthesis ჯერ გასავლელია.
3. **Group 2: `DISCOVERY_ONLY / missing mandatory facts`** — ცალკე „მონაცემი აკლია“ სიაში, არა „უსაფრთხო ალტერნატივა“.
4. **Within same eligible group:** (a) exact identity/evidence coverage; (b) lower number of *verified necessary* support components; (c) implementation simplicity; (d) user preferences; (e) deterministic key tiebreak (`manufacturer,MPN,revision`). **სხვადასხვა group-ები ერთ ქულად არ შედარდება.**

ეს განსხვავდება `0.8 compatibility score`-ისგან: რიცხვი, რომელიც safety unknown-ს დაბალი ფასით ან popularity-ით „აბათილებს“, დაუშვებელია. დასაშვებია *pure preference score* მხოლოდ verified eligible subgroup-ში, წინასწარ გაცხადებული weights-ით; ამ ეტაპზე ამის გაზომვა/განაწილება არ არსებობს [D].

**ალტერნატივა:** evidence completeness პირველ ადგილზე დაყენებას შეუძლია ქცევა biased გახადოს ცნობილ პროდუქტებზე და უარყოს ახალი, რეალურად უკეთესი ნაწილი. გამოსავალი — მტკიცებულებაგაკლებული **separate research queue**, არა უსაფრთხოების სტანდარტის დაწევა. `RequiredAuxiliaryParts` უნდა იყოს typed dependency, მაგრამ დაუდასტურებელი resistor divider ვერ ჩაითვლება verified bill of materials-ად.

## 10. Matching → synthesis → verifier-ის პასუხისმგებლობები

| საკითხი | Component matching (I) | Circuit synthesis (J, future) | Existing GPIO B | Electrical C (future) | Firmware L (future) |
|---|---|---|---|---|---|
| „ზომავს მანძილს“ | reviewed function claim და mode | sensor choice in design | – | – | runtime use |
| MCU პინის მოთხოვნა | select capability need, no own pin truth | propose terminal assignment | **authoritative** physical mapping/capability/board state | – | configured runtime function |
| VCC/GND supply | collect required supply conditions | propose supply nets | – | **authoritative** voltage/current/bound comparison | – |
| Echo output vs MCU input | collect explicit unresolved electrical prerequisite | propose level-conditioning topology for review | input capacity only | **authoritative** VOH/VIL/VIH/absolute limits, impedance/source/load | sampling timing |
| LED + resistor | discover LED/resistor families and missing constraints | choose resistor topology/rail/drive | GPIO output capability | forward voltage/current, dissipation, rail limits | blink/alarm behavior |
| I2C shared bus | declare required I2C role, address and pull-up flags | assign shared bus and support parts | chosen GPIO feasibility within B scope | rail/level/pull-up/bus currents | driver/controller/addresses/timing |
| SPI/UART and resource conflicts | typed capability requirements | assign bus/role/CS/RX/TX, unique resources | supported pin mapping where covered | signal electrical compatibility | active pinmux and peripheral conflict |
| Finding/hint | include source-backed context | propose—not verify—connection | emits finding/reason code | emits rule result once implemented | emits firmware evidence |

**Transfer payload rather than duplicate engine:** `requirement_refs`, `candidate_identity`, `component_claim_refs`, `terminal_refs`, `operating_conditions`, `needs_auxiliary`, `missing_electrical`, `catalog_digest`; engineering result later returns `finding_id + reason_code + rule_id + snapshot_digest + evidence_claim_ids`. Circuit synthesis proposals are *hypotheses*; approval of Research J and C/L actual software is outside this document. This arrangement deliberately preserves the DEMO-001 bridge as a **narrow adapter**, not a general synthesizer.

## 11. ქართულ საგანმანათლებლო ცოდნასთან კავშირი

`ComponentKnowledgeContext` უნდა შეიქმნას **deterministic join**-ით და არა model-generated „კარგი ახსნით“: `(selected instance, physical terminal, requirement, finding, source claim, concept reference)`. ის შეიძლება მოერგოს Research H-ის მომავალ `EducationalHint` კონტრაქტს. H-ის პროექტული სპეციფიკაცია ითხოვს `finding_id + reason_code + rule_id + snapshot_digest` join-ს; ეს **ინტეგრაციის სამიზნეა**, არა დამტკიცებული ახლანდელი H runtime [H01].

| Hint category | შემომავალი წყაროები | დასაშვები მაგალითი | დაუშვებელი განცხადება |
|---|---|---|---|
| `COMPONENT_FUNCTION` | capability + exact scope + source | „HC-SR04 გამოიყენება ულტრაბგერით მანძილის გასაზომად; კონკრეტული SKU-ის ტექნიკური პირობები ცალკე იხილეთ“ | „ნებისმიერი HC-SR04 უსაფრთხოა ESP32-ზე“ |
| `TERMINAL_ROLE` | physical `TerminalRef`, mapping, mode | „არჩეული დაფის J2.5 მიბმულია GPIO34-ზე, რომელიც input-only-ა“ | მხოლოდ „GPIO34“ label-იდან physical pin მტკიცება |
| `COMPATIBILITY_REASON` | real B/C finding, reason, claim | „გამომავალი ფუნქცია ამ კონტაქტზე უარყოფილია; B-ის `PHYSICAL_CAPABILITY` ჩავარდა“ | „სრული სქემა შეამოწმდა“ მხოლოდ GPIO PASS-ზე |
| `REQUIREMENT_MISMATCH` | user formal requirement + function claim | „ეს კომპონენტი გათვლილია სხვა ფუნქციაზე/ინტერფეისზე“ | „საუკეთესო ვარიანტია“ უნაკლო მიზნის გარეშე |
| `MISSING_EVIDENCE` | unresolved prerequisites, absent/contradictory claim | „არჩევისთვის საჭიროა output-high-ის პირობები და MCU input limits“ | „ალბათ 3.3 V-compatible-ა“ |
| `ALTERNATIVE_CANDIDATE` | ranked, clearly labelled discovery/verified scope | „სხვა 3.3 V-ლოგიკის სენსორი შეიძლება გამოვიკვლიოთ“ | „აუცილებლად უსაფრთხო drop-in“ ვალიდაციის გარეშე |
| `NEXT_ENGINEERING_STEP` | missing list + verifier owner | „შეამოწმე PCB revision და მიმართე მწარმოებლის დიაპაზონის ცხრილს“ | ავტომატური კაბელირების/გაყოფის „გაკეთდა უსაფრთხოდ“ |

**ავტორიტეტის წესი [D]:** 1) finding-ს ქმნის მხოლოდ ავტორიზებული verifier, 2) educational engine *ჩამოთვლის მის ფაქტებს*; 3) optional LLM არის ტექსტის რედაქტორი constrained claims-ზე, მხოლოდ მაშინ, თუ output post-validation **არ დაამატებს** ახალ ფაქტობრივ შედარებას/რიცხვს/დასკვნას; 4) failure→template fallback, არავითარი LLM-generated electrical claim. Georgian text localization-ზე უნდა შემოწმდეს critical terms: `input-only`, `output-capable`, `pull-up`, `active mode`, `unknown`, „გარე კვება“, „აბსოლუტური მაქსიმუმი“, „რეკომენდებული სამუშაო დიაპაზონი“.

**კომპონენტზე მიბმული პრაქტიკული ჰინტის მაკეტი:**

> **შეერთების პრობლემა:** ამ დაფაზე J2.5 კონტაქტი მიბმულია GPIO34-ზე. თქვენ მოითხოვეთ გამოსავალი (`GPIO_OUT`), მაგრამ წყაროზე დაფუძნებული GPIO წესი ამ ფუნქციას უარყოფს. **შემდეგი ნაბიჯი:** აირჩიეთ დამოწმებული output-capable კონტაქტი და ხელახლა გადაამოწმეთ wiring. **ჯერ არ შემოწმებულა:** HC-SR04-ის Echo ელექტრული თავსებადობა, LED-ის დრაივი და პროგრამული მართვა. **მტკიცებულება:** board pin table + ESP-IDF GPIO Summary; კონკრეტული finding-ის claim IDs.

**შენიშვნა:** ეს არის მხოლოდ ის შინაარსი, რომლის ნიმუშს B-ის რეალური წესები და ოფიციალური დოკუმენტი უჭერს მხარს; არა მიმდინარე აპში უკვე ნაჩვენები UI-ის screenshot. არ ვამტკიცებთ, რომ გადატანილი კავშირი ელექტრულად უსაფრთხოა [R03,P04,P05].

### 11.1 Educational concept provenance

`concept_ref` შეიძლება იყოს იდენტიფიკატორი `gpio.input_only`, `signal.echo_pulse`, `source_vs_load`, `unknown_vs_fail`, `voltage.absolute_vs_operating`, `resistor.package_vs_value`. მისი content შეიძლება სპეციალურად შეიქმნას ქართულად, versioned და pedagogically reviewed; **სასწავლო ტექსტი ≠ მწარმოებლის მტკიცებულება**. ერთ concept-ს შეიძლება უკავშირდებოდეს ბევრი component claim, მაგრამ ყოველი კონკრეტული hint მაინც references exact component/profile/finding. ფიზიკური უსაფრთხოების არცერთი რიცხვი არ გამომდინარეობს მხოლოდ concept-იდან.

### 11.2 Minimal hint construction contract

`HintInput = FindingRef(finding_id, rule_id, reason_code, snapshot_digest) + ComponentKnowledgeContext + query_requirement_id + locale("ka-GE")`. Join must prove: `finding.snapshot_digest == context.snapshot_digest`, `finding.terminal == context.terminal`, `context.claim_refs ⊇ finding.evidence_claims` (where available), `catalog version compatible`, `rule_id` recognized. Failure → generic non-factual `NEEDS_REVIEW` hint; zero inferred details. `HintOutput = {category, rendered_ka_text, factual_spans→claim_ids, next_action_kind, limitations, hint_template_version, dependency_digest}`. ეს არის H-ის ინტეგრაციის წინადადება და არა მეორე საინჟინრო finding [D].

## 12. Source → claim → rule → hint traceability

**Minimal dependency DAG [D]:**

`SourceArtifact(fingerprint/version/license)` → `SourceLocator` → `ComponentCapabilityFact`/`GpioSourceFact` → `QualificationReview` → `ComponentCandidate/RuleInput` → `VerifierFinding(rule_id,rule_version,snapshot_digest)` → `ComponentEducationalEvidence` → `RenderedHint(template_revision,locale)`.

- ამ DAG-ის შესანახად საკმარისია typed foreign-key/reverse-index table (SQLite ან ფაილური JSON sidecar); **სხვა** knowledge-graph DB საჭირო არ არის.
- წყაროს **content change** → affected claim IDs -> ruleset inputs -> affected candidate reports / snapshot-finding summaries -> hint cache. თითოეული ინფიცირებული derived result იღებს `STALE_REVALIDATION_REQUIRED`; fresh engineering PASS **არ შეიძლება**.
- ტექსტის თარგმანის/პედაგოგიური შაბლონის **only change** → invalidate educational hint only; არ უნდა შეცვალოს ძველი engineering finding.
- ფასის/stock-ის ცვლილება → procurement ranking refresh, არა ელექტრული claim invalidation.
- ლიცენზიის rollback / source permission change → distribution block; source identity/engineering claim ცალკე review (არსებული fact-ის სიმართლეს ლიცენზიის ცვლილება ავტომატურად არ აუქმებს, მაგრამ მისი ხელახალი გამოქვეყნების უფლება იცვლება).
- ახალი manufacturer edition → `NEEDS_REVIEW` dependent claim, `CONFLICTING` თუ ერთ exact condition-ზე შეუსაბამო ორი claim დარჩა; retrospective archived result remains traceable, **არ ჩაითვალოს ახალი ოპერაციული ავტორიზაციად**.
- ორი თანაბარი user display label არ ქმნის merge-ს; dependency ID ყოველთვის `instance_id`+`terminal_id` არის.

**Invariant:** `(catalog_digest, factset_digest, snapshot_digest, rule_version, hint_version)` სრული ნაკრები უნდა იყოს შედეგის რეკონსტრუქციისთვის; `timestamp`-ით ძველი წყაროს „უახლესად“ გამოცხადება დაუშვებელია. **მხოლოდ hash equality არც ავტორიტეტია, არც დამოუკიდებელი correctness oracle.**

## 13. ექვსი source-backed სცენარი — მკაფიო decision records

### I01 — ESP32-DevKitC-32E: board↔module↔SoC

**მოთხოვნა:** შეირჩეს board terminal, რომელსაც ACTIVE მდგომარეობაში `GPIO_OUT` შეუძლია; იგივე სქემა მოითხოვს `GPIO_IN` Echo-სთვის. **ფიქსირებული identity:** board `ESP32-DevKitC-32E`, V4 documented guide scope; module `ESP32-WROOM-32E`. **ხელმისაწვდომი**: `J2.5=IO34`, `J3.9=IO18`, `J3.8=IO19`, ასევე board-reserved `J3.19=CLK/GPIO6` კვლევაში გამოყენებული ლედჯერით [R04,P04,P05].

| ელემენტი | დადასტურებული/გადაწყვეტილება |
|---|---|
| წყაროები | official DevKitC V4 header mapping table, official GPIO summary, pinned project's `devkitc_32e_catalog.json` / `devkitc_32e_facts.json`, CORE-001B source-and-rule ledger [R03,R04,P04,P05] |
| extracted fields | exact `connector, position, printed_label, target_kind=soc_gpio, target_id, output_allowed, input_allowed, board_availability, mode, source IDs` |
| identity limit | რეალური პირადი დაფის revision ჯერ არ ჩანს; `board_family` ≠ ყველა კლონი; SoC mask ≠ board availability |
| hard result | `J2.5 GPIO34 OUTPUT → FAIL/OUTPUT_NOT_CAPABLE` (project rule name should be taken from B result); `J3.9 GPIO18 OUTPUT → PASS` **მხოლოდ** B's scoped physical capability; `J3.8 GPIO19 INPUT → PASS` **მხოლოდ** input capability; `J3.19 CLK` ACTIVE ordinary GPIO output **reserved/FAIL** |
| missing | runtime firmware pinmux/config, electrical input/output tolerance, actual received board PCB revision |
| matching | eligible GPIO resources **only** after existing B verifier result; matching layer does not compute masks independently |
| educational hint | GPIO34 input-only, GPIO18/19 function check, flash-reserved pins and remaining evidence |
| აკრძალული პრეტენზია | „GPIO18-ზე მთელი HC-SR04 სქემა უსაფრთხოა“, ან „B ადასტურებს firmware runtime configuration-ს“ |
| independent oracle | compare manufacturer J-header table + pinned SDK capability mask + B factset/`verify_gpio_requirements`; scope/factset pin preserved |

**`J2.5`-ის role source-backed claim** პროექტის ledger-ით დამოწმებულია; იდენტური display label სხვა board-ისთვის არ გადაიტანება. `GPIO34` input-only ოფიციალურ ESP-IDF-ში ცალკე დასტურდება [P04].

### I02 — Adafruit #3942 HC-SR04: retailer vs OEM

**მოთხოვნა:** დისტანციის გაზომვის candidate მიკროკონტროლერის trigger/echo interface-ით. **candidate scope:** `Adafruit product 3942`, არა სრულად დადასტურებული HC-SR04 OEM/hardware revision. [P06]

| ელემენტი | დადასტურებული/გადაწყვეტილება |
|---|---|
| წყარო | Adafruit official product #3942, მისი learning page, optional Zephyr `hc-sr04.yaml` as driver-role cross-check, not electrical manufacturer acceptance [P06,P09] |
| extracted fields | `function=ultrasonic_distance`, `VCC/GND/Trig/Echo labels`, listing-level 5 V supply recommendation, Echo 5 V logic, ~10 µs trigger; retailer kit includes 2×10 kΩ resistors |
| identity limit | exact OEM and PCB revision **UNKNOWN**; „generic HC-SR04“ → `exact manufacturer` ავტომატურად არ გარდაიქმნება |
| hard result | functional sensor candidate = `FUNCTION_PRESENT_AT_RETAIL_SCOPE`; direct 3.3 V MCU connection must remain `UNRESOLVED_ELECTRICAL` |
| missing | actual variant/PCB, source impedance/output-high min/max under conditions, processor pin absolute/recommended limits, load and supply specifics |
| selection | discovery yes; guaranteed full circuit compatibility no |
| hint | „მანძილის გასაზომი მოდულია, მაგრამ Echo-ზე 5 V ლოგიკური გამოსავალია; MCU-თან შეხამება ცალკე საჭიროებს შეფასებას“ |
| no claim | „ყველა #3942 რეალურად ერთი და იგივე OEM-ის პარტიაა“ ან „Echo პირდაპირ safeა“ |
| independent oracle | SKU and pin-roles from Adafruit current listing; exact-OEM blank must remain blank; voltage verdict requires dedicated C rule when approved |

### I03 — LibrePCB generic 0603 resistor vs YAGEO exact part

**მოთხოვნა:** resistor component capable of requested resistance/power/package. **candidate A:** LibrePCB generic resistor (`dev/483a71eb-318e-448e-82ff-f02efc4821aa/device.lp`); **candidate B:** YAGEO exact `RC0603FR-0710KL` [R05,P07].

| ელემენტი | დადასტურებული/გადაწყვეტილება |
|---|---|
| source | LibrePCB Base pin `dc037a238eb5efcc034dd9d62e5775d5c21e90e4`, DATA-001 evidence ledger and official YAGEO specsheet URL |
| extracted fields | LibrePCB `RESC1608/0603`, package pad `1/2`, component signals, device three-way UUID join; YAGEO 10 kΩ ±1% at manufacturer candidate scope (held for exact mapping) |
| identity limit | `generic-device` has **no approved** MPN→pad/footprint pairing; `value`/rated power cannot be copied into generic record by name |
| hard result | `STRUCTURALLY_VALIDATED`; exact resistor/drive suitability `UNKNOWN` until manufacturer electrical characteristics and package mapping reviewed |
| missing | YAGEO exact mounting/pad alignment with selected footprint, rating under relevant ambient/derating, circuit conditions |
| matching | `resistor,0603` discovery yes; `verified RC0603FR-0710KL electrical solution` no |
| hint | „ორი pad არის ცნობილი; 10 kΩ და სიმძლავრის რეალური ლიმიტები ამ generic ჩანაწერში არ არის მიღებული“ |
| no claim | „10 kΩ ახლა უკვე generic LibrePCB-ის fact-ია“ ან ავტომატური LED current-limit sizing |
| independent oracle | original LibrePCB pinned three-way UUID join + manufacturer exact revision + manual acceptance; no MPN link = no electrical PASS |

### I04 — LED visual alarm requirement

**მოთხოვნა:** 30 სმ-ზე ნაკლები მანძილისას ვიზუალური ინდიკაციის შესაძლებლობა. ეს არის **მიზანი**, რომელიც მოითხოვს LED output, circuit drive და firmware alarm behavior-ს. **candidate:** LED generic family ან მომავალში კონკრეტული LED MPN — ამ snapshot-ში **არცერთი კონკრეტული LED-ის სრული authoritative electrical facts არ დადასტურდა** [U].

| ელემენტი | დადასტურებული/გადაწყვეტილება |
|---|---|
| needed evidence | exact LED MPN/package/polarity; forward-current min/nominal/max; forward voltage spread vs current/temp; reverse voltage; power/thermal; rail bounds; GPIO output-current/VOH/VOL; resistor tolerance/power; MCU source/sink mode |
| auxiliary | current-limiting/drive element needed as a **design hypothesis**, actual resistor MPN/topology/value remains unverified |
| identity & hard result | `DISCOVERED_CANDIDATE` or `UNRESOLVED_MISSING`; not `ENGINEERING_ADMITTED` |
| verifier | GPIO B may check `GPIO_OUT`; circuit J must propose topology, C must later evaluate current/thermal, L must validate alarm logic |
| firmware | 30 cm threshold cannot be verified merely from an existing GPIO `PASS`; sensor timing and code behavior not evaluated |
| educational | „ვიზუალური ალარმისთვის LED-ს სჭირდება დენი და მართვის წრედი; რამდენი დენი დასაშვებია, ჯერ არ ვიცით“ |
| no claim | fabricated LED forward voltage, safe resistor value, safe wiring, or current budget |
| independent oracle | fixed empty exact-LED evidence ledger → `UNKNOWN`; explicit synthetic test bounds may be used solely in labelled test data |

### I05 — ESP32/HC-SR04 Echo logic-level compatibility

**მოთხოვნა:** Echo signal შეერთდეს ESP32-ის შესაბამის input contact-ზე სრული electrical compatibility-ით. **წყარო A:** retailer #3942 Echo 5 V logic; **წყარო B:** Espressif board + module/SoC datasheet; **source C:** future electrical verifier rule [P05,P06,P08].

| ელემენტი | გადაწყვეტილება |
|---|---|
| separate facts | **sensor supply** 5 V recommended by product listing; **Echo logic** listing says 5 V; **MCU input bound** exact SoC/module voltage tables and condition; **board terminal** exact mapping |
| hard check | direct Echo-to-ESP32 connection **არ** ჩაითვალოს electrically PASS. Input-capable GPIO19 ≠ 5 V tolerant GPIO19. [P04,P06] |
| conditional auxiliary | Adafruit #3942-ის კომპლექტში **ორი 10 kΩ** resistor და divider-ის მაგალითია; ის არის **vendor application suggestion**, არა ამ შერჩეული PCB revision-ზე/MCU input-ზე სრულად ვალიდირებული engineering design |
| missing | waveform HIGH/LOW extrema, output/source impedance, leakage and input clamp currents, MCU threshold/bounds, tolerance, resistor variants, ground/power reference, dynamic behavior, temp/supply |
| synthesized design | Research J may generate *candidate* level-shift/divider, future CORE C must evaluate all bounds and retain assumptions; until then `UNRESOLVED_AUXILIARY` |
| education | „შეყვანის ფუნქცია შეიძლება შესაძლებელი იყოს, მაგრამ ლოგიკური დონეების შეუთავსებლობა ჯერ შესამოწმებელია“ |
| no claim | „2×10 kΩ ყველასათვის უსაფრთხოა“; „VDD max იგივეა, რაც input 5 V tolerance“; „ჩართვა ჩვევით უსაფრთხოა“ |
| independent oracle | compare versioned operating/electrical tables, exact profile, formula with bounds, then C once available; any missing upper/lower bound→`UNKNOWN` |

**განსაკუთრებული დასკვნა:** Adafruit-ის ვებგვერდზე მათივე ორ resistor-იან divider-ს მაგალითად ვხედავთ [P06]; **მხოლოდ** ომის კანონით ტიპური `5×10/(10+10)=2.5 V` რიცხვის მიღება, თუ იდეალიზებული მნიშვნელობები დაიშვა, **არ წარმოადგენს** რეალური მაღალ/დაბალ მდგომარეობის, ნაკადის, leakage/ტოლერანსისა და სამუშაო რეჟიმის უსაფრთხოების მტკიცებას. ეს ფორმულა სასწავლო illustration-ია, არა ამ fixture-ის მიღებული electrical rule.

### I06 — სინთეზური ალტერნატიული MCU (transfer test)

**მოთხოვნა:** ერთი digital input და ერთი output functional requirement satisfy without ESP32-specific branch. **`SyntheticMCU-X`** [T]: fixed named board contacts `A.1`→`DIG0`, `A.2`→`DIG1`; scope `synthetic_test_data=true`. Injected test facts: `DIG0(input=true,output=false)`, `DIG1(input=true,output=true)`, review marker `TEST_ONLY_SYNTHETIC`, source class synthetic.

| ელემენტი | გადაწყვეტილება |
|---|---|
| authority | synthetic fixture only, **არ არის** რეალური მწარმოებლის მონაცემი |
| hard result | for `GPIO_OUT`, `A.1→REJECTED/FAIL` within synthetic oracle and `A.2→ELIGIBLE/PASS` only when deterministic synthetic verifier fixture explicitly permits |
| transfer value | matching algorithm uses typed `requested_function`, `terminal mapping`, `capability facts`, not string literal `ESP32` |
| unknown test | delete `A.2` mapping → `UNKNOWN` not `PASS`; replace scope with physical device → schema/review gate must reject synthetic authority |
| no claim | „SyntheticMCU-X არსებობს ბაზარზე“ ან „ეს GPIO properties რეალურ motherboard-ს ეკუთვნის“ |
| educational | clear „სატესტო ხელოვნური მოწყობილობა“ label and exact reason code |
| independent oracle | synthetic input fixture + pure expected truth table, re-run with same fixture digest |

**სცენარების დასკვნა:** I01-ში ზოგიერთ *GPIO check*-ზე PASS-ია შესაძლებელი; I02-ში function matching ცალკეა; I03-ში სტრუქტურა არსებობს, electrical fact არა; I04/I05 სრულ circuit acceptance-ს **არ ფარავენ**; I06 ამოწმებს device-specific hardcoding-ის არყოფნას. ამ მაგალითების ერთ UI-ში გაერთიანება არ ქმნის ავტომატურ circuit verifier-ს.

## 14. Maintenance, revision control, bounded catalog growth

**სამი დამოუკიდებელი ტრეკი:**

- **Data acquisition:** მოთხოვნებიდან frequency და component family-ის დალაგება; კანონიერი source discovery; parser candidate; **არ** გადადის engineering trust-ში. მიღწევა იზომება `valid_candidate_recall`-ით.
- **Engineering admission:** exact board/part scope, licensed use, reviewer, source-ledger, fixed regression → admission; სტატუსის კონტროლი claim-level; წარმატება იზომება false-positive admission rate და independently reproducible judgments-ით.
- **Educational enrichment:** ქართულ ენაზე review-დამტკიცებული explanations/concepts + hint templates; correction quality/learner comprehension, უსაფრთხოების ავტორიტეტის გარეშე.

**რევიზიის სცენარები და შედეგი:**

| Change detected | impact scope | mandatory transition |
|---|---|---|
| manufacturer datasheet edition changed (e.g. v1.9→v2.1) | exact affected claim + board/silicon conditions | `NEEDS_REVIEW`; source diff and manual claim requalification |
| ESP-IDF header / GPIO mask changed | exact chip target, release, affected B rule input | GPIO factset revision and B's own regression; old test passes do not auto-transfer |
| schematic or board contact changed | all mapping claims for board exact revision | mapping status `UNKNOWN` until pin table cross-reviewed; downstream findings invalidated |
| package pad mapping corrected | structural import + all affected instances | quarantine affected device join; new CORE catalog/definition digest and regression |
| component discontinued/stock changed | procurement recommendation | stock/availability refresh; historical electrical truth retained with source version |
| two same-scope sources contradict | affected property | `CONFLICTING` with claim IDs; prohibit positive inference |
| translation/concept text corrected | educational hint only | hint template revision, no rewriting engineering result |
| legal status revised | source distribution rights | halt prohibited reuse/export immediately; legal review; engineering facts separately tracked |

**Change detection cadence:** upstream release/tag scan or deliberate manual check (proposal: periodic batching, plus immediate handling of reported discrepancy); this is a *proposed process*, not an existing automated service. Avoid blind polling of manufacturer pages. Archive previous exact source version only where rights permit; otherwise preserve locator/version/reviewer snapshot/digest when lawfully obtained. Revalidate against **both** the previous and new oracle; irreversible deletion of provenance prohibited [D].

## 15. ეკონომიკა — სამი ოპერაციული სტრატეგია და ექსპერიმენტი

**არ არსებობს ამ ეტაპზე გაზომილი per-component ingestion benchmark.** Research E-ის ქვემოთ მოხსენიებული დიაპაზონები არის *დაგეგმვის შეფასებები*; ისინი არ უნდა აღიწეროს როგორც 2026-11-20-ზე გატარებული კვლევის გაზომილი შედეგი [E01].

| განზომილება | A. მთლიანად ხელით | B. official structure parse + human review (**SELECT**) | C. automatic discovery/extraction + human admission (**PILOT**) |
|---|---|---|---|
| პირველი schema/parser | ყველაზე იაფი | წინასწარი parser/ledger ღირებულება, DATA-001 ნაწილი უკვე შესრულებულია | ბევრი parser/LLM/QA maintenance, high variance |
| ახალი generic package | repeated manual data entry | LibrePCB CC0 reusable package/pad mapping; review | flexible discovery, but identity false matches გაიზრდება |
| exact MPN electrical | ხელით, მაღალ ავტორიტეტით | **ისევ** manual claim qualification; სტრუქტურული იმპორტი არ ანაცვლებს ამას | LLM extraction proposal-ს მაინც იგივე reviewer სჭირდება |
| source/legal risk | დაბალი, თუ link only | manageable pinned CC0 subset | მაღალი scraping/ToS/third-party data risk |
| false positive risk | reviewer error | parser join error + reviewer error | retrieval/extraction error + reviewer error + hidden source quality |
| runtime/API/cloud | offline, negligible | offline parsing/SQLite + existing tests; no mandatory paid API | source lookup/API recurring and token cost unless fully local; measured later |
| maintenance | every fact manually | version/diff + scoped impact | extractor drift/website format failures, additional review |
| family scaling | linear effort | fast where good official structural coverage | candidate recall higher, admission bottleneck not removed |
| Georgian education | manual mapping | structured source-backed templates reusable | generation can speed drafting but human factual gate remains |
| recommendation | fallback for rare/critical items | **main approach** | only bounded, zero trust-promotion experiment |

**Research E-ის შეფასებებიდან გამოსაყენებელი მაგალითი:** სტრუქტურული source თუ უკვე სწორი exact part-ით არსებობს, 0.5–2 საათის ტიპური intake ვარაუდი იქნა შემოთავაზებული; MPN/scope evidence join-ზე 4–12 საათის ვარაუდი, parser setup-ზე 12–30 საათი. ეს კონკრეტული შეფასება **არ არის** DATA-001-ის რეალური დროის გაზომვა; ბიუჯეტისთვის გამოიყენება მხოლოდ sensitivity analysis-ში [E01].

**შემოთავაზებული წინასწარი measurement design (არა Codex task):** აირჩეს 12 დასრულებული, სხვადასხვა family-ის specimen: 2 dev boards, 2 ultrasonic/distance, 2 resistors, 2 LED, 2 translators, 2 I2C sensors. თითო family-ში ერთი სრულად დოკუმენტირებული და ერთი identity-confounded case. A/B/C-ს მიეცეს იგივე ბრმად შეფასებული source package და fixed oracle; ჩაწერეთ stopwatch per stage (source discovery, legal check, identity, parser, electrical claim, review, regression, Georgian hint), accepted false fact count, source edition mismatch count, number of manual touches, review rework, runtime cost `$` (measured), unresolved identity fraction. Report median, p90 and uncertainty intervals **მხოლოდ** რეალურ მონაცემზე. Independent reviewer-ს არ ეცოდინება source path-ის ალგორითმის არჩევანი შეფასებისას. C ჩაითვალოს უკეთესად მხოლოდ მაშინ, თუ **engineering admission-ის შეცდომის არაგაზრდით** measured reviewer-hours/material maintenance გაუმჯობესდება; ადრე დადგენილი ROI threshold არ არსებობს.

**ხარჯის საბაზისო პრინციპი:** ამ მოცულობით SQLite, local parsers, source links და static concept copy საკმარისია; hosted vector database და paid third-party API არ წარმოადგენს აუცილებლობას. ეს არის არქიტექტურული შესაძლებლობის შეფასება, **არა** გარანტირებული $0 საოპერაციო ბიუჯეტი (ელექტროენერგია, reviewer labor, CI, hosting რჩება).

## 16. დამოუკიდებელი acceptance benchmark — 16 შემთხვევა

**სატესტო პროტოკოლი:** ყველა oracle უნდა მოდიოდეს upstream წყაროდან/განსაზღვრული synthetic premise-იდან, არა matcher-ის საკუთარ გამოთვლით პასუხთან შედარებიდან. ყველა case-ს აქვს ფიქსირებული `{catalog_digest, factset/source_digest, query, operating_mode, exact identity}`, და უნდა გაიაროს repeat/reordering tests. ქვემოთ `S` = source oracle, `ALG` = დამოუკიდებლად შემოწმებული მოსალოდნელი ნაბიჯი, `E` = educational effect. **Test plan; tests ამ კვლევაში არ გაშვებულა.**

| ID / fixed input | დამოუკიდებელი expected result | source evidence / ALG | failure classification / educational effect / reproducibility |
|---|---|---|---|
| **AT-I01:** exact `YAGEO RC0603FR-0710KL`, accepted source scope და *ხელით დამოწმებული* package join fixture | `EXACT_IDENTITY_MATCH`, მხოლოდ იმ reviewed fields-ში | S: exact YAGEO spec + approved mapping; ALG: equality on MPN/package/revision→admission | incorrect alias→`IDENTITY_CONFLICT`; E: კონკრეტული პროდუქტის დასახელება; R: locked manufacturer artifact + reviewed join |
| **AT-I02:** `generic_hc_sr04_family` მოთხოვნით exact OEM revision | `UNRESOLVED_IDENTITY`, no exact-match pass | S: Adafruit SKU listing lacks exact OEM revision; ALG: family vs MPN inequality | false promotion→`IDENTITY_FALSE_PROMOTION`; E: რას ნიშნავს SKU/OEM; R: fixed SKU snapshot |
| **AT-I03:** J3.9→GPIO18, `GPIO_OUT`, ACTIVE with approved B factset | B `PHYSICAL_CAPABILITY PASS` **only** | S: Espressif official + pinned B ledger; ALG: resolve terminal→delegate B | false reject→`FUNCTION_FALSE_NEGATIVE`; E: დასახელებული GPIO; R: snapshot+factset+ruleset digests |
| **AT-I04:** J2.5→GPIO34, `GPIO_OUT`, ACTIVE | B `FAIL` input-only | S: GPIO summary + board table; ALG: exact join→B | false pass→`UNSAFE_FUNCTION_FALSE_POSITIVE`; E: input-only; R: same pins |
| **AT-I05:** delete board contact→SoC mapping while keeping GPIO18 silicon capability | `UNKNOWN/MISSING_MAPPING`, not inferred by label | S: incomplete synthetic edit of real structural fixture; ALG: B typed mapping validation | false pass→`MAPPING_BYPASS`; E: `missing mapping`; R: controlled single-deletion diff |
| **AT-I06:** #3942 supply/echo mandatory exact electrical bound set to `UNKNOWN` | `UNRESOLVED_MISSING`, no circuit compatibility PASS | S: incomplete electrical evidence bundle; ALG: mandatory property completeness | false pass→`VOLTAGE_UNKNOWN_BYPASS`; E: „დოკუმენტაცია აკლია“; R: same absent fields |
| **AT-I07:** two same-scope conflicting manufacturer claims for max/current | `CONFLICTING`, quarantined | S: two reviewed fixture source locator records; ALG: condition-aware conflict-set | silent overwrite→`EVIDENCE_CONFLICT_IGNORED`; E: წყაროთა წინააღმდეგობა; R: versioned conflict fixture |
| **AT-I08:** cheap resistor, no admitted power rating, power hard | `UNRESOLVED_MISSING` despite cheapness | S: DATA-001 generic resistor + missing rating; ALG: hard before soft rank | false preference override→`RANK_LAUNDERING`; E: ფასის vs safety; R: fixed price and missing bound |
| **AT-I09:** HC-SR04 + MCU, required verified level-shifter absent | `AUXILIARY_REQUIRED_UNVERIFIED` or `UNKNOWN`, no safe circuit | S: Adafruit Echo 5 V listing + missing C; ALG: required_auxiliary dependency | false safe→`AUXILIARY_BYPASS`; E: logic-level conversion; R: fixed unresolved component set |
| **AT-I10:** `driver_required=true`, matching hardware candidate but no supported SDK version/driver evidence | `FIRMWARE_UNSUPPORTED_OR_UNKNOWN`, not eligible as full goal fulfillment | S: fixed SDK driver catalog no matched row; ALG: firmware predicate separate | false full match→`DRIVER_BYPASS`; E: driver availability; R: exact SDK version fixture |
| **AT-I11:** manufacturer source edition changes claimed electrical bound | dependent recommendation `STALE_REVALIDATION_REQUIRED` | S: old/new source fixtures with controlled one-field diff; ALG: reverse dependency walk | stale PASS→`REVISION_BYPASS`; E: „წყარო შეიცვალა“; R: two pinned digests |
| **AT-I12:** two `ComponentInstance`s same `user_label=LED`, different `instance_id` | separate terminal/finding/hint linkage | S: CORE snapshot schema; ALG: key by instance+terminal | cross-talk→`INSTANCE_COLLISION`; E: ზუსტი მოწყობილობის მონიშვნა; R: reorder/shuffle fixture |
| **AT-I13:** B finding `GPIO34 output FAIL` + reviewed `gpio.input_only` template | Georgian hint cites physical contact, reason, source and limitations | S: B report + Espressif GPIO/board docs; ALG: validated finding-to-context join | incomplete provenance→`HINT_TRACE_FAILURE`; E: correct pedagogical hint; R: fixed locale/template version |
| **AT-I14:** injected false hint „GPIO34 output-capable“ inconsistent with finding | reject/suppress hint, engineering finding unchanged | S: B `FAIL` oracle; ALG: claim-span validator rejects contradiction | incorrect wording→`EDUCATIONAL_FACT_CONFLICT`; E: fallback to safe wording; R: same bad output |
| **AT-I15:** synthetic MCU-X, two ports capabilities as defined I06 | `A.1 OUTPUT→FALSE`, `A.2 OUTPUT→TRUE` in test scope, no real admission | S: explicit synthetic fixture; ALG: same generic predicate engine | ESP32-only branch→`DEVICE_HARDCODING`; E: synthetic label; R: seedless, fixed fixture |
| **AT-I16:** unknown new component, indexed by vendor search only, no review | visible in discovery with `NOT_ENGINEERING_ADMITTED`, not recommended as verified | S: seeded unreviewed component candidate; ALG: admission gate | false PASS→`DISCOVERY_TRUST_LAUNDERING`; E: available data vs verification; R: same catalog state |

**დამატებითი metamorphic properties:** (1) wire/order permutation changes neither evidence fact nor verdict; (2) changing mere display label changes no identity/verdict; (3) removing required evidence can only degrade/hold status, never upgrade; (4) replacing exact reviewed claim with `synthetic` cannot maintain production engineering admission; (5) same source+rule+snapshot digests yield identical report; (6) translation change cannot change B findings; (7) cost preference changes only ordering among same hard-gate class. **Benchmark gate:** zero false-positive hard PASS on this fixed suite + all unknown propagation cases; this is a proposed acceptance threshold, not an observed score.

## 17. Proposed typed interfaces — application-layer, not CORE schema migrations

**წაკითხვის წესი:** ქვემოთ მოცემული field name/type არის **საბოლოო API-ს წინადადება**, არა უკვე არსებული Python კლასი. სვეტებში `M` = mandatory, `C` = conditional, `O` = optional; `UNKNOWN` აღწერს field absence-ის fail-closed ქცევას; `oracle` არის ვალიდაციის დამოუკიდებელი წყარო/წესი. `Ref` ტიპები კომპოზიტური existing IDs-ს აკავშირებს; v1-ში `extra=forbid`, immutable და serializable ფორმა სასურველია, მაგრამ ეს **არ არის** განხორციელების ნებართვა.

### 17.1 `RequiredCapabilityQuery`

**როლი:** H-დან მიღებული formal requirement-ის matching-სთვის გამოყენებადი დადასტურებული წარმოდგენა; არა sensor specification და არა engineering rule.

| Field : type | განმარტება / source of truth | M/C/O და მოქმედების პირობა | UNKNOWN და consumer / independent oracle |
|---|---|---|---|
| `query_id: Identifier` | immutable requirement reference, formal intent layer H | M | missing→invalid; selection trace; oracle unique within query batch |
| `origin_requirement_ids: tuple[Identifier]` | H-ის მოთხოვნების ბმა | M, nonempty | missing→invalid; educational trace; oracle formal spec entries exist |
| `capability_key: Identifier` | curated vocabulary, e.g. `distance.measure` | M | unknown key→`UNSUPPORTED_CAPABILITY`; typed catalog vocabulary oracle |
| `requested_interface: Identifier?` | user/H-declared I2C, digital pulse, UART etc | C when user demands specific interface | absent with mandatory interface→`UNRESOLVED`; matcher; oracle query requirement |
| `identity_constraint: ExactIdentityPredicate?` | user demands MPN/board/revision or family allowed | C if exact profile required | unspecified exact constraint not silently guessed; identity gate; oracle explicit spec |
| `operating_context: ContextRef` | requested ACTIVE/RESET, supply, environment, firmware version where declared | M as context object, fields may be unknown | missing required mode→`UNRESOLVED`; B/C/L; oracle source-supported mode set |
| `hard_constraints: tuple[ConstraintPredicate]` | H approved mandatory engineering conditions, with `source=USER_REQUIREMENT` (not manufacturer) | M, possibly empty for discovery-only | unknown predicate→unsupported; selection; oracle normalized requirements |
| `preferences: tuple[PreferencePredicate]` | cost, size, ease, examples, each optional | O | missing preference→no penalty; ranker; oracle user intent unchanged |
| `requirement_snapshot_digest: Digest` | frozen typed H spec payload | M | missing/stale→invalid; cache + evidence; oracle canonical digest |

### 17.2 `ComponentCandidate`

**როლი:** search result with explicit identity and admissibility; cannot by itself support a safe circuit assertion.

| Field : type | განმარტება / truth | M/C/O | UNKNOWN, consumer / oracle |
|---|---|---|---|
| `candidate_id: Identifier` | stable index key, generated by catalog | M | duplicate→invalid; search/display; uniqueness oracle |
| `definition_ref: DefinitionIdDigest?` | CORE catalog definition+digest if actually available | C if CORE-backed | absent→search-only; CORE resolver; oracle exact digest |
| `identity: ScopedIdentity` | manufacturer/Mpn/revision/retailer-kind from curated source | M | family or retailer doesn't count exact; identity gate; source-MPN equality |
| `identity_state: Enum` | `EXACT_VERIFIED/LISTING_ONLY/FAMILY_ONLY/CONFLICTING/UNKNOWN` | M | unknown→no exact pass; ranker; oracle source scope |
| `capability_claim_ids: tuple[Identifier]` | curated claim references, never free-form truth | M, may be empty | empty→not functionally admitted; matcher; ledger foreign keys |
| `admission_state: Enum` | `DISCOVERED...ENGINEERING_ADMITTED...` **claim eligibility summary** | M | must not override individual claim gate; report; validated transition ledger |
| `proposed_auxiliaries: tuple[AuxiliaryRequirement]` | unverified/verified support dependencies | O | unresolved part→candidate flagged; synthesizer J; source requirement |
| `unresolved_ids: tuple[Identifier]` | missing exact facts, conditions, rights | M, may empty | critical unresolved→no verified group; report; completeness oracle |
| `source_version_refs: tuple[SourceVersionRef]` | concrete upstream files/editions | M | no trace→discovery only; revision system; source ledger pins |

### 17.3 `ComponentCapabilityFact`

**როლი:** one scoped property proposition, not an unrestricted dictionary of manufacturer „truth“. Key must be semantically typed; physical and electrical categories have different authorities.

| Field : type | მნიშვნელობა / truth | M/C/O | UNKNOWN, consumer / oracle |
|---|---|---|---|
| `fact_id: Identifier` | immutable curated fact ID | M | missing→invalid; evidence graph; uniqueness |
| `subject_ref: ScopedIdentityRef` | MPN/board/module/terminal owner | M | family-only cannot prove MPN; matcher; source scope proof |
| `capability_key: Identifier` | `gpio.output`, `ultrasonic.distance`, `logic.echo`, etc. | M | unsupported→discovery only; matcher/verifier adapter; vocabulary |
| `value: TypedValue` | bool/enum/interval/quantity reference; no stringly numeric fallback | M, except explicit `UnknownValue` | missing value→unknown; predicate evaluator; type+unit compatibility |
| `bound_kind: Enum?` | exact `min/max/typ/abs/recommended` where numeric | C for quantitative | missing on safety limit→not admitted; C; manufacturer table header |
| `unit: UnitRef?` | SI or defined normalized unit; store original separately | C quantitative | unknown unit→not admitted; C; conversion dimension oracle |
| `operating_condition: ConditionSet` | mode/supply/temp/load/package constraints | M, possibly `CONDITIONS_UNKNOWN` | cannot imply all environments; matcher+C/L; condition coverage |
| `evidence_ids: tuple[Identifier]` | link to source claims, review records | M for engineering facts; nonempty | empty→discovery claim only; gate/hint; provenance join |
| `authority_class: Enum` | manufacturer/SDK/board/retailer/community/synthetic/derived | M | wrong authority→hold; admission; source type and claim purpose |
| `review_status: Enum` | approved/unverified/conflicting/missing, preserving CORE semantics | M | anything not approved→no engineering pass; gate; reviewer event |
| `catalog_revision: Digest` | exact version of fact universe | M | stale→needs review; cache/verifier; pinned artifact digest |

**აქ მთავარი ზღვარია:** ეს არის sidecar data contract. Quantitative `TypedValue` **არ უნდა** ჩაიტენოს CORE `EvidenceClaim.value`-ის დაშვებული სტრუქტურის დარღვევით; გააკავშირეთ existing `claim_id`/`source_document_id`-ით.

### 17.4 `EvidenceQualification`

**როლი:** legal+scientific gate თითო claim-ზე, და არა ავტომატურად მთელ კომპონენტზე.

| Field : type | მნიშვნელობა / truth | M/C/O | UNKNOWN, consumer / oracle |
|---|---|---|---|
| `qualification_id: Identifier` | audit event | M | absent→invalid; ledger; unique ID |
| `fact_id: Identifier` | exactly one proposed fact | M | unknown fact→invalid; gate; foreign key |
| `source_refs: tuple[SourceLocatorRef]` | publisher, URL, edition, line/table/pin, digest if legal | M | no locator→`NEEDS_REVIEW`; evidence viewer; reproducible source access |
| `rights_state: Enum` | per-artifact allowed use/action, owner/legal review | M | `UNKNOWN/RESTRICTED`→cannot copy/distribute; intake; license file/terms |
| `identity_basis: Enum` | exact manufacturer, retailer, generic, synthetic | M | not exact→MPN positive gate fails; matcher; exact orderable verification |
| `condition_scope: ConditionSet` | applicable mode/supply/load/temp | M | no conditions on critical numeric bound→hold; C; official tables |
| `review_decision: Enum` | `ENGINEERING_ADMITTED/NEEDS_REVIEW/CONFLICTING/REJECTED/...` | M | anything not admitted→no positive result; admission; authorized reviewer event |
| `review_record_ref: Identifier?` | reviewer, timestamp, rationale, evidence comparison | C for human admission | missing→no engineering gate; audit; signed/versioned review log |
| `conflicting_fact_ids: tuple[Identifier]` | same-scope contradiction set | M, possibly empty | unresolved conflicts force HOLD; rule/hint; independent cross-claim comparison |

### 17.5 `ConstraintMatchResult`

**როლი:** ერთი hard/soft predicate-ის შედეგი, სანამ ნამდვილი electrical verifier-ს ცალკე საკუთარი ანგარიში აქვს.

| Field : type | მნიშვნელობა / truth | M/C/O | UNKNOWN, consumer / oracle |
|---|---|---|---|
| `query_id: Identifier` | requirements source | M | invalid if absent; report; requirement snapshot lookup |
| `candidate_id: Identifier` | scoped candidate | M | missing→invalid; report; candidate ledger |
| `constraint_id: Identifier` | typed predicate ID | M | unknown→unsupported; report; formally declared constraint |
| `constraint_class: HARD/SOFT` | formal requirement | M | untyped→invalid; ranking; user spec |
| `match_state: TRUE/FALSE/UNKNOWN/CONFLICT/NOT_EVALUATED` | deterministic result; no score conversion | M | unknown/conflict never true; selector; truth-table oracle |
| `provenance_fact_ids: tuple[Identifier]` | facts actually used | M, may empty only unknown reason | no positive provenance→unresolved; educational; claim ledger |
| `missing_prerequisite_ids: tuple[Identifier]` | exact missing limits/mapping/driver | M, can empty | present hard prerequisite→unknown; report; dependency enumerator |
| `verifier_result_ref: FindingRef?` | authoritative B/C/L finding where invoked | C if check assigned to B/C/L | if uninvoked no PASS claiming hardware; report; matching exact snapshot/ruleset |
| `scope_digest: Digest` | requirement+candidate+conditions fingerprint | M | stale→invalidate; reproducibility; deterministic digest |

**ფუნდამენტური სხვაობა:** `match_state=TRUE` შეიძლება ნიშნავდეს მხოლოდ *functional predicate* satisfied; full electrical PASS-ს მოითხოვს შესაბამისი independent verifier `FindingRef`. Consumer-მა არ უნდა დააკავშიროს ეს ორი მნიშვნელობა ერთ „green compatible“ სტატუსში.

### 17.6 `CandidateSelectionReport`

| Field : type | მნიშვნელობა / truth | M/C/O | UNKNOWN, consumer / oracle |
|---|---|---|---|
| `report_id: Digest` | canonical report identity | M | absent→invalid; history/UI; hash recomputation |
| `requirements_digest: Digest` | freeze H specification | M | mismatch→stale; report/cache; H snapshot |
| `catalog_digest: Digest` | CORE catalog snapshot | M if CORE-backed | missing→discovery-only; CORE/selection; catalog validator |
| `capability_index_revision: Digest` | derived sidecar version | M | mismatch→re-run; search; index manifest |
| `candidate_results: tuple[CandidateAssessment]` | deterministic ordered groups, NOT unsafe global scores | M | per-result missing hard gate shown unresolved; UI; comparator oracle |
| `not_evaluated_scopes: tuple[Identifier]` | GPIO/electrical/firmware missing owners | M, possibly empty only proven complete | without coverage→explicitly `NOT_EVALUATED`; UI/H; coverage report |
| `source_revision_refs: tuple[SourceVersionRef]` | source versions used | M | unpinned source→no production positive; revision engine; ledger |
| `ordering_policy_version: Identifier` | published lexicographic ordering | M | policy mismatch→stale ranking; UI; comparator fixtures |
| `validation_summary: BoundedStatus` | `DISCOVERY_ONLY/FUNCTION_REVIEWED/PARTIALLY_VERIFIED/REJECTED` | M | no `SAFE_CIRCUIT` unless full relevant verifier coverage, currently unsupported; UI; coverage oracle |

### 17.7 `ComponentKnowledgeContext`

**როლი:** component-specific structured knowledge for Research H; does not parse PDFs at user request time.

| Field : type | მნიშვნელობა / truth | M/C/O | UNKNOWN, consumer / oracle |
|---|---|---|---|
| `context_id: Digest` | deterministic context fingerprint | M | invalid if absent; H; canonical digest |
| `component_identity: ScopedIdentityRef` | exact/retailer/generic identity including limitation | M | unknown shown explicit; H; identity ledger |
| `instance_ref: Identifier?` | CORE `instance_id` | C when tied to circuit | no instance→generic explanation only; H; snapshot membership |
| `terminal_ref: TerminalRef?` | exact physical contact | C when pin-specific | cannot describe pin if absent; H; CORE resolve |
| `requirement_ids: tuple[Identifier]` | H intent and capability need | M, may empty for encyclopedia-style | if absent no requirement-match claim; H; H snapshot |
| `capability_fact_ids: tuple[Identifier]` | reviewed function/role facts | M, may empty | no factual claims if empty; H; qualification ledger |
| `constraint_result_refs: tuple[Identifier]` | matching/verifier outputs already computed | M, may empty for generic learning | cannot claim pass/fail absent finding; H; report ledger |
| `condition_scope: ConditionSet` | known operating modes/loads | M | missing conditions limit claimed scope; H; source facts |
| `missing_fact_ids: tuple[Identifier]` | structured unknowns/contradictions | M, may empty | must render if nonempty; H; admission ledger |
| `concept_refs: tuple[Identifier]` | pedagogically reviewed concept IDs | O | missing→use generic safe template; H; concept registry |
| `alternative_candidate_ids: tuple[Identifier]` | explicitly status-labelled alternatives | O | cannot assert safe without evidence; H; selection report |
| `recommendation_limits: tuple[Identifier]` | prohibition of unsafe/topology inference | M | absent→fail-close hint builder; H; policy table |
| `snapshot_digest: Digest?` | CORE circuit snapshot | C for finding-specific hint | mismatch→no contextual hint; H; B report snapshot |

### 17.8 `ComponentEducationalEvidence`

| Field : type | მნიშვნელობა / truth | M/C/O | UNKNOWN, consumer / oracle |
|---|---|---|---|
| `hint_evidence_id: Digest` | normalized hint fact payload | M | absent→invalid; renderer; canonical digest |
| `context_id: Digest` | exact component knowledge context | M | mismatch→reject; H; context lookup |
| `finding_ref: FindingRef?` | `finding_id,reason_code,rule_id,snapshot_digest` | C for pass/fail cause hint | absent→cannot claim verifier judgment; H; B/C report join |
| `category: HintCategory` | one of seven reviewed categories | M | unknown→fallback; renderer; allowed enum |
| `fact_spans: tuple[ClaimSpan]` | each factual sentence fragment → fact/source claim IDs | M where factual text exists | missing citation→suppress fragment; validator; reviewed claim ID oracle |
| `educational_concept_refs: tuple[Identifier]` | reviewed learning concepts | O | absent→plain source-backed wording; renderer; concept registry |
| `suggested_action: ActionKind?` | e.g. `SELECT_DIFFERENT_TERMINAL`, `VERIFY_VOLTAGE` | O; not a synthesis instruction | if no safe action known→null; UI; action whitelist |
| `uncertainty_disclosure: tuple[Identifier]` | all uncovered checks and identity limitations | M | omitted mandatory unknown→reject hint; H; coverage comparison |
| `locale: Literal['ka-GE']` | Georgian localization | M for first product | unsupported locale→fallback; UI; localized template registry |
| `template_version: Identifier` | exact reviewer-approved educational copy | M | stale template→rerender; H; template digest |
| `status: VERIFIED_EXPLANATION / LIMITED / NEEDS_REVIEW` | explanatory quality/authority **not electrical** | M | unknown→needs-review; UI; factual consistency oracle |

### 17.9 `KnowledgeRevisionImpact`

| Field : type | მნიშვნელობა / truth | M/C/O | UNKNOWN, consumer / oracle |
|---|---|---|---|
| `impact_id: Digest` | source-version-diff impact identity | M | absent→invalid; maintenance; canonical version diff |
| `changed_source_ref: SourceVersionDelta` | old/new source edition or rights change | M | no validated old/new scope→needs review; ledger; pinned artifacts |
| `change_kind: Enum` | `ELECTRICAL/STRUCTURAL/IDENTITY/FIRMWARE/RIGHTS/EDUCATIONAL/PROCUREMENT` | M | unclassified→hold all dependent claims; impact engine; diff reviewer |
| `affected_fact_ids: tuple[Identifier]` | reverse-index reachable claims | M, possibly empty | cannot assume none without index integrity; reviewer; DAG walk |
| `affected_rule_refs: tuple[RuleRef]` | dependent B/C/L rule versions, where known | M, may empty | unknown dep→conservative hold; verifier owner; actual rule→claim linkage |
| `affected_report_ids: tuple[Digest]` | stale candidate/verifier outputs | M, possibly empty | changed critical claim→invalidate; reporting; diff oracle |
| `affected_hint_ids: tuple[Digest]` | stale Georgian explanations | M, possibly empty | suppress/re-render; H; claim-span reverse index |
| `required_revalidation: tuple[GateId]` | exact steps to reactivate | M | no automatic promotion; reviewer; policy gate list |
| `disposition: REVALIDATE / QUARANTINE / NO_ENGINEERING_CHANGE` | triaged effect, authorized reviewer | M | unknown→quarantine; operations; independent reviewed diff |
| `audit_record_ref: Identifier` | who/when/why approved new status | M for final disposition | absent→pending; governance; authorizer log |

### 17.10 Cross-interface invariants

`ComponentCandidate.identity` არ უნდა მიეკუთვნოს სხვა exact MPN-ს; `EvidenceQualification.fact_id` უნდა დაემთხვეს capability fact-ს; `ConstraintMatchResult.verifier_result_ref` უნდა ემთხვეოდეს კონკრეტულ selected instance/terminal/snapshot-ს; `ComponentEducationalEvidence` ვერ გამოაცხადებს `PASS` თუ შესაბამის finding-ში `UNKNOWN/FAIL/NOT_EVALUATED` წერია; `KnowledgeRevisionImpact`-მა უნდა იპოვოს ყველა დამოკიდებული fact/report/hint ან დააფიქსიროს incomplete dependency graph და fail closed. უარყოფილ proof path-ს შეუძლია დატოვოს discoverability, მაგრამ **ვერ** ასტიმულირებს production-ready selection-ს.

**არცერთი ეს schema არ ითხოვს CORE-ის rewrite-ს**; საჭიროების შემთხვევაში ის არის standalone, immutable, validated application-layer DTO/sidecar. Canonical `TerminalRef`, `CatalogSnapshot` და B report რჩება მფლობელებად [D].

## 18. Research H-თან და J/L/C-თან დამოკიდებულებები

**Upstream H (formal Georgian intent):** უნდა მიაწოდოს `requirement_id`, capability vocabulary, hard/soft distinction, user-supplied vs inferred assumptions, accepted operating context, confirmed ambiguities და digest. `„მანძილი 30 სმ-ზე ნაკლები“` მხოლოდ firmware/application outcome intent-ია; ის ვერ იქცევა MCU input limit-ად. H-ის ქართულმა ტექსტმა შეიძლება ბუნებრივი ენის სინონიმები იპოვოს, მაგრამ ფიზიკური მონაცემის ავტორიტეტი არ ეძლევა.

**Research I (this report):** ადგენს discoverable facts, admission state, identity, candidate grouping, evidence context. I არ აგებს კავშირებს ავტომატურად და არ ასრულებს ელექტრულ შედარებებს.

**Future J (circuit synthesis):** იღებს verified capability query-ს და bounded candidates-ს, ქმნის typed *circuit hypothesis* with terminal-to-net proposals, power nets, supporting parts, constraints and unresolved proof obligations; invokes CORE connectivity. J-ის ნამუშევარი დარჩება `PROPOSED` სანამ შესაბამის B/C verified outputs არ დაურთავს.

**Existing B (GPIO):** receives exact CORE snapshot + own `GpioFactSet`, returns its own report. No second GPIO code path. **Future C (electrical):** read sidecar numeric intervals, source conditions, conductance/voltage formula assumptions, build own findings; **future L (firmware):** check driver support and active configuration. Neither C nor L is assumed implemented today.

**Downstream H (educational feedback):** consumes `ComponentKnowledgeContext` joined to authoritative finding. One finding could have multiple pedagogical explanations, but **engineering status immutable**.

## 19. არქიტექტურული ალტერნატივები და რეკომენდაცია

| ვარიანტი | პირობითი სარგებელი | ფასი/რისკი | არჩევანი |
|---|---|---|---|
| **A. ხელით კურირებული flat facts** | უმცირესი ტექნიკური ზედნადები, ძალიან მკაფიო audit | რთული ზრდა, განმეორებითი input | **FALLBACK** კრიტიკულ ან იშვიათ source-ზე |
| **B. CC0 LibrePCB structural importer + typed sidecar + human claim admission + indexed retrieval** | DATA-001 რეალური ბაზა, canonical CORE უცვლელი, უფასო dependency path, explainable | ყოველი electrical rating-ის დამოუკიდებელი review; engineering effort | **SELECT FOR OWNER REVIEW** |
| **C. automated official source discovery/extraction + human admission** | recall, breadth, initial data collection სავარაუდოდ სწრაფი | identity confusion, parser drift, legal friction, LLM errors; measured gain unknown | **SMALL EXPERIMENT ONLY**, ვერ შევა trust path-ში თვითნებურად |
| **D. full knowledge graph + vector DB + LLM engineering agent** | გრძელვადიანი research exploration პოტენციალი | complex ops, ontology and provenance debt, false positive safety risk | **REJECT for MVP**, revisit only after measured retrieval failure |
| **E. proprietary simulator/vendor catalog as live truth** | demos და ბევრი visualization | license/payment/lock-in, simulator physics ≠ safety | **REJECT as core authority** |

**Decision logic:** B+bounded manual A is technically sufficient to answer the *first meaningful product question*: can selected exact board pin and candidate sensor functionally meet a narrowly specified requirement, with transparent unverified voltage/circuit conditions? It is **not** sufficient to say the complete ESP32+HC-SR04+LED system works safely. Proof obligations are not product bugs to hide; they're what prevents false confidence. B maximizes meaningful reuse of current working code; C earns scope only from measured improvements, not from „AI agents discover everything“ theory [D].

## 20. Critical unknowns and owner decision requests

| ID | Unknown / current evidence | Owner decision required (research, not implementation) |
|---|---|---|
| U-I01 | real purchased `Adafruit #3942` batch/OEM/PCB revision not confirmed | authorize only **retailer-scope** demo vs require photographed exact lot and manufacturer documents |
| U-I02 | actual DevKitC user's board hardware revision and module variant may differ from official V4 | mark demo `documented-profile only`, not universal real-hardware compatibility |
| U-I03 | exact YAGEO MPN↔LibrePCB footprint/package join held | whether to run a bounded independently reviewed mapping study before any resistor circuit recommendation |
| U-I04 | no exact LED electrical source-backed part in present fixture | hold safe LED circuit claims until one exact MPN and drive model are reviewed |
| U-I05 | C electrical verifier and J synthesis not approved/implemented in reviewed reference | do not present unsafe/unverified Echo / LED output wiring as solved; separate future research acceptance |
| U-I06 | Research H provided as assignment/specification; its final typed formal output contract unavailable | treat proposed H join as provisional interface; no claim of finalized H implementation |
| U-I07 | present reference commit pinned; newer branches/commits may exist; live repository head not asserted equivalent | architectural acceptance must refer to exact observed commit and compare revisions deliberately |
| U-I08 | vendor PDFs/certain data pack redistribution rights require artifact-specific assessment | permit links+curated narrowly reviewed factual claims; no bulk mirrored/vendor licensed corpus |
| U-I09 | candidates per family actual ingestion time, review speed, false-positive rate unmeasured | approve controlled A/B/C *study* before automation spend |
| U-I10 | consumer UX whether distinction `FUNCTION VERIFIED` vs `FULL CIRCUIT UNVERIFIED` is understood by learners | evaluate learning/unsafe-interpretation in usability testing; do not replace with one compatibility badge |
| U-I11 | source-to-rule dependency mapping for future C/L not established | design condition-level trace before claiming automatic invalidation coverage |
| U-I12 | driver compatibility cross-board/SDK versions absent for some parts | treat `supported driver` as user-declared mandatory/optional, not inferred from sensor class |

**კონკრეტული ასარჩევი გადაწყვეტილება:** მიიღოს თუ არა owner-მა როგორც *კვლევითი სამიზნე* B-მოდელი და სამი მკაცრად განცალკევებული outcome: `DISCOVERABLE`, `FUNCTIONALLY_EVIDENCED`, `ENGINEERING_VERIFIED_FOR_STATED_CHECKS`. თუ კი, შემდეგი ცალკე ქმედება შეიძლება იყოს interface-contract review. **ამ დოკუმენტს არ შეუძლია მისი დამტკიცება საკუთარი სახელით.**

## 21. როდის უნდა გადაისინჯოს ან შემობრუნდეს რეკომენდაცია

1. **Actual data density failure:** 12-part measurement-ში official structural coverage იმდენად დაბალია, რომ B-ის parser review-ის ფასი A-ზე მაღალი აღმოჩნდება — B→A/manual primary for affected family.
2. **Proven scale benefit:** C აჩვენებს lower reviewer minutes და თანაბარ/უკეთეს false admission rate-ს, official rights verified — extend C's *candidate discovery* scope, **not** human gate removal.
3. **Validated difficult constraints:** first product requires tens/hundreds of interdependent slots and bounded backtracking fails reproducible performance threshold — move from finite-domain to OR-Tools CP-SAT (with fixed test oracles), not directly to LLM reasoning.
4. **Cross-family evidence mismatch:** CORE model demonstrably cannot represent a required physical terminal, revision-specific mapping or contact mode even with thin adapter — propose **narrow** CORE change as separate owner decision, not universal ontology.
5. **Legal rights regression:** official library subset or selected use rights unavailable — stop that intake/export path, retain link-only/manual metadata with counsel review.
6. **High-stakes safety requirement:** users expect actual 5 V tolerance, thermal limits, battery/mains, fire/medical decisions — **block positive safety claims** until separately validated electrical models and expert review; do not lower standards to ship.
7. **New reliable vendor APIs:** manufacturer exposes structured, commercially reusable electrical/pin/part data with provenance, suitable pricing and stable schema — reassess A/B/C economics and source ranking.
8. **Educational harm measurement:** hint user tests reveal high false inference of complete safety from scoped PASS — strengthen labels/explicit limitations, reconsider hint delivery; preserve raw finding.
9. **Research H proves no stable requirement typing:** if Georgian intent is too ambiguous to freeze typed hard constraints, restrict component selection to user-confirmed structured input; do not embed guessing in matcher.

## 22. Primary sources / repository references and legal restrictions

Each reference has a specific authority scope. Links to mutable documentation must **not** be treated as immutable evidence pins; source ledger should separately store retrieved edition/digest. DOI/paper references are not required to establish an SDK's actual pin mask or a license; manufacturer and official source code have precedence for those claims.

### Project source-of-truth (exact commit)

- **[R01]** [`inventor_edu/models.py`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/inventor_edu/models.py), [`core.py`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/inventor_edu/core.py). Actual CORE types, catalog, physical terminals, net topology, digests.
- **[R02]** [`gpio_facts.py`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/inventor_edu/gpio_facts.py), [`gpio_verify.py`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/inventor_edu/gpio_verify.py). Scoped GPIO facts, rules, status and reports.
- **[R03]** [`CORE-001B source/rule ledger`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md); [`CORE-001B report`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/CORE-001B-01-REPORT.md).
- **[R04]** [`data/gpio/devkitc_32e_catalog.json`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/data/gpio/devkitc_32e_catalog.json), [`devkitc_32e_facts.json`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/data/gpio/devkitc_32e_facts.json).
- **[R05]** [`DATA-001 source/evidence ledger`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/DATA-001_SOURCE_AND_EVIDENCE_LEDGER.md), [`DATA-001 report`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/DATA-001-REPORT.md), [`pilot catalog`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/data/pilot/librepcb_resistor_catalog.json).
- **[R06]** [`demo_bridge.py`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/inventor_edu/demo_bridge.py), [`DEMO-001-REPORT.md`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/DEMO-001-REPORT.md). Test-only bounded bridge, not voltage verification.
- **[R07]** [`CORE-001A-R2-REPORT.md`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/CORE-001A-R2-REPORT.md). Typed physical-to-logical mapping scope.
- **[E01]** [`RESEARCH_E_COMPONENT_DATA_AND_EVIDENCE_PIPELINE.md`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/docs/research/raw/RESEARCH_E_COMPONENT_DATA_AND_EVIDENCE_PIPELINE.md). Baseline data/rights/cost methodology; previous research, not an autonomous authority for new facts.
- **[E02]** User-provided `RESEARCH_G_WOKWI_UX_ARCHITECTURE_AND_DEMO_STRATEGY.md` (library artifact); Wokwi UX limits, visible-label distinction and demo recommendation. **[H01]** User-provided `RESEARCH_H` assignment (2026-11-20); target not an implemented contract.
- **[R08]** [`RESEARCH_B_GPIO_VERIFICATION.md`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/docs/research/raw/RESEARCH_B_GPIO_VERIFICATION.md), [`RESEARCH_C_VOLTAGE_COMPATIBILITY.md`](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/docs/research/raw/RESEARCH_C_VOLTAGE_COMPATIBILITY.md) — supporting research, **not proof C is implemented**.

### External primary references

- **[P01]** LibrePCB official [license](https://librepcb.org/license/), [file format](https://librepcb.org/features/file-format/), Base repo [pinned license file](https://github.com/LibrePCB-Libraries/LibrePCB_Base.lplib/blob/dc037a238eb5efcc034dd9d62e5775d5c21e90e4/LICENSE.txt). **CC0 official libraries** vs **GPLv3 application** explicitly separate; CC0 does not override trademark/patent or third-party document rights.
- **[P02]** KiCad [library license and exception](https://www.kicad.org/libraries/license/). Designs using library are not automatically share-alike; **redistributing collections of library data** remains subject to required license/attribution.
- **[P03]** Espressif [ESP-IDF repository](https://github.com/espressif/esp-idf) (Apache-2.0 repository, inspect particular file SPDX and dependencies). SDK pin capability is not board schematics.
- **[P04]** Espressif [GPIO & RTC GPIO reference](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html): GPIO34–39 input-only, no software pull-up/pull-down, target-specific.
- **[P05]** Espressif [ESP32-DevKitC V4 guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html): exact header contact table, board/module differences; board clone identity not implied.
- **[P06]** Adafruit [HC-SR04 #3942](https://www.adafruit.com/product/3942) and [pinout learning reference](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/pinouts): retailer-scope pin roles, 5 V Echo statement and included resistors. Rights to scrape/redistribute are **not** established by page availability.
- **[P07]** YAGEO [RC0603FR-0710KL specsheet endpoint](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-0710KL); exact byte/version pin is documented in DATA-001 ledger. **Manufacturer MPN does not prove LibrePCB generic device join.**
- **[P08]** Espressif [ESP32-WROOM-32E/32UE datasheet HTML v2.1](https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html) (viewed 2026-11-20; URL may update), plus official [technical documents index](https://www.espressif.com/en/support/documents/technical-documents). Different recommended vs absolute bounds must not merge.
- **[P09]** Zephyr [HC-SR04 Devicetree binding YAML](https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/sensor/hc-sr04.yaml) (`trigger-gpios`, `echo-gpios`, `echo-timeout-ms`, SPDX Apache-2.0 on that file), plus [bindings syntax](https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/build/dts/bindings-syntax.rst). These are firmware/interface contracts, not proof of electrical tolerance. Pin a tagged commit before actual reuse.
- **[P10]** Arm [CMSIS-Pack PDSC specification](https://arm-software.github.io/CMSIS_5/5.8.0/Pack/html/packFormat.html), [CMSIS introduction](https://arm-software.github.io/CMSIS_5/latest/General/html/index.html). **The framework license does not automatically authorize every third-party Device Family Pack asset.**
- **[P11]** Wokwi [HC-SR04 simulator component reference](https://docs.wokwi.com/parts/wokwi-hc-sr04), [Custom Chips C API](https://docs.wokwi.com/chips-api/getting-started): simulated behaviors and pin names; commercial embed/API rights must be separately verified.
- **[P12]** Google [OR-Tools / LICENSE](https://github.com/google/or-tools/blob/stable/LICENSE), [project overview](https://github.com/google/or-tools): Apache-2.0 combinatorial solver; no claim that using it ensures electrical correctness.

**სალიცენზიო ფორმულირება:** ზემოთ მითითებული უფლებების ინტერპრეტაცია არის ტექნიკური intake policy, არა ინდივიდუალური იურიდიული დასკვნა. `CC0/CC BY-SA/Apache/GPL` უნდა შეფასდეს კონკრეტული **ფაილის**, reuse mode-ისა და distribution mode-ის მიხედვით. „ხელმისაწვდომია ინტერნეტში“ არ არის კომერციული მონაცემთა ლიცენზია. Manufacturer PDF-ის ტექსტის ან ვიზუალის bulk რეპუბლიკაცია არ შედის ამ რეკომენდაციაში.

## 23. Final assessment and authorization boundary

**[D] რეკომენდაცია: SELECT B, NARROW.** არსებული სისტემა უკვე იძლევა მტკიცებულებიან topology/GPIO verification-ს და ერთი domain-specific DEMO bridge-ს. რეალური მომდევნო სამეცნიერო მიღწევა არის **ზუსტად კონტექსტში არსებული კომპონენტის ფაქტების არჩევანი და გამოყოფა**, არა კიდევ ერთი ზოგადი თვითდაჯერებული AI engineering layer. ტექნიკურად მნიშვნელოვანი ახალი promise იქნება: „ნაპოვნი კომპონენტი, მისი ზუსტი id, რა ფუნქციას ასრულებს, რა ვიცით დადასტურებით, რა აკლია და რომელი existing verifier დაგვიდასტურებს მომდევნო ფაქტს“.

**NO-GO** automatic „safe circuit“ claim, „all HC-SR04 are equivalent“ claim, exact YAGEO generic join without review, generic LED drive, vector DB/ontology-first, duplicated GPIO engine, unlicensed vendor corpus. **GO for owner review only:** bounded typed capability search, two permission gates (discovery vs engineering), a minimal source→claim→finding→hint dependency chain, and independent oracle-based A/B/C ingestion study.

**არც ერთი ქვემოთ აღწერილი ალტერნატივა არ არის ამ ტექსტით დამტკიცებული განხორციელების დავალება.** გადაწყვეტილებისა და გაყინული implementation scope-ის უფლება რჩება პროექტის მფლობელს; Codex-ს არ გადაეცემა ამ კვლევიდან ავტონომიური არქიტექტურული არჩევანი.

---

*დოკუმენტის მომზადების მეთოდი:* საწყისი Research I-ის სრული დავალება, Research E/G/H-ის ხელმისაწვდომი მასალები, პროექტის კონკრეტული reference commit-ის API/ფაილები/ანგარიშები და 2026-11-20-ის ოფიციალური ონლაინ პირველწყაროები. **ლოკალური ტესტები, შემსყიდველი API-ების სრულმასშტაბიანი შემოწმება და ყველა vendor-PDF-ის ახალი ბაიტური inspection არ ჩატარებულა**; ამისი მტკიცება ამ კვლევას არ აქვს.
