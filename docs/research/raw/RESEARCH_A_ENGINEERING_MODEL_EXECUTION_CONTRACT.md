# RESEARCH A — Executable Engineering Model & Connectivity Contract

**ფაილი:** `RESEARCH_A_ENGINEERING_MODEL_EXECUTION_CONTRACT.md`  
**პროექტი:** INVENTOR EDU — დამოუკიდებელი Georgian-first საგანმანათლებლო ელექტრონიკის პლატფორმა  
**კვლევის/წყაროების შემოწმების თარიღი:** 2026-11-20 (Asia/Tbilisi)  
**სტატუსი:** ტექნიკური კვლევა და **დასამტკიცებლად შემოთავაზებული** კონტრაქტი; არ არის არქიტექტურის საბოლოო გადაწყვეტილება, გაშვებული კოდი, ინტეგრაციის ანგარიში ან Codex-ის დავალება.

**კლასიფიკაციის ნიშნები:** **[F]** — დოკუმენტირებული პირველადი წყაროს ფაქტი; **[M]** — მათემატიკური/გრაფული დასკვნა; **[R]** — ავტორის არქიტექტურული რეკომენდაცია; **[U]** — UNVERIFIED/საჭირო მტკიცებულება. წყაროთა იდენტიფიკატორები `[S01]` და სხვ. განმარტებულია §14-ში. **`SUPPORTED_TOPOLOGY` არ უდრის `ELECTRICALLY_SAFE`-ს.**

## 1. Executive recommendation

**[R] დასამტკიცებელი კანდიდატი:**

- **კანონიკური მოდელი:** მცირე, მკაცრად ტიპიზებული, ვერსირებული Python/Pydantic v2 ჩანაწერები: `DeviceDefinition`, `TerminalDefinition`, `CatalogSnapshot`, `ComponentInstance`, `TerminalRef`, `Junction`, `Conductor`, `CircuitSnapshot`, `TopologyResult`. მწარმოებლის დოკუმენტაცია არ არის runtime-გრაფი; ექსპორტი და UI ხედი ცალკეა.
- **ტოპოლოგია:** არამიმართული გრაფის connected components, **ყოველ ცვლილებაზე თავიდან რეკონსტრუქცია**, სტანდარტული Python-ის `collections.deque`-ზე დაყრდნობილი განსაზღვრული BFS. მხოლოდ დოკუმენტურად დადასტურებული *იდეალური/მყარი* შიდა გამტარები შეიძლება ჩაირთოს გრაფში. მავთულის წყვეტა, დიოდი, რეზისტორი, რეგულატორი, მაღალი წინაღობის პინი და საერთო წარწერა **არ ქმნის** ავტომატურ ელექტრულ ეკვივალენტობას.
- **მოწყობილობის წყაროები:** Espressif **ESP32-DevKitC V4 / orderable variant `ESP32-DevKitC-32E` / on-board `ESP32-WROOM-32E`** და Adafruit-ის **retail Product ID 3942**. უკანასკნელის *მოწყობილობის რეალური მწარმოებელი/PCB-რევიზია არ არის დადასტურებული*; მასზე maker-grade/absolute-limit მტკიცებების განზოგადება არ დაიშვება.
- **გარე runtime დამოკიდებულება:** Pydantic `==2.14.4` (MIT) ზუსტად განსაზღვრული ვალიდაცია/სქემა/რესტავრაციის საზღვრისთვის. **NetworkX `==3.7`** (BSD-3-Clause) მხოლოდ *დამოუკიდებელი სატესტო oracle*; `Hypothesis ==6.170.17` (MPL-2.0) — development/test-only. Production გრაფისთვის NetworkX-ს დამატებითი ფასეულობა არ გამოუვლენია ამ დახურულ მასშტაბზე; §4-ში მოცემულია უკუარყოფის კრიტერიუმი.
- **ფორმატი:** UTF-8 JSON envelope, `schema_version="1.0"`, ყველა კოლექციის მკაფიო ალფანუმერული იდენტობა, გამორჩევა *stable user-assigned IDs* და *derived net membership fingerprint*-ის. `sha256` განისაზღვრება მხოლოდ მკაფიო canonical-bytes პროფილისათვის; `model_dump_json()` **არ არის** თავისთავად კრიპტოგრაფიულად კანონიზებული ბაიტების გარანტია.

**რატომ არის ეს ყველაზე მცირე სრული მოდელი?** მას შეუძლია იპოვოს ერთი ნეტის ყველა ტერმინალი, გამოავლინოს გამოუსადეგარი/არარსებული კონტაქტის მიმართვა, შეინარჩუნოს მოწყობილობისა და პინის იდენტობა, ზუსტად გაიმეოროს შედეგი და გადასცეს დასაბუთებული ნეტები დამოუკიდებელ ვერიფიკატორს. ამ ეტაპზე **არც KiCad ERC, არც SPICE, არც PCB geometry, არც საკუთარი ზოგადი EDA ontology** არ არის აუცილებელი. ეს არის კანდიდატი და არა უკვე მიღებული ტექნიკური გადაწყვეტილება.

## 2. Required capabilities and invariants

### 2.1 მინიმალური გარანტირებული შესაძლებლობა

1. ორი შერჩეული ტიპის ზუსტად იდენტიფიცირებული მოწყობილობის განმარტებების ჩატვირთვა კონკრეტული catalog-digest-ით.
2. ინსტანსების შექმნა ორიგინალის შეცვლის გარეშე; ერთი და იგივე განმარტების მრავალჯერადი გამოყენება.
3. `terminal-to-terminal`, `terminal-to-junction` და `junction-to-junction` მყარი გამტარების შენახვა; არარსებული ტერმინალის უარყოფა.
4. კომპონენტის შიგნით მხოლოდ პირდაპირ დადასტურებული იდეალური საერთო ნეტის გათვალისწინება, **არა ნებისმიერი შიდა ელექტრონული კავშირის**.
5. ნეტების სრული და გამეორებადი დათვლა, მათ შორის ერთი წევრისგან შემდგარი გამოუყენებელი/ღია ტერმინალები.
6. ერთგვაროვანი serialized round-trip; ზომიერად შეცვლილი 2D-ხედისაგან საინჟინრო hash-ის დამოუკიდებლობა.
7. სტრუქტურირებული, ლოკალიზაციისგან დამოუკიდებელი შედეგები; ქართულენოვანი ახსნა შემდგომი adapter-ის საქმეა.

### 2.2 ინვარიანტები — **MUST**

| ID | ფორმალური პირობა | დარღვევის შედეგი |
|---|---|---|
| I01 | `definition_id` მიუთითებს ზუსტად ერთ immutable `definition_digest`-ზე | `CATALOG_DIGEST_MISMATCH` ან `UNKNOWN_DEFINITION` |
| I02 | ინსტანსის `instance_id` უნიკალურია ერთ snapshot-ში | `DUPLICATE_ID` |
| I03 | ყველა `TerminalRef(instance_id, terminal_id)` შედის ზუსტ განმარტებაში | `UNKNOWN_TERMINAL` |
| I04 | `Junction.id` უნიკალურია, სხვა vertex namespace-იდან განსხვავდება | `DUPLICATE_ID` |
| I05 | ყველა `Conductor`-ის ორივე ბოლო არსებობს, განსხვავებულია და დალაგებადი საკვანძო ID აქვს | `INVALID_ENDPOINT` / `SELF_LOOP` |
| I06 | ტერმინალის სახელის მსგავსება, GPIO ნომერი, screen coordinates ან voltage-label **არ** აერთებს ტერმინალებს | არავითარი implicit edge |
| I07 | დოკუმენტურად დადასტურებული შიდა ties მხოლოდ ერთ კონკრეტულ immutable მოწყობილობის პროფილზე ვრცელდება | incomplete evidence → **tie არ იქმნება** |
| I08 | ყველა ტერმინალი ზუსტად ერთ connected component-შია | topology invariant |
| I09 | ერთი და იმავე wire-ის შებრუნება/ჩამატების თანმიმდევრობა არ ცვლის `terminal_to_net`-ს | topology invariant |
| I10 | 2D geometry არც canonical snapshot-შია, არც net fingerprint-ის preimage-ში | view-invariance |
| I11 | წყაროში დაკარგული დიაპაზონი/რევიზია არ იქცევა „ნორმალურ მნიშვნელობად“ | `UNKNOWN_EVIDENCE` / unsupported verification |
| I12 | მუტაცია ცვლის snapshot-ს მხოლოდ ახალი ვერსიით; არსებული `CircuitSnapshot` აღარ იცვლება | API contract violation |

**[R] ვალიდაციის საზღვრები:** (i) დეკოდირება/სქემა — ტიპები, დამატებითი ველები, ელემენტების ფორმა; (ii) catalog integrity — identity, evidence, version, ცალსახა mapping; (iii) circuit integrity — ბმულების არსებობა, unique IDs, cross-reference; (iv) topology — გაწყვეტილი/შეერთებული კლასების გამოთვლა; (v) electrical verification — სხვა ფენა და სხვა მტკიცებულებები. Schema-valid ≠ domain-valid ≠ electrically safe.

## 3. Existing implementations and exact usable APIs

| კანდიდატი | გადამოწმებული შესაძლებლობა / API | რეალური როლი | საზღვარი და ზედმეტი ინტეგრაციის ფასი |
|---|---|---|---|
| **KiCad 10.x** | `.kicad_sch`-ში `uuid`, `junction`, `wire`, `no_connect`; `kicad-cli sch export netlist --format kicadxml INPUT_FILE`; `kicad-cli sch erc` [S01–S03] | შედარებითი ნიმუში explicit junction-ის, კავშირის/export-ის და identity-ისთვის; შემდგომში შესაძლო ფაილური adapter | native KiCad schematic parser, GUI, Qt/C++ API, symbol/PCB schema და ERC semantics არ არის საჭირო ამ 2-ობიექტიან ამოცანაში; GPIO 5V safety არ დასტურდება მხოლოდ ERC-ით |
| **LibrePCB 2.1.1** | `symbol pin → component signal → device package pad` map; device-ზე კონკრეტული manufacturer/MPN; UUID reference [S04–S06] | მეტამოდელის პრინციპები და pinout-ის ინდივიდუალური წყაროთი დადასტურება | `LibrePCB` C++/Qt/Rust ეკოსისტემის დაკავშირება ზედმეტია; GPLv3 source პირდაპირ არ გადმოვიტანოთ |
| **NetworkX 3.7** | `nx.Graph()`, `G.add_nodes_from`, `G.add_edges_from`, `nx.connected_components(G)`, `nx.node_connected_component(G, n)` [S07–S08] | test oracle და შესაძლო შემდგომი მრავალ-ალგორითმიანი adapter | production-ში 2+ MB dependency, generic graph interface, დამატებითი supply-chain სავალდებულოობა; insertion order კომპონენტთა გამოტანის წესად არ ვარგა, sort მაინც საჭიროა |
| **Python stdlib 3.12** | `collections.deque`, `set`, `dict`, `sorted`, `json.dumps/loads`, `hashlib.sha256`, `dataclasses.dataclass` [S09–S11] | connected components-ის საბაზისო კანდიდატი და მკაცრად განმარტებული JSON bytes | ვალიდაციის მექანიზმი/სქემის გენერაცია ხელით უნდა დაიწეროს, თუკი Pydantic არ გამოიყენება |
| **Pydantic 2.14.4** | `BaseModel`, `ConfigDict(extra='forbid', frozen=True, strict=True)`, `Field`, `model_validator`, `model_validate`, `model_validate_json`, `model_dump(mode='json')`, `model_json_schema` [S12–S14] | გარე და შიდა ტიპიზებული ჩანაწერები ერთ მოდელად; დამატებითი DTO-ების გარეშე | `frozen=True` shallow/faux-immutabilityა; `dict`/`list` mutable field-ები არ დაიშვას; JSON რიცხვებისა და datetime-ის coercion-ზე საკუთარი ტესტები აუცილებელია |
| **Python dataclasses** | `@dataclass(frozen=True, slots=True)`, `__post_init__`, `dataclasses.replace` [S10] | Pydantic-ის ალტერნატიული მსუბუქი typed records | JSON boundary/schema, nested validation, strict type rejection, cross-reference error paths — ცალკე ხელით სამუშაო |
| **DSU / union-find** | parent/rank/path-compression ოპერაციები, Tarjan-ის სირთულის ანალიზი [S15] | add-only connectivity კანდიდატი | წაშლისას ერთი `union` არ იშლება; მაინც სრული აღდგენა ან dynamic-connectivity სტრუქტურაა საჭირო |

**[F]** NetworkX `connected_components` იყენებს BFS-ს და აღწერს `O(n+m)` დროით სირთულეს; `Graph.add_edges_from()` ერთი და იმავე edge-ს ერთჯერ ინახავს (მის ატრიბუტებს ცვლის), ხოლო `MultiGraph` გამოიყენება parallel-edge-სთვის [S07–S08].  
**[R]** გამომავალი ნეტის კუთვნილება უნდა გამოითვალოს უშუალო, ბიბლიოთეკებისგან დამოუკიდებელი გრაფის სპეციფიკაციით; NetworkX მხოლოდ კონტროლია და არა კანონი, რის მიხედვითაც ცდები იწერება.

## 4. Dependency comparison and recommendation

### 4.1 Decision table

| არჩევანი | სარგებლობა პირველ შესაძლებლობაში | უარყოფის/მიღების კრიტერიუმი | კანდიდატი |
|---|---|---|---|
| Custom domain graph + stdlib BFS | ერთი traversal, მცირე კოდი, წაშლის სუფთა semantics, 0 graph dependency | უარყავით **მხოლოდ** თუ მოთხოვნილი ახალი graph operations იმდენია, რომ ტესტირებული stdlib ვარიანტი სირთულით აჭარბებს mature API-ს | **production** |
| `networkx.Graph` + `nx.connected_components` | დამტკიცებული API, ცალკე გრაფის ალგორითმის მოვლა არ სჭირდება | full graph library ნაკლებად საჭიროა მხოლოდ CC-ზე; API მაინც მოითხოვს domain-to-graph გარდაქმნას | **test-only independent oracle**; კანდიდატი თუ scope გაიზრდება |
| DSU ყოველი snapshot-ისათვის | სწრაფი union და მარტივი ეკვივალენტობის კლასები | დაზოგვა არ არსებობს ასეთ მასშტაბზე; deletion/reconnect მაინც rebuild | უარყოფილი პირველ ფაზაში |
| Incremental dynamic connectivity | ბევრი ცვლილებისას შესაძლოა კარგი წარმადობა | მხოლოდ დამტკიცებული bottleneck/large graphs და მკაცრი deletion tests | უარყოფილი |
| Stdlib dataclasses + manual schema | runtime dependency არ სჭირდება | reject როცა untrusted JSON-ის სრული typed validation აუცილებელია და DIY ვალიდაციის კოდი იზრდება | მეორე არჩევანი |
| Pydantic v2 records | მკაფიო validation, JSON Schema, immutable-style models, typed failures | უარყავით, თუ Rust extension/distribution constraints ობიექტურად შეუთავსებელია target-ს ან benchmark-ით overhead მიუღებელია | **runtime** |
| Native KiCad/LibrePCB core | უფრო მდიდარი EDA შესაძლებლობები | არ ამართლებს პირველ connectivity feature-ს, GPL საზღვრები და runtime მძიმეა | არა |

**[R] შემოთავაზებული ვერსიული პროფილი:** CPython `3.12.x` (მცირე security patch განახლება დასაშვებია ტესტებით), Pydantic `2.14.4` exact, `networkx==3.7` test-only, `hypothesis==6.170.17` test-only. PyPI-ზე 2026-11-20-ისთვის ეს გამოცემები, ლიცენზიები და Python requirements დადასტურებულია [S08, S12, S16]. ფაილური ქეშის/hash-ის გამეორებადობას მხოლოდ exact dependency ვერსია **არ** უზრუნველყოფს: აუცილებელია lockfile და digest.

**[M] ვრცელი ალგორითმის მიღება არ არის არგუმენტი მისი აუცილებლობისთვის.** BFS არის გრაფის კომპონენტების ზუსტი ამომთვლელი და არ ქმნის სტრუქტურული ოპტიმიზაციის ფარულ ვალდებულებებს. შეადარეთ `nx.connected_components`-თან გენერირებულ გრაფებზე, მაგრამ სატესტო oracle-მარტო-თვითონ correctness proof არ არის.

## 5. Proposed canonical semantic contract

### 5.1 ობიექტები და აუცილებელი ველები [R]

`ID` = ASCII regex `^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$`; case-sensitive; ყველა ID namespace-ით მუშავდება. `TerminalRef` **სტრუქტურული წყვილია** `(instance_id, terminal_id)`, არ არის შემთხვევითი string parse. გარე durable ID-ს ქმნის ავტორინგის ფენა **მხოლოდ ერთხელ** (მაგ. UUID-ის ლეგალური სტრიქონული ფორმა სხვა სტაბილური პროექტის ID-ით); ალგორითმი არ გენერირებს ინსტანსის ან სადენის ID-ს.

| ობიექტი | Mandatory v1 | Extension/NOT NOW |
|---|---|---|
| `DeviceDefinition` | `definition_id`, `definition_digest`, `kind ∈ {dev_board,sensor}`, `identity`, `terminals`, `internal_ideal_ties`, `evidence_claim_ids`, `definition_schema_version` | symbol variants, detailed behavioral circuits, package/3D, simulation |
| `DeviceIdentity` | `brand_or_distributor`, `manufacturer_status`, `manufacturer_name?`, `orderable_part_or_sku`, `hardware_family`, `hardware_revision_status`, `hardware_revision?`, `assembled_module?`, `silicon_revision_status` | serial number and supplier lot, alternates; არასოდეს auto-canonicalize clone |
| `TerminalDefinition` | `terminal_id`, `physical_connector_id`, `physical_contact_position`, `printed_label`, `electrical_role ∈ {power,ground,io,input,output,other,unknown}`, `signal_ref?`, `capability_claim_ids` | alternate pinmux config, curves, GPIO electrical limits |
| `SignalMapping` | `terminal_id`, `target_kind ∈ {soc_gpio,power_domain,signal,unknown}`, `target_id`, `source_claim_id`, `mapping_status` | board-to-chip multi-hop map, internal routing impedance |
| `ComponentInstance` | `instance_id`, `definition_id`, `definition_digest`, `user_label?` | orientation, pixel position, graphical rotation (only ViewModel) |
| `TerminalRef` | `instance_id`, `terminal_id` | display aliases |
| `Junction` | `junction_id` (explicit electrical joining point) | x/y, spline/crossing graphics |
| `Conductor` | `connection_id`, `endpoint_a: VertexRef`, `endpoint_b: VertexRef`, `kind='ideal_wire'` | length/diameter/resistance, bus width, harness geometry |
| `CircuitSnapshot` | `schema_version`, `catalog_digest`, `instances`, `junctions`, `conductors`; nested tuples | UI state, firmware, source-only models, output findings |
| `CatalogSnapshot` | `catalog_schema_version`, `definitions`, `source_documents`, `claims`, `catalog_digest` | remote auto-sync, permissions |
| `TopologyResult` | `topology_schema_version`, `snapshot_sha256`, `nets`, `terminal_to_net`, `connection_to_net`, `isolated_terminals` | voltage/current/pass/fail, graphics |
| `EvidenceClaim` | `claim_id`, `claim_type`, `value`, `source_document_id?`, `locator?`, `source_class`, `scope`, `qualification`, `review_status` | formal uncertainty propagation, lab metrology |

**[R] ატომურობის წესი:** `ComponentInstance` არასოდეს შეიცავს გამომუშავებულ GPIO mapping-ს ან დუბლირებულ დოკუმენტის ელექტრულ პარამეტრებს; ის მიუთითებს pinned `DeviceDefinition`-ზე. `TerminalDefinition` არის *ფიზიკური exposed contact*, ხოლო GPIO18 არის `SignalMapping.target_id`, **არა** `J3.9`-ის სინონიმური ID. `J3.9` და `J2.9` სხვადასხვა physical contact-ია, თუნდაც მათ სახელებს მსგავსება ჰქონდეს.

**მნიშვნელოვანი ახალი დეტალი:** ბორტზე სხვადასხვა ფიზიკური GND contact-ები შეიძლება რეალურად ერთ copper net-ზე იყვნენ. ასეთი კავშირი **მხოლოდ** `internal_ideal_ties`-ით აღიწერება და ექვემდებარება maker-schematic ფაქტებს. სინთეზურ გაკვეთილში წარმოსახული ორი power-label **არ** იწვევს implicit union-ს.

### 5.2 მკაცრი წესები snapshot-ის დონეზე

- ყველა list-collection გარდაიქმნას immutable tuple-ად; map-field v1-ში საერთოდ არ გამოიყენოს ან იყოს შეცვლადი სტრუქტურისგან იზოლირებული. `frozen=True` მარტო საკმარისი არ არის [S13].
- `definition_digest` SHA-256 შენიშვნის გარეშე არ ითვლება სწორად: უნდა ჰქონდეს canonical source JSON bytes წესები (§7/§8).
- `definition_id` და `identity` ვერ გადაფარავენ ერთმანეთს ნაწილობრივი სახელით. Unknown family/board/clone იწვევს `UNSUPPORTED_DEVICE`-ს, არა ავტომატურ ყველაზე მსგავს პროფილს.
- `GPIO` capability (`input_only`, `output_allowed`, `flash_reserved`, `strapping`) ცალკე fact-ია და მოქმედებს დაფის/მოდულის/კონფიგურაციის კონტექსტში. `mapping_status=unknown` არ იწვევს capability-ის დადებით დასკვნას.
- კონტაქტის `power`/`ground` ტიპი არის დანიშნულება და არა უკვე გამოცემული ძაბვის გაზომვა. კვების მოქმედი წყარო, რეჟიმი და მულტიპლექსირება შემდგომი verification context-ის ნაწილია.
- `VCC`, `GND`, `Trig`, `Echo` არის ოთხი დამოუკიდებელი sensor-interface contact. უკანა პლატაზე შიდა მიკროსქემა **არ უნდა** გადაიქცეს DC-short ნეტად.
- `Junction` არის ელექტრული merge-ის განზრახ ჩასმა; გეომეტრიული crossing-ისას junction არ წარმოიქმნება.
- `Conductor`-ის endpoint-ები სხვადასხვა `VertexRef`-ებია; missing/self-loop reject. ორ სხვადასხვა `connection_id`-ს ერთსა და იმავე ორი ბოლო შეიძლება ჰქონდეს — ორი რეალური იდენტობის გამტარი, მაგრამ ერთი გრაფული edge.

### 5.3 იდენტობისა და UI anchor-ის ურთიერთობა

შემდგომი `ViewDocument` შეიცავს `view_id`, `instance_id`, `terminal_id`, `anchor_id`, `x`, `y`, `wire_curve_points`; მხოლოდ `instance_id/terminal_id` უკავშირდება საინჟინრო ბირთვს. Geometry-ის ნებისმიერ ცვლილებაზე `CircuitSnapshot`-ის bytes/hash და topology **ზუსტად იგივე** უნდა იყოს. View-only labels ქართულად/ინგლისურად არ არის engineering identifiers.

## 6. Proposed connectivity algorithm and formal behavior

### 6.1 გრაფის ფორმალური განსაზღვრება [M + R]

- `V_T = {(instance_id, terminal_id) | definition's exposed terminals instantiated}`; `V_J = {junction_id}`; `V = V_T ⊔ V_J` (disjoint tagged union).
- `E_W = {{a,b} | valid Conductor(a,b)}`. არამიმართულია; duplicate და reversed წყვილები შერწყმულია **მხოლოდ გამოთვლისას**.
- `E_I =` pinned definition-ით დადასტურებული `internal_ideal_ties`. N-ტერმინალიანი tie ჯგუფისათვის გამოიყენება **ერთი root→დანარჩენი N−1** წიბო; O(N²) pairwise edge-ები არ არის საჭირო. არც დიოდი, არც power rail რეგულატორი არ არის `E_I`.
- `G=(V,E_W∪E_I)`. ელექტრული ნეტებია გრაფის კომპონენტები, **მხოლოდ იმ ნაწილებისათვის, რომლებშიც ≥1 physical terminal შედის**. `junction-only` orphan კომპონენტები უნდა უარყოფილ იქნეს `ORPHAN_JUNCTION_GROUP`-ით (არ გადაიქცეს „ცარიელ ნეტად“).
- ყველა disconnected terminal არის singleton-net; `no-connect` intent მომავალში ცალკე სტატუსია და არა terminal-ის გაქრობა.

**დადასტურების საზღვარი:** net აქ იდეალური გამტარების ეკვივალენტობის კლასია; resistor/LED/diode/device behavior სისტემაში **არც edge-ია, არც short**. შემდგომი circuit-theory solver შეიძლება კომპონენტების მეშვეობით ნეტებს შორის დამოკიდებულებას დაამატებდეს, მაგრამ მათი შერწყმა ფიზიკურად მცდარია.

### 6.2 ზუსტი კანდიდატი (არა კოდი)

1. ვალიდირებული immutable snapshot-ის ყველა exposed terminal და explicit junction გადაიყვანეთ ტიპიზებულ canonical vertex key-ზე. `terminal`/`junction` სხვადასხვა namespace-ით, უბრალო შედარებადი სტრიქონები.
2. დაამატეთ unordered conductor edge-ები, მათი ბოლოები დაადასტურეთ; runtime დუბლიკატი წყვილი ერთ graph-neighbor relation-ად ჩაითვალოს. ცალკე შეინახეთ `connection_id → endpoint pair`, რათა ერთი wire-ის წაშლამ მეორე არ წაშალოს.
3. დაამატეთ `internal_ideal_ties` მხოლოდ source-verified definition-იდან; მათ იდენტობებს მომხმარებლის connection ID არ აქვთ.
4. მკაცრად დალაგებული vertices-ით (lexicographic, case-sensitive UTF-8/ASCII key) ყოველი ჯერ არნახული vertex-დან გაატარეთ BFS; queue = `collections.deque`; visited = `set`; adjacency = `dict[VertexKey, set[VertexKey]]`. კომპონენტის წევრები დაალაგეთ.
5. დათვალეთ მხოლოდ physical terminal წევრებისთვის ერთი sorted tuple `members`. `net_id = "net:sha256:" + SHA256( UTF8("INVENTOR-EDU-NET-V1\\n" + joined(sorted(terminal keys), "\\n")) ).hexdigest()`; terminal key-ის canonical representation გამოიყენოს length-safe ფორმა: `"T:" + instance_id + "/" + terminal_id` (ID-ში `/` და newline აკრძალულია). **ჯანკშენის ID არ შედის** net fingerprint-ში: junction-ის ვიზუალური/არასემანტიკური გადანაცვლება წევრობის შეუცვლელად net ID-ს არ ცვლის.
6. `nets` დალაგდეს `members[0]`-ით; `terminal_to_net`, `connection_to_net` გასცეს `terminal key`/`connection_id`-ით დალაგებულად. `connection_to_net` აღნიშნავს ორივე endpoint-ის ერთსა და იმავე net ID-ს. `isolated_terminals` = physical terminals, რომელთა connected component-ში მეორე physical terminal არ არის; **მხოლოდ junction-connected orphan „სადენი“ მაინც ამ მნიშვნელობით isolated-ა**.
7. წაშლა: მონიშნული `connection_id`-ის ამოღებით შეიქმნას **ახალი** snapshot და ნაბიჯები 1–6 გამეორდეს. თუ პარალელური იგივე წყვილი დარჩა, net არ იყოფა. `E_I` user edit-ით არ იშლება.

**Net identity-ის ორი განსხვავებული მოთხოვნა:** `{members}`-ზე ჰეში სტაბილურია ordering/duplicate/geometry ცვლილებისას, მაგრამ **სწორად იცვლება**, როცა კავშირის შეცვლით net-ის წევრობა იცვლება. ამიტომ `finding`-ს ჰქონდეს `rule_id + terminal_refs + instance_ids + snapshot_sha256`, ხოლო net_id მხოლოდ მიმდინარე snapshot-ის დასაკავშირებელი secondary key. `net_id` არ წარმოადგენს ისტორიაში მარადიულ stable wire identifier-ს.

**სირთულე [M]:** traversal-ის შიდა ღირებულება `O(V+E)`, space `O(V+E)`. დალაგება/კანონიზაციის სრული deterministic pipeline უარეს შემთხვევაში `O(V log V + E log E)`; ეს განსხვავება არ უნდა დაიმალოს „O(V+E) საერთო runtime“-ის მტკიცებით. user-sized board/sensor ქსელში პირველადი bottleneck მოსალოდნელია data validation, თუმცა benchmarking **არ შესრულებულა**. დიდი snapshot-ებისთვის წინასწარ დაწესდეს ზომის/შეყვანის ლიმიტი და იზომებოდეს p95.

**სისწორის საფუძველი [M]:** BFS პოულობს თითოეული vertex-დან ყველა მისაწვდომ vertex-ს და არცერთ მიუწვდომელს; connectedness არის რეფლექსიური, სიმეტრიული, ტრანზიტიული, ამიტომ თითოეული vertex ზუსტად ერთ ეკვივალენტობის კლასშია. დუბლიკატი edges მისაწვდომობას არ ცვლის; შებრუნებული edge არ ცვლის undirected adjacency-ს. მხოლოდ edge deletion შეიძლება დაშალოს კლასი; სრული rebuild სწორად ითვალისწინებს ამას. ეს არ არის ელექტრული *უსაფრთხოების* მტკიცება.

## 7. Proposed module interfaces

**შენიშვნა:** ქვემოთ **API-ის ტიპობრივი წინადადებებია და არა შესრულებული პროგრამული კოდი**. Data models არის Pydantic-ით დასადგენი immutable-style structures; ფუნქციის სახელები/გამონაკლისები იკეტება მხოლოდ §15-ის დამტკიცების შემდეგ.

```python
# contract signatures ONLY; no implementation
load_catalog(payload: bytes, *, expected_sha256: str | None = None) -> CatalogSnapshot
resolve_terminal(catalog: CatalogSnapshot, snapshot: CircuitSnapshot,
                 ref: TerminalRef) -> ResolvedTerminal
create_snapshot(catalog: CatalogSnapshot, *, instances: tuple[ComponentInstance, ...],
                junctions: tuple[Junction, ...],
                conductors: tuple[Conductor, ...]) -> CircuitSnapshot
compute_nets(catalog: CatalogSnapshot, snapshot: CircuitSnapshot) -> TopologyResult
serialize_snapshot(snapshot: CircuitSnapshot) -> bytes
restore_snapshot(payload: bytes, catalog: CatalogSnapshot) -> CircuitSnapshot
serialize_topology(result: TopologyResult) -> bytes
```

### 7.1 წინაპირობები, შედეგები, შეცდომები

| ინტერფეისი | შემავალი შემოწმება | წარმატების გარანტია | შეცდომა |
|---|---|---|---|
| `load_catalog` | UTF-8, max bytes, schema version, canonical digest, unique IDs, ცალსახა mapping, evidence references | pinned source-backed immutable catalog | `MALFORMED_JSON`, `SCHEMA_UNSUPPORTED`, `CATALOG_DIGEST_MISMATCH`, `INVALID_CATALOG` |
| `resolve_terminal` | არსებობს ინსტანსი/definition digest/terminal_id | `ResolvedTerminal` შეიცავს physical contact, GPIO mapping-ის **სტატუსს** და evidence IDs-ს; არ აბრუნებს guessed alias-ს | `UNKNOWN_INSTANCE`, `UNKNOWN_TERMINAL`, `AMBIGUOUS_MAPPING`, `CATALOG_MISMATCH` |
| `create_snapshot` | pinned catalog; distinct IDs; valid endpoints; no self-loop; orphan junction group არ წარმოიქმნება | normalized snapshot; input arrays sorted-by-ID; canonical identity preserved | `DUPLICATE_ID`, `INVALID_ENDPOINT`, `UNKNOWN_DEFINITION`, `ORPHAN_JUNCTION_GROUP` |
| `compute_nets` | `snapshot.catalog_digest == catalog.digest`; revalidation for untrusted object | sorted `nets`, mappings, singleton nets, snapshot fingerprint | `CATALOG_MISMATCH`, `INVALID_SNAPSHOT` |
| `serialize_snapshot` | validated snapshot | canonical UTF-8 JSON, no BOM/trailing whitespace, no NaN/Inf, deterministic bytes | `SERIALIZATION_ERROR` |
| `restore_snapshot` | exact v1 schema, bytes limit, nested strict validation, catalog digest matches | `serialize_snapshot(restore_snapshot(bytes)) == canonical_normalized_bytes` | `SCHEMA_UNSUPPORTED`, `INVALID_SNAPSHOT`, `CATALOG_MISMATCH` |
| `serialize_topology` | sorted validated result | audit-usable canonical bytes, not a circuit save format | `SERIALIZATION_ERROR` |

**Failure semantics [R]:** no silent fallback to guessed pin; no partial `TopologyResult` on invalid references; caller receives structured `EngineeringModelError(code, path, context_ids)`. Exception text is developer-only; Georgian translation occurs in UI. Source rights errors block ingestion/distribution, not necessarily purely *local factual reading*.

### 7.2 სტრუქტურული JSON მაგალითი — არასრული illustrative subset

```json
{
  "schema_version": "1.0",
  "catalog_digest": "sha256:<validated-catalog-digest>",
  "instances": [
    {"instance_id": "board1", "definition_id": "esp32-devkitc-32e-v4", "definition_digest": "sha256:<validated-definition-digest>"},
    {"instance_id": "sensor1", "definition_id": "adafruit-3942-profile", "definition_digest": "sha256:<validated-definition-digest>"}
  ],
  "junctions": [{"junction_id": "j1"}],
  "conductors": [
    {"connection_id": "c1", "kind": "ideal_wire", "endpoint_a": {"kind": "terminal", "instance_id": "board1", "terminal_id": "J3.9"}, "endpoint_b": {"kind": "junction", "junction_id": "j1"}},
    {"connection_id": "c2", "kind": "ideal_wire", "endpoint_a": {"kind": "junction", "junction_id": "j1"}, "endpoint_b": {"kind": "terminal", "instance_id": "sensor1", "terminal_id": "Trig"}}
  ]
}
```

`<validated-...>` არის **placeholder და არა რეალური digest**. Data source-ის ან კონკრეტული PCB-ის სრული ვერიფიკაციის გარეშე ამის გამოცხადება მზა საბაზისო catalog-ად დაუშვებელია.

### 7.3 JSON bytes და ვერსიის წესები

- `schema_version` major/minor; ამ კვლევის კანდიდატი მხოლოდ exact `1.0`. სხვა version → `SCHEMA_UNSUPPORTED`; silently drop extra fields **აკრძალულია**.
- Pydantic `model_validate_json`/`model_validate`, `ConfigDict(extra='forbid', strict=True, frozen=True)`. `model_validator(mode='after')` cross-field checks; `model_json_schema()` tooling-ისთვის, მაგრამ JSON Schema **თავად ვერ ადასტურებს** references-ს, true circuit semantics-ს ან evidence provenance-ს [S13–S14].
- serialize: data → `model_dump(mode='json')` → dictionaries key sort `sort_keys=True`, arrays ID-based fixed sort, `ensure_ascii=False`, `separators=(',', ':')`, `allow_nan=False`, UTF-8 encode. v1 არ უშვებს floating-point ფიზიკურ პარამეტრებს canonical domain-ში; რაოდენობა ინახება `decimal` სტრიქონით + explicit SI unit (future rules). Identifier ASCII. **ეს არის INVENTOR-v1 JSON byte profile, არა სრულად RFC 8785 JCS** [S11, S17].
- განსაკუთრებული ხაფანგი: `snapshot_sha256` ითვლება snapshot-ის canonical bytes-დან; **არ** მოათავსოთ hash იმავე preimage-ში. Catalog digest-ის მსგავსად root digest-იც გარე ან გამორიცხული ველია, რათა არ შეიქმნას recursive hash. **ასევე `definition_digest` გამორიცხულია თავად `DeviceDefinition`-ის digest-ის canonical preimage-დან.**
- კოლექციების canonical order: `definitions`: definition_id; `instances`: instance_id; `junctions`: junction_id; `conductors`: connection_id; `claims`: claim_id; source docs: source_document_id; `nets`: lexicographic first terminal; members sorted. Explicit user IDs არ შეიცვლება normalization-ისას.
- Wire-ის `endpoint_a`, `endpoint_b` serialization-ში დაალაგეთ vertex key-ით. ამით ერთი და იგივე `connection_id`-ით *reversed wire* → იდენტურ serialized snapshot-ს. **სხვა ID-ით დუბლირებული wire** იგივე topology-ს იძლევა, მაგრამ snapshot bytes/hash განსხვავდება — audit trail ინახავს ორი connection-ის არსებობას.
- Future v1.x extension მხოლოდ წინასწარ შეთანხმებული schema migration-ით, opt-in, known input/output fixtures-ით; უცნობი ველის ავტომატური შენარჩუნება/უგულებელყოფა არა. v2 breaking ცვლილება ცალკე მიგრაციის ხელმოწერით.

## 8. Manufacturer data and evidence contracts

### 8.1 Espressif board: exact scope და კონტრ-შემთხვევები

**[F] დოკუმენტური იდენტობა:** Espressif `ESP32-DevKitC-32E` ჩასმულია `ESP32-DevKitC V4` სახელმძღვანელოს variant table-ში `ESP32-WROOM-32E` მოდულით, 4 MB flash-ით, PCB antenna-ით [S18]. `ESP32-DevKitC-32UE` **სხვა** orderable variant-ია და არ უნდა აირიოს [S18].

**[F] physical exposed header mapping-ის დასაწყისი [S18]:**

| Contact | Board label | SoC/signal target | წყაროს პირობა |
|---|---|---|---|
| `J3.9` | `IO18` | `GPIO18` | V4 guide J3 row 9 |
| `J3.8` | `IO19` | `GPIO19` | V4 guide J3 row 8 |
| `J2.5` | `IO34` | `GPIO34` — input-only (`I`) | V4 guide J2 row 5 |
| `J2.1` | `3V3` | 3.3 V supply header | V4 guide J2 row 1 |
| `J2.19` | `5V` | 5 V supply header | V4 guide J2 row 19 |
| `J2.14`, `J3.1`, `J3.7` | `GND` | board common ground | guide + V4 schematic independent confirmation [S18–S19] |
| `J2.16`, `J2.17`, `J2.18`, `J3.17`, `J3.18`, `J3.19` | `D2/D3/CMD/D1/D0/CLK` | SPI flash reserved signals | V4 guide says avoid use [S18] |

**[F] power-mode qualifier:** guide ამბობს USB, 5V+GND, 3V3+GND ალტერნატიულ კვებით რეჟიმებს, რომლებიც ერთდროულად არ უნდა გამოიყენონ [S18]. **[R]** ამ წესს topology engine არ აგვარებს: `5V`/`3V3` დანიშნულების metadata უნდა მიეწოდოს მომავალ power-validation layer-ს. Screenshot-ით შემოწმებული V4 reference schematic აჩვენებს USB/რეგულატორისგან შემდგარ შიდა კვებით გზას; რეგულატორი **არ** არის ideal tie `5V↔3V3` [S19].

**[F] revision risk:** V4 user guide აღწერს C15-ის პრობლემას ზოგიერთ ადრინდელ დაფაზე [S18]. Espressif-ის PCN აღწერს `ESP32-DevKitC-32E`-ში chip-revision ცვლილებას [S20]. `ESP32-WROOM-32E` datasheet-ის v2.1 გამოცემის თარიღი 2026-08-05 ჩანს ოფიციალურ ინდექსში [S21]. **[U] რეალურად შემოსული ფიზიკური board-ის PCB/assembly/SoC revision არ ადგინდება მხოლოდ orderable SKU-ით.**

**[R] ჩანაწერის გამოყენების დაშვების ორ დონეს შორის არჩევა:** `V4_DOCUMENTED_PROFILE` — მოდელური საინჟინრო დემოს ფიქსირებული შერჩეული reference; `PHYSICAL_REVISION_CONFIRMED` — საჭიროა აშკარა board marking/საჭიროებისას trace/photo/lot identifier. პირველი არ ამტკიცებს კონკრეტული ხელში არსებული დაფის ფიზიკურ რევიზიას. სხვა DevKit board-ების ავტომატური კოპირება აკრძალულია.

### 8.2 HC-SR04 sold by Adafruit, Product ID 3942

**[F]** Adafruit-ის პროდუქტის გვერდის SKU არის **3942**, დასახელებით *HC-SR04 Ultrasonic Sonar Distance Sensor + 2 × 10K resistors* [S22]. Adafruit-ის ტექსტში: კვება 5V საუკეთესო შედეგისთვის; `Trig` იღებს 3V/5V trigger-ს; `Echo` გამოდის 5V logic-ით; შედის ორი 10kΩ რეზისტორი divider-ისთვის [S22–S23]. Pinout-ის აღწერილია `Vcc`, `Trig`, `Echo`, `Gnd` [S23]. ამგვარად ეს ოთხი physical interface terminal არის მხარდაჭერადი პროტოტიპის დონეზე.

**[U] ზუსტი წარმოების იდენტობა:** Adafruit ამ შემთხვევაში სანდო **გამყიდველი/საგანმანათლებლო წყაროა**, მაგრამ ამ გვერდებზე არ დამტკიცებულა კონკრეტული PCB ასამბლეის OEM მწარმოებელი, ნაწილის MPN, BOM/PCB რევიზია, output-driver მინ/მაქს გარანტირებული დიაპაზონი და ყველა მიწოდებული პარტიის ეკვივალენტობა. Manufacturer-ის ველში `Adafruit` ავტომატურად ჩაწერა მცდარია; უნდა იყოს `manufacturer_name=null`, `manufacturer_status=unverified`, `distributor=Adafruit`, `retail_sku=3942`.

**[R] დაშვება:** catalog definition იდენტიფიცირდება როგორც `adafruit-3942-profile`, თუმცა `evidence_scope=retail_product_page` და `hardware_revision_status=unverified`. მომხმარებლის მიერ არჩევა/დადასტურება შეიძლება დაუშვას **კავშირების topology** და source-qualified წესები, მაგრამ ეს არ იძლევა გამოგონილი datasheet-ის/აბსოლუტური მარაგის უფლებას. უცნობი *generic HC-SR04* ან `US-100`/`RCWL-1601` არ გადადის ამ პროფილზე ავტომატურად.

**ძაბვის დონის სიფრთხილე [R]:** 10kΩ/10kΩ დაყოფა ნომინალური 5V HIGH-იდან იძლევა 2.5V-ს მხოლოდ იდეალიზებული წესით (`Vout=Vin·Rbottom/(Rtop+Rbottom)`). **არ ნიშნავს უნივერსალურ guaranteed logic-high margin-ს ESP32-ის ყველა მოქმედ VDD-ზე**; კონკრეტული ESP32 VIH ზღვარი, R tolerance, Echo drive და waveform მონაცემები ცალკე ინტერვალურ კვლევას საჭიროებს. Topology contract-ის არეალი **არ** შეიცავს ამ ძაბვის ალგორითმს. იგი მხოლოდ ქსელს უწვდის future verifier-ს.

### 8.3 Evidence ingestion: მიკვლევადი workflow — არა automatic scraping

1. **Source register:** `source_document_id`, URL, publisher, document title, edition/revision, publication_date? (unknown allowed), accessed_at_utc, media_type, download_sha256? (only if source bytes actually retrieved), `rights_state ∈ {verified_reusable,link_only,permission_required,unverified}`.
2. **Fact register:** `claim_id`, `source_class ∈ {manufacturer,retailer,user_assumption,derived,measurement}`, `subject_identity`, `exact_assembly_scope`, `property`, `value`, `unit?`, `condition?`, `min_typ_max?`, `locator` (page/table/row/paragraph), `source_document_id?`, `reviewer`, `review_status`. Contradicting facts *არ* გადაიწეროს; დაემატოს conflict ID.
3. **Exact pin map:** თითო exposed terminal-ზე board connector + პოზიცია + label + GPIO/module signal **ცალ-ცალკე**. ყოველ mapping-ს ერთი ან მეტი claim ID. Only complete and admitted mappings მიიღოს `verified` სტატუსი.
4. **Source reconciliation:** board guide + schematic + module datasheet ერთმანეთს შეუდარდეს; გაურკვეველი `V4` vs physical assembly, USB power path, GND ties გამოყოს. სენსორის retailer განცხადებები არ გაუთანაბრდეს OEM absolute maximum datasheet-ს.
5. **Review & lock:** human-approved `DeviceDefinition`-ის canonical byte SHA-256, approved source registry hash, evidence scope, reviewed date, review signature/actor. Snapshot მხოლოდ ამ digest-ზე მიუთითებს.
6. **Change handling:** წყაროს ახალი ვერსია არის ახალი `definition_digest`; ძველი project/snapshot არ „განახლდება“ ჩუმად; ცვლილება მოითხოვს migration/compare report-ს და შესაბამისი golden tests-ის rerun-ს.
7. **Rights gate:** PDF/schematic source-ის ტექსტის/გამოსახულების გადაკოპირება არ მოხდეს მხოლოდ იმიტომ, რომ URL საჯაროა. factual pin mapping-ის საკუთარი მოკლე ჩანაწერები და source URLs გაიმიჯნოს მესამე მხარის artwork/files-ის redistribution-ისგან.

## 9. Verification and independent test matrix

`T`-ტერმინალი, `J`-junction. ტესტის oracle არის ხელით დადგენილი reachable paths ან წყაროთი დადასტურებული identity; პროგრამის დაბრუნებულიდან არ უნდა შეიქმნას expected. რიცხვიანი `net_id` ჰეშის exact hex ამ ეტაპზე არ არის საჭირო correctness oracle-ისთვის; შედარდეს წევრთა სიმრავლე და, ცალკე, hash algorithm-ის ცნობილ დამოუკიდებელ digest test vector-ს.

| ID | Input fixture / მოქმედება | დამოუკიდებლად დასაბუთებული მოსალოდნელი შედეგი |
|---|---|---|
| T01 — multi-terminal | `A—J1`, `B—J1`, `C—J1` | ერთი კლასი `{A,B,C}`; ყველა წყვილისთვის არსებობს გზა J1-ით |
| T02 — order | T01-ის connections/instances საპირისპირო სიით | იგივე terminal membership და serialized normalized bytes; undirected graph არ დამოკიდებულია insertion order-ზე |
| T03 — duplicate/reverse | `A—B` connection `w1`, `B—A` სხვა `w2` | ერთი ნეტი `{A,B}`; ორი დამოუკიდებელი conductor ID; `w1`-ის წაშლის შემდეგ w2-ის არსებობისას ნეტი არ იყოფა |
| T04 — disconnected | A,B,C, მხოლოდ A—B | `{A,B}` და `{C}`; C singleton; „არაჩანს“ არ უდრის „არარსებობს“ |
| T05 — split on removal | A—B (`w1`), B—C (`w2`); წაიშალა `w2` | `{A,B}`, `{C}`; `A→C` გზა აღარ არსებობს |
| T06 — crossing | A—B და C—D geometry-ს წერტილში კვეთს, `J` არ არსებობს | ორი ცალკე ნეტი `{A,B}`, `{C,D}`; გრაფის edge მხოლოდ explicit endpoints-ზეა |
| T07 — explicit junction | A—J, B—J, C—J, D—J (იგივე ნახაზი) | ერთი `{A,B,C,D}`; junction კავშირის აშკარა კვანძია |
| T08 — unknown device | `definition_id=generic-clone-hcsr04` დაურეგისტრირებელია | `UNKNOWN_DEFINITION`, არანაირი fallback/admitted topology |
| T09 — ambiguous identity | `ESP32-DevKitC` family without specified `-32E` / verified profile | `UNSUPPORTED_DEVICE` ან `AMBIGUOUS_MAPPING`, არა forced default |
| T10 — view independence | იგივე snapshot, but `anchor.x/y`, zoom, wire bend ან Georgian label შეიცვალა | იგივე normalized snapshot bytes/hash, same topology; view data არასოდეს შედის preimage-ში |
| T11 — round-trip | valid canonical snapshot → encode → restore → encode | byte-for-byte identical; schema version retained; IDs unchanged |
| T12 — bad terminal | `board1/J3.99` როცა definition-ს არ აქვს `J3.99` | `UNKNOWN_TERMINAL`, no partial nets |
| T13 — missing instance | endpoint references `board99` | `UNKNOWN_INSTANCE`, no guess from label |
| T14 — self loop | `A—A` | `SELF_LOOP` reject; silent merge არ არის საჭირო |
| T15 — duplicated IDs | ორი `Conductor(connection_id='w1')` სხვადასხვა endpoints-ით | `DUPLICATE_ID` reject; no ambiguous deletion semantics |
| T16 — internal board tie | `board1/J2.14`, `board1/J3.1` sourced GND tie | ერთ ნეტში **მავთულის გარეშე**; maker schematic tie არის ერთადერთი oracle; user-added sensor GND სხვა ნეტში რჩება ვიდრე მავთული არაა |
| T17 — power separation | `board1/J2.19 (5V)` და `board1/J2.1 (3V3)` | განსხვავებული nets (თუ მომხმარებელმა არ დააერთა პირდაპირ); regulator not ideal conductor |
| T18 — source rights | unknown source PDF rights, ტექსტი/სურათი export bundle-ში | source binary redistribution blocked; link-only provenance allowed |
| T19 — schema extra | valid JSON + arbitrary `vendor_compat=true` unknown field | `INVALID_SNAPSHOT` (`extra_forbidden`), no silent ignore |
| T20 — catalog immutability | იგივე `definition_id`, შეცვლილი verified pin mapping, ძველი digest | `CATALOG_DIGEST_MISMATCH`, not auto-updated project |

### Property-based / metamorphic ტესტები [R]

- **[P1] Permutation invariance:** ყველა გრაფზე `permutation(wires)` და `permutation(instances)` → უცვლელი `terminal_to_net`, normalized bytes.
- **[P2] Edge reversal invariance:** `A—B` ჩანაცვლდეს `B—A` იგივე `connection_id`-ით → bytes და nets უცვლელი.
- **[P3] Redundant parallel edge:** მეორე `connection_id`-ით იგივე unordered endpoints დამატებული → nets უცვლელი; snapshot hash შეიძლება იცვლებოდეს.
- **[P4] Monotonic add-only:** valid edge დამატება **ვერ** გაზრდის connected-component რაოდენობას; შეუძლია უცვლელად დატოვოს ან ერთით შეამციროს, თუ ადრე სხვადასხვა კომპონენტს აკავშირებს.
- **[P5] Delete split bound:** ერთ edge-ის წაშლა კომპონენტების რაოდენობას ან უცვლელს ტოვებს, ან ზუსტად ერთით ზრდის; redundant edge-ს არ უნდა გაჰყვეს split.
- **[P6] Partition invariant:** ყველა ფიზიკური ტერმინალი ზუსტად ერთ ნეტშია, `∪ members == all terminals`, ნებისმიერი ორი net-ის კვეთა ცარიელია.
- **[P7] Independent oracle:** random მცირე graph-ის reachability თითო terminal pair-ზე შედარდეს თავიდან ხელით განსაზღვრულ BFS/DFS-oracle-ს ან **NetworkX `nx.connected_components`-ს**. NetworkX სარგებლობს cross-implementation disagreement-ის საპოვნელად, მაგრამ T01–T20-ის expected-ებს არ ცვლის.
- **[P8] No-view sensitivity:** ნებისმიერი transformations on `ViewDocument` with fixed `CircuitSnapshot` → exact same canonical bytes.
- **[P9] Error generation:** random valid snapshot-ში terminal/instance ID შეცდომით ჩაანაცვლეთ; ყოველთვის typed rejection, არასოდეს partial success.
- **[P10] Deterministic hashing:** ერთსა და იმავე canonical profile bytes-ზე SHA-256 ცნობილ დამოუკიდებელ ვექტორთან cross-check; არ გამოიყენოთ ორი ერთსა და იმავე ფუნქციაზე დაყრდნობილი oracle.

**[R] test-only** Hypothesis `given`, `strategies` ქმნის მცირე disconnected/connected graphs-ს (size cap წინასწარ). თითო generator-მა უნდა შეინარჩუნოს valid IDs და explicit tie constraints; invalid-fixture generator ცალკე. Test seed/ნაკლები counterexample ჩაიწეროს, რათა შესაძლებელი იყოს გამეორება. **არ არის გატარებული არც ერთი ტესტი** ამ ანგარიშის ფარგლებში.

## 10. Open-source licensing assessment

| Project/version/URL | SPDX | Intended APIs / საჭიროა? | Commercial reuse & redistribution boundary | რისკი/ალტერნატივა |
|---|---|---|---|---|
| **CPython 3.12 stdlib** — https://www.python.org/ ; https://docs.python.org/3.12/license.html | `Python-2.0` (PSF License v2, Python distribution includes historical notices) | `collections.deque`, `json`, `hashlib`, `typing`; **აუცილებელი runtime** | permissive, preserve required notices when distributing runtime; track bundled third-party portions | Python version and OS packaging; no separate BFS library |
| **Pydantic 2.14.4** — https://github.com/pydantic/pydantic ; https://pypi.org/project/pydantic/2.14.4/ | `MIT` | `BaseModel`, `ConfigDict`, `Field`, `model_validate_json`, `model_validator`, `model_dump`, `model_json_schema`; **recommended runtime** | commercial/closed-source permitted with license/copyright notices; transitive `pydantic-core` also MIT [S12–S13] | Rust binary/abi, upgrade drift; alternative stdlib dataclasses + manual validators |
| **NetworkX 3.7** — https://github.com/networkx/networkx ; https://pypi.org/project/networkx/3.7/ | `BSD-3-Clause` | `nx.Graph`, `nx.connected_components`; **test-only** | commercial use allowed with notices/non-endorsement; not runtime necessity; requires Python `>=3.12`, `!=3.14.1` [S08] | additional test dependency, test independence useful; alternative hand DFS oracle |
| **Hypothesis 6.170.17** — https://github.com/HypothesisWorks/hypothesis ; https://pypi.org/project/hypothesis/6.170.17/ | `MPL-2.0` | `given`, `strategies`; **test-only** | file-level copyleft obligations if distributing modified Hypothesis source files; mere use in tests not blanket copyleft on project | not runtime; transitive deps verify on lock; optional deterministic exhaustive small-graph enumeration |
| **KiCad 10.x** — https://www.kicad.org/about/licenses/ | **`GPL-3.0-or-later` for majority of code**, component license audit needed | `kicad-cli sch export netlist` documented; **not integrated** | study APIs/semantics; copying/linking KiCad core into proprietary application triggers GPL analysis; subprocess distribution questions require legal review | source copying rejected; optional future standalone file exchange with legal review |
| **LibrePCB 2.1.1** — https://librepcb.org/license/ | **`GPL-3.0-only` vs `GPL-3.0-or-later`: exact SPDX UNVERIFIED; ოფიციალური project გვერდი აცხადებს GPLv3-ს, კონკრეტული source-file header შემოწმებას საჭიროებს** | device/pad/signal semantic precedent, **not integrated** | GPL source not copied. Official LibrePCB libraries are `CC0-1.0` **but inspect each third-party library/file** [S05] | C++/Qt integration/relicensing overhead |
| **KiCad official libraries** — https://www.kicad.org/libraries/license/ | `CC-BY-SA-4.0` **with KiCad's specific library exception** | **not copied/admitted** | designs generated with libraries do not automatically inherit share-alike; bulk copying original library data requires separate license/attribution analysis | distinguish application code vs library data [S24] |
| **LibrePCB official libraries** — https://librepcb.org/license/ | `CC0-1.0` (official libraries) | **not required** | generous reuse subject to provenance and individual library rights checks | CC0 library facts insufficient for specific board revision |

**[F] legal difference:** „ალგორითმის გამოყენება“ ≠ „GPL კოდის გადმოწერა“. გრაფის connected-components თეორიისა და BFS იდეის დამოუკიდებლად აღწერა/დაწერა არ არის KiCad/LibrePCB source-code-ის დაკოპირება; source snippets, generator scripts და ოფიციალური artwork ცალკე ლიცენზიებს ექვემდებარება. **[R]** internal license register მოიცავდეს package hash, license, transitive dependencies, distribution mechanism, third-party notices, source attribution. ეს არ არის იურიდიული დასკვნა; GPL/CC media redistribution-ზე იურიდიული გადამოწმება ცალკე რჩება.

**მწარმოებლის დოკუმენტები ≠ OSS code:** Espressif disclaimer ამბობს, რომ დოკუმენტის გაზიარება საკუთრების ზოგადი ლიცენზია არ არის [S25]. Adafruit guide-ის ვიდეო/ფოტო/სქემის, PDF-ისა და ტექსტის შესაძლო Creative Commons პირობები **ამ კონკრეტული არტეფაქტებისთვის ერთიანად არ დადასტურებულა [U]**. თქვენი დამოუკიდებელი factual record, მოკლე ავტორირებული ახსნა და გადამოწმებული წყაროს URL მოერიდოს original art-ის redistribution-ს ნებართვის გარეშე.

## 11. Main technical risks and demonstrated remedies

| რისკი | ილუსტრირებული failure | გადაწყვეტის კონტრაქტი | სტატუსი |
|---|---|---|---|
| Pin identity collapse | board `J3.9` აღიქმება თვითონ `GPIO18`-ად; ჰედერ/SoC map იკარგება | separate physical terminal and `SignalMapping`; exact maker row | remedy design proposed, **not tested** |
| Bogus automatic power short | 5V header და 3V3 `power` label იმავე net-ში | never join rails except source-backed ideal ties; regulator as component relation | source-backed [S18–S19], code untested |
| GPIO on wrong board variant | `-32E` ↔ `-32UE`, V4 ↔ clone | exact definition/digest + variant rejection | source-backed [S18], code untested |
| Unknown sensor revision | distributor SKU აღიქმება OEM specification-ად | retail-source qualifiers; `manufacturer_status=unverified`; `UNKNOWN` on gaps | source limit demonstrated [S22–S23] |
| Crossing auto-connect | screen coordinate intersection creates edge | only explicit endpoint/junction; UI geometry excluded | semantics supported [S01], code untested |
| Deletion stale DSU | edge removal keeps historical union | no persistent DSU; full rebuild | mathematical remedy [S15] |
| Duplicate wires lost in editing | Graph collapses edges and overwrites editor state | immutable `Conductor` list by `connection_id`, topology adjacency set only | proposed remedy |
| False stable net IDs | counter `net1` changes after list permutation | membership-hash net ID; finding primary refs based on terminals | proposed remedy |
| Superficial deterministic JSON | `model_dump_json()` field order/or float differences alter bytes | fixed canonical profile, no float, normalized lists, explicit hash preimage | RFC/stdlib-supported principle [S11, S17] |
| Licenses misread | proprietary runtime copies GPL EDA source | use semantic design, not source; audit each dependency/artifact | verified license pages [S05,S24,S25] |
| Malicious/large input | huge graphs/JSON recursion or invalid refs | max bytes/counts, bounded string IDs, strict parser; reject early; no automatic remote fetch | proposed security control |
| Datasheet drift | `latest` URLs silently update evidence | immutable profile source revision/URL/hash, revision-history reporting | proposed provenance control |

**მნიშვნელოვანი სტატუსი:** ზემოთ remediation-ები არის **დასაბუთებული დიზაინი**, არა შესრულებული ინსტრუმენტებით დადასტურებული ფუნქციონირება. ამ კვლევაში არ გაშვებულა benchmark, Pydantic fixture, integration harness ან რეალური ელექტრული გაზომვა.

## 12. Rejected alternatives

1. **Full KiCad schematic/PCB as canonical truth** — app-ის სპეციფიკური UI/geometry/ფაილები ზედმეტად გადაწვდება მიზნობრივ ორნეტიან workflow-ს; voltage-compatibility მაინც საჭიროებს custom facts. მომავალში file import adapter შეიძლება ცალკე გადაწყდეს.
2. **LibrePCB device/library-დან სრული runtime** — სემანტიკა გამოსადეგია, მაგრამ ძირითადი app და GPL/Qt კომპლექსი პირველ კომპონენტურ დემოს არ სჭირდება.
3. **SPICE/ngspice/Xyce როგორც connectivity ნეტების პირველი გამოთვლა** — ელექტრულად კონკრეტული კომპონენტების მოდელები/პარამეტრები და არასწორი „simulation“ შთაბეჭდილება; ნეტები თვითონ graph connectivity-ია.
4. **NetworkX როგორც აუცილებელი production dependency** — მხოლოდ connected components საჭიროებისთვის სტანდარტული BFS მარტივია; library დატოვებულია დამოუკიდებელი graph oracle-ად. **გადაწყვეტილება შეიძლება შეიცვალოს**, თუ ახალი verified features ითხოვს cycles/cutsets/paths/algorithm portfolio-ს და measured maintenance cost შემცირდება.
5. **Persistent/incremental union-find / dynamic connectivity** — წაშლა არ არის მხარდაჭერილი ჩვეულებრივი DSU-ით; მცირე გრაფზე სირთულის გასამართლებელი benchmark არ არსებობს.
6. **`dataclasses`-ის სრული ხელით JSON validator** — ნაკლები dependency, მაგრამ მეტი code surface არატიპიზებული input-ებისთვის; ალტერნატივად დატოვებულია მხოლოდ Pydantic-ის დისტრიბუციის რეალური blocker-ისას.
7. **RDF/OWL/IP-XACT/SysML/Modelica universal ontology** — ნაკადის პირველ ეტაპზე არ მოაქვს პროპორციული დადასტურებული სარგებელი; დამტკიცებული thin canonical model შენარჩუნებულია.
8. **Auto-discovery/pin guessing via LLM, photos, clone names or internet search** — reproducibility და safety false-positive პრობლემები; მხოლოდ review-gated მონაცემები.
9. **Stable net ordinal `N1`, `N2`** — sorting-ის/edge deletion-ისას ცვლის referent-ს; editable conductor ID და derived member-hash უნდა გაიმიჯნოს.

## 13. Explicit unresolved decisions — architecture-owner only

| ID | კითხვა | აუცილებელი მტკიცებულება / gate | მანამდე მუშაობის წესი |
|---|---|---|---|
| U01 | `ESP32-DevKitC-32E` physical PCB/assembly/chip revision როგორ დადასტურდეს? | exact marking, Espressif V4 schematic match, PCN applicability, optional sample examination | only documented V4 reference profile, no physical-verified claim |
| U02 | Adafruit PID 3942-ის OEM მწარმოებელი/PCB revision ცნობილია? | OEM datasheet/BOM or verified supplier batch trace | retail-sku-qualified model only; no cloned sensor mapping |
| U03 | რამდენი `internal_ideal_ties` უნდა შევიდეს v1 board catalog-ში? | independently reviewed V4 schematic net list; list of GND/source/5V/3V3 paths | include only individually verified ideal ties, do not presume every label |
| U04 | როგორ მიენიჭოს user-inserted instance/conductor durable IDs? | product-level persistence & collaboration constraints | backend contract accepts stable supplied IDs; never derive IDs from order |
| U05 | Pydantic binary/runtime ყველა target-ში თავსებადია? | pinned Python 3.12 Windows/Linux/container install + rebuild reproducibility | no unsupported-deployment claim |
| U06 | Source documents/facts შეიძლება კომერციულ bundle-ში დაკოპირდეს? | artifact-specific licensing/license grant or legal analysis | link-only evidence, original own factual records |
| U07 | რა არის ადაპტერის publicly stable schema versioning policy? | migration test fixtures + owner approval | exact `1.0` only; reject unknown |
| U08 | project-native UUID vs human-readable ID selection? | UI/collaboration uniqueness requirements | strict opaque IDs allowed, no semantic implicit meaning |
| U09 | რა არის მაქს. graph/snapshot ზომა? | supported demo design + actual measured p95 | preliminary hard cap proposal: ≤128 instances, ≤8192 physical terminals, ≤16384 conductor records, ≤8192 junctions, ≤4 MiB JSON; subject to measurement |
| U10 | რამდენად ცალსახაა Echo output electrical guarantees beyond product blurb? | OEM-scope datasheet, guaranteed range/conditions or measurement | topology only; no unconditional voltage safety verdict |

**არც ერთი U-პუნქტი არ უნდა შეივსოს „სავარაუდოდ ასეა“ პრინციპით.** თუ წყაროს მტკიცება აკლია, ვერსირებული ფაილი ინახავს `unknown`-ს და მტკიცებულების მისამართს/გამოსაკვლევ ეტაპს.

## 14. Primary sources, versions, verification dates

ყველა ქვემოთ აღნიშნული წყარო შემოწმდა ონლაინ **2026-11-20**-ს (საქართველო). Version-იანი upstream release და ცოცხალი `latest` გვერდი **სხვადასხვა** რამეა; `latest`-ის რეგისტრაცია თვითონ არ წარმოადგენს frozen data artifact-ს. მესამე მხარის დოკუმენტის ადგილობრივი სრული bytes/content-hash არ ყოფილა არქივირებული ამ კვლევაში, თუ ზუსტად სხვა რამ არ არის მითითებული.

| ID | წყარო / ვერსია | URL | გამოყენებული მტკიცება |
|---|---|---|---|
| S01 | KiCad Schematic Editor 9 user guide, junction/no-connect | https://docs.kicad.org/9.0/en/eeschema/eeschema.html | explicit junction, crossing, electrical net semantics |
| S02 | KiCad developer schematic S-expression format | https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/ | `junction`, `wire`, `no_connect`, `uuid` |
| S03 | KiCad CLI 10.0 | https://docs.kicad.org/10.0/en/cli/cli.html | `kicad-cli sch export netlist`, formats |
| S04 | LibrePCB 2.1.1 docs, Component | https://librepcb.org/docs/quickstart/create-library-elements/component/ | symbol pin ↔ logical component signal |
| S05 | LibrePCB licensing / latest stable 2.1.1 | https://librepcb.org/license/ ; https://librepcb.org/download/ | GPL code; CC0 official libraries, version |
| S06 | LibrePCB docs, Device / UUID references | https://docs.librepcb.org/_branches/master/librepcb/quickstart/create-library-elements/device/ ; https://docs.librepcb.org/_branches/master/librepcb/user-manual/references/ | device pad mapping and stable IDs |
| S07 | NetworkX 3.7 connected components docs | https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.connected_components.html | BFS, `O(V+E)` |
| S08 | NetworkX 3.7 PyPI (2026-09-21), Graph APIs | https://pypi.org/project/networkx/3.7/ ; https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.add_edges_from.html | BSD-3-Clause, Python ≥3.12 excl. 3.14.1; duplicates |
| S09 | Python 3.12 deque docs | https://docs.python.org/3.12/library/collections.html | queue operations and costs |
| S10 | Python 3.12 dataclasses and license | https://docs.python.org/3.12/library/dataclasses.html ; https://docs.python.org/3.12/license.html | alternative typed records; PSF license |
| S11 | Python 3.12 JSON docs | https://docs.python.org/3.12/library/json.html | sorted keys, separators, allow_nan |
| S12 | Pydantic 2.14.4 PyPI (2026-11-19) | https://pypi.org/project/pydantic/2.14.4/ | latest verified version/date, MIT |
| S13 | Pydantic `ConfigDict` official docs | https://pydantic.dev/docs/validation/latest/api/pydantic/config/ | `strict`, `extra='forbid'`, faux-immutable `frozen` |
| S14 | Pydantic `BaseModel` API | https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/ | validation, dump, schema |
| S15 | Robert E. Tarjan, JACM 22(2), 1975 | https://doi.org/10.1145/321879.321884 | disjoint-set union theory; deletion limitation from data structure invariant |
| S16 | Hypothesis 6.170.17 PyPI (2026-11-20) | https://pypi.org/project/hypothesis/6.170.17/ | MPL-2.0, test-only availability |
| S17 | RFC 8785 JCS (2020, informational) | https://www.rfc-editor.org/info/rfc8785/ | cross-system deterministic JSON canonicalization distinction |
| S18 | Espressif ESP32-DevKitC V4 guide (live as of 2026-11-20) | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html | orderable -32E, module, J2/J3 header, warning, C15 |
| S19 | Espressif V4 reference schematic (PDF, 1 page; page screenshot reviewed) | https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_sch.pdf | physical nets, power circuit, connector relations |
| S20 | Espressif PCN 20220901, chip revision change | https://documentation.espressif.com/PCN20220901%20Upgrade%20Chip%20Revision%20of%20ESP32%20Series%20Products.pdf | source-index corroboration of revision risk; actual unit applicability **UNVERIFIED** |
| S21 | Espressif ESP32-WROOM-32E/32UE datasheet v2.1 (2026-08-05) | https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf | module physical identity, electrical specs; selected PDF schematic/timing screenshot consulted, not entire numeric model verified |
| S22 | Adafruit Product ID 3942 product page | https://www.adafruit.com/product/3942 | retail SKU, 5V Echo and divider description |
| S23 | Adafruit Ultrasonic Sonar guide, pinouts | https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/pinouts | physical sensor interface names and signal directions |
| S24 | KiCad source and library licenses | https://www.kicad.org/about/licenses/ ; https://www.kicad.org/libraries/license/ | GPL code vs CC-BY-SA+exception library |
| S25 | Espressif documentation copyright/disclaimer | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/disclaimer-and-copyright.html | no automatic grant to reproduce documentation |

**მოხმარებული წინამორბედი კონტექსტი:** `RESEARCH_01_ENGINEERING_DATA_MODEL.md`, `RESEARCH_02_COMPUTATIONAL_ARCHITECTURE.md`, `RESEARCH_03_FIRST_CAPABILITY_AND_DEMO.md` (ინვენტორის ადრე შექმნილი კვლევითი ანგარიშები; გამოყენებული იყო მხოლოდ შემოწმებული გადაწყვეტილებებთან თანხვედრისა და demo scope-ისთვის). მათი არქიტექტურული/რიცხვითი შეფასებები არ განიხილება მწარმოებლის პირველადი მტკიცებულების შემცვლელად. არც ერთი დაფარული ექსპერიმენტის შედეგი არ გადმოტანილა შესრულებულ ფაქტად.

## 15. Proposed frozen implementation contract — architecture-owner approval required

> **DRAFT / NOT APPROVED.** ეს ცხრილი არის შემოთავაზებული საბოლოო „გაყინვის“ საზღვარი. იგი არ აძლევს coding agent-ს მუშაობის ავტორიზაციას და არ არის მისთვის დავალება.

| Contract ID | შესათანხმებელი მკაცრი წესი | მიღების საზომი |
|---|---|---|
| F-A01 | მხოლოდ two-source documented profiles: V4/-32E board and Adafruit PID3942 retail-scope sensor | unknown/clone/ambiguous variant fails closed |
| F-A02 | exact `DeviceDefinition` + `definition_digest`, pinned `CatalogSnapshot` | identity/pin map change invalidates old digest |
| F-A03 | physical contact `J3.9` ≠ target GPIO18; sensor contact `Trig` ≠ visual anchor | explicit and auditable mapping |
| F-A04 | only ideal conductors and admitted internal ties create graph edges | 5V/3V3 regulator not merged; no implicit voltage labels |
| F-A05 | explicit junction is node; crossing without junction is not | fixtures T06/T07 differ exactly |
| F-A06 | full graph reconstruction on each snapshot modification; deterministic BFS | T01–T07 and P1–P7 expectations |
| F-A07 | wires have stable `connection_id`; graph edge dedup does not erase user records | remove one duplicate retains second |
| F-A08 | singleton nets included; member-set-derived hash and sorted results | T04/T05, P6 and stable net ordering |
| F-A09 | source status/evidence and `unknown` never silently upgraded | T08/T09/T20 reject/mark uncertainty |
| F-A10 | immutable-style Pydantic v2 models; `extra='forbid'`, strict validation, nested tuples | T11/T19, bad references fail early |
| F-A11 | JSON v1.0 canonical byte profile; no float, defined ID sorting, SHA-256 preimage | round trip byte equality, known checksum vector |
| F-A12 | `ViewDocument` physically separate from snapshot; no geometry in topology | T10/P8 exact invariance |
| F-A13 | runtime only Python 3.12 + Pydantic 2.14.4; NetworkX/Hypothesis test-only | lock file records exact versions + notices; target compatibility actually verified |
| F-A14 | structured domain errors, no partial successful topology on invalid input | T12–T15/T19 |
| F-A15 | no claim of electrical safety or physical simulation from connectivity alone | `TopologyResult` contains no `PASS_SAFE` or simulated outputs |

### Architecture-owner approval gate [R]

შესაძლებელია **`APPROVE`**, მხოლოდ თუ: (a) მომზადებულია და ხელით რევიზირებულია პირველადი მწარმოებლის connector/sensor pin mapping; (b) კონკრეტულად გათვალისწინებულია უცნობი physical board/HC-SR04 revision-ის გაშვების პოლიტიკა; (c) source licensing bundle policy განსაზღვრულია; (d) JSON/profile-version, reference IDs და graph rules მიიღეს მკაფიო თანხმობა; (e) independent test matrix და საზღვრები გადამოწმებისათვის მიღებულია. სხვა შემთხვევაში **`APPROVE WITH RESTRICTIONS`** უნდა შემოიფარგლოს მხოლოდ source-qualified virtual board/sensor topology-ით, ან **`DEFER`** დარჩეს მანამ, სანამ U01–U03/U06 კრიტიკული მტკიცებულება არ დაკომპლექტდება.

**დასკვნითი სტატუსი:** წარმოდგენილია ტექნიკურად შეზღუდული, წყაროზე დაფუძნებული, ტესტირებადი **საინჟინრო ტოპოლოგიის კანდიდატი**. ის ჯერ არ ყოფილა იმპლემენტირებული, ბენჩმარკირებული, ლიცენზიურად სრულად აუდირებული დისტრიბუციისათვის ან ფიზიკურ მოწყობილობებზე ვალიდირებული. სწორედ ამ საზღვრებით არის შესაძლებელი მინიმალური coding-agent discretion არქიტექტურის მფლობელის **შემდგომი** გადაწყვეტილების შემდეგ.
