"""Required source admission entry point. Missing files fail rather than skip."""

import argparse
from hashlib import sha256
from pathlib import Path
import re

from inventor_edu import load_catalog, load_gpio_factset
from tests.test_gpio_capability import CATALOG_PIN, DATA, FACT_PIN

ARTIFACTS = {
    "sdk-mask": "soc_caps.h",
    "sdk-reference": "gpio.rst",
    "sdk-gpio": "esp32.inc",
    "board-header": "board.rst",
    "board-ordering": "ordering.inc",
}
HEADER_ROWS = {"J2.5": "GPIO34", "J3.9": "GPIO18", "J3.8": "GPIO19", "J3.19": "GPIO6", "J3.14": "GPIO0"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_sources(root: Path) -> None:
    facts = load_gpio_factset((DATA / "devkitc_32e_facts.json").read_bytes())
    catalog = load_catalog((DATA / "devkitc_32e_catalog.json").read_bytes(), expected_sha256=CATALOG_PIN)
    require(facts.factset_digest == FACT_PIN and facts.catalog_digest == CATALOG_PIN, "unexpected reviewed pin")
    require({source.source_id for source in facts.sources} == ARTIFACTS.keys(), "unexpected source inventory")
    files = {}
    for source in facts.sources:
        path = root / ARTIFACTS[source.source_id]
        raw = path.read_bytes()
        require("sha256:" + sha256(raw).hexdigest() == source.artifact_sha256, f"source hash mismatch: {path.name}")
        files[source.source_id] = raw.decode("utf-8")

    rendered = files["sdk-reference"]
    notes = files["sdk-gpio"]
    require("gpio/{IDF_TARGET_PATH_NAME}.inc" in rendered, "unexpected GPIO reference include")
    require("do not have software-enabled pullup or pulldown functions" in notes, "pull-up restriction missing")
    require("GPIO34-39 can only be set as input mode" in notes, "GPIO34 input-only note missing")
    require("GPIO0, GPIO2, GPIO5, GPIO12 (MTDI), and GPIO15 (MTDO)" in notes, "strap source changed")
    masks = files["sdk-mask"]
    valid = re.search(r"^#define SOC_GPIO_VALID_GPIO_MASK\s+\((0x[0-9A-F]+)ULL & ~\(([^)]+)\)\)", masks, re.M)
    output = re.search(
        r"^#define SOC_GPIO_VALID_OUTPUT_GPIO_MASK\s+\(SOC_GPIO_VALID_GPIO_MASK & ~\(([^)]+)\)\)",
        masks, re.M,
    )
    require(valid is not None and output is not None, "unexpected mask expression")
    excluded_inputs = {int(bit) for bit in re.findall(r"BIT(\d+)", valid[2])}
    excluded_outputs = {int(bit) for bit in re.findall(r"BIT(\d+)", output[1])}
    require({f.target for f in facts.silicon} == set(HEADER_ROWS.values()), "unexpected silicon coverage")
    for row in facts.silicon:
        pin = int(row.target.removeprefix("GPIO"))
        source_input = bool(int(valid[1], 16) & (1 << pin)) and pin not in excluded_inputs
        require((row.input_allowed, row.output_allowed) == (source_input, source_input and pin not in excluded_outputs),
                f"silicon flags disagree with masks: {row.target}")
        require(row.pullup_allowed is (False if pin == 34 else None), "unexpected positive pull-up fact")

    guide = files["board-header"]
    headers = guide[guide.index("\nHeader Block\n"):guide.index("\nPin Layout\n")]
    sections = re.split(r"(?m)^J[23]\r?$", headers)
    require(len(sections) == 3, "board source missing J2/J3 tables")
    require("ESP32-DevKitC V4" in guide and
            re.search(r"\* - ESP32-DevKitC-32E\s+- ESP32-WROOM-32E", files["board-ordering"]),
            "exact board-module orderable row missing")
    require({row.terminal_id: row.target for row in facts.mappings} == HEADER_ROWS, "unexpected mapping facts")
    board = next(d for d in catalog.definitions if d.definition_id == facts.scope.definition_id)
    require(board.definition_digest == facts.scope.definition_digest, "board definition pin mismatch")
    for terminal, gpio in HEADER_ROWS.items():
        header, position = terminal.split(".")
        table = sections[{"J2": 1, "J3": 2}[header]]
        row = re.search(rf"\* - {position}\r?\n(?:\s+ -[^\r\n]+\r?\n){{3}}", table)
        require(row is not None and re.search(rf"\b{gpio}\b", row[0]), f"board row mismatch: {terminal}")
        mapping = next(p.signal_ref for p in board.terminals if p.terminal_id == terminal)
        require((mapping.target_kind, mapping.target_id, mapping.mapping_status) == ("soc_gpio", gpio, "verified"),
                "catalog mapping differs from pinned table")
    require("The pins D0, D1, D2, D3, CMD and CLK are used internally" in guide
            and "SPI flash memory" in guide, "flash resource note missing")
    require([(row.target, row.reservation, row.operating_state) for row in facts.resources] ==
            [("GPIO6", "reserved", "ACTIVE")], "unexpected board resource facts")
    require([(row.target, row.is_strapping, row.boot_state) for row in facts.straps] ==
            [("GPIO0", True, "RESET")], "strap facts exceed reviewed scope")
    print("PASS: five authentic artifacts matched pins; masks, pull-up, header, flash, strap and -32E scope checked")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    args = parser.parse_args()
    try:
        check_sources(args.source_dir)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"BLOCKED: GPIO source admission: {exc}\n")
