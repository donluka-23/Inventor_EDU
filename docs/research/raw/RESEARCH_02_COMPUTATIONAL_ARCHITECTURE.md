# RESEARCH 02 — Computational Verification & Simulation Architecture

**ფაილი:** `RESEARCH_02_COMPUTATIONAL_ARCHITECTURE.md`  
**პროექტი:** INVENTOR EDU — Georgian-first visual educational electronics platform  
**კვლევის თარიღი:** 2026-11-20 (Asia/Tbilisi)  
**სტატუსი:** დამოუკიდებელი ტექნიკური კვლევა; **არ არის დამტკიცებული არქიტექტურა, იმპლემენტაცია ან პროდუქტის შესაძლებლობის გარანტია**.  
**მიზანი:** პირველადი გამოთვლითი ბირთვის მეცნიერულად დასაცავი საზღვრებისა და მომავალი გაფართოების პირობების განსაზღვრა, არსებული მეთოდებისა და ღია ინსტრუმენტების ხელახალი გამოგონების გარეშე.

> **საზღვარი:** ამ დოკუმენტში მოხსენიებული ნებისმიერი გარე engineering data model მხოლოდ **provisional input interface**-ია. არცერთ ფორმატს, მოდელის სტრუქტურას ან ძრავის არჩევანს არ ენიჭება საბოლოო ავტორიტეტი მანამ, სანამ არქიტექტურის პასუხისმგებელი პირი შესაბამის ინტერფეისს დაადასტურებს. აქ არ იწერება პროგრამული კოდი და არ ნაწილდება განხორციელების დავალებები.

## 1. Executive technical findings

**F1 — „კავშირი დახატულია“ ≠ „სქემა ელექტრულად გამართულია“ ≠ „ფიზიკური ქცევა სიმულირებულია“.** 2D wiring visualizer ინახავს ნახატსა და კავშირებს; verification ამოწმებს იმ მოთხოვნებს, რომელთათვისაც აქვს საკმარისი მონაცემები; simulation კი კონკრეტულ მოდელსა და პირობებში გამოთვლის მდგომარეობას. Simulation-ის წარმატებული დასრულება არ წარმოადგენს რეალური მოწყობილობის უსაფრთხოების ან ფუნქციონირების მტკიცებულებას. KiCad თავად აღნიშნავს, რომ ERC ვერ ავლენს ყველა შეცდომას და მისი სიზუსტე დამოკიდებულია symbol pin properties-ზე [R01, R02].

**F2 — ექვსივე სავალდებულო სცენარის საწყისი შეფასებისთვის უნივერსალური SPICE ან firmware emulator საჭირო არ არის.** pin capability/direction-ის, voltage-domain-ის, rail loading-ისა და I²C bus-ის ძირითადი ნაწილები წყდება მონაცემებზე დაფუძნებული constraint checks-ით; resistor divider — Kirchhoff/Ohm-ის კანონებით და interval bounds-ით; sensor timing — მდგომარეობათა ავტომატით (finite-state machine) და სპეციფიცირებული დროითი შეზღუდვებით [R11–R14]. ეს **კვლევიდან გამომდინარე კანდიდატი არჩევანია**, არა განხორციელებული შედეგი.

**F3 — KiCad ERC გამოსადეგია როგორც შედარების ეტალონი/სურვილისამებრ adapter, მაგრამ არა მთელი პლატფორმის semantic authority.** KiCad 10 CLI ოფიციალურად უზრუნველყოფს `sch erc`-ს (ტექსტური/JSON რეპორტი) და `sch export netlist`-ს, მათ შორის KiCad-ისა და SPICE-ის ფორმატებით. ERC-ის pin-conflicts matrix იცნობს სიმბოლოს pin ტიპებს, მაგრამ მიკროკონტროლერის runtime multiplexing, mode-dependent limits და ნამდვილ კვების ბიუჯეტს თავისით არ ადასტურებს [R01–R03]. KiCad netlist არ უნდა იქცეს საკუთრივ device knowledge-ის ერთადერთ წყაროდ.

**F4 — ngspice არის მიზნობრივი, არა ნაგულისხმევი next layer.** ngspice 47 (აგვისტო, 2026) მხარს უჭერს DC, transient და სხვა SPICE ანალიზებს, shared-library API-სა და XSPICE mixed-signal behavioral models-ს [R04–R07]. მისი გამოყენება გამართლებულია იმ შემთხვევაში, როცა კონკრეტული ამოცანის შედეგი არსებითად დამოკიდებულია არაწრფივ/დინამიკურ ელექტრულ მოვლენაზე, რომლის საიმედო გადაწყვეტა ანალიტიკური ინტერვალებით ვერ ხერხდება. არც SPICE netlist-ის არსებობა და არც numerical convergence არ ადასტურებს input მოდელის ვალიდურობას.

**F5 — Xyce, OpenModelica/FMI, Renode და ESP32 QEMU ამ ეტაპზე არ არიან აუცილებელი დამოკიდებულებები.** Xyce 7.10 უფრო მასშტაბური/პარალელური analog simulation-ისთვისაა; OpenModelica 1.27.1 და FMI 3.0.2 — მრავალდომენიანი/კომპოზიციური მოდელირებისთვის; Renode 1.17.0 და Espressif QEMU — შერჩეული SoC/firmware/peripheral execution-ისთვის [R08–R10, R16–R21]. მათემატიკური ამოცანისა და შემოწმებადი model coverage-ის გარეშე ინტეგრაცია დაუფარავ ხარჯს შექმნის.

**F6 — ყველაზე მნიშვნელოვანი საინჟინრო რისკი solver-ის არარსებობა კი არა, device-level truth-ის არარსებობაა.** ზუსტი chip/board revision-ის, pin mux-ის, abs-max/recommended range-ის, VIH/VIL, output strength-ის, rail limits-ის, resistor tolerance-ისა და sensor operating mode-ის გარეშე „PASS“ დაუშვებელია. ურთიერთგამომრიცხავი წყაროები, არარსებული მონაცემები და დაუმოწმებელი ასუმფციები უნდა გამოჩნდეს `UNKNOWN`/`UNSUPPORTED`-ად, არა გამოიცნოს.

**F7 — სწორი პირველი საზომი არის soundness/coverage და არა ზოგადი „AI სიზუსტე“.** ოქროს სცენარებზე შეფასდეს: კონკრეტულ ვერსიასა და მონაცემებზე გამეორებადობა; არასწორი PASS-ების რიცხვი; დასაბუთებული უარყოფები; `UNKNOWN`-ის სწორად დაყენება; გამოთვლისა და დამოუკიდებელი ეტალონის თანხვედრა. ამ კვლევაში **არცერთი performance benchmark არ ჩატარებულა**.

**შემოთავაზებული ორიენტირი:** `provisional topology → deterministic engineering checks → bounded analytical calculations → structured evidence/result → 2D mapping → Georgian explanation`; უფრო მძიმე engine მხოლოდ კონკრეტული proof-of-capability-ისა და უფლებრივი შემოწმების შემდეგ. ეს არ არის არქიტექტურის დამოუკიდებელი დამტკიცება.

## 2. Computational capability taxonomy

| საფეხური | რას აკეთებს | საჭირო მონაცემი | რას **არ** ამტკიცებს | შესაძლო საშუალება |
|---|---|---|---|---|
| **V0. Interactive wiring visualizer** | 2D ელემენტებსა და terminal-to-net კავშირებს აჩვენებს | device/terminal IDs; geometry; connectivity | სიმძლავრეს, ძაბვას, firmware ქცევას | UI + graph connectivity |
| **V1. Structural/ERC-like** | open/short, conflicting drivers, unpowered pin, mandatory ground/supply | declared pin roles და net topology | pin-ის რეალურ რეჟიმს ან ვოლტაჟს | წესები; optional KiCad ERC cross-check |
| **V2. Parametric compatibility** | GPIO mux, input/output threshold, absolute limits, rail capacity, address/protocol checks | exact part/variant, mode, limits, conditions | უცნობ runtime მდგომარეობას | typed constraints; interval arithmetic |
| **V3. Analytical electrical** | DC divider, loads, power, worst-case, RC rise, simple logic margins | წყაროს/მიმღების რაოდენობრივი მოდელი | არაწრფივ/გარდამავალ დეტალებს bounds-ის მიღმა | Ohm/KCL/KVL, closed form, პატარა linear system |
| **V4. Circuit numerical** | DC operating point, AC, transient კონკრეტულ მოდელზე | SPICE-compatible კომპონენტები, stimuli, ground/initial conditions | მოდელის ფიზიკურ სიზუსტეს | ngspice; საჭიროებისას Xyce |
| **V5. Firmware/peripheral virtual execution** | CPU, memory, დაფარული peripherals, register-driven behavior | ზუსტი target, firmware, peripheral fidelity manifest | ADC analogue front-end-ის/PCB-ის რეალურ ქცევას | Renode ან ESP32 QEMU შერჩეულად |
| **V6. Coupled multi-domain / empirical** | electrical–thermal–mechanical ან firmware–analog co-simulation | clock synchronization, interface variables, validated component models | ავტომატურად „digital twin“-ის სიზუსტეს | FMI/Modelica, HIL, measured calibration |

**სიზუსტის ენა:** V0–V6 არის **შესაძლებლობის კატეგორია**, არა ავტომატურად ხარისხის ან რწმუნებულობის მონოტონური სკალა. ცუდი V4 შედეგი შეიძლება ნაკლებად სანდო იყოს, ვიდრე დადასტურებული V3 interval bound.

დამოუკიდებლად უნდა იყოს გამოყოფილი ოთხი კითხვა:

1. **Mathematical correctness:** სწორად დაისვა/გადაიჭრა მათემატიკური ამოცანა? (მაგ., KCL და საზღვრების სწორად გამოყენება).
2. **Model validity:** მოცემული equations/rules აღწერს სწორედ ამ მწარმოებლის ამ ვარიანტს, ამ რეჟიმში? (model identity, version, regime, abstraction).
3. **Numerical convergence:** iterative solver-მა მიაღწია მითითებულ residual/tolerance-ს? (`converged` არ ნიშნავს `validated`).
4. **Physical predictive accuracy:** შედეგი დამოუკიდებელ გაზომვას ეთანხმება მითითებული uncertainty-ითა და operating envelope-ით? (ეს ცალკე ექსპერიმენტული მტკიცებულებაა) [R23, R24].

## 3. Comparison of mathematical and simulation engines

### 3.1 გადაწყვეტისთვის არსებითი შედარება

| მეთოდი/ინსტრუმენტი | დადასტურებული შესაძლებლობა და interface | სიძლიერე | ფაქტობრივი ზღვარი/რისკი | საწყისი პოზიცია |
|---|---|---|---|---|
| **Deterministic domain rules + interval arithmetic** | typed pin/net/mode data-ზე თავსებადობის პირობები და worst-case bounds; არ საჭიროებს გარე runtime-ს | explainable, სწრაფად audit-able; ზუსტი მარტივი ამოცანებისთვის | არასრული datasheet = არასრული დასკვნა; რთული დინამიკა მიუწვდომელია | **აუცილებელი მეთოდი** |
| **KCL/KVL, Ohm, MNA / small linear algebra** | nodal equations; voltage sources-ისთვის Modified Nodal Analysis; grounded linear DC nets | დეტერმინისტური მცირე ქსელები, SPICE-ის გარეშე | nonlinear semiconductors, startup, hysteresis, capacitive/inductive transient უნდა მოდელირდეს დამატებით; singular matrices | **შერჩევითი მათემატიკური საფუძველი**, არა დამოუკიდებელი SPICE clone |
| **KiCad ERC 10.0.8** | schematic pin-type matrix; CLI `sch erc` (მათ შორის JSON report), netlist export (`kicadsexpr`, `kicadxml`, `spice` და სხვ.) [R01–R03] | დამკვიდრებული EDA semantics-ის reference implementation | საჭიროებს KiCad schematic/symbol semantics-ში კონვერტაციას; rule coverage არ არის board-specific dynamics | **optional comparator/adapter** |
| **ngspice 47** | SPICE netlist, `.op`/DC, transient, AC, shared C API; XSPICE code-model/event functionality [R04–R07] | mature analog/mixed-signal solver; integrable library | model portability, convergence, untrusted model/script execution, CPU/runtime | **optional gated experiment** |
| **Xyce 7.10** | SPICE-compatible high-performance parallel electrical simulation; documented user guide; XDM translation [R08, R09] | დიდი/მძიმე circuits და კვლევითი numerical workloads | larger build/dependency and integration surface; SPICE dialect divergence; FAQ-ში co-simulation API-ს შეზღუდული პრაქტიკული გამოყენება [R09] | **არ არის პირველი ბირთვის ნაწილი** |
| **Z3 4.15.6** | SMT-LIB2, typed SAT/UNSAT/UNKNOWN, arithmetic/bitvectors, unsat constraints [R15] | intertwined pin assignment/board-config constraint search; impossible-state proofs within encoded axioms | wrong axioms → „correct“ but misleading proof; solver timeout; real-valued nonlinear approximations | **optional**, მხოლოდ რეალური constraint-combinatorics-ის შემთხვევაში |
| **OpenModelica 1.27.1 / Modelica** | equation-based multi-domain simulation; model compiler/runtime [R16] | electrical+thermal+mechanical coupling | component model acquisition, license modes, complex toolchain; mere simple circuits do not justify | **defer** |
| **FMI 3.0.2** | standardized FMU packaging, Model Exchange/Co-Simulation/Scheduled Execution; versioned interface [R17] | black-box model exchange where independently validated FMUs exist | FMU model/license quality; CS time-stepping/events; only interface specification, not universal solver | **integration contract candidate, not core dependency** |
| **Renode 1.17.0** | selected CPU/SoC/peripheral virtual platforms, monitoring/automation, external control API, HDL co-simulation [R18, R19] | firmware/peripheral regression and selected virtual development | missing models; fidelity is per board/peripheral, not automatic electrical truth | **target-specific future experiment** |
| **Espressif QEMU fork** | selected ESP SoCs, CPU, memory and some peripherals; Espressif docs acknowledge unsupported devices [R20, R21] | ESP-IDF/selected firmware boot/testing | not a complete ESP32 electronics/analog simulator; version- and chip-specific coverage | **target-specific future experiment** |
| **Verilator 5.x** | SystemVerilog simulator/lint and HDL model compilation [R22] | digital RTL, validated peripheral HDL co-simulation | does not supply ESP32 silicon/PCB models; analog effects out of scope | **no general dependence** |

**MNA-ის ადგილი.** სტანდარტული DC linear circuit-ისთვის წერია `G·v = i`; იდეალური voltage sources-ის ჩართვით MNA გადადის block matrix-ზე, სადაც უცნობებად node voltages და source currents ითვლება. ეს დასაბუთებული მეთოდია Ho–Ruehli–Brennan (1975)-იდან [R25]. INVENTOR EDU-სთვის MNA-ს ახალი ზოგადი engine-ის აგება გაუმართლებელია: მისგან შეიძლება ისარგებლოს მხოლოდ პატარა, მკაცრად შეზღუდულმა analytical subsystem-მა. არაწრფივი circuit analysis-ის პასუხისმგებლობა უკეთ დარჩეს SPICE solver-ს, თუ ფუნქციური მტკიცებულება ამის საჭიროებას აჩვენებს.

**Z3-ის ადგილი.** Constraint engine სასარგებლო ხდება მაგალითად კითხვაზე: „არსებობს თუ არა იმავე MCU-ზე pin mux, voltage domains და ერთდროული timers-ის ისეთი განაწილება, რომელიც ყველა მოთხოვნას აკმაყოფილებს?“ თუ ამოცანა მხოლოდ `GPIO34` output-ის აკრძალვას ამოწმებს, simple deterministic rule იაფია და გამჭვირვალე. `UNSAT` მტკიცებაა **დარეგისტრირებული შეზღუდვების მიმართ**, არა მთელი მოწყობილობის რეალურ სამყაროში შეუძლებლობის შესახებ.

**Xyce vs ngspice.** Xyce-ის parallel scale საწყის 2D breadboard სცენარებში გამოყენებად უპირატესობად **არ დადასტურდა**. არც ერთი კონკრეტული INVENTOR EDU workload/benchmark არ არსებობს, სადაც Xyce-ის დამატებითი სირთულე თავს ამართლებს; ეს უნდა დარჩეს უარყოფადი ჰიპოთეზა და არა გეგმაში „შემდგომი ფაზის“ ავტომატური ნაბიჯი.

## 4. Six mandatory engineering scenarios: least-complex defensible method

### S1. Incorrect GPIO direction / unsupported pin functionality

- **Input:** exact SoC/board/revision; physical header→chip pad mapping; mux alternatives; input-only/output-capable flags; boot/strapping restrictions; requested signal role; optional firmware configuration/state.
- **Method:** graph lookup + finite-domain constraint validation. `required_function ∈ available_pin_functions` და `configured_direction` compatibility. Pin multiplexing-ის შესაძლო ალტერნატივები განისაზღვროს კონკრეტული chip-ის API/datasheet-ში; output-only assumption არ გაკეთდეს „GPIO“ სახელიდან.
- **Example:** generic ESP32-family board-ზე შემავალი pin შესაძლოა input-only იყოს; „OUT“ label-ის მიერთება კი არა, **ზუსტი pin capability** განსაზღვრავს დარღვევას [R12]. თუ firmware config არ არის მოწოდებული, ჩაიწეროს `UNVERIFIED_MODE` და არა „output verified“.
- **Output:** `BLOCKED` მხოლოდ დადასტურებული ფიზიკური შეზღუდვისას; `CONDITIONAL` სხვა pin function/mode-ის არსებობისას; `UNKNOWN` firmware state-ის არქონისას. 2D-ში გაესვას ხაზი relevant header pin-სა და conflicting mode-ს.
- **რატომ არა SPICE:** პროგრამულად განაწილებული digital pin-ის ფუნქცია არ გადაწყდება ანალოგური circuit solver-ით.

### S2. 5 V digital output → 3.3 V-class input

- **Input:** source `VOH(min/max)`/`VOL(max)` and supply envelope, receiver `VIH(min)`, `VIL(max)`, recommended input range, **absolute maximum** for that exact pin, 5 V tolerance, protection/clamp current, power-off behavior, possible level shifter.
- **Method:** interval/inequality checks: HIGH recognition (`VOH_min ≥ VIH_min`), LOW recognition (`VOL_max ≤ VIL_max`), stress (`Vsignal_max ≤ Vin_absmax`, with specified conditions), injection/clamp current where manufacturer permits and model exists. Mixed voltage tolerance must be pin-specific.
- **Output:** if a specified non-5V-tolerant input exceeds its input limit → `LIMIT_VIOLATION`; if tolerance/abs-max data missing → `UNKNOWN`, **not** an automatic 5V unsafe verdict for every 3.3V-powered part. „Logic works“ და „survives electrically“ ერთმანეთისგან განცალკევდეს.
- **Remedies:** documented logic-level translator, valid divider for **appropriate unidirectional, bounded-rate** signal, 5V-tolerant receiver; resistor alone is not automatically a safe clamp-current solution. Power-sequencing/phantom-powering remains separate condition.
- **რატომ არა SPICE:** limit check უმეტესად არითმეტიკულია; SPICE საჭიროა მხოლოდ ისეთი transient/clamp analysis-ისთვის, რომლის მოდელი რეალურად არსებობს.

### S3. Resistor divider: loading and tolerance

- **Input:** source voltage range and source impedance, `R1`, `R2`, tolerances, temperature effects if relevant, receiver input resistance/leakage range and input capacitance, target thresholds.
- **Method:** loaded DC divider via KCL/Ohm:

  `R_eq = R2 || R_load = (R2·R_load)/(R2 + R_load)`  
  `V_out = V_in · R_eq/(R1 + R_eq)`.

  Treat an effectively infinite `R_load` as the unloaded special case, not the default if unknown. Use boundary evaluation/interval propagation for independent component tolerances and supply variation; report applicable assumptions and dependence.
- **Illustrative calculation (not a validated component recommendation):** `Vin=5.0 V`, `R1=10 kΩ`, `R2=20 kΩ` → `3.333 V` unloaded. With `Rload=100 kΩ`, output becomes `3.125 V`. `Vin=5.5 V` with unloaded nominal resistors → `3.667 V`; 5%-tolerance adverse combination can increase this further. Therefore nominal `3.33 V` is not proof that the input limit is respected.
- **Additional checks:** divider current and resistor dissipation, voltage under dynamic load, RC edge/rise/fall and ADC sampling behavior when applicable. For a high-speed bidirectional bus this simple divider model is inadequate.
- **რატომ არა SPICE:** passive steady-state linear topology has a closed-form solution. SPICE only if frequency response, nonlinear input clamp, or transient edge requirement makes the additional fidelity relevant.

### S4. Multiple loads on a power rail

- **Input:** rail provenance, regulator/source `Iout` continuous/peak/derating, regulator input voltage/efficiency, current envelopes per load and mode, inrush coincidence, wire/contact resistance, acceptable voltage drop, thermals and upstream budget.
- **Method:** worst-case power-tree budget with a **concurrency envelope**: `I_rail,upper = Σ I_load,upper` only if loads can be simultaneously active; otherwise explicit mutually exclusive modes. Verify `I_rail ≤ I_source,derated`, `P≈V·I`, `ΔV≈I·R_path` and device operating range. Record separately steady-state, startup/inrush, thermal duration and branch constraints.
- **Outputs:** overload when a defensible upper bound breaks a documented source limit; `UNKNOWN` if a source's current rating/thermal derating is unavailable. The absence of overload based on *typical* current does not justify PASS.
- **Escalation:** SPICE/transient only for power-up droop, regulator dynamic response or switching behavior, and only with a validated regulator/source model; bench validation for Wi-Fi burst current or thermal response if model coverage is insufficient.

### S5. I²C compatibility, pull-ups and voltage domains

- **Input:** bus topology and controllers/targets; open-drain capability; pin voltage domains and power-off tolerance; pull-up rail(s) and all effective parallel `R_p`; bus capacitance `C_b` (pins+cable+traces), chosen mode/frequency, `VOL/IOL`, `VIH/VIL`, address, clock stretching support.
- **Method:** protocol/graph constraints + RC rise-time bounds. NXP UM10204 Rev 7 and TI SLVA689A define:

  `R_p,min = (V_pullup − V_OL,max)/I_OL`  
  `R_p,max = t_r,max/(0.8473 · C_b)`.

  Example using TI's **specified assumptions** for Fast-mode: `Vpullup=3.3 V`, `C_b=200 pF`, `t_r,max=300 ns`, `VOL,max=0.4 V`, `IOL=3 mA` → `R_p ≈ 0.967–1.77 kΩ`. This is **not** a universal I²C resistor recommendation; real sink ratings, additional pull-ups, voltage domains and hardware must be checked [R13, R14].
- **Outputs:** static pin voltage violations independently from timing; `CAPACITANCE_UNKNOWN` if cable/pin capacitance not bounded; conditional timing status if bus frequency/mode is unspecified; address collision, if addresses are fixed and on the same bus segment.
- **Limits:** 1st-order RC and spec margins do not capture all parasitics, ringing, buffer delay or device-specific stretching; scope measurement may be required. SPICE is unnecessary for an initial R-range validity test.

### S6. Sensor timing / operating-state dependence — Bosch BME280 example

- **Input:** exact Bosch BME280 variant and datasheet revision, register write sequence, `ctrl_hum`, `ctrl_meas`, `status`, oversampling, sleep/forced/normal mode, I²C/SPI transaction order, requested measurement cadence.
- **Method:** **bounded finite-state machine + specified timing inequalities**, rather than a full silicon emulator. Bosch documents that humidity oversampling changes in `ctrl_hum` take effect after writing `ctrl_meas`; `status.measuring` identifies conversion progress; measurement duration depends on oversampling [R11, R26].
- **Possible checks:** reading before conversion completion; treating prior sample as new; requesting a cadence inconsistent with stated measurement time; invalid register sequencing; attempting to infer state from wiring alone.
- **Output:** `TIMING_VIOLATION` only when the user supplied/observed sufficient event ordering and timing; `UNOBSERVED_FIRMWARE_STATE` if firmware traces are absent; `MODELLED_REGISTER_BEHAVIOR` only for the explicitly modeled state machine. A successful I²C wiring/ERC check does not establish correct sample freshness.
- **რატომ არა general MCU emulation:** deterministic, documented register-level behavior answers the narrow educational question more cheaply and transparently. Emulation becomes useful only when actual firmware execution, interrupts or multiple peripheral interactions are in scope.

### 4.1 სცენარების საერთო კომპაქტური რუკა

| სცენარი | პირველი საკმარისი მეთოდი | დასაბუთებული დამოწმება | როდის შეიძლება უფრო მძიმე ძრავი |
|---|---|---|---|
| GPIO | pin-mux/direction finite constraints | chip docs + negative/positive pins | firmware-dependent state replay |
| 5V→3.3V | interval threshold/stress comparison | exact IO limits and 5V-tolerance notes | transient/clamp current with valid model |
| divider | KCL closed form + bounds | hand calculation + independent circuit solver | ADC sampling/high frequency/nonlinear load |
| power rail | maximum concurrent-load budget | manufacturer rail rating + bench | regulator startup, droop, switching |
| I²C | protocol rules + RC interval | NXP/TI equations + oscilloscope | bus parasitics/buffers complex enough |
| sensor timing | register FSM + timing inequalities | Bosch datasheet + trace/real hardware | real firmware/hardware event test |

## 5. Constraint-to-remedy matrix

| Limitation | Root cause | Strongest demonstrated remedy and when applicable | Evidence | Residual risk / do not claim |
|---|---|---|---|---|
| **No SPICE model** | manufacturer provides specs but no equivalent network | use verified limit/threshold rules; closed-form linear/passive network; ideal/simplified behavioral block **only inside explicit envelope** | Ohm/KCL, MNA [R25]; device datasheets [R11, R12] | transient/nonlinear/internals not predicted; display `NOT_SIMULATED` |
| **Incomplete/proprietary model** | missing internal params; terms prohibit reuse | reference manufacturer specs and user-authorized locally supplied model; replace with abstraction only after test against documented observable behavior; do not redistribute restricted model | TOREX restrictions [R27]; ngspice model API [R06] | legal/IP constraints and abstraction error remain; **no scraped-model redistribution** |
| **No full MCU model** | silicon complexity, missing peripherals, analog paths | pin-config static checks; sensor FSM; selective Renode/QEMU **only with coverage manifest + target firmware** | [R18–R21] | firmware timing/electrical reality not guaranteed; mark unsupported peripheral |
| **Unknown operating mode** | state depends on firmware, boot, power sequencing or user input | conditional branches with explicit assumptions; observe firmware traces/registers if available; seek exact mode input | Bosch status/mode [R11, R26] | state not observable from static wiring; do not silently choose typical mode |
| **ERC cannot predict behavior** | topology constraints do not encode physics | add bounded equations/intervals; optional SPICE for validated analog model; real measurement where needed | KiCad ERC boundary [R02, R03]; ngspice [R04] | solver output is conditional on model and stimuli |
| **Solver dialect/assumption mismatch** | model languages, conventions, units, initial conditions differ | versioned adapter + test corpus + normalized result schema; netlist translator (e.g., XDM) only for tested device subset; no blind semantic conversion | KiCad export [R01]; Xyce docs [R09] | unsupported directives, different convergence and default parameter semantics |
| **Simulation vs measurement disagreement** | parameter uncertainty, parasitics, wrong model, setup error, measurement uncertainty | reproducible experiments; instrument calibration and trace; parameter estimation **without overfitting**; independent hold-out comparisons; revise envelope | JCGM GUM [R23], ASME VVUQ principle [R24] | measured circuit ≠ every nominally same board; generalization requires uncertainty |
| **User expects full simulation** | visual output overstates modeling | explicit capability tier per net/device/metric, conditional status, ‘what was not simulated’, escalation path to measurement | KiCad ERC limits [R02], Espressif missing peripherals [R21] | UX cannot eliminate physical unpredictability; no global simulation-success badge |
| **Available behavioral abstraction unvalidated** | convenient surrogate lacks external calibration | bounded surrogate plus documented tests at min/typ/max and corners; use only interpolation within measured/characterized domain | [R23, R24] | extrapolation and discontinuities; fail closed outside domain |
| **Co-simulation seems attractive** | separate firmware and analog/time solvers | synchronized event/time-step contract, FMI/HDL bridge when *specific* pair of models is independently validated | FMI [R17]; Renode API [R19] | timestep causality, rollback, timing divergence, deadlock; substantial cost |

**Hierarchical modeling** ნიშნავს, რომ თითოეული subsystem განსაზღვრულ abstraction boundary-ს იღებს (მაგ., logic-level sensor protocol vs analogue sensing physics). **Selective co-simulation** დასაშვებია მხოლოდ მაშინ, როცა დასაშვები ცვლადები, event order, units და timebase ორივე მხარეს ფიქსირებულია. ეს მიდგომები არ ქმნის არმოცემულ ფიზიკურ ინფორმაციას.

## 6. Proposed computational pipeline and module boundaries

ეს არის **evaluation pipeline candidate**, არა უკვე მიღებული platform architecture.

```text
[2D scene/editor]
       | persistent element_id / terminal_id / connection_id
       v
[Provisional canonical model adapter] ---> [provenance & license metadata]
       | exact devices, stable nets, requested modes, units
       v
[Normalization + graph/topology checks]
       | validated/ambiguous net graph; no silent inference
       +------------------+-------------------+
       |                  |                   |
       v                  v                   v
[Deterministic      [Analytical         [Optional model
 compatibility]     DC/RC/power]        eligibility gate]
       |                  |                   |
       |                  |                   v
       |                  |             [SPICE / firmware /
       |                  |              external FMU adapter]
       |                  |                   |
       +------------------+-------------------+
                          v
            [Normalized findings + evidence]
                          |
                 [Result interpretation]
                          |
            +-------------+--------------+
            v                            v
     [2D anchor mapper]       [Georgian explanation]
        (not solver)        (does not invent findings)
```

**Boundary contracts:**

**6.1 Topology adapter.** Receives mutable scene state only through a frozen snapshot; produces device IDs, physical terminal IDs, nets, connection graph, board-to-chip mappings and unresolved ambiguities. UI coordinates never decide electrical connectivity by visual proximity alone. Each terminal may belong to exactly one electrical net in a snapshot; a net may contain multiple terminals. Power-rail labels do not magically imply valid power sources.

**6.2 Rule validator.** Takes snapshot + device facts + modes + rule version. Produces violations/proven-safe conditions/unknowns with traceable sources; never runs a numerical solver; does not convert warnings to PASS just because an ERC tool is silent.

**6.3 Model preparation.** Admits only circuits where required models, terminals, ground reference, stimuli, initial/operating conditions and analysis type are defined. Makes an **eligibility decision** (`ELIGIBLE`, `MISSING_MODEL`, `OUTSIDE_ENVELOPE`, `LICENSE_BLOCKED`, `UNSUPPORTED`). Different solver formats generated through adapters, not by modifying authoritative topology.

**6.4 Solver execution.** Sandboxed, reproducible invocation (process isolation, resource limits); records engine/adapter/model versions, input hash, convergence log, chosen tolerances and units. Numerical failure (`SINGULAR`, `NON_CONVERGED`, `TIMEOUT`) is neither safe nor unsafe circuit verdict. Optional shared-library embedding of ngspice must be independently reviewed for isolation/reentrancy and licensing; process isolation is safer for untrusted models.

**6.5 Interpretation.** Normalizes physical results and checks them against **rated limits**; identifies which hypothesis failed. Example: solver returned `Vout = 3.8 V`, but interpretation needs receiver `Vin,max` and operating conditions before it can label a violation. Distinguishes observed numerical value from predicted real-world value.

**6.6 Anchoring to 2D.** Converts `component_id`, `terminal_id`, `net_id`, `constraint_id` into persistent UI markers. Reporting spans across multiple wires/loads must point to the causally relevant net and devices, not just one convenient canvas coordinate. Geometry is presentation, not proof.

**6.7 Educational explanation.** Deterministic statement template for numeric/structural findings: **observed condition → physical law or manufacturer limit → violated inequality → minimal correction → assumptions/uncertainty**. Georgian terminology can be localized without altering numbers, units or constraints. An LLM, if ever used, may paraphrase **bounded evidence records only** and may not upgrade `UNKNOWN` to `PASS` or invent specifications.

**6.8 Versioning and reproducibility.** Frozen input snapshot; exact device data version; source document revision; model source/hash/license; rule-set version; engine binary version and parameters; locale-independent SI storage; output schema version; event timebase. Nondeterministic Monte Carlo analysis additionally needs seed, sampling distribution and dependence assumptions. Cache keys include model/engine version: old PASS cannot be reused for changed board revisions.

## 7. Integration contracts required from the canonical engineering model

**ყველა ქვემოთ ჩამოთვლილი კონტრაქტი დასადასტურებელია canonical-model owner-ის მიერ.** ეს არის მოთხოვნილი საინჟინრო *semantics*, არა data schema-ზე გადაწყვეტილება.

| Required concept / proposed fields | Reason / consumer | Failure if absent |
|---|---|---|
| `manufacturer`, `part_number`, `exact_variant`, `silicon_revision`, `board_revision`, `package` | datasheet/footprint/model matching | `IDENTITY_AMBIGUOUS` |
| physical `terminal_id`, board-header→SoC pad mapping, electrical net membership | topology/ERC/2D anchor | `TOPOLOGY_UNKNOWN` |
| pin functional modes, direction, mux/alternate functions, boot/strap constraints | S1, S6 | `MODE_UNSPECIFIED` |
| power domains/rails, source path, common ground, source operating range | S2, S4, S5 | `RAIL_REFERENCE_UNKNOWN` |
| pin-level input voltage recommended/abs-max, `VIH`, `VIL`, leakage, 5V tolerance | S2, S5 | `LIMIT_UNAVAILABLE` |
| pin drive type (`push-pull`, `open-drain`, `Hi-Z`), `VOL/VOH` vs `IOL/IOH` and supply | S1, S2, S5 | `DRIVER_MODEL_UNKNOWN` |
| load `I_typ`, `I_max`, startup/inrush, concurrency modes, regulator derating | S4 | `LOAD_ENVELOPE_UNKNOWN` |
| passive values, units, tolerance, temperature coefficients, input resistance/capacitance | S3, S5 | `PARAMETER_RANGE_UNKNOWN` |
| protocol interface, controller/target roles, fixed/programmed I²C addresses, speed/mode, stretch | S5 | `PROTOCOL_CONFIG_UNKNOWN` |
| operating state, register settings, stimuli, clocks, timebase, firmware trace provenance | S6, V5 | `RUNTIME_UNOBSERVED` |
| model artifact URI/hash, syntax, component pins mapping, validity envelope, license | V4–V6 | `MODEL_NOT_ELIGIBLE` |
| exact source citation, page/table/revision, fact confidence, override audit | every check | `PROVENANCE_MISSING` |
| 2D stable element/terminal/net anchors, snapshot hash | UI traceability | `ANCHOR_UNRESOLVED` |

**Hard consistency gates:**

- No dimensions-only guessing: `3.3V` rail label is not a 3.3 V power guarantee; `GPIO21` does not identify pin mux without exact device/revision.
- All internal quantities normalize to SI units and preserve original display unit and source. Distinguish volts from millivolts, current *rating* from observed current and **absolute max** from recommended operating range.
- A net with 3 terminals is represented as **one** electrical equivalence class. Crossing lines on a canvas do not connect without connection semantics; board header names are aliases only with explicit mappings.
- Unknown, manufacturer-typical and measured parameters are different typed evidence. A user-entered override never silently replaces manufacturer-documented ratings.
- Rule applicability must record operating modes (`boot`, `normal`, `sleep`, `power-off`, bus speed), temperature/supply conditions and dependencies.
- Electrical library/model references cannot automatically be republished: source license and permission belong to model metadata.

## 8. Model fidelity, uncertainty and unsupported-state policy

### 8.1 Non-negotiable result statuses

| Status | Meaning; public-facing Georgian interpretation | Required behavior |
|---|---|---|
| `SUPPORTED_PASS` | **მხოლოდ მოცემული პირობების ფარგლებში** წესი/მონაცემი შესაბამისია | expose checks, bounds and scope; never global circuit guarantee |
| `CONFIRMED_VIOLATION` | ცნობილი requirement/limit დარღვეულია | show inequality, source and affected IDs |
| `CONDITIONAL` | verdict changes with supplied mode/parameter; safe in some states, not others | list branches and assumptions |
| `UNKNOWN_MISSING_INPUT` | insufficient part/revision/mode/parameter | name exact missing input; never assume typical values |
| `MODEL_UNAVAILABLE` | eligible physical model missing or restricted | allow limited V1–V3, explicitly say *not simulated* |
| `OUT_OF_DOMAIN` | model used beyond validity range | refuse predictive claim, name invalid dimension |
| `SOLVER_FAILED` | numerical divergence/singular matrix/timeout | no electrical PASS or FAIL, retain diagnostics |
| `NOT_EVALUATED` | requested metric/feature outside implemented coverage | explicit unsupported-state explanation |
| `CONFLICTING_EVIDENCE` | sources disagree or model revision mismatch | request adjudication; use conservative warnings without fabricated certainty |

**One result may contain multiple independent statuses**: e.g. topology PASS; voltage-limit confirmed violation; I²C timing UNKNOWN. A single green “all good” badge is misleading.

### 8.2 Evidence/fidelity labels

- **E0 (identity/spec missing):** only structural depiction; no safety inference.
- **E1 (manufacturer bounded spec):** limit/constraint checks within named conditions.
- **E2 (analytical model):** derivation, input intervals and applicability defined; independent calculation/oracle available.
- **E3 (solver model, not physically validated):** model provenance and convergence known; output remains *simulated prediction*.
- **E4 (bench-validated envelope):** independent measurement and uncertainty for specific device/setup envelope; no universal extension.

These are **evidence descriptors**, not automatic probabilities. Confidence labels should distinguish **source reliability** (official manufacturer vs community model), **rule applicability**, **numerical quality**, **empirical fit**. `E3` cannot be assumed better than `E2`.

### 8.3 Uncertainty calculus

1. **Deterministic bounds first:** use datasheet min/max and resistance tolerances; for safety-critical thresholds, report upper/lower bound and worst-case branch. If no dependencies are known, report assumptions of independent worst-case rather than probability.
2. **Measurement uncertainty:** instrument accuracy/calibration, repeatability, temperature, supply variation, batch/revision differences; use JCGM GUM principles [R23]. Difference from simulation must be compared against the combined documented uncertainty, not raw nominal numbers.
3. **Probabilistic Monte Carlo only with distributions:** if PDFs/distributions and correlation are supported by evidence, document sampling; otherwise Monte Carlo generates false precision. JCGM 101 is a reference for uncertainty propagation, not a reason to assume distributions [R23].
4. **Numerical error separate from model error:** residual, solver tolerances, iteration/time-step, conditioning and sensitivity belong to the solver report; they do not quantify manufacturing uncertainty or datasheet model quality.
5. **Physical validation:** check within domain across independent points, not just fit parameters on the same data. A failure triggers diagnosis, not silent parameter tuning until outputs match.

**Educational communication policy:** user must see **(a)** what was checked, **(b)** on what evidence, **(c)** what was assumed, **(d)** what was not evaluated, **(e)** what would change the result. Safety-related claims cannot be stated solely as „works“.

## 9. Licensing and commercial integration matrix

**Interpretation:** „commercial use allowed“ does **not** imply permission to embed, statically link, redistribute bundled libraries, distribute third-party models or keep modified derivatives closed. Exact component/packaging and deployment method require legal review; SaaS/remote execution and distributed desktop/mobile binaries are not automatically equivalent.

| Component | Documented license / source | Commercial consideration and redistribution | Operational cost/security | Candidate disposition |
|---|---|---|---|---|
| **Own analytical rules/equations** | physical laws public; data sources individually licensed | equations reusable; datasheet text/tables, symbols and model datasets separately protected | lowest runtime; upkeep for device revisions | core candidate |
| **KiCad core/CLI** | predominantly GPL-3.0-or-later [R28] | GPL obligations if redistributing/derivative or combining at code level; CLI as separate process requires legal assessment; libraries separate | packaging/installation and conversion; headless reliability | comparator only |
| **KiCad official symbol/footprint libraries** | CC BY-SA 4.0 with KiCad-specific exception [R29] | do **not** assume free rebranding, proprietary catalog reuse or direct redistribution without reviewing exception/attribution | sync burden | not canonical catalog by default |
| **ngspice** | principally modified BSD; exceptions include LGPLv2 code paths; XSPICE status noted in upstream license/docs [R30] | distribution obligations differ by compiled contents; track third-party model licenses independently | native library isolation, CPU/memory, model parsing | optional V4 |
| **Xyce** | GPL-3.0-or-later [R08, R09] | copyleft for distributed combinations/derivatives; build stack/dependencies to audit | expensive compile/maintenance vs low need | defer |
| **Z3** | MIT [R15] | permissive, attribution/license notices; model constraints remain application's responsibility | runaway solver/timeouts can be bounded | optional |
| **Renode** | MIT [R18] | permissive runtime; bundled firmware/peripherals separately licensed | virtual SoC model coverage and maintenance | selective future |
| **Espressif QEMU fork** | QEMU overall GPLv2; per-file exceptions [R20, R31] | must evaluate redistribution/derivative and bundled firmware separately | full emulation sandbox; target coverage gaps | selective future |
| **OpenModelica** | OSMC-PL options / AGPLv3; terms depend on selected parts and mode [R32] | **not** blanket permissive; commercial architecture needs specialist review | complex runtime; little initial use | defer |
| **FMI specification / FMUs** | free open model-exchange standard; individual FMU licenses separate [R17] | exchanging an FMU ≠ distribution rights to its model/binary | native binary execution risk, timebase integration | future contract only |
| **Verilator** | LGPL-3.0 or Artistic-2.0 options [R22] | generated runtime/linked components and HDL inputs need scope-specific review | compiler/runtime and HDL testbench | no initial dependence |
| **Manufacturer SPICE models** | vary by vendor; TOREX explicitly restricts some redistribution and derivative copying [R27] | require per-model permission, user-provided local use if terms permit; do not mirror all vendor files | provenance, restrictions, potentially untrusted code | license-gated |

**Threat model for solver services:** untrusted uploaded netlists, subcircuits, scripts, macros, user FMUs or external native code may consume unbounded compute, read unauthorized files or execute unsafe workloads. Candidate controls: allowlisted syntax/analysis types; deny runtime code-model compilation; immutable container; no network; read-only filesystem; CPU/RAM/time/process limits; pinned signed binaries; per-user data isolation; quota/rate limits; versioned logs; document/license authorization. These controls are required **before** permitting public arbitrary simulation uploads; not assumed implemented.

## 10. Alternatives, rejected approaches and unnecessary dependencies

| Approach | Evaluation | Decision reason |
|---|---|---|
| **„ყველაფერი KiCad-ში გადაიყვანე და ERC-მა გადაწყვიტოს“** | **Reject as sole architecture** | ERC pin-type consistency is not exact voltage/current/runtime simulation [R02]; mapping loses user-meaningful board-level semantics unless separately preserved |
| **Use SPICE for every wire drag** | **Reject** | common topological/parametric conditions are cheap and exact as rules; missing models and solver startup can produce misleading false certainty |
| **Build a custom general SPICE/MNA nonlinear engine** | **Reject** | mature engines exist; extraordinary verification and maintenance cost without unique need [R04, R25] |
| **Place Z3 at center of all validation** | **Reject for core; reserve** | straight inequality checks do not need SMT; encoding and solver unknown/timeout add complexity |
| **Auto-simulate any ESP32 firmware in QEMU/Renode** | **Reject as promise** | per-SoC/peripheral coverage; analog/pin electrical behavior unmodeled [R19–R21] |
| **Start with OpenModelica / FMI ecosystem** | **Reject for first six** | no demonstrated multiphysics requirement, FMU availability or license budget [R16, R17] |
| **Use an LLM to infer components/voltages or declare circuit safe** | **Reject as authority** | unverifiable hallucinated limits cannot replace exact manufacturer sources or equations |
| **User-facing „fully simulated“ on successful solver exit** | **Reject** | numerical convergence ≠ valid model or real-world safety |
| **Adopt vendor simulation library by copying public downloads** | **Reject without rights** | publicly accessible is not synonymous with redistributable [R27] |
| **Manual-only catalog forever** | **Not mandated** | provenance-aware catalog imports may be viable, but automated ingestion requires document accuracy, change control, conflict review and rights |
| **Use CircuitJS/other browser simulator as sole compute source** | **Not substantiated** | educational visualization alone does not establish exact manufacturer part/pin and board-level semantics; no proven advantage over bounded analytical core |

**Key falsification question:** Is there any first-use-case failure whose answer *requires* ngspice, Xyce, Z3 or firmware emulation, rather than clearer datasheet facts and elementary equations? Until named, these dependencies are unjustified.

## 11. Minimal proof-of-capability experiments (design only; none executed)

**E1 — GPIO capability and mode.** Fixture: exact board and chip data, known input-only pin, valid bidirectional pin, alternate-function conflict, unknown firmware mode. Oracle: manual datasheet/reference pin table. **Gate:** reject provably unavailable function; don't reject valid function; `UNKNOWN` when state absent; UI points to correct terminal. No simulator.

**E2 — Logic-level safety.** Fixture: documented 5V-incompatible 3.3V pin, explicitly 5V-tolerant pin, missing absolute-limit record, optional level translator. Oracle: source/receptor specified electrical maxima/minima. **Gate:** correct separation of `VIH` functional compatibility from abs-max stress; no universal „3.3V pins always damaged by 5V“ rule.

**E3 — Loaded divider corner cases.** Fixture: 5.0/5.5V source; 10k/20k resistors; unloaded and 100k load; 5% tolerance cases. Oracle: independent hand-calculation and (if desired) ngspice DC `.op` on **the same** linear model. **Gate:** correct unloaded 3.333V and loaded 3.125V nominal; source/tolerance bounds exposed, no promise of safe GPIO based on nominal only. Note that a SPICE cross-check validates the numerical implementation, **not the datasheet inputs**.

**E4 — Power rail concurrency.** Fixture: 3 loads with separate idle/active/boot modes, 1 regulator with continuous/peak ratings; test impossible mutual-concurrency and possible simultaneous peak. Oracle: manually constructed state budget. **Gate:** no reliance on Σ typical values; clear conditional assumptions; `UNKNOWN` when regulator derating absent.

**E5 — I²C RC and domain.** Fixture: Fast-mode 3.3V, 200pF, documented 3mA sink; valid and out-of-range pull-ups; 5V pull-up on a non-5V-tolerant device; two pull-ups in parallel. Oracle: NXP UM10204 + TI SLVA689A [R13, R14]. **Gate:** correctly calculate ~0.967–1.77kΩ bound for supplied assumptions; distinguish timing vs overvoltage vs unknown capacitance.

**E6 — BME280 event sequencing.** Fixture: `ctrl_hum` write before/after `ctrl_meas`, forced-mode conversion, read while `status.measuring=1`, read after valid completion; missing trace. Oracle: Bosch register semantics and documented driver sequence [R11, R26]. **Gate:** flag unready/stale sample when proven, no fabricated firmware state, structured explanation from actual register data.

**E7 — Optional ngspice integration eligibility (not core build mandate).** Same passive divider, one RC step, one intentionally unmodelled sensor, one incompatible/forbidden vendor model. **Gate:** match analytical result within documented numerical tolerance for the same ideal model; `MODEL_UNAVAILABLE`/`LICENSE_BLOCKED` remain explicit; reproducible adapter and solver logs; no blanket sensor simulation claim. No speed benchmark claimed.

**E8 — Optional firmware virtual-execution coverage audit.** Choose **one** exact SoC, one program and a small set of peripherals supported by an identified Renode/QEMU release. **Gate:** produce a per-peripheral coverage manifest; demonstrate state/trace reproducibility; do not infer analogue input tolerance from firmware execution. This experiment is *conditional* on a clear unmet requirement, not a prerequisite for V1–V3.

**Cross-cutting acceptance criteria** (no invented numeric target): every test has at least one positive, negative, ambiguous/unsupported and boundary condition; recorded source + revision; independent expected result; change-resilient UI anchor; no `SUPPORTED_PASS` when critical facts are absent. Count false-safe decisions separately from false warnings. Make runtimes/cost measurable **during** future trials rather than assigning unsupported benchmark numbers now.

## 12. Scientific and technical references, versions and confidence

**Confidence meanings:** **High** = direct official vendor/project specification of a claimed feature or license; **Medium** = official general statement but exact device/version/interoperability untested; **Limited** = sound proposal not empirically verified in INVENTOR EDU. **Source confidence is not physical prediction accuracy.** Access/review date for sources below: **2026-11-20**.

| ID | Primary source and version | Specific evidence used | Confidence |
|---|---|---|---|
| **R01** | [KiCad CLI 10.0](https://docs.kicad.org/10.0/en/cli/cli.html); [10.0.8 release, 2026-10-30](https://www.kicad.org/blog/2026/10/KiCad-10.0.8-Release/) | `sch erc` report, CLI JSON and `sch export netlist` formats; current patch | High |
| **R02** | [KiCad Schematic Editor ERC 10.0](https://docs.kicad.org/10.0/en/eeschema/eeschema.html) | ERC pin-type conflicts, undriven nets and dependence on accurate symbol metadata | High |
| **R03** | [KiCad Getting Started 10.0](https://docs.kicad.org/10.0/mk/getting_started_in_kicad/getting_started_in_kicad.html) | explicit ERC does not guarantee design will function | High |
| **R04** | [ngspice news](https://ngspice.sourceforge.io/news.html), [documentation/manual 47](https://ngspice.sourceforge.io/docs.html) | ngspice 47, released Aug 2026, documented solver features | High |
| **R05** | [ngspice shared-library interface](https://ngspice.sourceforge.io/shared.html) | controlling functions and result callbacks | High |
| **R06** | [ngspice XSPICE](https://ngspice.sourceforge.io/xspice.html) | code models, event and mixed-signal abstractions | High |
| **R07** | [ngspice source/COPYING](https://github.com/ngspice/ngspice/blob/master/COPYING) | license composition and exceptions | High for project terms; dependent distribution review pending |
| **R08** | [Sandia Xyce official site](https://xyce.sandia.gov/), [News](https://xyce.sandia.gov/news/) | Xyce GPL and release **7.10**, Aug 2025 | High |
| **R09** | [Xyce documentation and FAQ](https://xyce.sandia.gov/documentation-tutorials/frequently-asked-questions/) | netlist translators, build/integration and API/co-sim caveats | High |
| **R10** | [FMI 3.0.2 official specification](https://fmi-standard.org/docs/3.0.2/) | Model Exchange vs Co-Simulation, FMU model interface | High |
| **R11** | [Bosch BME280 datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf), §5.4 | `ctrl_hum`, `ctrl_meas`, `status`, modes/timing | High for exact Bosch BME280 model; not clone sensors |
| **R12** | [Espressif ESP32 Series Datasheet](https://documentation.espressif.com/esp32_datasheet_en.html), §2, §5 | pin restrictions, electrical limits and revisions | High for named silicon; board-header mapping still required |
| **R13** | [NXP UM10204 Rev. 7 (2021)](https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/other/18306/1/UM10204_I2CSpec.pdf?inline=true), §7.1 | I²C pull-up min/max and RC timing | High |
| **R14** | [TI SLVA689A, revised Oct 2026](https://www.ti.com/lit/an/slva689/slva689.pdf) | standard/Fast-mode pull-up equations and numerical example | High |
| **R15** | [Z3 GitHub/docs](https://github.com/Z3Prover/z3), [release notes](https://github.com/Z3Prover/z3/blob/master/RELEASE_NOTES.md) | MIT, SMT-LIB2; reported release 4.15.6 | High for features/license; fit to specific workflow Limited |
| **R16** | [OpenModelica official release](https://openmodelica.org/), [download/version](https://openmodelica.org/download/download-windows/) | 1.27.1, released Sep 2026; equation-based tooling | High for version/capability; benefit Limited |
| **R17** | [FMI official site](https://fmi-standard.org/), [3.0.2 specification](https://fmi-standard.org/docs/3.0.2/) | FMU interface and model exchange; not universal solver | High |
| **R18** | [Renode release 1.17.0, Sep 2026](https://antmicro.com/blog/2026/09/renode-1-17-0-release), [GitHub license](https://github.com/renode/renode/blob/master/LICENSE) | hardware-software virtualization, MIT | High |
| **R19** | [Renode documentation](https://renode.readthedocs.io/en/latest/), [co-simulation](https://renode.readthedocs.io/en/latest/advanced/co-simulating-with-an-hdl-simulator.html) | scoped peripheral modeling / HDL interface | High for capability; exact target coverage Medium |
| **R20** | [Espressif ESP-IDF QEMU docs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/tools/qemu.html) | ESP32 fork, CPU/memory/some peripherals | High |
| **R21** | [Espressif QEMU scope and limitations](https://github.com/espressif/esp-toolchain-docs/blob/main/qemu/README.md); [Sep 2026 Zephyr example](https://developer.espressif.com/blog/2026/09/zephyr-espressif-qemu-hello-world/) | partial peripheral support and explicit lack of support for missing models | High |
| **R22** | [Verilator docs](https://verilator.org/guide/latest/overview.html), [license](https://verilator.org/guide/latest/copyright.html) | HDL simulation/lint; LGPL-3.0 / Artistic-2.0 | High |
| **R23** | [BIPM/JCGM GUM 100 & supplement 101](https://www.bipm.org/en/committees/jc/jcgm/publications/) | measurement uncertainty and Monte Carlo propagation methodology | High for metrology principles; specific application Limited |
| **R24** | [ASME VVUQ standards](https://www.asme.org/codes-standards/vvuq-standards) | verification/validation distinction; ASME V&V20 is CFD/heat-transfer domain, cited **by analogy only** | Medium for transfer to electronics; not an electronics compliance standard |
| **R25** | Ho, C.-W., Ruehli, A. E., Brennan, P. A., *The Modified Nodal Approach to Network Analysis*, IEEE Transactions on Circuits and Systems 22(6), 1975. [Publication record](https://mst.elsevierpure.com/en/publications/the-modified-nodal-approach-to-network-analysis/) | foundational MNA method | High for mathematics |
| **R26** | [Bosch BME280 SensorAPI](https://github.com/boschsensortec/BME280_SensorAPI), [pressure example](https://github.com/boschsensortec/BME280_SensorAPI/blob/master/examples/pressure/pressure.c) | official reference sequence and measuring-status behavior | High for reference API semantics; not automatically validated firmware timing |
| **R27** | [TOREX SPICE model use agreement](https://product.torexsemi.com/en/design-support/spicemodel/usage) | example of vendor restrictions on derivative model redistribution | High; conditions vendor/model-specific |
| **R28** | [KiCad software licenses](https://www.kicad.org/about/licenses/) | majority GPLv3-or-later | High |
| **R29** | [KiCad libraries license](https://www.kicad.org/libraries/license/) | CC BY-SA 4.0 with exception | High |
| **R30** | [ngspice developer licensing](https://ngspice.sourceforge.io/devel.html), [COPYING](https://github.com/ngspice/ngspice/blob/master/COPYING) | modified BSD with exceptions | High |
| **R31** | [QEMU source license](https://www.qemu.org/docs/master/about/license.html) | QEMU as a whole GPLv2; individual files may vary | High |
| **R32** | [OpenModelica Terms and License](https://openmodelica.org/terms-of-service/), [OSMC license](https://github.com/OpenModelica/OpenModelica/blob/master/OSMC-License.txt) | OSMC-PL/AGPL licensing modes | High for terms; integration implications require counsel |

### 12.1 What was and was not verified

- **Verified by published, directly inspected primary descriptions:** current named releases, main engine capabilities, KiCad CLI export/ERC boundaries, I²C equations, BME280 register sequence, major upstream license statements and QEMU/Renode fidelity caveats.
- **Not independently executed or benchmarked:** headless KiCad/netlist interchange; ngspice↔Xyce semantic parity; any SPICE manufacturer model with actual chips; Renode/QEMU target coverage for a nominated INVENTOR EDU board; solver performance, latency or cloud cost; real 2D integration; physical circuit measurement. Claims about these remain **architectural hypotheses** rather than empirical results.
- **Revision limits:** a `latest` upstream documentation branch can move after this research date; pin electrical limits and legal licenses must be locked to exact component/model/document releases at actual use. The version table is a dated evidence snapshot, not a future guarantee.

---

## DECISION RECORD CANDIDATE

**Status:** **PROPOSED FOR ARCHITECTURE REVIEW — NOT APPROVED.**  
**Decision question:** What is the smallest scientific computation surface that can honestly verify common educational electronics connections, while permitting future simulation where proven necessary?

### A. Essential to the first working core (candidate)

1. **Exact component/terminal/net identity and provenance contract** from the approved canonical model; no reliance on canvas geometry as electrical source of truth.
2. **Deterministic topology + pin-function + voltage-domain + protocol validation**, including explicit normal/absolute limit and mode-conditional results.
3. **Small, audited analytical library:** Ohm/KCL/KVL, loaded divider, DC power/load budgets, RC rise-time, bounded worst-case interval comparisons; closed-form first, no new universal SPICE clone.
4. **Structured findings with `SUPPORTED_PASS / CONFIRMED_VIOLATION / CONDITIONAL / UNKNOWN / UNSUPPORTED / SOLVER_FAILED`-type semantics**, provenance, versioning, assumptions and 2D anchors.
5. **Evidence-constrained Georgian explanations** that do not fabricate ratings or promise real-hardware predictability.
6. **Positive, negative, boundary and unsupported-state fixtures** on the six scenarios, with independent calculation/datasheet oracles.

### B. Optional, requiring a problem-specific gate

- **KiCad ERC adapter:** only if equivalence/cross-check to the approved engineering semantics is beneficial and reliable. Do not make its netlist format canonical by default.
- **ngspice 47:** only when a named analogue/transient problem requires more than validated elementary formulas, model eligibility and license are demonstrated, and an isolated integration passes a reproducible oracle.
- **Z3:** only when valid pin/resource/configuration search becomes sufficiently combinatorial that typed rule enumeration is demonstrably inadequate.
- **Renode / Espressif QEMU:** only after an exact target+firmware+peripheral coverage contract demonstrates value that register-level FSMs cannot supply.
- **FMI / OpenModelica:** only after a demonstrated, bounded coupled/multidomain model and model-license availability; evaluate synchronization and residual error empirically.

### C. Not to adopt without further evidence

- Xyce as a routine starter dependency; OpenModelica as a default simulator; general HDL/Verilator environment; custom nonlinear SPICE engine; automatic full ESP32 hardware simulation; blanket third-party manufacturer-model mirroring; unconstrained LLM engineering verdicts; UI that calls every validated connection a “physics simulation.”

### D. Criteria for changing the candidate decision

The architecture owner should require **all** of the following for any extra engine: (1) identified user-visible failure unsolved by the simpler method; (2) exact supported device/observable/mode envelope; (3) available and legally usable model with provenance; (4) independent positive/negative/boundary oracle; (5) measured incremental accuracy/coverage against integration/maintenance/security cost; (6) failure semantics that avoid false-safe results.

**Open architecture-owner questions:** Which exact first devices and board revisions are supported? Is the first product a wiring verification tool, a parametric calculator or a physical simulator—and which user claim is being tested? Will models be executed on-device, on a server, or only supplied as third-party exports? Which manufacturer device facts are redistributable? What is the acceptable false-safe behavior when a pin's electrical specification is incomplete? No architectural choice is finalized until these contracts are approved.

**Final research position:** The scientifically defensible first core is **scope-limited verification with bounded electrical calculations**; simulation is a **selective, evidence-gated extension**, not the definition of the product.
