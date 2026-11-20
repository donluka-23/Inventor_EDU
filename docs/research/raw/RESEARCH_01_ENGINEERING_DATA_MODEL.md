# RESEARCH 01 — Canonical Engineering Data Model

**დოკუმენტი:** `RESEARCH_01_ENGINEERING_DATA_MODEL.md`  
**პროექტი:** INVENTOR EDU — დამოუკიდებელი, Georgian-first საგანმანათლებლო ელექტრონიკის პლატფორმა  
**კვლევის თარიღი / წყაროების გადამოწმება:** 2026-11-20 (Asia/Tbilisi)  
**სტატუსი:** დამოუკიდებელი არქიტექტურული კვლევა; **არ არის დამტკიცებული დიზაინი**, კოდი ან განხორციელების გეგმა.  
**მეთოდი:** ინგლისურენოვანი პირველადი წყაროების შედარება, capability-based შეფასება და ექვსი სავალდებულო სცენარის წინააღმდეგ შემოწმება. `UNVERIFIED` აღნიშნავს საკითხს, რომლის დამადასტურებელი მასალა ვერ მოიძებნა ან ვერ შემოწმდა სრულად.

---

## 1. Executive decision summary

**მთავარი დასკვნა:** INVENTOR EDU-სთვის ერთი უნივერსალური, უშუალოდ ყველა გამოთვლასა და ვიზუალიზაციას მომცველი „კანონიკური ფორმატის“ არჩევა ტექნიკურად გაუმართლებელია. დასაცავია **მინიმალური კანონიკური სემანტიკური კონტრაქტი** — განსაზღვრული იდენტობები, მოწყობილობის რევიზიები, ტერმინალებს შორის რეალური ელექტრული კავშირები, პირობითი ტექნიკური მახასიათებლები, დასაბუთება და შედეგის მიკვლევადობა. ცალკე ინტერპრეტაციებად უნდა დარჩეს 2D ხედი, წესების შემოწმება და მომავალში SPICE/სხვა სიმულატორისთვის შექმნილი საანგარიშო წარმოდგენა.

მიგნებები:

1. **ტოპოლოგიური საფუძველი:** KiCad-ის schematic/netlist-ის სემანტიკა (მრავალტერმინალიანი net-ები, junction, label, hierarchical sheet, ERC) პრაქტიკულად გამოცდილი ორიენტირია. KiCad 10-ს აქვს alternate pin functions, თუმცა მისი ERC **არ იძლევა გარანტიას**, რომ GPIO კონკრეტულ კვებით/რეჟიმულ/სილიკონის რევიზიის პირობებში უსაფრთხოა [R1–R4].
2. **ბიბლიოთეკის საფუძველი:** LibrePCB-ს `symbol → component signal → device pad`, `package`, `part/MPN` და ვერსირებული ბიბლიოთეკის მკაფიო გამიჯვნა უფრო გამძლე კონცეპტუალური საფუძველია, ვიდრე ხატულასა და რეალურ მწარმოებლის ნაწილს შორის ერთ-ერთზე-ერთი კავშირი [R5–R9]. **ეს არის დასასესხებელი სემანტიკური პრინციპი და არა მისი GPL კოდის ავტომატური გამოყენების ნებართვა.**
3. **ფიზიკის საფუძველი:** SPICE/ngspice ადგენს ანალოგური წრედის ფიზიკურ პასუხს **მხოლოდ** საკმარისი კომპონენტური მოდელებისა და საწყისი/საზღვრული პირობების შემთხვევაში; netlist არ ნიშნავს სიმულაციას. ngspice 47 გამოცემულია 2026 წლის აგვისტოში [R10–R12].
4. **დამატებითი ფორმალიზმი:** QUDT 3.5.3 სასარგებლოა ერთეულებისა და სიდიდეების ნორმალიზებისთვის; IEC 61360 — კომპონენტის თვისებების განსაზღვრების პრინციპებისთვის; IBIS 8.0 — შესაბამისი I/O ბუფერების მოდელებისთვის. IP-XACT და SysML v2 პროექტის პირველადი wiring representation არ უნდა გახდეს; მათგან შეიძლება მხოლოდ კონკრეტული ინტერფეისებისა და მიკვლევადობის პრაქტიკის გადმოტანა [R13–R21].
5. **საბაზისო რისკი არის მონაცემები, არა ფორმატი.** მწარმოებლის exact board/module/chip-revision, პინების რეალური კავშირები, input thresholds, რეჟიმული დენები, რეალური breakout-ის შიდა pull-up-ები და მოდელების ლიცენზიები ხშირად არ არის სრულყოფილად სტრუქტურირებული. `unknown` უნდა დარჩეს `unknown`; ის არ უნდა გადაქცეულიყოს `safe`-ად.
6. **მომავალი 2D აღქმა:** ელექტრული პინისა და ეკრანზე მდებარე ვიზუალური anchor-ის იდენტობები განცალკევებულია, მაგრამ ერთმანეთთან მყარად დაკავშირებულია. ერთი ტექნიკური დარღვევა შეიძლება ერთდროულად მიემართოს კონკრეტულ ტერმინალს, net-ს, სადენსა და ინსტრუქციულ ახსნას.

**რეკომენდაცია:** აირჩეს *thin semantic core + explicit, versioned evidence + replaceable computation/view adapters*. პირდაპირ არ აიღოთ „canonical“ ფორმატად არც KiCad-ის `.kicad_sch`, არც LibrePCB-ის სრული პროექტი, არც SPICE netlist, არც RDF/OWL, არც IP-XACT ან SysML. ამის ნაცვლად ხელახლა გამოიყენეთ მათი გამოცდილი სემანტიკური განყოფები და უზრუნველყავით კონვერტირებადი საზღვარი. ეს **ახალი ელექტრონიკის სტანდარტის შექმნის რეკომენდაცია არ არის**.

**გადაწყვეტილების სიმტკიცე:** მაღალი — ფენების გამიჯვნა; საშუალო — მინიმალური კონტრაქტის ვარგისობა წარმოდგენილი ექვსი სცენარისთვის; დაბალი/UNVERIFIED — ყველა შესაძლო ESP32 clone-board-ისა და sensor breakout-ის მონაცემების სრული ხელმისაწვდომობა.

---

## 2. Capability requirements and traceability matrix

### 2.1 სავალდებულო ფენები

| ფენა | რა ფაქტს ფლობს | რა **არ** უნდა მიეწეროს |
|---|---|---|
| **Identity / catalog** | მწარმოებელი, MPN, board assembly/revision, module, SoC, მონაცემის რევიზია | სქემაში დადგმული ობიექტის უნიკალური იდენტობა |
| **Instance / composition** | კონკრეტულად რომელი ნაწილი დგას პროექტში, board-ის შიდა ნაწილები და გარეთ გამოტანილი header-ები | კატალოგის ზოგადი pinout |
| **Topology** | რეალური ტერმინალების ეკვივალენტობის კლასები — nets, junctions, intentional no-connects | ძაბვა, დენი ან „კავშირი უსაფრთხოა“ |
| **Characteristics** | ზომადი თვისება, `min/typ/max`, limit-ის სახეობა და პირობები | ყველა პირობაზე მოქმედი ერთი უნივერსალური რიცხვი |
| **Behavior** | წყაროს, რეზისტორის, ADC input-ის, ბუფერის, რეგულატორის და ა.შ. განტოლება/მოდელის რეფერენსი | solver-ის შესრულებული შედეგი |
| **Operating context** | mode, firmware/pinmux/configuration, კვების გზა, სიხშირე, ტემპერატურა, დატვირთვა | კონტექსტის გარეშე გარანტირებული შეუსაბამობა/თავსებადობა |
| **Constraint / rule** | შესამოწმებელი პირობა, ფარგლები, წინაპირობები, წყარო | მიღებული გაზომვა ან სიმულაცია |
| **Results / evidence** | pass/fail/indeterminate, გამოთვლის ვერსია, input snapshot, ზუსტი მიზეზი | უცვლელი რეალობის მტკიცება ყველა ახალ რევიზიაზე |
| **Visualization** | 2D ობიექტი, anchor, geometry, wire segment, არჩევანი/მონიშვნა | ელექტრული ჭეშმარიტების დამოუკიდებელი წყარო |

### 2.2 მოთხოვნიდან შემოწმებამდე

| ID | მოთხოვნა | არსებული სანდო სემანტიკური პრეცედენტი | აუცილებელი დამატება / acceptance criterion |
|---|---|---|---|
| R01 | Generic vs concrete part | LibrePCB component/device/part | exact MPN, maker, assembly revision ერთმნიშვნელოვნად იკითხება |
| R02 | Board vs module vs SoC | EDA hierarchical composition, Espressif manuals | exposed header → board trace/net → module terminal → chip pin mapping; არ აირიოს იდენტობები |
| R03 | Symbol pin vs physical pad/contact | LibrePCB 2-საფეხურიანი mapping | UI anchor არ არის physical contact; ვარიანტის შეცვლისას mapping არ ჩუმდება |
| R04 | GPIO mux/alternate roles | KiCad 10 alternate pins; vendor GPIO matrix | conditional capability: pin, chip, module, config, revision |
| R05 | Multiple pins on shared net | KiCad schematic/netlist | net N terminals, label/junction წესები; ვიზუალური crossing ≠ junction |
| R06 | Power rails, ground | KiCad power nets; SPICE reference node | supply source/path, independent grounds, regulator-current constraints |
| R07 | Absolute vs recommended limits | datasheet parameter tables | limit_kind, temperature/mode/supply conditions, source pointer |
| R08 | Signal role/direction | KiCad ERC pin types, IP-XACT port direction | open-drain/tri-state/conditional mode; fixed input/output არ იკმარებს |
| R09 | Timing and protocol | IBIS; protocol standards; optional behavioral solver | I²C/UART/SPI timing მხოლოდ metadata+analysis-ით; waveform evidence ცალკე |
| R10 | Passive network loading | SPICE/Ohm/Kirchhoff | DC/AC/temporal context, impedance/input model, tolerances |
| R11 | Operating modes | vendor datasheets, SysML state semantics | mode-dependent current, state transitions, activation conditions |
| R12 | Violations and uncertainty | KiCad ERC; engineering V&V | `PASS / FAIL / INDETERMINATE / NOT_EVALUATED`, cause IDs, evidence |
| R13 | Editable 2D cross-reference | KiCad UUID, LibrePCB references | persistent engineering IDs + independent view anchors; bidirectional lookup |
| R14 | Versioned/reproducible knowledge | LibrePCB project-local library snapshot | library record version/hash, source date, governing revision |
| R15 | Simulation interchange | SPICE netlist, IBIS; optional FMI | explicit model availability, pin-map, boundary conditions, output provenance |
| R16 | Data rights | official OSS/standards licenses | per-artifact legal provenance; no blind redistribution |

**მნიშვნელოვანი ზღვარი:** გამართული netlist-ის არსებობა ადასტურებს მხოლოდ კავშირების განსაზღვრულობას; ელექტრული ფუნქციონირება შემდეგი, დამოუკიდებელი შემოწმების საგანია [R2, R4, R10].

---

## 3. Comparison of established representations

### 3.1 წყაროების კლასიფიკაცია

- **Formal standards / specifications:** IEC 61360, IEEE 1685 IP-XACT, OMG SysML 2.0, IBIS 8.0, FMI 3.0.2, Modelica 3.7; QUDT — გამოქვეყნებული ონტოლოგიური specification, **არა IEC/IEEE ელექტრონიკის სტანდარტი**.
- **Proven open implementations / format conventions:** KiCad 10.x, LibrePCB 2.1.x, ngspice 47, CMSIS-SVD და vendor support files. ისინი ერთმანეთთან სრულად ურთიერთჩანაცვლებადი normative standards არ არიან.
- **Engineering theory / scientific foundations:** circuit graph/network equations, Ohm/Kirchhoff, nodal analysis, numerical simulation; SPICE-ის ისტორიული Berkeley ნაშრომები [R11–R12, R27].
- **ამ ანგარიშის არქიტექტურული წინადადება:** ID-ებით დაკავშირებული მცირე სემანტიკური კონტრაქტი, mode-aware parameters, evidence-backed checks და view mappings. ის **არცერთი ზემოთ მოცემული სტანდარტის ოფიციალური ქვესიმრავლე არ არის**.

### 3.2 შედარების ცხრილი

| მიდგომა / შემოწმებული ვერსია | ძლიერი მშობლიური შესაძლებლობა | დაუფარავი მოთხოვნა | შემოთავაზებული გამოყენება |
|---|---|---|---|
| **KiCad 10.0 / 10.0.8**, 2026 | S-expression schematic; UUID/sheet path; wire/junction/label/hierarchy; pin electrical type; ERC; alternate pin functions; netlist/BOM; ngspice front-end [R1–R4] | PCB/სქემის გრაფი ≠ voltage-rating database; პინის სახელის შეცვლა ≠ mode-specific verified logic levels | topology/ERC-ის ფორმალური საორიენტაციო მოდელი, შესაძლო იმპორტ/ექსპორტ-ადაპტერი |
| **LibrePCB 2.1.1**, 2026 | symbol, generic component signal, device-pad mapping, package/footprint, manufacturer part; UUID; project-contained, version-stable libraries [R5–R9] | სრულფასოვანი pin-mux ელექტრული წესები და ანალოგური solver არ გამომდინარეობს library მოდელიდან | reference semantics for reusable parts, concrete device & board identity |
| **SPICE/ngspice 47**, 2026 | net/node, element terminal order, subcircuits, controlled sources, DC/transient/AC numerical analysis; nonlinear models [R10–R12] | maker identity, board revision, GPIO firmware, editable 2D semantics, რეალური მოდელის გარანტია | **მხოლოდ** simulation target და behavior model reference |
| **IBIS 8.0**, 2025 | vendor I/O buffer, package/driver/receiver characteristics და signal-integrity-oriented მოდელები [R22] | board-level wiring library, firmware/pinmux truth, universal low-frequency power modeling | კონკრეტული buffer evidence; no blanket availability assumption |
| **IEC 61360-1:2017 / -2:2012** (corrected 2025) და CDD | კლასებისა და properties/attributes-ის განსაზღვრის ზოგადი ფორმალიზმი [R13–R14] | wiring nets, executable physical behavior, free-to-redistribute full database | თვისების სახელების/მნიშვნელობების დისციპლინა, reference IDs მხოლოდ უფლებების ფარგლებში |
| **QUDT 3.5.3**, 2026-10-20 | quantity kind, unit, dimension, conversions/OWL/SHACL [R15] | device, pin, net, electrical safety & simulation | შესაბამისი სიდიდეების/ერთეულების reference vocabulary; სრული RDF graph **არაა აუცილებელი** |
| **IEEE 1685-2022 IP-XACT** | IP components, port/bus interfaces, register/memory maps, views, connections; schemas, semantic consistency rules [R17–R18] | breadboard hardware/physical voltage drops/consumer sensors; SoC IP metadata ≠ breakout physical pinout | მხოლოდ boundary-ებსა და registers-ის შემდგომი ინტეგრაციისთვის |
| **OMG SysML v2.0**, 2025 | system relationships, requirements, parts, constraints, semantics, API/interoperability [R19–R20] | out-of-box elementary EDA pinout/electrical property catalog და SPICE-სთან პირდაპირი ერთგულება | შეიძლება მოგვიანებით requirement traceability; **არა** native 2D wiring core |
| **CMSIS-SVD** (საჯარო specification) | MCU memory-mapped peripherals, registers, fields [R23] | physical header nets, thresholds, power, ზოგადი ESP32 chip pinout | optional firmware/register metadata (არც უნივერსალური MCU მხარდაჭერა) |
| **Modelica 3.7 / FMI 3.0.2** | equation-based multi-domain behavior / model exchange, co-simulation [R24–R25] | კომპონენტის MPN/board header catalog, beginner-oriented topology | მხოლოდ მომავალი სიმულატორის შესაძლო interface; **არა** პირველადი მონაცემთა საცავი |

**შენიშვნა KiCad-ზე:** მისი native schematic ხშირად ინახავს გრაფიკულ განლაგებასაც; კვლევისთვის სასარგებლოა UUID-ებისა და კავშირების მაგალითი, მაგრამ სქემის 2D coordinate-ები **არ უნდა გამოცხადდეს** INVENTOR EDU-ის ფიზიკური ტერმინალის იდენტობად. 10.0 documentation-ში არის alternate pin names/electrical types, თუმცა ეს არაა ნებისმიერი firmware-ის ავტომატური დადასტურება [R2–R3].

**შენიშვნა LibrePCB-ზე:** Device არ უნდა გავაიგივოთ სავალდებულოდ ერთ MPN-თან: შეიძლება ერთი device/pinout რამდენიმე manufacturer part-ს უკავშირდებოდეს. `part`/MPN, `device`, `package` და `component` განსხვავებული იდენტობის დონეებია [R5–R8].

### 3.3 ჩამოყალიბებული, მართლაც გადასატანი semantic patterns

1. **Type ≠ occurrence:** ბიბლიოთეკის კომპონენტის განმარტება არ არის პროექტში განთავსებული კონკრეტული instance.
2. **Functional signal ≠ package pad ≠ drawn pin ≠ board header:** Explicit mappings შუაში; არ დაეყრდნოთ თანხვედრილ string-სახელებს.
3. **Net = ეკვივალენტური ელექტრული node:** ერთი net შეიძლება შეიცავდეს მრავალ ტერმინალს. Bus/group არის ჯგუფი და არა ერთი ავტომატურად მოკლედ ჩართული net.
4. **Contextual property:** `3.3 V typical` არ ნიშნავს `3.3 V absolute maximum`; ყოველი ფაქტი დაკავშირებულია მოქმედების პირობებთან.
5. **Version-immutable binding:** კონკრეტული პროექტი უკავშირდება კონკრეტული წყაროს *snapshot*-ს; სახელით auto-upgrade აკრძალულია ელექტრული მნიშვნელობების შეცვლისას.
6. **Model vs observation:** datasheet, calculated result, simulated result და measured result ცალ-ცალკე evidentiary classes-ია.
7. **View-model separation:** UI-ს გადიდება, გადაწევა, სხვა layout ან Georgian translation ვერ ცვლის ელექტრულ ჭეშმარიტებას.

---

## 4. Mandatory engineering test cases — A–F

### 4.1 შეფასების კოდები

- **N** — ძირითადი სტრუქტურა/წესი მოცემული სისტემის native მოდელში არსებობს; *არ ნიშნავს სცენარის ბოლომდე გადაწყვეტას*.
- **M** — მოითხოვს დამატებით, ზუსტად განსაზღვრულ metadata-ს და ამ metadata-ზე შემოწმების ლოგიკას.
- **B** — ფიზიკური/რეჟიმული შედეგისთვის საჭიროა ადეკვატური **behavioral model + computation**, ზოგჯერ დროითი solver.
- **U** — კონკრეტული მოთხოვნა სისტემის პირდაპირი მოდელის მიღმაა; მასზე დაყრდნობა დამოუკიდებლად დაუშვებელია.

უჯრედში `N+M`, `M+B` ან `N+M+B` ნიშნავს სხვადასხვა აუცილებელ პასუხისმგებლობას — არა ავტომატურად დადასტურებულ სრულ ფუნქციონირებას. „native“ ეხება **მხოლოდ შესაბამის ხელსაწყოს მიმდინარე ფუნქციას**, არა INVENTOR EDU-ში ამ ფუნქციის უკვე არსებობას.

| მოდელი | A: საერთო კვება/GND | B: GPIO + revision | C: 5V→3.3V | D: loaded divider | E: mode-dependent | F: violation→2D |
|---|---|---|---|---|---|---|
| **KiCad 10** | **N+M** | **N+M** | **M** | **N+B** | **M+B** | **N+M** |
| **LibrePCB 2.1** | **N+M** | **M** | **M** | **M+B** | **M+B** | **N+M** |
| **SPICE/ngspice 47** | **N+B** | **U/M+B** | **M+B** | **N+B** | **M+B** | **U/M** |
| **IBIS 8.0** | **U** | **U/M** | **M+B** | **U/M+B** | **M+B** | **U** |
| **IEC 61360 / QUDT** | **M** | **M** | **M** | **M** | **M** | **U** |
| **IP-XACT 1685-2022** | **U/M** | **M** | **M** | **U/M** | **M** | **U/M** |
| **SysML v2** | **M** | **M** | **M** | **M+B** | **M+B** | **M** |
| **Modelica/FMI** | **M+B** | **U/M+B** | **M+B** | **N+B** | **N+B** | **U/M** |

ეს არის **capability assessment**, არა ავტომატური interoperability-ის ანგარიში. მაგალითად „SPICE, D: N+B“ ნიშნავს, რომ წრედის ელემენტების ქსელის და პასუხის გამოთვლის მექანიზმი აქვს, მაგრამ რეალური ESP32 ADC-ის კონკრეტული input model მის ბიბლიოთეკაში **UNVERIFIED** რჩება.

### A. ESP32 development board + რამდენიმე sensor + საერთო power/GND

**საცდელი ობიექტი:** ESP32-DevKitC V4, ორი/სამი დაბალი ძაბვის sensor breakout, ერთი 3V3 net, საერთო GND net; ზოგი sensor დამატებით SDA/SCL ან GPIO-სთანაა მიერთებული. დაფის ზუსტი module variant წინასწარ დასახელდება. Espressif-ის ოფიციალური DevKitC V4 დოკუმენტი ასხვავებს 5V/GND, 3V3/GND და USB კვების ალტერნატიულ გზებს, თან აფრთხილებს, რომ ერთდროულად არ გამოიყენონ [R26].

- **Native:** KiCad/LibrePCB-ს შეუძლიათ მრავალ ტერმინალის ერთ net-ზე მიბმა, ცალკე GND-სა და 3V3-ს დანიშვნა, არაერთი signal-ის დაკავშირება; EDA hierarchy გამოდგება board-internal wiring-ის აღწერისთვის.
- **Metadata:** საჭიროა `board_rev`, კონკრეტული module, header→module map, board-ის regulator/diodes/internal pull-ups, კომპონენტების მიწოდების დასაშვები დიაპაზონები, shared-rail semantics, რომელ power path-ზეა board ჩართული, sensor breakout-ის revision. ერთნაირი „GND“ წარწერები ყოველთვის ვერ ამტკიცებს გალვანურ საერთო კვანძს, თუ სხვადასხვა იზოლირებულ domain-ს ეხება.
- **Behavior/computation:** საერთო რეილის დენის ბიუჯეტი მხოლოდ შესაბამის mode/profile-სა და regulator-ის შესაძლებლობაზე დაყრდნობით ითვლება; voltage droop/startup/inrush/USB current limiter — power-network მოდელის/გაზომვის საქმეა.
- **Unsupported:** „ყველა sensor მუშაობს“ მხოლოდ ტოპოლოგიის ან საერთო მიწის გამო არ დასტურდება. I²C-ს შეიძლება address collision, pull-up voltage და rise-time პრობლემები ჰქონდეს.

**სწორი შედეგი:** `TOPOLOGY_VALID`, ხოლო `POWER_BUDGET=INDETERMINATE` სანამ ზუსტი load/profile/regulator არ მოიძებნება; ან კონკრეტული წყაროთი დადასტურებული `FAIL`.

### B. GPIO function და ელექტრული ლიმიტი კონკრეტულ board/chip revision-ზე

- **Native:** KiCad 10-ს alternate pin function-ის სახელის და electrical pin type-ის მითითება შეუძლია; LibrePCB-ის მოწყობილობის mapping-ში კონკრეტული pad შეიძლება დაფიქსირდეს; vendor-ის GPIO matrix დოკუმენტურად არსებობს [R3, R28].
- **Metadata:** board revision, fitted module/SoC, silicon revision, reserved flash/PSRAM pins, strap/boot restrictions, input-only pins, selected firmware/pinmux mode. Espressif-ის ცნობით **GPIO34–GPIO39 input-only**-ა და software pull-up/down არ აქვს; DevKitC V4-ზე ადრეული დაფების **C15** GPIO0-ის boot/clock ფუნქციას ცვლის; ზოგიერთ module variant-ში GPIO16/17-ის ხელმისაწვდომობა განსხვავდება [R26, R28–R29]. ეს განსხვავებები ერთ განზოგადებულ „ESP32 GPIO table“-ში არ უნდა დაიკარგოს.
- **Behavior:** თუ ამოცანა pulse timing, current sourcing ან analog input-ია, საჭირო შეიძლება გახდეს signal waveform/load/input model. Firmware-ის მიმდინარე კონფიგურაცია მხოლოდ ვიზუალური wiring-დან ვერ გამოიცნობა.
- **Unsupported:** კონკრეტული chip revision-ის ყოველ განსხვავებაზე ავტომატური დასკვნა **UNVERIFIED**, სანამ შესაბამის errata/PCN/board schematic არ უკავშირდება. „KiCad has alternate names“ ≠ „KiCad checks actual runtime mux“.

**სწორი შედეგი:** როცა output ფუნქციას ანიჭებენ GPIO34-ს, ფუნქციურ წესზე `FAIL` ზუსტი SoC/mode-ის დადასტურების შემდეგ; უცნობ board revision-ზე შესაბამისი board-specific საკითხი `INDETERMINATE`.

### C. შესაძლო 5 V → 3.3 V ლოგიკური შეუთავსებლობა

- **Native:** net connectivity/Electrical Rule Checker აღმოაჩენს ზოგიერთი ტიპის output-to-output conflict-ს, **არა** ავტომატურად ძაბვის ყველა შეუთავსებლობას.
- **Metadata:** source pin-ის რეალური `VOH/VOL`, push-pull/open-drain, supply domain, receiver-ის `VIH/VIL` და დასაშვები pin voltage შესაბამისი რეჟიმის/ტემპერატურისთვის; 5 V rail-ის არსებობა **არ ნიშნავს**, რომ ყველა ამ რეილზე მყოფი კომპონენტი 5 V logic-high-ს გამოიტანს.
- **Behavior:** pull-up, series resistor, ESD diode/clamp, input leakage ან level-shifter-ის არსებობისას მხოლოდ სახელობითი ძაბვების შედარება შეიძლება არასაკმარისი იყოს; შესაბამისი load/transient მოდელია საჭირო.
- **Unsupported:** ESP32-ის კონკრეტული GPIO-ს `5V-tolerant`-ად გამოცხადება შესაბამისი მწარმოებლის დასტურის გარეშე დაუშვებელია. ESP32 datasheet-ის **power-supply absolute maximum 3.6 V** ცხრილი პირდაპირ GPIO input-ის ცალკე absolute maximum მნიშვნელობად **არ უნდა გადაიწეროს** [R27].

**სწორი შედეგი:** `FAIL` თუ გამომავალი **დადასტურებულად** აჭარბებს მიმღების დადასტურებულ დასაშვებ ზღვარს შესაბამის პირობებში; სხვაგვარად `POTENTIAL_RISK/INDETERMINATE` და ხილული missing fact-ები. უსაფრთხოება არ დასტურდება `nominal 3.3 V`-ით.

### D. რეზისტიული გამყოფი და receiving pin-ის დატვირთვა

**განზრახ ხელოვნური საცდელი მონაცემები (არა რომელიმე რეალური ESP32 GPIO-ს ფაქტობრივი input resistance):** 5.00 V იდეალური DC წყარო; `Rtop=10 kΩ`, `Rbottom=20 kΩ`; მიმღების `Rin=100 kΩ` ground-სკენ პარალელურად.

- **Native:** SPICE-ს აქვს ორი/სამი resistor-ისა და voltage source-ის ზუსტი circuit topology და DC operating-point calculation. KiCad-ის simulator-ს შეუძლია ngspice გამოიყენოს, **თუ შესაბამისი models დანიშნულია** [R4, R10].
- **Metadata:** მნიშვნელობები, tolerance, წყაროს nominal/min/max, receiver-ის `Rin`/leakage, input capacitance, ADC acquisition time, pin mode და დაცვის აბსოლუტური ზღვარი.
- **Behavior/computation:** **unloaded:** `Vout = 5 × 20/(10+20) = 3.333... V`. **loaded:** `20 kΩ || 100 kΩ = 16.667 kΩ`; `Vout = 5 × 16.667/(10+16.667) = 3.125 V`. წყაროს Thevenin resistance დაუტვირთავ შემთხვევაში `10 kΩ || 20 kΩ ≈ 6.667 kΩ`. Time-dependent ADC sample/hold-სა და transient-ზე მხოლოდ DC ფორმულა არ კმარა.
- **Unsupported:** „გამყოფი უსაფრთხოა“ არ გამომდინარეობს ნომინალური 3.125/3.333 V-დან, თუ resistor/source tolerances, startup და ADC input limits უცნობია. SPICE-ის generic resistor network **არ ნიშნავს**, რომ ESP32-ის ზუსტი ADC ფიზიკური მოდელი ხელმისაწვდომია. Espressif თავად განიხილავს ADC input-ის გამოყენებასა და divider-ს, ამიტომ ეს სპეციფიკური გამოყენების დადასტურებას საჭიროებს [R30].

**სწორი შედეგი:** ზემოთ მოცემულ *გამჭვირვალე* საცდელ პირობებში numerical result; რეალური ESP32-ის უსაფრთხოებაზე — `INDETERMINATE`, სანამ datasheet input bounds და სრული variation profile არ გამოიკვლევა.

### E. რეჟიმის მიხედვით შეცვლილი ელექტრული მახასიათებლები

- **Native:** ჩვეულებრივი KiCad/LibrePCB pin role ამ ცვლილებას ავტომატურად ვერ აღწერს; vendor datasheet-ს ხშირად აქვს sleep/active/RF current profiles. SysML-ით მდგომარეობისა და constraint-ის აღწერა შეიძლება, ხოლო SPICE/Modelica-ით შესაბამისი ცვალებადი წყაროს სიმულაცია შესაძლებელი ხდება.
- **Metadata:** რეჟიმის სახელები და ტრანზიციები; `active`, `sleep`, `wake`, `boot`, firmware-dependent driver mode; quantity + condition; თითოეული რეჟიმის `typ/max` და datasheet revision.
- **Behavior:** startup current peak, transient, mode transition timing და დროითი ენერგიის მოხმარება **behavioral model**-ს ან გაზომვას მოითხოვს; mode-ის დადგენა შესაბამის ექსპერიმენტში ნათლად უნდა ითქვას.
- **Unsupported:** რომელიმე datasheet-ის ერთ `typical current`-ზე მთელი power budget-ის `PASS` არასწორია. მოყვანილი დენის რიცხვები აქ განზრახ არ არის წარმოდგენილი — შესაბამისი ზუსტი part/revision/mode წინასწარ არ დაფიქსირებულა.

**სწორი შედეგი:** `SLEEP_ONLY_PASS` არ უნდა გადაიზარდოს `ALL_MODES_PASS`-ში; თუ კვების წყაროს capacity აქტიურ რეჟიმზე უცნობია, პასუხი `INDETERMINATE`.

### F. detected violation-ის პირდაპირი 2D mapping

- **Native:** KiCad schematic objects, pins, wires, junctions და ERC markers ინახავენ ობიექტის იდენტობებს/ლოკაციებს; LibrePCB ასევე მართავს reference IDs/UUID-ებს [R2, R9].
- **Metadata:** მინიმუმ violation→engineered instance/terminal/net/rule→view element/anchor mapping; view may be a **breadboard/board face**, არა მხოლოდ EDA symbol. ერთი ფიზიკური ტერმინალი შესაძლოა რამდენიმე ხედში გამოჩნდეს.
- **Behavior:** fault-ის გამოანგარიშება, თუ ის electrical-domain შედეგია, UI-გან დამოუკიდებელია; UI მხოლოდ მიზეზს აჩვენებს.
- **Unsupported:** raw SPICE node name, 2D pixel coordinate, symbol label ან line crossing თავისთავად სტაბილური semantic identity ვერ გახდება; `ERROR`-ის შემთხვევითი გეომეტრიის შეღებვა არ არის causal explanation.

**სწორი შედეგი:** შეცდომა მიუთითებს კონკრეტულ GPIO/terminal-ს, ამავე net-ის შესაბამის სეგმენტებს და დამადასტურებელ წესს; სხვა zoom, translation, drag, alternate graphic view და layout-ზე შედეგი არ იცვლება; შემოწმებისეული შეცდომა **არ უჩინარდება** უბრალოდ UI-ის გადაწყობით.

---

## 5. Data coverage, source provenance and governance

### 5.1 წყაროების ხარისხობრივი იერარქია

| კატეგორია | ტიპური ხელმისაწვდომი მონაცემი | ხშირი დანაკლისი / საფრთხე | შეფასება |
|---|---|---|---|
| **Manufacturer datasheet, errata, PCN, board schematics** | electrical limits, pin function, supply, conditions, revisions | ტექსტი/PDF არასტრუქტურირებულია; board revision და module SKU შეიძლება არ იყოს ზუსტი | **პირველადი ტექნიკური მტკიცებულება**, მაგრამ საჭიროა კონკრეტული გამოცემის binding |
| **Official KiCad symbols** | schematic pins, electrical types, footprints, datasheet links | არ იძლევა ყველა absolute limit-ს ან board-level hidden paths-ს | კარგია structural mapping-ზე; **არ არის safety certification** |
| **Official LibrePCB libraries** | symbol/component/device/package/part identity, pad mapping | pin function mode, calibrated current/thresholds ხშირად ვერ მოიძებნება | კარგია reusable catalog-ზე; არა complete physics dataset |
| **Vendor firmware support (ESP-IDF, SVD, packs)** | mux/peripheral capabilities, register semantics, target-specific configuration | board-specific analog limit/power paths ვერ დასტურდება მხოლოდ software headers-ით | conditional second-source; უნდა შეესაბამებოდეს chip & SDK version-ს [R23, R29, R31] |
| **Vendor SPICE/IBIS** | transistor/buffer/analog response under defined model assumptions | მოდელი შეიძლება არასრული, დაშიფრული, კონკრეტულ EDA-სთან მიბმული ან არარედისტრიბუცირებადი იყოს | გამოიყენება **მხოლოდ** exact-device+license+validation linkage-ით |
| **Third-party crowd libraries/marketplaces** | symbol, footprint, nominal part fields | provenance, revision mismatch, license, verified electrical characteristics | `UNVERIFIED`; ავტომატური safety rule source არ ხდება |
| **User-entered facts** | selected exact board, operating mode, missing loads | თვითდეკლარირებული მონაცემი შეიძლება მცდარი იყოს | `USER_ASSERTED`, არა manufacturer-verified |
| **Measurement / calibration** | რეალური ობიექტის პასუხი განსაზღვრულ პირობებში | instrument calibration, setup, noise, sample size | `MEASURED`, explicit uncertainty/conditions required |

**დადასტურებული მაგალითი:** Espressif-ის ESP32 DevKitC V4-ის დოკუმენტაცია ცალკე ასახელებს board-ის კვების გზებს, header pin-ებს, C15-ის ადრეულ რევიზიულ ეფექტს; ESP32 Series Datasheet v5.3-ში არის electrical tables, GPIO matrix და revision metadata [R26–R29]. ეს *სხვადასხვა წყაროს ერთობლივი საჭიროების* პირდაპირი მტკიცებულებაა.

**UNVERIFIED (coverage):** საჯარო ღია კომპონენტურ ბიბლიოთეკაში ყველა გავრცელებული HC-SR04/DHT22/BH1750/სხვა breakout-ის ყველა კლონის **ზუსტი სქემა, რეალური pull-up ღირებულება და მიკროსქემის რევიზია** დადასტურებული არ არის. ერთი sensor chip-ის datasheet არ ამტკიცებს ნებისმიერი ამავე სახელწოდების breakout-ის გარეთა პინების ელექტრულ ქცევას.

### 5.2 მინიმალური provenance record — სემანტიკური მოთხოვნა, არა schema

ნებისმიერი safety-relevant ფაქტისთვის უნდა იკითხებოდეს: **(ა)** ვის ეხება — manufacturer, exact MPN/board SKU/module/chip/revision; **(ბ)** წყარო — publisher, სრული URL/DOI, document title/version/date, section/table/page; **(გ)** რა claim-ია — value, unit, quantity kind, `min/typ/max`, `absolute/recommended/characterized`, tolerance; **(დ)** რა პირობებით — supply, temp, load, mode, timing, firmware; **(ე)** მიღების ფორმა — original/manual transcription/machine extraction/derived estimate; **(ვ)** confidence, verification date და human-review status; **(ზ)** license/redistribution rights; **(თ)** checksum ან უცვლელი ვერსიის იდენტიფიკატორი; **(ი)** contradiction/superseded-by links.

*კონფლიქტის მაგალითი:* ბიბლიოთეკა GPIO-ს „I/O“-ს უწოდებს, ხოლო მწარმოებლის datasheet კონკრეტულ variant-ზე `input-only`-ს. აბსტრაქტული generic role ვერ გადაწერს უფრო სპეციფიკურ მტკიცებულებას; დაფიქსირდეს `CONFLICT`, შესაბამისი scopes და source priority. რეალურ გამოყენებას წყვეტს **სკოპისა და მტკიცებულების სისწორის** ექსპერტული შეფასება, არა მხოლოდ წყაროს რანგი.

### 5.3 დამოწმებადი პროდუქტის snapshot

ერთ კონკრეტულ ექსპერიმენტს უნდა ჰქონდეს immutable კომპონენტების ვერსიები, selected assembly, connection graph, selected modes/configuration, rule version, model version, analysis settings, source set და result hash. ახალი datasheet ან შეცვლილი library element არ ცვლის ძველი შედეგის მნიშვნელობას ჩუმად; ახალი შეფასება ახალ provenance record-ს ქმნის. LibrePCB-ს self-contained project library და UUID/breaking-change დისციპლინა ამ პრინციპის პრაქტიკული პრეცედენტია [R8–R9].

---

## 6. Representation limits and established technical remedies

| შეზღუდვა | რატომ ვერ გადაიჭრება მხოლოდ data representation-ით | დამკვიდრებული საშუალება და აუცილებელი წინაპირობა |
|---|---|---|
| GPIO driving/input voltage | კავშირის გრაფიდან ძაბვა არ გამომდინარეობს | bounded voltage compatibility check თუ worst-case datasheet limits ცნობილია; სხვა შემთხვევაში circuit/buffer simulation |
| Voltage divider loading | მხოლოდ კავშირი ვერ განსაზღვრავს input impedance-სა და tolerance-ს | Ohm/Kirchhoff + Thevenin; ngspice DC/transient, როცა input model არსებობს |
| Shared power supply sufficiency | wake-up/inrush/mode peaks და regulator dropout დროითია | profile-based arithmetic, power transient model, measured load traces |
| I²C/SPI/UART timing | bus name არ ამტკიცებს protocol compliance-ს | electrical pull-up/capacitance, timing thresholds, configuration, waveforms; NXP I²C-ის ზღვრული პარამეტრები შესაბამისი მაგალითია [R32] |
| MCU pinmux collision | native pin aliases არ იძლევა მთელი firmware-ის runtime state-ს | SoC-specific resource constraints + firmware config evidence; თუ unknown — indeterminate |
| Analog ADC accuracy | sampling capacitor, source impedance, attenuation/calibration და noise | ADC vendor model/characterization; laboratory measurement [R30] |
| Component part substitutions | სახელის მსგავსება ან ერთი package ვერ ამტკიცებს ელექტრულ equivalence-ს | exact MPN/revision, datasheet-backed parameter compatibility |
| Aging, tolerance, damage | normal operating nominal ≠ physical state of particular specimen | worst-case/interval analysis, derating, empirical validation |
| Behavioral model credibility | მხოლოდ SPICE/IBIS file-ის არსებობა არ ნიშნავს, რომ კონკრეტული გამოყენებისას სწორი შედეგია | model validation domain, correlation with manufacturer test/measurement |
| UI-causal correctness | 2D highlight შეიძლება არასწორ net-ს ან terminal-ს ეხებოდეს | model-view invariants, graph-to-view cross-probing tests |
| Missing data | მონაცემის სქემა სიზუსტეს ვერ ქმნის | `INDETERMINATE`, explicit missing fields; source request / measured evidence |

**განვითარებული solver არ არის ამ კვლევის რეკომენდაცია.** ელემენტარული DC ამოცანა მათემატიკურად გადაწყვეტადია; მაღალი სიხშირის digital signal integrity ან GPIO-ს clamp/injection current სხვა მასშტაბისა და ხშირად არახელმისაწვდომი მოდელების ამოცანაა. SPICE-ის ისტორიული ნაშრომიც წრედს დიფერენციალურ/ალგებრულ მოდელად და არა უბრალოდ „მავთულების ვიზუალურ სიად“ განიხილავს [R11–R12].

---

## 7. Open-source licensing and commercial reuse

| აქტივი | დადასტურებული უფლებრივი მდგომარეობა | კონკრეტული დიზაინისთვის პრაქტიკული შედეგი |
|---|---|---|
| **KiCad application code** | პროგრამის ძირითადი კოდი GPLv3 or later [R33] | ფორმატისა და სემანტიკის შესწავლა ნებადართულია; წყაროს კოდის შერწყმა/დისტრიბუცია მოითხოვს კონკრეტული GPL ვალდებულებების განხილვას |
| **KiCad official symbol/footprint libraries** | CC BY-SA 4.0 სპეციალური exception-ით: ბიბლიოთეკით დიზაინის შექმნა თავისთავად არ ხდის დიზაინს BY-SA-დ [R34] | **exception არ არის blanket permission** modified library database-ის დახურული რედისტრიბუციისთვის; attribution/share-alike შემთხვევაზე იურიდიული შეფასება |
| **LibrePCB application code** | GPLv3 [R35] | კვლევა/გამოყენება ≠ საკუთარი დახურული კოდის GPL compliance-ის ავტომატური გამორიცხვა |
| **LibrePCB official libraries** | CC0-1.0 [R35] | დაბალი ლიცენზიური ბარიერი catalog/graphical reuse-ისთვის; ტექნიკური ჭეშმარიტება კვლავ დასამტკიცებელია; მესამე მხარის ფაილები ინდივიდუალურად მოწმდება |
| **ngspice code** | პროექტის მიხედვით ძირითადად modified/new BSD, *few exceptions* [R36] | კონკრეტული subcomponent, model და redistribution terms ცალ-ცალკე გადაამოწმეთ; SPICE models შეიძლება vendor-restricted იყოს |
| **QUDT ontology** | CC BY 4.0 [R15–R16] | reuse attribution-ით; license notice/changes record; quantity/unit semantics გამოყენებადია |
| **IEC standards/CDD** | copyrighted; უფასო access **არ ნიშნავს** CDD-ის მასობრივ კოპირებას ან კომერციულ რედისტრიბუციას [R13–R14, R37] | გამოიყენეთ public references და დამოუკიდებლად შექმნილი property semantics; სრული CDD replication მხოლოდ შესაბამისი უფლებებით |
| **IEEE IP-XACT standard/guide** | IEEE normative text და Accellera-ის guide ცალკე საავტორო წესების ქვეშაა; XML schema availability ≠ ყველა მასალის unrestricted copying [R17–R18] | conceptual semantics შეიძლება შეისწავლოთ; ინტეგრაციამდე გადაამოწმეთ schema/guide redistribution rights |
| **OMG SysML spec** | ოფიციალური specification საჯაროდაა, მაგრამ licensing of particular tool, generated artifacts და copyrighted text სხვადასხვა საკითხია [R19–R20] | არ გამოაცხადოთ თავისუფალი ნებისმიერი მასალის კოპირება მხოლოდ public spec-ის საფუძველზე |
| **IBIS specification vs vendor IBIS file** | public spec 8.0; კონკრეტული მწარმოებლის model file-ის გავრცელების უფლება **UNVERIFIED** სანამ მისი terms არ ჩანს [R22] | default-ად არ შეიტანოთ/გაავრცელოთ vendor models მომხმარებელთა პროექტებში ნებართვის გარეშე |
| **Modelica / FMI specification and model packages** | specification-ის საჯარო ხელმისაწვდომობა ≠ ნებისმიერი compiled FMU-ს ან model library-ის რედისტრიბუციის უფლება [R24–R25] | future interface interoperability შეფასდეს; თითოეული FMU/model library ცალკე |
| **Manufacturer PDFs/board schematics; marketplace models** | copyright/contract განსხვავდება გამომცემლით; bulk extraction/redistribution და AI ingestion შეიძლება შეზღუდული იყოს | reference/link + manually curated attributable facts; არ ივარაუდოთ unrestricted dataset creation |

**გაფრთხილება:** IEC-ის ოფიციალური Webstore terms მიუთითებს დამატებით შეზღუდვებს IEC პროდუქტის AI ტექნოლოგიებში გამოყენებასთან დაკავშირებით შესაბამისი ნებართვის გარეშე [R38]. აქ **არ არის დაკოპირებული ფასიანი ნორმატიული ტექსტი**: შეფასება ეყრდნობა საჯარო აღწერებს. სრული IEC 61360 ტექსტის შიდა ნორმატიული პუნქტები — **UNVERIFIED**. ეს იურიდიული დასკვნა არ არის.

---

## 8. Proposed **minimum canonical semantic contract**

ეს არის **აუცილებელი დომენური მნიშვნელობებისა და invariant-ების რეკომენდაცია** — განზრახ **არ** არის კლასების, JSON schema-ს, ORM-ის, storage engine-ის ან API-ის დიზაინი.

### 8.1 აუცილებელი semantic commitments

**C01 — immutable identity scope.** გაიმიჯნოს (i) generic definition, (ii) concrete device/part, (iii) assembled board/module, (iv) კონკრეტულ design-ში instance, (v) კონკრეტული view-ის graphical element. ერთნაირი label არ წარმოადგენს იდენტობას.

**C02 — hierarchical actual hardware mapping.** Board header contact განსხვავდება module pad-ისა და chip pin-ისგან. ცხადი და ვერსირებული კავშირები აღწერს მათ ფიზიკურ ურთიერთობას; boot resistor/regulator/USB-to-UART და internal rail არ დაიკარგოს „ESP32 board“ შავი ყუთის უკან, როცა მათი ცოდნა წესისთვის აუცილებელია.

**C03 — functional vs physical mapping.** Symbol pin, functional signal, selectable mux function და package pad ერთმანეთისგან დამოუკიდებელი ცნებებია; mapping შეიძლება განსხვავდებოდეს part/board revision-ით.

**C04 — electrical node semantics.** Net არის რეალური ტერმინალების დაკავშირებულობის კლასი. Multiple grounds, rail domains, labels, jumper positions და switch-state topologies არ ერთიანდება მხოლოდ მსგავსი სახელის გამო. Wire intersection არ ქმნის net-ს junction-ის გარეშე.

**C05 — contextual characteristics.** Electrical facts მოიცავს quantity kind, unit, numeric bound/range/tolerance, limit type (`absolute / recommended / characterized / typical`), scope და applicability predicate-ს — supply, mode, revision, temperature, load, timing.

**C06 — behavioral model isolation.** Passive/source/active element-ის behavior model დაკავშირებულია შესაბამის რევიზიასთან, pin order-სა და validity domain-თან; მისი არქონა არ ავსებს სავარაუდო „იდეალური“ მოდელით მომხმარებლის გაფრთხილების გარეშე.

**C07 — explicit operating context.** Configuration/firmware pinmux, supply method, operating mode, environment და measurement/simulation assumption არის კონტრაქტის შემადგენელი ნაწილი, როცა მის გარეშე შედეგი იცვლება.

**C08 — rule provenance.** ყოველი constraint უკავშირდება source claim-ს, rule semantics/version-ს, selected scope-სა და prerequisite data-ს; violation არ არის უბრალო natural-language ტექსტი.

**C09 — four-state judgment.** ნებისმიერი check აბრუნებს `PASS`, `FAIL`, `INDETERMINATE` ან `NOT_EVALUATED`; severity/educational message ამ სტატუსისგან განსხვავებული თვისებებია. `WARN` ვერ ჩაანაცვლებს უცნობობას.

**C10 — causality & uncertainty.** შედეგის ჩანაწერი შეიცავს affected engineering IDs, მოკლე განმარტების მიზეზს, selected facts/models, assumptions, model/data versions, input snapshot-ს, bounds/error/coverage-ს და გამოთვლის მეთოდის იდენტობას. `derived`, `simulated`, `measured`, `datasheet-claimed` არ აირიოს.

**C11 — presentation-independent anchors.** View links მიუთითებენ canonical instance+terminal+net IDs-ზე; pixel location/transforms მხოლოდ გამოსახულებაა. Invariant: layout edit არ ცვლის electrical connectivity-ს; wiring edit კი ცვლის relevant topology-ს და შესაძლოა verification result-ს.

**C12 — machine-readable analysis boundary.** მომავალ engine-ს მიეწოდება მხოლოდ იმ domain-ის net/terminals, parameters+units, conditions, model refs, required outputs და mapping back-to-source IDs, რომელიც ესმის. Engine პასუხი არის *result*, **არა** canonically rewritten source truth. Unsupported analysis იძლევა `NOT_EVALUATED`-ს ან `INDETERMINATE`-ს.

**C13 — versioned source immutability.** დაზიანების ან გამომცემლის ცვლილების გამოსწორება არ ახდენს ძველი project-ის silent reinterpretation-ს; მომდევნო მონაცემი ცალკე ვერსიასა და migration decision-ს მოითხოვს.

**C14 — minimal semantic scope.** პირველადი კონტრაქტი არ მოითხოვს owl reasoner-ს, SysML profile-ს, compiled SPICE/IBIS models-ს ან manufacturer-wide component ontology-ს. მათი შესაბამისი semantics ხელმისაწვდომი დარჩეს references/adapters-ით, *მხოლოდ საჭიროების დადასტურებისას*.

### 8.2 რატომ არის ეს მინიმალური და არა ახალი „electronics standard“

- **მსგავსება KiCad-თან:** აღებულია graph/net/pin/junction + UUID/reference principle, მაგრამ არ არის გამეორებული KiCad-ის სრული document syntax/PCB domain.
- **მსგავსება LibrePCB-თან:** აღებულია generic electrical interface-ის, physical package-ის, concrete part-ის და graphical symbol-ის გამიჯვნა, მაგრამ არ არის დაკოპირებული proprietary-to-LibrePCB file structure.
- **მსგავსება QUDT/IEC-თან:** აღებულია type/unit/property semantics; არ შექმნილა ახალი SI units taxonomy და არ ხდება copyrighted CDD-ის რეპუბლიკაცია.
- **მსგავსება SPICE/IBIS-თან:** მიღებულია model binding და node/terminal order-ის აუცილებლობა; არ კეთდება განცხადება, რომ ქართული სასწავლო პლატფორმა საკუთარ circuit solver-ს ფლობს.

**გადამწყვეტი საზღვარი:** „canonical“ უნდა ნიშნავს *ერთმნიშვნელოვან მნიშვნელობასა და source-of-truth-ს*, არა ერთ ფაილს ან ერთ უნივერსალურ მეტამოდელს, რომელსაც ყველა სამომავლო ძრავა პირდაპირ კითხულობს.

---

## 9. Alternative architectures and rejected approaches

| ალტერნატივა | რეალური უპირატესობა | რატომ არ არის ახლა რეკომენდებული | რა ფაქტმა შეიძლება შეცვალოს არჩევანი |
|---|---|---|---|
| **A1 — KiCad schematic as sole canonical** | proven ERC/netlist ecosystem; simpler standard exports | 2D board-face UI, actual board internals, mode-aware limits/uncertainty supplementary data-ში მაინც გადავა; native syntax/Electrical rules mismatch | თუ ძირითადი მოთხოვნა KiCad-ში სრულფასოვანი სქემის შექმნა/დაბრუნება გახდება |
| **A2 — LibrePCB entire project as sole canonical** | strong device/package/part identity, versioned local libraries | სრული PCB editing data model ძალზე ფართოა educational breadboard-ისთვის; current/voltage behavior დამატებითია; GPL code handling | თუ ძირითადი მიზანი LibrePCB PCB workflow interoperability გახდება |
| **A3 — SPICE netlist as sole canonical** | solver-ზე უშუალო გადასვლა | ვერ ასახავს MPN/revision, graphics, mux, full provenance; ბევრი sensor/MCU accurate model არ არის | თუ პროდუქტი მხოლოდ analog simulation tool გახდება |
| **A4 — OWL/QUDT/IEC mega-ontology** | semantic formalism, interoperability, reasoning | ontology does not supply missing parameters, equations, UI mapping, runtime context; costly curation; CDD rights | თუ multi-institution metadata exchange regulatory requirement დადასტურდება |
| **A5 — IP-XACT/SysML full canonical** | SoC/system abstraction, formal requirements | არასწორი domain center for beginner physical wiring; model/tooling overhead | თუ primary customer becomes SoC/MBSE enterprise and integration deliverable |
| **A6 — visuals-first wiring objects as source truth** | quickest initial rendering | wire overlap, SVG image, alias mistakes; unverifiable board mapping; unstable UI links | **უარყოფილია** safety-relevant educational product-ისთვის |
| **A7 — full custom proprietary electronics standard** | unconstrained expressivity | მრავალწლიანი standards burden; interoperability and correctness risk, needless invention | **უარყოფილია**; საჭიროების დადასტურება ჯერ არ არსებობს |
| **A8 — thin, versioned semantic core + adapters** | separates meaning, evidence, checks, solver/view; minimum cross-view IDs | explicit mapping discipline & model-coverage policy required | **რეკომენდებულია პირობითად**, ამ ანგარიშის ექსპერიმენტული gates-ის შემდეგ |

**უარყოფის საფუძველი** არის *requirement fit*, არა სტანდარტის ან პროგრამის პოპულარობა.

---

## 10. Assumptions, unresolved questions, confidence

### 10.1 დადასტურებული/სავარაუდო წანამძღვრები

| ID | მტკიცება / წინაპირობა | სტატუსი | სანდოობა |
|---|---|---|---|
| H1 | Topology, device identity, simulation, UI განსხვავებულ ინფორმაციას შეიცავს | დასაბუთებული EDA მოდელების შედარებით [R1–R12] | **High** |
| H2 | LibrePCB-ის library semantics სასარგებლოა board/device identity-სთვის | ოფიციალური დოკუმენტაცია [R5–R9] | **High** |
| H3 | KiCad 10 alternate pin modes ავტომატურად ამოწმებს MCU runtime mode-ს | **არ დასტურდება; არ არის მიღებული** | **Low / rejected assumption** |
| H4 | ngspice-ის არსებობა უზრუნველყოფს ნებისმიერ ESP32 sensor-ის physics simulation-ს | **არ დასტურდება; არ არის მიღებული** | **Low / rejected assumption** |
| H5 | ერთეულები/რიცხობრივი თვისებები შეიძლება QUDT reference-ებით გაიმიჯნოს | ოფიციალური QUDT specification [R15] | **High** |
| H6 | ყველა მოსალოდნელ breakout variant-ს აქვს verified machine-readable schematics/limits | **UNVERIFIED** | **Low** |
| H7 | 2D visual anchors reliable cross-probing-ს გაუძლებს | არქიტექტურული ჰიპოთეზა, ჯერ არა გამოცდილი INVENTOR EDU-ში | **Medium** |
| H8 | ძირითადი გამოყენება არის beginner wiring verification, არა PCB fabrication | მოცემული product scope, არა ბაზრის ან მომხმარებლის კვლევის შედეგი | **Medium** |
| H9 | curated facts-ის ლიცენზიური გამოყენება შეიძლება ყოველ შემთხვევაში | **UNVERIFIED** კონკრეტული vendor/marketplace-ის terms-ის გარეშე | **Low** |
| H10 | thin contract ექვსივე შემთხვევისთვის საკმარისია საწყის დონეზე | დადებითი სემანტიკური შეფასება, მაგრამ უშუალო round-trip/measurement ჯერ არ ჩატარებულა | **Medium** |

### 10.2 გადაუწყვეტელი კითხვები

1. **სიზუსტის ზღვარი:** პირველადი სწავლისთვის დასაშვებია მხოლოდ safety rule + `indeterminate`, თუ მომხმარებელი კომპონენტის operating voltage-ის ზუსტ worst-case შედარებას მოითხოვს?
2. **Board catalog-ის ფარგლები:** მხოლოდ ოფიციალური Espressif DevKitC V4-ის ზუსტი variants, თუ ფართოდ გავრცელებული „ESP32 DevKit“ clone-ებიც? უკანასკნელი გაცილებით მაღალი მონაცემობრივი რისკია.
3. **ვიზუალური სამყარო:** მხოლოდ board-face 2D wiring, თუ schematic/breadboard ორი დამოუკიდებელი view? ორივე მოითხოვს ერთსა და იმავე engineering IDs-ზე mapping-ის გამოცდას.
4. **Firmware context:** ვიზუალური wiring-ის ეტაპზე მომხმარებელმა იცის რეალური GPIO mux/config? თუ არა, წესის შედეგი ხშირად mode-conditional იქნება.
5. **Component model rights:** რომელი vendor SPICE/IBIS models შეიძლება კანონიერად მოხდეს platform-hosted reuse? ამ ეტაპზე per-model answers **UNVERIFIED**.
6. **Measured truth:** არსებობს reference bench, reference boards და სანდო measurements, რომ კომპონენტური მახასიათებლების ინტერპრეტაცია შემოწმდეს? არ იყო მოწოდებული.
7. **Data curation cost:** რამდენი verified part/board შესაძლებელია მოვლის რესურსში და რა update policy ექნება errata-ს/PCN-ს? **UNVERIFIED**.
8. **IEC CDD rights:** public link/reference-ის გადაღმა რა permission იქნება საჭირო ავტომატური მონაცემთა დასამუშავებლად/გასავრცელებლად? სრული terms review/permission — **UNVERIFIED**.

---

## 11. Recommended validation experiments **before implementation**

ესენი არის არქიტექტურული მტკიცების *ფალსიფიკაციის ექსპერიმენტები*, არა დეველოპმენტის ეტაპები ან Codex-ის დავალებები.

| ექსპერიმენტი | მინიმალური შემოწმება | მისაღები/უარმყოფელი დასკვნა |
|---|---|---|
| **V1: cross-format topology round-trip** | ერთი 3+ sensor ESP32 wiring fixture-ის კავშირები შეადარეთ KiCad XML/netlist-სა და LibrePCB-ით დამოუკიდებლად აღწერილ topology-ს | **Accept:** terminal-to-net equivalence ზუსტად ერთნაირია, nonconnected crossings არ ირევა; **Reject:** UUID/alias ან crossing ქმნის უხილავ short-ს |
| **V2: library identity mutation** | ერთი generic component-ს მიეცით 2 devices, 2 packages და 2 MPN/revision; შეცვალეთ pin-to-pad assignment | **Accept:** unchanged instances არ იძენენ ახალ physical mapping-ს უხმოდ; violation-ს აქვს კონკრეტული variant cause |
| **V3: actual board-source audit** | DevKitC V4 header→module→SoC, 3V3 rail/regulator, GPIO34, GPIO0/C15, GPIO16/17 გადაამოწმეთ official docs + board schematic + errata | **Accept:** ყველა safety-critical assertion has exact scoped source; **Reject:** „ESP32 board“ generic table შეუმოწმებლად ცვლის hardware variant-ს |
| **V4: 5V logic tri-state gate** | ცნობილი 5V push-pull case, ცნობილი 3V3-compatible case და missing-output-spec case | **Accept:** `FAIL`, `PASS` (სრულყოფილი bounds-ით), `INDETERMINATE` ზუსტად არის გამიჯნული; **Reject:** nominal labels ცვლის evidence-ს |
| **V5: divider analytical vs numerical** | D-ის unloaded/loaded DC შედეგი შესადარებელია დამოუკიდებელ ხელით გამოთვლასთან და ngspice-თან; დაამატეთ input capacitance/tolerance | **Accept:** 3.333... V და 3.125 V (მოცემულ პირობებში), ხოლო უცნობი ADC model ვერ იძლევა ცრუ safe claim-ს |
| **V6: mode & power budget** | ერთი source + 2 sensors sleep/active/wake profiles, ერთი გამოტოვებული peak | **Accept:** შეფასება mode-specific-ა; missing peak იძლევა `INDETERMINATE`, არა safe all-modes |
| **V7: UI cross-probing invariants** | view zoom/pan/rotate, part swap, disconnect/reconnect, renaming, alternate artwork | **Accept:** unique terminal/net/rule mapping რჩება სწორი; UI geometry ვერ ცვლის topology-ს; dead refs გამოვლინდება |
| **V8: provenance/license audit** | კომპონენტის 10 პრაქტიკულად გავრცელებულ მონაცემს მიაბით source version/section/rights; მინიმუმ ერთი intentionally ambiguous clone | **Accept:** ყველა rule claim გამჭვირვალეა; proprietary source ან unverified part automatic inclusion არ ხდება |
| **V9: differentiated simulator output** | იგივე passive circuit-ის structured facts/constraints და solver model-დან მიღებული waveform/result განსხვავდება provenance-ში | **Accept:** solver run-ის არქონისას result არ არის `SIMULATED`; equation/domain mismatch იძლევა `NOT_EVALUATED` |

**შეჩერების კრიტერიუმი:** თუ V2/V3/V4/V7 ვერ იძლევა ერთმნიშვნელოვან hardware identity-ს, უსაფრთხოების გაურკვევლობის შენარჩუნებას და დარღვევის 2D ობიექტამდე მიკვლევადობას, canonical contract-ის საბოლოო დამტკიცება ნაადრევია. Model choice-ის დახვეწა ვერ შეავსებს მოწმობის დანაკლისს.

---

## 12. Primary references — URLs, versions, dates, verification

ყველა URL-ის ხელმისაწვდომობა/მიმდინარე საჯარო აღწერა გადამოწმდა **2026-11-20**. `release/publication date` და `verification date` განზრახ განსხვავდება. თუ PDF-ის normative full text არ იყო თავისუფლად სრულად შემოწმებული, ეს მითითებულია.

| ID | პირველადი წყარო და კონტროლირებადი ვერსია / გამოცემის თარიღი | URL |
|---|---|---|
| **R1** | KiCad 10.0.8 release, **2026-10-30** | https://www.kicad.org/blog/2026/10/KiCad-10.0.8-Release/ |
| **R2** | KiCad Developer Documentation, **S-expression Schematic Format**, page last modified **2025-02-20** (format semantics; compare KiCad 10 docs) | https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/ |
| **R3** | KiCad **Schematic Editor 10.0**, alternate pin functions, ERC, netlists, integrated ngspice (documentation for major version 10) | https://docs.kicad.org/10.0/en/eeschema/eeschema.html |
| **R4** | KiCad **Getting Started 10.0**, ERC-ის შესაძლებლობებისა და საზღვრების განმარტება | https://docs.kicad.org/10.0/en/getting_started_in_kicad/getting_started_in_kicad.html |
| **R5** | LibrePCB **2.1.1**, release **2026-06-12** | https://librepcb.org/blog/2026-06-12_release_2.1.1/ |
| **R6** | LibrePCB, **Library Concept**, symbol↔signal↔pad | https://librepcb.org/features/library-concept/ |
| **R7** | LibrePCB, **Create Library Elements**, component/device/package | https://librepcb.org/docs/quickstart/create-library-elements/ |
| **R8** | LibrePCB, **File Format**, project-local self-contained libraries, major-format versions | https://librepcb.org/features/file-format/ |
| **R9** | LibrePCB, **UUID References**, breaking-change behavior (current docs branch; individual page publication date **UNVERIFIED**) | https://docs.librepcb.org/_branches/master/librepcb/user-manual/references/ |
| **R10** | ngspice **47**, official NEWS **2026-08-11** (project FAQ records **2026-08-09** — minor date discrepancy) | https://ngspice.sourceforge.io/news.html |
| **R11** | ngspice official documentation, netlist → model/solver → results, manual version list incl. 46 (web/manual revision may trail binary release) | https://ngspice.sourceforge.io/docs.html |
| **R12** | L. W. Nagel, *SPICE2: A Computer Program to Simulate Semiconductor Circuits*, UC Berkeley technical report **UCB/ERL M520, 1975-05-09** | https://www2.eecs.berkeley.edu/Pubs/TechRpts/1975/9602.html |
| **R13** | IEC **61360-1:2017**, concepts/properties definition (public official abstract; full normative sections **UNVERIFIED**) | https://webstore.iec.ch/en/publication/28560 |
| **R14** | IEC **61360-2:2012**, corrected version **2025-03**; IEC CDD public metadata (normative full text **UNVERIFIED**) | https://webstore.iec.ch/en/publication/5381 |
| **R15** | QUDT **3.5.3**, schema/unit/quantitykind, published catalog **2026-10-20** | https://www.qudt.org/catalog/qudt-catalog.html |
| **R16** | QUDT public-repo license, **CC BY 4.0**, GitHub | https://github.com/qudt/qudt-public-repo/blob/main/LICENSE.md |
| **R17** | **IEEE 1685-2022 IP-XACT**, official IEEE description/metadata, **2022**, IEEE Xplore document **10054520** | https://standards.ieee.org/ieee/1685/10583/ |
| **R18** | Accellera, *IP-XACT 2022 User Guide*, **2023** (official explanatory guide, **not** replacement for normative standard) | https://www.eda.org/images/downloads/standards/ip-xact/IPXACT-2022_user_guide.pdf |
| **R19** | OMG **SysML v2.0**, formal spec **2025-09** | https://www.omg.org/spec/SysML/2.0 |
| **R20** | OMG final adoption announcement **2025-07-21**, SysML v2 + KerML + API services | https://www.omg.org/news/releases/pr2025/07-21-25.htm |
| **R21** | IEC **61360-7:2024**, general-items cross-domain dictionary | https://webstore.iec.ch/en/publication/72956 |
| **R22** | IBIS Open Forum, **IBIS 8.0**, ratified **2025-12-05**; model supplier licenses assessed individually | https://www.ibis.org/specs/ |
| **R23** | Arm **CMSIS-SVD**, public device/peripheral register specification; publicly visible docs, earlier CMSIS_5 reference; exact vendor SVD versions vary | https://arm-software.github.io/CMSIS_5/latest/SVD/html/index.html |
| **R24** | Modelica Language Specification **3.7**, **2026-05** | https://specification.modelica.org/maint/3.7/MLS.html |
| **R25** | FMI specification **3.0.2**, **2024-11-27**, model exchange / co-simulation | https://fmi-standard.org/docs/3.0.2/ |
| **R26** | Espressif **ESP32-DevKitC V4** user guide, board pinout, power and C15 note (living online version, page date **UNVERIFIED**) | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html |
| **R27** | Espressif **ESP32 Series Datasheet v5.3** as retrieved **2026-11-20**, electrical tables and GPIO matrix (exact PDF publication date **UNVERIFIED**) | https://documentation.espressif.com/esp32_datasheet_en.html |
| **R28** | Espressif **ESP-IDF GPIO reference (ESP32)**, input-only pins/mux constraints (living docs; exact commit version **UNVERIFIED**) | https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html |
| **R29** | Espressif **Chip Revision Identification / Errata** (living docs, exact silicon mapping per part required) | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/01-chip-identification/index.html |
| **R30** | Espressif **ESP-FAQ ADC**, ADC input/divider/sample-and-hold discussion (living docs) | https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/peripherals/adc.html |
| **R31** | Espressif **ESP-IDF SoC caps**, chip-specific feature database; tool source guide (version-sensitive) | https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/soc_caps.rst |
| **R32** | NXP **UM10204**, I²C-bus specification, Rev. 7.0 **2021-10-01** (manufacturer spec; source trace) | https://www.nxp.com/docs/en/user-guide/UM10204.pdf |
| **R33** | KiCad official application licensing, **GPLv3 or later** majority | https://www.kicad.org/about/licenses/ |
| **R34** | KiCad official library licensing, **CC BY-SA 4.0 + project-use exception** | https://www.kicad.org/libraries/license/ |
| **R35** | LibrePCB licensing, **GPLv3 source; official libraries CC0-1.0** | https://librepcb.org/license/ |
| **R36** | ngspice developer licensing, mainly **modified BSD with exceptions** | https://ngspice.sourceforge.io/devel.html |
| **R37** | IEC official copyright / CDD database reproduction conditions | https://webstore.iec.ch/en/copyright |
| **R38** | IEC Webstore terms / FAQ, rights and AI-technology-use restrictions (terms subject to change, legal review required) | https://webstore.iec.ch/en/faq/ |
| **R39** | Nagel & Pederson, *SPICE (Simulation Program with Integrated Circuit Emphasis)*, UC Berkeley **UCB/ERL M382, 1973** | https://www2.eecs.berkeley.edu/Pubs/TechRpts/1973/22871.html |

**Bibliographic precision:** UC Berkeley-ის R12/R39 არის პირველადი *research technical reports*, **არა** თვითნებურად „peer-reviewed journal articles“. IEEE-ს SPICE-ის ისტორიის კონფერენციული მიმოხილვა 2023 წელს არსებობს: https://resourcecenter.cas.ieee.org/conferences/mwscas-2023/cas2023mwscas0010 . ამ კვლევაში **ვერ დადასტურდა ახალი peer-reviewed comparative study**, რომელიც ზუსტად KiCad/LibrePCB/SPICE/QUDT/IP-XACT/SysML-ს beginner-board safety coverage-ით ერთნაირი ტესტებით ადარებს — **UNVERIFIED**. შესაბამისად არქიტექტურული შეფასება ეფუძნება თითოეულის პირველადი დოკუმენტაციის capabilities-სა და განსაზღვრულ test fixtures-ს, და არა არარსებული head-to-head სამეცნიერო შედეგის წარმოდგენას.

---

## DECISION RECORD CANDIDATE

**არქიტექტურის მფლობელმა ცალკე უნდა დაამტკიცოს ან უარყოს თითოეული პუნქტი; ეს კვლევა მათ თვითნებურად არ ამტკიცებს.**

| Decision ID | ზუსტად გასამტკიცებელი არჩევანი | რეკომენდებული პოზიცია | პირობა / რას არ ნიშნავს |
|---|---|---|---|
| **DR-01** | იქნება თუ არა canonical „ერთი უნივერსალური ფაილი“? | **არა**; მხოლოდ ერთმნიშვნელოვანი semantic source of truth | solver/view payloads არის წარმოებული representations |
| **DR-02** | მიიღება თუ არა ფენების სავალდებულო გამიჯვნა — identity, topology, characteristics, behavior, context, constraints, results, view? | **დიახ** | არ იძლევა შენახვის ან module architecture-ის განკარგულებას |
| **DR-03** | მიენიჭოს თუ არა LibrePCB-ის component→signal→device→pad/part semantics-ს მთავარი reference pattern-ის სტატუსი? | **დიახ, კონცეპტუალურად** | არ ნიშნავს GPL აპის კოდის გადმოტანას |
| **DR-04** | იყოს თუ არა netlist-ის მთავარი სემანტიკა KiCad-ის მსგავსად explicit terminal-to-net connectivity და junction handling? | **დიახ** | KiCad `.kicad_sch` არ ხდება obligatory storage format |
| **DR-05** | უნდა იყოს თუ არა exact board→module→SoC→terminal mapping და board/chip revisions safety-sensitive წესებისთვის სავალდებულო? | **დიახ** | უცნობ clone-board-ზე შეფასება `INDETERMINATE` |
| **DR-06** | იქნება თუ არა source-backed limit/context/provenance სავალდებულო ყველა safety result-ში? | **დიახ** | no silent default `5V tolerant`, `3.3V safe`, `typical=max` |
| **DR-07** | იქნება თუ არა verification four-state და falsifiable? | **დიახ:** PASS/FAIL/INDETERMINATE/NOT_EVALUATED | UI severity ვერ გადაწერს დასკვნის uncertainty-ს |
| **DR-08** | იყოს თუ არა UI geometry non-authoritative, immutable engineering IDs-ზე mapping-ით? | **დიახ** | ვიზუალური anchor შეცდომის მიზეზია მხოლოდ presentation link-ით |
| **DR-09** | დარჩეს თუ არა SPICE/IBIS/Modelica/FMI optional model-bound external analysis, არა source-of-truth? | **დიახ** | simulator-ის ან ფიზიკური სისწორის შეძენის დაპირება არ არის |
| **DR-10** | იყოს თუ არა official LibrePCB CC0 + attributable source facts სასურველი library seed, ხოლო KiCad BY-SA/Copyrighted IEC/proprietary vendor model rights ცალკე review-ს ექვემდებარებოდეს? | **დიახ, პირობითად** | ყოველი imported artifact-ის rights audit აუცილებელია |
| **DR-11** | შეიზღუდოს თუ არა თავდაპირველი hardware assertions ზუსტად დასახელებული ოფიციალური board/module revisions-ით? | **დიახ, მონაცემების დადასტურებამდე** | clone-board „compatibility“ არ უნდა იყოს ნაგულისხმევი |
| **DR-12** | დამტკიცდეს თუ არა ეს კონტრაქტი უშუალოდ V2/V3/V4/V7 evidence gates-ის ჩატარების გარეშე? | **არა** | კვლევითი რეკომენდაცია ჯერ არ არის validated operational model |

**რეზოლუცია:** **CONDITIONAL APPROVAL RECOMMENDED** — thin, layered semantic contract არის ამ ეტაპზე ყველაზე ნაკლებად თვითნებური და ყველაზე მეტად interoperable მიმართულება. **დაუყოვნებლივ უნდა უარვყოთ** უნივერსალური EDA/physics/visualization representation-ის მოთხოვნა და `unknown = safe` ლოგიკა. **ჯერ არ უნდა გამოცხადდეს დამტკიცებულად** exact device-data coverage, simulation fidelity ან 2D mapping correctness; ეს ცალკე ემპირიული ვალიდაციის საგანია.
