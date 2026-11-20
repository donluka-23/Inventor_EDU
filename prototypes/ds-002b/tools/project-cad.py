"""Project the reviewed Innerscene mesh JSON exported by occt-import-js."""
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from PIL import Image, ImageDraw

source = Path(sys.argv[1])
assert hashlib.sha256(source.read_bytes()).hexdigest() == "7d6580aaa58a8d3e4b5bb237e6d2d10f8330891ba063873430379542e0b2ed01"
meshes = json.loads(Path(sys.argv[2]).read_text())["meshes"]
output = Path(sys.argv[3])
scale = 20
width, height = 29, 51
rows, faces = [], []
for mesh in meshes:
    data = mesh["attributes"]["position"]["array"]
    vertices = list(zip(data[::3], data[1::3], data[2::3]))
    name = mesh["name"]
    contact = re.fullmatch(r"Header_([01])_pin_(\d+)", name)
    if contact:
        row = ["J2", "J3"][int(contact[1])]
        number = 20 - int(contact[2])
        x, y = [(min(v[axis] for v in vertices) + max(v[axis] for v in vertices)) / 2 for axis in (0, 1)]
        rows.append(dict(id=f"{row}.{number}", mesh=name, x=round((x + .53) / width, 8), y=round((49 - y) / height, 8)))
    if name.startswith("Header_") and name.endswith("housing"):
        continue
    indices = mesh["index"]["array"]
    base = (40, 47, 51)
    if contact:
        base = (220, 172, 84)
    elif name in ("RF_shield", "Micro_USB_shield") or name.endswith("_lid"):
        base = (170, 185, 192)
    elif name == "PCB":
        base = (35, 44, 50)
    elif name == "WROOM_module":
        base = (20, 61, 49)
    elif name == "Illustrative_antenna":
        base = (157, 113, 55)
    elif name in ("Regulator", "USB_UART"):
        base = (16, 22, 27)
    for i in range(0, len(indices), 3):
        a, b, c = [vertices[index] for index in indices[i:i + 3]]
        u, v = [[point[k] - a[k] for k in range(3)] for point in (b, c)]
        normal = [u[(k+1)%3]*v[(k+2)%3]-u[(k+2)%3]*v[(k+1)%3] for k in range(3)]
        size = math.sqrt(sum(value**2 for value in normal))
        if size == 0 or abs(normal[2]) < 1e-5:
            continue
        shade = .75 + .25 * abs(normal[2]) / size
        faces.append((sum(point[2] for point in (a,b,c)) / 3,
                      [((x + .53)*scale, (49-y)*scale) for x,y,_ in (a,b,c)],
                      tuple(round(channel*shade) for channel in base)))
image = Image.new("RGBA", (width*scale, height*scale))
draw = ImageDraw.Draw(image)
for _, points, color in sorted(faces, key=lambda face: face[0]):
    draw.polygon(points, fill=(*color,255))
image.save(output / "devkitc-v4.png", optimize=True)
rows.sort(key=lambda pin: (pin["id"][:2], int(pin["id"][3:])))
assert len(rows) == len({pin["id"] for pin in rows}) == 38
(output / "devkitc-v4.json").write_text(
    json.dumps(dict(width=width, height=height, pins=rows), indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)
