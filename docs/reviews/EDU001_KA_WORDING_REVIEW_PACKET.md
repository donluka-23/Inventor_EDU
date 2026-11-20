# EDU-001 Georgian wording review packet

**PENDING_HUMAN_REVIEW · TEST_ONLY_NOT_PRODUCTION**

This packet reproduces the inherited `ka-GE/edu-001-v1` drafts. Braced placeholders describe substitutions from the actual EDU context. Each row has a blank reviewer decision field for **APPROVE / CORRECT / REJECT**. No reviewer or owner has signed off in this packet.

## `output_not_capable`

**Allowed binding** — `PHYSICAL_CAPABILITY / FAIL / OUTPUT_NOT_CAPABLE` with qualified mapping and GPIO source rows. Example `sensor/Trig → board/J2.5`, `GPIO34`, claim IDs `board-J2.5`, `map-J2.5`, `silicon-GPIO34`.

```text
სქემაში {source} უკავშირდება {contact} კონტაქტს ({target_gpio}). {source_terminal_id} სიგნალის გასაგზავნად დაფას სჭირდება გამოსასვლელი (GPIO_OUT). {basis} {target_gpio} ამ ფუნქციას ვერ ასრულებს.
```

`basis` is exactly `დოკუმენტირებული ვარიანტის მიხედვით` for the reviewed example or `ამ საცდელი ჩანაწერის მიხედვით` for synthetic test evidence.

**Uncertainty** — Direction failure only. Board, firmware and electrical uncertainties stay separate.

Decision ____________________ Reviewer ____________________ Date ____________________

Notes _______________________________________________________________________________

## `direction_pass`

**Allowed binding** — `PHYSICAL_CAPABILITY / PASS / CAPABILITY_CONFIRMED` with qualified mapping and GPIO source rows. Example `sensor/Trig → board/J3.9`, `GPIO18`, `board-J3.9`, `map-J3.9`, `silicon-GPIO18`.

```text
სქემაში {source} უკავშირდება {contact} კონტაქტს ({target_gpio}). ACTIVE რეჟიმში {direction} ფუნქციის შემოწმება (PHYSICAL_CAPABILITY) გავლილია.
```

`direction` is exactly `გამოსასვლელის` for Trig or `შესასვლელის` for Echo. This preview holds Echo fixed.

**Uncertainty** — The stated direction check passed. Other checks keep their raw statuses.

Decision ____________________ Reviewer ____________________ Date ____________________

Notes _______________________________________________________________________________

## `reserved_resource`

**Allowed binding** — `BOARD_AVAILABILITY / FAIL / RESERVED_RESOURCE` with qualified mapping and resource evidence. Example `board/J3.19`, `GPIO6` and the live reservation finding for the documented board.

```text
{contact} ({target_gpio}) კონტაქტი დაფის რესურსისთვის არის დაკავებული. მიმართულების მხარდაჭერა ამ შეზღუდვას არ ხსნის. ამ დაფისთვის განიხილე სხვა კონტაქტი და ხელახლა გაუშვი შემოწმება.
```

**Uncertainty** — The recorded board resource is the scope. The underlying direction result remains distinct.

Decision ____________________ Reviewer ____________________ Date ____________________

Notes _______________________________________________________________________________

## `boot_conditions_unknown`

**Allowed binding** — `BOOT_STRAP_CONTEXT / UNKNOWN / BOOT_STRAP_CONDITIONS_UNKNOWN` through a separate B call on the current snapshot. Example `board/J3.14`, `GPIO0`, `strap-gpio0`, RESET.

```text
{contact} ({target_gpio}) კონტაქტისთვის ჩატვირთვის პირობები უცნობია (UNKNOWN). GPIO-ის მიმართულების მხარდაჭერა ჩატვირთვის ქცევას ვერ ადგენს. გადაამოწმე მტკიცებულების ჩანაწერში ჩამოთვლილი საწყისი პირობები.
```

**Uncertainty** — The example retains `external_pull`, `reset_level` and `sampling_timing` as prerequisites.

Decision ____________________ Reviewer ____________________ Date ____________________

Notes _______________________________________________________________________________

## `board_unknown`

**Allowed binding** — `BOARD_AVAILABILITY / UNKNOWN / EVIDENCE_MISSING`. Example `board/J3.9`.

```text
{contact} კონტაქტის ხელმისაწვდომობა დაფაზე დაუდგენელია (BOARD_AVAILABILITY=UNKNOWN). გადაამოწმე ამ დაფის რესურსების დოკუმენტაცია.
```

**Uncertainty** — Board availability is unknown.

Decision ____________________ Reviewer ____________________ Date ____________________

Notes _______________________________________________________________________________

## `active_unknown`

**Allowed binding** — `ACTIVE_CONFIGURATION / UNKNOWN / ACTIVE_CONFIG_UNKNOWN`. Example the ACTIVE finding for `board/J3.9`.

```text
პროგრამული კონფიგურაცია დაუდასტურებელია (ACTIVE_CONFIGURATION=UNKNOWN). ამის დასადგენად საჭიროა შემოწმებული დაკვირვება პროგრამის გაშვებაზე.
```

**Uncertainty** — Validated firmware observation is missing.

Decision ____________________ Reviewer ____________________ Date ____________________

Notes _______________________________________________________________________________

## `electrical_not_evaluated`

**Allowed binding** — actual coverage `ELECTRICAL_COMPATIBILITY / NOT_EVALUATED / ELECTRICAL_CHECK_DELEGATED`. Example `drive` coverage for the selected candidate.

```text
ელექტრული თავსებადობა არ შემოწმებულა (ELECTRICAL_COMPATIBILITY=NOT_EVALUATED).
```

**Uncertainty** — Electrical evaluation has not occurred.

Decision ____________________ Reviewer ____________________ Date ____________________

Notes _______________________________________________________________________________

## `evidence_request`

**Allowed binding** — an actual replayed record whose rule/status/reason is unsupported for richer wording, or lacks the qualified source bindings that wording requires. Example `PHYSICAL_CAPABILITY / UNKNOWN / UNTRUSTED_FACTSET` in the existing missing-pin control.

```text
{contact} კონტაქტზე ამ შემოწმების შედეგის ასახსნელად საჭიროა შესაბამისი, გადამოწმებული მტკიცებულება.
```

**Uncertainty** — This wording abstains from a pin-specific hardware assertion. The structured reference keeps the actual status.

Decision ____________________ Reviewer ____________________ Date ____________________

Notes _______________________________________________________________________________

## `try_candidate`

**Allowed binding** — an exact alternative in the anchored domain with no qualified replayed PASS for that proposal. No engineering verdict is attached to the action. The current CHAT browser uses neutral option buttons. This inherited EDU-only draft is included for review completeness.

```text
შემდეგი ცდა: მოდელში შეამოწმე {proposed_contact} კონტაქტი და ხელახლა გაუშვი შემოწმება. ელექტრული თავსებადობა დაუდასტურებელია.
```

**Uncertainty** — Candidate action only. Direction and electrical evidence are open for the proposed action unless separately established.

Decision ____________________ Reviewer ____________________ Date ____________________

Notes _______________________________________________________________________________

## `try_scoped_alternative`

**Allowed binding** — exact alternate candidate with replayed `PHYSICAL_CAPABILITY / PASS / CAPABILITY_CONFIRMED`, no known failing check for that role and qualified sources. Example `sensor/Trig → board/J3.9` in the EDU CLI. The CHAT buttons do not render this separate EDU action draft.

```text
შემდეგი ცდა: მოდელში გადაიტანე {source} კავშირი {proposed_contact} კონტაქტზე და ხელახლა გაუშვი შემოწმება. ელექტრული თავსებადობა დაუდასტურებელია. ამ ალტერნატივაზე მიმართულების შემოწმება გავლილია.
```

**Uncertainty** — Direction evidence only, with electrical compatibility still unresolved.

Decision ____________________ Reviewer ____________________ Date ____________________

Notes _______________________________________________________________________________
