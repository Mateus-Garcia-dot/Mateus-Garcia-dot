# Builds img/space-banner-light-v13.svg: the target-locked "star chart"
# scene shown on GitHub's light theme -- same node layout as the dark scene,
# but as a technical diagram (dashed links, corner brackets, rune glyphs)
# instead of trying to fake atmosphere on a white background.
#
# Prerequisite: same vec/<name>.svg symbols as build_dark_scene.py (this one
# only needs sun, earth, planet_magenta, planet_green, planet_teal_ring,
# planet_orange_ring, moon, asteroid -- no earth_shattered or moon_small,
# no black hole).
#
# Usage: python build_light_starchart.py   (run from this directory)

import re, os, random

VEC = "./vec"

def load_symbol(name, sym_id):
    with open(os.path.join(VEC, f"{name}.svg")) as f:
        content = f.read()
    vb = re.search(r'viewBox="([^"]+)"', content).group(1)
    inner = re.search(r'shape-rendering="crispEdges">\n(.*)\n</svg>', content, re.S).group(1)
    return f'<symbol id="{sym_id}" viewBox="{vb}">\n{inner}\n</symbol>'

SPRITES = {
    "sun": "sun",
    "earth": "earth",
    "planet-magenta": "planet_magenta",
    "planet-green": "planet_green",
    "planet-teal-ring": "planet_teal_ring",
    "planet-orange-ring": "planet_orange_ring",
    "moon": "moon",
    "asteroid": "asteroid",
}
symbols = "\n".join(load_symbol(fname, sid) for sid, fname in SPRITES.items())

W, H = 540, 810
INK = "#14161f"
AMBER = "#d98a2b"

# same layout as the dark (black hole) scene, so both themes share one composition
HUB = (360, 120)

NODES = {
    "teal":   (160, 260, "planet-teal-ring", 60),
    "magenta":(390, 330, "planet-magenta", 38),
    "earth":  (190, 470, "earth", 44),
    "orange": (380, 590, "planet-orange-ring", 48),
    "green":  (150, 680, "planet-green", 30),
    "asteroid":(330, 740, "asteroid", 26),
}

# hub-and-spoke plus a couple of cross links, like a network diagram.
# "earth" gets its own emphasized lock-line instead of a plain dashed link.
LINKS = [
    ("hub", "teal"), ("hub", "magenta"),
    ("hub", "orange"), ("hub", "green"), ("hub", "asteroid"),
    ("teal", "earth"), ("magenta", "orange"),
]

def pt(key):
    return HUB if key == "hub" else NODES[key][:2]

# small invented rune glyphs -- angular strokes, drawn in the node's own
# local -8..8 box
RUNES = [
    "M-6,-8 L-6,8 M-6,-2 L6,-8 M-6,2 L6,8",
    "M-7,8 L0,-8 L7,8 M-3,2 L3,2",
    "M-7,-8 L7,-8 M0,-8 L0,8 M-6,8 L6,8",
    "M-7,-6 L7,6 M-7,6 L7,-6",
    "M0,-8 L0,8 M-6,-4 L6,-4 M-6,4 L6,4",
    "M0,-8 L0,8 M-6,-8 L0,-2 L6,-8 M-6,8 L0,2 L6,8",
    "M-6,-8 L6,-8 L-6,8 L6,8",
    "M0,-8 L-6,0 L0,8 L6,0 Z",
    "M-7,-4 L7,-4 M-7,4 L7,4 M0,-8 L0,8",
]
RUNE_POS = [
    (480, 220, 6), (60, 430, 1), (470, 630, 4), (90, 720, 8), (250, 190, 5),
    (90, 90, 2), (450, 70, 7), (490, 400, 3), (460, 760, 0), (300, 280, 8),
]

links_svg = "\n".join(
    f'    <line x1="{pt(a)[0]}" y1="{pt(a)[1]}" x2="{pt(b)[0]}" y2="{pt(b)[1]}" '
    f'class="link" style="animation-delay:{i * 0.4}s;"/>'
    for i, (a, b) in enumerate(LINKS)
)

node_dots = "\n".join(
    f'    <circle cx="{x}" cy="{y}" r="3" fill="{INK}"/>'
    for (x, y, _, _) in NODES.values()
)

def bracket(r):
    d = 6
    return f'''<path d="M{-r},{-r+d} L{-r},{-r} L{-r+d},{-r}" fill="none" stroke="{AMBER}" stroke-width="2"/>
      <path d="M{r-d},{-r} L{r},{-r} L{r},{-r+d}" fill="none" stroke="{AMBER}" stroke-width="2"/>
      <path d="M{r},{r-d} L{r},{r} L{r-d},{r}" fill="none" stroke="{AMBER}" stroke-width="2"/>
      <path d="M{-r+d},{r} L{-r},{r} L{-r},{r-d}" fill="none" stroke="{AMBER}" stroke-width="2"/>'''

runes_svg = "\n".join(
    f'    <path d="{RUNES[i]}" transform="translate({x},{y})" class="rune" '
    f'style="animation-delay:{y * 0.01:.2f}s;" stroke="{AMBER}" stroke-width="1.6" fill="none"/>'
    for (x, y, i) in RUNE_POS
)

random.seed(21)
PLANET_MOTION = [
    (round(random.uniform(3.4, 7.4), 2), random.randint(5, 15), round(random.uniform(0, 2.4), 2))
    for _ in NODES
]

planet_uses = "\n".join(
    f'  <g transform="translate({x},{y})" style="--famp:{PLANET_MOTION[i][1]}px;">\n'
    f'    <g class="float-med" style="animation-duration:{PLANET_MOTION[i][0]}s; animation-delay:{PLANET_MOTION[i][2]}s;">\n'
    f'      <use href="#{sprite}" x="{-size/2}" y="{-size/2}" width="{size}" height="{size}"/>\n'
    f'    </g>\n'
    f'    <g class="bracket-follow" style="animation-duration:{PLANET_MOTION[i][0]}s; animation-delay:{PLANET_MOTION[i][2] + 0.5:.2f}s;">\n'
    f'      {bracket(size * 0.62 + 10)}\n'
    f'    </g>\n'
    f'  </g>'
    for i, (x, y, sprite, size) in enumerate(NODES.values())
)

svg = f'''<!-- Sprite art from JIK-A-4's "Freepixel" pack (https://jik-a-4.itch.io/freepixel,
     Unlicense); vectorized to SVG paths with the contour-meshing engine from
     GLORP (c) 2026 ZackGphom, https://github.com/ZackGphom/GLORP -->
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Animated pixel-art star chart banner"
     shape-rendering="crispEdges" preserveAspectRatio="xMidYMid meet">
  <title>Mateus's pixel star chart</title>
  <defs>
{symbols}
  </defs>

  <style>
    svg {{ background: transparent; }}

    .link {{
      stroke: {INK};
      stroke-width: 1.4;
      stroke-dasharray: 3 4;
      opacity: 0.55;
      animation: pulseLink 5s ease-in-out infinite;
    }}
    @keyframes pulseLink {{
      0%, 100% {{ opacity: 0.3; }}
      50% {{ opacity: 0.75; }}
    }}

    .rune {{
      animation: flicker 4.5s ease-in-out infinite;
    }}
    @keyframes flicker {{
      0%, 100% {{ opacity: 0.35; }}
      50% {{ opacity: 0.9; }}
    }}

    .lock-line {{
      stroke: {AMBER};
      stroke-width: 2;
      animation: lockPulse 2.4s ease-in-out infinite;
    }}
    @keyframes lockPulse {{
      0%, 100% {{ opacity: 0.6; }}
      50% {{ opacity: 1; }}
    }}

    .float-med {{ animation-name: floatY; animation-timing-function: ease-in-out; animation-iteration-count: infinite; }}
    @keyframes floatY {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(calc(-1 * var(--famp, 7px))); }}
    }}

    /* the target bracket rides the same path as its planet, but delayed
       and with a springy overshoot, so the planet clearly moves first and
       the bracket visibly chases and catches up behind it */
    .bracket-follow {{
      animation-name: floatY;
      animation-timing-function: cubic-bezier(0.3, 1.3, 0.6, 1);
      animation-iteration-count: infinite;
      animation-fill-mode: backwards;
    }}

    .hub-ring {{
      animation: spin 30s linear infinite;
      transform-box: fill-box;
      transform-origin: center;
    }}
    .hub-ticks {{
      animation: spinBack 22s linear infinite;
      transform-box: fill-box;
      transform-origin: center;
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes spinBack {{ to {{ transform: rotate(-360deg); }} }}

    .hub-pulse {{
      animation: pulse 4s ease-in-out infinite;
      transform-box: fill-box;
      transform-origin: center;
    }}
    @keyframes pulse {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.05); }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      svg * {{ animation: none !important; }}
    }}
  </style>

  <!-- connecting lines, drawn first so nodes sit on top -->
  <g>
{links_svg}
  </g>

  <!-- emphasized lock-line, targeting earth specifically -->
  <line x1="{HUB[0]}" y1="{HUB[1]}" x2="{NODES['earth'][0]}" y2="{NODES['earth'][1]}"
        class="lock-line"/>

  <g>
{node_dots}
  </g>

  <!-- runes -->
  <g>
{runes_svg}
  </g>

  <!-- hub: the sun, wrapped in target-lock HUD rings -->
  <g transform="translate({HUB[0]},{HUB[1]})">
    <circle r="50" fill="none" stroke="{INK}" stroke-width="1.2" stroke-dasharray="2 5" class="hub-ring"/>
    <g class="hub-ticks">
      <line x1="0" y1="-62" x2="0" y2="-54" stroke="{AMBER}" stroke-width="2"/>
      <line x1="0" y1="62" x2="0" y2="54" stroke="{AMBER}" stroke-width="2"/>
      <line x1="-62" y1="0" x2="-54" y2="0" stroke="{AMBER}" stroke-width="2"/>
      <line x1="62" y1="0" x2="54" y2="0" stroke="{AMBER}" stroke-width="2"/>
    </g>
    <use href="#sun" x="-30" y="-30" width="60" height="60" class="hub-pulse"/>
  </g>

  <!-- planets -->
{planet_uses}

  <!-- moon, orbiting earth -->
  <g transform="translate({NODES['earth'][0]},{NODES['earth'][1]})">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="9s" repeatCount="indefinite"/>
      <use href="#moon" x="26" y="-7" width="14" height="14"/>
    </g>
  </g>
</svg>
'''

out_path = "../img/space-banner-light-v13.svg"
with open(out_path, "w") as f:
    f.write(svg)
print("wrote", out_path, len(svg), "bytes")
