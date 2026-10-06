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


# the DM logo, traced from the avatar: first line is "w h", second is the path
_size, DM_PATH = (OUT / "dm_logo.path").read_text().splitlines()
DM_W, DM_H = map(int, _size.split())
TICKER = "FABLE-SKILLS  ///  LANDLORD  ///  FLINT  ///  AI-ENGINEERING-BRAIN  ///  660 NOTES  ///  NEOFORGE 1.21.1  ///  MCP  ///  "


def dm(x, y, scale, fill):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="{fill}" shape-rendering="crispEdges"><path d="{DM_PATH}"/></g>'


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
    tick_w = len(TICKER) * 8.8  # textLength pins it, so any mono font loops cleanly
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 330" width="1200" height="330">
<style>
  .wire {{ stroke: {WHITE}; stroke-opacity: .55; stroke-width: 2; stroke-dasharray: 6 8; animation: flow 1s linear infinite; }}
  .run {{ stroke-dasharray: 1400; stroke-dashoffset: 1400; animation: run 4s cubic-bezier(.6,0,.2,1) infinite; }}
  .speed {{ animation: speed linear infinite; }}
  .wipe {{ animation: wipe .9s cubic-bezier(.7,0,.2,1) .2s both; }}
  .reveal {{ animation: reveal .9s cubic-bezier(.7,0,.2,1) .2s both; }}
  .glitch {{ opacity: 0; animation: glitch 5s steps(1) 1.4s infinite; }}
  .ticker {{ animation: tick 22s linear infinite; }}
  @keyframes speed {{ from {{ transform: translateX(760px); }} to {{ transform: translateX(-260px); }} }}
  @keyframes wipe {{ from {{ transform: translateX(0); }} to {{ transform: translateX(1400px); }} }}
  @keyframes reveal {{ from {{ clip-path: inset(0 100% 0 0); }} to {{ clip-path: inset(0 0 0 0); }} }}
  @keyframes glitch {{ 0% {{ opacity: 1; transform: translateX(12px); }} 2% {{ opacity: 1; transform: translateX(-8px); }} 4%, 100% {{ opacity: 0; }} }}
  @keyframes tick {{ to {{ transform: translateX(-{tick_w:.0f}px); }} }}
  @keyframes flow {{ to {{ stroke-dashoffset: -28; }} }}
  @keyframes run {{ 0% {{ stroke-dashoffset: 1400; }} 45%, 70% {{ stroke-dashoffset: 0; }} 100% {{ stroke-dashoffset: -1400; }} }}
</style>
<rect width="1200" height="330" fill="{WHITE}"/>
<rect class="speed" style="animation-duration:1.9s" x="0" y="34" width="140" height="3" fill="{INK}"/>
<rect class="speed" style="animation-duration:2.7s;animation-delay:.6s" x="0" y="232" width="220" height="2" fill="{RED}"/>
<rect class="speed" style="animation-duration:3.4s;animation-delay:1.3s" x="0" y="270" width="90" height="4" fill="{INK}"/>
<polygon points="780,0 1200,0 1200,300 690,300" fill="{RED}"/>
{dm(842, 48, 3.1, "#9b2d2d")}
<line x1="742" y1="300" x2="830" y2="0" stroke="{WHITE}" stroke-width="5"/>
<line x1="1150" y1="300" x2="1200" y2="140" stroke="{WHITE}" stroke-width="3"/><line x1="1172" y1="300" x2="1200" y2="210" stroke="{WHITE}" stroke-width="3"/>
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
<g class="reveal"><text x="60" y="172" font-family="{SANS}" font-size="80" font-weight="900" font-style="italic" fill="{INK}" letter-spacing="-1">KADE HEGLIN</text></g>
<g class="glitch"><clipPath id="slice"><rect x="0" y="118" width="700" height="14"/><rect x="0" y="146" width="700" height="8"/></clipPath>
<text x="60" y="172" clip-path="url(#slice)" font-family="{SANS}" font-size="80" font-weight="900" font-style="italic" fill="{RED}" letter-spacing="-1">KADE HEGLIN</text></g>
<polygon class="wipe" points="40,100 110,100 90,186 20,186" fill="{RED}"/>
<path d="M64 196 H560 L590 220 H640" fill="none" stroke="{RED}" stroke-width="5" class="run"/>
<text x="64" y="252" font-family="{MONO}" font-size="16" font-weight="700" fill="{GREY}" letter-spacing="3">AGENT TOOLING / CLAUDE SKILLS / MINECRAFT MODS</text>
<rect width="1200" height="6" fill="{INK}"/>
<rect y="300" width="1200" height="30" fill="{INK}"/>
<g class="ticker" xml:space="preserve" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2" fill="{WHITE}">{"".join(f'<text x="{24 + i * tick_w:.0f}" y="320" textLength="{tick_w - 22:.0f}" lengthAdjust="spacing">{escape(TICKER)}</text>' for i in range(3))}</g>
<polygon points="0,300 150,300 136,330 0,330" fill="{RED}"/>
<text x="20" y="320" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2" fill="{WHITE}">NOW SHIPPING</text>
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


def heading(label):
    w = 40 + len(label) * 15
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 52" width="1200" height="52">
<polygon points="14,6 {w + 14},6 {w},46 0,46" fill="{RED}"/>
<text x="24" y="35" font-family="{SANS}" font-size="24" font-weight="900" font-style="italic" fill="{WHITE}" letter-spacing="1">{escape(label)}</text>
<polygon points="{w + 22},6 {w + 34},6 {w + 20},46 {w + 8},46" fill="{RED}"/>
<rect x="{w + 44}" y="40" width="{1200 - w - 44}" height="6" fill="#30363d"/>
</svg>
'''


QUERY = """query($login: String!) { user(login: $login) {
  followers { totalCount }
  repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) { nodes {
    stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } } }
  contributionsCollection { totalCommitContributions totalPullRequestContributions
    contributionCalendar { totalContributions weeks { contributionDays { contributionCount } } } } } }"""


def fetch_stats(login="DizzyMii"):
    import json, subprocess
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"login={login}"],
                         capture_output=True, text=True, check=True).stdout
    u = json.loads(out)["data"]["user"]
    repos = u["repositories"]["nodes"]
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    c = u["contributionsCollection"]
    days = [d["contributionCount"] for w in c["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    if days and days[-1] == 0:  # today not started yet doesn't break the streak
        days.pop()
    streak = 0
    for n in reversed(days):
        if not n:
            break
        streak += 1
    return {
        "numbers": [("CONTRIBUTIONS", c["contributionCalendar"]["totalContributions"]),
                    ("STARS EARNED", sum(r["stargazerCount"] for r in repos)),
                    ("PULL REQUESTS", c["totalPullRequestContributions"]),
                    ("DAY STREAK", streak)],
        "langs": sorted(langs.items(), key=lambda kv: -kv[1])[:5],
    }


def stats(s):
    cells = "".join(
        f'<text x="{40 + i * 205}" y="112" font-family="{SANS}" font-size="52" font-weight="900" font-style="italic" fill="{INK}">{n:,}</text>'
        f'<text x="{42 + i * 205}" y="138" font-family="{MONO}" font-size="12" font-weight="700" fill="{RED}" letter-spacing="2">{label}</text>'
        for i, (label, n) in enumerate(s["numbers"]))
    total = sum(v for _, v in s["langs"]) or 1
    bars = ""
    for i, (name, v) in enumerate(s["langs"]):
        y, pct = 196 + i * 30, v / total
        bars += (f'<text x="40" y="{y + 13}" font-family="{MONO}" font-size="13" font-weight="700" fill="{INK}">{escape(name.upper())}</text>'
                 f'<rect x="220" y="{y}" width="540" height="16" fill="#e1e4e8"/>'
                 f'<rect x="220" y="{y}" width="0" height="16" fill="{RED if i == 0 else INK}">'
                 f'<animate attributeName="width" to="{540 * pct:.0f}" dur=".9s" begin="{0.2 + i * 0.12:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 0 .2 1" keyTimes="0;1"/></rect>'
                 f'<text x="820" y="{y + 13}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{GREY}">{pct:.0%}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 360" width="860" height="360">
<rect x=".5" y=".5" width="859" height="359" fill="{WHITE}" stroke="{RULE}"/>
<rect width="10" height="360" fill="{RED}"/>
<polygon points="760,0 860,0 860,70" fill="{RED}"/><line x1="800" y1="0" x2="860" y2="42" stroke="{WHITE}" stroke-width="3"/>
<text x="40" y="40" font-family="{MONO}" font-size="12" font-weight="700" fill="{GREY}" letter-spacing="2">LAST 12 MONTHS</text>
{cells}
<rect x="40" y="162" width="780" height="2" fill="{RULE}"/>
<text x="40" y="184" font-family="{MONO}" font-size="12" font-weight="700" fill="{GREY}" letter-spacing="2">LANGUAGES / PUBLIC REPOS</text>
{bars}
</svg>
'''


(OUT / "hero.svg").write_text(hero(), encoding="utf-8")
(OUT / "terminal.svg").write_text(terminal(), encoding="utf-8")
(OUT / "footer.svg").write_text(footer(), encoding="utf-8")
for c in CARDS:
    (OUT / f"card-{c[0].lower()}.svg").write_text(card(*c), encoding="utf-8")
for h in ["AGENTS", "SMALLER STUFF", "STACK", "STATS"]:
    (OUT / f"h-{h.lower().replace(' ', '-')}.svg").write_text(heading(h), encoding="utf-8")
try:
    (OUT / "stats.svg").write_text(stats(fetch_stats()), encoding="utf-8")
except Exception as e:  # no gh / no network: keep the last stats.svg
    print("stats skipped:", e)
