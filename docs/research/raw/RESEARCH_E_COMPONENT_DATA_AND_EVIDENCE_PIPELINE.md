# RESEARCH E — Engineering Component Data, Evidence Acquisition & Legally Reusable Sources

**პროექტი:** INVENTOR EDU  
**დოკუმენტი:** `RESEARCH_E_COMPONENT_DATA_AND_EVIDENCE_PIPELINE.md`  
**გამოკვლევის თარიღი:** 2026-11-20 (Asia/Tbilisi)  
**სტატუსი:** დამოუკიდებელი კვლევა; **არც არქიტექტურის ცვლილების, არც კოდის, არც Codex-ის დავალების ავტორიზაცია**  
**საზღვარი:** CORE-001A-ის ფაქტობრივად დოკუმენტირებული API არის ინტეგრაციის სამიზნე. CORE-001B/C — კვლევითი მომხმარებლები და არა ამ კვლევით უკვე განხორციელებული კომპონენტები.

**ნიშნები:** [F] გადამოწმებული პირველწყაროს ფაქტი; [M] ფორმალური/მათემატიკური დასკვნა; [R] საინჟინრო რეკომენდაცია; [U] დაუდასტურებელი/გაურკვეველი. ლიცენზიის „დაშვება“ არის კვლევითი კატეგორია და არა იურიდიული გარანტია. მწარმოებლის სპეციფიკაციის გამოყენება არ ნიშნავს მის გამოცდას რეალურ აპარატურაზე. წყაროების ინდექსი მოცემულია §15-ში.

---

## 1. Executive recommendation

**[R] SELECT — მცირე, რეცენზირებული ფაქტების კატალოგი + CC0 LibrePCB სტრუქტურული იმპორტი + ოფიციალური მწარმოებლის დოკუმენტებით თითოეული კრიტიკული მონაცემის დამოუკიდებელი გადამოწმება.**

1. **სტრუქტურა:** `LibrePCB-Libraries/LibrePCB_Base.lplib`, კონკრეტული `LibrePCB_ICs.lplib`/სხვა ოფიციალური CC0 ბიბლიოთეკა მხოლოდ იმ ფაილებისთვის, რომლებსაც ახლავს შესაბამისი `LICENSE.txt`; აიღოს package pad, device pad-to-signal და component signal-ის მინიმალური, გამოსადეგი ქვეჯგუფი. ეს ფაილები მონაცემის *კანდიდატია*, არა ტექნიკური უსაფრთხოების მტკიცებულება. [F/R; S01–S05]
2. **სილიკონის ფუნქციები:** კონკრეტული SoC-ის ოფიციალური SDK/board-definition არტეფაქტების ვერსირებული გამოყენება: საწყის ESP32-ზე ESP-IDF-ის `soc_caps.h`/GPIO-მასკები და Espressif-ის DevKitC V4-ის user guide; დამატებით Zephyr-ის DTS/YAML მხოლოდ გამჭვირვალე cross-check. Board header → module contact → silicon pad აუცილებელია გაირჩეს ცალ-ცალკე. [F/R; S10–S13]
3. **ელექტრული ფაქტები:** მწარმოებლის გამოცემაში, ცხრილში, პარამეტრში, ერთეულში, სამუშაო ტემპერატურასა და ვერსიაში მიბმული *ხელით დადასტურებული, მცირე ზომის რიცხვითი ჩანაწერები*. არ გადმოვიტანოთ PDF-ის გამოსახულება, მთელი ცხრილები, ტექსტი ან ილუსტრაციები კომერციულ პროდუქტში სათანადო უფლებების გარეშე. [R; S16–S23]
4. **დამატებითი საკონტროლო ობიექტები:** (A) Raspberry Pi Pico, board R3, RP2040; (B) YAGEO RC0603FR-0710KL 10 kΩ ±1% 0603; (C) TI SN74LVC1T45DBVR, 6-pin SOT-23 voltage translator. ყველაზე კარგად დოკუმენტირებული ახალი electrical acceptance არის C-ის **VCCA/VCCB/DIR-ის კონკრეტულ პირობებზე** დადებითი/უარყოფითი შემოწმება; მას შეიძლება მოემსახუროს ESP32 board ან მეორე, RP2040-family board, ოღონდ ყოველი board-level ფაქტი ცალკე უნდა გაიაროს მიღება. [F/R; S16–S20]
5. **არ ავაშენოთ პირველ რიგში:** უნივერსალური PDF/LLM extractor, vendor scraper, paid distributor API, SaaS-ზე დამოკიდებული catalog API, მორიგი graph/ontology, ან „უნივერსალური compatibility checker“. [R]

**[U] გადაწყვეტილება არ უდრის დასრულებულ კატალოგს.** ამ კვლევაში არც ერთი source-commit SHA, მიღებული ცალკეული ფაილის digest, პროდუქტის რეალური PCB revision, პროგრამულად გადმოტანილი LibrePCB device-ფაილი ან TI-ის კონრეტული `DBVR` შეკვეთის მატრიცა ადგილობრივ CORE-001A-ში არ შემოწმებულა. ესენი admission-gate-ებია და არა დამალული დაშვებები.

---

## 2. Existing structured engineering-data ecosystems

ცხრილი პასუხობს: არსებობს თუ არა **მართლა მანქანურად წასაკითხი მონაცემი**, რას ამტკიცებს და რა უნდა გადაიტანოს არსებული მოდელისაკენ. „ვერსია“ განასხვავებს კონკრეტულ upstream release-სა და ჯერ დაუფიქსირებელ ბიბლიოთეკის Git revision-ს. მყარი მიღება მოითხოვს **ფაილის blob SHA-256-ს + upstream full commit SHA-ს**, არა `main/master/latest` URL-ს.

| წყარო / ოფიციალური მდებარეობა | ვერსია / მდგომარეობა კვლევისას | რეალური ფორმატი / შემოწმება | ნამდვილად გამოსადეგი | არ ამტკიცებს | სტატუსი |
|---|---|---|---|---|---|
| **LibrePCB official Base** `github.com/LibrePCB-Libraries/LibrePCB_Base.lplib` | ბიბლიოთეკის `master`; **კონკრეტული commit ჯერ არ დაპინულა** [U]; LibrePCB აპის release 2.1.1 მხოლოდ თავსებადობის კონტექსტია | ტექსტური S-expressions; `library.lp`, `sym`, `cmp`, `pkg`, `dev` ელემენტები; ოფიციალური CLI `open-library --check` | component signals, package pads, device pad→signal, ზოგადი რეზისტორები/დიაკვშირის ტოპოლოგია | ძაბვის რეკომენდირებულ დიაპაზონს, IEC safety-ს, სენსორის რეალურ PCB ვერსიას | **APPROVED_CANDIDATE** CC0-ფაილებისთვის [S01–S05] |
| **LibrePCB official ICs** `github.com/LibrePCB-Libraries/LibrePCB_ICs.lplib` | `master`; SHA დაუფიქსირებელია [U] | იგივე `.lplib`/S-expressions | ზოგიერთი IC package/device mapping | რომ კონკრეტული MPN ან supplier რევიზია აუცილებლად ზუსტია | **APPROVED_CANDIDATE** მხოლოდ artifact LICENSE გადამოწმებისას [S01,S06] |
| **KiCad Symbols** `gitlab.com/kicad/libraries/kicad-symbols` | KiCad 10 ფორმატი; დამოუკიდებელი library release/tag/commit საჭიროა, არ მივაწეროთ აპის ნომერი მონაცემთა revision-ს | `.kicad_sym`, documented S-expression; pins: number/name/type, alternate symbols; `kicad-cli sym export svg` ვიზუალური ექსპორტისთვის | სიმბოლოს pin numbers/types, შესაძლო MPN metadata | package footprint-თან დადასტურებულ board net-ს, GPIO firmware mode-ს, max voltage-ს | **APPROVED_WITH_CONDITIONS**, CC BY-SA 4.0 + KiCad exception [S07–S09] |
| **KiCad Footprints** `gitlab.com/kicad/libraries/kicad-footprints` | დამოუკიდებელი Git tag/SHA; არა symbols-ის SHA | `.pretty/*.kicad_mod` S-expression; documented footprint parser | physical pad number, package geometry, ზოგადი კორპუსები | კომპონენტის ფუნქციის ამა თუ იმ პადზე არსებობას, board header-ს, ელექტრულ ზღვარს | **APPROVED_WITH_CONDITIONS** [S07–S09] |
| **Espressif ESP-IDF** `github.com/espressif/esp-idf` | შესადარებლად ფიქსირებული tag **v6.0.3**; `master` ცვლადია | C headers/macros, `soc_caps.h`, GPIO types/masks, driver source; SDK compiler/preprocessor; `soc` directory target-specific | SoC capabilities, GPIO output eligibility, SDK-დაშვებული შესაძლებლობები და რესურსების ნაწილი | დევბორდის header რეალურ PCB wiring-ს, firmware-ის იმ მომენტში აქტიურ მდგომარეობას, datasheet-ის ყველა limit-ს | **APPROVED_WITH_CONDITIONS**, ფაილობრივად SPDX [S10,S11] |
| **Espressif board docs** `github.com/espressif/esp-dev-kits`; `docs.espressif.com/.../esp32-devkitc` | board **ESP32-DevKitC V4**, `-32E` orderable ვარიანტი; დოკუმენტის Git SHA ჯერ არაა დაპინული [U] | RST/HTML user-guide pin tables; schematic ცალკე PDF | კონკრეტული J-header label→GPIO ფუნქციები და მოდულთა გამონაკლისები | დაფის კლონის იგივეობას, ყველა board revision-ს, PDF-ის კომერციულ რედისტრიბუციას | **RIGHTS_UNVERIFIED** დოკუმენტის კოპირებაზე, ფაქტების ხელით რეფერირებას ვთავაზობთ [S12] |
| **Zephyr** `github.com/zephyrproject-rtos/zephyr` | კონკრეტული tagged baseline **v4.3.0**; მხარდაჭერის აქტუალობა შემდგომ გადახედვას მოითხოვს | `.dts/.dtsi` + YAML binding, phandle, `pinctrl`; official Python `dtlib.py`/`edtlib.py` | declared board wiring, peripheral instance/alias, pinctrl state, GPIO flags | ელექტრულ tolerance-ს, PCB revision match-ს, installed firmware-ს | **APPROVED_WITH_CONDITIONS** file-level SPDX/Apache-2.0 [S13,S14] |
| **CMSIS-SVD schema** `github.com/Open-CMSIS-Pack/svd-spec` | schema 1.x; კონკრეტული schema commit მოგვიანებით დაიპინოს | `.svd` XML + `CMSIS-SVD.xsd`; open-source `cmsis-svd` Python parser | peripheral registers, field masks, reset/interrupt definitions | physical lead/package, package pin mux, analogue maximums | **APPROVED_CANDIDATE** specification/parser code; **RIGHTS_UNVERIFIED** თითოეული მესამე მხარის `.svd`-სთვის [S15] |
| **CMSIS-Pack PDSC** `github.com/Open-CMSIS-Pack/Open-CMSIS-Pack-Spec` | პუბლიკაციის specification 1.7.62 კონტექსტი; pack-ის *საკუთარი ვერსია* აუცილებელია | `.pdsc` XML / `.pack` ZIP, `PACK.xsd`; `cpackget`, `packchk` | vendor/device identification, tools/boards, pack metadata, package/member paths | pack-ს შიგნით არსებული ყველა SVD/სურათის უფლების ერთიანობას, electrical correctness-ს | **APPROVED_WITH_CONDITIONS** specification; pack-level **RIGHTS_UNVERIFIED** [S15,S24] |
| **Adafruit Fritzing** `github.com/adafruit/Fritzing-Library` | `master`/ცალკე commit, განახლებადი | `.fzp` XML + SVG graphics in `.fzbz` | breadboard contact layouts/illustrations, ზოგიერთი PCB/module pin label | სტანდარტიზებულ safety limits-ს, კლონის რევიზიას | **APPROVED_WITH_CONDITIONS** CC BY-SA; არ არის საწყისი ტექნიკური ფაქტების ბაზა [S25] |
| **STMicroelectronics STM32CubeF4/CMSIS Device** `github.com/STMicroelectronics/STM32CubeF4`, `.../cmsis-device-f4` | კონკრეტული STM32CubeF4 release/tag ან module SHA დასაპინია; ST repo/კომპონენტის ვერსიები ცალკეა | C header `stm32f4xx.h`/`stm32f4xx_hal_gpio.h`, CMSIS peripheral definitions, board example files; conditional compile flags | კონკრეტული STM32-ის register/peripheral შესაძლებლობები; firmware-კონფიგურაციის candidate წყარო | PCB header-to-package mapping-ს, ყველა package pin alternative-function გარანტიას ან tolerance/absolute maximum ცხრილებს | **APPROVED_WITH_CONDITIONS** — `LICENSE.md`-ით ფაილობრივი უფლებების განხილვა [S31] |
| **SparkFun Eagle libraries** `github.com/sparkfun/SparkFun-Eagle-Libraries` | `main`, ფაილის/commit SHA admission-მდე უცნობია | Eagle XML `.lbr` (`<devicesets>`, `<packages>`, `<symbols>`, `<connects>`); XML parser | package pads, symbol pins, device pad-to-signal candidates | მრავალ contributor-ის ფაილის electrical accuracy-ს, სენსორის revision-სა და მონაცემის სრულდოკუმენტურ მტკიცებულებას | **APPROVED_WITH_CONDITIONS** CC BY-SA 4.0; default proprietary catalog-ში არ შემოვიტანოთ [S32] |
| **Microchip Device Family Packs** `packs.download.microchip.com` | კონკრეტული `*_DFP` და pack semver აუცილებელია; მთელ repository-ს ერთი უცვლელი release არ აქვს | `.atpack`/ZIP + `.pdsc`/XML, vendor `atdf/*.atdf` XML, headers; XML parser/pack manager | device/package/signals და peripheral metadata ზოგიერთ AVR/SAM ოჯახში; მოცემულ package-ში შეიძლება იყოს alternate signals | board wiring-ს, operating/absolute limits-ის სრული ცხრილების არსებობას, pack შიგთავსის საჯარო გადაბეჭდვის უფლებას | **RIGHTS_UNVERIFIED** vendor pack data; no initial bundled catalog [S33] |
| **Raspberry Pi Pico official** `pip.raspberrypi.com/categories/610`, documentation | board **Pico R3**, RP2040; კონკრეტული schematic edition/digest ჩასაბარებელია | official schematic/pinout PDF; hardware source design files ხელმისაწვდომია; SDK headers ცალკე | 40 pin edge connector, mapping და board-vs-SoC სემანტიკა source review-ით | HTML გვერდზე ყველა limit-ის ავტომატურ შემოტანას, ყველა სხვა Pico/H/W ვარიანტზე იდენტურობას | **RIGHTS_UNVERIFIED** copied documentation; ხელით ფაქტების შერჩევა [S26] |

**[M] ფუნქციური სისრულე ≠ ელექტრული სისრულე.** მონაცემთა სრული `pad→signal` mapping შეიძლება არსებობდეს, მაგრამ იმავე profile-ის `VIH`, `VIL`, `VOH`, `VOL`, `IOH`, `IOL`, `VCC` ცარიელი იყოს. არც „სქემაზე ჩანს“ და არც `pin_type=power_in` არ ადასტურებს რეჟიმისა და აბსოლუტური მაქსიმუმის ნორმებს.

### 2.1 კონკრეტული ფორმატები, ვალიდატორები და narrow transforms

- **[F/R] LibrePCB:** `component` ლოგიკურ signals-ს ასახავს; `package` რეალურ pads-ს; `device` არის მათი კონკრეტული pad-to-signal კავშირი. **ნულიდან device-identity არ განვსაზღვროთ**: ავიღოთ მხოლოდ ზუსტი pad სახელი/ნომერი და მის მიერ დაკავშირებული signal, თუ MPN/package ნამდვილად დადასტურდა. `librepcb-cli open-library --check` ბიბლიოთეკის სინტაქსისა და შიდა ურთიერთობების validator-ია, არა დამოუკიდებელი ელექტრული truth-checker. Importer-ის ფრთხილი failure modes: სხვადასხვა unit/gate, package substitution, hidden pads, alternate package, არანულოვანი electrical ties. [S02–S05]
- **[F/R] KiCad:** ოფიციალურად დოკუმენტირებული `(symbol ...)` და `(pin ...)` s-expression; footprint pad-ის ნომერი ცალკეა. განსხვავებულ repo-ებს, პაკეტებსა და versions შორის join უნდა გაიაროს consistency gate; არ გამოიყენოთ generic footprint-ის reference როგორც manufacturer package guarantee. Symbol-ის „power_in/output/bidirectional“ ფართო ERC-მინიშნებებია და არა voltage contract. [S07–S09]
- **[F/R] ESP-IDF:** C preprocessor conditionals, Kconfig target და silicon-specific `soc` headers ნიშნავს, რომ ტექსტში `#define`-ის აღება ზოგად, unconditional ფაქტად შეცდომაა. იკითხოს concrete target+tag+build-configuration context. `GPIO_IS_VALID_OUTPUT_GPIO` მხოლოდ ერთი eligibility predicate-ია. SDK driver-ის მისაღები ოპერაცია ≠ board pin electrical safety. [S10,S11]
- **[F/R] Zephyr:** `.dts` chain resolution (`#include`, overlays), board qualifier/SoC variant, `compatible`, YAML, `pinctrl-0`, `status` უნდა ამოიხსნას ვერსიის გათვალისწინებით; `dtlib/edtlib` არის ესმის-უნარიანი parser-ები. `GPIO_ACTIVE_LOW` ფუნქციური პოლარობაა, არა დამტკიცებული VIL threshold. [S13,S14]
- **[F/R] STM32/SparkFun/Microchip:** `CMSIS Device` C headers მოითხოვს კონკრეტულ compile-target-ს, EAGLE `.lbr` არის XML წყვილით `package/deviceset`, ხოლო Microchip ATDF-შიც XML device/package/signal metadata ხშირად არსებობს; ცალკეული source file / pack-version უნდა იქნეს მიბმული იმავე exact chip/package scope-ზე. **არც ერთი მათგანის რეგისტრების აღწერა არ ადგენს voltage threshold-ს.** Microchip-ის pack-ების proprietary conditions-ს გადაცემის ნებართვად არ მივიჩნევთ. [S31–S33]
- **[F/R] CMSIS-SVD:** XML `peripheral/register/field/interrupt` აღწერს debugger-ისთვის register map-ს; `pin number` ხშირად საერთოდ არ აქვს. სქემის Apache-2.0 ლიცენზია არ გადაიტანოთ იმ ფაილებზე, რომლებიც სხვა chip vendor-ებმა შექმნეს. `.pdsc`-ის `licenseSets`/შიდა license files შეამოწმოს **თითო pack-ისთვის**. [S15,S24]

### 2.2 შეცდომები და maintenance

- [R] `master/latest`-ზე ჩუმი განახლება დაუშვებელია; upstream pinout change გააჩერებს profile-ს, ვიდრე scope/diff განხილული არ იქნება.
- [R] lib importer არასოდეს უნდა დაამატოს ახალი pin ან ახალი ideal internal tie solely geometry-დან; hidden/power pads აუცილებლად სრულად გამოფინოს review-ში.
- [R] „official library“ არ ნიშნავს რომ file author = part manufacturer; vendor primary datasheet-ით გადამოწმდეს კრიტიკული part mapping.
- [R] source revision drift event შეიძლება ეხებოდეს მხოლოდ display-name-ს; ამ შემთხვევაშიც topology record უნდა დარჩეს წინა reproducible snapshot-ს მიბმული და არ შეიცვალოს ჩუმად.

---

## 3. Data coverage and accuracy comparison

ნიშნები: **H** = ტიპურად ძლიერი ამ მონაცემთა კატეგორიისთვის; **P** = ნაწილობრივი/რეჟიმზე დამოკიდებული; **–** = არ არის წყაროს მიზანი; **?** = კონკრეტული არტეფაქტი აუდიტს ითხოვს. ეს **არ არის** რაოდენობრივად დათვლილი ბაზის coverage.

| წყარო | physical pad | logical contact/function | board/revision | GPIO mode/pinmux | abs/recommended electrical | permission clarity |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| LibrePCB official CC0 | H | H/P | P | – | – | H |
| KiCad symbols/footprints | H/P | P | P/? | – | – | P, share-alike |
| ESP-IDF pinned | P (SoC) | H | P | H/P | – | H/P, file-level |
| Zephyr DTS | P | H/P | P | H/P | – | H/P, file-level |
| CMSIS-SVD/Packs | – | H registers | P | P | – | ? pack-level |
| Manufacturer datasheet | H | H | H/P | H/P | **H, თუ ცხრილი არსებობს** | ? copying/redistribution |
| Adafruit #3942 retail listing | P | P | ? | – | **P, არა გარანტირებული ყველა limit** | ? |
| Proprietary CAD/distributor API | H/P | P | ? | – | P/? | ხშირად შეზღუდული |

**[M] მონაცემის ტიპის რისკი:** `wrong physical terminal` შეიძლება გამოიწვიოს არასწორი net; `wrong nominal resistance` შეცვალოს divider; `wrong absolute maximum` წარმოშობს ცრუ safety-დასკვნას. ბოლო ორი კლასი კრიტიკულია და მოითხოვს დამოუკიდებელ manufacturer-source review-ს, თუნდაც ისინი machine-readable აღმოჩნდეს.

---

## 4. License and commercial reuse matrix

| წყარო/არტეფაქტი | კოდის ლიცენზია | data/docs ლიცენზია | proprietary SaaS internal use | bundling/export ან derived catalog | attribution/notices, copyleft, API | **კვლევითი სტატუსი** |
|---|---|---|---|---|---|---|
| LibrePCB **აპი/CLI** | GPLv3 [F] | – | CLI ცალკე პროცესად გამოყენების ლიცენზიური განხილვა; API linking-ის შეცდომისგან დაცვა | აპის modified distribution source/notice obligation; ნუ მოაქვთ მისი GPL კოდი proprietary SDK-ში | GPLv3; proprietary SaaS *თავისთავად* ავტომატურად არაა GPL გავრცელება, მაგრამ deployment/distribution სცენარი ცალკე შესამოწმებელია | **APPROVED_WITH_CONDITIONS** მხოლოდ tool use |
| LibrePCB **official libraries**: Base/ICs | – | **CC0-1.0** [F] | დიახ | **დიახ** შესაბამისი ოფიციალური library-ფაილისთვის; არ მოიცავს ცალკე linked vendor PDFs-ს | CC0: ჩვეულებრივ არ მოითხოვს attribution-ს; წყაროსა და version-ს მაინც ვაფიქსირებთ audit trace-ისთვის | **APPROVED_CANDIDATE** [S01,S06] |
| KiCad application | GPLv3 [F] | სხვა | შესაძლებელი tool-run | კოდის ბანდლს ცალკე GPL ვალდებულებები აქვს | GPLv3 (აპი) | **APPROVED_WITH_CONDITIONS** |
| KiCad official symbols/footprints | – | **CC BY-SA 4.0 + KiCad libraries exception** [F] | შესაძლებელია | დიზაინის შედეგს exception ამსუბუქებს; **იმპორტირებული/შეცვლილი ბიბლიოთეკის proprietary redistribution ავტომატურად გამონაკლისში არ მოექცეს** | attribution, same-license/ShareAlike შესაძლო მოთხოვნები copied/adapted data-თვის; იურიდიული განხილვა აუცილებელია | **APPROVED_WITH_CONDITIONS**; არა default bundled source [S07] |
| ESP-IDF (ზუსტი files) | main repo Apache-2.0; გარკვეული headers Apache-2.0 OR MIT; third-party განსხვავდება | docs და vendor PDFs ცალკე | SDK header-ის განჭვრეტა შესაძლებელია | code reuse file-level SPDX+NOTICE, third-party provenance; PDF არ შედის Apache ნებართვაში ავტომატურად | Apache notice/changes/license; build tag pin; Git clone უფასო, no mandatory runtime API | **APPROVED_WITH_CONDITIONS** [S10,S11] |
| Zephyr DTS/YAML/tools | ძირითადად Apache-2.0; ფაილობრივად SPDX | external board docs ცალკე | დიახ ფაილების უფლების ფარგლებში | permissive code permitted notice/attribution-ით; არ გაიტანოს opaque vendor package | SPDX; upstream release pinned; Git source acquisition costs $0, hosting quotas/conditions ცვალებადია | **APPROVED_WITH_CONDITIONS** [S13] |
| CMSIS schema/spec/parser | Apache-2.0 (შესაბამის upstream) | vendor .svd/.pack **მრავალფეროვანი** | schema/parser okay | SVD/Pack დოკუმენტი შეიძლება proprietary vendor license იყოს | `licenseSets`, pack `LICENSE`, vendor ID; `cmsis-svd-data` aggregation არ ავლენს ერთიან უფლებას | **RIGHTS_UNVERIFIED** vendor datasets [S15,S24] |
| Raspberry Pi Pico official docs/source | SDK examples BSD-3-Clause; schematic/design artifact ცალკე | docs/diagrams **artifact-specific** | ფაქტების კვლევა | source-design availability ≠ ყველა დოკუმენტის blanket CC0; copy only if explicit license found | no automatic official diagrams in commercial UI | **RIGHTS_UNVERIFIED** compiled docs [S26] |
| Espressif/Adafruit/TI/YAGEO manufacturer & retailer datasheets | არა code | copyright/terms, განსხვავებული | ფაქტების ცალკეული ხელით განხილვა | **არ დავუბანდლოთ PDF, სურათი, სრული ცხრილი, ტექსტი ნებართვის გარეშე** | official link+edition+locator; TI scraping/data mining აკრძალულია მის პირობებში | **RESTRICTED_OR_BLOCKED** third-party document copy; curated factual record ცალკე legal gate [S16–S23] |
| SnapMagic Search / SnapEDA | proprietary | terms restrict competing database/scrape | შეზღუდული design use | catalog aggregation/republishing **აკრძალული ან ლიცენზირებას მოითხოვს** | API/enterprise agreement საჭირო | **RESTRICTED_OR_BLOCKED** [S27] |
| SamacSys / ComponentSearchEngine | proprietary | internal/informational, no redistribution | შეზღუდული | **არა** | site terms expressly prohibit distributing service content | **RESTRICTED_OR_BLOCKED** [S28] |
| DigiKey distributor data/API | contractual, proprietary | data/database protected | API მხოლოდ agreement-ით | no blanket catalog-republication permission | API credential/contract, quotas/cost conditional; არა mandatory dependency | **RESTRICTED_OR_BLOCKED** as initial source [S29] |
| STM32CubeF4/CMSIS Device | რეპოზიტორია მრავალკომპონენტიანია: CMSIS Device Apache-2.0; HAL BSD-3-Clause და სხვა ფაილები განსხვავდება [F] | reference manuals/vendor PDFs ცალკე | ცნობების შიდა დამუშავება შესაბამისი პირობებით | imported header/pack ფაილის `LICENSE.md` და SPDX აუცილებელია; vendor manual არ შედის CMSIS ლიცენზიაში | include license/notice and exact artifact license; not first-wave requirement | **APPROVED_WITH_CONDITIONS** [S31] |
| SparkFun Eagle `.lbr` | – | CC BY-SA 4.0 (ოფიციალური ბიბლიოთეკის დეკლარაციით) [F] | yes, terms respected | copied/adapted library database-in-proprietary product needs attribution/ShareAlike review; not our default | GPL კოდზე არ ვსაუბრობთ; CC BY-SA data conditions ფაილობრივად | **APPROVED_WITH_CONDITIONS** [S32] |
| Microchip DFP `.atpack/.atdf` | vendor proprietary pack terms, per archive | pack/folder/artifact license review required [U] | tools' documented intended use possible | **არ აქვს დამტკიცებული general redistribution grant** | archive `license` metadata and terms must be checked; no automated bulk importing | **RIGHTS_UNVERIFIED** [S33] |
| Adafruit Fritzing files | – | CC BY-SA terms on repo [F] | შესაძლებელია | share-alike/attribution, source file-specific | electronics illustration ≠ manufacturer accuracy | **APPROVED_WITH_CONDITIONS** [S25] |

**[F] განსაკუთრებული სამართლებრივი რისკი — TI:** TI-ის ოფიციალური website terms კრძალავს `data mining`, `robots` ან მსგავსი ავტომატური extraction-ით სერვისის გამოყენებას და ზოგად ბეჭდვა/გავრცელების უფლებას non-commercial/personal ფარგლებში ზღუდავს. ამას ვერ გააუქმებს საჯარო PDF link. თავდაპირველ pipeline-ში **არ გამოიყენოთ TI-website scraper** და არ გაავრცელოთ TI datasheet გვერდები/ნახატები. [S22,S23]

**[R] პრაქტიკული გამიჯვნა:** საჯარო მონაცემიდან მცირე, დამოუკიდებლად ჩამოყალიბებული ფაქტობრივი მახასიათებლების ჩანაწერი (მაგ., 1.65–5.5 V — როგორც შემოწმებული ნორმა შესაბამისი პირობებით) და საავტორო უფლებებით დაცული დოკუმენტის/ცხრილის კოპირება სხვადასხვაა. თუმცა კონკრეტულ იურისდიქციაში ფაქტების/DB extraction-ის უფლებები და საიტის ხელშეკრულებითი შეზღუდვები **არ უნდა ივარაუდოთ**. დამატებითი მოცულობის bulk extraction-მდე საჭიროა შემდგომი სამართლებრივი review ან ოფიციალური თანხმობა. ეს დოკუმენტი არ წარმოადგენს იურიდიულ დასკვნას.

**SaaS versus distribution:** [M/R] მხოლოდ server-side internal parser-ის გაშვება განსხვავდება GPL კოდის მომხმარებლისთვის დისტრიბუციისგან; ლიცენზია CC BY-SA/CC0 მონაცემებისთვის არ იცვლება SaaS-ით; თუ downloaded dataset საჯარო API/UI-ით რეალურად ვრცელდება, redistribution პირობები აქტუალურია. არ არის დასაშვები `GPL app ⇒ GPL data` ან `open SDK ⇒ open PDF` დასკვნები.

**API/rate/cost:** initial path uses reviewed, versioned Git sources and manually opened official docs: **no runtime API, subscription, per-request fee or token bill**. GitHub/GitLab hosting-ის auth/rate policy შეიძლება იცვლებოდეს; operational ingestion არ დაეყრდნოს არაუთენტიფიცირებულ high-frequency API-ს. TI საიტზე bots არ დაიგეგმოს. Distributor API-ებზე უცნობი რაოდენობრივი limit-ები **UNKNOWN**, არა `unlimited`. [R/U]

---

## 5. ESP32-DevKitC-32E + Adafruit HC-SR04 #3942 — evidence gap

**ფიზიკური იდენტობა:** `ESP32-DevKitC V4` board, orderable variant `ESP32-DevKitC-32E`, installed module `ESP32-WROOM-32E`, silicon revision variation, header contacts **J2/J3-ის კონკრეტული პინები**. Adafruit `Product ID 3942` არის საცალო ერთეულის იდენტობა, მაგრამ **არა ყველა წარმოებული HC-SR04 PCB/OEM revision-ის მტკიცებულება**. [F/U; S12,S16–S18]

| საკითხი | ცნობილი წყარო / მტკიცებულების ხარისხი | შედეგი კატალოგისთვის |
|---|---|---|
| Board header labels, GPIO map | [F] Espressif V4 DevKitC pin tables; module-dependent reservation warning [S12] | valid exact board+module mapping source reviewed; clone mismatch→UNKNOWN |
| GPIO34–39 input-only, GPIO18 output capable, pin matrix/boot limitations | [F] Espressif chip data + ESP-IDF constraints [S10,S11,S18] | silicon capability და board mapping ცალკე, configuration/firmware ცალკე |
| ESP32-WROOM-32E supply / input thresholds | [F] ოფიციალური module datasheet **v2.1 (2026-08-05)**, sections 6.1–6.3 [S17] | DC characteristic-ს მიეწეროს supply/temp context; pin-domain exceptions separate |
| Adafruit #3942 VCC, Trig, Echo, GND | [F] Adafruit retail `power & logic 5V`, `Echo = 5V logic`, 3V/5V Trig statement [S16] | *retailer-declared behavior*, არა სენსორის სრული manufacturer-guaranteed transfer curve |
| Echo guaranteed VOH_min, VOL_max under output load; I_Echo and timing tolerances | [U] ოფიციალური fixed OEM/PCB revision datasheet არ დადასტურდა | **UNKNOWN**; end-to-end guaranteed-high PASS აკრძალულია |
| Adafruit bundled ორი 10 kΩ resistor-ის ზუსტი tolerance/power/series | [U] პროდუქტის აღწერა არაა კონკრეტული resistor MPN / tolerance guarantee | **UNKNOWN**, სანამ ცალკე resistor profile არ განისაზღვრება |
| Module/board revision-specific GPIO pad input abs maxima | [F/U] manufacturer docs contain limits, but each pad domain/footnote needs exact claim scope [S17,S18] | 5V input compliance check possible under stated conditions; no simplistic “5V always destroys” claim |
| Physical-board USB/3.3V regulator rail under all power-source modes | [U] board schematic and regulator model/conditions require separate review | არ გავაიგივოთ nominal `3V3` და certified regulated interval ყველა მდგომარეობაში |
| Commercial copying of source PDFs, diagrams | [U] artifact-specific written permission absent | no PDF/graphics bundle; source link & factual evidence only |

### 5.1 voltage-divider — bounded mathematical check

**[M]** 10 kΩ/10 kΩ ideal divider: `Vout = Vin * Rbottom/(Rtop + Rbottom)`; თუ `Vin=5.000 V` და nominal `Rtop=Rbottom=10 kΩ`, `Vout=2.500 V`. 1%-იანი ორი **კონკრეტული YAGEO** resistor-ის worst-case interval იქნება, `Vin=5.000 V` assumption-ით: `2.475 V ≤ Vout ≤ 2.525 V` (Rtop 10.1k/Rbottom 9.9k და პირიქით). ორივე რეზისტორის worst-case dissipated power nominal ამ მაგალითში ≈0.625 mW — გაცილებით ნაკლები 0.1 W 70°C-ზე, *მაგრამ მხოლოდ ტემპერატურის, transient/load და power assumptions-ის ფარგლებში*. [S20]

**[M]** Espressif-ის documented `VIH,min = 0.75 × VDD` DC relation-ისთვის `VDD=3.4 V` ⇒ `VIH,min=2.55 V`. Ideal divider 2.500 V და მით უმეტეს 2.525 V მაქსიმუმი **ვერ ადასტურებს guaranteed HIGH**-ს ამ მდგომარეობაში; ეს არის **logic recognition problem**, არა თავისთავად absolute-stress proof. ასევე source Echo-სა და receiver leakage/load-ის დამტკიცებული ზღვარი არ გვაქვს. დადებითი verdict-ი უნდა დარჩეს `INDETERMINATE` ან უფრო ვიწრო კონკრეტული მოთხოვნის PASS (მაგ., მხოლოდ resistance/divider math). [S17,S18]

**[R]** ცალ-ცალკე გამოიტანეთ `GPIO_CAPABILITY`, `STRESS_WITHIN_RECOMMENDED`, `LOGIC_HIGH_GUARANTEED`, `LOAD_WITHIN_SPEC`; არასოდეს მიაბათ ისინი ერთ „SAFE“ სტატუსს.

### 5.2 Missing-data recovery

1. Adafruit-ის **ზუსტად მიწოდებული PCB/OEM mark** და official manufacturer datasheet საჭიროა guaranteed output/temperature/timing specs-ისთვის; პროდუქტის გვერდის გარეთ, მხოლოდ სხვა HC-SR04 clone datasheet-ზე დაყრდნობა მიუღებელია. [R/U]
2. Espressif official source-იდან hard facts შეიძლება აღდგეს; module datasheet edition+footnotes+revision-თან მიბმა სავალდებულოა. [F/R]
3. resistor packet-ის ბრენდი/MPN არ უნდა გამოვიცნოთ — educational fixture-ში YAGEO საკუთარი orderable exact 10 kΩ fixture შეიძლება ჩავანაცვლოთ **ლოგიკურ/მათემატიკურ ტესტში**, მაგრამ არ ვამტკიცოთ, რომ Adafruit-ის bundle-ში სწორედ ის იყო. [R]
4. Unknown manufacturer guarantee → `UNKNOWN`, არა სხვა PDF-იდან „საშუალო“ ვარაუდი. [R]

---

## 6. სამი განზოგადებული component profile

### P1. Raspberry Pi Pico, RP2040, **board R3** (microcontroller development board)

**[F]** Raspberry Pi-ის ოფიციალურ product portal-ს აქვს Pico R3 pinout/materials; Pico platform აღწერს 40 ფიზიკურ edge pins-სა და RP2040 chip-ს. [S26]

- **საჭირო ფაქტები:** board revision, 40 edge contact-ის მდებარეობა/ნომერი; GND/VSYS/VBUS/3V3/3V3_EN კონტაქტები; GPIO physical→RP2040 signal; USB/flash/LED board routes; RP2040-ის variant/edition. [R]
- **available:** board identity და pinout; silicon datasheet/SDK ცალკე. **manual:** board+silicon join, regulated power modes, actual I/O electrical limit table, hardware rev/routing; firmware function claims მხოლოდ შესაბამის profile-მდე. [R]
- **გაფრთხილება:** Pico, Pico H, Pico W, Pico 2 **არ არის interchangeable exact hardware**. ოფიციალური pinout diagram-ის კოპირება commercial UI-ში **უფლებების review-ის გარეშე არა**. [R/U]
- **დადებითი ტესტი:** ფიზიკური edge pin-ის სწორად mapped GPIO-ზე permitted digital IN/OUT capability, როდესაც exact official revision+register claims მიღებულია. **უარყოფითი:** swapped GPIO/contact, fictitious pad, reserved/internal pin / incorrectly claimed board tie. Electrical check რჩება ცალკე, სანამ ყველა საჭირო source claim არ მიგვიღია. [R]
- **Status:** structural **APPROVED_WITH_CONDITIONS**, electrical admission **HOLD**. [R/U]

### P2. YAGEO **RC0603FR-0710KL**, 0603 resistor

**[F]** მწარმოებლის part-specific fact sheet: resistance **10 kΩ**, tolerance **±1%**, rated power **0.1 W at 70°C**, max DC working **75 V** (full-rated-power condition), TCR ±100 ppm/°C, operating temperature **−55…+155 °C**. PDF-ს აქვს generated date **2025-12-23**. ეს ღირებულებები სხვადასხვა *მიზეზით* იზღუდება და max over-voltage/withstand არ უდრის continuous working voltage-ს. [S20]

- **2 physical terminals:** მეტალიზებული ბოლოები A/B, რომლებიც დამოუკიდებელ კონტაქტებად და 2-terminal passive behavior-ით უნდა აღიწეროს; **არანაირი ideal conductive internal tie**. [M/R]
- **შესატანი:** exact MPN+package, `R_nominal=10000 Ω`, tolerance, ratings with `Ta=70°C`, datasheet locator, version. Resistor upper/lower tolerance table direct is source-backed. [R]
- **შესამოწმებელი:** `P=I²R=V²/R`, worst-case tolerance, continuous voltage/power/temp applicability; transient, frequency, thermal/PCB derating condition თუ არ გვაქვს → UNKNOWN. [M/R]
- **Status:** **APPROVED_WITH_CONDITIONS** curated numeric facts; PDF redistribution blocked by default. [R]

### P3. TI **SN74LVC1T45DBVR**, 6-pin DBV/SOT-23 dual-voltage transceiver

**[F]** TI datasheet **SCES515N, Rev N, revised June 2024**, §4 pin definition, §5.1 absolute maxima, §5.3 recommended operating conditions. DBV package contact mapping: **1 VCCA, 2 GND, 3 A, 4 B, 5 DIR, 6 VCCB**. DIR low selects **B→A**, high **A→B**. 1.65–5.5 V is *recommended* per-supply interval; 6.5 V is absolute stress maximum (not permitted operating target). At VCCI 3–3.6 V data VIH,min 2.0 V, VIL,max 0.8 V; at 4.5–5.5 V VIH,min 0.7×VCCI, VIL,max 0.3×VCCI. `DIR` control thresholds reference VCCA. [S19]

- **Required facts:** each terminal and package; A/B direction conditioned on `DIR`; VCCA/VCCB referenced input/output side; common GND; full operating voltage interval; VI/VO, VIH/VIL per VCCI band; output IOH/IOL and VOH/VOL under specified load; power-up/down and undefined/floating input conditions. [R]
- **Direct reuse:** LibrePCB package/pad mapping if exact MPN and DBV footprint found and reviewed; no assumption that existing `LibrePCB_ICs` has exact TI device. **manual:** safety-critical electrical tables + source edition/footnotes. [R/U]
- **Strong test:** this chip provides actual positive and negative **bounded** electrical requirements without relying on HC-SR04's missing VOH. [R]
- **Status:** technical profile **APPROVED_WITH_CONDITIONS**; TI PDF bundle/scraper **RESTRICTED_OR_BLOCKED**. [R]

### 6.1 recommended generalized acceptance fixture — explicit expected outcomes

**[R] Main fixture:** `ESP32-DevKitC-32E` ↔ `SN74LVC1T45DBVR` ↔ declared external 5 V test source, two shared GNDs, board output pin mapping sourced separately. **Alternate cross-family structural fixture:** `Raspberry Pi Pico R3` ↔ same TI part; do not claim RP2040 full electrical capability before RP2040 official limits/board mapping are admitted.

| Test | Approved input assumptions | Expected scoped verdict | What is **not** being claimed |
|---|---|---|---|
| TI-SUPPLY-POS | `VCCA=3.3 V, VCCB=5.0 V, Ta=25°C`, correct 6 pads, verified PDF Rev N | **PASS** for TI supply recommended-range check | not PASS for wiring/drive/logic/timing/full-system |
| TI-SUPPLY-NEG | `VCCA=3.3 V, VCCB=6.0 V` | **FAIL** for TI *recommended* VCCB max 5.5 V | no assertion of irreversible damage (absolute max 6.5 V) |
| TI-DIR-POS | `DIR=GND`, B input → A output; VCCA and VCCB as above, correct port mapping | **PASS** for **direction-configuration** condition | no end-to-end guaranteed logic if source VOH/load unknown |
| TI-DIR-NEG | `DIR=GND` but requirement is A→B output direction | **FAIL** for explicit direction requirement | not a physical damage claim |
| TI-LOGIC-NEG | B-side `VIH requirement` at VCCB=5.0 V, source guaranteed high max only 3.3 V | **FAIL** for guaranteed B HIGH (3.3 < 3.5 V) | not a verdict that every 3.3 V waveform always fails in practice |
| TI-LOGIC-UNKNOWN | B-side source only “5V logic” but no VOH_min/load spec | **INDETERMINATE** for guaranteed HIGH | nominal language cannot be upgraded to manufacturer guarantee |
| CROSS-FAMILY-PIN | Pico R3 contact mapping pending manufacturer physical review | **NOT_EVALUATED/INDETERMINATE** until source admitted | no fabricated Pico claim |

**[M]** For the TI-LOGIC-NEG case, `VIH,min(B)=0.7*5.0=3.5 V` from the manufacturer table. An explicitly defined **guaranteed** source maximum `3.3 V` is below 3.5 V: positive guarantee impossible. This is a constructed negative-control **test stimulus**, not a claim that the particular ESP32 physical output's actual VOH,max is 3.3 V. [S19]

**[R]** This fixture is much stronger than copying a long datasheet: the exact `DBV` package, DIR dependency and per-rail voltage limits map onto named terminals. Additional current/VOH tests need a declared load/driver and exact table row; missing load → UNKNOWN, not automatic PASS.

---

## 7. Acquisition strategies and maintenance economics

Estimates are **planning assumptions, not timed benchmarking**. Typical cost assumes one experienced reviewer with access to authoritative documentation; 1 engineer-hour is not a quoted salary. Preparation costs for custom parsing exclude legal counsel, hardware procurement and manufacturing tests.

| Strategy | Single simple passive | Complex board/IC | Up-front engineering | Correctness/rights | Drift/repeatability | Classes/scale |
|---|---:|---:|---:|---|---|---|
| **1. Manually reviewed factual records** | **1–3 h** | **6–16 h** | near-zero parsing code | highest human-traceable quality if 2nd reviewer; rights need source check | low drift with immutable SHA pin; manual refresh | slow catalog growth, universal device classes |
| **2. LibrePCB CC0 thin adapter + review** | **0.5–2 h** (if exact part exists) | **4–12 h** (if mappings found) | **12–30 h** narrow importer/validation design estimate | good pad topology, still separate electrical review | stable revision pin, upstream diff triage | useful for passives/IC packages, less for exact boards |
| **3. Semi-automatic PDF/table extraction** | **1–3 h review** despite extraction | **6–20 h review** | **30–90 h** QA+pipeline estimate | OCR/LLM misread ranges/footnotes; vendor ToS risk | PDF edition/section shifts; fragile | theoretically broad, high legal/QA burden |

**[M] Break-even heuristic:** 30 h importer cost vs 1.5 h average net saving = ~20 *eligible* parts, **only if** imports really exist, reviewers are still required, and supplier updates are manageable. For 10 complex boards requiring manual source joins, a generic parser cannot justify its maintenance. This is a cost model, not measured data.

**[R] Chosen hybrid:** for initial 3–8 profiles, use *manual critical evidence + permitted CC0 structure import*. Keep importer *advisory* until a representative sample demonstrates verified pad/mapping precision, actual time reduction and stable licensing. No paid API or scraper dependency. No LLM auto-admission of numerical safety facts.

**[R] AI extraction (later, conditional):** allow only suggestion queue with source-id, exact page/table/cell/footnote, units, context, independent second review for electrical limit, negative controls, conflict resolution; a model-generated fact never attains `APPROVED` automatically. If the website forbids automated extraction, no AI workflow bypasses that restriction.

---

## 8. Evidence acquisition and verification workflow — minimum viable

**[R] Minimal maintainable catalog workflow (7 logical operations, no new topology engine):**

1. **Select exact profile:** manufacturer, orderable MPN, package, board generation/revision, module, SKU and silicon; reject generic label. Source candidates are tracked separately.
2. **Rights review per artifact:** identify exact `LICENSE.txt` or ToS, intended internal/read-only/public API/bundled distribution use, provenance, notices; `RIGHTS_UNVERIFIED` source not eligible for copied import.
3. **Acquire reproducibly:** clone/download *permitted* library artifact once with full commit SHA and file digest; for restricted manufacturer docs retain URL, publication/version, page/section/table/row — don't bulk archive or publish PDFs without rights.
4. **Import structure narrowly:** extract `physical_contact` candidate and pad-to-signal mapping from CC0 records; normalize names, test duplicates/pad sets, and review exact MPN/package; no ideal internal tie automatically invented.
5. **Curate critical facts:** two-person review for `abs_max`, `recommended_op`, `VIH/VIL/VOH/VOL`, drive current, voltage reference, conditional mode/revision; each claim receives stable source locator, confidence, condition, unit, source class and reviewer identity in **auditable records**. This does not require inventing a new canonical ontology.
6. **Resolve conflicts explicitly:** if two revisions differ, retain both version-scoped claims; unresolved same-scope conflict blocks positive verdict. Later source update is change request, not silent override.
7. **Admit + freeze:** deterministic catalog digest, source revisions, test vectors and ruleset version are pinned; CORE-001A `load_catalog` admits only validated snapshots; B/C only consume independently reviewed typed evidence that satisfies their separate contract.

**Source ledger minimum fields [R]:** canonical source URL, publisher/manufacturer, artifact name and edition/revision, Git tag+full SHA or immutable date/version, artifact SHA-256 when lawfully stored, `page/section/table/row`, license-id/terms URL, permission scope, acquisition method, reviewer, review date, copied-vs-derived flag, conflict status. Property ledger must also retain subject identity, terminal(s), property predicate, SI unit, exact bound type (`min/max/typ/abs/recommended`), temperature/supply/load/mode conditions, `UNKNOWN` flag, evidence claim ID and approving reviewer. These are *pipeline metadata requirements*, not a proposal to replace CORE-001A schemas.

**[R] Operational maintenance:** compare upstream pinned SHA against candidate version at a low frequency (e.g. release-based/manual review), classify diff as geometry/metadata/functional/electrical/license. No automatic promotion. Quarterly review is a planning cadence, **not a mandatory background service**; physical labels, discontinued variants and errata may require immediate review when detected.

---

## 9. Thin integration boundary with actual CORE-001A / B / C

### 9.1 Actual audit record (not live repo inspection)

**[F internal project record, not independently re-executed here]** The 2026-11-20 independent CORE-001A audit reports `ACCEPT_WITH_RESTRICTIONS`, **11/11 existing tests passed**, no new code added during audit. It reports exact catalog/definition hashes, frozen typed records, deterministic BFS net reconstruction, evidence-scoped internal ties and canonical serialization. **Crucial failure:** `resolve_terminal` checks physical contact/target value but does **not prove mapping target kind**; a manipulated `GPIO18` `power_domain` claim could appear verified if relying only on the resolver's flag. Source catalog can self-declare approval/publisher; an external trusted catalog pin remains necessary. This report has **not inspected the currently checked-out source tree**, so API claims are documentary rather than fresh runtime certification.

**Documented current exports:** `load_catalog`, `create_snapshot`, `restore_snapshot`, `resolve_terminal`, `compute_nets`, `serialize_snapshot`, `serialize_topology`; records include `CatalogSnapshot`, `DeviceDefinition`, `DeviceIdentity`, `TerminalDefinition`, `SignalMapping`, `EvidenceClaim`, `SourceDocument`, `TerminalRef`, `ResolvedTerminal`, `TopologyResult`. No public catalog-authoring API is documented. The existing graph already represents **two-terminal passives** (supersedes an old Research C premise). [internal audit: `Pasted markdown(20261120-130845).md`]

### 9.2 Boundary table

| Upstream fact | Integration treatment | B or C usage / restrictions |
|---|---|---|
| LibrePCB exact physical pad + device mapping | **narrow transformation** into reviewed existing `TerminalDefinition`/mapping where schema permits | B must prove **contact + target + target kind** separately; missing kind evidence blocks B PASS |
| Generic passive physical leads | **direct structure** after reviewed exact device identity, no ideal tie | C reads 2 distinct terminal references + external R/thermal profile; A does not compute resistance |
| Physical wire/junction, net membership | **already owned by CORE-001A**; never re-import as independent truth | B/C consume a coherent validated `CircuitSnapshot`/`TopologyResult`, not graphics-derived graph |
| ESP-IDF capability masks | **narrow conditional transform**, target/tag/revision pinned | B evaluates possible/configuration/observed separately; no automatic active-firmware claim |
| Zephyr DTS pinctrl/alias | **cross-check only** pending board and source correspondence | cannot overrule exact board hardware or vendor electrical datasheet |
| TI electrical tables, YAGEO resistor rating | **separate typed/versioned fact set**, not topology fields | C checks operating bounds and chosen physical model assumptions; A net connectivity ≠ analog transfer |
| CMSIS-SVD peripheral registers | **keep outside topology catalog** | future B peripheral-mode evidence; no physical pins without other source |
| SVG illustration / 2D placement | **presentation-only** and rights-scoped | NEVER modifies terminal identity or evidence claim |
| Complex analogue dynamics, thermal SPICE models, firmware emulation | **defer** beyond proven bounded analytical checks | future decision and model-extension review if required |

**[R] Integration invariant:** `A_catalog_digest + definition_digest + A_snapshot_digest + B/C_approved_factset_digest + B/C_ruleset_version + operating_context` collectively bind provenance. A definition digest alone **does not** pin a changed evidence-document revision; internal audit explicitly verified catalog digest can change without definition digest changing. Source authenticity requires independent trust of publisher/permissions, not merely self-consistent checksums.

**[U] Possible future model extension:** conditional output transfer behavior, thermal derating curves, multiple mutually exclusive signal ports / stateful buses and exact production lot identity may exceed currently documented `DeviceDefinition`/`EvidenceClaim` schema. This research **does not approve** extensions; represent as separate externally reviewed B/C fact sets until a new decision. When a fact cannot be represented in an approved consumer contract: **NOT_EVALUATED**, not a forged `SignalMapping` or artificial `InternalIdealTie`.

---

## 10. Independent evidence admission and legal acceptance tests

| Gate / input | Requirement | Blocking failure | Expected impact |
|---|---|---|---|
| E-01 exact MPN | manufacturer + orderable package/revision+board generation | generic/clone/unknown revision when relevant | no positive board-specific verdict |
| E-02 physical contacts | manufacturer/source-backed pad count, pad #, names, hidden leads | unresolved duplicate/dangling/missing pad | reject source profile/topology claim |
| E-03 provenance | document edition, source locator, immutable source/fact digest | no page/table/revision, unpinned `latest` for critical item | block critical claim approval |
| E-04 license | file-level rights + intended public distribution checked | no license, copied commercial PDF, restricted CAD source | block import/distribution |
| E-05 kind-binding | contact, target ID and **target kind** independently proved | `J3.9` kind mutated while claim only proves `GPIO18` value | B cannot use verified mapping flag alone |
| E-06 typed limits | SI units and correct `recommended/absolute/typical` semantics | 6.5 V abs max mistaken for 5.5 V recommended | positive voltage outcome blocked |
| E-07 conditions | temperature, VCCI/VCCO, output loading, DIR mode, revision | unconditional extrapolation from one spec row | `INDETERMINATE` |
| E-08 missing bounds | `UNKNOWN` persists for HC-SR04 VOH min, etc. | fabricated zero, nominal guessed as guaranteed | no guaranteed logic PASS |
| E-09 source conflict | same-scope material contradictions shown to reviewer | `latest wins` without adjudication | `EVIDENCE_CONFLICT`, no PASS |
| E-10 independent review | second engineer for electrical limits and critical mappings | same person/LLM suggestion auto-approved | fail admission |
| E-11 deterministic replay | same source+profile+rules ⇒ same canonical findings/hash | order/localization/geometry changes verdict | fail release |
| E-12 negative controls | supply above `5.5 V` TI recommended, swapped A/B, wrong DIR, wrong header | verifier returns global PASS despite violated local rule | fail release |
| E-13 partial success | structural mapping true but electrical data missing | UI says “safe” based on GPIO PASS | no full-system PASS |
| E-14 upstream revision | source edition/part changes | old claim silently applied to new revision | source scope mismatch, review needed |
| E-15 claim scope | chip vs module vs board vs retailer | retail text treated as chip manufacturer-guaranteed limit | claim rejected/reclassified |
| E-16 API and file trust | public methods use validated objects, recomputed `compute_nets`, trusted catalog pin | serialize manually inconsistent snapshot and treat as accepted | reject/never base B/C on it |
| E-17 licensing regression | imported part's LICENSE changes in upstream revision | new restrictive file silently shipped | freeze last admitted artifact; stop promotion |
| E-18 no unsafe inference | absent firmware/mode/simulation, unknown rails | observed ACTIVE or physical safety inferred from wiring alone | `NOT_EVALUATED/INDETERMINATE` |

**[M] Three indispensable negative statements:** (i) `known correct graph` **does not imply** `electrical compatibility`; (ii) `pin capable` **does not imply** `firmware configured or observed active`; (iii) `within absolute maximum` **does not imply** `within recommended operation`.

**[R] Release criterion for single profile:** identity+pins+source+license+critical claims+conditions+unit+negative controls+independent reviewer must all pass; an unknown or legally restricted evidence component may be retained as an *unapproved candidate* but not a basis for safety-positive output.

---

## 11. Rejected sources, methods and misleading shortcuts

- **REJECT [R/F]:** SnapMagic/SnapEDA aggregation of Design Files for competing catalog, given explicitly restrictive terms. [S27]
- **REJECT [R/F]:** SamacSys ComponentSearchEngine material republishing; site terms limit use to internal informational purposes and prohibit distribution. [S28]
- **REJECT [R/F]:** TI site scraping, automated data mining and bundling its manuals in a commercial catalog without permission. [S22,S23]
- **DEFER [R]:** DigiKey/Nexar/Octopart API as primary component truth: supply-chain availability/price does not establish engineering safety; rights/plan/rate terms create recurring dependency. [S29,S30]
- **REJECT [M/R]:** vendor PDF uploaded to LLM → unconditional import of voltage/current maxima. Footnote, package and temperature errors create false positives; usage rights remain unresolved.
- **REJECT [M/R]:** universal `KiCad electrical pin type → hard safe/unsafe` mapping. Pin types are ERC abstractions, not voltage ratings. [S08]
- **REJECT [M/R]:** taking schematic visual net connections from random reference-design source and treating them as board-revision truth without exact source/validation.
- **REJECT [R]:** internal source catalog automatically signs its own claims; CORE-001A audit identified missing external trust pin.
- **REJECT [R]:** importing an open-source application (GPL) just to read CC0 data, unless a specific standalone command-line functionality justifies it.
- **DEFER [R]:** reimplementing KiCad/LibrePCB ERC, CMSIS register debugger, ngspice full solver, or new ontology to acquire component facts. These solve different problems.

---

## 12. Unresolved legal/technical issues — tracked, not invented

| ID | Unresolved | Needed independent resolution | Interim safe behavior |
|---|---|---|---|
| U-E01 | official LibrePCB part files exact MPN availability, file licenses, full Git SHA | read concrete source files before physical import | structural candidates only |
| U-E02 | KiCad copied/adapted library subset ShareAlike scope in proprietary public API | case-specific counsel and exception review | CC0 default; no KiCad binary library publication |
| U-E03 | Espressif board guide and TI/YAGEO/Pi doc redistribution/extraction rights | publisher terms/permission + local legal review | links+independently authored facts; no copies |
| U-E04 | third-party CMSIS packs per-file licenses and origin | read `licenseSets`, files, provenance | no bulk pack import |
| U-E05 | supplied Adafruit #3942 OEM revision and guaranteed output transfer | official matching manufacturer datasheet or measured production characterization | `UNKNOWN` |
| U-E06 | CORE-001A `target kind` evidence gap | independent owner decision after audit | never claim B mapping PASS solely from A verified flag |
| U-E07 | environmental, load, power sequencing for SN74LVC1T45/Pico fixture | approved operating context, full datasheet footnotes, actual rails | narrow local scoped tests only |
| U-E08 | actual local CORE-001A checkout/runtime schemas after audit | verify in separate permitted acceptance phase | no API mutation/implementation authorized |
| U-E09 | source format parser robustness (duplicates, hidden pads, multi-gate) | import dry-run and independent golden test vectors | manual record fallback |
| U-E10 | EU/Georgia database, facts and site-contract treatment of systematic numeric extraction | specialized legal interpretation | non-bulk human review; limited catalog |
| U-E11 | maintenance workload at 50/500 parts | sampled timed study, review drift metrics | no projection as measured savings |

---

## 13. Minimal later implementation recommendation (for future approval only)

**[R] Recommend a bounded acquisition pilot, not authorization:** one pinned LibrePCB CC0 `Base` library import for **two-terminal passive topology**, one manufacturer-reviewed **YAGEO RC0603FR-0710KL** bounded electrical profile, one manually pinned **TI SN74LVC1T45DBVR** device/pad/electrical profile, and an external **Espressif** module/board evidence profile. Optionally stage **Raspberry Pi Pico R3** solely as second-family mapping/capability profile after it meets same evidence gate. There is no reason to ingest millions of parts before validating the gates.

**Acceptance before proceeding:** exact upstream source commit SHA and file digests; a written per-artifact licensing record; documented technical fact source locators and conditions; no unreviewed positive electrical decisions; B mapping-kind limitation resolved or external blocked; CORE-001A tests and new E-01–E-18 negative-control design reviewed; stable provenance across A/B/C. Development sequence, specific code changes and Codex tasks are **not authorized by this report**.

**[R] Decision checkpoint:** Continue only if a small sample demonstrates that exact part pads can be reused lawfully, electrical facts can be independently reviewed, and more than one component family can produce correctly scoped PASS/FAIL/INDETERMINATE without device-specific graph code. Otherwise **narrow** to human-curated fact records rather than enlarging an unreliable importer.

---

## 14. Final decision — SELECT / HOLD / BLOCK

| Question | Final selection |
|---|---|
| **საწყისი წყაროს კომბინაცია** | **SELECT:** official LibrePCB **CC0** structure (Base + applicable official IC library) + official manufacturer **independently curated facts** + ESP-IDF source-backed capability checks; Zephyr / CMSIS მხოლოდ შერჩევითი cross-check [R] |
| **რისი გამოყენება შეიძლება გადაკეთების გარეშე** | CC0 library source files as files; existing LibrePCB CLI library syntax validator as an **optional separate tool**; existing official SDK target headers / Zephyr DTS parsers conditional licensing. `CORE-001A` topology APIs **unchanged** [F/R] |
| **რა უნდა მოერგოს ვიწრო ადაპტერით** | CC0 package pads + signal map → არსებული exact device/terminal fields; ESP-IDF target-specific capability predicates → B typed evidence; stable source IDs/digests → existing catalog / external factset [R] |
| **რა უნდა კურირდეს ხელით** | manufacturer limits, footnotes, exact MPN/revision, `GPIO→board contact`, resistor tolerance/power, TI DIR/logic/load/rail conditions, source rights and conflicts [R] |
| **რა არ შეიძლება ჩაშენდეს არსებულ პირობებში** | TI/manufacturer PDF images/full tables, restricted SnapMagic/SamacSys data, unlicensed CMSIS packs, vendor scraped bulk DB, copied KiCad share-alike-derived proprietary dataset without legal clearance [F/R] |
| **უმცირესი პროცესის სტრუქტურა** | `exact identity → license check → source pin → CC0 structure candidate → manual safety evidence + peer review → admission/negative checks → frozen digest/controlled update` [R] |
| **დამატებითი აპარატურული acceptance** | **TI SN74LVC1T45DBVR** (6 pins) dual-supply bidirectional level translator + declared 3.3 V/5 V rails. Narrow TI supply / DIR / VIH tests have official source-backed PASS and FAIL examples. Link to existing ESP board for immediate bounded test; use **Pico R3** afterwards to challenge MCU-family generalization [F/M/R] |

**კონკრეტული საბოლოო გადაწყვეტილება:** **`SELECT HYBRID-CURATED-CC0`**, **`HOLD` ავტომატურ/მასობრივ კრიტიკულ extraction-ს**, **`BLOCK` არალიცენზირებულ commercial redistribution-სა და უცნობ ფაქტებზე დაფუძნებულ safety PASS-ს**. ეს არის მინიმალური ტექნიკურად გამართლებული, რეპროდუცირებადი და დაბალი recurring-cost გზა, მაგრამ მისი სამართლებრივი და საინჟინრო admission მხოლოდ კონკრეტული არტეფაქტების მიღების შემდეგ გახდება საბოლოო.

---

## 15. Primary-source register — URLs, artifacts and scope

> ბიბლიოთეკის/კოდის ვერსია და datasheet publication edition სხვადასხვა იდენტობაა. ყველა URL არის ოფიციალური მწარმოებლის, პროექტის ან პირობების მფლობელის წყარო, თუ ცალკე მითითებული არაა; კვლევაში მრავალი მათგანი `main/master` ვებ-პუბლიკაციით ჩანს, მაგრამ **reproducible import** ჯერ არ ჩატარებულა.

- **S01 LibrePCB licensing:** https://librepcb.org/license/ ; official libraries CC0-1.0, application GPLv3.
- **S02 LibrePCB Base library:** https://github.com/LibrePCB-Libraries/LibrePCB_Base.lplib ; artifact LICENSE: https://github.com/LibrePCB-Libraries/LibrePCB_Base.lplib/blob/master/LICENSE.txt .
- **S03 LibrePCB S-expression file formats:** https://librepcb.org/features/file-format/ .
- **S04 LibrePCB component/device mapping:** https://librepcb.org/docs/quickstart/create-library-elements/component/ ; https://docs.librepcb.org/_branches/master/librepcb/quickstart/create-library-elements/device/ .
- **S05 LibrePCB CLI:** https://docs.librepcb.org/_branches/master/librepcb/cli/open-library/ ; official release 2.1.1: https://github.com/LibrePCB/LibrePCB/releases .
- **S06 LibrePCB ICs official library:** https://github.com/LibrePCB-Libraries/LibrePCB_ICs.lplib .
- **S07 KiCad licensing:** https://www.kicad.org/libraries/license/ ; symbols https://gitlab.com/kicad/libraries/kicad-symbols ; footprints https://gitlab.com/kicad/libraries/kicad-footprints ; exception https://spdx.org/licenses/KiCad-libraries-exception.html .
- **S08 KiCad documented symbol format:** https://dev-docs.kicad.org/en/file-formats/sexpr-symbol-lib/ ; official KiCad 10 editor pin types https://docs.kicad.org/10.0/en/eeschema/eeschema.html .
- **S09 KiCad footprint format:** https://dev-docs.kicad.org/en/file-formats/sexpr-footprint/ ; official library download https://www.kicad.org/libraries/download/ .
- **S10 Espressif ESP-IDF source & rights:** https://github.com/espressif/esp-idf ; https://github.com/espressif/esp-idf/blob/master/LICENSE ; tagged release https://github.com/espressif/esp-idf/releases/tag/v6.0.3 .
- **S11 ESP32 target capabilities (source-level cross-check):** https://github.com/espressif/esp-idf/blob/master/components/soc/esp32/include/soc/soc_caps.h ; https://github.com/espressif/esp-idf/blob/master/components/esp_driver_gpio/src/gpio.c .
- **S12 Espressif exact board documentation:** https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html ; source https://github.com/espressif/esp-dev-kits/blob/master/docs/en/esp32-devkitc/user_guide.rst .
- **S13 Zephyr main project, binding syntax & source rights:** https://github.com/zephyrproject-rtos/zephyr ; https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/build/dts/bindings-syntax.rst ; release https://github.com/zephyrproject-rtos/zephyr/releases/tag/v4.3.0 .
- **S14 Zephyr devicetree phandle and python parsers:** https://docs.zephyrproject.org/latest/build/dts/phandles.html ; https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/build/dts/intro-input-output.rst .
- **S15 CMSIS spec / parser / data license caution:** https://github.com/Open-CMSIS-Pack/svd-spec ; https://github.com/cmsis-svd/cmsis-svd ; https://github.com/cmsis-svd/cmsis-svd-data ; https://github.com/Open-CMSIS-Pack/Open-CMSIS-Pack-Spec .
- **S16 Adafruit #3942 listing + pinout:** https://www.adafruit.com/product/3942 ; https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/pinouts .
- **S17 Espressif official module datasheet v2.1:** https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html ; official docs index https://www.espressif.com/en/support/documents/technical-documents/esp32-wroom .
- **S18 ESP32 silicon datasheet:** https://documentation.espressif.com/esp32_datasheet_en.html .
- **S19 TI SN74LVC1T45 source, datasheet SCES515N Rev N (June 2024):** https://www.ti.com/product/SN74LVC1T45 ; https://www.ti.com/lit/ds/symlink/sn74lvc1t45.pdf — §4 pins, §5.1 abs max, §5.3 operating, §5.5 electrical.
- **S20 YAGEO RC0603FR-0710KL manufacturer part fact sheet:** https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-0710KL ; generated 2025-12-23.
- **S21 TI legal disclaimer:** https://www.ti.com/legal/important-notice-and-disclaimer.html .
- **S22 TI online terms (scraping/data mining, redistribution):** https://www.ti.com/en-us/legal/terms-conditions/terms-of-use .
- **S23 TI copyright terms:** https://www.ti.com/legal/terms-conditions/copyright.html .
- **S24 CMSIS-Pack rights metadata:** https://open-cmsis-pack.github.io/Open-CMSIS-Pack-Spec/main/html/packFormat.html ; https://open-cmsis-pack.github.io/Open-CMSIS-Pack-Spec/main/html/pdsc_licenseSets_pg.html ; https://github.com/Open-CMSIS-Pack/cmsis-toolbox .
- **S25 Adafruit Fritzing library license:** https://github.com/adafruit/Fritzing-Library .
- **S26 Raspberry Pi Pico board and R3 source:** https://pip.raspberrypi.com/categories/610 ; https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html ; official Pico datasheet https://datasheets.raspberrypi.org/pico/pico_datasheet.pdf .
- **S27 SnapMagic Search legal terms:** https://www.snapeda.com/about/terms/ .
- **S28 SamacSys ComponentSearchEngine terms:** https://componentsearchengine.com/TermsOfUse.html .
- **S29 DigiKey API agreement and data terms:** https://developer.digikey.com/api-user-agreement ; https://www.digikey.com/en/terms-and-conditions .
- **S30 Nexar official API overview:** https://support.nexar.com/support/solutions/articles/101000450648-introduction-to-the-nexar-api ; https://support.nexar.com/support/solutions/articles/101000497890-frequently-asked-questions .

- **S31 ST STM32Cube and CMSIS Device licensing:** https://github.com/STMicroelectronics/STM32CubeF4 ; https://github.com/STMicroelectronics/STM32CubeF4/blob/master/LICENSE.md ; https://github.com/STMicroelectronics/cmsis-device-f4 .
- **S32 SparkFun Eagle XML and library rights:** https://github.com/sparkfun/SparkFun-Eagle-Libraries ; https://github.com/sparkfun/SparkFun-Eagle-Libraries/blob/main/SparkFun-IC-Comms.lbr ; https://creativecommons.org/licenses/by-sa/4.0/ .
- **S33 Microchip official manufacturer machine-readable device packs:** https://packs.download.microchip.com/ ; https://developerhelp.microchip.com/xwiki/bin/view/software-tools/ides/x/projects/packs/work-with-dfps/ ; https://developerhelp.microchip.com/xwiki/bin/view/software-tools/ides/x/projects/packs/dfps-introduction/ ; https://onlinedocs.microchip.com/oxy/GUID-A5330D3A-9F51-4A26-B71D-8503A493DF9C-en-US-11/GUID-A1E48517-2E8D-4E14-B1BB-B3541DB0DA27.html .

### Verification limitations

**[U]** წყაროების URL-ები და გარკვეული კონკრეტული ოფიციალური datasheet ცხრილები ამ ანგარიშისთვის გადამოწმებულია ვებში; თუმცა: (a) არ განხორცილებულა ყველა candidate-library-ის full-tree checkout, Git SHA pin და parser execution; (b) სამართლებრივი დასკვნა კონკრეტულ commercial deployment-ზე იურისტის მიერ არ გაცემულა; (c) არც ერთი ფიზიკური board/sensor არ შემოწმებულა bench-ზე; (d) CORE-001A აუდიტის ანგარიში წავიკითხეთ, მაგრამ ამ კვლევის ფარგლებში source/tests პირდაპირ არ გამოგვიშვია; (e) ზუსტი costs და per-component saved hours შეფასებითი მოდელია. ამიტომ „APPROVED_CANDIDATE“ ნიშნავს **გამოსადეგი მიმართულების არჩევას**, არა უკვე admissible catalog record-ს.
