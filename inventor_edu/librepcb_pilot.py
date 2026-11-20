"""DATA-001 reader for one pinned LibrePCB Base resistor, not a general importer."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from uuid import UUID

from .core import load_catalog
from .models import CatalogSnapshot, DeviceDefinition, DeviceIdentity, EvidenceClaim, SourceDocument, TerminalDefinition

UPSTREAM = "LibrePCB-Libraries/LibrePCB_Base.lplib"
REVISION = "dc037a238eb5efcc034dd9d62e5775d5c21e90e4"
RAW_ROOT = f"https://raw.githubusercontent.com/{UPSTREAM}/{REVISION}/"
COMPONENT = "ef80cd5e-2689-47ee-8888-31d04fc99174"
PACKAGE = "5d9abd1b-cf0b-4cf7-8666-20a1add9971e"
DEVICE = "483a71eb-318e-448e-82ff-f02efc4821aa"
DEFINITION_ID = f"librepcb-{DEVICE}"
COMPONENT_FILE = f"cmp/{COMPONENT}/component.lp"
PACKAGE_FILE = f"pkg/{PACKAGE}/package.lp"
DEVICE_FILE = f"dev/{DEVICE}/device.lp"
MARKERS = (".librepcb-lib", f"cmp/{COMPONENT}/.librepcb-cmp",
           f"pkg/{PACKAGE}/.librepcb-pkg", f"dev/{DEVICE}/.librepcb-dev")
PINNED_FILES = (
    ("LICENSE.txt", "36ffd9dc085d529a7e60e1276d73ae5a030b020313e6c5408593a6ae2af39673"),
    ("README.md", "619212a20dd4d83914a890d64dceda8f9d36d764ec91ce49c818c17d6f61ccb3"),
    *((path, "53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3") for path in MARKERS),
    (COMPONENT_FILE, "8e76dc4bfaf40f56e6856883b4dee5af0f2c368633c3e3c9a7031fcdf1b17b07"),
    (PACKAGE_FILE, "61ee014c8bb7200eaf4c523b044dbc8090d8074c923059cfba46d601c98900c8"),
    (DEVICE_FILE, "3c4cce7d485a1260ac5980bb0ad1d5c9c292f384a49a9a920e95912092431a80"),
)
MAX_BYTES = 64 * 1024
MAX_DEPTH = 24
MAX_TOKENS = 12_000
TOKEN = re.compile(r'\s+|[()]|"(?:[^"\\\x00-\x1f]|\\["\\nrt])*"|[A-Za-z0-9_.:+/\-]+', re.ASCII)
META_FIELDS = frozenset("name description keywords author version created deprecated generated_by category".split())


class PilotSourceError(ValueError):
    """A selected source failed integrity, syntax, or relationship checks."""


class _Quoted(str):
    """Distinguish LibrePCB quoted text from bare structural atoms."""


def _parse(raw: bytes) -> list:
    if len(raw) > MAX_BYTES:
        raise PilotSourceError("source exceeds byte limit")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PilotSourceError("source is not UTF-8") from exc
    roots = []
    stack = [roots]
    position = count = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        if match is None:
            raise PilotSourceError(f"unsupported token at character {position}")
        token = match.group()
        position = match.end()
        if token.isspace():
            continue
        count += 1
        if count > MAX_TOKENS:
            raise PilotSourceError("source exceeds token limit")
        if token == "(":
            if len(stack) > MAX_DEPTH:
                raise PilotSourceError("source exceeds nesting limit")
            node = []
            stack[-1].append(node)
            stack.append(node)
        elif token == ")":
            if (len(stack) == 1 or not stack[-1] or type(stack[-1][0]) is not str):
                raise PilotSourceError("unbalanced or unsupported list")
            stack.pop()
        else:
            if position < len(text) and text[position] not in " \t\r\n()":
                raise PilotSourceError(f"missing delimiter at character {position}")
            stack[-1].append(_Quoted(json.loads(token)) if token.startswith('"') else token)
    if len(stack) != 1 or len(roots) != 1 or not isinstance(roots[0], list):
        raise PilotSourceError("expected one complete source record")
    return roots[0]


def _read_pinned(root: Path, relative: str, expected: str) -> bytes:
    with (root / relative).open("rb") as stream:
        contents = stream.read(MAX_BYTES + 1)
    if len(contents) > MAX_BYTES:
        raise PilotSourceError(f"source exceeds byte limit: {relative}")
    if sha256(contents).hexdigest() != expected:
        raise PilotSourceError(f"pinned digest mismatch: {relative}")
    return contents


def _uuid(value) -> str:
    try:
        if type(value) is str and str(UUID(value)) == value:
            return value
    except ValueError:
        pass
    raise PilotSourceError("expected a canonical UUID atom")


def _fields(node: list, first: int, allowed: frozenset[str]) -> dict[str, list]:
    fields = {}
    for item in node[first:]:
        if not isinstance(item, list) or item[0] not in allowed:
            raise PilotSourceError(f"unsupported field on {node[0]}")
        fields.setdefault(item[0], []).append(item)
    return fields


def _single(fields: dict, key: str, value_type: type = str):
    items = fields.get(key, ())
    if len(items) != 1 or len(items[0]) != 2 or type(items[0][1]) is not value_type:
        raise PilotSourceError(f"expected one {key} value")
    return items[0][1]


def _indexed(nodes: list) -> dict[str, list]:
    indexed = {}
    for node in nodes:
        key = _uuid(node[1] if len(node) >= 2 else None)
        if key in indexed:
            raise PilotSourceError(f"duplicate {node[0]} UUID {key}")
        indexed[key] = node
    return indexed


def _record(raw: bytes, root: str, expected_id: str, allowed: str) -> dict:
    node = _parse(raw)
    if len(node) < 2 or node[0] != root or _uuid(node[1]) != expected_id:
        raise PilotSourceError(f"wrong {root} identity")
    fields = _fields(node, 2, META_FIELDS | frozenset(allowed.split()))
    if _single(fields, "deprecated") != "false":
        raise PilotSourceError(f"unsupported deprecated {root}")
    return fields


def _extract(component: bytes, package: bytes, device: bytes) -> tuple[tuple[str, str, str], ...]:
    """Return (package pad UUID, printed pad number, mapped component signal UUID)."""
    cmp = _record(component, "librepcb_component", COMPONENT,
                  "schematic_only default_value prefix attribute signal variant")
    pkg = _record(package, "librepcb_package", PACKAGE,
                  "assembly_type grid_interval min_copper_clearance pad 3d_model footprint")
    dev = _record(device, "librepcb_device", DEVICE, "component package pad approved")
    if (_single(cmp, "schematic_only") != "false" or _single(pkg, "assembly_type") != "smt"
            or _single(dev, "approved") != "no_parts"
            or _uuid(_single(dev, "component")) != COMPONENT or _uuid(_single(dev, "package")) != PACKAGE):
        raise PilotSourceError("source is outside the generic resistor subset or joins do not match")

    signals = _indexed(cmp.get("signal", []))
    pads = _indexed(pkg.get("pad", []))
    mappings = _indexed(dev.get("pad", []))
    if len(signals) != 2 or len(pads) != 2 or mappings.keys() != pads.keys():
        raise PilotSourceError("expected exactly two complete package pad mappings and component signals")
    for node in signals.values():
        fields = _fields(node, 2, frozenset("name role required negated clock forced_net".split()))
        _single(fields, "name", _Quoted)
        if (_single(fields, "role") != "passive" or _single(fields, "required") != "true"
                or _single(fields, "negated") != "false" or _single(fields, "clock") != "false"
                or _single(fields, "forced_net", _Quoted)):
            raise PilotSourceError("unsupported component signal semantics")
    contacts = []
    for pad_id, pad in pads.items():
        label = _single(_fields(pad, 2, frozenset({"name"})), "name", _Quoted)
        fields = _fields(mappings[pad_id], 2, frozenset({"optional", "signal"}))
        if _single(fields, "optional") != "false":
            raise PilotSourceError("optional device pads are outside the pilot")
        contacts.append((pad_id, str(label), _uuid(_single(fields, "signal"))))
    if {label for _, label, _ in contacts} != {"1", "2"} or {signal for _, _, signal in contacts} != signals.keys():
        raise PilotSourceError("ambiguous pad labels or dangling/non-bijective signal references")

    footprints = _indexed(pkg.get("footprint", []))
    if not footprints:
        raise PilotSourceError("missing footprints")
    for footprint in footprints.values():
        fields = _fields(footprint, 2, frozenset(
            "name description tag 3d_position 3d_rotation 3d_model pad polygon stroke_text".split()
        ))
        links = []
        for pad in _indexed(fields.get("pad", [])).values():
            pad_fields = _fields(pad, 2, frozenset(
                "side shape position rotation size radius stop_mask solder_paste clearance function package_pad".split()
            ))
            if _single(pad_fields, "side") != "top" or _single(pad_fields, "function") != "standard":
                raise PilotSourceError("unsupported footprint pad type")
            links.append(_uuid(_single(pad_fields, "package_pad")))
        if len(links) != 2 or set(links) != pads.keys():
            raise PilotSourceError("hidden, duplicate or dangling footprint pad")
    return tuple(sorted(contacts))


def _json(data: dict) -> bytes:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def build_candidate(source_dir: Path) -> bytes:
    """Verify the nine selected artifacts and emit an admitted generic-only catalog."""
    files = {path: _read_pinned(source_dir, path, checksum) for path, checksum in PINNED_FILES}
    if not files["LICENSE.txt"].startswith(b"CC0 1.0 Universal") or any(files[p] != b"2\n" for p in MARKERS):
        raise PilotSourceError("unexpected license or library format marker")
    contacts = _extract(files[COMPONENT_FILE], files[PACKAGE_FILE], files[DEVICE_FILE])
    scope = f"Generic 1608 / 0603 device {DEVICE} at {REVISION}"
    documents = tuple(SourceDocument(
        source_document_id=key, url=RAW_ROOT + path, publisher="LibrePCB Libraries",
        title=path, edition=f"Git {REVISION}, format 2", accessed_at_utc="2026-11-20",
        media_type="text/plain", download_sha256=_digest(files[path]), rights_state="verified_reusable",
    ) for key, path in (("component", COMPONENT_FILE), ("device", DEVICE_FILE), ("package", PACKAGE_FILE)))
    claims = tuple(EvidenceClaim(
        claim_id=f"pad-{label}", claim_type="generic_pad_to_signal", subject_definition_id=DEFINITION_ID,
        value=signal_id, source_class="derived", source_document_id="device",
        locator=f"Root pad {pad_id}, signal child, joined to package and component records",
        condition=pad_id, scope=scope, qualification="Structural candidate only; no exact MPN linkage.",
        review_status="unverified",
    ) for pad_id, label, signal_id in sorted(contacts, key=lambda contact: contact[1]))
    definition = DeviceDefinition(
        definition_schema_version="1.0", definition_id=DEFINITION_ID, definition_digest="sha256:" + "0" * 64,
        device_class="passive.resistor", identity=DeviceIdentity(
            brand_or_distributor="LibrePCB Base library", manufacturer_status="unverified",
            orderable_part_or_sku=f"generic-device:{DEVICE}", hardware_family="Generic SMD resistor 1608 / 0603",
            hardware_revision_status="unverified", silicon_revision_status="not_applicable", profile_scope=scope,
        ), terminals=tuple(TerminalDefinition(terminal_id=pad_id, contact_type="pad", connector_id=PACKAGE,
            contact_position=label, printed_label=label, electrical_role="unknown")
            for pad_id, label, _ in contacts),
        evidence_claim_ids=tuple(claim.claim_id for claim in claims),
    )
    definition_body = definition.model_dump(mode="json", exclude={"definition_digest"})
    root = CatalogSnapshot(
        catalog_schema_version="1.1", definitions=(definition.model_copy(
            update={"definition_digest": _digest(_json(definition_body))}
        ),), source_documents=documents, claims=claims, catalog_digest="sha256:" + "0" * 64,
    ).model_dump(mode="json", exclude={"catalog_digest"})
    result = _json({**root, "catalog_digest": _digest(_json(root))})
    load_catalog(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--output", type=Path, help="Write catalog to a file instead of stdout")
    args = parser.parse_args()
    try:
        result = build_candidate(args.source_dir)
    except (OSError, PilotSourceError) as exc:
        parser.exit(1, f"DATA-001: {exc}\n")
    if args.output is None:
        sys.stdout.buffer.write(result)
    else:
        args.output.write_bytes(result)


if __name__ == "__main__":
    main()
