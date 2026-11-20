# RESEARCH C — ელექტრული თავსებადობა, შეზღუდული ფიზიკური მოდელები და სამეცნიერო გამოთვლები

**პროექტი:** INVENTOR EDU · **შემოთავაზებული ქვესისტემა:** CORE-001C  
**კვლევისა და საჯარო წყაროების გადამოწმების თარიღი:** 2026-11-20, Asia/Tbilisi  
**სტატუსი:** დამოუკიდებელი საინჟინრო კვლევა და *დასამტკიცებელი* გადაწყვეტილების პაკეტი. **არ არის** გაშვებული პროგრამა, დამტკიცებული არქიტექტურა, რეალური აპარატურის გაზომვა, უსაფრთხოების სერტიფიცირება ან შესრულების დავალება.

**მტკიცებულების კლასები:** `[F]` — უშუალოდ პირველადი/ავტორიტეტული წყაროდან დადასტურებული ფაქტი; `[M]` — დადგენილი კანონიდან/გაცხადებული დაშვებებიდან გამოყვანილი მათემატიკური შედეგი; `[R]` — საინჟინრო რეკომენდაცია; `[U]` — დაუდასტურებელი მონაცემი ან არაგარანტირებული დაშვება. `PASS` ყოველთვის კონკრეტულ წესსა და სამუშაო არეალს ეხება, არასოდეს მთელ მოწყობილობას.

## 1. Executive recommendation — მთავარი გადაწყვეტილება

**[R] რეკომენდებულია: `evidence-gated voltage constraints + exact/bounded passive-circuit mathematics + independent findings for logic and stress`.** საწყისად საკმარისია ტიპიზებული ფაქტების შედარება, ორ-რეზისტორიანი გამყოფის ზუსტი ფორმულები, შეზღუდული დატვირთვის მოდელი, ინტერვალური უკიდურესობების გამოთვლა და შედეგის წყაროებთან მიკვლევადი მიბმა. **არ არის საჭირო საკუთარი SPICE, ზოგადი MNA solver ან მძიმე numerical dependency პირველ მიღების შემთხვევაზე.**

**გათვალისწინებული ძირითადი შედეგები:**

1. **[F]** Adafruit #3942-ის `Echo` აღწერილია როგორც 5V logic, ხოლო გაყიდული კომპლექტის ორი 10kΩ წინაღობა 5V-ის 2.5V-მდე შესამცირებლად არის რეკომენდებული [S03, S04]. ეს **არ არის გარანტირებული `VOH(min)`, `VOL(max)` ან დინამიკური გამოსასვლელი მოდელი**.
2. **[F]** Espressif-ის 2026-08-05 დოკუმენტი `ESP32-WROOM-32E/32UE Datasheet v2.1`, §6, Table 15, ასახელებს `VIH` ქვედა ზღვარს `0.75×VDD`, `VIL` ზედა ზღვარს `0.25×VDD` (ცხრილის ზოგადი კონტექსტი **3.3V, 25°C**). `VDD` არის შესაბამისი I/O domain-ის კვება [S01, S02].
3. **[M]** ნომინალურ 5V-ზე 10kΩ/10kΩ გამყოფი 2.500V-ს იძლევა. თუ `VDD=3.4V` და შესაბამისობა `VIH=0.75×VDD` ფორმულით ამ მდგომარეობაზეც დასაშვებია, მოთხოვნილი გარანტირებული HIGH დონე 2.550V ხდება: **მარაგი −0.050V**. ეს ნიშნავს *გარანტირებული HIGH-ის პირობის დაუკმაყოფილებლობას*, არა იმის მტკიცებას, რომ რეალური GPIO აუცილებლად LOW-ს წაიკითხავს.
4. **[M]** 6.8kΩ ზედა / 10kΩ ქვედა წინაღობა ნომინალურ 5V-ზე იძლევა 2.976190V-ს. წინასწარ ნავარაუდევი `Echo HIGH=4.50–5.25V` და ±1% წინაღობებით, *იდეალური არადატვირთული მოდელის* გამოთვლითი დიაპაზონია **2.656846–3.150250V**. `VDD=3.2–3.4V`-ზე ფორმალური მაღალი დონის ზღვართან ყველაზე ცუდი მარაგი **+0.106846V** გამოდის. **[U]** არ არის დასაბუთებული, რომ `Echo HIGH`-ის 4.50V მინიმუმი რეალურად გარანტირებულია, ამიტომ ამ გამოთვლიდან უპირობო hardware `PASS` არ მიიღება.
5. **[F/M]** ESP32-WROOM-32E-ის *module supply* `VDD33` absolute maximum `−0.3…3.6V` არის Table 13-ში; **ეს არ არის GPIO-ის abs-max შეყვანის ძაბვა**. Table 15-ის `VIH` მწკრივში არსებული `VDD+0.3V` **არც ცალკე გარანტირებული დაზიანების ზღვარია** [S01]. შესაბამისად **სიგნალის ამოცნობა, DC-characteristics envelope და ელექტრული სტრესის ვერდიქტი ცალ-ცალკე უნდა დარჩეს**.
6. **[R]** CORE-001C-ს დაუბრუნდეს `PASS / FAIL / INDETERMINATE / NOT_EVALUATED` *თითოეული check-ისთვის*, ცალკე `severity`, `reason_code`, პირობითობის/მტკიცებულების ხარისხის ნიშნებით. `CONDITIONAL` არის შედეგის **qualifier**, არა `PASS`-ის ფარული სინონიმი.

**გადაწყვეტილება კვლევის დონეზე:** **GO** ვიწრო, დემონსტრირებადი **მათემატიკური/კონსტრეინტის კონტრაქტის** დასამტკიცებლად; **NO-GO** „ყველაფერი უსაფრთხოა“, „ESP32 + HC-SR04 სრულად სიმულირებულია“ ან „აპარატურულად დამოწმებულია“ მარკეტინგული მტკიცებებისთვის. არაა შესრულებული დამოუკიდებელი hardware test, calibration ან ბრაუზერის ინტეგრაცია.

### 1.1 ფაილებიდან მიღებული პასუხისმგებლობის საზღვრები

| წინა მასალა | მიღებული ან გასათვალისწინებელი ვალდებულება | რა არ უნდა შეცვალოს RESEARCH C-მ |
|---|---|---|
| `RESEARCH_01_ENGINEERING_DATA_MODEL(3).md` | thin semantic core; variant/revision; condition-aware evidence; topology ≠ physical validity | canonical model-ის არსებითი სემანტიკა |
| `RESEARCH_02_COMPUTATIONAL_ARCHITECTURE(3).md` | V1–V3 deterministic/analytical დონეები; ngspice მხოლოდ gate-ით; შედეგის მრავალგანზომილებიანობა | V0–V6-ის ფენები და solver-ის საბოლოო შერჩევა |
| `RESEARCH_03_FIRST_CAPABILITY_AND_DEMO(3).md` | ESP32-DevKitC-32E + Adafruit #3942; direct `Echo`, 10k/10k და 6.8k/10k სცენარები; მკაცრი demo envelope | უცნობი მოწყობილობების ავტომატური მხარდაჭერა |
| `RESEARCH_A_ENGINEERING_MODEL_EXECUTION_CONTRACT(3).md` | `CircuitSnapshot`, `TopologyResult`, exact `TerminalRef`; immutability; evidence claims; მხოლოდ ideal conductor-ები ქმნის net-ს | CORE-001A ტოპოლოგიის ან ID-ების თავისებური ფორმატი |
| `Pasted text(20261120-122247).txt` | ამ ანგარიშის კვლევითი ამოცანა; 18 სავალდებულო განყოფილება; ფიზიკური/ლიცენზიური/სასწავლო შეზღუდვები | არ განხორციელდეს კოდი ან უპირობო არქიტექტურული დამტკიცება |

**საყურადღებო გადაკვეთა:** CORE-001A პირველ ეტაპზე აღწერს board-სა და sensor-ს; მის `DeviceDefinition.kind` არჩევანში შესაძლოა საერთოდ არ იყოს `resistor`. ამიტომ CORE-001C-ს **არ შეუძლია** ჩათვალოს, რომ რეზისტორები უკვე canonical topology-ში არსებობს. ქვემოთ წარმოდგენილია ორი კონტრაქტული ალტერნატივა, *CORE-001A მფლობელის დასამტკიცებლად*, ნაცვლად დამოუკიდებელი schema-მიგრაციისა.

## 2. Scientific and mathematical foundations — მეცნიერული საფუძვლები

### 2.1 ელექტრული კანონები

- **[M] ომის კანონი:** რეზისტორისთვის, მის დასაშვებ სამუშაო არეალში, `V=IR` და `P=VI=I²R=V²/R`. ნომინალური `R` არ უდრის უცვლელ სიდიდეს ტემპერატურისა და წარმოების ტოლერანსის მიუხედავად.
- **[M] კირხჰოფის დენის კანონი (KCL):** კვანძთან შემავალი და გამომავალი დენების ალგებრული ჯამი ნულია. სწორად გამოიყენება კვანძებთან, რომლებიც CORE-001A-მ რეალურ კონტაქტებად და მყარ ერთიან net-ებად განსაზღვრა.
- **[M] კირხჰოფის ძაბვის კანონი (KVL):** შეკრულ კონტურში ძაბვათა ალგებრული ჯამი ნულია შესაბამისი lumped/quasi-static მოდელის ფარგლებში. ძლიერი მაგნიტური ინდუქციის/განაწილებული პარამეტრების რეჟიმი სხვა მოდელს მოითხოვს.
- **[M] კვანძური ანალიზი:** პასიური ხაზოვანი DC წრედისთვის `G v = i`; ცნობილ voltage source-ებზე იდეალური წყაროს დენი დამატებითი უცნობი ხდება — **Modified Nodal Analysis (MNA)**. მისი სტანდარტული საფუძველია Ho–Ruehli–Brennan (1975) [S20]. *ზოგადი MNA-ის იმპლემენტაცია პირველი გამყოფისთვის საჭირო არ არის*.
- **[M] დენისა და ძაბვის თეორემული გამარტივება:** ცნობილი, ხაზოვანი ორი-ტერმინალიანი დატვირთვებისათვის Thevenin/Norton ეკვივალენტები შეიძლება გამოყენებულ იქნას. აქტიური sensor output-ისათვის ასეთი ეკვივალენტი უნდა დაეყრდნოს ცნობილ `I–V`/output-impedance მახასიათებელს, არა სახელწოდებას „5V logic“.

### 2.2 რატომ არ იძლევა ტოპოლოგია ელექტრულ ჭეშმარიტებას

`Echo → Rtop → node → GPIO` და `node → Rbottom → GND` განსაზღვრავს *ტოპოლოგიურ* ფიგურას. `GPIO` მაღალ-წინაღობიანად თუ განიხილება, ეს ცალკე **ელექტრული დაშვებაა**. თუ `Echo` ვერ აწვდის divider-ის საჭირო დენს, სიგნალი შეიცვლება. თუ GPIO input ჩართულია შიდა pull-up/down-ით ან უცნობი დამცავი დიოდით, გამყოფი აღარ არის იდეალურად არადატვირთული. ფიზიკური ქცევა იწყება **კომპონენტების მოდელის, პირობებისა და წყაროს/მიმღების ფიზიკური მტკიცებულების** არსებობის შემდეგ.

### 2.3 ოთხი დამოუკიდებელი სისწორე

1. **მათემატიკური:** ფორმულა/უკიდურესობები სწორია მიღებული მოდელისთვის.
2. **მოდელის ვალიდურობა:** ელემენტი და სამუშაო რეჟიმი შეესაბამება რეალურ განსაზღვრულ აპარატურას.
3. **ნუმერიკული:** გამოთვლა ამოხსნილია საკმარისი სიზუსტით; `converged` ნიშნავს მხოლოდ რიცხვით ამოხსნას.
4. **ემპირიული:** დამოუკიდებელი გაზომვები ემთხვევა პროგნოზს წინასწარ აღწერილი გაურკვევლობისა და operating envelope-ის ფარგლებში. JCGM GUM იცავს ამ განსხვავებას [S19].

**[R]** ერთი „accuracy“ მეტრიკა ოთხივე დონის შეფასებას ვერ ჩაანაცვლებს. უნდა გაიმიჯნოს `math_verified`, `model_evidenced`, `numerically_resolved`, `bench_validated`.

## 3. Existing numerical and circuit-analysis implementations

| კანდიდატი / განხილული ვერსია | ფუნქცია და საზღვარი | დასაწყისში | ვერდიქტი |
|---|---|---|---|
| Python stdlib 3.12 (`fractions`, `decimal`, `math`, `hashlib`) | ზუსტი რაციონალური გამოთვლა დეციმალური input-იდან; კონტროლირებადი ფორმატირება; დამოუკიდებელი კოდის მცირე ზედაპირი [S12] | runtime უკვე Python-ია CORE-001A კანდიდატში | **[R] ძირითადი** |
| NumPy **2.5.x** (დადასტურებული 2.5.5 patch, 2026-11) | `numpy.linalg.solve`, `numpy.linalg.cond`; dense linear circuits; floating point [S13] | მხოლოდ ზოგადი `Gv=i` საჭიროებისას | **[R] defer** |
| SciPy **1.18.1** (2026-08) | `scipy.linalg.solve`, `scipy.sparse.linalg.spsolve` — დიდი ან sparse ქსელი [S14] | ზედმეტი ორ-რეზისტორიანი მოდელისთვის | **[R] defer** |
| SymPy **1.14.0** | `Matrix.LUsolve`, `Rational`, symbolic expression validation [S15] | research/test oracle, არა per-drag runtime | **[R] test-only optional** |
| Pint **0.26.2** (2026-10) | `UnitRegistry`, `Quantity.to()`; dimensional safety [S16] | რამდენიმე SI სიდიდე შესაძლებელია მკაცრი schema conversion-ით | **[R] optional, scope gate** |
| mpmath **1.4.1** | `iv.mpf` arbitrary-precision interval evaluation; *interval support experimental* [S17] | უსაფრთხოების შედეგისთვის არაგამოყენებადი ალტერნატივა დამატებითი აუდიტის გარეშე | **[R] not core** |
| PyInterval / `pyinterval` ძველი პაკეტი | interval package ისტორიული, მიმდინარე support/compatibility საკმარისად არ დადასტურდა [S18] | არ შეიძლება production-bounds ნდობის ავტომატური გაცემა | **[U] not approved** |
| ngspice **47** (2026-08-11) | `.op`/DC, `.tran`, netlist, external process ან shared library [S21, S22] | model + analysis + license gate | **[R] gated optional** |
| KiCad **10.x** | ERC / netlist export; schematic/visual reference; ngspice interface | არ ფლობს exact `Echo` output guarantee-ს და ESP32-ის power safety-ს [S23] | **[R] comparator only** |
| Xyce **7.10** | მაღალი წარმადობის SPICE-თან ახლოს მდგომი circuit simulation; GPLv3 [S24] | არ არსებობს პირველი დატვირთვის საჭიროება | **[R] reject as dependency** |

**[U]** ამ ვერსიებით LIVE ტესტირება/benchmark ამ კვლევაში არ ჩატარებულა. „განხილული“ ნიშნავს upstream-ის ოფიციალური interface/license/release ინფორმაციის გადამოწმებას, არა იმას, რომ პაკეტები დაინსტალირდა და წარმატებით ინტეგრირდა. ნამდვილი dependency lock უნდა გამოცხადდეს ცალკე approval/compatibility gate-ზე.

## 4. Exact reusable functions and APIs — რა უნდა გამოიყენოს არსებული კოდიდან

| ოპერაცია | კონკრეტული არსებული API/მექანიზმი | როდის არის გამართლებული | ზღვარი |
|---|---|---|---|
| ზუსტი decimal→rational | `fractions.Fraction` decimal-string / integer numerator-denominator | 6.8kΩ, 10kΩ, ±1%, 4.50V და სხვა შეზღუდული რაციონალური input | ითვლის **ზუსტად** მოდელს, არა დანადგარის გაზომვებს |
| decimal display / გარეთ დამრგვალება | `decimal.Decimal`, `Context`, `localcontext`, `ROUND_FLOOR`/`ROUND_CEILING` [S12] | საბოლოო ქვედა/ზედა საზღვრის `down/up` ფორმატირება | მარტო default `ROUND_HALF_EVEN` არ არის rigorous outward bound |
| dense სისტემის ამოხსნა | `numpy.linalg.solve(A,b)`, `numpy.linalg.cond(A)` [S13] | ახალი მხარდაჭერილი მცირე ზოგადი ხაზოვანი ქსელი, ცალკე gate-ის შემდეგ | ill-conditioned matrix; singular; float rounding |
| dense/sparse solver | `scipy.linalg.solve(A,b)`, `scipy.sparse.linalg.spsolve(A,b)` [S14] | ზომის/სისწორის საჭიროება გაზომილია | solver residual + condition აუცილებელია; sparse permutation შეიძლება განსხვავდეს |
| სიმბოლური oracle | `sympy.Rational`, `sympy.Matrix(...).LUsolve(...)` [S15] | independent symbolic test basis | მსგავსი ფორმულის გადაკოპირება არ ითვლება independent evidence-ად |
| ერთეულების კონვერტაცია | `pint.UnitRegistry`, `Quantity.to('volt')` [S16] | დიდი catalog და სხვადასხვაგვარი unit expressions | ვერ ავსებს უცნობ `VOH`/`Vin,max`; dimensional check ≠ correct electronics |
| interval library | `mpmath.iv.mpf` [S17] | nontrivial experimental comparison | დოკუმენტაცია ამბობს experimental; პირდაპირ safety gate-ში არ უნდა მოხვდეს |
| ngspice standalone | CLI batch execution (`-b`) და SPICE `.op`/`.tran`; გამომავალის structured parsing [S21] | სიმულაციის უფლება და სრული ბიჰევიორული მოდელი | process sandbox; timeout, memory, file/command restrictions |
| ngspice embedded | upstream `sharedspice.h`/`sharedspice.c`, `ngSpice_Init` ტიპის shared API [S22] | მხოლოდ დამტკიცებული trusted workload | in-process native code ართულებს crash/isolation-ს |
| KiCad | `kicad-cli sch erc`, `kicad-cli sch export netlist` [S23] | cross-check სქემური graph / symbol metadata | არა ESP32-ის electrical survival oracle |

**[R] მატერიალური დამოკიდებულების ტესტი:** სანამ დაემატება ახალი library, უნდა არსებობდეს ისეთი მხარდაჭერილი ამოცანა, რომლის ამოხსნისას `stdlib` არჩევანი measurable ცუდია **სისწორით, დოკუმენტირებული შენარჩუნებადობით ან შესრულების ხარჯით**. სუბიექტური „მომავალში შეიძლება დაგვჭირდეს“ საკმარისი არ არის.

## 5. Electrical-compatibility constraint model

### 5.1 ჩანაწერები და ტერმინები

| პარამეტრი | ზუსტი მნიშვნელობა/ტიპი | როდის დასაშვებია |
|---|---|---|
| `V_nom` | მხოლოდ nominal; ერთი დიზაინის საორიენტაციო წერტილი | **არა** guaranteed bound |
| `V_source_high = [VOH_min, VOH_max]` | გამოსასვლელი HIGH **გარანტირებული** დიაპაზონი კონკრეტული დენისა და რეჟიმისთვის | maker-grade claim; source current dependence |
| `V_source_low = [VOL_min, VOL_max]` | LOW დიაპაზონი | maker-grade claim; sink/drive conditions |
| `VIH_min(VDD, mode, T)` | მიმღების HIGH-ის გარანტიისათვის საკმარისი შესასვლელი დონე | exact pin domain და მოქმედი პირობები |
| `VIL_max(VDD, mode, T)` | LOW-ის გარანტიისათვის საკმარისი ზედა დონე | exact pin domain და მოქმედი პირობები |
| `Vin_recommended_range` | ოპერაციის დადასტურებული დიაპაზონი | **არ უდრის** absolute maximum stress limit-ს |
| `Vin_absolute_max/min` | მწარმოებლის კონკრეტული *pin/input*-ის stress rating | საჭიროა safety/stress check; ნუ ჩაანაცვლებთ `VDD33`-ის rating-ით |
| `I_source_max`, `I_sink_max` | დასაშვები drive/load condition; fixed state | დატვირთული divider-ის შეფასება |
| `I_input_leakage`, `R_input`, `C_input` | შესასვლელის დატვირთვა/დინამიკა | ცნობილი რეჟიმი/ტემპერატურა; თუ არა — `UNKNOWN` |
| `I_clamp`, `power_off_state`, `V_transient` | protection/injection/sequence/overshoot | მხოლოდ შესაბამისი maker-grade მონაცემებით ან გაზომვით |

### 5.2 ფორმალური მოთხოვნები

**[M] გარანტირებული HIGH** ამ შეზღუდულ, დოკუმენტირებულ რეჟიმში მხოლოდ მაშინ აკმაყოფილებს მოთხოვნას, თუ:

`min(V_source_high_at_receiver) ≥ max_applicable(VIH_min)`.

**[M] გარანტირებული LOW** მხოლოდ მაშინ:

`max(V_source_low_at_receiver) ≤ min_applicable(VIL_max)`.

**[M] DC operating-domain** ტესტი მოითხოვს, რომ **ყველა** დასაშვებმა წყაროს მდგომარეობამ და დაცულმა კონტექსტმა დააკმაყოფილოს კონკრეტული `Vin_recommended_range` (თუკი ასეთი სრულადაა დადგენილი). **Stress/survival** სხვა, ცალკე ინვარიანტია `Vin_absolute_*`, injection/overshoot/power-off დოკუმენტაციით. დამტკიცებული `VIH` მარტო stress gate-ს ვერ ხურავს.

**[M] საჭირო current budget:** მაქსიმალური მოთხოვნილი მიმდინარე დენი `I_required_max ≤ I_source_available_min`, *იმავე output voltage/temperature/state-ის პირობებში*. `5V logic` არ იძლევა output current-ის ამ რიცხვებს. Divider-ის მოთხოვნილი დენის გამოთვლა შეიძლება, მაგრამ შესაბამისი სენსორის drive-capability **დაუდასტურებელი რჩება**.

**[M] ზღვრის თანასწორობა:** `≥` ან `≤` ნიშნავს spec-ის ფორმალურ საზღვარზე ყოფნას, თუ spec-ი ზუსტად და მთელი საჭირო conditions-ით მოქმედებს. მაგრამ `zero margin` რეალურ სამყაროში მაღალი მგრძნობელობის შემთხვევაა — არ უნდა დამრგვალდეს დადებით მარაგამდე; UI-ში შეუძლია warning `ZERO_MARGIN`.

**გამოტანის ლოგიკა:**

- `FAIL` — **დადგენილი წესის** დარღვევა, მაგ. მოდელის შესაძლო ყველა მდგომარეობაში გარანტირებული HIGH **ვერ მტკიცდება**, ან კონკრეტული *დოკუმენტირებული limit* აუცილებლად გადაჭარბებულია. მიზეზში აუცილებელია შემოწმებული წესი და არ შეიძლება „hardware აუცილებლად დაზიანდა“ შემოწმების გარეშე.
- `PASS` — ყველა აუცილებელი **ამ კონკრეტული წესის** მონაცემი ხელმისაწვდომია, პირობები შეესაბამება და უტოლობა დაცულია. სხვა, დამოუკიდებელი stress ან timing check შეიძლება `INDETERMINATE` დარჩეს.
- `INDETERMINATE` — ინტერვალები კვეთს ზღვარს, წყარო არასრულია, პირობები დაუდგენელია ან ერთმანეთთან კონფლიქტშია. შეიძლება დაბრუნდეს `conditional_on_assumptions=true` გამოთვლითი მაგალითისთვის, მაგრამ არა უეჭველი მტკიცება.
- `NOT_EVALUATED` — დასმული კითხვა მიმდინარე computational scope-ს სცდება; მაგალითად, ESD/transient/boot sequencing.

**[R] მნიშვნელოვანია `FAIL`-ის ორი სხვადასხვა მიზეზი:** `LIMIT_VIOLATION_PROVEN` და `GUARANTEED_HIGH_NOT_ESTABLISHED` ერთსა და იმავე „მოწყობილობა დაიწვება“ დასკვნაში არ გადაიქცეს. `VIH`-ზე დაბალი წაკითხვა არაა ლოგიკური LOW-ის გარანტია, არამედ გარდამავალი/არადადგენილი ზონა შეიძლება იყოს.

### 5.3 ურთიერთსაწინააღმდეგო მტკიცებულებების მართვა

თუ ორი სხვადასხვა რევიზიის datasheet განსხვავებულ მნიშვნელობას იძლევა, თუ ერთმა seller page-მ „safe“ უწოდა შედეგს და მოდულის კონკრეტული `VIH` მოითხოვს მეტს, არცერთი წყარო არ შთანთქავს მეორეს. გაარჩიეთ **(i) თვითონ რიცხვები, (ii) მოქმედების არეალი, (iii) იმპორტირებული ვარიანტი, (iv) source authority**, და დაბრუნდეს `CONFLICTING_EVIDENCE` ან scope-specific reasoning. **[R]** user override მხოლოდ `assumption`-ის როლში შეიძლება, არა maker guarantee-ის ჩანაცვლება.

## 6. Manufacturer-data completeness and evidence audit

### 6.1 ცხრილი: სად არის ფაქტი, სად — მხოლოდ კონცეპტუალური სახელწოდება

| მტკიცება/მონაცემი | წყარო და ლოკატორი | კლასი | შედეგი CORE-001C-სთვის |
|---|---|---|---|
| ESP32-WROOM-32E/32UE **v2.1**, 2026-08-05 | Espressif ოფიციალური დოკუმენტების ინდექსი [S02]; `Datasheet` [S01] | **[F]** | snapshot-ში pinned doc/revision |
| Module `VDD33` absolute maximum `−0.3…3.6V` | [S01], Table 13, გვ.28 | **[F]** | **არ** ჩაწეროთ როგორც GPIO Vin(abs-max) |
| Module recommended `VDD33 3.0…3.6V` | [S01], Table 14, გვ.28 | **[F]** | supply domain input, **არა** 3V3 header-ის რეალური გაზომვა |
| `VIH`: `0.75×VDD` → `VDD+0.3V`; `VIL`: `−0.3V` → `0.25×VDD`; `I_in high/low` max `50nA` | [S01], Table 15 **DC Characteristics (3.3 V, 25°C)**, გვ.28–29 | **[F]** | mode/domain/T conditions; ვრცელდება მხოლოდ დასაბუთებულ რეჟიმზე |
| `VDD` შესაბამისი I/O power domain-ის ძაბვაა | [S01], Table 15 შენიშვნა, გვ.29 | **[F]** | არა ყოველ terminal-ზე მხოლოდ generic `3.3` |
| DevKitC V4 USB/5V/3V3 კვების სამი *ურთიერთგამომრიცხავი* გზა | [S05], Power Supply Options | **[F]** | USB-only initial context; პარალელური feeding არასწორია |
| დაფაზე GPIO18/19 I/O, GPIO34 Input-only; 6–11 შიდა flash | [S05], Header Block | **[F]** | ეს CORE-001B-ის ცალკე პასუხისმგებლობაა |
| Adafruit #3942 HC-SR04 5V logic Echo; Trig 3V/5V; 2×10kΩ რეკომენდაცია | [S03], Description / Technical Details | **[F]** seller-declared | კონცეპტუალური output class; **არა** manufacturer-bound waveform |
| `Echo VOH_min`, `Echo VOL_max`, `Rout`, `Iout`/drive curve, `tr/tf`, overshoot | Adafruit #3942 საჯარო აღწერაში ვერ იქნა ნაპოვნი [S03–S04] | **[U]** | `MISSING_OUTPUT_LEVEL_BOUNDS`, `MISSING_DRIVER_MODEL` |
| sensor-ის maker/PCB revision exact | #3942 retailer SKU ასახელებს პროდუქტს; exact PCB fabrication revision არა | **[U]** | არ გათანაბრდეს ყველა HC-SR04 clone-სთან |
| board-ის რეალური 5V `Echo` supply 4.75–5.25V | არც [S03], არც [S05] არ იძლევა ზუსტად ამ კონკრეტული assembled path-ის სრულ measured guarantee-ს | **[U]** | მხოლოდ declared simulation assumption |
| model `Echo HIGH=4.50–5.25V`, `LOW=0–0.30V` | წინა Research03-ის სცენარის *assumption* | **[U]** | არ ჩაიტვირთოს maker catalog fact-ად |
| `VDD=3.2–3.4V` | Research03-ის *assumption*; actual USB-board rail measurement არაა | **[U]** | conditionally evaluate; ნუ შეერევა 3.0–3.6V recommended range-ში |
| YAGEO `MFR-25FBF52-6K8`/`...-10K`, ±1%, 0.25W | [S06–S07] distributor catalog; exact manufacturer original specsheet აქედან დამოუკიდებლად არ გაიხსნა | **[F] distributor-listed, [U] maker-primary** | precision assumption დოკუმენტაციით pending; physical part ID უნდა შემოწმდეს |

**გამორიცხვა:** Adafruit-ის უფრო ზოგად `Ultrasonic Sonar Distance Sensors` გვერდზე ერთ გვერდზე საუბარია რამდენიმე sensor variant-ზე, მათ შორის 3V/5V და UART ვარიანტებზე [S04]. მისი ერთ-ერთი ზოგადი ფრაზის მიჩნევა #3942-ის exact maker guarantee-ად შეცდომაა. #3942-ის retailer product page-ს აქვს პრიორიტეტი იმისთვის, თუ **რას ყიდის Adafruit**, მაგრამ ის არ უდრის ჩიპის silicon characterization-ს.

### 6.2 მონაცემების სიზუსტის წინაპირობები

- [R] ყველა `ElectricalProperty` მოითხოვს `quantity_kind`, SI unit, `bound_kind` (`guaranteed_min`, `guaranteed_max`, `typical`, `absolute_rating`, `assumed`, `measured`), `source_id`, PDF/HTML `locator`, vendor/board/SoC scope, test condition, date, revision.
- [R] `VDD=3.4V` მაგალითზე Table 15-ის ფორმულის გავრცელება **გაცხადებულ მოდელურ ექსტრაპოლაციად** აღირიცხოს: ცხრილის სათაური 3.3V, 25°C-ია, ხოლო ფორმულის ალგებრული დამოკიდებულება VDD-ზე არ ნიშნავს დაუზუსტებელი ტემპერატურული/რეჟიმული მუშაობის სრული გარანტიის დამტკიცებას.
- [R] App UI-ში `5V` rail label არ უნდა გადაიქცეს `4.75–5.25V` maker guaranteed output-ად; ადეკვატური სისტემისთვის საჭიროა board-specific rail path და measured/specified range.

## 7. Bounded divider and linear-network computations

### 7.1 იდეალური, არადატვირთული გამყოფი

**[M]** ორი იდეალური დადებითი წინაღობისა და იდეალური ძაბვის წყაროსათვის:

\[
V_o = V_i\frac{R_b}{R_t+R_b},\qquad I = \frac{V_i}{R_t+R_b},\qquad P_t=I^2R_t,\quad P_b=I^2R_b.
\]

`R_t` = `Echo → midpoint` ზედა წინაღობა; `R_b` = `midpoint → GND` ქვედა წინაღობა. `GPIO`-ის ეფექტიანი შესასვლელი დენი ნულია **მხოლოდ ამ მოდელში**.

**ინტერვალის საზღვრების მტკიცებულება [M]:** როდესაც `V_i≥0`, `R_t>0`, `R_b>0`, და დასაშვები კუთხეები ქმნის დამოუკიდებელ rectangular bound-set-ს, მაშინ

\[
\frac{\partial V_o}{\partial V_i}=\frac{R_b}{R_t+R_b}>0,\qquad
\frac{\partial V_o}{\partial R_t}=-\frac{V_iR_b}{(R_t+R_b)^2}\le0,\qquad
\frac{\partial V_o}{\partial R_b}=\frac{V_iR_t}{(R_t+R_b)^2}\ge0.
\]

ამიტომ **ზუსტი** უკიდურესობები ამ მოდელისთვისაა:

`Vout_low = Vin_low × Rb_low / (Rt_high + Rb_low)`;
`Vout_high = Vin_high × Rb_high / (Rt_low + Rb_high)`.

თუ inputs ერთმანეთზეა დამოკიდებული, სრული rectangular box მაინც შეიცავს ყველა დასაშვებ მდგომარეობას **მხოლოდ იმ შემთხვევაში**, თუ მოცემული ინდივიდუალური საზღვრები მართლაც მოქმედი გარე bounds-ია. შედეგი მაშინ გარეთა (conservative) enclosure-ია, მაგრამ შეიძლება არარეალისტურად ფართო იყოს. **თუ `Echo` მაღალი ძაბვა თვითონ divider-ის დატვირთვის ფუნქციაა და მის დასადგენად ინფორმაცია არ არსებობს, `Vin_high/low` არ არის დადასტურებული და ეს enclosure ფიზიკური გარანტია ვერ გახდება.**

### 7.2 სავალდებულო რიცხვითი შემთხვევები

| სცენარი | წინაპირობები | `Vout` შედეგი | აღსანიშნავი შეზღუდვა |
|---|---|---|---|
| **Adafruit: 10kΩ/10kΩ** | `Vin=5.00V`, ideal no-load | **2.500000V** | `VDD=3.4V` პირობით `VIH=2.550V`: margin **−0.050V** |
| 10kΩ/10kΩ worst-case | `Vin HIGH=4.50–5.25V`, ორივე ±1% | **2.227500–2.651250V** | model assumptions, არა maker guarantee |
| **6.8kΩ/10kΩ nominal** | `Vin=5.00V`, ideal no-load | **2.976190V** | `I=5/16.8k≈0.297619mA` |
| 6.8kΩ/10kΩ HIGH extrema | `Vin HIGH=4.50–5.25V`, `Rt=6.8k±1%`, `Rb=10k±1%` | **2.656846–3.150250V** | `VIH(3.4)=2.550V`: conditional margin **+0.106846V** |
| 6.8kΩ/10kΩ LOW upper | `Vin LOW≤0.30V`, ±1% | **0.180014V** | `VIL(3.2)=0.800V`: conditional LOW margin **+0.619986V** |
| **შებრუნებული 10kΩ/6.8kΩ** | `Vin=5V`, no load | **2.023810V** | ratio-შეცდომა; არ არსებობს გარანტირებული HIGH |
| შებრუნებული 10kΩ/6.8kΩ extrema | HIGH assumptions ზემოთ, ±1% | **1.799786–2.150346V** | assurance for HIGH fails under stated model |

**სიფრთხილე:** 6.8k/10k model-high ზედა 3.150250V ნაკლებია `VDD_min=3.2V`-ზე ფორმალურად დამოკიდებულ DC `VDD+0.3=3.5V`-ზე. **მაგრამ ეს შუალედური შედარება არც GPIO absolute maximum-ს ადგენს, არც რეალურ overshoot/power-off უსაფრთხოებას.** მოქმედი `Vin(abs-max)` არ არის დადასტურებული [S01].

### 7.3 დატვირთული გამყოფი — ორი ერთმანეთისგან განსხვავებული მოდელი

**[M] Resistive load (ფიზიკური ეკვივალენტი მხოლოდ მაშინ, თუ მართლაც რეზისტიულია):**

\[
R_{eq}=\frac{R_bR_L}{R_b+R_L},\qquad V_o=V_i\frac{R_{eq}}{R_t+R_{eq}},\quad R_L>0.
\]

`R_eq` მატულობს `R_b`-ისა და `R_L`-ის ზრდასთან ერთად. ამიტომ `Vout` ასევე იზრდება `R_b`, `R_L`, `Vin` ზრდასთან და მცირდება `R_t` ზრდასთან; მონოტონურობით გამართლებული corner-evaluation მოქმედებს **თუ** `R_L` სტატიკურია, დადებითი და მისი შესაბამისი bounds მითითებულია. **გამოთვლითი მაგალითი:** `Vin=5V`, `Rt=6.8kΩ`, `Rb=10kΩ`, `R_L=100kΩ` → `R_eq≈9090.909Ω`, `Vout≈2.860412V`.

**[M] Fixed input leakage-current model (სხვა მოდელია, არ უნდა შეერიოს resistive load-ს):**

\[
V_o=V_{i}\frac{R_b}{R_t+R_b}-I_{leak}\frac{R_tR_b}{R_t+R_b}
\]

სადაც დადებითი `I_leak` ნიშნავს დენს, რომელიც კვანძიდან receiver-ში გადის. `R_th=Rt||Rb`; 6.8kΩ/10kΩ-ზე nominal `R_th≈4047.619Ω`; მხოლოდ **ილუსტრაციისთვის** `I_leak=50nA` → `~0.0002024V` ძაბვის ცვლა. Espressif Table 15-ში 50nA სპეციფიკაციას აქვს საკუთარი 3.3V/25°C პირობები [S01]; **არ გამოიყენოთ** ავტომატურად სრული ტემპერატურული/ჩატვირთვის ზღვარისათვის.

**[R]** model type (`OPEN_INPUT`, `RESISTIVE_LOAD`, `FIXED_LEAKAGE_CURRENT`) უნდა იყოს explicit. თუ user-only input assumption არის `Rin=∞`, ეს შედეგს შეუძლია განმარტოს, მაგრამ **ვერ ხურავს missing physical-load requirement-ს**.

### 7.4 დენი, სიმძლავრე და გამომავალი საფეხურის რეალური დატვირთვა

**[M]** 6.8k/10k, 5.25V, ორივე −1% → `I≈0.315657mA`. იდეალურ მოდელში corner-check-ით თითო რეზისტორზე მაქსიმალური დისიპაცია ამ დახურულ bounding-box-ში დაახლოებით `P_top≤0.673mW`, `P_bottom≤0.987mW`. ეს ბევრად ნაკლებია distributor-listed 0.25W ნომინალურ rating-ზე [S06–S07], **მაგრამ** სიმძლავრის შედარება საჭიროა maker-სერიის ტემპერატურული დერეიტინგისა და გარემოს პირობების გარეშე არ განზოგადდეს. მთავარი დაუფარავი პირობა არის **HC-SR04-ის გამომავალი საფეხურის რეალური current-drive / `VOH(Iout)`**.

### 7.5 მომავალი ხაზოვანი ქსელები — არა პირველადი ასაწყობი solver

**[M]** ზოგადი დადებითი რეზისტორული ქსელი reference ground-ით და ცნობილ წყაროებთან: KCL/Ohm → `Gv=i`; ideal voltage source-ებისათვის MNA. დასაშვებია მხოლოდ შემდეგი პირობებით: unambiguous netlist, known source and load values, nonzero finite resistances, consistent voltage references, full-rank/non-singular model, explicitly stated precision. Native linear solve-ის შედეგი არ ნიშნავს, რომ diode, semiconductor sensor, protection clamp ან firmware ქცევა წარმოდგენილია. ახალ workload-ზე გადადით NumPy/SciPy-მდე, **არ გააკეთოთ ახალი SPICE clone** [S13, S14, S20].

## 8. Numerical precision, interval methods and uncertainty

**[R] პროცედურა CORE-001C-სათვის:**

1. **Input parsing:** მხოლოდ აშკარა, ტიპიზებული სიდიდე და ერთეული, მაგ. `"6.8"`+`"kOhm"`; უარყავით NaN/∞, `R≤0` სტატიკური resistor-თვის, ნეგატიური tolerance, mismatched units, მცდარი decimal commas თუ საერთაშორისო input contract არ ითვალისწინებს.
2. **Internal exact math:** two-resistor + rational fixed-current მოდელისათვის გამოიყენეთ decimal-string→`Fraction` (`Fraction('6.8')`-ის ტიპის განმარტება). რეგულარული დეციმალური პარამეტრები რაციონალურებია და algebraically ზუსტად შეიძლება შეფასდეს. ეს გამორიცხავს float-ის boundary misclassification-ს, თუმცა რეალური მოდელის uncertainty უცვლელია.
3. **Bound report:** გამოიტანეთ exact rational comparison; UI-ის decimal bounds ფორმატირეთ *outward*, მაგ. ქვედა 2.656846374… → `2.656846` **დაბლა**, ზედა 3.150249524… → `3.150250` **მაღლა**. გარეთ დამრგვალებული ცხრილი უნდა ატარებდეს `rounded_outward=true`.
4. **No false precision:** აჩვენეთ source measurement precision/tolerance და არ თქვათ, რომ ნაჩვენები 6-decimal-იანი რიცხვი რეალურად დამზომილი 6-decimal-იანი ძაბვაა.
5. **General solver gate:** floating-point `solve`-ის შემდეგ აღირიცხოს residual norm `||Av−b||`, normalization scale, estimated condition, solver tolerance; near-boundary unresolved result = `INDETERMINATE` თუ ვერ მიიღწა conservative error enclosure.
6. **Interval package:** არ აირჩეს მხოლოდ სახელით. `mpmath.iv` ოფიციალურად experimental-ია [S17]; `pyinterval` maintenance/precision/compatibility audit დაუსრულებელია [S18]. ამ ამოცანისთვის analytic monotonic endpoint evaluation **უფრო ძლიერი და მცირე** კონტრაქტია.

### 8.1 მგრძნობელობა და საერთო წყაროზე დამოკიდებულება

**[M]** `f=V Rb/(Rt+Rb)` ფორმულიდან მცირე ცვლილებებისთვის:

\[
\frac{\delta V_o}{V_o}\approx\frac{\delta V_i}{V_i}
-\frac{R_t}{R_t+R_b}\frac{\delta R_t}{R_t}
+\frac{R_t}{R_t+R_b}\frac{\delta R_b}{R_b}.
\]

ეს არის **ლოკალური first-order sensitivity**, არა worst-case bound-ის შემცვლელი. თუ `Vin` და `VDD` დამოკიდებულია ერთ USB supply-ზე, HIGH margin `Vout(VUSB) − 0.75×VDD(VUSB)` უნდა შეფასდეს **ერთიანი feasible-domain**-ის საზღვრებში, და არა აბსურდული არარეალიზებადი extrema-ს მხოლოდ დამოუკიდებლად კომბინირებით. დამოუკიდებელი boxed extrema შეიძლება უსაფრთხო (conservative) იყოს, თუ ორივე გარე ზღვარი ნამდვილად დამტკიცებულია, მაგრამ შედეგს მკაცრი `PASS` მნიშვნელობის გარეშე დარჩენა შეიძლება.

### 8.2 uncertainty არ არის probability by default

**[F]** BIPM/JCGM 100 აყალიბებს გაზომვის გაურკვევლობის აღწერას; JCGM 101 განიხილავს probability-distribution propagation-ს Monte Carlo მეთოდით [S19]. **[R]** undocumented resistor batch variation-ისთვის ან sensor driver-ისთვის ნორმალური/ერთგვაროვანი განაწილების „მოსახერხებლად“ გამოგონება აკრძალულია. ყველაზე ცუდი დადასტურებული bound, measurement uncertainty და model inadequacy სამი დამოუკიდებელი რამაა.

### 8.3 შეჩერების საზღვრები

**[R]** თუ snapshot-ს არ აქვს signal ground-ის დასტური, proper resistor placement, maker-grade HIGH/LOW bounds, source/load model ან required pin absolute rating, CORE-001C მაინც აგენერირებს *სასწავლო, პირობითი არითმეტიკის* შედეგს, მაგრამ corresponding physical guarantee/status რჩება `INDETERMINATE`/`NOT_EVALUATED`-ში. „მონაცემი არ გვაქვს“ არ არის ნულოვანი შეცდომა.

## 9. Device-independent computational architecture

**[R] დაბალბიუჯეტიანი ჩანაცვლებადი ფენები:**

```text
CORE-001A immutable CircuitSnapshot + TopologyResult + pinned CatalogSnapshot
                              |
                  [read-only adapter / validator]
                              |
      Signal/domain facts + physical-property EvidenceClaims
                              |
      contextual rule eligibility (identity, mode, T, supply, load)
                              |
  +---------------------+----------------------------+
  | electrical limits   | passive analytical model   |
  | logic / DC / stress | divider / resistance / I/P |
  +---------------------+----------------------------+
                              |
       independent typed Findings + computation provenance
                              |
        educational Georgian formatter + stable UI anchors
                 (not truth, not calculation)
```

**მოდულის პასუხისმგებლობები:**

- `property_resolver` — დააბრუნებს pinned, type-correct, scope-valid claims; unknown/contradiction flag. **არ** გამოიგონებს დაკარგულ მონაცემებს.
- `domain_check` — გადამოწმებს supply/logic/DC/stress/sequence-ის კონკრეტულ უტოლობებს. ერთი domain check მეორეს არ შთანთქავს.
- `analytical_model` — გამოიყენებს მხოლოდ წინასწარ დაშვებულ topology motifs-ს; `LIMITED_DIVIDER_2R`, `LOADED_DIVIDER_RESISTIVE`, `LEAKAGE_CURRENT` და შემდეგ სხვა explicit model IDs.
- `result_protocol` — ფორმატს, evidence IDs, assumptions, affected nets, math proof/bounds და rule versions; locale-independent values.
- `solver_adapter` — **ამ ეტაპზე არ არის dependency**; შემდგომში კონკურენტმა tool-მა მხოლოდ გამოთვლის შედეგი უნდა დააბრუნოს, არ შეცვალოს canonical topology.

**[R] plugin/engine interop:** მოდელი და constraints არიან წესების და source records-ის საფუძველზე, არა `adafruit`-ზე hardcoded conditionals. ახალი sensor/board-ის დამატება მოითხოვს data-profile + same generic checks; ახალი ფიზიკა — ახალ მოდელს და acceptance case-ს, არა default fallback-ს „ყველა სენსორის სიმულაცია“.

## 10. Proposed integration interfaces — მხოლოდ დასამტკიცებელი კონტრაქტი

**[R] proposed input logical signature, *not application code*:**

`EvaluateElectrical(topology: TopologyResult, circuit: CircuitSnapshot, catalog: CatalogSnapshot, context: OperatingContext, assumptions: AssumptionSet, required_checks: CheckSet) -> ElectricalEvaluation`

| Input | სავალდებულო შინაარსი | გადამოწმების წესი |
|---|---|---|
| `CircuitSnapshot` | immutable `instances`, `conductors`, `catalog_digest`, SHA; `schema_version` | `snapshot_sha256` matches topology |
| `TopologyResult` | stable `terminal_to_net`, `nets`, reference IDs | must not infer connected nets from 2D coordinates |
| `CatalogSnapshot` | concrete `DeviceIdentity`, terminal mappings, `EvidenceClaim` | digest and exact board/sensor revision |
| `OperatingContext` **proposal** | supply path (`USB_ONLY`), temperature, firmware mode, effective VDD, configured GPIO input/pull states, drive path, active power state | unavailable inputs named precisely; user-level defaults not silently trusted |
| `AssumptionSet` **proposal** | `parameter`, `bounds`, `unit`, `assumption_owner`, `purpose`, `not_manufacturer_guarantee` | preserve independently from maker facts |
| `PassiveNetwork` **proposal** | optional exact resistors `Rtop/Rbottom` MPN+value+tolerance, physical terminal IDs + resistor connections | **not** introduced into canonical schema without CORE-001A approval |

### 10.1 პირველი შეუსაბამობა CORE-001A-ის current scope-თან

A კონტრაქტის `DeviceDefinition.kind` მხოლოდ `dev_board,sensor`-ს ითვალისწინებს (წინა დოკუმენტის §5.1); მას არ აქვს passive component `resistor`. ორ-რეზისტორიანი სქემის შეფასება ამიტომ **სრულად executable physical topology-ში არსებული ფაქტი ვერ იქნება მანამ**, სანამ არქიტექტურის მფლობელი არ აირჩევს ერთ-ერთს:

- **ალტერნატივა A — ადრეული დახურული demonstration motif:** CORE-001C მოიხმარს აშკარად ავტორიზებულ `PassiveNetwork` sidecar-ს, რომელიც exact terminal/net anchors-ს უკავშირდება; მოწმდება, რომ sidecar-ის ნეტები არ ეწინააღმდეგება CORE-001A-ს. **შეზღუდვა:** ეს *არ არის სრული რეზისტორიანი canonical circuit*; UI უნდა ასახელებდეს bounded model demonstration-ს.
- **ალტერნატივა B — მომავალი საერთო მოწყობილობის მოდელი:** CORE-001A-ის ავტორმა დაამატოს პასიური two-terminal device-ის representation და მისი `Conductor`/net semantics; R-top და R-bottom **არ** უნდა გახდეს same-net ideal tie. **სარგებელი:** ნამდვილი მრავალკომპონენტიანი სქემის მხარდაჭერა. **ფასი:** დამოუკიდებელი schema/evidence/identity migration and test coverage.

**[R]** რომელიმე ალტერნატივის ცალმხრივად დანერგვა ამ კვლევით **არ არის დამტკიცებული**. ეს არის ღია არქიტექტურული წინაპირობა, არა მცირე implementation detail.

### 10.2 შემოთავაზებული Findings semantics

| Field | მოთხოვნა |
|---|---|
| `evaluation_id`, `rule_id`, `rule_version`, `model_id`, `model_version` | replay და audit |
| `status` | **exactly** `PASS`, `FAIL`, `INDETERMINATE`, `NOT_EVALUATED` |
| `qualifier` | `ASSUMPTION_CONDITIONAL`, `MANUFACTURER_BOUNDED`, `MODEL_ONLY`, `MEASURED`, optional |
| `severity` | `error`, `warning`, `info`; სტატუსისგან დამოუკიდებელი |
| `reason_code` | `DC_INPUT_LIMIT`, `GUARANTEED_HIGH_NOT_ESTABLISHED`, `MISSING_VOH_MIN`, `GPIO_ABS_MAX_MISSING`, `POWER_OFF_UNMODELED`, `LOAD_MODEL_MISSING`, `MODEL_SCOPE_UNSUPPORTED`, ... |
| `affected` | `instance_id`, `terminal_id`, `net_id`, `connection_id` optional — CORE-001A IDs |
| `quantities` | SI values + display units + exact bounds + outward-rounding metadata |
| `requirement` | limit ID, limit kind, inequality, applicable conditions |
| `evidence` | doc id, source claim id, revision, locator, hash/URL |
| `assumptions` / `missing_inputs` | explain what makes result conditional or indeterminate |
| `model_scope` / `excluded_phenomena` | DC linear, ideal source, no transients, unknown clamp, etc. |
| `reproducibility` | snapshot hash, catalog digest, operating-context digest, algorithm revision, math backend/precision, deterministic output version |

**[R]** სისტემა ერთდროულად შეიძლება დაუბრუნდეს: `DIVIDER_MATH=PASS (MODEL_ONLY)`, `HIGH_RECOGNITION=INDETERMINATE (MISSING_VOH_MIN)`, `PIN_STRESS=INDETERMINATE (GPIO_ABS_MAX_MISSING)`, `TRANSIENT=NOT_EVALUATED`. საერთო `"no_errors":true` ვერ იქნება საინჟინრო დასკვნა.

## 11. Development-efficiency and maintenance comparison

| ვარიანტი | დაწყების engineering effort | მომავალი verification debt | recurring cost | შედეგი |
|---|---|---|---|---|
| **Explicit rules + 2R exact math** | დაბალი: რამდენიმე კარგად განსაზღვრული ფორმულა, unit/claim gates | დაბალი/საშუალო: datasheet updates და proof tests | მინიმალური, უფასო local CPU | **[R] შეირჩეს candidate** |
| Typed Pint + SymPy runtime every drag | საშუალო: units/expressions/config; deployment | მაღალი API/dependency/latency complexity first motif-ისთვის | free licenses, მეტი memory/CI | **[R] unnecessary initially** |
| NumPy/SciPy general MNA upfront | საშუალო/მაღალი: stamping, source constraints, singularities, solver validation | მუდმივი სიზუსტისა და topology coverage-ის ვალი | native wheels, OS support | **[R] defer** |
| KiCad schematic/netlist/ERC as canonical truth | მაღალი: EDA converter, variant identity, migration | მაღალი compatibility/legal integration | CLI install/packaging | **[R] comparator, not core** |
| ngspice for every action | მაღალი: models, batch/worker, security, adapter | მაღალი model-fidelity + licensing + performance | CPU, sandbox, ops | **[R] reject without eligibility gate** |
| Xyce / OpenModelica / custom SPICE | ძალიან მაღალი, არაამოცანებრივი | უკონტროლო პირველი scope-ისთვის | build/runtime | **[R] not now** |

**[U]** ცხრილის სირთულის შეფასებები **ხარისხობრივი პროგნოზებია**, არა გაზომილი engineering-hours, latency, RAM, dollar benchmark. ნამდვილი გეგმური ვადა და ხარჯი შეისწავლება დამოუკიდებელი trial-ით.

**შენარჩუნებადობის განსაკუთრებული რისკი:** ყველაზე ხარჯიანი არაა `Vout` ფორმულა; ყველაზე ხარჯიანია exact variant mapping, conflicting manufacturer claims, effective supply-mode, user-assumption governance, evidence-version migration და UI-ში შეცდომის ნამდვილი მიზეზის ჩვენება.

## 12. Open-source and component-model licensing audit

**[R] ლიცენზირების სიფრთხილე:** ქვემოთ აღწერილია upstream terms და პრაქტიკული სამოქმედო ზღვარი; **არ არის იურიდიული დასკვნა** კონკრეტულ distributable build-ზე. მესამე მხარის component model, documentation, data catalog, compiled plugins და transitively bundled binaries საჭიროებს ცალკე inventory-ს.

| არტეფაქტი (განხილული ვერსია) | საჯარო ლიცენზია / წყარო | კომერცია, redistribution, notices, SaaS | დასკვნა |
|---|---|---|---|
| Python 3.12 stdlib | PSF License v2 [S12b] | commercial use და redistribution დაშვებულია შესაბამისი notices-ით; არ არის subscription | **[F] usable** |
| NumPy 2.5.x | BSD-3-Clause [S13b] | commercial / SaaS yes; binary distribution notices + bundled license inventory | **[F] usable if needed** |
| SciPy 1.18.x | BSD-3-Clause + `LICENSES_bundled` [S14b] | usable; wheel/BLAS/backend/third-party notices უნდა შევინარჩუნოთ | **[F] usable if needed** |
| SymPy 1.14.0 | new BSD / repo license [S15b] | commercial generally permitted with notice; per-file exceptions check packaging | **[F] usable as test oracle** |
| Pint 0.26.2 | BSD-3-Clause; PyPI release [S16b] | commercial permitted; package and dependency notices | **[F] optional** |
| mpmath 1.4.1 | permissive BSD-style (package license check required at exact artifact) [S17] | legal availability ≠ interval mathematical fitness | **[U] not safety-approved** |
| ngspice 47 | base modified BSD with **source-tree exceptions** [S21b, S21c] | commercial possible; **binary composition-specific** file-license audit and 3rd-party model licensing; shared library vs process changes risk | **[R] optional, conditional license review** |
| KiCad 10.x application | primarily GPL-3.0-or-later [S23b] | commercial is not banned, but copied/combined/distributed derivatives may trigger copyleft/notice/source obligations; CLI separation needs factual/legal review | **[R] no core copy/link** |
| Xyce 7.10 | GPL v3 [S24] | commercial possible subject to GPLv3 conditions when distributing; build dependencies/solver licensing | **[R] defer** |
| Adafruit #3942 product page | public seller description, **not a model/data redistribution license** [S03] | quote/extract minimal facts with provenance; don't mirror product database/photos for application without rights | **[R] derived facts only; no blind copying** |
| Espressif WROOM-32E datasheet v2.1 | public readable technical reference [S01] | public PDF **not automatic permission** to redistribute entire copyrighted tables/images; cite documents and maintain separately verified claims | **[R] provenance/rights audit** |
| YAGEO exact MPN reseller entries | seller catalog info [S06–S07] | retail metadata ≠ manufacturer PCB or commercial database copying license | **[U] maker original/rights to recheck** |
| User-uploaded SPICE models | each model's own terms; unknown model may include executable constructs | **LICENSE_UNVERIFIED / LICENSE_BLOCKED** until explicit scope; sandbox essential | **[R] do not auto-run** |

**SaaS-specific distinction [R]:** open-source permissions generally do not vanish on SaaS; however, no-public-distribution does not excuse third-party model restrictions, service access rules, trade secrets, dataset rights, binaries bundled to client or license notices. Exact AGPL/GPL/other obligations must be examined per included artifact, not generalized as “GPL forbids commercial software” (false). No mandatory paid API/cloud simulator/vendor subscription is required in the recommended starting subsystem.

**Security gate for optional simulation:** accept only explicit allowlisted netlists/models, processes isolated by user with CPU/RAM/wall-clock quotas, no network, read-only file scope, restricted paths, no native user model loading, recorded inputs and version hashes, deterministic allowed analyses. Embedded ngspice in main web process is more dangerous than isolated process execution for untrusted workloads.

## 13. Simulation eligibility and escalation gates

| საფეხური | სრული input / model წინაპირობა | რა გარანტიას იძლევა | failure handling | ოპერაციული/იურიდიული ფასი |
|---|---|---|---|---|
| **L1 manufacturer constraints** | exact part/revision, applicable guarantee, supply/mode | documented inequality within specific conditions | missing → `INDETERMINATE` | დაბალი; claim governance |
| **L2 closed-form** | defined passive topology, source interval, positive R bounds, explicit load model | exact/bounded *mathematical* model | invalid model → `NOT_EVALUATED` | მინიმალური; stdlib |
| **L3 established linear algebra** | general linear graph, reference, source equations, valid matrix, scale | solution of admitted `Av=b` model, residual/condition | singular/ill-conditioned → `INDETERMINATE` | NumPy/SciPy install and regression |
| **L4 ngspice DC/transient** | exact model with license and validated pin mapping, stimuli, initial conditions, engine version | numerical solution of that model; **not** automatic physical truth | `MISSING_MODEL`, `LICENSE_BLOCKED`, `NON_CONVERGED`, `TIMEOUT` | native runtime, security, audit, model maintenance |
| **L5 physical measurement** | concrete parts/revisions, power conditions, instrument calibration, uncertainty budget, repetitions | empirical fit **within measured envelope** | out-of-range/uncertain → conditional/no blanket claim | hardware, operator time, calibration |

**[R] შეცვლის კრიტერიუმი:** გადადით შემდეგ საფეხურზე მხოლოდ იმ შემთხვევაში, როცა კონკრეტული acceptance case წინა საფეხურით ვერ წყდება, საჭირო მონაცემები უკვე არსებობს, და მიღებული სარგებლობა ფარავს ინტეგრაციისა და რისკის ღირებულებას. Solver-ის უბრალოდ თავისუფალი ხელმისაწვდომობა არ არის ტექნიკური საჭიროება.

**კონკრეტული counterexample [M/U]:** ngspice-ს მიეწოდება იდეალური 5.0V pulse source და 6.8k/10k resistor. `.tran` კონვერგირებს და `GPIO` შუა კვანძზე იძლევა იდეალურ 2.97619V HIGH-ს. რეალურ #3942-ში კი `VOH` შეიძლება დაიწიოს დატვირთვის დროს, edge შეიძლება შეაფერხოს უცნობმა `Rout/Cin`, ხოლო power-off GPIO protection network შეიძლება inject current-ს გაატარებდეს. შემავალი *მოდელი* ამ მოვლენებს არ აღწერს. **სიმულაცია რიცხვობრივად მართალია საკუთარი განტოლებებისთვის, მაგრამ სენსორის ფიზიკურ უსაფრთხოებას/ლოგიკურ გარანტიას ვერ ადგენს.** იგივე ეხება მასშტაბურ Xyce solver-საც.

## 14. Independent test and falsification matrix

| ID | საცდელი პირობა / დამოუკიდებელი oracle | მოსალოდნელი შედეგი | რას ამოწმებს |
|---|---|---|---|
| T01 | 10k/10k, `Vin=5`, fraction hand equation | `Vout=5/2=2.5V` | baseline algebra |
| T02 | 6.8k/10k, `Vin=5` → `5×100/168` | `2.976190476…V` | ratio, unit conversion |
| T03 | reversal `10k top /6.8k bottom` | `2.023809524…V`; no guaranteed HIGH for selected assumption | orientation matters |
| T04 | loaded `R_L=100k`, `6.8k/10k`, `Vin=5` | `2.860411899…V` by Thevenin *and separately* KCL | two independent derivations |
| T05 | no-load HIGH extrema, `4.5–5.25V`, ±1% `6.8k/10k` | `[2.656846374…,3.150249524…]V` | monotone bounds, exact arithmetic |
| T06 | 10k/10k, `5V`, `VDD=3.4V` | `margin=-0.05V`, guarantee **not established** | avoid false-safe |
| T07 | 6.8k/10k, `VDDmax=3.4`, model HIGH minima | `margin≈+0.106846V` **MODEL_ONLY**, physical `INDETERMINATE` with missing VOH guarantee | assumptions vs real guarantee |
| T08 | LOW `Echo≤0.30`, R extrema | `VLOW≤0.180014259V`; compare VIL at stated supply | LOW check separate from HIGH |
| T09 | `VOH_min` omitted; all nominal values given | no physical `PASS`; `MISSING_VOH_MIN` | unknown not treated typical |
| T10 | maker `Vin(abs max)` missing, `VDD33(abs max)=3.6V` present | stress `INDETERMINATE`, no misapplication of supply rating | limit-kind fidelity |
| T11 | `0.050 V` vs `50 mV` | identical; `50 mA` on voltage field rejected | dimensions |
| T12 | out-of-range: `Rbottom=0`, negative tolerance, `NaN` | invalid model/input, not arbitrary numeric result | validation |
| T13 | shared USB supply correlated VDD and sensor VCC | feasibility envelope instead of unjustified independence | correlation/data governance |
| T14 | power-off receiver + HIGH Echo, no injection/clamp data | `NOT_EVALUATED`/`INDETERMINATE`; no no-damage claim | sequence coverage |
| T15 | unknown HC-SR04 clone or DevKit revision | `UNSUPPORTED_DEVICE` / `INDETERMINATE` | exact identity |
| T16 | equality `Vout_min=VIH_required` | zero exact margin; boundary warning; do not round to positive | exact comparison |
| T17 | selected model replay/serialization reorder, graphical move | same exact electrical result / different view only | reproducibility and UI independence |
| T18 | two independent derivations (`R_eq` and KCL), optional ngspice ideal DC | match **same ideal mathematical model** within stated numeric tolerance | independent math, **not empirical** |
| T19 | documented `Rtop` dissipated bound vs rating; unknown source-driver current | resistor-power math model recorded; sensor-current admissibility `INDETERMINATE` | multi-check isolation |
| T20 | UI drag wire, topology returns physically different net | recompute only affected check with new `snapshot_sha256` | no stale verdict |

**[R] acceptance metrics:** count separately (a) incorrect `PASS` under withheld critical data — **must be 0** in curated golden fixtures; (b) wrong inequality boundary; (c) wrong affected terminal/net; (d) missing assumptions; (e) replay disagreement; (f) license/model eligibility failure. ეს არის **მიზნობრივი კრიტერიუმები**, არა შესრულებული ტესტების ანგარიში.

**შეზღუდული აპარატურული ვალიდაციის პროტოკოლი [R]:** exact board/module/PCB revision-ის ჩანაწერი, `USB_ONLY`, VDD/5V rail-ის კალიბრირებული დაკვირვება ±uncertainty, sensor `Echo` HIGH/LOW ტალღების ოსცილოსკოპული შეფასება resistor network-თან და მის გარეშე, rise/fall/overshoot, output loading, cold/normal states, შესაბამისი უსაფრთხოების პრაქტიკა. გაზომვები არ იძლევა ყველა გაყიდული clone-ის გარანტიას; მიღებული მოდელი scope/revision-ით უნდა შემოიფარგლოს.

**ფალსიფიკაცია:** რეკომენდებული მიდგომა ჩაითვლება არასაკმარისად, თუ ერთსა და იმავე model inputs-ზე მეორე დამოუკიდებელი algebra/linear solver შედეგი არ ემთხვევა; დადასტურებული maker extreme არ ხვდება მიღებულ bounds-ში; script-ი აძლევს `PASS`-ს საჭირო source-model-ის გარეშე; სადენის წაშლის შემდეგ ძველი hash-ის verdict ბრუნდება; ან მოთხოვნილი ახალი use-case ვერ აიხსნება არსებული primitives-ით და ამ პრობლემისათვის solver აშკარად აუცილებელია.

## 15. Unsupported behavior and technical blockers

| ბლოკერი | რატომ ვერ მტკიცდება პირველ მოდელში | რა ხსნის ბლოკერს |
|---|---|---|
| `Echo VOH_min / VOL_max` ზუსტი variant | seller-ის `5V logic` არ არის maker-grade guarantee | maker datasheet/batch validation, condition-specific output measurement |
| `Echo Rout / Iout` | არ არსებობს source-load transfer curve | valid I–V evidence ან bench characterization |
| GPIO exact abs-max/input injection | supply `VDD33` absolute rating არაა GPIO pin rating | chip/pin-specific vendor statement + domain mapping |
| transient overshoot / capacitance | DC equations არ აღწერს edges, EMI, wiring/parasitics | validated dynamic model / scope-limited oscilloscope measurements |
| GPIO power-off | clamp current/back-power unknown | manufacturer data + sequencing model/test |
| resistor physical graph vs A's 2-kind schema | CORE-001A passive component-kind ჯერ არ არის approved | explicitly approved sidecar vs model extension |
| sensor variant/manufacturer/board revision | retailer SKU/printed label არ უდრის maker revision-ს | procurement and reference profile audit |
| output HIGH guarantees 3.2–3.4V / ambient variations | DC Table 15 headed 3.3V/25°C; applicability extension unverified | vendor applicability clarification or measured envelope |
| firmware, ultrasonic timing, distance, acoustics | core electrical DC is not firmware/physical sensing simulator | scoped independent firmware/physics model + test |
| I²C, regulator inrush, multi-domain loading | new source/load/temporal models and datasets needed | new evidence-gated acceptance package |

## 16. Rejected alternatives

- **ყველა ძაბვის შემოწმება მხოლოდ `VIH/VIL`-ით — უარყოფილი.** signal recognition ≠ electrical stress; აბს-მაქსიმუმის მონაცემი არ უნდა შეივსოს `VDD33` კვების ცხრილით.
- **„Adafruit ურჩევს 2.5V-ს, მაშასადამე ESP32-ის ყველა რეჟიმში უსაფრთხოა“ — უარყოფილი.** კონკრეტული 3.4V მაგალითი 50mV-ით ჩამორჩება წარმოდგენილ HIGH guarantee-ს.
- **`6.8k/10k` უნივერსალური აღიარება — უარყოფილი.** missing `VOH_min`, source loading, transients, exact rating, power-off.
- **მთელი არითმეტიკა float-ით და მხოლოდ სამნიშნა rounding-ით — უარყოფილი.** boundary `>=` მარტივად გადაიქცევა მცდარ `PASS`-ად; მცირე რაციონალური მოდელები ზუსტად გამოითვლება.
- **საკუთარი SPICE/MNA nonlinear engine — უარყოფილი.** maturity, validation, maintenance cost და პირველ scope-ში არარსებული საჭიროება.
- **ngspice ყველასათვის default — უარყოფილი.** valid model-ის არქონამ შეიძლება კონვერგირებული, მაგრამ ფიზიკურად მცდარი პასუხი გამოიწვიოს.
- **KiCad/ERC canonical source-of-truth — უარყოფილი.** ERC არ ფლობს exact output guarantees ან physical safety-ს; GPL integration boundaries.
- **Xyce/Modelica/SMT ყველა უბრალო divider-ზე — უარყოფილი.** unnecessary native execution/solver burden, დამატებითი იურიდიული და სიზუსტის ზედაპირი.
- **შემთხვევითი tolerance distributions / Monte Carlo — უარყოფილი.** დაუდასტურებელი probability distributions წარმოქმნის ცრუ სიზუსტეს.
- **უნივერსალური ESP32 clone catalog — უარყოფილი.** hardware and revision mismatch; გაურკვევლობა არ უნდა გარდაიქმნას საჩვენებელ მწვანე შედეგად.

## 17. Proposed CORE-001C implementation decision package — დასამტკიცებელი არქიტექტურული პაკეტი

> ეს **არ არის დავალებების განაწილება, კოდი ან დამტკიცების აქტი**. ეს არის მტკიცებულებებით შეზღუდული არქიტექტურული წინადადება მფლობელის გადასაწყვეტად.

| საკითხი | წინადადება | კონტექსტი/უარყოფის საფუძველი |
|---|---|---|
| **Primary responsibility** | measured/claimed logic voltage, DC envelope, stress and passive arithmetic checks separate | ერთ-ერთი pass არ გულისხმობს სხვების pass-ს |
| **Dependency** | Python stdlib rational/decimal for 2R; **no mandatory paid/native engine** | სანამ ორი რეზისტორის ფარგლებია |
| **Data provenance** | exact board/part/version claims and scope, assumptions separate from manufacturer | source may be seller, maker, test, user assumption — ნუ შეაზავებთ |
| **Canonical integration** | immutable read-only CORE-001A input; no geometry/truth coupling | board/sensor identity must match digests |
| **Physical network gap** | passive-network sidecar OR approved passive canonical modeling | **open architecture-owner decision** |
| **Evaluation** | four statuses per check + qualifier/severity, independent logic/stress, exact missing fields | no green “all safe” |
| **Analytical model** | 2R no-load, optional resistive-load/fixed-leakage explicitly typed | source remains ideal only in scoped math mode |
| **Simulation** | ngspice 47 only eligibility+license+model fidelity gate | L4 not first-release requirement |
| **Acceptance scenario** | exact DevKitC-32E/WROOM-32E + Adafruit #3942, direct mismatch and divider arithmetic | do not generalize to all HC-SR04 |
| **Independent verification** | T01–T20 / source-specific logic check / corpus with incorrect-PASS=0 | targets, not executed test data |
| **Production wording** | `model result`, `manufacturer-bounded`, `conditional`, `insufficient evidence`; never `hardware verified` absent measurements | educational clarity and duty of care |

### 17.1 დასამტკიცებელი საკითხები (წესრიგით)

1. **Passive graph ownership:** სად არის 2× resistor-ის physical terminals/net edges — A-sidecar თუ A extension?
2. **Pin-stress fact availability:** არის თუ არა official GPIO abs-max/input-current/clamp envelope-ის შესაბამისი დასაბუთება ამ კონკრეტული module+pin-ისთვის? თუ არა, voltage survival check რჩება `INDETERMINATE`.
3. **Assumptions vs guaranteed maker facts:** supplier output waveform bounds დადასტურებულია თუ არ არის, რა conditional claims უნდა ჩანდეს UI-ში?
4. **Formal decision granularity:** ითვლება თუ არა `GUARANTEED_HIGH_NOT_ESTABLISHED` `FAIL`-ად *მხოლოდ guarantee check-ზე* და `INDETERMINATE`-ად actual logic behavior-ზე? რეკომენდაციაა დიახ, ერთმანეთისგან განსხვავებით.
5. **Gate for general linear solver:** რა დადასტურებული ახალი circuit family და measurement/KCL oracle ჩაითვლება საკმარის მიზეზად NumPy/SciPy-ის დამატებისთვის?
6. **Legal artifact inventory:** რა exact firmware/model/compiled binary/part catalog გავრცელდება მომხმარებლამდე, რა ლიცენზიით?

**საბოლოო რეკომენდებული პოზიცია:** **ვადასტურებთ მხოლოდ მათემატიკისა და წყაროთა კლასიფიკაციის კვლევით სანდოობას**; appliance safety, manufacturer `Echo` guarantees, full electrical compatibility, commercial willingness-to-pay და implementation QA არ არის მიღწეული. ტესტირებულ პროდუქტად გამოცხადება ნაადრევია.

## 18. Source register — პირველადი წყაროები, ვერსიები, გადამოწმების თარიღი

ყველა ქვემოთ მოცემული web წყაროს სტატუსი ნიშნავს **საჯარო პირველადი დოკუმენტის/პროექტის ოფიციალური გვერდის გახსნას და რელევანტური ტექსტის გადამოწმებას 2026-11-20-ს**; ეს **არ ნიშნავს** Python wheels-ის დაყენებას, PDF-ის კომერციული რეპუბლიკაციის უფლებას, source-code audit-ის სრულ დასრულებას ან ლაბორატორიულ ტესტს. Manufacturer direct datasheet-ის უხილავი დამატებითი მონაცემები `UNVERIFIED` რჩება.

| ID | პირველადი წყარო, ზუსტი ცნობილი ვერსია/ლოკატორი | URL | გამოყენება / შენიშვნა |
|---|---|---|---|
| **S01** | Espressif ESP32-WROOM-32E/32UE Datasheet **v2.1**, §6.1–6.3, Tables 13–15, გვ.28–29 | https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html | official module VDD, `VIH/VIL`, DC conditions; **GPIO absolute input rating not established from this table** |
| **S02** | Espressif official technical documents index; **v2.1, 2026-08-05** | https://www.espressif.com/en/support/documents/technical-documents/esp32-wroom | version corroboration |
| **S03** | Adafruit **Product ID 3942**, `Description`, `Technical Details` | https://www.adafruit.com/product/3942 | 5V logic Echo; 2×10k; seller evidence |
| **S04** | Adafruit Learning System, Ultrasonic Sonar Distance Sensors / Pinouts | https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/pinouts | common documentation with variant caveat |
| **S05** | Espressif **ESP32-DevKitC V4** user guide, `Power Supply Options`, `Header Block` | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html | board supply choices, GPIO34/18/19, flash pins |
| **S06** | Distributor DigiKey, YAGEO `MFR-25FBF52-6K8`, consulted 2026-11-20 | https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-6K8/9138205 | secondary supplier part/tolerance evidence; original maker PDF not independently opened |
| **S07** | Distributor DigiKey, YAGEO `MFR-25FBF52-10K`, consulted 2026-11-20 | https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-10K/13219 | secondary supplier part/tolerance evidence |
| **S12** | Python 3.12 `fractions`, `decimal` documentation (PSF) | https://docs.python.org/3.12/library/fractions.html ; https://docs.python.org/3.12/library/decimal.html | stdlib rational/decimal reference |
| **S12b** | Python 3.12 History and License | https://docs.python.org/3.12/license.html | PSF License 2 |
| **S13** | NumPy **2.5** `numpy.linalg.solve/cond`, version family (2.5.5 published Nov 2026) | https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html ; https://numpy.org/doc/stable/reference/generated/numpy.linalg.cond.html | API + numerical solve |
| **S13b** | NumPy project BSD-3 license / release info | https://github.com/numpy/numpy/blob/main/doc/source/license.rst ; https://numpy.org/news/ | license; version |
| **S14** | SciPy **1.18.x**, `scipy.linalg.solve`, `scipy.sparse.linalg.spsolve` | https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve.html ; https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.spsolve.html | solver API |
| **S14b** | SciPy GitHub source/license/`LICENSES_bundled`; release 1.18.1 2026-08-21 | https://github.com/scipy/scipy ; https://github.com/scipy/scipy/blob/main/LICENSES_bundled.txt ; https://scipy.org/news/ | distribution/notice obligations |
| **S15** | SymPy **1.14.0**, matrix `LUsolve`, `Rational` | https://docs.sympy.org/latest/modules/matrices/matrices.html | symbolic oracle |
| **S15b** | SymPy repository LICENSE | https://github.com/sympy/sympy/blob/master/LICENSE | permissive BSD-style repo license |
| **S16** | Pint tutorial / `UnitRegistry`, `Quantity.to()` | https://pint.readthedocs.io/en/latest/getting/tutorial.html | units conversion |
| **S16b** | Pint **0.26.2** PyPI, **BSD-3-Clause**, 2026-10-19 | https://pypi.org/project/Pint/0.26.2/ | reviewed package version/license |
| **S17** | mpmath contexts, `iv` warning (**experimental**); 1.4.1 2026 | https://mpmath.org/doc/current/contexts.html ; https://pypi.org/project/mpmath/1.4.1/ | interval limits, not selected runtime |
| **S18** | PyInterval project PyPI | https://pypi.org/project/pyinterval/ | old release; exact modern reliability/compatibility not proven |
| **S19** | BIPM/JCGM **100:2008**, **101:2008** | https://www.bipm.org/en/committees/jc/jcgm/publications | measurement uncertainty & Monte Carlo |
| **S20** | C.-W. Ho, A. Ruehli, P. A. Brennan, *The Modified Nodal Approach to Network Analysis*, **IEEE TCAS 22(6), 504–509, 1975** | https://mst.elsevierpure.com/en/publications/the-modified-nodal-approach-to-network-analysis/ | established MNA foundations |
| **S21** | ngspice release **47**, **2026-08-11**, official NEWS / downloads | https://ngspice.sourceforge.io/news.html ; https://ngspice.sourceforge.io/download.html | available mature simulator |
| **S21b** | ngspice Developers: predominantly modified BSD with exceptions | https://ngspice.sourceforge.io/devel.html | license baseline |
| **S21c** | ngspice source COPYING; artifact-level exceptions | https://github.com/ngspice/ngspice/blob/master/COPYING | review license inventory, not blanket BSD assumption |
| **S22** | ngspice shared library documentation | https://ngspice.sourceforge.io/shared.html | optional embedded interface + risk |
| **S23** | KiCad 10 CLI docs | https://docs.kicad.org/10.0/nl/cli/cli.html | ERC/netlist comparator; not safety engine |
| **S23b** | KiCad licenses (majority **GPLv3+**) | https://www.kicad.org/about/licenses/ | derivative/distribution considerations |
| **S24** | Sandia Xyce **7.10**, GPLv3 official downloads | https://xyce.sandia.gov/downloads/source-code/ ; https://xyce.sandia.gov/downloads/ | deferred solver license |

### Source integrity / negative findings

- **[U]** არ დადასტურდა #3942-ის კონკრეტული მწარმოებლის `Echo VOH(min)`, `VOL(max)`, output impedance, output drive current guarantee, transient waveform specification და ზუსტი PCB revision.
- **[U]** არ დადასტურდა სპეციფიკური ESP32 GPIO-ის სრულყოფილი input absolute maximum/current injection envelope იმავე მოწყობილობის და supply/power-off პირობებში. Module supply `VDD33` stress rating **არ გამოიყენება** GPIO stress truth-ად.
- **[U]** არ დადასტურდა `Echo HIGH=4.50–5.25V`, `Echo LOW=0–0.30V`, `VDD=3.2–3.4V` როგორც maker-guaranteed ranges. ისინი **explicit teaching/test assumptions** არიან.
- **[U]** YAGEO-ის exact original PDF spec sheets ვერ გაიხსნა ამ კვლევის გარემოში; distributor-listed ratings შეიძლება გამოყენებულ იქნეს მხოლოდ secondary-evidence label-ით maker-level `PASS`-ის დამტკიცების გარეშე.
- **[U]** არცერთი third-party binary/model-ის commercial redistribution-ის საბოლოო, artifact-by-artifact audit და benchmark არ ჩატარებულა.

**კვლევის საბოლოო დასკვნა:** **CORE-001C უნდა იყოს მტკიცებულებით შემოფარგლული ელექტრული შემმოწმებელი და არა ეკრანზე სიმულაციის ილუზიის მწარმოებელი.** ყველაზე ძლიერი პირველი demonstrable capability იქნება **დამაჯერებელი `INDETERMINATE`-იც**, როცა მას ზუსტად შეუძლია თქვას რომელი მწარმოებლის ფაქტი აკლია, რომელი უტოლობა ვერ მტკიცდება და რა შერჩეული დაშვებებით გამოიყურება შედეგი განსხვავებულად.
