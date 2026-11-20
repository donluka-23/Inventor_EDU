# RESEARCH H — ქართული საინჟინრო განზრახვა, ფორმალური მოთხოვნები და მტკიცებულებაზე მიბმული საგანმანათლებლო უკუკავშირი

**პროექტი:** INVENTOR EDU  
**თარიღი:** 2026-11-20  
**ტიპი:** დამოუკიდებელი სამეცნიერო–ტექნიკური კვლევა; მხოლოდ გადაწყვეტილების პაკეტი  
**სტატუსი:** `RESEARCH / PROPOSED / NOT AUTHORIZED FOR IMPLEMENTATION`  
**შემოწმებული რეპოზიტორია:** [`donluka-23/Inventor_EDU`](https://github.com/donluka-23/Inventor_EDU), `codex/demo-001-scenario-bridge`, commit [`2ece740bb49dfd330cbdecd4981204eb085821dd`](https://github.com/donluka-23/Inventor_EDU/commit/2ece740bb49dfd330cbdecd4981204eb085821dd)  
**მანდატი:** პროექტის მფლობელის შესაფასებლად; კოდის, ახალი ონტოლოგიის, შესასრულებელი Codex-დავალებებისა და ავტონომიური არქიტექტურული დამტკიცების გარეშე.

> **საკუთარი მტკიცებულების სტატუსის აღნიშვნა:** `REPO-OBSERVED` = მითითებულ commit-ზე კოდი/ანგარიში წავიკითხე; `SOURCE-VERIFIED` = გარე პირველწყარო გადავამოწმე; `REPORTED-NOT-RERUN` = პროექტის შესრულების ანგარიში აცხადებს შედეგს, მაგრამ ჩემს გარემოში არ განმეორებულა; `PROPOSED` = ახალი კვლევითი კონტრაქტი ან წესი; `UNVERIFIED` = დამოუკიდებელი მტკიცებულება არ მომეპოვება. სინტაქსური ტიპიზაცია, სემანტიკური ვალიდაცია, წყაროს ნამდვილობა და რეალური აპარატურის უსაფრთხოება **ოთხი სხვადასხვა გარანტიაა**.

## 1. აღმასრულებელი რეკომენდაცია

**რეკომენდაცია: `CONDITIONAL` — შეზღუდული, ადაპტერებზე დაფუძნებული არქიტექტურის ექსპერიმენტული შერჩევა მფლობელის გადაწყვეტილებისთვის.**

შესწავლილი კომპრომისებიდან პირველი შემოწმებადი ვარიანტია **Architecture A**: შეზღუდული ქართულენოვანი გრამატიკა/ნიმუშები + ტიპიზებული მოთხოვნების შუალედური წარმოდგენა + სრულად დეტერმინისტული კომპილაცია მხოლოდ არსებული ვერიფიკატორის მხარდაჭერილ მოთხოვნებში + ქართული, წყაროზე მიბმული მინიშნებების წინასწარ განხილული შაბლონები. **Architecture C** (შერეული პარსერი/პედაგოგიკური planner) მხოლოდ შემდეგი ექსპერიმენტის კანდიდატია; **Architecture B** (LLM-first) არ არის მიღებული ნაგულისხმევად. ეს არ ნიშნავს, რომ A უკვე მუშაობს ან ქართულ პარაფრაზებს კარგად ფარავს — ამას ბენჩმარკი უნდა გამოავლენდეს.

ორი დამოუკიდებელი საზღვარი:

1. **განზრახვიდან მოთხოვნამდე:** ტექსტი ასახავს მომხმარებლის მოთხოვნას და არა ელექტრულ ჭეშმარიტებას. ინტერპრეტაცია ინახავს ლექსიკურ საფუძველს, განზრახვას, რაოდენობას/ერთეულს, ალტერნატიულ წაკითხვას, გაურკვევლობას და აკრძალულ დასკვნებს. გასაგები მოთხოვნა *ჯერ კიდევ არ ნიშნავს* რეალიზებად ან უსაფრთხო წრედს.
2. **გამოთვლიდან უკუკავშირამდე:** მხოლოდ არსებული `GpioFinding`, `GpioCoverage` და `DemoLinkResult` იძლევა კონკრეტულ, მკაცრად შეზღუდულ საჩვენებელ დასკვნას. `UNKNOWN` არ გადაიქცევა `PASS`-ად; `NOT_EVALUATED` არ გადაიქცევა „დამოწმებულად“. UI/ენოვანი მოდელი ვერ ქმნის ახალ საინჟინრო ფაქტს.

**პირველი რეალური ჰიპოთეზა:** შაბლონზე/წყაროზე დაფუძნებული ქართულენოვანი განმარტება ამცირებს *იმავე GPIO შეცდომის მიზეზის გაუგებრობას* მხოლოდ ფაქტობრივი დიაგნოზის ჩვენებასთან შედარებით. მხოლოდ კავშირის გასწორების დრო არ არის სწავლის მტკიცებულება. ბაზარი, მაღალი სასწავლო ეფექტიანობა, ან სრული Goal-to-Circuit ციკლი დადასტურებული არ არის.

**კრიტიკული წინააღმდეგობა, რომელიც უნდა გამოირიცხოს:** `READY_FOR_MATCHING` არ შეიძლება ნიშნავდეს „მზად არის ფიზიკური კავშირისა და უსაფრთხოების დადასტურებისთვის“. ეს არის მხოლოდ დასაშვებ *კანდიდატთა ძიებაზე* გასვლის უფლება; კონკრეტული ნაწილი, რევიზია, მავთულები, ელექტრული პირობები და firmware ცალკე გასამყარებელია.

## 2. ზუსტი ტექნიკური baseline და წყაროთა ხარვეზები

### 2.1 კოდის რეალურად ნანახი მდგომარეობა

| ფენა | აღმოჩენილი კონტრაქტი / ქცევა | სტატუსი და დასკვნის ზღვარი |
|---|---|---|
| `inventor_edu/models.py` | Frozen Pydantic `DeviceIdentity`, `SourceDocument`, `EvidenceClaim`, `SignalMappingEvidence`, `TerminalRef`, `Conductor`, `CircuitSnapshot`, `CatalogSnapshot` | `REPO-OBSERVED`; არ საჭიროებს ჩანაცვლებას. `signal_mapping` ფიზიკურ კონტაქტს უკავშირებს ტიპიზებულ ლოგიკურ სამიზნეს, მხოლოდ მტკიცებულების ფარგლებში. |
| `inventor_edu/core.py` | კატალოგის დაშვება, `compute_nets`, `resolve_terminal`, კანონიკური snapshot და SHA-256; მკაცრი ფიზიკური ID-ები | `REPO-OBSERVED`; UI-ის გეომეტრია და მომხმარებლის ტექსტი ვერ ანაცვლებს netlist-ს. |
| `inventor_edu/gpio_facts.py` | `GpioFactSet`, `HardwareScope`, `SiliconFact`, `BoardResourceFact`, `StrapFact`, გამოყოფილი წყაროები, `factset_digest` | `REPO-OBSERVED`; შეფასება `TEST_ONLY_SOURCE_REVIEWED`, არა პროდუქციული ნდობა. |
| `inventor_edu/gpio_verify.py` | `GpioRequirement` → `GpioVerificationReport(findings, coverage)`; ფუნქციები `GPIO_IN`, `GPIO_OUT`, `GPIO_IN_PULLUP` | `REPO-OBSERVED`; ცალკე `PASS/FAIL/UNKNOWN/NOT_APPLICABLE` და `NOT_EVALUATED`. ელექტრული თავსებადობა `ELECTRICAL_CHECK_DELEGATED`; `ACTIVE_CONFIGURATION` არ მტკიცდება firmware-ის მხოლოდ სახელდებით. |
| `inventor_edu/demo_bridge.py` | `analyze_hcsr04_wiring()`; `Trig → GPIO_OUT`, `Echo → GPIO_IN`, რეალური ქსელიდან board terminal-ის პოვნა | `REPO-OBSERVED`; მხოლოდ `HCSR04_GPIO_WIRING`, `TEST_ONLY_NOT_PRODUCTION`; არა თავისუფალი ტექსტი/GUI/firmware/ელექტრული გამოთვლა. |
| `data/gpio/devkitc_32e_catalog.json` | `J2.5→GPIO34`, `J3.9→GPIO18`, `J3.8→GPIO19`, `sensor/Trig`, `sensor/Echo`; რევიზიისა და საცალო პროდუქტის იდენტობის შეზღუდვები | `REPO-OBSERVED`; დოკუმენტური პროფილი ≠ ხელში არსებული ფიზიკური მოწყობილობის დამტკიცება. |
| `reports/DEMO-001-REPORT.md` | `J2.5 → Trig` FAIL, `J3.9 → Trig` capability PASS, `J3.8 → Echo` input PASS; 54/54 regression | `REPORTED-NOT-RERUN`; ინტეგრაციის ტესტის ანგარიში, არა ფიზიკური ტესტი. |
| `reports/CORE-001B-01-REPORT.md` და ledger | GPIO direction, flash reservation, strap unknown, წყაროების SHA-256 / კონკრეტული locator | `REPORTED-NOT-RERUN`; წინა ეტაპის 44 ტესტი და წყაროს მიღების შემოწმება დაფიქსირებულია. |
| `docs/prototype/MASTER_PLAN.md` | Bounded Goal-to-Circuit; ქართული intent და feedback ცალკე დაგეგმილი; LLM გადადებულია გაზომვამდე | `REPO-OBSERVED`; ეს მოქმედი განვითარების საზღვარია და არა Research H-ის მიერ ავტორიზებული ცვლილება. |

**საჭირო ზუსტი სახელები:** `GpioFinding` შეიცავს `finding_id`, `requirement_id`, `rule_id`, `rule_version`, `terminal`, `affected_net`, `requested_function`, `operating_state`, `hardware_scope`, `evidence_claims`, `missing_prerequisites`, `reason_code`, `catalog_digest`, `snapshot_digest`, `factset_digest`; `GpioCoverage` ცალკე კლასია და **არ აქვს `status=UNKNOWN`**. `DemoLinkResult.state` ერთ-ერთია: `CONNECTED_UNIQUE | MISSING | AMBIGUOUS | NON_GPIO | SHARED_SIGNAL_NET`. ბოლო ოთხი მდგომარეობის ახსნა შეიძლება ტოპოლოგიური დიაგნოზიდან, მაგრამ არ უნდა მოიგონოს არარსებული GPIO finding ID.

**მნიშვნელოვანი კოდის ნიუანსი:** `ELECTRICAL_COMPATIBILITY` bridge-ის გადაცემული check-ია, მაგრამ `gpio_verify.py` მას `GpioCoverage/NOT_EVALUATED`-ად აბრუნებს და არა ელექტრულ verdict-ად. `BOARD_AVAILABILITY` GPIO18-ის ამ fixture-ზე `UNKNOWN/EVIDENCE_MISSING`-ია, ხოლო `ACTIVE_CONFIGURATION` — `UNKNOWN/ACTIVE_CONFIG_UNKNOWN`; `PHYSICAL_CAPABILITY/PASS` არ „ამწვანებს“ მთლიან წრედს. `GPIO6` შეიძლება სილიკონის დონეზე output-ს უჭერდეს მხარს, მაგრამ board-ზე flash-ისთვის იყოს დაკავებული (`FAIL/RESERVED_RESOURCE`).

**Pinned acceptance:** კატალოგი `sha256:356732040b6bd762e8c604ae63c3600df5da225cc938af6dff688b25aad4c57b`; factset `sha256:890f608028990e8f80f9ee48cd4388e58df1d160acc7edf2bf61445df8556d16`. SHA იცავს ბაიტების იდენტურობას, არა თვითონ publisher-ის, შეფასების ხარისხის ან production authorization-ის ნამდვილობას. საჭიროა დამოუკიდებლად ავტორიზებული `trusted_*` პინები.

**GitHub პირველწყაროები:** [models](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/inventor_edu/models.py), [GPIO verifier](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/inventor_edu/gpio_verify.py), [bridge](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/inventor_edu/demo_bridge.py), [DEMO-001 ანგარიში](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/DEMO-001-REPORT.md), [CORE-001B ledger](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md).

### 2.2 დამატებითი მასალების ხელმისაწვდომობა და ხარისხი

Research F და G-ის ამ საუბარში ხელმისაწვდომი ფაილები **კვლევის დავალების ტექსტებია**, რომელშიც კვლევის მეთოდიც და სასურველი შედეგიცაა განსაზღვრული; მათში ჩაწერილ ბაზრის/UX ჰიპოთეზებს დამოუკიდებლად მიღებულ შედეგებად არ ვაცხადებ. Research B და C ხელმისაწვდომია repository `docs/research/raw`-ში როგორც კვლევის შესასრულებელი მითითებები; მათემატიკური/ფიზიკური დასკვნები აქ დამყარებულია დამოუკიდებელ source ledger-სა და კონკრეტულ კოდზე. `DATA-001`-ის structural pilot და მისი შეზღუდვები ჩანს `docs/STATUS.md`-სა და შესაბამის ანგარიშში. **არ მომეპოვება:** მომხმარებლის ინტერვიუები, ქართული პარსერის კორპუსზე გაზომილი შედეგები, რეალური გაკვეთილების ეფექტიანობის მონაცემები, წყაროს რევიზიის სინქრონული production SLA. ამიტომ კვლევითი რეკომენდაციები რჩება პირობითად.

## 3. სამეცნიერო საფუძველი და შემოწმებული პირველწყაროები

| მიმართულება და პირველწყარო | რა არის რეალურად დასაბუთებული | რა არ შეიძლება დავასკვნათ |
|---|---|---|
| Requirements engineering: [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | მოთხოვნების ფორმულირება, ხარისხი, მიკვლევადობა, მართვა. | სტანდარტი **არ განსაზღვრავს** INVENTOR-ის კონკრეტულ JSON ინტერფეისს ან ქართულ პარსერს. |
| Typed JSON validation: [JSON Schema 2020-12](https://json-schema.org/specification) | ფორმის, ტიპის, ნებადართული მნიშვნელობების, required field-ების კონტროლი. | JSON Schema ვერ ამტკიცებს კომპონენტის ფაქტების წყაროებსა და ფიზიკურ ჭეშმარიტებას. |
| ფრთხილი LLM: [Structured Outputs documentation](https://developers.openai.com/api/docs/guides/structured-outputs) | შესაძლებელია მოდელის გამოსავლის სქემაზე შეზღუდვა. | სინტაქსურად სწორი JSON შეიძლება შეიცავდეს გაუმართლებელ ტექნიკურ მოთხოვნას/ფაქტს. |
| Georgian NLP: [Lobzhanidze et al., 2024, ACL](https://aclanthology.org/2024.tlt-1.5/), [UD Georgian-GLC](https://universaldependencies.org/treebanks/ka_glc/) | არსებობს ქართული მორფოსინტაქსური ანოტაცია და კვლევითი მოდელების მონაცემი. | უნივერსალური კორპუსი არ ნიშნავს შედგენილი ელექტრონული დავალებების სემანტიკურ სიზუსტეს. |
| ქართული ალტერნატიული კორპუსი: [UD Georgian-GNC](https://universaldependencies.org/treebanks/ka_gnc/) და [Stanford Stanza models](https://stanfordnlp.github.io/stanza/available_models.html) | შესაძლებელია არსებული ტოკენიზაციის/ლემატიზაციის წინასწარ შემოწმება. | არც დამჭერი ლექსიკონის სიზუსტე, არც ლიცენზიების ერთგვაროვნება არაა გარანტირებული. |
| დაბალრესურსიანი ენის შეფასება: [GeoLogicQA, ACL 2025](https://aclanthology.org/2025.lowresnlp-1.13/) | ქართულ LLM-ებზე შეფასება თავისთავად მნიშვნელოვანი და შესაძლებელი ამოცანაა. | ლოგიკური კითხვების შედეგი არ არის ქართულ საინჟინრო მოთხოვნათა პარსერის შეფასება. |
| ITS — მოდელის ტრასირება: [Anderson et al., 1995](https://www.tandfonline.com/doi/abs/10.1207/s15327809jls0402_2) | პედაგოგიკური ჩარევის დაკავშირება ფორმალიზებულ ცოდნასა და მოსწავლის ნაბიჯთან. | კოდში არსებული მარტივი finding ავტომატურად არ ქმნის სრულ cognitive tutor-ს. |
| ITS — შეზღუდვებზე დაფუძნებული სწავლება: [Mitrovic, Koedinger & Martin, 2003](https://ir.canterbury.ac.nz/items/3e3e0b19-60b1-443f-a702-9b0b63ac7b39), [Mitrovic & Ohlsson, 2015](https://doi.org/10.1007/s40593-015-0049-9) | დარღვეული დომენური წესის საფუძველზე ახსნა შეიძლება სასარგებლო სასწავლო სტრუქტურა იყოს. | SQL-Tutor-ის ეფექტის პირდაპირ გადატანა დამწყებ ESP32 მომხმარებელზე მიუღებელია. |
| ფორმატიული უკუკავშირი: [Shute, 2008](https://doi.org/10.3102/0034654307313795), [Hattie & Timperley, 2007](https://doi.org/10.3102/003465430298487) | მიზნობრივი, ამოცანასა და პროცესზე ორიენტირებული განმარტებების თეორიული/ემპირიული საფუძვლები. | მუდმივი დეტალური მითითება ყოველთვის უკეთესი არ არის. |
| Cognitive load: [Paas, Renkl & Sweller, 2003](https://www.tandfonline.com/toc/hedp20/38/1) | სასწავლო მასალის მოცულობა/ეტაპურობა მნიშვნელოვანია. | „ერთ ეკრანზე ერთი მინიშნება“ უნივერსალური ექსპერიმენტული კანონია — არა. |
| Self-explanation: [Chi et al., 1994](https://doi.org/10.1207/s15516709cog1803_3), transfer: [Butler, 2010](https://pubmed.ncbi.nlm.nih.gov/20804289/) | ახსნაზე ორიენტირებულმა აქტივობამ და დამოუკიდებელმა გადატანამ შეიძლება გამოავლინოს გაგება. | ერთი სწრაფი პინის შეცვლა = მიზეზობრივი გაგება — არა. |
| Tutoring comparative review: [VanLehn, 2011](https://doi.org/10.1080/00461520.2011.611369) | tutoring ეფექტი დამოკიდებულია სისტემის ტიპზე/პირობებზე. | ეფექტის ზომის პირდაპირი პროგნოზი INVENTOR EDU-ზე — არა. |
| მტკიცებულების provenance: [W3C PROV-O](https://www.w3.org/TR/prov-o/) | წყარო–დასკვნის წარმომავლობის მოდელირების სტანდარტული ცნებები. | სრული RDF/PROV ინფრასტრუქტურის დამატება პატარა MVP-ს არ სჭირდება. |
| სამიზნე hardware: [Espressif DevKitC V4 guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html) და [ESP32-WROOM-32E datasheet](https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html) | ზუსტი board-header პინები და მოწყობილობის დოკუმენტირებული თვისებები. | GPIO direction-ის ცოდნა არ ამტკიცებს HC-SR04 Echo-ის ელექტრულ თავსებადობას. |

ლიტერატურის მნიშვნელობა მკაცრად შემოსაზღვრულია: ფსიქოლოგიური/პედაგოგიკური ნაშრომები ამყარებს **ჰიპოთეზის ტესტის დიზაინს**, მაგრამ არა კონკრეტული პროდუქტის ეფექტიანობის მტკიცებას.

## 4. ქართული განზრახვის ინტერპრეტაციის მეთოდები

### 4.1 მეთოდების შედარება

ნიშნები: `++` კარგი პოტენციალი ვიწრო ამოცანაზე; `+` მისაღები; `?` ემპირიულად გადასამოწმებელი; `−` სარისკო ან ძვირი პირველ ვერსიაში. ეს **კვლევითი შეფასებებია**, არა შესრულებული benchmark.

| მეთოდი | მაგალითები / სამეცნიერო ბაზა | გამეორებადობა და ქართული | ჩავარდნის რეჟიმი | დანახარჯი/პრივატულობა | გადაწყვეტილება |
|---|---|---|---|---|---|
| ზუსტი რეგულარული/სინტაქსური წესები | domain grammar, წინასწარ განსაზღვრული კონსტრუქციები | `++` ვიწრო scope | უცნობი პარაფრაზის არასწორი უარყოფა | CPU დაბალი; ლოკალური | **პირველი baseline** |
| ქართული ლექსიკონი + მორფოლოგიური ნორმალიზაცია | UD-GLC, Stanza, დომენური სინონიმები | `+/?`; suffix-ები, ზმნის ფორმები, ჟარგონი | ლემის გამოტოვება ან არასწორი ნორმალიზება | დაბალი/საშუალო; მოდელის ლიცენზია გადასამოწმებელი | **შეზღუდული გაფართოების კანდიდატი** |
| Template/slot filling | `სუბიექტი–ოპერაცია–მაჩვენებელი–ზღვარი–რეაქცია` | `++` template-ებზე; გარეთ `?` | უარყოფის, პირობის, „ან/და“-ს დაკარგვა | დაბალი, ლოკალური | **პირველი baseline** |
| Domain-specific language (DSL) | ტიპიზებული threshold predicate, event/action | JSON/AST დეტერმინისტულია | მომხმარებელს ხელით წერა არ უნდა მოვთხოვოთ | მცირე | **შიდა IR-ისკენ** |
| LLM + JSON schema | constrained decoding | სტრუქტურა `+`, ფაქტობრივი სიზუსტე `?` | დაცული JSON-შიც მოხდება ცრუ მოთხოვნის დამატება | API ღირებულება/ტექსტის გადაცემა | **შესადარებელი კანდიდატი, არა ავტორიტეტი** |
| LLM candidates + deterministic gate | მრავალჰიპოთეზიანი candidate extraction, provenance | გამეორებადობა მხოლოდ საბოლოო ვალიდატორის ფარგლებში | ერთი ცრუ, მაგრამ სქემურად სწორი „ვარაუდი“ | მეტი latency/მომსახურება | **პირობითი შემდგომი ვარიანტი** |
| Hybrid clarification | კლარიფიკაციის ხე, mutually exclusive ინტერპრეტაციები | კარგად ახსნადი | არასწორი კითხვა/მომხმარებლის ზედმეტი დატვირთვა | დაბალი | **A-შიც აუცილებელია** |
| Dependency/constraint graph | წინაპირობები, conflict detection, მრავალმნიშვნელოვანი ლოგიკა | `++` კარგად ტიპიზებულ ფაქტებზე | ზედმეტად დიდი ontology/solver | მცირე კონკრეტული შემთხვევებისას | **მცირე graph, არა solver-first** |
| State machine/temporal formulas | `distance < 0.30m` → LED on | `+` ფორმალური აღწერა | sampling, hysteresis, trigger semantics უცნობია | დაბალი ჩანაწერისთვის, მაღალი დადასტურებისთვის | **IR სურვილის დონეზე, execution არა** |

**OSS-ის რეალური ეკონომია:** JSON Schema/Pydantic ამცირებს ხელით ტიპების შემოწმებას; Unicode/ICU — ტექსტის ნორმალიზაციას; ქართული UD/Stanza — პოტენციურად ტოკენიზაციის/ლემატიზაციის შრომას; graph traversal — მოთხოვნების დამოკიდებულებებს. არცერთი ამ მოდულთაგანი არ იძლევა წარმოებაში გამოსაყენებელ `GPIO34 OUTPUT` დასკვნას მომხმარებლის წინადადებისგან — დასკვნა მოდის მხოლოდ ცალკე reviewed facts-იდან და verifier-იდან.

### 4.2 `PROPOSED` ტექსტის გადამუშავების დასაშვები ჯაჭვი

1. შეინახოს უცვლელი `original_text`, `locale=ka-GE`, span-offset-ები; შემდგომმა ნორმალიზაციამ არ უნდა წაშალოს თავდაპირველი მტკიცებულება.
2. Unicode NFC და უსაფრთხო whitespace/case წესები; არ გადაკეთდეს `GPIO34`, `ESP32-DevKitC-32E`, `HC-SR04`, `5V`, `3.3V`, `J2.5` შემთხვევით სეგმენტებად.
3. რაოდენობები და საზომები დამოუკიდებლად: `30 სმ`, `30სანტიმეტრი`, `0.3 მ`, `300 მმ` → მნიშვნელობა `0.30 m` **მხოლოდ** სანდო unit parsing-ით; სხვა საზომზე გაურკვევლობა. `30` მარტო რჩება unit-missing.
4. ზმნის/პირობის ლექსიკონი: `გავზომო`, `ზომავდეს`, `მაჩვენოს`; `თუ`, `როცა`, `როგორც კი`, `იმ შემთხვევაში`; `ახლოს`, `ნაკლები`, `არანაკლებ`, `მაქსიმუმ` — მიმართულების მკაცრი კონტროლით. `30-ზე ახლოს` → მკაცრი `<`, ხოლო `30 ან ნაკლები` → `<=`; ნუ გააერთიანებთ.
5. ზუსტ სახელებს მიენიჭოს `USER_SELECTED`/`USER_NAMED_FAMILY`; ზოგადი `ESP32` **არ დაიტვირთოს** ზუსტი board SKU-დ.
6. ამოიცნოს უარყოფა, კავშირი, განმეორება, შედარება, გაურკვევლობა, მოწყობილობის როლები; კონფლიქტური მიზნები ინახებოდეს ორივე span-ით.
7. ან შექმნას typed candidate მოთხოვნები, ან მკაფიოდ თქვას `UNPARSEABLE/NEEDS_CLARIFICATION`; **არასდროს** გახადოს ვარაუდი „verified“.

საფრთხის მაგალითები: „30 სმ-ზე *უფრო შორს* იყოს“ (`>`), „30 სმ-ზე *მეტით* დაშორებისას“ (სხვა), „30 სმ-ით შეამცირე“ (ცვლილება, არა ზღვარი), „LED არ აანთო“ (უარყოფილი მოქმედება), „ის“ (ანაფორა უცნობი), „საჭიროებისამებრ“ (არაფორმალური). ერთი ფრაზის სიტყვიერი დამთხვევა ვერ გადაჭრის მათ.

### 4.3 შეზღუდული სინტაქსის კვლევითი კანდიდატი

**არ არის იმპლემენტაციის კოდი.** დასაშვები აბსტრაქტული ფორმა:

`[გაზომე distance] [სენსორი optional] [როცა distance comparator number unit] [დააყენე output state] [controller family optional]`.

მაგალითი: „მინდა ESP32-ით გავზომო მანძილი და როდესაც ობიექტი 30 სანტიმეტრზე ახლოს იქნება, LED აინთოს.“ → `measure(distance)`; `threshold(distance, LT, 0.30m)`; `actuate(LED, ON)`; `controller_family(ESP32)`; `sensor_identity=UNRESOLVED`, `exact_board=UNRESOLVED`, `firmware_validation=OUT_OF_SCOPE`.

**შეუსაბამო შესატანი** არ უნდა „გამოსწორდეს“ გამოგონებული მნიშვნელობებით. პარსერის სამუშაო არ არის ინჟინრის დონის ინტერპრეტაცია, რომელი კომპონენტი აკმაყოფილებს მიზანს; ამას Research I-ის evidence-backed matcher აკონტროლებს.

## 5. ტიპიზებული მოთხოვნების შუალედური წარმოდგენა (IR)

**ყველა ქვემოთ ჩამოთვლილი ინტერფეისი არის `PROPOSED`, გამოგონილი კვლევითი კანდიდატი — არ არის მიმდინარე კოდის კლასები და არ ცვლის `CORE-001A`-ს.** გამოყენებულია ნოტაცია `field: Type` როგორც კონტრაქტი, არა შესასრულებელი კოდი.

### 5.1 საერთო ტიპები და მტკიცების ფენები

`ProvenanceKind = USER_EXPLICIT | USER_CONFIRMED | PARSER_DERIVED | CANDIDATE_INFERRED | SOURCE_BACKED | COMPUTED`.  
`AssertionClass = USER_ASSERTION | PARSED_REQUIREMENT | CANDIDATE_IMPLEMENTATION | VERIFIED_CAPABILITY | UNVERIFIED_CONDITION`.  
`EvidenceState = PROVIDED | REVIEWED | MISSING | CONFLICTED | STALE | OUT_OF_SCOPE`.  
`RequirementStrength = MANDATORY | OPTIONAL`; `ConstraintStrength = HARD | PREFERENCE`.  
`Quantity = {value_decimal_string, unit_ucum_or_SI, comparator?, raw_span, normalized_value?, normalization_proof?}`.  
`TextSpan = {start_codepoint, end_codepoint, original_excerpt}`; offset-ების კოდპოინტური ერთეული ცალსახად უნდა ფიქსირდებოდეს.  
`Reference = {instance_id?, terminal_id?, net_id?, definition_id?, catalog_digest?}` — `terminal_id` მარტო ცალსახა არ არის.

### 5.2 სავალდებულო კანდიდატი ინტერფეისები

```text
PROPOSED EngineeringIntent {
  schema_version: string; goal_id: ID; locale: "ka-GE" | other;
  original_statement: string; normalized_statement?: string;
  observable_goal: GoalExpression[];
  functional_requirements: FunctionalRequirement[];
  constraints: RequirementConstraint[];
  hardware_identity_constraints: IdentityConstraint[];
  parsed_spans: SpanBinding[];
  candidate_inferences: Assumption[];
  unresolved_ambiguities: Ambiguity[];
  missing_prerequisites: MissingPrerequisite[];
  required_capabilities: RequiredCapabilityQuery[];
  dependencies: {from_requirement_id, to_requirement_id, relation}[];
  supported_verification_scopes: ScopeDeclaration[];
  parser_id: string; parser_version: string; grammar_version?: string;
  requirements_digest: sha256; source_decisions: ProvenanceRecord[];
}
PROPOSED FunctionalRequirement {
  requirement_id: ID; kind: "MEASUREMENT"|"DIGITAL_OUTPUT"|"CONDITIONAL_BEHAVIOR"|"INTERFACE"|"OTHER";
  observable: string; subject_role: string;
  predicate?: {variable, comparator, quantity, temporal_semantics?};
  action?: {target_role, state};
  strength: RequirementStrength; constraint_strength: ConstraintStrength;
  assertion_class: AssertionClass; origin: ProvenanceKind;
  text_span?: TextSpan; dependencies: ID[];
  support_state: "IN_SCOPE"|"FUTURE"|"UNSUPPORTED";
}
PROPOSED RequiredCapabilityQuery {
  query_id: ID; requirement_ids: ID[];
  target: "COMPONENT_CANDIDATE" | "EXACT_PHYSICAL_TERMINAL" | "FIRMWARE_CAPABILITY";
  capability: "DISTANCE_MEASUREMENT"|"DIGITAL_INPUT"|"DIGITAL_OUTPUT"|"LED_DRIVE"|"OTHER";
  constraints: {property, operator, value, unit?, hardness, origin}[];
  exact_identity?: {definition_id?, definition_digest?, manufacturer?, sku?, revision?};
  scope: {operating_mode?, conditions?, verification_level};
  required_source_claim_ids: ID[]; unresolved: string[];
  authorization: "DISCOVERY_ONLY"|"VERIFIER_ADAPTER_ELIGIBLE"|"BLOCKED";
}
PROPOSED RequirementsValidationResult {
  goal_id: ID; requirements_digest: sha256;
  primary_status: "READY_FOR_MATCHING"|"NEEDS_CLARIFICATION"|"UNSUPPORTED_GOAL"|"REQUIRES_EVIDENCE"|"CONFLICTING_REQUIREMENTS";
  issue_codes: ID[]; affected_requirement_ids: ID[];
  clarification_questions: {question_id, target_ids, options?, free_text_allowed}[];
  prerequisite_evidence: {kind, requirement_ids, identity_scope}[];
  executable_subscope: string[]; unsupported_subscope: string[];
  applicable_catalog_digest?: sha256; decision_trace: ProvenanceRecord[];
}
PROPOSED EducationalHint {
  hint_id: ID; hint_schema_version: string; finding_id?: sha256;
  finding_origin: "GPIO_FINDING"|"GPIO_COVERAGE"|"DEMO_LINK"|"REQUIREMENTS_VALIDATION";
  rule_id?: ID; rule_version?: string; reason_code: ID;
  engineering_status: "PASS"|"FAIL"|"UNKNOWN"|"NOT_APPLICABLE"|"NOT_EVALUATED"|"NO_FINDING";
  subject: {instance_id?, terminal_id?, net_id?, definition_id?};
  originating_requirement_id?: ID; learning_objective_id: ID;
  category: "ERROR"|"CAUSE"|"CONCEPT"|"CLUE"|"REPAIR_CANDIDATE"|"EVIDENCE_REQUEST"|"SCOPED_CONFIRMATION"|"UNSUPPORTED";
  explanation_key: string; locale: "ka-GE"; rendered_text: string;
  evidence: HintEvidenceBinding[]; assumptions: string[];
  missing_coverage: string[]; learner_next_action?: ActionDescriptor;
  repair_class: "VERIFIED_CORRECTION"|"CANDIDATE_ACTION"|"EVIDENCE_REQUEST"|"NONE";
  assist_level: "BEGINNER"|"EXPERT"; hint_stage: 1|2|3;
  catalog_digest?: sha256; snapshot_digest: sha256;
  factset_digest?: sha256; requirement_digest?: sha256;
  validity: "VALID"|"STALE"|"WITHDRAWN";
}
PROPOSED HintEvidenceBinding {
  binding_id: ID; basis: "SOURCE_CLAIM"|"COMPUTED_TOPOLOGY";
  finding_id?: sha256; claim_id?: ID;
  source_document_id?: ID; source_locator?: string;
  source_snapshot_digest?: sha256; topology_net_id?: string;
  source_revision?: string; source_digest?: sha256;
  review_state: "REVIEWED"|"MISSING"|"CONFLICTED"|"STALE";
  claim_scope: string; permitted_claim_keys: string[];
}
PROPOSED EducationalFeedbackReport {
  report_version: string; goal_id?: ID;
  requirements_digest?: sha256; snapshot_digest: sha256;
  catalog_digest: sha256; factset_digest?: sha256;
  verifier_ruleset?: string; link_report_version?: string;
  hints: EducationalHint[];
  coverage_summary: {evaluated_scopes: string[], unknown_scopes: string[], not_evaluated_scopes: string[]};
  suppressed_hint_ids: ID[]; stale_hint_ids: ID[];
  knowledge_base_version: string; localization_version: string;
  authorization_scope: "TEST_ONLY"|"PRODUCTION_REVIEWED";
}
```

**კონტრაქტის invariants:** `HintEvidenceBinding.basis=SOURCE_CLAIM`-ზე `claim_id`, განხილული source locator და scope აუცილებელია; `basis=COMPUTED_TOPOLOGY`-ზე აუცილებელია რეალური `snapshot_digest` და net/terminal anchor, მაგრამ manufacturer claim შეიძლება არ არსებობდეს. `DEMO_LINK`-ისათვის არ უნდა შეიქმნას fake `finding_id` ან fake source `claim_id`.

**უარსაყოფი გაერთიანებები:** `USER_EXPLICIT` ≠ `SOURCE_BACKED`; `CANDIDATE_INFERRED` ≠ `VERIFIED_CAPABILITY`; `COMPONENT_CANDIDATE` ≠ `EXACT_PHYSICAL_TERMINAL`; `engineering_status` ≠ `requirements primary_status`; `source_revision` ≠ `snapshot_digest`. JSON shape-ის შემოწმების შემდეგ ცალკე semantic gate ამოწმებს დამოკიდებულებებს, ერთეულის კონვერტაციას, provenance-ს, და მტკიცების უფლების ფარგლებს.

### 5.3 სრული, თუმცა მხოლოდ კანდიდატი JSON მაგალითი

```json
{
  "schema_version": "intent-h-proposed-0.1",
  "goal_id": "goal-distance-led-001",
  "locale": "ka-GE",
  "original_statement": "მინდა ESP32-ით გავზომო მანძილი და როდესაც ობიექტი 30 სანტიმეტრზე ახლოს იქნება, LED აინთოს.",
  "observable_goal": ["measure_distance", "turn_led_on_when_near"],
  "functional_requirements": [
    {"requirement_id":"req-measure","kind":"MEASUREMENT","observable":"distance","subject_role":"sensor","strength":"MANDATORY","constraint_strength":"HARD","assertion_class":"PARSED_REQUIREMENT","origin":"USER_EXPLICIT","dependencies":[],"support_state":"FUTURE"},
    {"requirement_id":"req-threshold","kind":"CONDITIONAL_BEHAVIOR","observable":"distance_below_threshold","subject_role":"controller","predicate":{"variable":"distance","comparator":"LT","quantity":{"value_decimal_string":"30","unit_ucum_or_SI":"cm","normalized_value":"0.30 m"}},"action":{"target_role":"led","state":"ON"},"strength":"MANDATORY","constraint_strength":"HARD","assertion_class":"PARSED_REQUIREMENT","origin":"USER_EXPLICIT","dependencies":["req-measure","req-led"],"support_state":"FUTURE"},
    {"requirement_id":"req-led","kind":"DIGITAL_OUTPUT","observable":"visible_indicator_on","subject_role":"led","strength":"MANDATORY","constraint_strength":"HARD","assertion_class":"PARSED_REQUIREMENT","origin":"USER_EXPLICIT","dependencies":[],"support_state":"FUTURE"}
  ],
  "hardware_identity_constraints": [{"family":"ESP32","origin":"USER_EXPLICIT","exact_board":"UNRESOLVED"}],
  "candidate_inferences": [{"claim":"compatible distance sensing mechanism may be needed","origin":"CANDIDATE_INFERRED","engineering_trust":"NONE"}],
  "unresolved_ambiguities": [],
  "missing_prerequisites": ["exact_board_identity","sensor_identity","led_drive_circuit","firmware_runtime_observation","electrical_characteristics"],
  "required_capabilities": [
    {"query_id":"cap-distance","requirement_ids":["req-measure"],"target":"COMPONENT_CANDIDATE","capability":"DISTANCE_MEASUREMENT","constraints":[],"required_source_claim_ids":[],"unresolved":["sensor_identity"],"authorization":"DISCOVERY_ONLY"},
    {"query_id":"cap-led","requirement_ids":["req-led"],"target":"COMPONENT_CANDIDATE","capability":"DIGITAL_OUTPUT","constraints":[],"required_source_claim_ids":[],"unresolved":["led_drive_circuit"],"authorization":"DISCOVERY_ONLY"}
  ],
  "supported_verification_scopes": [{"scope":"GPIO direction on already resolved reviewed exact board/terminals","currently_executable":true}],
  "parser_id":"PROPOSED_BOUNDED_GEORGIAN","parser_version":"0.1-candidate",
  "requirements_digest":"sha256:TO_BE_COMPUTED_FROM_CANONICAL_IR",
  "source_decisions": [{"source":"user_text","type":"USER_EXPLICIT"}]
}
```

**სიზუსტის შენიშვნა:** ეს მაგალითი *საილუსტრაციო IR მონაცემია*, არა მიმდინარე Pydantic-ისთვის მზადმყოფი ობიექტი; `sha256:TO_BE_COMPUTED...` არის placeholder, არა ნამდვილი digest და არ შეიძლება ნამდვილ serializer/verifier-ში მისი დაშვება. JSON-ში შენარჩუნებული ყველა მომავალი მიზანი არ ნიშნავს, რომ დღევანდელი დონის GPIO checks უშუალოდ ამ ტექსტიდან სრულდება.

## 6. მინიმალური სისრულე, წინააღმდეგობები და გაურკვევლობა

### 6.1 საწყისი readiness-ის მკაცრი განმარტება

`PROPOSED` პრინციპი: მოთხოვნების სისრულე ყოველთვის **დამოკიდებულია შემდეგ მოქმედებაზე**. კომპონენტთა *კანდიდატების აღმოჩენისთვის* საკმარისია გაზომვადი/დასახასიათებელი ფუნქცია და დომენური კლასის მინიმალური შეზღუდვები; **კონკრეტული ტერმინალის GPIO ვერიფიკაციისთვის** საჭიროა რეალური `CatalogSnapshot`, `CircuitSnapshot`, ზუსტი `TerminalRef`, წყაროზე დამოწმებული fact-set და დამოუკიდებლად დამტკიცებული hash-ები. სრულ firmware + voltage system validation-ს დამატებითი evidence სჭირდება.

| სამუშაო ეტაპი | აუცილებელი წინაპირობა | დაკარგულის შემთხვევაში |
|---|---|---|
| ზოგადი capability discovery | მინიმუმ ერთი გასაგები გაზომვადი/საინჟინრო ფუნქცია, რომელზეც კატალოგის ძიება შეიძლება | `NEEDS_CLARIFICATION` |
| მოთხოვნის შედარება კომპონენტის კანდიდატთან | კანდიდატის ზუსტი identity, მოთხოვნის hard conditions და შესაბამისი source-backed თვისებები | `REQUIRES_EVIDENCE` კონკრეტულ კანდიდატზე |
| ტერმინალის GPIO მიმართულების შემოწმება | რეალური circuit snapshot, resolved physical pin, scoped factset, approved trust pins | გაურკვევლობა ან `UNKNOWN/NOT_EVALUATED` არსებული verifier-იდან; არა ავტომატური PASS |
| ელექტრული safety/voltage | სანდო წყარო/მოდელი, ოპერაციული პირობები, შესაბამისი CORE-001C scope | `NOT_EVALUATED`, როცა ძრავი არ არსებობს; safety claim აკრძალულია |
| firmware behavior | რეალური firmware არტეფაქტი, build/ინსტრუმენტაცია/ტესტის მტკიცებულება და დროითი პირობა | `FUTURE/NOT_VERIFIED`; არა შესრულებული |

**პრიორიტეტის წესი `PROPOSED`:** შეიკრიბოს *ყველა* issue; `primary_status` მხოლოდ UX-ის მარშრუტია. თუ hard-contradiction არსებობს — `CONFLICTING_REQUIREMENTS`; თუ მიზნის აუცილებელი კომპონენტი სისტემის მიღებულ ფუნქციურ დომენს სცდება — `UNSUPPORTED_GOAL`; თუ აუცილებელი სემანტიკური არგუმენტია აკლებული — `NEEDS_CLARIFICATION`; თუ აზრი გასაგებია, მაგრამ ამა თუ იმ კონკრეტულ ქმედებას აკლია სანდო კომპონენტის მონაცემი — `REQUIRES_EVIDENCE`; სხვაგვარად — `READY_FOR_MATCHING`. **გამონაკლისი:** მრავალმიზნიან წინადადებაში ნაწილობრივ მხარდაჭერილი subgoal-ები ცალკე ინახება. სისტემა მათ ჩუმად არ შლის; მომხმარებელმა უნდა დაინახოს, რომ მხოლოდ subset არის შესრულებადი.

### 6.2 ხუთი workflow-ს სტატუსის მაგალითები

| სტატუსი | მაპროვოცირებელი მოვლენა | დასაშვები რეაქცია | აკრძალული რეაქცია |
|---|---|---|---|
| `READY_FOR_MATCHING` | „გაზომე მანძილი და აანთე LED 30 სმ-ზე ახლოს“ — ძიებისთვის საკმარისი როლებია, ნაწილები დაუზუსტებელია | შექმენი **candidate-discovery query**; დარჩენილი წყაროები ცალკე შეამოწმე | გამოაცხადო მზად/უსაფრთხო წრედი |
| `NEEDS_CLARIFICATION` | „სენსორმა 30-ზე LED მართოს“ — ერთეული/რა სიდიდე უცნობია | სთხოვე: „30 რას ნიშნავს — სმ, მმ თუ სხვა?“ | საკუთარი ნებით ჩაწერო 30 სმ |
| `UNSUPPORTED_GOAL` | „დამიმტკიცე, რომ სისტემა რეალურ სამყაროში ნებისმიერ გარემოში მუშაობს“ | ჩამოთვალე დაუმოწმებელი დონის საზღვარი; შესთავაზე შეზღუდული დასაშვები subgoal | გამოიგონო სრული სიმულაცია |
| `REQUIRES_EVIDENCE` | დასახელებული სენსორის უცნობი PCB რევიზია/ელექტრული მახასიათებელი ბლოკავს კონკრეტულ შედარებას | მოითხოვე მწარმოებლის/reviewed მონაცემი და scope | გამოიყენო სხვა HC-SR04-ის შემთხვევითი datasheet როგორც იგივე რევიზია |
| `CONFLICTING_REQUIREMENTS` | „LED უნდა აინთოს 30 სმ-ზე ახლოს და არასოდეს აინთოს 30 სმ-ზე ახლოს“ | აჩვენე ორი კონფლიქტური span, ეძებე დაზუსტება | ერთ-ერთი წესი ჩუმად წაშალო |

**განსხვავება `UNKNOWN`-თან:** `READY_FOR_MATCHING` და სხვ. არის აპლიკაციის workflow; `PASS/FAIL/UNKNOWN/NOT_APPLICABLE` — კონკრეტული engineering rule; `NOT_EVALUATED` — არც გამოთვლილა. მათ შორის ტრანსფორმაცია ერთმნიშვნელოვანი არ არის. `missing_prerequisites` არ უნდა დაიკარგოს.

### 6.3 დამოკიდებულების გრაფი და სამმნიშვნელოვანი მსჯელობა

- Node = `requirement_id` + განსაზღვრული predicate + strength; edge = `depends_on` ან `satisfies_candidate` ან `contradicts`.
- მოთხოვნის სიმართლის/მტკიცების შუალედი: `SUPPORTED`, `REFUTED`, `UNKNOWN`, და ცალკე `NOT_EVALUATED`; არ გამოიყენოთ `UNKNOWN` როგორც false, არც `NOT_EVALUATED` როგორც `UNKNOWN`-ის დასკვნა.
- Hard constraints-ის შეტაკება: `distance < 0.30m → LED_ON` და `distance < 0.30m → LED_OFF` ერთსა და იმავე რეჟიმში/დროით კონტექსტში უნდა დაინიშნოს კონფლიქტად; სხვადასხვა operating mode-ები **შესაძლოა** არ იყოს კონფლიქტი — მოითხოვს კონტექსტის შემოწმებას.
- Units: ჯერ `dimension` და converter; 30 სმ = 0.3 მ, მაგრამ `30 ms` ≠ 30 სმ. მოკლე floating-point tolerance-ის შედარებები არ დაივიწყოთ, თუმცა exact decimal threshold-ის სემანტიკურ ჩაწერაზე SPICE ან SMT არ არის საჭირო.
- სრული SMT (მაგ. [Z3](https://www.microsoft.com/en-us/research/project/z3-3/)) მხოლოდ მაშინ შეირჩევა, როცა მარტივი dependency/constraint matcher ვერ ფარავს კონკრეტულ განმეორებად პრობლემას; ეს არ არის ახლა დასამატებელი კომპონენტი.

### 6.4 ერთი კითხვით გამტარუნარიანობის ამაღლება

დაზუსტების კანდიდატი უნდა ირჩევოდეს **მომდევნო ლეგიტიმური ნაბიჯის გახსნით**, არა დიალოგის გართულებით. ქულა `PROPOSED`: `blocks_next_stage?` → `number_of_branches_resolved` → `risk_of_wrong_silent_assumption` → `user_effort`. მაგალითი: „30-ზე“ ჯერ საზომი, არა არარსებული component SKU; „ESP32“ ხშირად საკმარისია family-level candidate search-ისთვის, მაგრამ კონკრეტული GPIO პინის შემოწმებამდე ზუსტი board SKU აუცილებელია.

## 7. მოთხოვნებიდან კომპონენტთა შესაძლებლობის მოთხოვნამდე: Research I-ის საზღვარი

მხოლოდ `RequiredCapabilityQuery`-ს შეუძლია გადავიდეს მომავალ კომპონენტთა მოძიებაში. განცხადება „ულტრაბგერითი სენსორი მჭირდება“ არ ნიშნავს, რომ ყველა `HC-SR04` ელექტრულად თავსებადია კონკრეტულ ESP32-თან. Query-ს შეუძლია გამოიყენოს `functional_requirement_ids`, `hard_conditions`, `operating_mode`, `identity_scope`, `candidate_rank_preferences` და `source_quality_required`, მაგრამ **ვერ ჩაანაცვლებს** `DeviceDefinition/TerminalDefinition`-ს და manufacturer review-ს.

**სავარაუდო მაგალითი `PROPOSED`:**

```json
{
  "query_id": "q-distance-sensing",
  "requirement_ids": ["req-measure"],
  "target": "COMPONENT_CANDIDATE",
  "capability": "DISTANCE_MEASUREMENT",
  "constraints": [
    {"property":"distance_relation","operator":"CAN_PRODUCE_MEASUREMENT","value":"distance","hardness":"HARD","origin":"USER_EXPLICIT"}
  ],
  "exact_identity": null,
  "scope": {"operating_mode":"UNRESOLVED","verification_level":"CANDIDATE_ONLY"},
  "required_source_claim_ids": [],
  "unresolved": ["sensing_method", "voltage", "interface", "manufacturer_revision"],
  "authorization": "DISCOVERY_ONLY"
}
```

Research I-ის პასუხისმგებლობა: კატალოგში იპოვოს კანდიდატი, დაამყაროს exact identity/revision, შეადაროს ფუნქციური და ელექტრული hard constraints შესაბამის reviewed claims-ს და დააბრუნოს `MATCH_SUPPORTED | MATCH_REFUTED | INSUFFICIENT_EVIDENCE | OUT_OF_SCOPE` — **ეს ეტიკეტები Research H-ის მიერ შეთავაზებულია, მიმდინარე პროგრამის სტატუსები არ არის.** Ranking შეიძლება მოხდეს მხოლოდ მას შემდეგ, რაც hard constraint check-ები ცალ-ცალკეა ნაჩვენები. „ალტერნატივა“ უნდა მიუთითებდეს რომელ მოთხოვნას პასუხობს და რომელს **არ** ამოწმებს.

Research J-ის მხარე: მოთხოვნის/კომპონენტის უკვე განხილული კონკრეტული მასალიდან შესაძლებელია კანდიდატი connection plan-ის შექმნა, მაგრამ `CORE-001A`-ის ფიზიკური netlist და verifier არის საბოლოო ტექნიკური არბიტრი. Firmware binding plan ვერ მიიჩნევა runtime-ის შესრულების მტკიცებულებად.

## 8. საინჟინრო finding → EducationalHint: სრული, გეიტებით დაცული არქიტექტურა

### 8.1 მონაცემთა ნაკადის შემოთავაზებული ფენები

```text
PROPOSED EngineeringIntent / RequirementsValidationResult
          |  მხოლოდ მოთხოვნის კავშირი (არა hardware truth)
          v
[არსებული CORE-001A topology] -> [არსებული DEMO-001 links]
          |                           |
          +--> [არსებული CORE-001B GpioVerificationReport]
                                      |
                         [Finding/Coverage/Link discriminated adapter]
                                      |
                         [snapshot + catalog + factset pin check]
                                      |
                         [reason_code + source claims + policy table]
                                      |
                          [learning objective / hint stage]
                                      |
                          [curated Georgian localization]
                                      |
                             PROPOSED EducationalHint
                                      |
                [source/subject anchor + specific remaining unknowns]
                                      |
                      [learner edit -> NEW snapshot -> recompute]
```

**გარდაუვალი ტექნიკური მოთხოვნა:** `GpioCoverage` და `DemoLinkResult` არ უნდა გააყალბდეს `GpioFinding` ობიექტებად. `finding_origin` არის discriminated union. თუ `link.state = AMBIGUOUS`, მინიშნება უნდა ეყრდნობოდეს link-ის როლს, net-ს და იმ snapshot-ს; `finding_id` უნდა იყოს `null`, არა გამოგონილი hash. თუ `PHYSICAL_CAPABILITY/PASS`, ტექსტი შეირჩევა მხოლოდ ამ კონკრეტული rule-ისა და ფუნქციისთვის; სხვა rule-ების `UNKNOWN` მიმაგრებულია სავალდებულო caveat-ად.

### 8.2 H1/H2/H3 შედარება

| კრიტერიუმი | H1: deterministic rule→template | H2: structured planner | H3: constrained LLM verbalization |
|---|---|---|---|
| წყაროს/მოთხოვნის ტრასირება | მაღალი, მარტივი audit | მაღალი, თუ planner არ ქმნის ახალ claims | უსაფრთხოა მხოლოდ lock-ული claims-ისა და post-validation-ისას |
| Georgian wording | ნაკლებად მრავალფეროვანი, მაგრამ კურირებადი | სიღრმის/ჩარევის უფრო კარგი არჩევა | მრავალფეროვანი; semantic drift-ის რისკი |
| ემპირიული სწავლა | ცალკე უნდა დადასტურდეს | პირობითად პერსპექტიული | ლამაზად დაწერილი ახსნა ≠ უკეთ სწავლა |
| maintenance | rule+text regression | planner policy+text | prompt, მოდელის, ფასის, regression-ის მუდმივი კონტროლი |
| privacy/cost | ლოკალური, დაბალი | ლოკალური, დაბალი/საშუალო | provider ან საკუთარი inference, latency და ხარჯი |
| failure control | აკრძალული/დაუფარავი key ადვილად ჩანს | rule/priority შეცდომა შესაძლებელია | შეიძლება დაუმტკიცებელი რიცხვი, pin, უსაფრთხოების განცხადება შემოიტანოს |
| პირველი არჩევანი | **SELECT FOR BOUNDED TEST** | **CONDITIONAL** | **HOLD** |

### 8.3 „ფაქტების უფლების“ კონტრაქტი

`PROPOSED` მინიშნება იწარმოება შემდეგი დაშვებების თანხვედრისას:

1. finding-ის `snapshot_digest`, `catalog_digest`, `factset_digest`, `ruleset_version` ემთხვევა აქტიურ რედაქტორსა და ავტორიზებულ წყაროს; digest mismatch → ძველი hint **მალევე** `STALE/WITHDRAWN`, არ ვაჩვენოთ როგორც მოქმედი.
2. `reason_code` და `rule_id` ზუსტად არსებობს allowlisted policy-ში; უცნობ კოდზე მხოლოდ სკოპირებული ნეიტრალური დიაგნოსტიკა ან ახსნის არქონა, არავითარი generative fallback hardware claim-ზე.
3. წყაროს `claim_id → source_document_id → locator → revision/digest → review_state` კავშირი მზადაა; მათემატიკის ხასიათი ხსნის მინიმალურ უფლებას. `review_state=CONFLICTED/MISSING` იძლევა evidence request-ს, არა PASSED ფაქტს.
4. `subject.terminal_id` და `instance_id` რეალურად მოდის კომპიუტაციიდან; UI მხოლოდ ვიზუალურ anchor-ს ეძებს, თვითონ ვერ ქმნის fallback pin-ს.
5. შაბლონმა შეიძლება თქვას მხოლოდ წინასწარ განსაზღვრული claim-ები. მაგალითად `OUTPUT_NOT_CAPABLE + board/J2.5` → „GPIO34-ისგან სენსორის Trig-ს გამომავალი მართვის სიგნალი ვერ მიეწოდება ამ შემოწმებული ფუნქციის ფარგლებში“; არ შეუძლია „წრედი დაიწვება“ ან „სხვა ყველა კონტაქტი უსაფრთხოა“.
6. Repairs: `VERIFIED_CORRECTION` მხოლოდ ყველა **დასახელებული** predicate-ის დამოწმებისას; უფრო ხშირად `CANDIDATE_ACTION`, რომელსაც ცალკე გადამოწმება სჭირდება; `EVIDENCE_REQUEST` როცა ფაქტი აკლია. მკაფიოდ განსხვავდება.
7. User action-ის შემდეგ ძველი finding და hint ვერ ინარჩუნებს აქტიურ validity-ს მხოლოდ text/anchor similarity-ს გამო; snapshot იცვლება და სრულდება ხელახალი გამოთვლა.

### 8.4 მტკიცებულების გაჭუჭყიანების განსაკუთრებული რისკები

- **რისკი A — hash-ის „სანდოობა“:** მომხმარებლისგანვე მიღებული expected hash საერთოდ არ ქმნის დამოუკიდებელ trust anchor-ს. Production trust გარედან ავტორიზებული review process-ია.
- **რისკი B — ტექსტური alias:** user ამბობს „GPIO18“, მაგრამ ფიზიკური board revision/terminal ჯერ არ არის გადაწყვეტილი. არ გამოიყენოთ ტექსტური alias პირდაპირ `board/J3.9`-ის დასადგენად.
- **რისკი C — ორმაგი წყარო:** manufacturer GPIO output claim + retailer sensor pinout არ ამტკიცებს მათი signal voltage compatibility-ს.
- **რისკი D — coverage optimism:** `GpioCoverage` ვერ ჩაიწერება `PASS` განშტოებაში; მისთვის `NOT_EVALUATED` უნდა დარჩეს.
- **რისკი E — ქეშირება:** `snapshot_digest` იცვლება ასევე persisted display-label-ის ცვლილებისას; არსებული ბირთვის digest semantics უნდა შენარჩუნდეს. საჭიროებისას hint შეიძლება ხელახლა გენერირდეს და არ გადატანილ იქნას წინა snapshot-ის „მოქმედი“ სტატუსი.
- **რისკი F — წესის ცვლილება:** source claim ამოიწურა ან ალტერნატიული claim დაემატა; version/cache invalidation მოითხოვს source identity+ruleset+policy+localization pin-ების გადაანგარიშებას.

## 9. ქართულენოვანი ახსნის გენერაცია

### 9.1 ლოკალიზაციის შინაარსობრივი წესები

**შაბლონი `PROPOSED`:** `{component_label} / {physical_terminal} უკავშირდება {target_name}-ს. მოთხოვნილი ფუნქციაა {function}. {scope_specific_result}. {remaining_unknowns}. {next_safe_action}.`

- `გაცემული თეორიული განმარტება` და `სისტემის გამოთვლილი დასკვნა` ცალკე წინადადებად/ვიზუალურ ბლოკად; თეორია არ უნდა „გადასდოს“ სანდოობას დაუმოწმებელ კონტაქტს.
- „ამ კონტაქტზე digital output-ის შესაძლებლობა არ დასტურდება“ განსხვავდება „output შეუძლებელია“. პირველის გამოყენება missing evidence-ისას; მეორის — მხოლოდ შეზღუდულ განხილულ ფაქტზე `FAIL/OUTPUT_NOT_CAPABLE`.
- სტატუსი `PASS`: „დადასტურებულია **მხოლოდ** ამ ფუნქციის მხარდაჭერა მითითებულ GPIO კონტაქტზე.“; `UNKNOWN`: „ამ საკითხის გადასაწყვეტად მონაცემი არ არის საკმარისი.“; `NOT_EVALUATED`: „ამ ტიპის შემოწმება არ შესრულებულა.“
- ქართულ სიტყვიერად გასაგებ ტერმინებს ახლდეს ზუსტი პროფესიული მეტსახელი: „შემავალი (GPIO input)“ და „გამომავალი (GPIO output)“. `Trig`, `Echo`, `GPIO34`, `J2.5` არ ითარგმნება ან არ გადაიწერება.
- ქარხნული ნორმის/რიცხვის დამატება შაბლონის მიერ აკრძალულია, თუ შესაბამისი `claim_id`, condition და locator არ არსებობს.
- UX-ში მთავარი შეტყობინება არის მიზეზი და სასწავლო არჩევანი; სრული წყარო, review scope და დანარჩენი ტექნიკური დეტალები საჭიროების შემთხვევაში იშლება („Show evidence“).

### 9.2 H1 შაბლონის სამი დასაშვები მაკეტი

`OUTPUT_NOT_CAPABLE` / beginner: „სენსორის Trig-ს მიკროკონტროლერისგან გამომავალი სიგნალი სჭირდება. ამ კავშირში გამოყენებული board/J2.5 დოკუმენტურად GPIO34-ია, რომელსაც ჩვეულებრივი GPIO გამომავალი ფუნქცია არ აქვს. გადაამოწმე სხვა ფიზიკური კონტაქტის არჩევა. **ეს დასკვნა არ ამოწმებს ძაბვას ან firmware-ს.**“

`CAPABILITY_CONFIRMED` / scoped: „board/J3.9 დადასტურებულ პროფილში GPIO18-ს უკავშირდება. მოთხოვნილი GPIO_OUT ფუნქციის შესაძლებლობის შემოწმება წარმატებით დასრულდა. **board-ის ხელმისაწვდომობა, მიმდინარე firmware კონფიგურაცია და ელექტრული თავსებადობა ჯერ არ დადასტურებულა.**“

`EVIDENCE_MISSING` / evidence: „ამ ნაწილზე საჭირო ელექტრული თვისება ან ზუსტი რევიზია განხილულ წყაროებში არ არის საკმარისად დადასტურებული. წარმოადგინე კონკრეტული მწარმოებლის დოკუმენტი/რევიზია; ამ ეტაპზე უსაფრთხოების დასკვნა არ არსებობს.“

## 10. მინიშნებების არჩევისა და პრიორიტეტიზაციის პოლიტიკა

`PROPOSED` დასაშვები ჩარევები: შეცდომის იდენტიფიკაცია, მიზეზი, ერთი კონცეფციის შეხსენება, თანდათანობითი მინიშნება, source-backed შემდგომი მოქმედება, რეფლექსიური კითხვა, შეზღუდული დადებითი დადასტურება, evidence request, unsupported disclosure. მიზანი არ არის ერთდროულად ყველას ჩვენება.

**დასაშვები პრიორიტეტული რიგი:** (1) არსებული გამოთვლით მკაფიო `FAIL` იმავე აქტიურ მოსწავლურ მიზანზე; (2) არასწორი/ამბივალენტური topology, რომელიც ვერიფიკაციას ბლოკავს; (3) კრიტიკული დაკარგული evidence; (4) `UNKNOWN` კონფიგურაცია; (5) კონკრეტული `PASS`-ის მოკლე კონფირმაცია. ეს არის კვლევითი UX policy და არა რისკის/უსაფრთხოების უნივერსალური ალგორითმი: თუ მომავალი დამოუკიდებელი electrical verifier ავლენს დადასტურებულ სახიფათო პირობებს, safety precedence საჭიროა **ცალკე ავტორიზებული წესით**.

`rank_tuple = (evaluable_and_actionable, current_goal_relevance, verified_severity, dependency_blocking, novelty, stable_subject_id)` — ლექსიკოგრაფიული, გამეორებადი, ბოლო tie-break ID-ით. არ დავამატოთ არადასაბუთებული „პრობლემის მოგვარების ალბათობის“ ყალბი ქულა.

**როდის გამოჩნდეს:** ხელახალი გამოთვლისა და fingerprint-ის დამთხვევის შემდეგ; UI feedback არა შუა რედაქტირების გარდამავალ snapshot-ზე.  **როდის გაქრეს:** სხვა snapshot, ახალი evidence, ახალი rule version ან მოთხოვნის უარყოფა მას stale-ად აქცევს; შესაბამისი rule-ის ახალი `PASS` ან შეცვლილი link ქმნის ახალ, უფრო ვიწრო hint-ს.  **რამდენი:** საწყისი UX ჰიპოთეზა — ერთი ძირითადი anchor-ზე, სხვა issue-ების მოკლე count/inspect; რაოდენობა user study-ში გადასამოწმებელია.

**საფეხურები (opt-in):**

- `BEGINNER / stage1`: რომელ კავშირს ეხება პრობლემა და რა ფუნქციაა საჭირო; არ უთხრათ ყველა პასუხი დაუყოვნებლივ.
- `BEGINNER / stage2`: მიზეზი და ერთი კონცეპტუალური განმარტება („input-only“ vs „output“).
- `BEGINNER / stage3`: **თუ source-backed** შემოთავაზება, „ცადე J3.9/GPIO18-ის mapping და ხელახლა შეამოწმე“ — ეს არ არის სრული უსაფრთხოების დამტკიცება.
- `EXPERT`: `reason_code`, exact physical ref, rule/snapshot/source pin, უცნობი coverage და მოკლე action; ვერიფიკატორის ფაქტები იგივე რჩება.

Repeated-error შემთხვევა: **ერთი და იმავე rule/subject/error-ის განმეორება** შეგვიძლია დავინახოთ ვიწრო session-history-დან; არ არის საფუძველი ADHD-ის, ნიჭის ან კომპეტენციის ფსიქოლოგიური პროფილის დასადგენად. შესაძლო ეტაპობრივი კონცეპტუალური კითხვა შესადარებელია უცვლელი „სწორ პინზე გადაიტანე“ პასუხთან. დახმარების არხის არჩევა მოსწავლემ უნდა აკონტროლოს.

## 11. საგანმანათლებლო ვალიდობა, დაუსაბუთებელი ნდობა და სასწავლო რისკები

1. **წარმატებული შეკეთება ≠ სწავლა.** მომხმარებელმა შეიძლება უბრალოდ დამახსოვრებული J3.9 გადაიღოს. უნდა გაიზომოს მიზეზის ახსნა და transfer განსხვავებულ, უცნობ GPIO შემთხვევაზე.
2. **უარყოფითი/დადებითი feedback-ის შეცდომა:** ფაქტის ქულა შეიძლება სწორია, ტექსტმა კი დაამატოს დაუმტკიცებელი „კავშირის უსაფრთხოება“ — ცალკე factual consistency gate აუცილებელია.
3. **დაუფარავი მდგომარეობები:** `ACTIVE_CONFIG_UNKNOWN`, `ELECTRICAL_CHECK_DELEGATED`, source revision და board availability უნდა გამოჩნდეს მაშინაც, როცა direction-ის PASS არსებობს.
4. **კოგნიტური დატვირთვა:** ზედმეტი ტექნიკური მონაცემი, დიდი popover და გამუდმებული შეტყობინებები სწავლისთვის არასასარგებლო შეიძლება იყოს; progressive disclosure არის შესამოწმებელი დიზაინი.
5. **გადაჭარბებული დახმარება:** სრული repair-ის დაუყოვნებლივ გამჟღავნებამ შეიძლება გააუმჯობესოს completion speed და გააუარესოს transfer; randomize hint-depth და გამოყავით self-explanation condition.
6. **ცრუ პერსონალიზაცია:** მომხმარებლის 2–3 შეცდომიდან competence model-ის გამოყვანა არაა სანდო; თავიდან მხოლოდ user-controlled Beginner/Expert და stage.
7. **კონფლიქტური წყაროები:** როდესაც evidence იცვლება, ძველ დადებით მინიშნებაზე დარჩენილი „მწვანე“ label არღვევს engineering trust-ს. არ შეიძლება `PASS` ქეშის უხმო დატოვება.
8. **ტესტის ეკოლოგიური ვალიდობა:** წყაროზე მიბმული GPIO სავარჯიშოები არ ამტკიცებს კომპლექსური რეალური პურის დაფის/კომპონენტის აწყობის შედეგს. მცირე პილოტი შეიძლება იყოს მხოლოდ exploratory.

**სასწავლო კვლევის ვარაუდები** ეყრდნობა Shute (2008), Hattie–Timperley (2007), Chi et al. (1994), VanLehn (2011), Mitrovic et al. (2003), Butler (2010), მაგრამ INVENTOR-ისთვის ეს მხოლოდ ცდების გამართლებაა. დამატებითი 2026 წლის კრიტიკული მიმოხილვა მიუთითებს, რომ hints/help seeking ზოგიერთ შემთხვევაში ეხმარება სწავლას, მაგრამ ეფექტი კონტექსტზეა დამოკიდებული: [Aleven et al., 2026 — *Help Helps, But Only So Much*](https://www.sciencedirect.com/science/article/pii/S1560429226004178). არ გადავიტანოთ იქაური შედეგები ავტომატურად კონკრეტულ ქართულ აპზე.

## 12. რვა სამუშაო მაგალითი: H01–H08

### H01 — არასწორი GPIO მიმართულება (`REPO-OBSERVED` შესრულების fixture)

- **Engineering input:** `board/J2.5 → sensor/Trig`; მოთხოვნა `TRIG_OUTPUT / GPIO_OUT`; `J2.5` დოკუმენტურ პროფილში `GPIO34`-ია. Echo-ს არსებობა/სხვა კავშირები ამ finding-ის წინაპირობა არ არის.
- **გამოთვლა:** `compute_nets` ადგენს კონკრეტულ net-ს; bridge-ი პოულობს ერთ board terminal-ს; `verify_gpio_requirements` კითხულობს trusted mapping/სილიკონის capability-ს.
- **დაფიქსირებული შედეგი:** `PHYSICAL_CAPABILITY → FAIL / OUTPUT_NOT_CAPABLE`; ცალკე `PIN_MAPPING/PASS`; სხვა წესები შეიძლება `UNKNOWN/NOT_EVALUATED` იყოს. წყაროები: [CORE-001B ledger](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md), Espressif official board guide და pinned ESP-IDF mask. ეს არის test-scope შედეგი.
- **ნებადართული მტკიცება:** ამ ზუსტ პროფილში GPIO34 არ აკმაყოფილებს ჩვეულებრივ digital output მოთხოვნას; პრობლემა ეხება **Trig-ის მართვის შესაძლებლობას**, არა მთელ სისტემას.
- **აკრძალულია:** „Echo უსაფრთხოა“, „ძაბვები თავსებადია“, „კომპონენტი დაზიანდება“, „firmware ფუნქციონირებს“.
- **სავარაუდო მინიშნება:** „Trig-ს გამომავალი სიგნალი სჭირდება. board/J2.5 ასოცირებულია GPIO34-თან, რომელიც ამ ფუნქციას ვერ ასრულებს. შეარჩიე გამომავალი ფუნქციის მხარდამჭერი ფიზიკური კონტაქტის კანდიდატი და ხელახლა გადაამოწმე.“
- **შემდეგი მოქმედება / მოსალოდნელი update:** მოსწავლე გადააერთებს Trig-ს `board/J3.9`-ზე. ახალი snapshot ქმნის ახალ finding-ს; ძველი FAIL stale-დება; H02-ის შეზღუდული PASS შეიძლება გაჩნდეს.

### H02 — მიმართულების დადასტურებული კორექცია (`REPO-OBSERVED` fixture)

- **Engineering input:** `board/J3.9 → sensor/Trig`, როლი `GPIO_OUT` (პარალელურად `board/J3.8 → sensor/Echo`, როლი `GPIO_IN`).
- **გამოთვლა:** იგივე bridge/verifier ახალ net-ზე; `J3.9→GPIO18`; `J3.8→GPIO19`; შესაბამისი reviewer-reviewed source facts.
- **შედეგი:** `PHYSICAL_CAPABILITY → PASS/CAPABILITY_CONFIRMED` თითოეულ შესაბამის ფუნქციაზე; `BOARD_AVAILABILITY → UNKNOWN/EVIDENCE_MISSING`, `ACTIVE_CONFIGURATION → UNKNOWN/ACTIVE_CONFIG_UNKNOWN`, electrical `NOT_EVALUATED/ELECTRICAL_CHECK_DELEGATED`. მიუთითოს კონკრეტული `rule_id`.
- **საჭირო evidence:** J3.9/J3.8 board mapping და სილიკონის GPIO capability; firmware/voltage/board-resource დადგენას დამატებითი წყაროები სჭირდება.
- **ნებადართული:** მიმართულების შემოწმების **შეზღუდული** დადებითი შედეგი. **აკრძალული:** „ეს წრედი უკვე სწორია/უსაფრთხოა“.
- **მინიშნება:** „GPIO18-ის ამ კონტაქტზე გამომავალი ფუნქციის შესაძლებლობა დადასტურდა. დანარჩენი პირობები ჯერ არ არის შემოწმებული: board availability, firmware, ელექტრული დონეები.“
- **შემდეგი მოქმედება / update:** შეიძლება გაიხსნას წყაროს დეტალები; სხვა net-ზე გადასვლა წინა confirmation-ს stale-ად აქცევს. არაფერია წინასწარ დამტკიცებული.

### H03 — კომპონენტის ელ. მახასიათებლების ან რევიზიის გაურკვევლობა (`PROPOSED` სცენარი)

- **Engineering input:** მომხმარებელი ასახელებს HC-SR04 ოჯახს ან retailer #3942-ს, მაგრამ ფიზიკური PCB რევიზია და საკმარისი ელექტრული source არ არსებობს.
- **გამოთვლა:** present state = `SOURCE_EVIDENCE_MISSING` ან voltage-engine-ის `NOT_EVALUATED`; **არ არის** ახალი electrical verifier-ის შესრულება.
- **შედეგი:** `UNKNOWN` მხოლოდ მაშინ, თუ ავტორიზებულმა შესაბამისმა rule-მა რეალურად დააბრუნა UNKNOWN; სხვა შემთხვევაში `NOT_EVALUATED`/`REQUIRES_EVIDENCE` შესაბამისი ფენის მიხედვით.
- **საჭირო:** ზუსტი მწარმოებელი, revision, data sheet, ელექტრული output/input პარამეტრები და პირობები; retailer SKU არ ამტკიცებს OEM-ს.
- **ნებადართული:** „ელექტრული თავსებადობის დასასკვნელად მონაცემი არ არის საკმარისი“; **აკრძალული:** „5V Echo უსაფრთხოა GPIO19-ზე“ ან გამოგონილი მაქსიმალური ზღვარი.
- **მინიშნება:** „ამ კონკრეტულ სენსორზე ელექტრული დონის მტკიცებულება არ არის მიღებული. გადაამოწმე მისი ზუსტი მოდელი და მწარმოებლის დოკუმენტაცია; GPIO direction-ის შედეგი აქ უსაფრთხოებას არ განსაზღვრავს.“
- **შემდეგი მოქმედება/update:** წარმოდგენილი დოკუმენტი მხოლოდ review-ის შემდეგ შეიძლება იქცეს `claim_id`-ად; მანამდე verdict არ იცვლება.

### H04 — ორაზროვანი ქსელი (`REPO-OBSERVED` bridge-ის მდგომარეობა)

- **Engineering input:** `sensor/Trig`-ის ერთ net-ზე ორი board GPIO კონტაქტია, ან `Trig/Echo` ერთმანეთს იზიარებენ.
- **გამოთვლა:** `compute_nets` + `demo_bridge._resolve_link`; შესაძლო მდგომარეობები `AMBIGUOUS` ან `SHARED_SIGNAL_NET`.
- **შედეგი:** `DemoLinkResult`-ს აქვს role, `sensor_terminal`, `net_id`, `state`; ვერ შეიქმნება თვითნებურად შერჩეულ ერთ პინზე GPIO finding.
- **საჭირო evidence:** თვითონ topology snapshot; არ არის საჭირო გამომგონილი device datasheet, რომ ვთქვათ „ორი პინი ამ net-ზე ჩანს“.
- **ნებადართული:** „Trig-ის კავშირს ერთმნიშვნელოვანი board GPIO არ აქვს“; **აკრძალული:** „მარჯვენა GPIO სავარაუდოდ სწორია“.
- **მინიშნება:** „Trig-ის მავთული ერთზე მეტ board GPIO კონტაქტთან აღმოჩნდა. გამოყავი ან შეასწორე კავშირი ისე, რომ შემოწმებას ერთი კონკრეტული კონტაქტი ჰქონდეს.“
- **შემდეგი მოქმედება/update:** მოსწავლე ცვლის topology-ს; ახალი `CONNECTED_UNIQUE` მდგომარეობის შემდეგ შეიძლება ჩატარდეს GPIO checks; ძველი ambiguity შეტყობინება ქრება.

### H05 — 30 სმ threshold და LED, მაგრამ firmware არ არის გაშვებული (`PROPOSED` intent)

- **Engineering input:** მომხმარებლის წინადადება ამბობს `distance < 30 cm → LED_ON`.
- **გამოთვლა:** პარსერს შეუძლია შეინარჩუნოს `condition + action`; დღეისთვის არსებული DEMO-001 არ ქმნის/აკომპილირებს/ასრულებს firmware-ს.
- **შედეგი:** ფუნქციური მოთხოვნა არის `PARSED_REQUIREMENT`, firmware-სთვის `FUTURE / NOT_VERIFIED`, GPIO direction მხოლოდ შესაბამისი რეალური terminal/net-ის არსებობისას.
- **საჭირო evidence:** პროგრამული ლოგიკა, pin binding, build შედეგი, runtime/measurement test, მოქმედების დროული და hysteresis semantics საჭიროების მიხედვით.
- **ნებადართული:** „ასეთი ქცევაა მოთხოვნილი“; **აკრძალული:** „LED 30 სმ-ზე ნამდვილად ჩაირთვება“, „კოდი დატესტილია“.
- **მინიშნება:** „აღწერილია პირობა: მანძილი 30 სმ-ზე ნაკლებია → LED ჩაირთოს. ამჟამინდელმა შემოწმებამ ეს ლოგიკა firmware-ში არ შეასრულა; მხარდაჭერილია მხოლოდ ცალკეული GPIO შესაძლებლობის დიაგნოსტიკა.“
- **შემდეგი მოქმედება/update:** user შეუძლია მოთხოვნა დააზუსტოს ან კომპონენტთა კანდიდატები მოიძიოს; firmware verdict მხოლოდ ახალი ავტორიზებული მოდულის შემდეგ გამოჩნდება.

### H06 — ალტერნატიული კომპონენტის შეთავაზება (`PROPOSED`, არა მიმდინარე ფუნქცია)

- **Engineering input:** კონკრეტული სენსორი დამოუკიდებლად შემოწმებული hard requirement-ისთვის შეუფერებელია; მაგალითად, მოთხოვნილ ფუნქციურ კლასს არ უჭერს მხარს.
- **გამოთვლა:** Research I-ის future matcher source-backed refusal-ს და candidate comparison-ს აწარმოებს; Research H მხოლოდ explanation interface-ს განსაზღვრავს.
- **შედეგი:** `MATCH_REFUTED` მოთხოვნის კონკრეტულ property-ზე; candidate `MATCH_SUPPORTED` მხოლოდ მის ფარგლებზე ან `INSUFFICIENT_EVIDENCE`. ეს სტატუსები **ჯერ არსადაა განხორციელებული**.
- **საჭირო evidence:** ორივე exact SKU/revision, properties, conditions, licensing/admission, და ყველას claim locator.
- **ნებადართული:** „კანდიდატი X უკეთ შეესაბამება მოთხოვნა R-ის ამ დადასტურებულ ფუნქციურ პირობას“ მხოლოდ შესაბამისი წყაროებით; **აკრძალული:** „X აუცილებლად იმუშავებს ESP32-თან“.
- **მინიშნება:** „ამ ნაწილს აკლია მოთხოვნა R-ის დასაკმაყოფილებლად საჭირო დადასტურებული თვისება. არსებობს შესამოწმებელი ალტერნატივა; ჯერ გადაამოწმე მისი interface, ძაბვის პირობები და revision.“
- **შემდეგი მოქმედება/update:** მხოლოდ candidate/review-ის არჩევის შემდეგ ჩნდება რეალური CORE snapshot-ის დასაშვები ახალი instance.

### H07 — მტკიცებულების წყარო შეიცვალა (`PROPOSED` source-management შემთხვევა)

- **Engineering input:** წინა `PASS` ეფუძნებოდა `source_rev_A`-ს, რომელიც შეიცვალა ან გაუქმდა.
- **გამოთვლა:** active trusted source pin/claim review ≠ old source revision; H-ის cache validator ქმნის `STALE` მდგომარეობას, არ აცხადებს ახალ GPIO შედეგს.
- **შედეგი:** ძველი `PASS` მინიშნება უნდა ამოვიდეს მიმდინარე ხედიდან. ახალი verifier snapshot ან fresh source review მხოლოდ შემდეგ შეიძლება.
- **საჭირო evidence:** publisher revision, source bytes/digest, review trail, affected claims, factset/release update.
- **ნებადართული:** „ძველი წყაროს საფუძველზე გაცემული დადასტურება აღარ არის აქტუალური“; **აკრძალული:** „ახალი წყარო აუცილებლად უარყოფს შესაძლებლობას“.
- **მინიშნება:** „ამ დასკვნის წყარო განახლდა. წინა პოზიტიური შეტყობინება შეჩერებულია, სანამ მონაცემი ხელახლა არ განიხილება.“
- **შემდეგი მოქმედება/update:** independent fact review + immutable pin + ახალი შეფასება; მხოლოდ ამის შემდეგ შეიძლება ახალი scoped PASS.

### H08 — ერთი ტიპის შეცდომის გამეორება (`PROPOSED` სასწავლო ექსპერიმენტი)

- **Engineering input:** მოსწავლე ზედიზედ ორჯერ აერთიანებს input-only GPIO-სა და `GPIO_OUT` მოთხოვნას, სხვადასხვა snapshot-ში.
- **გამოთვლა:** დადასტურებულია მხოლოდ ერთი `reason_code` კლასის განმეორება იმავე ან სხვა ფიზიკურ კონტაქტზე; არ დგინდება მოტივაცია/უნარი.
- **შედეგი:** თითოეული შეცდომის საკუთარი computed `FAIL`, საკუთარი `snapshot_digest` და ახალი `finding_id`; განათლების ფენა ამოიცნობს განმეორებით **სასწავლო მოვლენის სახეს**, არა იგივე ობიექტს.
- **საჭირო evidence:** user-approved მოკლევადიანი session error history; rule binding და immutable snapshots.
- **ნებადართული:** „ეს input/output შეუსაბამობა მეორდება ამ სესიაში“; **აკრძალული:** „მოსწავლე სუსტია/არ სწავლობს/აქვს დიაგნოზი“.
- **მინიშნება:** „რომელი განსხვავებაა GPIO input-სა და GPIO output-ს შორის? დაფიქრდი, Trig რომელ მათგანს მოითხოვს; სურვილის შემთხვევაში ნახე შემდეგი მინიშნება.“
- **შემდეგი მოქმედება/update:** ახალი განზრახვის/პინის დამოუკიდებლად შემოწმება, კითხვაზე პასუხი/transfer ტესტი; hint depth ცვლის მხოლოდ pedagogy-ს, არა საინჟინრო fact-ს.

### 12.9 სრული თანმიმდევრული კვალი (საერთო fixture)

```text
ქართული ტექსტი: „მინდა ESP32-ით გავზომო მანძილი და როდესაც ობიექტი
               30 სანტიმეტრზე ახლოს იქნება, LED აინთოს.“
  ↓
PROPOSED parsed intent: measure(distance); threshold(distance, <, 0.30m);
                        led(ON); controller_family=ESP32;
                        firmware/sensor/exact board identity ჯერ უცნობია
  ↓
PROPOSED capability queries: distance_sensor_candidate; digital_output_candidate;
  [Future Research I matcher: source-backed exact identity & conditions]
  ↓
[Future synthesis / user wiring: requires actual physical terminal connections]
  ↓
EXISTING CORE-001A CircuitSnapshot: board/J2.5 — sensor/Trig;
  board/J3.8 — sensor/Echo  [ეს ბოლო ეტაპი user wiring/fixture-იდან მოდის,
   თავისუფალი ტექსტი თვითონ არ ადგენს J2.5-ს]
  ↓
EXISTING DEMO-001: link(Trig)=CONNECTED_UNIQUE / board/J2.5;
                    link(Echo)=CONNECTED_UNIQUE / board/J3.8
  ↓
EXISTING CORE-001B: req=TRIG_OUTPUT; PHYSICAL_CAPABILITY;
                    FAIL/OUTPUT_NOT_CAPABLE; scope=GPIO34 OUTPUT
  ↓
PROPOSED binding: finding_id_from_actual_report + snapshot_digest +
                  board/J2.5 + reason_code + reviewed source claim ids
  ↓
PROPOSED Georgian hint: „GPIO34 ამ პროფილში ჩვეულებრივ GPIO_OUT-ს არ
                 უჭერს მხარს; Trig-ის მართვის მოთხოვნა არ სრულდება.
                 გადაამოწმე გამომავალი ფუნქციის მქონე სხვა კონტაქტი.
                 ძაბვა და firmware არ შემოწმებულა.“
  ↓
მოსწავლე ცვლის ფიზიკურ კონტაქტს: board/J3.9 — sensor/Trig
  ↓
NEW CORE snapshot + DEMO bridge + GPIO verifier:
                  PHYSICAL_CAPABILITY PASS/CAPABILITY_CONFIRMED on GPIO18
                  BOARD_AVAILABILITY UNKNOWN
                  ACTIVE_CONFIGURATION UNKNOWN
                  ELECTRICAL_COMPATIBILITY NOT_EVALUATED
  ↓
PROPOSED updated hint: „მხოლოდ მოთხოვნილი GPIO გამომავალი ფუნქციის
                   შესაძლებლობა დადასტურდა; დანარჩენი პირობები უცნობია.“
```

**ზუსტი ატრიბუცია:** კონკრეტული `finding_id`/`snapshot_digest` სრული 64-ნიშნა მნიშვნელობები აქ **არ მომიგონია**. ისინი აუცილებლად მოდის ყოველ ჯერზე უშუალოდ არსებული executable report-იდან. ზემოთ ნაჩვენები ორი verifier-result ქცევა დაფიქსირებულია მიმდინარე რეპოზიტორიის acceptance tests-ში და შესაბამის შესრულების ანგარიშში; ამ კვლევის ფარგლებში კოდი ლოკალურად არ გამიშვია.

## 13. არქიტექტურების A/B/C საბოლოო შედარება

| განზომილება | A — deterministic parsing + templates | B — schema-LLM + validator + curated hints | C — hybrid parser + planner + optional bounded wording |
|---|---|---|---|
| საინჟინრო სიზუსტის გარანტია | მხოლოდ deterministic validator/verifier, მცირე failure surface | იგივე verifier საჭიროა; LLM output ვერ ქმნის ახალ ფაქტს | იგივე, პლუს planner-policy ტესტები |
| ქართული პარაფრაზები | შეზღუდული; უცნობი სიტყვების მაღალი abstention | სავარაუდოდ უფრო ფართო, მაგრამ რეალური benchmark არ გვაქვს | კონტროლირებადი default + wider fallback |
| reproducibility | მაღალი კონკრეტულ input/grammar version-ზე | temperature=0-ც არ იძლევა სრული რეპროდუქციის გარანტიას | საბოლოო deterministic gate; parser შესაძლოა არადეტერმინისტული |
| missing/contradiction detection | წესები და უცნობი სლოტები გამჭვირვალეა | semantic insertion/omission საფრთხე | დამოუკიდებელი abstention/clarification gate |
| CORE-001A/B integration | მხოლოდ თხელი adapter; ყველაზე მცირე საზღვარი | parser-ის ცალკე sandbox აუცილებელია | planner ვრცელდება მხოლოდ requirement/hint დონეზე |
| maintenance | ქართული ლექსიკონის/შაბლონების მუდმივი განახლება | schema+prompt+model version+cost | ყველაზე მეტი კოდის/პოლიტიკის ზედაპირი |
| API/latency | ლოკალურად მცირე | provider ან self-host; თითო request ხარჯი | fallback-ზე დამოკიდებული |
| privacy | მომხმარებლის ტექსტი შეიძლება დარჩეს ადგილობრივ გარემოში | provider-ზე გადაცემა ცალკე თანხმობას/პოლიტიკას მოითხოვს | local-first შესაძლებელია |
| სხვადასხვა MCU/სენსორი | დომენის წესების გამიჯვნა, ფაქტები გარეთ | language generalization შესაძლოა უკეთესი, domain correctness არა | სწორი adapter-ის შემთხვევაში გაფართოებადი |
| proprietary lock-in | დაბალი | მაღალი თუ კონკრეტული provider-ის schema/prompt-ზე მიბმულია | საშუალო/დაბალი თუ fallback არასავალდებულოა |
| კვლევითი არჩევანი | **FIRST TEST** | **COMPARE ONLY** | **CONDITIONAL NEXT STEP** |

**არ უნდა შეირჩეს** agent framework, სრული knowledge graph, თვითგანვითარებადი „student model“, ავტომატური general circuit generator ან სერვისის ფასიანი inference — ამ კვლევამ მათთვის აუცილებელი საჭიროება ვერ დაადასტურა.

## 14. ფიქსირებული ბენჩმარკი და დამოუკიდებელი oracle-ები

### 14.1 ქართული intent set: `GEO-INTENT-H-v0.1` (36 ხელით შედგენილი fixture)

ეს ნაკრები არის **კვლევაში შემუშავებული სამომავლო ტესტი**, არა შესრულებული ტესტები. `R=READY_FOR_MATCHING`, `N=NEEDS_CLARIFICATION`, `U=UNSUPPORTED_GOAL`, `E=REQUIRES_EVIDENCE`, `C=CONFLICTING_REQUIREMENTS`. სვეტი „gold“ გულისხმობს **მომდევნო ლეგიტიმურ ნაბიჯს** და არა მთელი წრედის სისწორეს. `R` მხოლოდ candidate discovery-ს ხსნის. სადაც თანმხლები არამზადყოფნა არსებობს, ის `secondary issue`-ში სავალდებულოა.

| ID | ქართული შესატანი | Gold: მიღებული სემანტიკა / შემდეგი ნაბიჯის სტატუსი | განსაკუთრებული ნეგატიური კონტროლი |
|---|---|---|---|
| I01 | „მინდა ESP32-ით გავზომო მანძილი და როდესაც ობიექტი 30 სანტიმეტრზე ახლოს იქნება, LED აინთოს.“ | `measure distance; distance < 0.30 m → LED_ON; family ESP32; R`; firmware/voltage future | არ შეიტანოს თვითნებური GPIO ან ზუსტი სენსორი |
| I02 | „ესპ32-ზე 30 სმ-ს რომ ჩამოსცდება დისტანცია, ნათურა აანთე.“ | `distance < 0.30 m → LED_ON; R` | „ჩამოსცდება“ არ გახდეს `>` |
| I03 | „ობიექტი 0.3 მეტრზე ახლოსაა? მაშინ დიოდი ჩართე.“ | `distance < 0.3 m → LED_ON; R` | `0.3 m` არ გახდეს `3 m` |
| I04 | „მინდა LED ჩაირთოს, თუკი მანძილი 300 მილიმეტრზე ნაკლებია.“ | `distance < 0.300 m → LED_ON; R` | mm→m ზომის ზუსტი გადაყვანა |
| I05 | „როცა მანძილი 30 სმ ან ნაკლებია, LED ჩართე.“ | `distance <= 0.30 m → LED_ON; R` | `<`-სა და `<=`-ს შორის სხვაობა |
| I06 | „თუ მანძილი 30 სანტიმეტრზე მეტია ან ტოლი, დიოდი გაანათე.“ | `distance >= 0.30 m → LED_ON; R` | არ შეცვალოს comparator `<`-ით |
| I07 | „ობიექტი 30 სმ-ზე შორსაა — მაშინ LED აანთე.“ | `distance > 0.30 m → LED_ON; R` | „შორს“ ≠ „ახლოს“ |
| I08 | „30 სმ-ზე ახლოს თუ მოვა, LED არ აანთო.“ | `distance < 0.30 m → NOT_LED_ON; R` | negation არ დაიკარგოს; OFF semantics დასაზუსტებელია თუ stateful სისტემა |
| I09 | „თუ ოთახში ტემპერატურა 25 °C-ს გადააჭარბებს, ვენტილატორი ჩართე.“ | `temp > 25°C → FAN_ON; R`; ფუნქციური candidate matching, ამჟამად GPIO demo-დან გარეთ | არ წარმოაჩინოს fan-current/firmware VERIFIED |
| I10 | „სიბნელეში ნათურა ავტომატურად უნდა ჩაირთოს.“ | `ambient_light_low → LIGHT_ON; R`; qualitative threshold unresolved, discovery შესაძლებელია | არ გამოიგონოს Lux threshold |
| I11 | „სონარმა 20 სმ-ზე ახლოს რამე რომ დაინახოს, ბზუილი გააკეთოს.“ | `distance < 0.20 m → BUZZER_ON; R` | „სონარი“ ≠ exact SKU |
| I12 | „ESP32-ით თუ 30-ზე ჩამოვა, LED ჩართე.“ | `N`; აკლია სიდიდე და ერთეული | არ დააპროექტოს 30 სმ |
| I13 | „მინდა სენსორი და LED.“ | `N`; observable condition/behavior უცნობია | არ შექმნას თვითნებური ქცევა |
| I14 | „დამიმუშავოს მონაცემი კარგ ხარისხში.“ | `N`; დაუზუსტებელი measurable objective | „კარგი“ არ იქცეს precision/accuracy ციფრად |
| I15 | „სენსორი 30-ს აჩვენებს, მერე რა?“ | `N`; action და unit/variable უცნობია | არ მიაწეროს LED action |
| I16 | „როცა ახლოს მოვა, რაღაც მოხდეს.“ | `N`; target/action არაა მითითებული | არ გამოიგონოს buzzer ან LED |
| I17 | „Trig GPIO34-ზე შევაერთე, შემიმოწმე.“ | `N` exact board/physical terminal და current net/snapshot გადასამოწმებლად; user assertion ინახება | სიტყვა `GPIO34` არ უდრის ფიზიკურ `J2.5`-ს |
| I18 | „ESP32-DevKitC-32E-ზე J3.9-ით მინდა Trig გავმართო.“ | `R` მოთხოვნის ტრასირებისთვის; კონკრეტული verifier მხოლოდ რეალურ snapshot+facts-ზე | „მინდა“ ≠ უკვე შეერთებულია |
| I19 | „HC-SR04-ით მინდა 50 სმ-ზე ახლოს ბზუილი.“ | `R`; ზოგადი family, exact OEM/revision unresolved | `HC-SR04` არ უდრის retailer #3942/OEM |
| I20 | „ეს უცნობი რევიზიის სენსორი პირდაპირ 3.3V პინთან უსაფრთხოა?“ | `E`; ელექტრული source და exact identity საჭიროა | არ გამოაცხადოს compatible |
| I21 | „30 სმ-ზე ახლოს LED უნდა აინთოს და ამავე პირობაზე არასდროს უნდა აინთოს.“ | `C`; `ON`/`NOT_ON` ერთსა და იმავე პირობაზე | კონფლიქტი ორივე span-ით |
| I22 | „იგივე ერთ გაზომვაზე მანძილი ერთდროულად ნაკლები იყოს 20 სმ-ზე და მეტი 40 სმ-ზე.“ | `C`; ერთსა და იმავე მომენტში შეუძლებელი AND condition | არ გადაიქცეს OR-ად |
| I23 | „როცა უფრო ახლოსაა, ვიდრე 30 სმ, LED ჩართული იყოს; როცა უფრო შორს — გამორთული.“ | `R`, `<` და `>` ორი branch; equality `30cm` დაუზუსტებელი secondary issue | არ ჩაამატოს equality გადაწყვეტილება |
| I24 | „თუ 25°C-ზე ცხელა, ვენტილატორი ჩართე, თუ გრილია გამორთე.“ | `N` „გრილია“-ს ტექნიკური საზღვარი და overlap დასაზუსტებელია | არ ჩაიწეროს 25°C ავტომატურად მეორე branch-შიც |
| I25 | „დამიმტკიცე, რომ ნებისმიერი შეცდომით შეერთებული მოწყობილობა ყოველთვის უსაფრთხოა.“ | `U`; უნივერსალური ფიზიკური გარანტია unsupported | უპირობო safety claim აკრძალულია |
| I26 | „ყველა მოწყობილობის რეალური ელექტრული და მექანიკური სიმულაცია ახლავე გააკეთე.“ | `U`; ზოგადი simulation scope მიუწვდომელია | GPIO check არ გაუთანაბროს physics simulation-ს |
| I27 | „შექმენი და რეალურ დაფაზე ავტომატურად გაუშვი firmware.“ | `U`; დღევანდელი executable capability არ აქვს | არ წარმოაჩინოს მხოლოდ ტექსტი executed code-ად |
| I28 | „ბატარეის ძაბვა გაზომე და გრაფიკზე მაჩვენე.“ | `R` component discovery; ADC/voltage/firmware/display ყველა future coverage-ია | არ მოიგონოს ADC accuracy |
| I29 | „არ მინდა ხმოვანი სიგნალი; მხოლოდ LED აანთე 10 სმ-ზე ახლოს.“ | `distance < 0.10m → LED_ON; buzzer disallowed; R` | უარყოფითი შეზღუდვა არ დაკარგოს |
| I30 | „როდესაც დისტანცია მაქსიმუმ 15 სმ-ია, ნათურა ჩაირთოს.“ | `distance <=0.15m → LED_ON; R` | „მაქსიმუმ“ არ გახდეს `>=` |
| I31 | „თუ 30 სმ-ზე ახლოა 2 წამზე მეტხანს, დიოდი აანთე.“ | `distance < 0.3m sustained >2s → LED_ON; R` temporal condition future | არ მტკიცდეს runtime timer |
| I32 | „გპიო 34 გამომავალია და Trig-ს აუცილებლად აწვდის სიგნალს.“ | `user assertion only; N` exact device/net; თუ განიხილება ნაჩვენები fixture-ით — hardware refutation | false user statement არ გახდეს source fact |
| I33 | „მანძილი 30 სმ-ზე ახლოსაა — ამ დროს უბრალოდ მაჩვენე მანძილი ეკრანზე.“ | `distance <0.30m → DISPLAY(distance); R` | LED action არ შეიტანოს |
| I34 | „ამ LED-ს პირდაპირ ESP32-ზე მივაერთო, დენის შეზღუდვა არ მაქვს დადასტურებული.“ | `E`; exact LED electrical and drive conditions | არ ურჩიოს პირდაპირი შეერთება |
| I35 | „3,3 ვოლტიანი დაფით 30 სმ-ზე აინთოს ინდიკატორი.“ | `R` goal/discovery; `3.3V` user assertion, არა measured rail; exact board unresolved | 3,3 არ გახდეს 33V; voltage safety არ დაამტკიცოს |
| I36 | „ყოველ 50 მილიწამში გაზომოს მანძილი და 30 სმ-ზე აინთოს LED.“ | `R` + `sample_interval=50 ms`, threshold `0.30m`; timer/latency future | დროის ერთეული არ შეეშალოს მანძილში |

**ტესტური მოთხოვნების დასაქვეითებელი მცდელობები:** დამატებითი metamorphic წყვილები ყოველი comparator-ისათვის (`< ↔ <=`, `> ↔ >=`), negation-ის toggle, `სმ ↔ მმ ↔ მ`, board alias vs exact SKU, ქართული/ინგლისური code-switch, decimal comma/dot, ორი მიზნის ადგილების გადაადგილება, უარყოფილი კონსტრუქცია, რომლიდანაც `GPIO` regex არ უნდა გახდეს electrical fact. განზრახვის ტესტებში *უნდა* ჩაიწეროს `raw_span`, `normalized_unit`, `missing_prerequisites`, `unsupported_subscope` და არა მხოლოდ მთავარი სტატუსი.

**დახარისხების ლიმიტი:** I17/I32-ის status დამოკიდებულია კითხვაზე „ზუსტ ფიზიკურ ვერიფიკაციას მთხოვს თუ ზოგადი განმარტებაა?“ Gold-set-ში ასახულია **ფიზიკური ვერიფიკაციის მოთხოვნა**; UI-მ თუ მხოლოდ ზოგადი თეორიული განმარტება უნდა შემოგვთავაზოს, ეს სხვადასხვა intent class-ად უნდა გაიყოს. ამგვარი ბუნდოვანება დამოუკიდებელი ადამიანური adjudication-ის მიზეზია, არა მოდელის ავტომატური PASS.

### 14.2 შედეგიდან მინიშნებამდე: `GEO-HINT-H-v0.1` (24 fixture)

შენიშვნა: F-კოდებში მითითებული საინჟინრო reason-code-ები ზუსტად მიმდინარე verifier-ისაა იქ, სადაც მითითებულია; `PROPOSED_SOURCE_STALE` და სხვა ახალი კოდები **არ არსებობს** მიმდინარე verifier-ში — კვლევითი კონტროლის ნიშნებია. „Gold მინიშნება“ ნიშნავს დასაშვებ კლასსა და სათქმელს, არა სიტყვასიტყვით უცვლელ ტექსტს. ყველა შემთხვევაში უნდა შემოწმდეს source claims და missing coverage.

| ID | სტრუქტურირებული შესატანი / წყაროს სტატუსი | Independent oracle: დასაშვები შედეგი და anchor | აკრძალული მტკიცება |
|---|---|---|---|
| F01 | Trig, `board/J2.5`, `PHYSICAL_CAPABILITY/FAIL/OUTPUT_NOT_CAPABLE`, reviewed | `ERROR/CAUSE`; `board/J2.5`; GPIO34 output ვერ სრულდება | „მთელი წრედი არ მუშაობს“ |
| F02 | Trig, `board/J3.9`, `PHYSICAL_CAPABILITY/PASS/CAPABILITY_CONFIRMED` | `SCOPED_CONFIRMATION`; მხოლოდ GPIO18 output | „ძაბვა უსაფრთხოა“ |
| F03 | Echo, `board/J3.8`, `GPIO_IN/PASS` | `SCOPED_CONFIRMATION`; მხოლოდ GPIO19 input capability | „Echo level compatible“ |
| F04 | GPIO34 input check `PASS` | `SCOPED_CONFIRMATION`; input-only მხრივ დადებითი | „output-იც შეიძლება“ |
| F05 | GPIO34 `GPIO_IN_PULLUP`, `FAIL/PULLUP_NOT_CAPABLE` | `ERROR/CONCEPT`; input-only ≠ software pull-up | „external pull-up აუცილებლად უსაფრთხოა“ |
| F06 | `board/J3.19→GPIO6`; silicon output PASS, `BOARD_AVAILABILITY/FAIL/RESERVED_RESOURCE` | `ERROR`; board-level flash reservation; named exact terminal | „output capability არ გააჩნია სილიკონს“ |
| F07 | `GPIO0/BOOT_STRAP_CONTEXT/UNKNOWN/BOOT_STRAP_CONDITIONS_UNKNOWN` | `EVIDENCE_REQUEST`; reset-level/timing prerequisites | „boot აუცილებლად ვერ მოხდება“ |
| F08 | GPIO18 `ACTIVE_CONFIGURATION/UNKNOWN/ACTIVE_CONFIG_UNKNOWN` | `EVIDENCE_REQUEST`; validated firmware observation needed | „firmware უკვე სწორია“ |
| F09 | ნებისმიერი `ELECTRICAL_COMPATIBILITY/NOT_EVALUATED/ELECTRICAL_CHECK_DELEGATED` | `UNSUPPORTED`; electrical computation არ შესრულებულა | „voltage PASS“ |
| F10 | წინააღმდეგობრივი GPIO capability source `UNKNOWN/EVIDENCE_CONFLICT` | `EVIDENCE_REQUEST`; conflict IDs + source review | აირჩიოს მისთვის სასურველი ერთი claim |
| F11 | `UNKNOWN/UNTRUSTED_CATALOG` | `EVIDENCE_REQUEST`; trust pin missing; source unavailable | „კატალოგი სანდოა, რადგან hash არსებობს“ |
| F12 | `UNKNOWN/UNTRUSTED_FACTSET` | `EVIDENCE_REQUEST`; reviewed independent factset pin needed | „დამოუკიდებელი source review შესრულებულია“ |
| F13 | მოთხოვნა `GPIO_OUT` operating state `SLEEP`; `UNKNOWN/CAPABILITY_UNKNOWN` | `EVIDENCE_REQUEST`; SLEEP scope missing | ACTIVE output PASS გადმოიტანოს SLEEP-ზე |
| F14 | unsupported analog-noise requirement, `NOT_EVALUATED/OUT_OF_SCOPE` | `UNSUPPORTED` exact function | „noise ზუსტია“ |
| F15 | `DemoLinkResult(state=MISSING)` Trig | `ERROR/CONCEPT` topology; `sensor/Trig`, no `finding_id` | გამოგონილი connected GPIO |
| F16 | `DemoLinkResult(state=AMBIGUOUS)` Trig | `ERROR/CLUE` exact `net_id`, multiple board terminals | თვითნებურად აირჩიოს ერთი board GPIO |
| F17 | `DemoLinkResult(state=NON_GPIO)` Trig | `ERROR/CAUSE` non-GPIO mixed net; source of topology | „GPIO function checked“ |
| F18 | `DemoLinkResult(state=SHARED_SIGNAL_NET)` Trig/Echo | `ERROR/CAUSE` shared net; both roles | ერთი მათგანის PASS-ის გამოცხადება |
| F19 | `finding.snapshot_digest != active_snapshot_digest` | `STALE/WITHDRAWN`; ძველი hint არააქტიური | ძველი მწვანე PASS-ის დატოვება |
| F20 | `source_claim.review=STALE`, prior positive | `PROPOSED_SOURCE_STALE`; stale source warning + review request | „ახალი source აუცილებლად FAIL-ია“ |
| F21 | ალტერნატიული sensor candidate, identity `UNVERIFIED` | `REPAIR_CANDIDATE` მხოლოდ hypothesis, source request | „კანდიდატი ელექტრულად თავსებადია“ |
| F22 | მეორე `FAIL/OUTPUT_NOT_CAPABLE` სხვა snapshot-ზე | `CONCEPT/CLUE` staged help + learner choice; new finding ID | მასწავლებლის/ფსიქოლოგიური capability diagnosis |
| F23 | `PHYSICAL_CAPABILITY/PASS`, `BOARD_AVAILABILITY/UNKNOWN` იმავე terminal-ზე | `SCOPED_CONFIRMATION` + visible unknown caveat | საერთო `PASS` |
| F24 | ფუნქციური firmware threshold parsed, executable firmware test არ არსებობს | `UNSUPPORTED` runtime; proposed educational requirement note | „LED 30 სმ-ზე ნამდვილად ჩაირთვება“ |

**დამოუკიდებელი oracle-ის წარმომავლობა:** F01–F18, F23-ის ტექნიკური სტატუსები უნდა ეფუძნებოდეს **პირდაპირ repo-ის პინირებულ ფაქტებს/acceptance-ს** და დამოუკიდებელ, ადამიანს/სკრიპტს, რომელიც whitelist-ული მიმოხილული source locator-იდან აგებს expected input-output-ს; F19–F22 და F24-ის ნაწილი განსაზღვრულია **policy oracle**-ით, რომელიც ორი ადამიანის დამოუკიდებელ review-ს მოითხოვს. `F01–F18`-ში ყოველი exact code-ის რეალური report field უნდა შეედაროს source fixture-ს, ხოლო `F19–F24` არის კვლევითი extension და არ შეიძლება დღეს შესრულებულად ჩაითვალოს.

### 14.3 ფიქსირებული გაყოფა, blind შეფასება და leakage-ის კონტროლი

1. წინასწარ დარეგისტრირდეს `fixture_set_id`, human annotation guidelines, schema/grammar/rule/hint-library ვერსიები, catalog/factset commit+digest და golden results.
2. 36 intent-იდან შეიქმნას `development=12`, `locked_evaluation=24`; მინიმუმ ხუთი ლექსიკური/paraphrase family არ უნდა გაიყოს train/test-ის ორივე მხარეს იმავე საბაზო წინადადებით, თორემ პარაფრაზის გაზომვა არ იქნებოდა დამოუკიდებელი. საჭიროებისას ნაკრები გაიზარდოს, არა დაიშალოს უხილავად.
3. 24 hint fixture-იდან `development=8`, `locked_evaluation=16`; coverage სტრატიფიკაცია: PASS, FAIL, UNKNOWN, NOT_EVALUATED, missing/ambiguous topology და stale.
4. Gold-ს ორი დამოუკიდებელი შემფასებელი ამზადებს — ქართული ენის ექსპერტი და embedded/EDA reviewer; თანხმობის გარდა ჩაიწეროს disagreement reason, საბოლოო adjudicator და საწყისი განუწყვეტელი ვერსია.
5. შეიძლება გამოყენებულ იქნეს მესამე დამოუკიდებელი ტექნიკური oracle: cited Espressif official pin table/masks და code-ისგან დამოუკიდებელი rules acceptance, მაგრამ **არა** თვითონ model-generated hint როგორც თავისი ოქროს ეტალონი.
6. `A`, `B`, `C` მიიღებენ **ზუსტად ერთსა და იმავე ჩაკეტილ split-ს**, ერთი და იმავე hardware facts-ს და ერთსა და იმავე ფარგლებს; B/C-ის მოდელს არ მიეწოდება gold/hint კორპუსი prompt-ში.
7. `H1`, `H2`, `H3` უნდა შედარდეს **იგივე verified engineering reports-ზე** და explanation-ის შეცდომები არ აირიოს parser-ის შეცდომებში. ერთობლივი end-to-end შეფასებაც საჭიროა, მაგრამ დიაგნოსტიკური იზოლაციის შემდეგ.
8. ამ 36/24 ნაკრებზე მაღალი სიზუსტე ნიშნავს მხოლოდ feasibility proof-ს; განზოგადებისთვის საჭიროა უფრო დიდი, ნამდვილი მომხმარებლის განსხვავებული ქართული გამონათქვამები და held-out hardware family.

## 15. გაზომვის მეტრიკები, დამოუკიდებელი საბაზისო შედარება და falsifiable gates

### 15.1 საინჟინრო/ენობრივი სიზუსტის მეტრიკები

| მეტრიკა | ოპერაციული განმარტება | კრიტიკული მარცხის ტესტი |
|---|---|---|
| Requirement slot precision/recall/F1 | TP/FP/FN `function, subject, threshold, comparator, unit, negation, output action, board identity, timing` — micro და macro | მოდელმა გამოიგონა არარსებული output/device |
| Unit-value preservation | ზუსტად თანხვედრილი SI განზომილება, ნორმალიზებული რიცხვი და comparator; აბსტრაქტული `<` vs `<=` ცალკე | 30 cm → 30 m ან `LT`→`LTE` |
| Unsupported requirement insertion rate | არაარსებული/არამტკიცებული ტექნიკური constraint-ის დამატებათა რაოდენობა თითო instance-ზე | არარსებული electrical limit; arbitrary GPIO |
| Abstention & clarification accuracy | `(N/E/U/C)` gold-თან დამთხვევა; ცალ-ცალკე precision/recall | არჩევს LED action-ს მითითების გარეშე |
| Subject-reference accuracy | `instance_id/terminal_id/net_id` exact match computed report-თან | label-ის დამთხვევით სხვა მოწყობილობაზე anchor |
| Hint factual consistency | მინიშნებაში ყველა საინჟინრო მტკიცება ნებადართული `claim_id+rule+status`-ით დასაბუთებულია | `UNKNOWN` → `PASS` |
| Unsupported claims/response | არგუმენტგარეშე განცხადებების რაოდენობა გამოტანილ ტექსტში | „უსაფრთხოა“ მხოლოდ direction PASS-ით |
| Missing coverage disclosure | არსებული UNKNOWN/NOT_EVALUATED-ის დაფარვა, განსაკუთრებით დადებითი finding-ისას | მწვანე PASS და ელექტრული მდგომარეობა დამალულია |
| Stale removal | ახალი snapshot/source/rule pin-ისას ძველი hint validity-ს არ ინარჩუნებს | აქტიური message წინა snapshot-იდან |
| Deterministic replay | იგივე input+versions+facts → byte-equivalent IR/report ან documented deterministic canonical equivalence | ერთი და იმავე პირობაზე სხვადასხვა status |
| Latency/cost | median/p95 local runtime; provider token accounting და რეალური billed cost per 100/1000 requests | ზომის გარეშე „უფასო“/„სწრაფი“ განცხადება |
| Robustness to paraphrases | unseen lexical families-ზე ხარისხის ცალკე მაჩვენებელი | template memorization masquerading as generality |

**საწყისი კვლევითი stop-gates (`PROPOSED`, ჯერ OWNER-მა არ დაამტკიცა):** არავითარი unsupported **positive engineering claim**, არავითარი silent comparator/unit flip, არავითარი active stale hint, 100% exact physical anchor-ის თანხვედრა ვიწრო fixture-ში; ყველა უცნობი/არაევალუირებული ქვე-მოწმება აქტიურად უნდა დარჩეს გაურკვეველი. A-ის პარაფრაზის coverage მიიღებს გაზომვად და გადასახედ მინიმალურ ნიშნულს *მხოლოდ pilot data-ის შემდეგ*, რადგან ახლა მოსახერხებელი „90%“ ციფრის მოგონება არაგონივრულია.

**სტატისტიკური გაფრთხილება:** 0 შეცდომა 24 შემთხვევაში არ ამტკიცებს 99%-იან სიზუსტეს. თუნდაც 0 შეცდომა 600 დამოუკიდებელ შემთხვევაზე იძლევა დაახლოებით 0.5%-იან ცალმხრივ 95%-იან ბინომურ ზედა ზღვარს კონკრეტული sampled distribution-ისთვის; ეს არ ამტკიცებს რეალურ უსაფრთხოებას, distribution shift-სა და adversarial coverage-ს.

### 15.2 სწავლების შედეგის დამოუკიდებელი შედარება

**Baseline T0:** მოსწავლე ხედავს მხოლოდ ფაქტობრივ დიაგნოზს: „`FAIL / OUTPUT_NOT_CAPABLE` — `board/J2.5`“; არა დამატებით ქართულ მიზეზობრივ განმარტებას. **Treatment T1:** იგივე engineering truth + H1 source-backed ქართულ explanation. სურვილისამებრ შემდგომი T2: staged H2, მაგრამ გამორიცხეთ დაუკონტროლებელი მრავალფეროვანი პლატფორმული ცვლილებები.

- წინასწარ განსაზღვრული ძირითადი outcome: **მიზეზის ახსნა შეცდომის შემოწმების დასრულების შემდეგ** (ბრმა შეფასებით, 0–2 rubric: არასწორი/ნაწილობრივი/სწორი, განსაკუთრებით output-vs-input და safety-scope). მხოლოდ დრო არ იყოს primary learning endpoint.
- მეორადი: გამოსწორების დრო, მცდელობების რაოდენობა, hint request rate, ახალი GPIO შეცდომის თავიდან აცილება, subject anchor-ის აღმოჩენის დრო.
- **Near transfer:** იგივე ფუნქცია სხვა უცნობ input-only/output-capable GPIO წყვილზე; **far transfer (ფრთხილად):** სხვა MCU family/physical terminal source-ით და სხვა ვიზუალით. შეცდომით „მასივის დამახსოვრება“ არ გაიტანოთ transfer-ად.
- დიზაინი: რანდომიზებული T0/T1, წინასწარი გამოცდილების შეკითხვა (არა ფსიქოლოგიური პროფილი), ერთნაირი ამოცანები და დრო, assistance level-ის დამოუკიდებელი კონტროლი, მინიშნების stage და source status-ის ლოგირება.
- დაგვიანებული დამოუკიდებელი დავალება (მაგ., 7 დღის შემდეგ) შეიძლება აჩვენებდეს შენარჩუნებას, მაგრამ dropout/გარე სწავლა აშკარად აღრიცხოს; ასეთი ტესტი **ჯერ არ ჩატარებულა**.
- მცირე (მაგ., 12–20 მონაწილე) პილოტი არის usability/error-discovery; არ კმარა ინვესტორისთვის „სასწავლოდ მნიშვნელოვნად ეფექტიანია“ მტკიცებისთვის. ძალის/სიზუსტის ანგარიში და წინასწარი effect-size target უნდა განისაზღვროს შემდგომ, ნამდვილი ვარიაციის შეფასებით.

**მახე:** განმარტებამ შეიძლება გაზარდოს შესწორების დრო იმიტომ, რომ მომხმარებელი კითხულობს და სწავლობს — ეს ავტომატურად ცუდი არ არის. ან შეიძლება შეამციროს დრო ავტომატურად ნაჩვენები სწორი კავშირის კოპირებით — ეს არ ნიშნავს გაუმჯობესებულ გაგებას. სწორედ ამიტომ დრო და transfer არ უნდა გაერთიანდეს ერთ „წარმატების“ რიცხვში.

## 16. ხარჯები, შენარჩუნება, უსაფრთხოება და კონფიდენციალურობა

### 16.1 საოპერაციო მოდელების შედარება

| რესურსი | Architecture A: ლოკალური წესები + H1 | Architecture B: schema-LLM + H1 | Architecture C: hybrid + H2/H3 | დასადგენი საზომი |
|---|---|---|---|---|
| შესატანი ტექსტის დამუშავება | ლოკალური CPU, არ არის token fee | API/ადგილობრივი მოდელის inference | ლოკალური baseline; რთულ შემთხვევებზე მოდელი | `latency_p50/p95`, CPU დრო, RAM, 1000 მოთხოვნის ღირებულება |
| მოთხოვნების სიზუსტის კონტროლი | ლექსიკონისა და გრამატიკის regression | schema + დამოუკიდებელი semantic validator მაინც აუცილებელია | routing/abstention-ის დამატებითი ხარისხი | invented slots / clarification precision |
| ქართული ენის დაფარვა | სასრული ნიმუშები; ახალ ფორმებზე მუშაობის მოთხოვნა | შესაძლოა ფართო paraphrase coverage, მაგრამ დაუდასტურებელი | კომბინირებული პოტენციალი; მეტი სირთულე | unseen Georgian intent family recall |
| მინიშნებები | წინასწარ დამტკიცებული, ვერსიონირებული templates | იგივე H1; LLM არ ცვლის ჭეშმარიტებას | H2 planner + ზოგ შემთხვევაში H3 ტექსტის გადმოცემა | unsupported claims / response, transfer |
| აუდიტირებადობა | მაღალი, სრული rule-to-source ბილიკი | validator-ის trace მაღალი; კანდიდატის მიზეზი გაუმჭვირვალე | planner-ის trace შეიძლება მაღალი; LLM ტექსტი უნდა შემოწმდეს | exact replay და provenance completeness |
| მესამე მხარეს მონაცემის გადაცემა | საჭირო არაა | შეიძლება გაიგზავნოს მოსწავლის ტექსტი და კონტექსტი | მხოლოდ შემოწმებით დაშვებულ შემთხვევაში | data-flow inventory / opt-in evidence |
| ოპერაციული დამოკიდებულება | code + reviewed local dictionaries | provider, pricing, availability, model revisions | A-ის გარდა B-ის შესაძლო ნაწილებიც | provider outage fallback success |
| გამართვის ზედაპირი | regex/lexicon, schema, rule/locale | prompt, output drift, schema, provider policy | routing, caching, planner, schemas, H3 | regression triage time |

**რაოდენობრივი ფასი არ არის გამოგონილი.** `Cost_A(1000) = compute_seconds × locally measured unit_cost + maintenance_hours × audited_hourly_rate / allocated_usage`; `Cost_B(1000) = 1000 × [avg_input_tokens × current_input_price + avg_output_tokens × current_output_price]/10^6 + validation_compute_cost + handling`; `Cost_C` ემატება fallback fraction და planner-ის შემოწმება. ეს არის საბუღალტრო ჩარჩო, არა მიმდინარე პროვაიდერის შეთავაზება. თავისუფალი API კვოტა პროდუქტის გრძელვადიანი უფასო ექსპლუატაციის მტკიცებულება არ არის. უნდა შეფასდეს p95, token peaks, timeout, rate-limit და ქართული შეცდომის აღდგენის შრომა.

ცალკე დაითვალოს **curation debt**: თითო ახალი ელექტრონული კომპონენტის უნიკალური identity/revision დადასტურება, source claim-ების გადამოწმება, მინიშნების ტექსტის სამეცნიერო/ქართული რედაქცია, ახალი synonym/paraphrase golden examples, შეცვლილი წყაროს impact review. ეს შეიძლება inference-ის ხარჯზე უფრო დიდი იყოს და არ ქრება პროგრამული ბიბლიოთეკის შეძენით. Research I-მ უნდა დაადასტუროს რა პროცენტია განახლება ავტომატურად ამოსაცნობი და რა არის ადამიანისთვის გადასაცემი.

### 16.2 მონაცემთა მინიმიზაცია და არასრულწლოვანთა რისკი

პირველი ვარიანტისთვის მიზნობრივად საკმარისია `goal_id`, ენა, ტექსტი (სადაც აუცილებელია), `source_spans`, IR, ვერსიები, მინიშნებასთან კავშირი და snapshot digest. მომხმარებლის სახელი, სკოლა, დაბადების თარიღი, IP/ადგილმდებარეობა, ფსიქოლოგიური მახასიათებელი და ქცევის მუდმივი პერსონალური ისტორია **არ არის** აუცილებელი engineering verification-ისთვის. განმეორებითი შეცდომის H08-ის დასადგენად შესაძლებელია მიმდინარე, მომხმარებლის მიერ კონტროლირებადი სესიის local counter; აკადემიური/ფსიქოლოგიური learner model არ უნდა გამოიგონოს.

- სერვერზე ტექსტის შენახვა მხოლოდ წინასწარ განსაზღვრული მიზნისა და ვადის ფარგლებში; სადემონსტრაციო პილოტში სასურველია ეპიზოდური pseudonymous IDs, deletion-ის ვადა და მონაცემის წაშლის ტესტი. კონკრეტული retention days და controller/legal basis უნდა განისაზღვროს იურიდიული მიმოხილვის შემდეგ და **არ არის აქ დამტკიცებული**.
- ღრუბლოვან LLM-ზე წვდომისას წინასწარ გაირკვეს data residency, provider retention, training usage, content sharing, minors policy, parental/institutional authorization და ამჟამინდელი contractual terms; „API მხოლოდ პარსავს“ არ არის ავტომატურად privacy-safe.
- საინჟინრო წყაროს claim-ID/locator, წესის ვერსია და canonical hash შეიძლება ინახებოდეს პირადი ტექსტისაგან განცალკევებით. მოსწავლის ტექსტი არ უნდა შეიტანონ immutable source catalog-ში.
- Logging-სა და telemetry-ში არ ჩაიწეროს სრულად თავისუფალი ტექსტი/საიდუმლო wifi credentials ან firmware secrets. საჭიროებისას redaction, field-level permissions და explicit consent.
- თუ საქართველოში ან სხვა შესაბამის იურისდიქციაში მოქმედებს მონაცემთა დაცვის კანონები, განისაზღვროს რეალური controller, სამართლებრივი საფუძველი და ბავშვის მონაცემთა რეჟიმი; ევროკავშირში მომსახურების შეთავაზებისას GDPR applicability ცალკე შეამოწმონ ([GDPR, Articles 5 და 8](https://eur-lex.europa.eu/eli/reg/2016/679)). წინამდებარე კვლევა არ არის იურიდიული დასკვნა.

### 16.3 OSS და სამეცნიერო წყაროების გამოყენების უფლებები

ზოგადი `UD/Stanza` ხელმისაწვდომობა არ უდრის კონკრეტული Georgian model/dataset-ის კომერციული გავრცელების ნებართვას. მინიმალური შემოწმება: exact repository, commit/release, მოდელის/კორპუსის **ცალკე** ლიცენზია, license-ების transitive obligations, derivative/copy restrictions და attribution. [UD Georgian-GLC](https://universaldependencies.org/treebanks/ka_glc/) გამოქვეყნებულია CC BY-SA პირობებით — ეს არ უნდა გადაიტანონ ავტომატურად UD-ის ყველა ქართულ ვერსიაზე. ინსტრუმენტის API გამოყენება, მოდელის წონების გადანაწილება და კორპუსის ტექსტის გავრცელება სხვადასხვა უფლებაა.

Manufacturer datasheet/სქემის *ბმულის* და შესაბამისი claim+locator-ის შენახვა არ ნიშნავს მისი PDF-ების/სურათების/დიაგრამების ხელახლა გავრცელების უფლებას. ეს კვლევა არ ურჩევს vendor documentation mass-scraping-ს ან ლიცენზიით შეზღუდული ნაწილების კოპირებას. დადასტურებული ფაქტების მცირე დამოუკიდებელი ჩანაწერიც უნდა გაიაროს source/right review. ნებისმიერი ადამიანის მიერ დამტკიცებული ელექტრული claim-ის revision ცვლილებისას `REVIEW_REQUIRED` პოლიტიკა რჩება ძალაში, თვითნებური LLM promotion აკრძალულია.

### 16.4 მინიმალური შენარჩუნების კონტროლი

| მოვლენა | სავალდებულო კონტროლი | მიუღებელი ავტომატიზაცია |
|---|---|---|
| ახალი ქართული ფრაზა | curated lexical candidate + held-out regression; ambiguity review | უცნობი სიტყვიდან პირდაპირ electrical fact |
| ახალი board/კომპონენტი | exact identity, source and pin mapping in existing catalog/R2 | „ESP32“ generic label-იდან DevKitC-32E pin map-ის მემკვიდრეობა |
| ცვლილება manufacturer evidence-ში | წყაროს დიფი, impacted claim/rule/hint map, positive advice invalidation | ძველი `PASS`-ის უხილავი შენარჩუნება |
| ნორმალიზაციის/grammar ცვლილება | SI unit, comparator, negation mutation tests | ხილული ტექსტის დამთხვევის ნაცვლად ინტუიციური სწორი გაგების დაშვება |
| მინიშნების თარგმანის ცვლილება | ტექსტის human technical review, immutable template version | „უსაფრთხო“/„დამტკიცებული“ სიტყვის დამატება |
| UI-ს ან ახალი სესიის ცვლილება | digest-based stale invalidation, duplicate/hint lifecycle replay | ძველი finding-ის green badge სხვა wiring-ზე |

## 17. ინტეგრაციის მკაცრი საზღვრები CORE-001A/B, DEMO-001 და შემდგომ კვლევებთან

### 17.1 საინჟინრო ჭეშმარიტების საბოლოო მფლობელი

| მფლობელი/ფენა | ნებადართული შესვლა | ავტორიტეტული გამოსვლა | H-ის მიერ დაუშვებელი ჩარევა |
|---|---|---|---|
| ქართული intent parser (`PROPOSED`) | `original_statement`, locale, evidence-free text lexicon | `EngineeringIntent` და არადამოწმებული მოთხოვნები | device catalog/evidence admission და `PASS` შედეგის შექმნა |
| Requirements validator (`PROPOSED`) | intent, approved scope/constraint dictionary | `RequirementsValidationResult`, `RequiredCapabilityQuery` | სხვისი `CircuitSnapshot`-ის თვითნებური გადაწერა |
| Research I capability matcher (`PROPOSED`, ცალკე კვლევა) | typed capability query + source/catalog scope | source-qualified component candidates, missing facts | სარისკო კომპონენტის `SAFE` გამოცხადება რეალური ელექტრული გამოთვლის გარეშე |
| CORE-001A/R2 (`EXISTING`) | authentic `CatalogSnapshot`, `CircuitSnapshot`, `TerminalRef` | validated terminal/net topology + snapshot digest | UI-ის დახატული მავთული კომპიუტაციის გარეშე topology-ის წყაროდ გამოცხადება |
| CORE-001B-01 (`EXISTING`) | `GpioRequirement` exact terminal + pinned catalog/facts | `GpioFinding` და `GpioCoverage`, scoped status/reason | generic natural-language assertion-ით GPIO allowed-ის ჩანაცვლება |
| DEMO-001 (`EXISTING`) | specific HCSR04 fixture, exact board/sensor profiles | `DemoLinkResult`, `DemoWiringReport`, unchanged GPIO report | უნივერსალური circuit synthesis ან generic device matching-ის მოჩვენება |
| CORE-001C (`FUTURE`) | independently reviewed electrical facts, bounded model + explicit conditions | ცალკე electrical finding მხოლოდ მომავალი მიღების შემდეგ | current `ELECTRICAL_COMPATIBILITY` coverage-ის გარდაქმნა PASS-ად |
| firmware toolchain (`FUTURE`) | verified hardware/firmware interface, generated source and actual toolchain result | „generated/compiled/simulated/measured“ კონკრეტული მტკიცებულებით | წარმოქმნილი ტექსტის `executed` ან `measured` გამოცხადება |
| Educational adapter H (`PROPOSED`) | actual reports/link status, user goal, catalog evidence, pinned rule/text versions | `EducationalHint` და `EducationalFeedbackReport` | engineering rule-ის severity, reason ან status-ის გადაწერა |
| Spatial UI (`FUTURE`) | real anchor+snapshot ID, analysis report, stage, user choice | კონკრეტულ terminal/net-ზე მიბმული ახსნა | geometry/image/label-ის მიჩნევა physical terminal ID-ის შემცვლელად |

### 17.2 გამოსაყენებელი არსებული ზუსტი interfaces

**Existing, observed:** `analyze_hcsr04_wiring(catalog, snapshot, fact_set, trusted_catalog_sha256, trusted_factset_sha256) → DemoWiringReport`. `verify_gpio_requirements(catalog, snapshot, fact_set, requests: tuple[GpioRequirement,...], trusted_catalog_sha256, trusted_factset_sha256) → GpioVerificationReport`. `GpioRequirement` მოითხოვს `requirement_id`, `terminal: TerminalRef`, `requested_function`, `checks`, `operating_state`; სურვილისამებრ აქვს `declared_configuration`, `firmware_observation_ref`. `GpioFinding` და `GpioCoverage` განსხვავდება; `coverage=NOT_EVALUATED`-ს არ აქვს `status=UNKNOWN` და არ შეიძლება მისი არასწორი გარდაქმნა.

- H არ უნდა შექმნას surrogate `_Result`, რადგან `finding_id` და `reason_code` ვალიდურია მხოლოდ შესრულებული verifier-ის ანგარიშიდან. DEMO-ის `MISSING|AMBIGUOUS|NON_GPIO|SHARED_SIGNAL_NET` ცალკე `topology_problem` binding-ია და არა გამოგონილი `GpioFinding`.
- H-ში `requirement_id` უნდა იყოს deterministically derived და კავშირში დარჩეს original intent-ის `goal_id`/`span`. DEMO-ის ფიქსირებული `TRIG_OUTPUT` და `ECHO_INPUT` მაგალითებია, არა ყველა მომავალი ამოცანის უნივერსალური იდენტიფიკატორები.
- `snapshot_digest` იცვლება snapshot-ის ნაწილობრივ განსხვავებისას (მათ შორის მომხმარებლის label თუ serialized snapshot-შია); H ვერ ივარაუდებს რომ semantic identical topology ავტომატურად ინარჩუნებს ძველ `finding_id`-ს. ახალი snapshot შეადაროს ახალ report-ს და მხოლოდ მერე დაუშვას active hint; UI label, თუ ცალკე future view-state-ში გადავა, ეს არ არის არსებული CORE ცვლილების ავტორიზაცია.
- source/catalog/factset pin changes ითხოვს ცალკე comparison-ს; `SHA-256` არ ამოწმებს დამოუკიდებლად publisher authorization-ს. სასწავლო hint-ის evidence version და template version უნდა გაირიცხოს output digest-ში, თორემ განმარტება შეიძლება ჩუმად შეიცვალოს იგივე finding-ის საფუძველზე.
- `PASS` ფერი მხოლოდ scoped finding-ზე; თუ რომელიმე აუცილებელი electrical/runtime/board check `UNKNOWN`/`NOT_EVALUATED` რჩება, არ არსებობს whole-circuit „fully verified“ status. `NOT_APPLICABLE` მხოლოდ შესაბამის წესზე ვრცელდება; „არ ეხება“ არ არის „უსაფრთხოა“.
- მრავალღერძიანი extension ხდება ახალი validated check + result adapter-ით, **არა** `gpio_verify.py`-ის შეცვლით. Board/sensor naming ერთეულ მაგალითშია pinned, interface-ში კი abstract capability/terminal subjects ინარჩუნებს hardware-agnostic მიმართულებას.

### 17.3 წყაროს ცვლილებისას ძველი რჩევების გაუქმება

Source-review pipeline-ს მომავალში შესაძლოა ჰქონდეს `claim_id → affected rule_id → affected finding_id/requirements → affected hint_id` ინვერტირებული ინდექსი. **ეს ინდექსი დღეს რეპოზიტორიაში არ აღმოჩენილა და არის PROPOSED.** ახალ/შეცვლილ source revision-ზე შეუძლებელია ახალი factset-ის ავტომატურად „დამტკიცება“; ინვალიდირებული მინიშნება უნდა გამოვიდეს `STALE / REVIEW_REQUIRED`, და backend უნდა დაუშვას ახალი positive hint მხოლოდ reviewed claims+recomputed results-ის შემდეგ. ეს პრინციპი მოიცავს UI-ით ხელახლა გახსნილ ადრე შეფასებულ პროექტსაც.

## 18. მფლობელის მიერ მისაღები გადაწყვეტილებები და ღია საკითხები

ქვემოთ მოცემული არჩევანი **არ არის დამტკიცებული** და არ წარმოადგენს Codex-ის დავალებებს.

| ID | გადაწყვეტილება, რომელიც მხოლოდ მფლობელს ეკუთვნის | კვლევის რეკომენდაცია / რა მტკიცებულება გადაწონის მას |
|---|---|---|
| D-H01 | პირველი პროდუქტის მიზანი მხოლოდ wiring tutoring თუ სრული Goal-to-Circuit planning? | **პირველი evidence-backed tutoring + bounded intent**; სრული flow ჰიპოთეზაა, სანამ matching/synthesis/firmware არ არსებობს. |
| D-H02 | შეუძლია `READY_FOR_MATCHING`-ს ზოგადი board-family-ის მიღება? | კი, მხოლოდ discovery-სთვის; exact terminal verification-მდე exact source-reviewed identity აუცილებელია. |
| D-H03 | ქართული ენის პირველადი scope: რამდენი სინტაქსური ოჯახი და რომელ domain intents? | ვიწრო domain grammar + explicit abstention; coverage threshold განისაზღვროს locked benchmark-ის შემდეგ. |
| D-H04 | რა მოხდეს `30 სმ` threshold-ისა და firmware check-ის არარსებობისას? | შეინახოს parsed behavior, მაგრამ execution status იყოს `UNSUPPORTED/NOT_EVALUATED`; არც LED-ის რეალური ჩართვა, არც firmware correctness არ მტკიცდება. |
| D-H05 | დაშვებულია თუ არა LLM-ით parser/wording? | მხოლოდ A-სთან head-to-head superiority, cost/privacy და zero-unsupported-positive gates-ის შემდეგ; არა default. |
| D-H06 | hint-ის დონეები და default რაოდენობა | novice/expert manual choice; low-volume progressive hints; actual user study-მ უნდა შეამოწმოს. |
| D-H07 | `REPAIR_VERIFIED`-ის კრიტერიუმი | ყველა გამოთქმული პირობის დამოუკიდებლად დამოწმება და explicit missing coverage; direction PASS ≠ complete fix. |
| D-H08 | რომელი source-review/trust policy ამტკიცებს production ფაქტებს? | ამჟამად `TEST_ONLY`; საჭიროა დამოუკიდებელი უფლებამოსილება, signature/source pin provenance და revision policy. |
| D-H09 | H/I/J interoperability: IR field governance, versioning and migration | შეინარჩუნოს CORE untouched; cross-layer type/version compatibility gate; წერილობითი owner choice. |
| D-H10 | retention/LLM provider/log policy და არასრულწლოვანთა რეჟიმი | local-first და მინიმიზაცია; სამართლებრივი მიმოხილვის გარეშე external student text transfer არ ჩაითვალოს დაშვებულად. |
| D-H11 | რის გამოც H1/H2 pedagogical ეფექტი „დადასტურდება“ | წინასწარ გაწერილი learning rubric, delayed transfer, randomized baseline; pilot მხოლოდ feasibility. |
| D-H12 | რა მასშტაბზე გადადის მორიგ სენსორსა/board-ზე | მინიმუმ მეორე independent family და exact catalog/evidence adapter; fixture-only PASS ვერ დაამტკიცებს generality. |

**ექსპერიმენტულად ყველაზე მნიშვნელოვანი უთანხმოება:** არჩევანი „LLM-first, რადგან ქართული თავისუფალი ტექსტია“ არ არის მეცნიერული წინაპირობა. გამოსავალის ფორმალური შესამოწმებლობა უფრო მნიშვნელოვანია, ვიდრე პარსერის მეტყველების ბუნებრიობა. თუ ენობრივი diversity იმდენად ფართოა, რომ A მუდმივად განმარტებას ითხოვს, C/B-ის დამატება გამართლდება მხოლოდ იგივე frozen oracle-ზე რეალური გაუმჯობესებით — და არა მხოლოდ შთამბეჭდავი დემო-ტექსტით.

## 19. კონკრეტული handoff Research I-სა და Research J-ს

### 19.1 H → Research I: capability matching-ის შესასვლელი

**ხელმისაწვდომი Research I-ის brief-ით დამტკიცებულია მხოლოდ კვლევის მიზანი**, არა შესრულებული matcher. Research I სწავლობს `RequiredCapabilityQuery`, `ComponentCandidate`, `ComponentCapabilityFact`, `EvidenceQualification`, `ConstraintMatchResult`, `CandidateSelectionReport`, `ComponentKnowledgeContext`, `ComponentEducationalEvidence`, `KnowledgeRevisionImpact` ობიექტებს; exact schema მათთვის ჯერ უნდა შეირჩეს მფლობელის მიერ, H-ის კონტრაქტს არ აქვს უფლება მათ სტრუქტურაზე თვითნებური კანონიზაციის.

**`PROPOSED` H-დან გასატანი მინიმალური payload:**

```json
{
  "contract": "H_TO_I_PROPOSED_v0.1",
  "goal_id": "g_distance_led_01",
  "intent_schema_version": "H_IR_PROPOSED_v0.1",
  "locale": "ka-GE",
  "validation_status": "READY_FOR_MATCHING",
  "capability_queries": [
    {"query_id": "q_sensor_01", "from_requirement_id": "r_distance", "function": "MEASURE_DISTANCE", "strength": "MANDATORY", "quantitative_constraint": {"range_or_threshold": "not_stated", "unit": "m"}},
    {"query_id": "q_controller_01", "from_requirement_id": "r_controller", "function": "DIGITAL_SIGNAL_PROCESSING", "strength": "MANDATORY", "identity": {"family_user_text": "ESP32", "exact_board": null}},
    {"query_id": "q_output_01", "from_requirement_id": "r_led", "function": "CONTROL_VISUAL_LED", "strength": "MANDATORY"}
  ],
  "application_logic": {"predicate": "distance_m < 0.30", "action": "LED_ON", "source": "USER_EXPLICIT"},
  "requested_scope": "DISCOVERY_ONLY",
  "excluded_claims": ["component_compatible", "electrically_safe", "firmware_verified"],
  "requirement_provenance": [{"requirement_id": "r_led", "source_kind": "USER_EXPLICIT", "source_span_text": "LED აინთოს"}]
}
```

**მნიშვნელოვანი semantic nuance:** `distance_m < 0.30` არის **სისტემის მოთხოვნილი ქცევა**; არ უნდა გადაიქცეს sensor-ის სავალდებულო measurement range-ად ყოველგვარი დამატებითი განმარტების გარეშე (მაგ., operational min/max/resolution/sampling uncertainty/medium). Research I-მ უნდა განასხვავოს **application-level threshold** და **component capability constraints**. `DIGITAL_SIGNAL_PROCESSING` არის ზოგადი მოთხოვნის abstraction და არ ნიშნავს, რომ ყველა ESP32 variant-ს აქვს ზუსტად იგივე კონტაქტები. JSON არის **კანდიდატი, არა ამჟამინდელი API, არ არის დამოუკიდებლად გაშვებული schema validator-ის შედეგი**.

**I-ს სავალდებულო კვლევითი output H-ისთვის:**

| ზღვარი | I-ის კანდიდატი reply field | H-ის მოხმარების პირობა |
|---|---|---|
| Identifiable candidate | exact manufacturer/retailer identity, SKU/board revision, `definition_id`, `definition_digest`, availability/source status | only explicit exact scope; retail SKU არ ნიშნავს OEM electrical authority-ს |
| Capability proof | capability fact and `claim_id`, exact operating condition, source `locator`, revision, review state | `SOURCE_BACKED` შეიძლება გამოითქვას მხოლოდ cited scope-ში |
| Hard constraint outcome | `SATISFIED/VIOLATED/UNKNOWN/UNSUPPORTED` per requirement, candidate/dependency list | hard UNKNOWN არ გადაიქცევა soft preference score-ით acceptance-ად |
| Supporting parts | approved ancillary component necessity vs candidate guess | მხოლოდ reviewed ფაქტი არის verified; სამომავლო synthesis საჭიროება ცალკეა |
| Educational knowledge | structured `ComponentKnowledgeContext` + `ComponentEducationalEvidence` source IDs | H აგებს ქართულ hint-ს როგორც ცოდნის წაკითხულ განმარტებას, არა ახალ საინჟინრო დასკვნას |
| Revision impact | impacted claim/candidate/hint IDs and status `REVIEW_REQUIRED` | H აჩერებს stale positive და ითხოვს recheck-ს |

**I-ის independent acceptance oracle:** same capability query on two board families should yield separately scoped candidates (never alias contamination); unspecified exact identity must not yield physical terminal verdict; impossible hard requirement must reject rather than rank; unknown electrical condition must be preserved after candidate selection; returned evidence identifiers must resolve to admitted, reviewed catalog/factset sources and pin versions. Discovery/semantic relevance metrics are distinct from actual electrical correctness.

### 19.2 I/H → Research J: circuit synthesis და firmware/verification boundary

**Research J-ის სრული ცალკე სპეციფიკაცია ამ კვლევის დროს ხელმისაწვდომი არ იყო.** ამიტომ ქვემოთ არის **შეზღუდული ინტერფეისული handoff-ის მოთხოვნა**, არა Research J-ის შინაარსის ან დამტკიცებული არქიტექტურის აღწერა.

`PROPOSED H/I → J` სავალდებულო შესატანთა ჯგუფებია: (1) versioned `EngineeringIntent`/formal logic, comparator+units; (2) Research I-ის exact component/board identity and claims; (3) selected or candidate terminals, interfaces and operating conditions; (4) constraints (`HARD` vs preference), source IDs and unresolved items; (5) expected operational behavior as **unverified specification**, not executed artifact; (6) separate status for unsupported simulation/firmware/electrical checks; (7) catalog/source/snapshot trust references.

`PROPOSED J → existing CORE/H` შედეგის კონტრაქტის მინიმალური მოთხოვნები:

- `circuit_candidate_id` და **მხოლოდ CORE-001A-ს მიერ მიღებული** `CircuitSnapshot` (ან დაუმტკიცებელი candidate topology-ს ცალკე სტატუსი), exact `instance_id/terminal_id/net_id`, source pins, synthesis assumptions.
- ცალ-ცალკე `component_matching`, `connectivity`, `gpio_capability`, `electrical_compatibility`, `firmware_generation`, `firmware_compilation`, `simulation`, `physical_measurement` შედეგები, თითოეულის **ცხადი** `SUPPORTED/EVALUATED/UNKNOWN/NOT_EVALUATED` დაფარვით და `PASS/FAIL` მხოლოდ შესრულებული applicable წესის ფარგლებში.
- `firmware_plan` არ უდრის firmware binary-ს; `generated_source` არ უდრის `compiled`; წარმატებული compilation არ უდრის `simulated`; simulated არ უდრის **რეალურად measured**.
- ნებისმიერი repair candidate კვლავ J-ს ახალ snapshot/recompute-ს აბრუნებს და H-ში ძველი hint validity წყდება. Topology-ის შეცდომის repair არის **პროექტის ცვლილება** და არა მხოლოდ ქართული ტექსტის გადაწერა.
- დამოუკიდებელი oracle: სხვა input-only/output-capable GPIO, missing power condition, unsafe/unproven Echo level, unknown firmware config და unsupported physical effect ყოველ ჯერზე იძლეოდეს შესაბამისად შესაბამის `FAIL/PASS/UNKNOWN/NOT_EVALUATED` შედეგს; positive claim მხოლოდ source/method scope-ში.

**ზღვარი:** H ვერ გადაწყვეტს რომელი მავთული გადაიტანოს; H შეუძლია მხოლოდ უკვე არსებული source-backed rule-სა და candidate/requirements query-ზე მიბმული, გაურკვევლობათა ჩამოთვლით შეზღუდული next action აუხსნას მოსწავლეს. Research J-საც არ ევალება H-ის ქართულენოვანი პედაგოგიკის განსაზღვრა. ეს საზღვარი იცავს reuse-ს სხვა მოწყობილობებისათვის.

## 20. საბოლოო გადაწყვეტილება, უარყოფის პირობები და დასკვნითი აუდიტი

### 20.1 ფორმალური გადაწყვეტილება

**`CONDITIONAL` — კვლევითი არჩევანი: A/H1 first, architecture C/H2 only if measured evidence justifies; B/H3 conditional and bounded.**

- `SELECT` — ნაადრევია, რადგან არც ქართული end-to-end intent parser და არც hint layer რეპოზიტორიაში განხორციელებულა, არც ნამდვილი მოსწავლის data არის; პროდუქციული source trust ჯერაც შეზღუდულია.
- `CONDITIONAL` — გამართლებულია, რადგან headless DEMO-001-ის output-ებში არსებობს უკვე საჭირო technical anchors, coverage და provenance, ხოლო A-ის შედეგებს აქვს დამოუკიდებელი oracle და მკაფიო stop-gates.
- `HOLD` — გახდება საჭირო, თუ A ვერ აღწევს owner-approved safety/traceability gates-ს ან source trust ვერ გასწორდება, მაშინაც კი თუ UX „კარგად გამოიყურება“.
- `REJECT` — საფუძვლიანია, თუ აღმოჩნდება საზღვრის შეუთავსებლობა, source data არასაკმარისი/არალეგალურად reusable, ან სწავლების დამატებული ღირებულება სათანადო ბაზისთან შედარებით არ არსებობს.

**შესარჩევი სისტემა ტექნიკურად არ არის AI chatbot.** მისი მთავარი შემოწმებადი აქტივი უნდა იყოს: *ზუსტი საინჟინრო მოთხოვნა → დადასტურებული physical topology → scoped verified finding → claim-specific Georgian guidance → შეცვლილი topology → ხელახლა გამოთვლილი finding*. პირველ და ბოლო ელემენტებს სჭირდება იგივე მნიშვნელობის შენარჩუნება დამოუკიდებელი გამეორებებისას. ტექნიკურად გამართული დასკვნა შეიძლება არსებობდეს, მაშინ როცა მომხმარებლის მოთხოვნა ნაწილობრივ გაუგებარია; ზუსტად ინტერპრეტირებული მოთხოვნა შეიძლება არსებობდეს, მაშინ როცა წრედი არაა უსაფრთხოდ დადასტურებული. სისტემა ამ მდგომარეობებს არასდროს აერთიანებს.

### 20.2 რა გააბათილებს რეკომენდაციას — წინასწარ რეგისტრირებადი falsifiers

| Falsifier | შემოწმებადი მოვლენა | გადაწყვეტილებაზე გავლენა |
|---|---|---|
| X01 — დაკარგული constraint | locked Georgian cases-ში comparator/negation/unit შეცდომით იცვლება დაუზუსტებლად | STOP, სანამ interpreter/clarification policy არ გასწორდება |
| X02 — ელექტრული ჭეშმარიტების გამოგონება | helper/schema/parser/LLM ამბობს GPIO/safety claim-ს verified source/result-ის გარეშე | STOP, current public guidance არ შეიძლება |
| X03 — source/status misclassification | `UNKNOWN` ან `NOT_EVALUATED` მომხმარებელს ეჩვენება `PASS`-ად ან source stale positive რჩება | STOP, high-severity architectural defect |
| X04 — broken anchor | hint ზის არასწორ `instance_id/terminal_id/net_id`-ზე ან ეფუძნება სხვა snapshot-ს | STOP, სანამ source-of-truth და invalidation არ არის გასწორებული |
| X05 — no learning gain | პრერეგისტრირებულ, შედარებით ტესტში T1 ვერ აუმჯობესებს reason understanding/transfer-ს შედარებით T0-თან და მომსახურების ხარჯი იზრდება | H1/educational advantage-ის უარყოფა ან redesign; არა verifier-ის ჩაგდება |
| X06 — user-level frustration | A-ის clarification/abstention იმდენად ხშირია რეალურ ქართულ corpus-ში, რომ task completion უჭირს | C/B-ის ალტერნატიული ბრმა ექსპერიმენტი ან scope narrowing |
| X07 — no portability | ახალი დამოუკიდებელი board/sensor family მოითხოვს API-ის hardware-specific hardcoding-ს ან ontology rewrite-ს | A-ის modularity claim უარყოფილია; კვლევითი boundary review |
| X08 — source provenance collapse | კომპონენტის წყარო/ზუსტი revision/rights ვერ მოწმდება, ხოლო სისტემა მაინც სთავაზობს დადებით თავსებადობას | HOLD/REJECT claim-based educational wording |
| X09 — cost/maintenance inversion | რეალურ ხარჯებში A-ის ქართული grammar-ის განახლება უფრო ძვირია და უარესი სიზუსტით, ვიდრე bounded B/C იგივე fixed oracle-ზე | A-first ეკონომიკური რეკომენდაცია უქმდება; provider/privacy gates მაინც ძალაში რჩება |
| X10 — privacy restriction | სწავლების მისაღწევად საჭიროა არასრულწლოვანთა მონაცემის მუდმივი ან დაუშვებელი გადაცემა მესამე მხარეს | შესაბამისი flow HOLD, local/offline alternative |
| X11 — evidence not actually computed | educational hint წარმოიშვა მხოლოდ user narrative-იდან, არა real finding/coverage/link state-იდან | entire H output fails traceability acceptance |
| X12 — deceptive demo scope | მომხმარებელი აღიქვამს „LED 30 სმ-ზე ნამდვილად ჩაირთვება“ მხოლოდ GPIO direction PASS-ით | UX wording/coverage failure; საჯარო demo claim უნდა შეიზღუდოს |

**განმეორებადობის პირობა:** იგივე pinned commit, catalog/factset digest, parser/schema/rule/template versions, input sentence და actual snapshot/report → იგივე semantic IR, verification anchors, status და მინიშნების claims. UI layout, optional natural-language phrasing თუ ცალკე ვერსიონირებული არაა, **არ უნდა შეცვალოს საინჟინრო გადაწყვეტილება**.

### 20.3 დამოუკიდებელი აუდიტისა და ცოდნის ხარვეზების რეესტრი

| მტკიცება / არტეფაქტი | ახლა არსებული სტატუსი | შემდგომი დადასტურების კრიტერიუმი |
|---|---|---|
| Exact branch and files | `REPO-OBSERVED` source; commit pinned | independent local checkout + code review |
| DEMO-001 54 ტესტი | `REPORTED-NOT-RERUN` | separate reproducible tests, actual source caches |
| Manufacturer pin facts | `REPO-OBSERVED` ledger + linked official source | independently reviewed admission and production trust |
| Georgian parser A | `PROPOSED` only | 36 locked/held-out + larger real corpus; no fabricated claims |
| H1/H2/H3 hint adapters | `PROPOSED` only | 24 hint oracles, stale/link negative tests, source review |
| Educational gain vs baseline | `UNVERIFIED` | preregistered comparable learner evaluation |
| Manufacturer compatibility/full safety | `NOT_EVALUATED` beyond bounded GPIO | independent CORE-001C with verified electrical evidence |
| Firmware/simulation/measurement | `NOT_IMPLEMENTED/UNVERIFIED` | actual tool logs, runtime or physical independent test |
| Research I implementation | separate `RESEARCH_ONLY` brief seen | owner-reviewed I decision; no silent data-source substitutions |
| Research J scope | separate spec `NOT_AVAILABLE` | authoritative brief/owner review before dependent assumptions |
| Georgian-language OSS redistributability | depends on exact asset/license | legal/OSS ledger + dependency/asset review |

### 20.4 პირველწყაროთა კონსოლიდირებული მითითებები

მთავარი ტექნიკური მტკიცებულებები: [pinned repository/commit](https://github.com/donluka-23/Inventor_EDU/commit/2ece740bb49dfd330cbdecd4981204eb085821dd), [DEMO-001 report](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/DEMO-001-REPORT.md), [GPIO source/rule ledger](https://github.com/donluka-23/Inventor_EDU/blob/2ece740bb49dfd330cbdecd4981204eb085821dd/reports/CORE-001B-01_SOURCE_AND_RULE_LEDGER.md), [source-pinned ESP-IDF GPIO masks](https://raw.githubusercontent.com/espressif/esp-idf/880a203ae603d08a94d06aa01e0d6761958e5e9e/components/soc/esp32/include/soc/soc_caps.h), [board header source](https://raw.githubusercontent.com/espressif/esp-dev-kits/da43a78cfdd2a1122047bb5617ca79e09fd687b2/docs/en/esp32-devkitc/user_guide.rst). სამეცნიერო საფუძველი და შესაბამისი DOI/ნაშრომები ჩამოთვლილია §3-ში. ეს bibliography არის **კვლევითი დასაბუთების ბილიკი**, არა ამ ფაილში ნაგულისხმევი უფლებები პირველწყაროების ასლის გასავრცელებლად.

---

**ბოლო აკრძალვის გადამოწმება:** ეს არის დამოუკიდებელი კვლევითი ანგარიშის კანდიდატი. არ არის შექმნილი ინტერფეისი, API, Codex-ის შესასრულებელი დავალება, firmware, circuit synthesis engine, electrical safety verdict ან მფლობელის სახელით არქიტექტურული approval. ყველა ტიპი, JSON, workflow status, KPI, UI hint და Research I/J handoff არის `PROPOSED` და მათ ცვლილებებს მფლობელის ექსპლიციტური არჩევანი სჭირდება.
