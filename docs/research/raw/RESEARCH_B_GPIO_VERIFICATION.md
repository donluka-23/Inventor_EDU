# RESEARCH B — GPIO Capability, Pin-Multiplexing & Deterministic Verification

**პროექტი:** INVENTOR EDU  
**დოკუმენტის ტიპი:** დამოუკიდებელი საინჟინრო კვლევა და გადაწყვეტილების *კანდიდატი*, არა დამტკიცებული არქიტექტურა/კოდი/Codex-ის დავალება  
**წყაროების შემოწმების თარიღი:** 2026-11-20 (Asia/Tbilisi)  
**საკვლევი fixture:** Espressif `ESP32-DevKitC V4` / `ESP32-DevKitC-32E` / `ESP32-WROOM-32E` + Adafruit HC-SR04, retail Product ID `3942`  
**მთავარი შეზღუდვა:** `CORE-001A`-ის რეალური იმპლემენტაცია და API ამ კვლევაში **არ არის შემოწმებული**. ქვემოთ აღწერილი შეერთების ინტერფეისები პირობითია.  
**მტკიცებულების ნიშნები:** **[F]** პირველწყაროს ფაქტი; **[M]** ფორმალური/მათემატიკური დასკვნა; **[R]** არქიტექტურული რეკომენდაცია; **[U]** დაუდასტურებელი, შესამოწმებელი ვარაუდი.

---

## 1. Executive recommendation and confidence

**[R] რეკომენდაცია: `SOURCE-BACKED TYPED FACTS + DETERMINISTIC FINITE-DOMAIN RULES`.** პირველ GPIO-სუბსისტემას უნდა მიეწოდოს `CORE-001A`-ის *დადასტურებული* physical-terminal/net references, იდენტობაზე მიბმული წყაროები, მოთხოვნილი ფუნქციები და ცალკე კონფიგურაციის კონტექსტი. მან უნდა შეაფასოს მკაფიო შეზღუდვები და დააბრუნოს ლოკალიზაციისგან დამოუკიდებელი ახსნადი შედეგები. ზოგადი წესები არ უნდა შეიცავდეს ESP32-თვის ჩაშენებულ GPIO-ნომრებს. პირველი მტკიცებულებათა ნაკრები კი შეიძლება იყოს ხელით კურირებული და მკაცრად ვერსირებული.

**არ ავიღოთ თავდაპირველ დამოკიდებულებად** KiCad ERC engine, Z3, SDK-ის runtime, firmware emulator, SPICE ან დიდი გარე pinout database. Espressif-ის SDK გამოიყენება **ფაქტების დამოუკიდებელი გადამოწმებისთვის და შემდგომი არჩევითი runtime-ინსპექციისთვის**, არა canonical model-ის ჩანაცვლებისთვის. Zephyr-ის DTS მხოლოდ დამატებითი, ვერსიისა და დაფის კონტექსტით შეზღუდული cross-check-ია. [S01–S09]

| გადაწყვეტილება | სტატუსი | დასაბუთება/ნდობა |
|---|---|---|
| ოთხი დამოუკიდებელი შემოწმება: *possible*, *configuration permitted*, *actually active*, *electrical compatible* | **დასამტკიცებელი MUST** | [M/R], მაღალი; სხვადასხვა ტიპის დასკვნების გაერთიანება ცრუ PASS-ს ქმნის |
| typed lookup/constraints + deterministic evaluation | **SELECT კანდიდატი** | [F/M/R], მაღალი პირველ GPIO პრობლემებზე, შესრულების benchmark ჯერ არაა |
| board→module→SoC mapping მხოლოდ დადასტურებული ფაქტით | **MUST** | [F/R], მაღალი; დაფა და სილიკონი არ არის ერთი იდენტობა |
| `ESP32-DevKitC-32E` + Adafruit #3942 | **მხოლოდ acceptance fixture** | [F], მაღალი დასახელებულ კატალოგურ დონეზე; რეალური PCB revision არ დადასტურებულა |
| live ESP-IDF config reader | **DEFER** | API დოკუმენტირებულია, მაგრამ telemetry/instrumentation/firmware coverage არ შემოწმებულა |
| SMT/Z3, KiCad ERC runtime | **DEFER/REJECT as mandatory** | შედეგისთვის საჭირო დამატებითი უნიკალური ამოცანა ვერ დასტურდება |

**ნდობის საზღვრები:** ESP32-ის input-only და board header mapping — მაღალი; pinmux architecture — მაღალი პრინციპის დონეზე, არა ყველა პერიფერიის ყველა timing რეჟიმზე; დასახელებულ Adafruit ნივთზე retail აღწერა — საშუალო, რადგან OEM/PCB რევიზია და გარანტირებული electrical transfer characteristics არ დადასტურებულა; CORE-001A ინტეგრაცია, ტექნიკური KPI და კომერციული ღირებულება — **UNVERIFIED**.

## 2. Formal verification requirements

შესამოწმებელი ობიექტია **მოთხოვნა**, არა ზოგადად „კარგი ან ცუდი წრედი“. ყოველი მოთხოვნა იდენტიფიცირებულია `requirement_id`-ით, კონკრეტული ფიზიკური `TerminalRef`-ით, `net_id`-ით (როდესაც საჭიროა), `requested_function`-ით, `mode`-ით, `configuration`-ით, `device_definition_digest`-ით, `evidence_set_digest`-ით და `rule_set_version`-ით.

**R-B01 Identity.** `board variant`, მოდული, სილიკონის family/revision (თუ rule-ზე მოქმედებს), ინსტანსი და ფიზიკური terminal არასოდეს შეიცვალოს თავისუფალი სახელით/სურათით/„მსგავსი ESP32“-ით. [R]

**R-B02 Mapping.** physical board contact → module/SoC GPIO mapping იყოს `verified / ambiguous / unknown` სტატუსის მქონე. ერთი და იგივე GPIO ნომერი არ ადგენს, რომ სხვადასხვა დაფის header-ები იდენტურია. [R]

**R-B03 Requested function.** `GPIO_IN`, `GPIO_OUT`, `PWM_OUT`, `ADC_IN`, `UART_TX`, `I2C_SDA` და ა.შ. იყოს ტიპიზებული intent; `Trig`/`Echo` ურთიერთობა მოდის კონკრეტული sensor-interface contract-დან, **არა** მხოლოდ მავთულის ნახატიდან. [R]

**R-B04 Physical possibility.** იმ კონკრეტული silicon+board+pin+mode წყვილის მხარდაჭერა/შეუძლებლობა წყაროდან დასტურდებოდეს. ESP32-ზე GPIO34 output-ის უარყოფა აქ ფუნდამენტურია. [F/M]

**R-B05 Configuration legality.** „შესაძლებელია“ არ ნიშნავს „მოცემულ კონფიგურაციაში დაშვებულია“: პარალელური ownership, GPIO matrix, flash/PSRAM, boot strap, low-power state და pinmux პრიორიტეტები ცალკე შეფასდეს. [R]

**R-B06 Active state.** გამოცხადებული configuration (design intent), firmware-ში დანახული configuration (snapshot observation) და რეალურად მიმდინარე electrical signal სამ სხვადასხვა მტკიცებულებად დარჩეს. ცარიელი firmware data → `INDETERMINATE` შესაბამის active-config მოთხოვნაზე. [R]

**R-B07 Electrical boundary.** 3.3V↔5V compatibility, thresholds, current limits, pull-ups და load არ გადაწყდეს GPIO capability PASS-იდან. ეს RESEARCH C-ს/შემდგომ ელექტრულ checker-ს ეკუთვნის. [R]

**R-B08 Evidence conflict.** ერთი და იმავე revision/scope-ის ურთიერთგამომრიცხავი ავტორიტეტული ცნობები არ გაიხსნას ავტომატური `latest wins`/`strongest source wins` წესით; საჭიროა ექსპერტის adjudication. [R]

**R-B09 Determinism.** მოცემულ frozen input+catalog+rules version-ზე ერთი და იგივე `findings`, ID-ებით დალაგებული, დამოუკიდებლად input order/locale/UI geometry-ისა. [M/R]

**R-B10 Result vocabulary.** მხოლოდ `PASS`, `FAIL`, `INDETERMINATE`, `NOT_EVALUATED`; warning/error `severity` არის *ცალკე ველი*. `PASS` ნიშნავს **მხოლოდ** კონკრეტული check-ის დაკმაყოფილებას, არა მთლიანი მოწყობილობის უსაფრთხოებას. [R]

## 3. Scientific and established engineering foundations

### 3.1 Formal model — capability is not configuration

განვსაზღვროთ: `b` — ზუსტი board+module+SoC პროფილი; `p` — ფიზიკური კონტაქტიდან გადაყვანილი SoC pad; `f` — მოთხოვნილი ფუნქცია/მიმართულება; `c` — გამოცხადებული კონფიგურაცია; `s` — operating/power/boot state; `e` — მოქმედი მტკიცებულებები.

1. `Mapped(b,p,e)` — არსებობს დადასტურებული board-terminal→SoC mapping.
2. `Capable(b,p,f,s,e)` — შესაბამის მდგომარეობაში სილიკონს/მოდულს შეუძლია ფუნქციის შესრულება.
3. `Allowed(b,p,f,c,s,e)` — კონფიგურაცია აკმაყოფილებს known occupancy, pinmux, reserved, mode constraints-ს.
4. `ObservedActive(b,p,f,t,e)` — მითითებულ დროის `t`-ზე ცალკე დაკვირვება ადასტურებს შესაბამის მიმდინარე კონფიგურაციას.
5. `ElectricalCompatible(net,loads,conditions,e)` — სხვა checker-ის ფორმალური მიზანი.

**[M]** `Capable ⇒ Allowed` მცდარია; `Allowed ⇒ ObservedActive` მცდარია; `ObservedActive ⇒ ElectricalCompatible` მცდარია. მაგალითად `GPIO18` output-capableა, მაგრამ პროგრამამ შეიძლება ის input-ად გადაიყვანოს; `GPIO19` input-capableა, მაგრამ დაუცველი 5V `Echo` მის ფიზიკურ მიმღებლობას მაინც არღვევს. [S01–S04,S07]

**[M]** თუ ყველა საჭირო წინაპირობა წყაროებით დადასტურდა, check აბრუნებს `PASS`; თუ ცნობილი და მოქმედი წინაპირობის პირდაპირი უარყოფა დასტურდება — `FAIL`; თუ მნიშვნელოვანი ფაქტი, mode ან კონფიგურაცია აკლია — `INDETERMINATE`; თუ requested metric ან device-profile საერთოდ არ არის შემოწმების მხარდაჭერილ საზღვრებში — `NOT_EVALUATED`. `INDETERMINATE` არ უდრის ნებადართულობას. `NOT_EVALUATED` არ ნიშნავს ფიზიკურ შეუძლებლობას.

### 3.2 Engineering methods

| მეთოდი | რას აგვარებს | წინაპირობები / ფორმალური საფუძველი | პირველ ეტაპზე |
|---|---|---|---|
| EDA ERC (KiCad 10) | electrical pin-type conflict, undriven power, open connections | symbol pin-type matrix; სწორად მინიჭებული type-ები; ERC-ს არ აქვს firmware/სილიკონის სრული კონტექსტი [S08] | კონცეპტუალური reference; არა runtime truth |
| Finite-domain typed rules | `input_only`, `output_allowed`, role/mode, reserved/pinmux constraints | finite sets, predicate checks, set membership; source-backed scope | **შერჩეული** |
| Deterministic state machine | boot/runtime/deep-sleep/hold transitions | explicit transitions; არარსებული state არ გამოიცნოს | მინიმალური mode enum; ღრმა state machine მოგვიანებით |
| SAT/SMT (Z3) | *არსებობს თუ არა* ერთდროული pin assignment ფიქსირებული დამატებითი constraints-ით | სრული და სწორი axioms; `SAT/UNSAT/UNKNOWN`; solver correctness ≠ spec correctness [S15,S16] | გადავადებული |
| Runtime firmware inspection | ერთი *მიმდინარე* pinmux/enable setting-ის ამოკითხვა | target-ზე instrumented trusted firmware, შესაბამისი SDK release, timestamp | არ არის mandatory; future optional |
| Netlist/topology | რომელი terminals იზიარებს net-ს | CORE-001A connected components; ელექტრული თავსებადობა არ გამომდინარეობს | გარე სავალდებულო input, არა ხელახალი implementation |

**[M] soundness:** შედეგი `FAIL` უნდა ჰქონდეს შემოწმებული წინაპირობის საზღვრებში რეალურ საწინააღმდეგო მტკიცებულებას; `PASS` — ყოველი საჭირო წინაპირობის დაკმაყოფილებას. **[U] completeness** ყველა შესაძლო silicon/pinmux/firmware combination-ზე არ მიიღწევა. Z3-ის mathematical `UNSAT` მხოლოდ ფორმულირებული constraints-ის არაშესრულებადობას ამტკიცებს, არა datasheet-ის ან firmware-ის სიმართლეს.

## 4. Existing OSS implementations and exact reusable APIs

**ვერსიის წესი:** `ESP-IDF v5.5.6` გამოიყენება ქვემოთ reproducible *source review target*-ად, რადგან შესაბამისი ოფიციალური documentation/source paths ამ თარიღისთვის ხელმისაწვდომია; ეს **არ ნიშნავს SDK-ის დაყენებას** backend-ზე. სხვა SDK release-ს ავტომატურად არ მივანიჭოთ იდენტური API-ს/behaviour-ის გარანტია.

| წყარო / ბმული | კონკრეტული მონაცემი ან callable interface | პრაქტიკული გამოყენება | ზღვარი |
|---|---|---|---|
| `esp-idf/components/soc/esp32/include/soc/soc_caps.h` at `v5.5.6` [S03] | `SOC_GPIO_VALID_GPIO_MASK`, `SOC_GPIO_VALID_OUTPUT_GPIO_MASK` | silicon-level valid/output-capable sets-ის cross-check | **არ** შეიცავს DevKitC header pinmap-ს, onboard flash policy-ს და firmware activity-ს |
| ESP-IDF GPIO API [S02,S04] | `GPIO_IS_VALID_GPIO`, `GPIO_IS_VALID_OUTPUT_GPIO`, `gpio_config()`, `gpio_get_io_config()` | compiled SDK-ით cross-check/სურვილისამებრ target snapshot | SDK-ს კითხვა არ ადასტურებს გარე circuitry-ს; output mask ≠ board availability |
| `gpio_dump_io_configuration(FILE*, uint64_t)` [S02] | მიმდინარე `InputEn`, `OutputEn`, `OpenDrain`, `FuncSel`, GPIO matrix signal, `RESERVED` report | არჩევითი instrumentation / verification-test observation | `stdout`-ის text parsing brittle; უფრო მკაფიო structured adapter საჭიროა; მხოლოდ temporal snapshot |
| `soc/esp32/include/soc/gpio_sig_map.h` [S05] | peripheral signal IDs | `gpio_dump...` signal-ის decoding/reference | signal ID ≠ pin-ის assigned active truth უცვლელად ყველა firmware-ზე |
| `driver/gpio.h`, `hal/gpio_types.h` [S04] | configuration enums/structs/inspection declarations | inventory იმისა, რა შეიძლება ვნახოთ target-იდან | `gpio_config()` overwrites earlier settings; runtime არ უნდა გამოვიძახოთ checker-იდან არასასურველი side effect-ით |
| Espressif board guide [S01] | physical J2/J3 position, board variant, flash pins, power source modes | **პირველადი board mapping authority** | board PCB variant/revision-ის ფიზიკური იდენტიფიკაცია ჯერ საჭიროა |
| `Zephyr ... esp32_devkitc_procpu.dts` [S09] | `gpio-reserved-ranges`, aliases, `pinctrl-0` | მეორე software representation-ით discrepancy detection | `PROCPU` software target და მისი DTS **არ არის** exact `ESP32-DevKitC-32E` maker schematic; ზოგ ნაწილს ხვდება სხვა module configuration |
| CMSIS-SVD schema [S11] | register/peripheral memory-map schema | სხვა Arm-family metadata evaluation | memory-mapped registers ≠ header contacts, electrical ratings ან active firmware; ESP32 classic Xtensa target-ზე არ არის primary source |
| KiCad 10 ERC [S08] | symbol pin categories/conflicts map | pin-type semantics-ის შესადარებელი მოდელი | symbol pin table ≠ runtime pinmux ან guaranteed voltage compatibility |
| Z3 4.15.6 [S15] | SMT-LIB/`Solver.check()`/`model()`/UNSAT reasoning | **მხოლოდ მომავალი constraint planning**, თუ კომბინატორული მტკიცებულება საჭირო გახდა | სერვისის/ორაკლის ახალი dependency და ფორმალიზაციის ღირებულება; პირველ ვერსიაში არ დავამატოთ |

**კონკრეტული ეფექტურობა:** პირველ fixture-ზე `GPIO34`-ის output-ით შეზღუდვა არის ერთი sourced boolean/role predicate; `GPIO18` output / `GPIO19` input — მსგავსი finite checks; flash pins — board-policy membership; unspecified firmware → explicit unknown. ამისთვის გარე solver-ის ჩართვა არ ამცირებს სემანტიკური მონაცემების შექმნის სამუშაოს. [M/R]

**Source artifacts არ გადმოვაკოპიროთ default-ად.** ტექნიკურად შეიძლება SDK-ის `soc_caps.h`-ის mask-ებიდან დამოუკიდებელი curated facts-ის მიღება, მაგრამ ფაქტების წყარო, exact release, scope და human review დადასტურდეს. Pydantic v2 მოდელები RESEARCH A-ს კუთვნილებაა; დამატებითი „parallel canonical schema“ არ არის საჭირო.

## 5. Manufacturer data sources and legal access

### 5.1 Silicon vs board vs module vs firmware — evidence hierarchy

| დონე | მაგალითი | რას ამტკიცებს | რას ვერ ამტკიცებს |
|---|---|---|---|
| silicon | ESP32 `SOC_GPIO_VALID_OUTPUT_GPIO_MASK`, ESP-IDF GPIO docs [S02,S03] | GPIO34–39 input-only; შესაძლო matrix routes | საბოლოო header availability, firmware state |
| module | ESP32-WROOM-32E datasheet v2.1 [S06] | module pinout, flash connections, boot modes | კონკრეტული DevKitC connector position |
| assembled board | DevKitC V4 / `-32E` guide [S01] | J2.5=IO34; J3.9=IO18; J3.8=IO19; board-level warnings | ყველა clone-ვარიანტის ან დაუდგენელი PCB assembly-ს სისწორე |
| firmware build | pinned ESP-IDF project/`sdkconfig`, inspected source | code-declared pin settings კონკრეტულ build-ზე | გარანტირებული runtime/external hardware state |
| live observation | trusted firmware `gpio_get_io_config`/dump output [S02] | pin register მდგომარეობა დაკვირვების მომენტში | sensor-ის ძაბვა, I/O waveform, სხვა დროის მდგომარეობა |
| retail sensor listing | Adafruit #3942 page & guide [S07] | `Trig` input/3V or 5V trigger, `Echo` reported 5V logic | OEM/manufacturing revision; VIH/VIL, output driver guaranteed `min/max` |

**[F] Exact board pins, official guide:** `J2.5 → IO34 (I)`, `J3.9 → IO18 (I/O)`, `J3.8 → IO19 (I/O)`. `J2.16–18` და `J3.17–19` გამოსახავს D2/D3/CMD და D1/D0/CLK-ს, რომელიც SPI-flash-ისთვის გამოიყენება; ეს *არსებობს* როგორც board contact, მაგრამ SDK-ის `GPIO_IS_VALID_OUTPUT_GPIO` წარმატებაც არ აძლევს უფლებას ის გამოცხადდეს თავისუფალ application pin-ად. [S01,S02]

**[F] Official strapping pins:** GPIO0, GPIO2, GPIO5, GPIO12 (MTDI), GPIO15 (MTDO). Boot-mode ეფექტი დამოკიდებულია reset/startup timing, pull level და board circuitry-ზე; მხოლოდ „strapping“ ფაქტი **არ** ნიშნავს ავტომატურ boot failure-ს. [S02,S14]

**[F] GPIO34–39:** input-only და software-enabled internal pull-up/pull-down არ აქვთ; GPIO34 `Echo` input-ისთვის *როლის* გამო არ არის აკრძალული, თუმცა input bias/electrical compatibility სხვა checker-მა უნდა შეაფასოს. [S02,S03]

**[U] Hardware gap:** ერთ ცალ რეალურ DevKitC-სა და Adafruit SKU #3942-ის OEM PCB revision-ს ვერ ვიდენტიფიცირებთ მხოლოდ კატალოგით. `Adafruit sold SKU` არ უდრის `Adafruit manufactured silicon/module`. 5V `Echo` აღწერა არ არის guaranteed output-Voh interval. შესაბამისად manufacturer-level electrical `PASS` აქ არ არსებობს. [S07]

### 5.2 Mandatory claim record

`claim_id`; `subject_identity` (maker/part/board/module/revision); `physical_terminal_ref` / `target_soc_signal`; `predicate` (`OUTPUT_ALLOWED`, `STRAPPING`, `FLASH_RESERVED`, `PULLUP_AVAILABLE`, `MAPPING`); `value`; `conditions` (mode, voltage, boot phase); `source_url`; `source_revision`/release; `page_or_symbol_locator`; `source_class`; `reviewer`; `review_date`; `rights_status`; `derivation_status`; `confidence_qualification`; `supersedes?`; `catalog_digest`. **[R]** Derived metadata should never overwrite direct vendor observations. Null source/revision → blocked positive verdict if required.

**[R] Admission workflow:** authoritative HTML/datasheet/source version → independently compare exact board/module claim → human record approval → stable catalog digest → golden fixtures. Source changes require new `definition_digest`/claim version and regression tests; old projects are not silently reinterpreted. Datasheet/website contents are **viewable evidence**, not automatically redistributable source assets.

## 6. GPIO/pin-function constraint model

### 6.1 Minimum typed fact categories

| Type | Required semantics | Example value |
|---|---|---|
| `PhysicalPadMapping` | `board_terminal`, `module_contact?`, `soc_signal`, mapping evidence and ambiguity | `board1:J3.9 → GPIO18` |
| `PinDirectionCapability` | supported input/output/analog/open-drain driver type *if sourced* | GPIO34 `input=true`, `output=false` |
| `PinFunctionCapability` | generic/peripheral function identifiers, prerequisites, mode | GPIO18 `GPIO_OUT` supported; exact peripheral route separately sourced |
| `PinOwnershipConstraint` | exclusive output selector, shared input allowance, reserved resource | external flash owns GPIO6–11 under `-32E` board policy |
| `BootStrapConstraint` | sampled startup level, conditions, lifecycle | `GPIO0`, `GPIO2` marked strapping; exact boot judgment needs more data |
| `PowerModeConstraint` | active/sleep/reset state, persistence/hold, conditional capability | unknown deep-sleep config → not PASS |
| `FirmwareEvidence` | declared vs observed, target/build digest, time, capture method | `observed GPIO18 output` at instant T; not whole runtime |
| `RulePrerequisite` | needed identity/claims/context and evidence quality | output-only checker does not require Echo voltage |

### 6.2 Rule set — deterministic, machine-checkable semantics

**B-G01 / Mapping.** If no unique pinned physical-contact-to-target mapping exists, stop downstream GPIO-specific verdict for that contact with `INDETERMINATE`, reason `AMBIGUOUS_MAPPING`/`MISSING_MAPPING`. If the device has no admitted definition → `NOT_EVALUATED: UNSUPPORTED_DEVICE`.

**B-G02 / Physical direction.** For `GPIO_OUT`, a documented `output=false` is `FAIL: OUTPUT_NOT_CAPABLE`; `output=true` is `PASS` **only for the capability check**. For `GPIO_IN`, documented `input=true` is `PASS` for capability; no special blanket ban on input-only pins. Missing fact is `INDETERMINATE: CAPABILITY_UNKNOWN`.

**B-G03 / Board availability.** If exact board policy tags a pad as occupied by internal flash or other non-releasable resource, using it for user-requested output is `FAIL: RESERVED_RESOURCE` **for this board-use policy**, not proof that silicon cannot output. Variant mismatch → `NOT_EVALUATED` or `INDETERMINATE` by coverage/missing-data distinction. `GPIO_IS_VALID_OUTPUT_GPIO` is *not* sufficient here. [S01–S03]

**B-G04 / Pinmux eligibility.** `function∈documented_supported_functions(pin,mode)` is necessary. For functions with movable GPIO matrix signals, allow alternative routes where source and mode support; high-speed/dedicated IOMUX conditions remain explicit. Unsupported function → `FAIL`; absent sufficient profile or mode data → `INDETERMINATE`. **Do not encode a universal one-pin/one-input-function restriction:** input fan-out may be legal; output control/peripheral ownership should be assessed by actual hardware semantics. [S02,S05]

**B-G05 / Ownership/conflict.** Two mutually exclusive *output* functions assigned to the same physical driver in the same active state → `FAIL: OUTPUT_OWNER_CONFLICT` if exclusivity is documented. Input monitor alongside PWM output must not be rejected automatically because ESP-IDF documents dual-purpose IO. Unknown sharing rules → `INDETERMINATE`. [S02]

**B-G06 / Boot strap.** If a known strapping pad participates in a design, emit a scoped `BOOT_STRAP_CONDITION` check. Without specified reset-time pull/timing and board circuitry → `INDETERMINATE` + warning severity, **not** `FAIL: BOOT_FAILURE`. Demonstrated, explicit contradictory reset constraints can support a narrower `FAIL`; simply assigning `GPIO0` after boot cannot. [S14]

**B-G07 / Firmware.** `requested_function` and `configured_function` differ → `FAIL: DECLARED_CONFIG_MISMATCH` *only where the specified configuration is authoritative for that check*. If unknown → `INDETERMINATE: ACTIVE_CONFIG_UNKNOWN`; if current register observation confirms matched state → `PASS` for `OBSERVED_CONFIGURATION_AT_T`, **not** `pass for all firmware states`. One-time firmware source analysis alone cannot prove current runtime config. [S02]

**B-G08 / Power state.** Applicability predicate must include `ACTIVE`, `RESET`, `BOOT_SAMPLING`, `SLEEP` etc. Unknown state or state transitions → scoped `INDETERMINATE`; do not promote ACTIVE capability to all sleep states. [S02]

**B-G09 / Open-drain vs push-pull.** Output-drive electrical interface is conditional on configured mode and external pull-up/rail: permitted `open-drain` driver setting alone is not proof of a valid bus. GPIO B verifies supported drive mode; voltage and resistor/bus adequacy are delegated to RESEARCH C. [R]

**B-G10 / Conflicting/missing evidence.** Same scope, different incompatible claims → `INDETERMINATE: EVIDENCE_CONFLICT`; no silent precedence. Source missing → `INDETERMINATE: EVIDENCE_MISSING`; unsupported request → `NOT_EVALUATED: OUT_OF_SCOPE`. [R]

### 6.3 Output status and message contract

| `status` | Strict meaning | Typical `reason_code` | `severity` example |
|---|---|---|---|
| `PASS` | specified check, specified scope, all necessary verified predicates satisfied | `CAPABILITY_CONFIRMED` | info |
| `FAIL` | specified, applicable rule violated by sourced fact/config | `OUTPUT_NOT_CAPABLE` | error |
| `INDETERMINATE` | supported check cannot settle result because required fact/state/evidence is missing/conflicting | `ACTIVE_CONFIG_UNKNOWN` | warning |
| `NOT_EVALUATED` | checker does not implement request/device/metric, or deliberately delegated | `UNSUPPORTED_DEVICE`, `ELECTRICAL_CHECK_DELEGATED` | info/warning |

**[R]** `WARNING` არ არის status და არ ფარავს `INDETERMINATE`-ს. One `PASS` for GPIO direction must coexist with `NOT_EVALUATED` for electrical voltage and `INDETERMINATE` for unknown live firmware. Final UI should not invent a single universal green pass.

## 7. Device-independent rule architecture

**[R] Basic engine consists of five *logical* roles, not five mandatory services:** (1) `Topology/identity adapter` reads verified CORE-001A result; (2) `EvidenceResolver` loads frozen data; (3) `RequestNormalizer` makes explicit intents; (4) `ConstraintEvaluator` traverses typed rules, no vendor constants; (5) `FindingFormatter` returns stable IDs/codes/links. Localization and display are downstream.

**Rule representation:** `rule_id`, `rule_version`, `applicability_predicate`, `required_claim_types`, `required_context_keys`, `evaluation_operator` (finite set membership/equality/conflict/implication), `failure_code`, `unknown_code`, `affected_ref_selector`, `evidence_policy`. For the first stage **typed, reviewed rule modules/functions** are preferable to a free-form YAML/RDF rule language or arbitrary-expression execution. No dynamic `eval` and no user-supplied Python code. Device-specific pin facts live in versioned profiles, not `if gpio == 34` production logic.

**Evaluation order:**

1. Validate snapshot/catalog hashes, IDs and schema; malformed input is *typed validation error*, not `PASS/FAIL` engineering finding.
2. Resolve physical terminal and mapping; unresolved mapping blocks dependent constraints.
3. Normalize requested function and context; if no requirement was requested, do not infer it from a random wire.
4. Evaluate known silicon/board-capability predicates.
5. Evaluate state, pinmux and ownership constraints where their prerequisites exist.
6. Evaluate declared-vs-observed firmware as **separate** evidence channels.
7. Attach deferred electrical check refs; never compute GPIO voltage safety here.
8. Sort findings by `(requirement_id, rule_id, affected_ref, reason_code)`; compose stable deterministic report.

**[M]** For fixed finite rules and pins, direct evaluation scales approximately with relevant `(requirements × indexed rules/facts)` and source resolution; no SAT search is needed. Formal proof uses conjunction of applicable predicates. A rule failure is supported only if its antecedent holds and its expected consequent is demonstrably false; otherwise retain unknown. **No performance figure is asserted because no benchmark was run.**

## 8. Proposed integration interfaces — provisional, CORE-001A audit required

**Existing Research A candidate (NOT a verified production API):** `CatalogSnapshot`, `DeviceDefinition`, `TerminalDefinition`, `SignalMapping`, `CircuitSnapshot`, `TerminalRef`, `TopologyResult`, `resolve_terminal(...)`, `compute_nets(...)`. Research A suggests Python/Pydantic v2, immutable-style models, explicit nets and SHA-256 catalog pinning. The *actual* fields/functions may differ: CORE-001B must not be authorized until a real CORE-001A report proves them. [Internal: RESEARCH A §§5–7]

### 8.1 Narrow semantic adapter input

| Proposed field | Consumer | Provenance/invariant |
|---|---|---|
| `snapshot_sha256`, `catalog_digest`, `topology_schema_version` | repeatability and version rejection | from verified CORE-001A result |
| `terminal_ref` (`instance_id`, `terminal_id`) | finding anchor | persistent physical contact, never text label |
| `net_id` | relation to external Trig/Echo and joint nets | existing topology; no new graph interpretation |
| `mapping_target` and `mapping_status` | SoC/board pin mapping | catalog + sourced mapping, unknown allowed |
| `device_definition_id`, `definition_digest`, `module_variant`, `reviewed_claim_set` | applicable facts | exact scope; no clone fallback |
| `requested_function`, `requested_direction`, `requirement_id` | evaluation demand | educational scenario intent / user action, typed |
| `declared_config`, `observed_config`, `operating_state`, `observation_time` | mode and activity checks | distinct optional inputs; unknown by default |
| `rule_set_version`, `evidence_set_digest` | reproducible findings | pinned rule/catalog versions |

### 8.2 Candidate interface signatures (*description only; not implementation*)

- `resolve_gpio_context(topology, catalog, terminal_ref, request, operating_context) -> GpioContextResolution`.
- `verify_gpio_requirements(contexts, capability_claims, ruleset) -> tuple[VerificationFinding, ...]`.
- `summarize_gpio_coverage(findings, requested_checks) -> VerificationCoverage`.

**`VerificationFinding` suggested fields:** `finding_id`, `requirement_id`, `rule_id`, `rule_version`, `status`, `reason_code`, `severity`, `affected_terminals`, `affected_nets`, `evaluated_function`, `specified_state`, `source_claim_ids`, `missing_claim_types`, `assumptions`, `source_snapshot_hash`, `catalog_digest`, `evidence_set_digest`, `rule_set_digest`, `observed_at?`, `scope`, `remediation_key?`. Text explaining a failure is created outside checker from `reason_code` and explicit source data. `finding_id` generation must use versioned canonical bytes, **not Python hash()/random**.

**[R]** Avoid adding GPIO-specific mutable fields to `ComponentInstance` or embedding device lists into the algorithm. If CORE-001A supplies only one-hop `SignalMapping`, the multi-hop board→module→chip proof can initially live as independent catalog claims resolved by an adapter: no change to connectivity or net definitions without a proven contradiction.

**Boundary failure policy:** schema/catalog mismatch → typed ingestion/contract error; unsupported device but valid snapshot → `NOT_EVALUATED`; supported but source incomplete → `INDETERMINATE`; invalid net mapping/unknown physical terminal → propagate CORE-001A error, do not create a synthetic GPIO. **No assumed actual API names.**

## 9. Development cost-reduction comparison

| Approach | Correctness / extensibility | Initial effort and maintenance | Zero-fee / legal risk | Decision |
|---|---|---|---|---|
| **A. Manually curated, versioned typed facts + deterministic checks** | high where exact facts exist; vendor-independent predicates; explicit `unknown` | tiny first fixture, but each new board takes review; source changes trigger tests | no additional runtime license/cloud; externally sourced facts retained as provenance | **SELECT v1** |
| **B. SDK/Zephyr/CMSIS metadata ingestion + thin adapter** | partial silicon/peripheral facts, multi-family growth possible; board revision coverage not guaranteed | parser/sync, upstream schema/version changes, conflict adjudication; cannot replace manual datasheet review | SDK and Zephyr largely Apache-2.0, specific files/third parties audit | **OPTIONAL next, source-by-source gate** |
| **C. Generalized Z3/SMT solver** | useful for multi-pin assignment with global constraints; no automatic hardware truth | encoding, solver limits, unsat explanations, maintenance/QA increase | Z3 MIT; runtime/binary distribution audit | **DEFER** |
| **D. KiCad ERC as native runtime** | excellent electrical pin-type ERC for schematics; firmware/pinmux gaps remain | format conversions, GPL distribution constraints, conflict of authority | GPLv3+ and varied component assets | **NO** first B verifier |
| **E. Build a firmware emulator** | selected peripheral observations only; analog pin truth absent | large model/target/coverage cost | tool-specific licenses/complexity | **NO** |

**[R] Quantitative gate rather than invented cost figures:** track new `DeviceDefinition`/claim preparation minutes per part, review failures, source mismatch rate, fixtures passed, dependency count, maintenance changes per upstream release, and number of previously undecidable checks newly resolved by each adapter. Until measured, claiming automation of vendor metadata produces a net saving is **[U]**.

**Upgrade to B** only after at least two additional distinct board families reveal repeated sourced field-extraction work that a maintained parser reduces *without* lowering audit quality. **Upgrade to C/Z3** only when a concrete simultaneous assignment problem (e.g., allocate N peripheral signals across M GPIOs subject to exclusive owners, reserved pads and boot constraints) defeats simple explicit enumeration in measured scenarios, and independently hand-derived SAT/UNSAT oracle cases are available.

## 10. Licensing, distribution and maintenance audit

**No runtime service, account, API key, pay-per-call quota or commercial library license is required by the recommended first checker.** *Free access* and *right to redistribute a PDF/PCB image/dataset* are not the same. The per-artifact release/notice/transitive-dependency review is still mandatory.

| Component / source | Version & official URL | License / reviewed evidence | SaaS, commercial and redistribution position | Admission decision |
|---|---|---|---|---|
| Python stdlib | CPython 3.12.x for A proposal; https://www.python.org/ | Python Software Foundation License; upstream release and dependency lock to be pinned | commercial use ordinarily permitted subject to license notices; stdlib algorithms no cloud cost | **ALLOW** subject to release notice audit |
| Pydantic v2 | A candidate `2.14.4`; https://github.com/pydantic/pydantic | MIT; repository `LICENSE`; `pydantic-core` and dependencies need packaged lock/SBOM [S17] | commercial modification/use allowed; include MIT notice when distributing | **REUSE from A**, no duplicate model package |
| ESP-IDF metadata/header | reference `v5.5.6`; https://github.com/espressif/esp-idf | root Apache-2.0, *third-party components may differ* [S12] | commercial use and modified Apache code distribution subject to notices/license/patent terms; embedded SDK not required in SaaS core | **SOURCE CROSS-CHECK**; specific header audit if copying |
| Espressif board/module docs | guide latest revision [S01]; WROOM-32E v2.1 [S06] | publicly readable manufacturer material; permission for wholesale content/artwork redistribution **not verified** | citations/source URLs and independently expressed factual assertions; no blind PDF/image bundling | **LINK/FACT-ONLY**, rights of copied assets `LICENSE_UNVERIFIED` |
| Adafruit retail/guide | Product ID 3942; [S07] | publicly readable, no blanket license for all product images/text or OEM hardware data verified | use own short facts + source links; retailer does not confer OEM rights | **LINK/FACT-ONLY**, asset redistribution not admitted |
| Zephyr devicetree | `main` inspected 2026-11-20; pin commit before any reuse [S09,S10] | repository Apache-2.0; file SPDX headers and exceptions [S10] | commercial reuse usually permitted with notice; no need to bundle OS; source pin/version and attribution required if copying | **OPTIONAL COMPARATOR**, exact snapshot/variant audit required |
| CMSIS-SVD schema | schema v1.3 family; [S11] | reference schema Apache-2.0; third-party vendor SVD files licensed separately | schema reusable under notices; vendor pack rights not inferred | **DEFER** |
| KiCad source / ERC | 10.x docs [S08] | majority GPLv3-or-later; exceptions [S13] | GPL permits commercial use; obligations principally on distribution of covered software/derivatives; ordinary SaaS-only use is not automatically GPL network source disclosure; avoid copying/bundling absent legal review | **NO native integration**; reference semantics only |
| Z3 | 4.15.6 [S15] | MIT [S15] | commercial use/bundling allowed with copyright/license notice; dependencies/build provenance review | **DEFER** |
| NetworkX / Hypothesis | A test-only proposed versions `3.7`/`6.170.17`; [S18] | NetworkX BSD-3-Clause; Hypothesis MPL-2.0; individual package notices | test/dev-only, no mandatory SaaS dependency, maintain lockfile | **REUSE A test infrastructure**, not production dependency |

**Legal gate MUST:** license ID + authoritative `LICENSE`/SPDX file; exact tag/commit and hash; commercial modification/distribution rights; notice/source/copyright obligations; dependencies/SBOM; binary bundling vs server use; trademarks/images/datasets separable; no account/quotas; last verified date. If unclear: `LICENSE_UNVERIFIED`; prohibited redistribution: `LICENSE_BLOCKED`. Do not conflate GPL source copying with learning from publicly documented ERC algorithms. This is an engineering rights review, **not legal advice**.

## 11. Independent acceptance test matrix

**Fixtures must include physical J2/J3 contact and mapping evidence.** Expected outcomes below are *per check*; `F` is a verified maker fact, `M` is a logic oracle and `SYN` labels invented devices. **No test has been executed.**

| ID | Input / check | Expected `status` + reason | Independent oracle and falsification purpose |
|---|---|---|---|
| B01 | `board:J2.5(GPIO34) → Trig`, requested output | `FAIL / OUTPUT_NOT_CAPABLE` | Espressif board guide and ESP-IDF output mask [S01,S03]; prevents false PASS |
| B02 | `board:J3.9(GPIO18) → Trig`, requested GPIO output physical possibility | `PASS / CAPABILITY_CONFIRMED` | board J3 table + SDK masks [S01–S03]; **not** active mode PASS |
| B03 | `board:J3.8(GPIO19) ← Echo`, requested GPIO input physical possibility | `PASS / CAPABILITY_CONFIRMED` | board J3 table + silicon docs [S01,S02]; **not** Echo voltage PASS |
| B04 | `board:J2.5(GPIO34) ← Echo`, requested GPIO input physical possibility | `PASS / CAPABILITY_CONFIRMED` | GPIO34 input-only means input permissible; reverse negative-control [S01,S02] |
| B05 | GPIO34, requested internal software pull-up | `FAIL / PULLUP_NOT_CAPABLE` (only when declared requirement) | vendor GPIO docs [S02]; no false all-input PASS |
| B06 | exact board flash `J3.19(CLK/GPIO6) → Trig` general application output | `FAIL / RESERVED_RESOURCE` **board-policy check** | board guide flash note [S01]; separate silicon vs board proof |
| B07 | GPIO0 used as output after startup; boot pull/timing absent | `INDETERMINATE / BOOT_STRAP_CONDITIONS_UNKNOWN` | boot docs [S14]; avoid automatic boot failure |
| B08 | GPIO18 output-capable; active firmware mode not provided | capability `PASS`, active state `INDETERMINATE / ACTIVE_CONFIG_UNKNOWN` | implication counterexample; no config invention |
| B09 | GPIO18, trusted observed `GPIO_MODE_INPUT` at time T, requirement `OUTPUT_ACTIVE_AT_T` | `FAIL / OBSERVED_CONFIG_MISMATCH` at time T | documented `gpio_get_io_config`/dump [S02]; snapshot only |
| B10 | two mutually exclusive output owners assigned to one pad in same active mode, exclusive constraint sourced | `FAIL / OUTPUT_OWNER_CONFLICT` | predicate negation, known exclusive resource; no double-owned output |
| B11 | same pad monitored as input while PWM output, dual-use supported by verified mode facts | **No blanket `FAIL`**; evaluation according to explicit sharing constraints | ESP-IDF dual-use example [S02]; catches naive uniqueness rule |
| B12 | exact `-32E` device identity missing, user supplies generic `ESP32 DevKit` | `NOT_EVALUATED / UNSUPPORTED_DEVICE` or unresolved identity error before check | catalog admission contract; no clone default |
| B13 | same scope two contradictory official claims, neither adjudicated | `INDETERMINATE / EVIDENCE_CONFLICT` | explicitly constructed conflict fixture (SYN) |
| B14 | mapping to unknown physical contact `J3.99` | CORE-001A typed error, **not** a GPIO verdict | Research A topology/identity invariants |
| B15 | same valid requirements, reversed input order / localized labels | identical canonical findings and finding digests | mathematical permutation/view invariance |
| B16 | GPIO19 input possible but Echo voltage not checked by B | capability `PASS`; electrical `NOT_EVALUATED / ELECTRICAL_CHECK_DELEGATED` | check partition; protects against global-safe PASS |
| B17 | GPIO18 `UART_TX` eligibility with unknown matrix/peripheral ownership | `INDETERMINATE / FUNCTION_OR_OWNER_CONTEXT_UNKNOWN` | partial constraints, no guessed peripheral availability |
| B18 | GPIO18 output in ACTIVE state, then SLEEP state unspecified | ACTIVE result preserved; SLEEP check `INDETERMINATE` | state-specific applicability; no context promotion |
| B19 — SYN MCU-X | board family X: `P0` output-capable; `P1` input-only; output request at `P1` | `FAIL / OUTPUT_NOT_CAPABLE`; `P0` physical check `PASS` | **Synthetic** manually defined independent data; same rules no `ESP32` references |
| B20 — SYN peripheral-Y | board family Y: pin `Q2` supports open-drain I2C only in `PERIPH_MODE`, not `GPIO_PP`; request I2C with `GPIO_MODE` | `FAIL / MODE_RESTRICTION`; unspecified mode `INDETERMINATE` | **Synthetic** finite-state predicate and mode domain; non-GPIO-specific |
| B21 — SYN dynamic ownership | MCU-X: `P0` is UART_TX during `S1`, GPIO_OUT during `S2`, requested UART_TX in S2 | `FAIL / CONFIG_MISMATCH` only when state/assignment sourced | **Synthetic** state scoped rules |
| B22 | shuffled claim order, same evidence digest, 100 repeated calls | byte-identical ordered finding payload | determinism/metamorphic oracle; *target*, no run claimed |
| B23 | missing source for input capability on admitted third-board terminal | `INDETERMINATE / CAPABILITY_UNKNOWN` | incomplete but admitted profile; not false PASS |
| B24 | requested analog noise waveform simulation | `NOT_EVALUATED / OUT_OF_SCOPE` | clear coverage boundary; no implied simulation |

**[R] Required metrics (not achieved):** `false_PASS=0` over closed golden set; `false_FAIL=0` over negative controls; all missing/unknown/unsupported cases correctly classified; exact reproducibility per frozen hash; full physical `TerminalRef` anchoring; no engine rules with hardcoded ESP32 GPIO numbers. These metrics prove *fixture-level consistency*, **not** universal hardware correctness. Test results must later include selected test runner commands, executed counts, failures, source/version hashes, and independent review.

**Independent-oracle discipline:** source facts hand-transcribed from cited vendor tables, not generated by the same verification function; synthetic counterexamples hand-derived from stated axioms; SDK bitmask and board docs can disagree and are correlated vendor sources, not statistically independent laboratory measurements. Optionally add mutation tests that deliberately flip `output_allowed`, omit `mode`, replace board digest and change requested direction.

## 12. Technical limitations and remedies

| Gap / risk | Why material | Remedy / state |
|---|---|---|
| Runtime mode changes after snapshot | firmware can reconfigure pad at any time | `observed_at`, build identity, repeat sampling only if product later supports live instrumentation; no timeless claim |
| Pinmux routes not fully captured by GPIO number | peripheral index, direction, IOMUX/RTC and driver ownership differ | profile per function+mode; start generic GPIO direction; `UNKNOWN` other peripheral mappings |
| Firmware static parsing insufficient | macros, conditionals, runtime calls, libraries, bootloader | source parsing may produce *declared* intent only; cannot certify active state |
| Reserved vs impossible confusion | flash pins may be silicon output-capable yet board unavailable | separate `PHYSICAL_CAPABILITY` and `BOARD_POLICY` results |
| Strapping pin overblocking | postboot GPIO reuse might be legal | mode/timing evidence; warning+indeterminate without startup context |
| Device/revision mismatch | ESP32-WROVER vs WROOM and clone pinouts differ | strict variant digest; no fuzzy auto-canonicalization |
| Source claim conflicts or license uncertainty | false safety + legal exposure | conflict register, adjudication; fact-only links and rights gate |
| Dual-purpose IO exception | incorrect exclusivity rule rejects valid use | per-signal direction/ownership and documented sharing behavior |
| Electrical unsafe despite GPIO PASS | logic thresholds, 5V Echo, output drive/load | separate electrical checker; never aggregate local `PASS` into safety |
| ESP-IDF/Zephyr upstream changes | source semantics and paths can evolve | pin release/commit; review diff and rerun golden suite |
| UI translation drift | Georgian wording could turn `INDETERMINATE` into safe | deterministic localization templates keyed by status/reason |
| Resource exhaustion/untrusted payload | oversized data, malformed IDs, pathological combinations | CORE-001A schema and size caps; limit rules and normalization; no arbitrary executable rule content |

## 13. Rejected alternatives

1. **“Just check KiCad ERC.”** Incorrect boundary: KiCad pin electrical type matrix does not know runtime pinmux, true hardware assembly or guaranteed voltage. It is not the accepted source of ESP32 truth. [S08]
2. **“Take all board pinout images from GitHub.”** Visual labels are neither authoritative source licenses nor unique board/revision facts. Could silently mis-map clones. [S01,S09]
3. **“Use only `GPIO_IS_VALID_OUTPUT_GPIO`.”** Silicon macro ignores DevKitC flash and board constraints, firmware state and electrical interface. [S01–S03]
4. **“Every pin supports only one function at all times.”** Too strict; ESP-IDF describes GPIO input monitoring during LEDC output. [S02]
5. **“Use Z3 now for better scientific credibility.”** Solver adds no new true facts and no first-fixture decision power; SMT only valuable with nontrivial global assignment obligations. [S15,S16]
6. **“Emulate ESP32 or integrate SPICE immediately.”** Different questions; incomplete models create apparent, not validated certainty. Research 02 already defers them.
7. **“Turn unknown into warning but still overall PASS.”** Unsafe result semantics, confuses lack of evidence with positive evidence.
8. **“Copy SDK/Zephyr/GPL project sources into proprietary backend without audit.”** Mis-scoped dependencies and rights. Prefer documented methods and independently authored profiles.

## 14. Unresolved decisions and evidence gaps

| ID | Missing fact / decision | Required evidence or owner | Consequence now |
|---|---|---|---|
| U-B01 | CORE-001A actual artifact names/fields/error conventions | completed CORE-001A implementation + exhaustive test report | **cannot freeze B integration signatures** |
| U-B02 | exact physical PCB sub-revision of sample DevKitC V4 | manufacturer board schematics + real unit inspection | board claims scoped to selected guide, not all units |
| U-B03 | Adafruit #3942 sensor OEM/PCB revision and guaranteed output-high/low specs | maker-grade documentation/measurement | cannot make unconditional electrical PASS |
| U-B04 | minimum `requested_function` enum for B MVP | architecture owner + Research 03 demo acceptance | avoid accidental peripheral-wide scope |
| U-B05 | exact pinmux table coverage for PWM/UART/I2C beyond GPIO direction | pinned ESP-IDF/TRM extraction review | support only proved functions, otherwise unknown |
| U-B06 | format of firmware active-state evidence and trust model | target agent instrumentation/security review | active state `INDETERMINATE` by default |
| U-B07 | whether source-backed extraction beats manual claims across families | measured second/third board review work | no automated ingestion dependency yet |
| U-B08 | Zephyr source commit & legal status of every reused file | pinned commit + SPDX/NOTICE audit | comparator only, not bundled data |
| U-B09 | error policy on partial invalid snapshot vs valid unsupported device | CORE-001A owner decision | proposed contract only |
| U-B10 | rule-set versioning canonical JSON bytes and finding hash profile | architecture owner following A canonical contract | cannot assert byte-stable public API until defined |
| U-B11 | commercial demand/value of first capability | Research 03 user studies/comparison, not this method research | no commercial GO |
| U-B12 | real device/firmware waveform performance | separate measured bench acceptance | no hardware-verified result |

## 15. Proposed CORE-001B implementation decision package — *not an implementation task*

**Decision recommendation:** **APPROVE DIRECTION, HOLD INTERFACE FREEZE.** Research supports independent GPIO capability constraints with source-backed fact profiles; it does **not** prove CORE-001A already exposes any proposed signatures. Architecture owner should review B as semantic contract, then reconcile against the actual A report before authorizing a frozen task.

**Candidate approved semantic scope if owner agrees:** (a) exact board contact mapping; (b) GPIO input/output capability; (c) flash-reserved board policy; (d) unknown firmware activity; (e) strapping context warning; (f) physical/board/mode result separation; (g) deterministic evidence-backed findings; (h) two synthetic non-ESP32 fixtures. Other peripherals, voltage, simulation, firmware runtime and interactive UX implementation are outside B.

**Admission checks before an eventual coding instruction:**

- A real `CORE-001A` completed report with actual schema/export/interface names, tests and example snapshot is inspected.
- `GPIO34`/`18`/`19`, flash and strapping facts are scoped to manufacturer source IDs, reviewed and digest-pinned.
- A bounded enum of initial supported functions and evidence requirements is approved; *no broad “all GPIO” claim*.
- Ingestion and unsupported-device policies match A without silently modifying its semantics.
- Open-source license decisions are recorded per exact copied/bundled artifact; no SDK, emulator or SMT requirement introduced without new proof.
- Independent negative controls B01–B24 are approved as the acceptance set; `PASS` cannot be elevated from one check to all checks.
- All unresolved engineering decisions return to the architecture owner. **Codex is not authorized by this document to choose models, dependencies, algorithms, next tasks or modify a repository.**

**GO gate (architecture):** owners approve source-backed typed predicates and mapped A adapter.  
**REVISE gate:** A implementation contradicts proposed field names/identity semantics or active firmware claims need narrower meaning.  
**NO-GO gate:** exact hardware identities and evidence cannot be validated; or product insists on global electrical/firmware safety PASS based on GPIO-only checks.

## 16. Primary sources, reviewed versions and verification dates

**Review date for all links: 2026-11-20.** *A link’s accessibility is not a runtime test and does not itself grant redistribution rights.* Versions shown are source review anchors, not verified installed environments.

| ID | Primary source / reviewed version | URL | Supports |
|---|---|---|---|
| S01 | Espressif ESP32-DevKitC V4 User Guide, official current documentation, inspected 2026-11-20 | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html | board identity, `-32E`, J2/J3 header mapping, flash warning, boot/USB power |
| S02 | ESP-IDF GPIO & RTC GPIO docs, **v5.5.6** | https://docs.espressif.com/projects/esp-idf/en/v5.5.6/esp32/api-reference/peripherals/gpio.html | GPIO restrictions, strapping list, matrix, `gpio_dump_io_configuration`, `gpio_get_io_config`, macro docs |
| S03 | ESP-IDF `soc_caps.h` **v5.5.6** | https://github.com/espressif/esp-idf/blob/v5.5.6/components/soc/esp32/include/soc/soc_caps.h | valid and output-capability masks, GPIO34–39 input-only |
| S04 | ESP-IDF GPIO driver header **v5.5.6** | https://github.com/espressif/esp-idf/blob/v5.5.6/components/esp_driver_gpio/include/driver/gpio.h | callable API declarations and types |
| S05 | ESP-IDF `gpio_sig_map.h` **v5.5.6** | https://github.com/espressif/esp-idf/blob/v5.5.6/components/soc/esp32/include/soc/gpio_sig_map.h | GPIO matrix peripheral signal IDs |
| S06 | Espressif ESP32-WROOM-32E/32UE Datasheet **v2.1** (HTML publication) | https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html | module-level pin definitions, boot and electrical data; not DevKitC PCB revision |
| S07 | Adafruit #3942 product + official Ultrasonic Sonar Distance Sensors pinouts | https://www.adafruit.com/product/3942 ; https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/pinouts | `Trig` accepts 3/5 V, `Echo` described 5V logic, retail origin; guaranteed OEM ranges absent |
| S08 | KiCad Schematic Editor **10.0** ERC documentation | https://docs.kicad.org/10.0/en/eeschema/eeschema.html | ERC pin-conflicts map / limits |
| S09 | Zephyr `esp32_devkitc_procpu.dts`, main inspected (must pin commit if actually reused) | https://github.com/zephyrproject-rtos/zephyr/blob/main/boards/espressif/esp32_devkitc/esp32_devkitc_procpu.dts | reserved ranges, pinctrl and software board description |
| S10 | Zephyr top-level license and licensing documentation | https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE ; https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/LICENSING.rst | Apache-2.0/individual-file exceptions |
| S11 | CMSIS-SVD schema official maintained group | https://github.com/Open-CMSIS-Pack/svd-spec/blob/main/schema/CMSIS-SVD.xsd ; https://github.com/cmsis-svd/svd-schema | ARM peripheral register schema; not board-level electrical truth; Apache-2.0 schema |
| S12 | ESP-IDF copyright/third-party notice **v5.5.6** | https://docs.espressif.com/projects/esp-idf/en/v5.5.6/esp32/COPYRIGHT.html ; https://docs.espressif.com/projects/esp-idf/en/v5.5.6/esp32/contribute/copyright-guide.html | Apache-2.0 and third-party exceptions |
| S13 | KiCad source-license README | https://github.com/KiCad/kicad-source-mirror/blob/master/LICENSE.README | majority GPLv3-or-later plus exceptions |
| S14 | Espressif esptool Boot Mode Selection and hardware guidelines | https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/boot-mode-selection.html ; https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/schematic-checklist.html | boot pin sampling and timing context |
| S15 | Z3 MIT license, releases including **4.15.6** | https://github.com/Z3Prover/z3/blob/master/LICENSE.txt ; https://github.com/Z3Prover/z3/releases | solver licensing and pinned candidate |
| S16 | de Moura & Bjørner, *Z3: An Efficient SMT Solver*, TACAS **2008**, DOI | https://doi.org/10.1007/978-3-540-78800-3_24 | scientific SMT method justification, not GPIO data |
| S17 | Pydantic upstream MIT license; Research A's candidate `2.14.4` | https://github.com/pydantic/pydantic/blob/main/LICENSE | baseline validation library; exact transitive lock still needs audit |
| S18 | NetworkX `connected_components` **3.7**; Hypothesis MPL-2.0 license | https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.connected_components.html ; https://github.com/HypothesisWorks/hypothesis/blob/master/LICENSE.txt | reuse A's test-only graph oracle/property testing |

### Internal research inputs — dependency traceability

- **RESEARCH 01 — Canonical Engineering Data Model:** thin semantic core; physical/logic/UI separation; `PASS / FAIL / INDETERMINATE / NOT_EVALUATED`, provenance and strict identity.
- **RESEARCH 02 — Computational Verification & Simulation Architecture:** V0–V6 boundary; deterministic rules before simulation; method-vs-model-vs-hardware evidence; uncertainty and no unsupported physical claims.
- **RESEARCH 03 — First Verifiable Engineering Capability & Demo Contract:** ESP32-DevKitC-32E + Adafruit #3942, `GPIO34` Trig negative-control, `GPIO18` Trig and `GPIO19` Echo; 5V Echo issue; sensor device information limits and conditional analysis only.
- **RESEARCH A — Executable Engineering Model & Connectivity Contract:** Pydantic-based typed snapshot candidate, physical `TerminalRef`, `SignalMapping`, source-backed catalog, deterministic BFS topology and independent UI geometry; **no verified implemented API**.

**Final research state:** `GO` for the **semantic/algorithmic direction**, `HOLD` for interface freeze and coding authorization, `UNVERIFIED` for runtime firmware, PCB revision and broad commercial value. No repository inspection, implementation, testing or benchmark was performed for this B report.
