# Regenerates the animated header and terminal. Edit LINES / the graph and rerun:
#   python assets/make_svgs.py
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
MONO = "ui-monospace, 'JetBrains Mono', 'Cascadia Code', Consolas, Menlo, monospace"
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"


def hero():
    hub = (900, 150)
    tenants = [(1060, 62), (1110, 175), (1010, 255), (790, 245), (760, 70)]
    lines, packets, nodes = [], [], []
    for i, (x, y) in enumerate(tenants):
        lines.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" class="wire"/>')
        packets.append(
            f'<circle r="3" fill="#58a6ff"><animateMotion dur="2.4s" begin="{i * 0.45}s" repeatCount="indefinite" '
            f'path="M{hub[0]},{hub[1]} L{x},{y}"/></circle>')
        # one tenant breaks contract, goes red, gets evicted and comes back green
        fill = ('<animate attributeName="fill" dur="7s" repeatCount="indefinite" '
                'values="#a371f7;#a371f7;#f85149;#f85149;#3fb950;#a371f7" keyTimes="0;.45;.5;.62;.7;1"/>') if i == 2 else ""
        nodes.append(
            f'<circle cx="{x}" cy="{y}" r="7" fill="#a371f7">{fill}'
            f'<animate attributeName="r" values="7;9;7" dur="2.4s" begin="{i * 0.45}s" repeatCount="indefinite"/></circle>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300">
<style>
  .wire {{ stroke: #a371f7; stroke-opacity: .45; stroke-width: 1.5; stroke-dasharray: 4 8; animation: flow 1.2s linear infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -24; }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#17122e"/></linearGradient>
  <radialGradient id="glow" cx=".75" cy=".5" r=".45"><stop offset="0" stop-color="#8957e5" stop-opacity=".38"/><stop offset="1" stop-color="#8957e5" stop-opacity="0"/></radialGradient>
  <linearGradient id="shine" x1="0" x2="700" gradientUnits="userSpaceOnUse" spreadMethod="repeat">
    <stop offset="0" stop-color="#e6edf3"/><stop offset=".35" stop-color="#a371f7"/><stop offset=".65" stop-color="#58a6ff"/><stop offset="1" stop-color="#e6edf3"/>
    <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="700 0" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="#8957e5" stop-opacity="0"/><stop offset=".5" stop-color="#a371f7"/><stop offset="1" stop-color="#58a6ff" stop-opacity="0"/></linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#30363d" stroke-opacity=".45"/></pattern>
  <linearGradient id="fadeR" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <mask id="m"><rect width="1200" height="300" fill="url(#fadeR)"/></mask>
  <clipPath id="clip"><rect width="1200" height="300" rx="14"/></clipPath>
</defs>
<g clip-path="url(#clip)">
  <rect width="1200" height="300" fill="url(#bg)"/>
  <g mask="url(#m)"><rect y="-40" width="1200" height="380" fill="url(#grid)">
    <animateTransform attributeName="transform" type="translate" from="0 0" to="0 40" dur="5s" repeatCount="indefinite"/></rect></g>
  <rect width="1200" height="300" fill="url(#glow)"/>
  {"".join(lines)}
  {"".join(packets)}
  {"".join(nodes)}
  <circle cx="{hub[0]}" cy="{hub[1]}" r="26" fill="none" stroke="#a371f7" stroke-opacity=".5">
    <animate attributeName="r" values="18;40" dur="2.4s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values=".6;0" dur="2.4s" repeatCount="indefinite"/></circle>
  <circle cx="{hub[0]}" cy="{hub[1]}" r="16" fill="#0d1117" stroke="#a371f7" stroke-width="3"/>
  <circle cx="{hub[0]}" cy="{hub[1]}" r="6" fill="#e6edf3"/>
  <g>
    <text x="72" y="104" font-family="{MONO}" font-size="16" fill="#a371f7">&gt; DizzyMii</text>
    <text x="68" y="170" font-family="{SANS}" font-size="72" font-weight="800" fill="url(#shine)">Kade Heglin</text>
    <text x="72" y="214" font-family="{MONO}" font-size="19" fill="#8b949e">agent tooling · claude skills · minecraft mods</text>
  </g>
  <rect y="297" width="1200" height="3" fill="url(#edge)"/>
</g>
</svg>
'''


# (prompt typed char by char, output lines shown all at once)
LINES = [
    ("whoami", ["kade heglin, self-taught, builds agent tooling and minecraft mods"]),
    ("ls ~/projects", ["fable-skills/  landlord/  Flint/  ai-engineering-brain/  Git-Kitchen/"]),
    ("cat landlord/README.md | head -1", ["parallel claude agents with contracts. break one and you get evicted"]),
    ("find ai-engineering-brain -name '*.md' | wc -l", ["660"]),
]
CHAR_W, ROW_H, TOP, LEFT = 9.6, 26, 70, 28
TYPE_SPEED, PAUSE = 0.055, 0.6


def terminal():
    rows, t, y = [], 0.6, TOP
    for i, (cmd, outs) in enumerate(LINES):
        w = CHAR_W * (len(cmd) + 4)
        steps = len(cmd)
        dur = steps * TYPE_SPEED
        vals = ";".join(f"{CHAR_W * (4 + k):.1f}" for k in range(steps + 1))
        rows.append(
            f'<clipPath id="c{i}"><rect x="{LEFT - 2}" y="{y - 18}" height="{ROW_H}" width="{CHAR_W * 4:.1f}">'
            f'<animate attributeName="width" values="{vals}" begin="{t:.2f}s" dur="{dur:.2f}s" calcMode="discrete" fill="freeze"/></rect></clipPath>'
            f'<text x="{LEFT}" y="{y}" clip-path="url(#c{i})" opacity="0">'
            f'<set attributeName="opacity" to="1" begin="{t - 0.3:.2f}s" fill="freeze"/>'
            f'<tspan fill="#3fb950">~</tspan><tspan fill="#a371f7"> $ </tspan><tspan fill="#e6edf3">{escape(cmd)}</tspan></text>')
        t += dur + 0.25
        for out in outs:
            y += ROW_H
            rows.append(f'<text x="{LEFT}" y="{y}" fill="#8b949e" opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>{escape(out)}</text>')
        y += ROW_H + 8
        t += PAUSE
    height = y + 10
    rows.append(
        f'<text x="{LEFT}" y="{y}" opacity="0"><set attributeName="opacity" to="1" begin="{t - 0.3:.2f}s" fill="freeze"/>'
        f'<tspan fill="#3fb950">~</tspan><tspan fill="#a371f7"> $ </tspan></text>'
        f'<rect x="{LEFT + CHAR_W * 4:.1f}" y="{y - 15}" width="10" height="19" fill="#a371f7" opacity="0">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 {height}" width="860" height="{height}">
<rect x=".5" y=".5" width="859" height="{height - 1}" rx="12" fill="#0d1117" stroke="#30363d"/>
<path d="M.5 40V12.5a12 12 0 0 1 12-12h835a12 12 0 0 1 12 12V40z" fill="#161b22"/>
<line x1="0" y1="40" x2="860" y2="40" stroke="#30363d"/>
<circle cx="24" cy="20" r="6" fill="#f85149"/><circle cx="44" cy="20" r="6" fill="#d29922"/><circle cx="64" cy="20" r="6" fill="#3fb950"/>
<text x="430" y="25" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8b949e">kade@dizzymii: ~</text>
<g font-family="{MONO}" font-size="16" xml:space="preserve">{"".join(rows)}</g>
</svg>
'''


(OUT / "hero.svg").write_text(hero(), encoding="utf-8")
(OUT / "terminal.svg").write_text(terminal(), encoding="utf-8")
