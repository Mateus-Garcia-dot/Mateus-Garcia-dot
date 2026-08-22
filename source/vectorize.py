# Turns a pixel-art PNG into a crisp SVG <path> per color, instead of an
# embedded raster image. Uses the contour-meshing engine from GLORP
# (c) 2026 ZackGphom, https://github.com/ZackGphom/GLORP -- non-commercial
# use, credit required. Clone that repo and put glorp_meshing.py next to
# this file (or on your PYTHONPATH) before running.
#
# Usage: python vectorize.py path/to/sprite.png [output.svg]

import numpy as np
from PIL import Image
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from glorp_meshing import path_finding


def png_to_paths(png_path):
    im = Image.open(png_path).convert("RGBA")
    arr = np.array(im)
    h, w = arr.shape[0], arr.shape[1]

    flat = arr.reshape(-1, 4)
    colors, inverse = np.unique(flat, axis=0, return_inverse=True)
    grid = inverse.reshape(h, w).astype(np.int32)

    paths = []
    for idx, (r, g, b, a) in enumerate(colors):
        if a == 0:
            continue
        d = path_finding(grid, idx)
        if not d:
            continue
        fill = f"#{r:02x}{g:02x}{b:02x}"
        opacity = round(int(a) / 255, 3)
        paths.append((d, fill, opacity))
    return paths, w, h


def paths_to_svg_group(paths):
    parts = []
    for d, fill, opacity in paths:
        op = "" if opacity >= 1 else f' fill-opacity="{opacity}"'
        parts.append(f'<path d="{d}" fill="{fill}"{op}/>')
    return "\n".join(parts)


if __name__ == "__main__":
    src = sys.argv[1]
    paths, w, h = png_to_paths(src)
    body = paths_to_svg_group(paths)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" shape-rendering="crispEdges">\n{body}\n</svg>'
    )
    out = sys.argv[2] if len(sys.argv) > 2 else src.rsplit(".", 1)[0] + ".svg"
    with open(out, "w") as f:
        f.write(svg)
    print("wrote", out, "paths:", len(paths))
