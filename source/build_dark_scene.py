# Builds img/space-banner-dark-v2.svg: the black-hole space scene shown on
# GitHub's dark theme.
#
# Prerequisite: vectorize.py has already been run on each sprite from the
# "Freepixel" pack (https://jik-a-4.itch.io/freepixel, Unlicense) to produce
# a vec/<name>.svg file for each of: sun, earth, earth_shattered,
# planet_magenta, planet_green, planet_teal_ring, planet_orange_ring, moon,
# moon_small, asteroid, blackhole.
#
# Usage: python build_dark_scene.py   (run from this directory)

import re, random, os

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
    "earth-shattered": "earth_shattered",
    "planet-magenta": "planet_magenta",
    "planet-green": "planet_green",
    "planet-teal-ring": "planet_teal_ring",
    "planet-orange-ring": "planet_orange_ring",
    "moon": "moon",
    "moon-small": "moon_small",
    "asteroid": "asteroid",
    "blackhole": "blackhole",
}

symbols = "\n".join(load_symbol(fname, sid) for sid, fname in SPRITES.items())

W, H = 540, 810

random.seed(11)
stars = []
for i in range(95):
    x = random.uniform(10, W - 10)
    y = random.uniform(8, H - 8)
    size = random.choice([1, 1, 1, 2, 2, 3])
    dur = round(random.uniform(2.2, 5.0), 2)
    delay = round(random.uniform(0, 5), 2)
    stars.append((round(x, 1), round(y, 1), size, dur, delay))

star_rects = "\n".join(
    f'      <rect class="star" x="{x}" y="{y}" width="{s}" height="{s}" '
    f'style="animation-duration:{d}s; animation-delay:{dl}s;"/>'
    for (x, y, s, d, dl) in stars
)

svg = f'''<!-- Sprite art from JIK-A-4's "Freepixel" pack (https://jik-a-4.itch.io/freepixel,
     Unlicense); vectorized to SVG paths with the contour-meshing engine from
     GLORP (c) 2026 ZackGphom, https://github.com/ZackGphom/GLORP -->
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Animated pixel-art space banner (black hole)"
     shape-rendering="crispEdges" preserveAspectRatio="xMidYMid meet">
  <title>Mateus's pixel space (dark)</title>
  <defs>
{symbols}
    <radialGradient id="glowCyan" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#4fd6ff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#4fd6ff" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <style>
    svg {{ background: transparent; }}

    .star {{
      fill: #eaf6ff;
      opacity: 0.15;
      animation-name: twinkle;
      animation-timing-function: ease-in-out;
      animation-iteration-count: infinite;
    }}
    @keyframes twinkle {{
      0%, 100% {{ opacity: 0.12; }}
      50% {{ opacity: 0.95; }}
    }}

    .float-slow {{ animation: floatY 6s ease-in-out infinite; }}
    .float-med  {{ animation: floatY 4.2s ease-in-out infinite; }}
    .float-fast {{ animation: floatY 3.1s ease-in-out infinite; }}
    @keyframes floatY {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-8px); }}
    }}

    .hero {{
      animation: pulse 4s ease-in-out infinite;
      transform-box: fill-box;
      transform-origin: center;
    }}
    .hero-glow {{ animation: glowPulse 4s ease-in-out infinite; }}
    @keyframes pulse {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.05); }}
    }}
    @keyframes glowPulse {{
      0%, 100% {{ opacity: 0.45; }}
      50% {{ opacity: 0.8; }}
    }}

    .spin-self {{
      animation: spin 12s linear infinite;
      transform-box: fill-box;
      transform-origin: center;
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}

    .drift {{ animation: driftX 17s ease-in-out infinite; }}
    @keyframes driftX {{
      0%, 100% {{ transform: translateX(0px); }}
      50% {{ transform: translateX(24px); }}
    }}

    .crossfade-a {{ animation: crossA 10s ease-in-out infinite; }}
    .crossfade-b {{ animation: crossB 10s ease-in-out infinite; }}
    @keyframes crossA {{
      0%, 68% {{ opacity: 1; }}
      78%, 92% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
    @keyframes crossB {{
      0%, 68% {{ opacity: 0; }}
      78%, 92% {{ opacity: 1; }}
      100% {{ opacity: 0; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      svg * {{ animation: none !important; }}
    }}

    /* the SVG's own rendered width -- fires based on how big the banner is
       actually displayed, not the page viewport, so the scene thins out
       instead of turning to mush on a narrow profile view */
    @media (max-width: 520px) {{ .tiny-detail {{ display: none; }} }}
    @media (max-width: 360px) {{ .small-detail {{ display: none; }} }}
  </style>

  <!-- stars -->
  <g>
{star_rects}
  </g>

  <!-- hero: the black hole -->
  <g transform="translate(360,120)">
    <circle r="46" fill="url(#glowCyan)" class="hero-glow"/>
    <use href="#blackhole" x="-30" y="-30" width="60" height="60" class="hero"/>
  </g>

  <!-- teal ringed planet -->
  <g transform="translate(160,260)">
    <g class="float-slow">
      <use href="#planet-teal-ring" x="-30" y="-30" width="60" height="60"/>
    </g>
  </g>

  <!-- small magenta planet with a tiny moon -->
  <g transform="translate(390,330)">
    <g class="float-med">
      <use href="#planet-magenta" x="-19" y="-19" width="38" height="38"/>
      <g class="tiny-detail">
        <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="7s" repeatCount="indefinite"/>
        <use href="#moon-small" x="23" y="-6" width="12" height="12"/>
      </g>
    </g>
  </g>

  <!-- earth <-> shattered earth, with an orbiting moon: a nod to "love breaking things" -->
  <g transform="translate(190,470)">
    <g class="float-slow" style="animation-duration:5.4s;">
      <use class="crossfade-a" href="#earth" x="-22" y="-22" width="44" height="44"/>
      <use class="crossfade-b" href="#earth-shattered" x="-28" y="-28" width="56" height="56"/>
      <g class="tiny-detail">
        <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="8s" repeatCount="indefinite"/>
        <use href="#moon" x="28" y="-8" width="15" height="15"/>
      </g>
    </g>
  </g>

  <!-- orange ringed planet -->
  <g transform="translate(380,590)">
    <g class="float-med" style="animation-duration:5s;">
      <use href="#planet-orange-ring" x="-24" y="-24" width="48" height="48"/>
    </g>
  </g>

  <!-- small green planet -->
  <g transform="translate(150,680)" class="small-detail">
    <g class="float-fast">
      <use href="#planet-green" x="-15" y="-15" width="30" height="30"/>
    </g>
  </g>

  <!-- tumbling asteroid near the bottom -->
  <g transform="translate(330,740)" class="tiny-detail">
    <g class="drift">
      <g class="spin-self">
        <use href="#asteroid" x="-13" y="-13" width="26" height="26"/>
      </g>
    </g>
  </g>
</svg>
'''

out_path = "../img/space-banner-dark-v2.svg"
with open(out_path, "w") as f:
    f.write(svg)
print("wrote", out_path, len(svg), "bytes")
