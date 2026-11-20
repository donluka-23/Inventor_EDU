"""Source-qualified and synthetic fixtures for CORE-001A."""

import hashlib
import json

from inventor_edu import ComponentInstance, Conductor, Junction, TerminalRef, compute_nets, create_snapshot, load_catalog
from inventor_edu.models import CatalogSnapshot, DeviceDefinition

BOARD = "esp32-devkitc-32e-v4"
SENSOR = "adafruit-3942-profile"
PASSIVE = "test-passive"
MODULE = "test-module"
ZERO = "sha256:" + "0" * 64


def encode(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode()


def checksum(value):
    return "sha256:" + hashlib.sha256(encode(value)).hexdigest()


def seal(definitions, sources=(), claims=(), *, version="1.0"):
    """Pin typed fixture data independently of the production encoder."""
    definitions = [json.loads(DeviceDefinition.model_validate_json(encode({
        **item, "definition_digest": ZERO,
    })).model_dump_json()) for item in definitions]
    for item in definitions:
        del item["definition_digest"]
        item["terminals"].sort(key=lambda terminal: terminal["terminal_id"])
        item["definition_digest"] = checksum(item)
    root = dict(catalog_schema_version=version, definitions=sorted(definitions, key=lambda x: x["definition_id"]),
                source_documents=sorted(sources, key=lambda x: x["source_document_id"]),
                claims=sorted(claims, key=lambda x: x["claim_id"]), catalog_digest=ZERO)
    root = json.loads(CatalogSnapshot.model_validate_json(encode(root)).model_dump_json())
    del root["catalog_digest"]
    root["catalog_digest"] = checksum(root)
    return encode(root)


def source(key, publisher, url, title, edition, media_type="text/html", publication_date=None):
    return dict(source_document_id=key, publisher=publisher, url=url, title=title, edition=edition,
                media_type=media_type, accessed_at_utc="2026-11-20", publication_date=publication_date,
                rights_state="link_only")


def terminal(key, label, role="unknown", contact_type="header_contact", **fields):
    return dict(terminal_id=key, printed_label=label, electrical_role=role, contact_type=contact_type, **fields)


def identity(provider, part, family, scope, **fields):
    return dict(brand_or_distributor=provider, orderable_part_or_sku=part, hardware_family=family,
                profile_scope=scope, **{"manufacturer_status": "unverified",
                "hardware_revision_status": "unverified", "silicon_revision_status": "unverified", **fields})


def definition(key, category, product, terminals, **fields):
    return dict(definition_schema_version="1.0", definition_id=key, device_class=category,
                identity=product, terminals=terminals, **fields)


def claim(key, property_name, device, value, source_key, locator, **fields):
    return dict(claim_id=key, claim_type=property_name, subject_definition_id=device["definition_id"],
                value=value, source_document_id=source_key, locator=locator,
                scope=device["identity"]["profile_scope"], review_status="approved", **fields)


def fixture_data():
    sources = [
        source("S18", "Espressif",
               "https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html",
               "ESP32-DevKitC V4 guide", "Live V4 guide"),
        source("S19", "Espressif", "https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_sch.pdf",
               "ESP32-DevKitC V4 schematic", "V4", "application/pdf", "2020-02-25"),
        source("S22", "Adafruit", "https://www.adafruit.com/product/3942",
               "HC-SR04 retail listing", "Product 3942 listing"),
        source("S23", "Adafruit", "https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/pinouts",
               "Ultrasonic Sonar Distance Sensors pinouts", "Edited 2024-03-08"),
    ]
    board = definition(BOARD, "dev_board", identity(
        "Espressif", "ESP32-DevKitC-32E", "ESP32-DevKitC", "Documented V4 / -32E / ESP32-WROOM-32E",
        manufacturer_status="verified", manufacturer_name="Espressif", hardware_revision="V4",
        assembled_module="ESP32-WROOM-32E",
    ), [], evidence_claim_ids=["board-identity"], internal_ideal_ties=[
        dict(terminal_ids=["J2.14", "J3.1", "J3.7"], evidence_claim_id="board-ground"),
    ])
    sensor = definition(SENSOR, "sensor", identity(
        "Adafruit", "3942", "HC-SR04", "Adafruit retail PID3942",
    ), [], evidence_claim_ids=["sensor-identity"])
    claims = [
        claim("board-identity", "profile_identity", board, "ESP32-DevKitC-32E / ESP32-WROOM-32E",
              "S18", "Ordering Information, -32E row", source_class="manufacturer",
              qualification="Documented variant only. Physical PCB and silicon revisions unverified."),
        claim("board-ground", "internal_ideal_tie", board, ["J2.14", "J3.1", "J3.7"],
              "S19", "Sheet 1, Connector, J2 pin 14 and J3 pins 1 and 7, common GND",
              source_class="manufacturer", qualification="V4 schematic and S18 header rows. Virtual profile only."),
        claim("sensor-identity", "profile_identity", sensor, "HC-SR04 retail PID3942", "S22",
              "Product title and Product ID", source_class="retailer",
              qualification="Retail identity only. Actual OEM and PCB revision unverified."),
    ]
    for key, label, role, target, kind in (
        ("J2.1", "3V3", "power", "3V3", "power_domain"),
        ("J2.5", "IO34", "input", "GPIO34", "soc_gpio"),
        ("J2.14", "GND", "ground", "GND", "power_domain"),
        ("J2.19", "5V", "power", "5V", "power_domain"),
        ("J3.1", "GND", "ground", "GND", "power_domain"),
        ("J3.7", "GND", "ground", "GND", "power_domain"),
        ("J3.8", "IO19", "io", "GPIO19", "soc_gpio"),
        ("J3.9", "IO18", "io", "GPIO18", "soc_gpio"),
    ):
        connector, position = key.split(".")
        claim_id = f"board-{key}"
        claims.append(claim(claim_id, "signal_mapping", board, target, "S18",
                            f"Header Block, {connector} row {position}", condition=key,
                            source_class="manufacturer", qualification="Documented header mapping only."))
        board["terminals"].append(terminal(key, label, role, connector_id=connector, contact_position=position,
                                           signal_ref=dict(terminal_id=key, target_kind=kind, target_id=target,
                                                           source_claim_id=claim_id, mapping_status="verified")))
    for key, role in (("Vcc", "power"), ("Trig", "input"), ("Echo", "output"), ("Gnd", "ground")):
        claim_id = f"sensor-{key}"
        claims.append(claim(claim_id, "signal_mapping", sensor, key, "S23", f"HC-SR04 Pinouts, {key}",
                            source_class="retailer", condition=key, qualification="Retail pinout only."))
        sensor["terminals"].append(terminal(key, key, role,
            signal_ref=dict(terminal_id=key, target_kind="signal", target_id=key,
                            source_claim_id=claim_id, mapping_status="verified")))
    passive = synthetic(PASSIVE, "passive", ("A", "B"), "lead")
    module = synthetic(MODULE, "integrated_circuit", ("P1", "P2", "P3"), "pad")
    return [board, sensor, passive, module], sources, claims


def reviewed_mapping_fixture_data():
    """Keep v1 definitions intact and author v1.1 evidence from reviewed primary source rows."""
    definitions, sources, claims = fixture_data()
    by_id = {item["definition_id"]: item for item in definitions}
    records = [item for item in claims if item["claim_type"] != "signal_mapping"]
    # S18 header table and ordering row for ESP32-DevKitC-32E / ESP32-WROOM-32E.
    for connector, position, target_kind, target_id in (
        ("J2", 1, "power_domain", "3V3"), ("J2", 5, "soc_gpio", "GPIO34"),
        ("J2", 14, "power_domain", "GND"), ("J2", 19, "power_domain", "5V"),
        ("J3", 1, "power_domain", "GND"), ("J3", 7, "power_domain", "GND"),
        ("J3", 8, "soc_gpio", "GPIO19"), ("J3", 9, "soc_gpio", "GPIO18"),
    ):
        terminal_id = f"{connector}.{position}"
        records.append(claim(
            f"board-{terminal_id}", "signal_mapping", by_id[BOARD],
            dict(terminal_id=terminal_id, target_kind=target_kind, target_id=target_id),
            "S18", f"Header Block, {connector} row {position}", source_class="manufacturer",
            qualification="R2 source review: documented V4 / -32E header contact only.",
        ))
    # S23 names these exposed interface signals for the S22 retail product, without OEM attribution.
    for terminal_id in ("Vcc", "Trig", "Echo", "Gnd"):
        records.append(claim(
            f"sensor-{terminal_id}", "signal_mapping", by_id[SENSOR],
            dict(terminal_id=terminal_id, target_kind="signal", target_id=terminal_id),
            "S23", f"HC-SR04 Pinouts, {terminal_id}", source_class="retailer",
            qualification="R2 source review: PID3942 retail interface only.",
        ))
    return definitions, sources, records


def synthetic(key, category, contacts, contact_type):
    return definition(key, category, identity(
        "Synthetic test data", key, "Opaque test part", "Synthetic topology fixture",
        manufacturer_status="not_applicable", hardware_revision_status="not_applicable",
        silicon_revision_status="not_applicable", synthetic_test_data=True,
    ), [terminal(contact, contact, contact_type=contact_type) for contact in contacts])


def part(catalog, instance_id, definition_id=PASSIVE):
    profile = next(item for item in catalog.definitions if item.definition_id == definition_id)
    return ComponentInstance(instance_id=instance_id, definition_id=definition_id,
                             definition_digest=profile.definition_digest)


def t(instance_id, terminal_id):
    return TerminalRef(instance_id=instance_id, terminal_id=terminal_id)


def wire(key, a, b):
    return Conductor(connection_id=key, endpoint_a=a, endpoint_b=b)


if __name__ == "__main__":
    from inventor_edu import JunctionRef

    catalog = load_catalog(seal(*fixture_data()))
    junction = JunctionRef(junction_id="j")
    snapshot = create_snapshot(catalog, instances=(part(catalog, "board", BOARD), part(catalog, "sensor", SENSOR)),
        junctions=(Junction(junction_id="j"),),
        conductors=(wire("signal-a", t("board", "J3.9"), junction),
                    wire("signal-b", junction, t("sensor", "Trig"))))
    for net in compute_nets(catalog, snapshot).nets:
        print(net.net_id, ", ".join(net.members))
