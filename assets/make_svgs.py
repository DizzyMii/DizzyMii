# Regenerates every SVG in assets/. Edit LINES / CARDS and rerun:
#   python assets/make_svgs.py
# Flat colors only, pulled from the DM logo.
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
RED, WHITE, INK, GREY, RULE = "#ac3232", "#f2f2f2", "#0d1117", "#57606a", "#d0d7de"
MONO = "ui-monospace, 'JetBrains Mono', 'Cascadia Code', Consolas, Menlo, monospace"
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"


def hero():
    hub = (960, 150)
    tenants = [(1100, 60), (1140, 180), (1050, 255), (850, 250), (870, 62)]
    wires, packets, nodes = [], [], []
    for i, (x, y) in enumerate(tenants):
        wires.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" class="wire"/>')
        packets.append(
            f'<rect x="-3" y="-3" width="6" height="6" fill="{WHITE}"><animateMotion dur="2.4s" begin="{i * 0.45}s" '
            f'repeatCount="indefinite" path="M{hub[0]},{hub[1]} L{x},{y}"/></rect>')
        # one tenant breaks contract, goes black, gets evicted and comes back
        evict = (f'<animate attributeName="fill" dur="7s" repeatCount="indefinite" calcMode="discrete" '
                 f'values="{WHITE};{INK};{WHITE};{INK};{WHITE}" keyTimes="0;.5;.56;.62;.7"/>') if i == 2 else ""
        nodes.append(f'<rect x="{x - 7}" y="{y - 7}" width="14" height="14" fill="{WHITE}" transform="rotate(45 {x} {y})">{evict}</rect>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300">
<style>
  .wire {{ stroke: {WHITE}; stroke-opacity: .55; stroke-width: 2; stroke-dasharray: 6 8; animation: flow 1s linear infinite; }}
  .run {{ stroke-dasharray: 1400; stroke-dashoffset: 1400; animation: run 4s cubic-bezier(.6,0,.2,1) infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -28; }} }}
  @keyframes run {{ 0% {{ stroke-dashoffset: 1400; }} 45%, 70% {{ stroke-dashoffset: 0; }} 100% {{ stroke-dashoffset: -1400; }} }}
</style>
<rect width="1200" height="300" fill="{WHITE}"/>
<polygon points="780,0 1200,0 1200,300 690,300" fill="{RED}"/>
<line x1="742" y1="300" x2="830" y2="0" stroke="{WHITE}" stroke-width="5"/>
<line x1="700" y1="318" x2="790" y2="-10" stroke="{RED}" stroke-width="3"/>
{"".join(wires)}
{"".join(packets)}
<circle cx="{hub[0]}" cy="{hub[1]}" r="20" fill="none" stroke="{WHITE}" stroke-width="2">
  <animate attributeName="r" values="20;46" dur="2.4s" repeatCount="indefinite"/>
  <animate attributeName="stroke-opacity" values="1;0" dur="2.4s" repeatCount="indefinite"/></circle>
{"".join(nodes)}
<rect x="{hub[0] - 16}" y="{hub[1] - 16}" width="32" height="32" fill="{INK}" stroke="{WHITE}" stroke-width="4" transform="rotate(45 {hub[0]} {hub[1]})"/>
<rect x="64" y="70" width="138" height="26" fill="{RED}" transform="skewX(-14)"/>
<text x="80" y="89" font-family="{MONO}" font-size="15" font-weight="700" fill="{WHITE}" letter-spacing="2">DIZZYMII</text>
<text x="60" y="172" font-family="{SANS}" font-size="80" font-weight="900" font-style="italic" fill="{INK}" letter-spacing="-1">KADE HEGLIN</text>
<path d="M64 196 H560 L590 220 H640" fill="none" stroke="{RED}" stroke-width="5" class="run"/>
<text x="64" y="252" font-family="{MONO}" font-size="16" font-weight="700" fill="{GREY}" letter-spacing="3">AGENT TOOLING / CLAUDE SKILLS / MINECRAFT MODS</text>
<rect width="1200" height="6" fill="{INK}"/>
</svg>
'''


# (prompt typed char by char, output lines shown all at once)
LINES = [
    ("whoami", ["kade heglin, self-taught, builds agent tooling and minecraft mods"]),
    ("ls ~/projects", ["fable-skills/  landlord/  Flint/  ai-engineering-brain/  Git-Kitchen/"]),
    ("cat landlord/README.md | head -1", ["parallel claude agents with contracts. break one and you get evicted"]),
    ("find ai-engineering-brain -name '*.md' | wc -l", ["660"]),
]
CHAR_W, ROW_H, TOP, LEFT = 9.6, 26, 72, 28
TYPE_SPEED, PAUSE = 0.055, 0.6


def prompt():
    return f'<tspan fill="{RED}" font-weight="700">~</tspan><tspan fill="{INK}" font-weight="700"> $ </tspan>'


def terminal():
    rows, t, y = [], 0.6, TOP
    for i, (cmd, outs) in enumerate(LINES):
        steps = len(cmd)
        dur = steps * TYPE_SPEED
        vals = ";".join(f"{CHAR_W * (4 + k):.1f}" for k in range(steps + 1))
        rows.append(
            f'<clipPath id="c{i}"><rect x="{LEFT - 2}" y="{y - 18}" height="{ROW_H}" width="{CHAR_W * 4:.1f}">'
            f'<animate attributeName="width" values="{vals}" begin="{t:.2f}s" dur="{dur:.2f}s" calcMode="discrete" fill="freeze"/></rect></clipPath>'
            f'<text x="{LEFT}" y="{y}" clip-path="url(#c{i})" opacity="0">'
            f'<set attributeName="opacity" to="1" begin="{t - 0.3:.2f}s" fill="freeze"/>'
            f'{prompt()}<tspan fill="{INK}" font-weight="700">{escape(cmd)}</tspan></text>')
        t += dur + 0.25
        for out in outs:
            y += ROW_H
            rows.append(f'<text x="{LEFT}" y="{y}" fill="{GREY}" opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>{escape(out)}</text>')
        y += ROW_H + 8
        t += PAUSE
    height = y + 14
    rows.append(
        f'<text x="{LEFT}" y="{y}" opacity="0"><set attributeName="opacity" to="1" begin="{t - 0.3:.2f}s" fill="freeze"/>{prompt()}</text>'
        f'<rect x="{LEFT + CHAR_W * 4:.1f}" y="{y - 15}" width="10" height="19" fill="{RED}" opacity="0">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 {height}" width="860" height="{height}">
<rect x=".5" y=".5" width="859" height="{height - 1}" fill="{WHITE}" stroke="{RULE}"/>
<rect width="860" height="40" fill="{INK}"/>
<rect x="18" y="14" width="12" height="12" fill="{RED}"/><rect x="38" y="14" width="12" height="12" fill="#30363d"/><rect x="58" y="14" width="12" height="12" fill="#30363d"/>
<text x="842" y="25" text-anchor="end" font-family="{MONO}" font-size="13" font-weight="700" fill="{WHITE}" letter-spacing="2">KADE@DIZZYMII</text>
<polygon points="0,40 120,40 112,46 0,46" fill="{RED}"/>
<g font-family="{MONO}" font-size="16" xml:space="preserve">{"".join(rows)}</g>
</svg>
'''


CARDS = [
    ("fable-skills", "CLAUDE CODE SKILLS",
     "Six skills that push Opus 4.8 toward Fable 5 behavior. Pressure-tested on real Opus subagents until the failure flipped, transcripts in the repo."),
    ("landlord", "PYTHON / MCP",
     "Splits one task into parallel Claude Agent SDK sessions bound by contracts. Break one and you get evicted. ~1,200 lines, 52 tests."),
    ("Flint", "TYPESCRIPT",
     "Agent runtime. Six primitives, one agent loop, one runtime dependency, errors come back as values."),
    ("ai-engineering-brain", "OBSIDIAN / 660 NOTES",
     "Linked notes from floating point up to inference economics. Every applied claim carries an evidence tier, a source and a date."),
]


def card(name, tag, desc):
    body = "".join(f'<text x="34" y="{92 + i * 20}">{escape(l)}</text>' for i, l in enumerate(wrap(desc, 54)))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 180" width="440" height="180">
<rect x=".5" y=".5" width="439" height="179" fill="{WHITE}" stroke="{RULE}"/>
<rect width="10" height="180" fill="{RED}"/>
<polygon points="360,0 440,0 440,56" fill="{RED}"/>
<line x1="392" y1="0" x2="440" y2="34" stroke="{WHITE}" stroke-width="3"/>
<text x="34" y="34" font-family="{MONO}" font-size="12" font-weight="700" fill="{RED}" letter-spacing="2">{escape(tag)}</text>
<text x="32" y="64" font-family="{SANS}" font-size="26" font-weight="900" font-style="italic" fill="{INK}">{escape(name.upper())}</text>
<g font-family="{SANS}" font-size="14" fill="{GREY}">{body}</g>
</svg>
'''


def footer():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 48" width="1200" height="48">
<rect width="1200" height="48" fill="{WHITE}"/>
<polygon points="0,0 900,0 880,48 0,48" fill="{INK}"/>
<polygon points="912,0 1200,0 1200,48 892,48" fill="{RED}"/>
<text x="1176" y="31" text-anchor="end" font-family="{MONO}" font-size="14" font-weight="700" fill="{WHITE}" letter-spacing="3">DM</text>
</svg>
'''


(OUT / "hero.svg").write_text(hero(), encoding="utf-8")
(OUT / "terminal.svg").write_text(terminal(), encoding="utf-8")
(OUT / "footer.svg").write_text(footer(), encoding="utf-8")
for c in CARDS:
    (OUT / f"card-{c[0].lower()}.svg").write_text(card(*c), encoding="utf-8")
