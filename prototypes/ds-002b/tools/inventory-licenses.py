"""Record all npm lock entries and retain the installed runtime notices."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
packages = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))["packages"]
ledger = root / "ASSET_AND_LICENSE_LEDGER.md"
marker = "\n## Locked npm packages\n"
table = ["| Package path | Version | License | Scope |",
         "| --- | --- | --- | --- |"]
notices = ["DS-002B third-party runtime notices",
           "Innerscene Corp. ESP32-DevKitC V4 nominal STEP derivative: CC0-1.0.",
           "Source: https://www.innerscene.com/tools/library/3d-parts/esp32-devkitc-v4-layout-1ab70892"]
for name, metadata in packages.items():
    if not name:
        continue
    if not metadata.get("license") or not metadata.get("integrity"):
        raise ValueError(f"Missing lock evidence for {name}")
    scope = "dev" if metadata.get("dev") else "runtime"
    if metadata.get("optional"):
        scope += " optional"
    license_text = metadata["license"].replace("|", "\\|")
    table.append(f"| `{name}` | {metadata['version']} | {license_text} | {scope} |")
    if scope == "runtime":
        files = sorted(path for path in (root / name).iterdir()
                       if path.is_file() and path.name.lower().startswith(("license", "notice", "copying")))
        if not files and name == "node_modules/@lit-labs/ssr-dom-shim":
            # The npm tarball omits LICENSE. The repository's BSD license
            # was checked byte-for-byte against Lit's installed copy.
            shared = root / "node_modules/lit/LICENSE"
            if hashlib.sha256(shared.read_bytes()).hexdigest() == "45d31799d0db956cc3eb5469346abbd9b7025babc5ff29fab10d7095da992ef1":
                files = [shared]
        if not files:
            raise ValueError(f"No runtime license file for {name}")
        for path in files:
            notices += [f"\n{'=' * 72}\n{name} {metadata['version']} / {path.name}",
                        path.read_text(encoding="utf-8-sig").rstrip()]

document = ledger.read_text(encoding="utf-8").split(marker)[0]
ledger.write_text(document.rstrip() + "\n" + marker + "\nEach entry's full registry URL and integrity hash is in [package-lock.json](package-lock.json).\n\n" +
                  "\n".join(table) + "\n", encoding="utf-8", newline="\n")
(root / "public").mkdir(exist_ok=True)
(root / "public/THIRD_PARTY_NOTICES.txt").write_text("\n".join(notices) + "\n", encoding="utf-8", newline="\n")
