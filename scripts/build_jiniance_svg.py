from PIL import Image
import base64
from io import BytesIO
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = root / "jiniance.png"
im = Image.open(src).convert("RGBA")
px = im.load()
removed = 0
for y in range(im.height):
    for x in range(im.width):
        r, g, b, a = px[x, y]
        if min(r, g, b) >= 252:
            px[x, y] = (r, g, b, 0)
            removed += 1
        elif r >= 250 and g >= 250 and b >= 250 and max(r, g, b) - min(r, g, b) <= 6:
            px[x, y] = (r, g, b, 0)
            removed += 1

print("removed", removed)
im.save(root / "jiniance-alpha.png", optimize=True)

buf = BytesIO()
im.save(buf, format="PNG", optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode("ascii")

svg = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink" '
    'viewBox="0 0 830 623" width="830" height="623">\n'
    '  <image width="830" height="623" preserveAspectRatio="xMidYMid meet" '
    f'xlink:href="data:image/png;base64,{b64}"/>\n'
    "</svg>\n"
)
(root / "jiniance.svg").write_text(svg, encoding="utf-8")
print("wrote jiniance-alpha.png and jiniance.svg")
