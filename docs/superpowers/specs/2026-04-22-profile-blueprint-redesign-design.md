# GitHub Profile Blueprint Redesign — Design Spec

**Date:** 2026-04-22
**Repo:** github.com/DizzyMii/DizzyMii
**File:** README.md

---

## Summary

Full replacement of the current dark-minimal profile README with a System Blueprint aesthetic. The profile reads like a technical system manifest — boot sequence header, intercepted signal quote, and field-value module tables throughout. No external image widgets. Pure monospace text with amber accent color.

---

## Visual Identity

| Property | Value |
|---|---|
| Font family | `Courier New` / monospace (rendered via `<pre>` blocks or `code` spans where supported; otherwise inline HTML) |
| Background | `#0d1117` (GitHub dark native) |
| Accent color | `#d29922` (amber / warning-system) |
| Primary text | `#e6edf3` (field labels, names) |
| Secondary text | `#8b949e` (descriptions, metadata) |
| OK status | `#3fb950` (green) |
| Active/warning | `#d29922` (amber) |
| Dividers | `#21262d` (subtle dark rule) |
| Section headers | `────` / `════` monospace box-drawing characters in amber |

---

## Structure (top to bottom)

### 1. Boot Sequence Header

Opens with a simulated system boot log. No banner image, no capsule-render, no typing SVG.

```
SYSTEM BOOT ─ DizzyMii OS v2.0 ───────────────────────────────
[OK]  loading identity          ......done
[OK]  mounting stack            ......done
[OK]  initializing agents       ......done
[!!]  reverse engineering       ......active
[OK]  minecraft runtime         ......loaded
───────────────────────────────────────────────────────────────
```

- `[OK]` lines in `#3fb950` green
- `[!!]` lines in `#d29922` amber
- Header/footer dividers in amber at 9.5px, letter-spacing: 3px
- Status words (`done`, `active`, `loaded`) right-aligned via `&nbsp;` padding

### 2. Incoming Signal / Quote

Framed transmission block immediately after boot sequence.

```
▶ INCOMING SIGNAL ──────────────────────────────────────────
  "I don't just use systems. I take them apart."
▶ SIGNAL END ───────────────────────────────────────────────
```

- Quote in `#e6edf3`, font-size 13.5px, italic, indented 16px
- Frame lines in amber, letter-spacing 3px

### 3. MODULE: IDENTITY

Field-value table with no borders — tab-aligned using `&nbsp;`.

```
◆ MODULE: IDENTITY ─────────────────────────────────────────
CLASSIFICATION  │ System Architect · Context Engineer · Reverse Engineer
ORIGIN          │ self-taught · no bootcamp · no framework tutorials
PHILOSOPHY      │ understand the system, not just the framework
CURRENT BUILD   │ multi-agent orchestration · Minecraft mods
```

- Field labels in `#e6edf3`
- `│` pipe in `#8b949e`
- Values: highlighted items in `#d29922`, plain metadata in `#8b949e`

### 4. MODULE: STACK

```
◆ MODULE: STACK ────────────────────────────────────────────
primary      │ Java · Kotlin
scripting    │ Python · TypeScript · JavaScript
platform     │ Git · GitHub · Linux · Bash · Docker
design       │ Aseprite · Blockbench
```

- No skill icon images — pure text
- Primary language values in `#d29922`, others in `#8b949e`

### 5. MODULE: ACTIVE PROCESSES

Projects listed as running processes with status indicators.

```
◆ MODULE: ACTIVE PROCESSES ─────────────────────────────────
landlord         │ ● DEPLOYED   task delegation framework for multi-agent AI
dreamcatcher     │ ● ACTIVE     RE suite for server structures + protocol analysis
context-hunter   │ ● STABLE     static analysis CLI — extracts context from binaries
hiring-platform  │ ○ ARCHIVED   solo-built end-to-end hiring process application
```

- `● DEPLOYED` / `● ACTIVE` in `#d29922`
- `● STABLE` in `#3fb950`
- `○ ARCHIVED` in `#8b949e`
- Project names link via HTML `<a>` tags:
  - `landlord` → `https://github.com/DizzyMii/Landlord`
  - `dreamcatcher` → `https://github.com/DizzyMii/Dreamcatcher`
  - `context-hunter` → `https://github.com/DizzyMii/ContextHunter`
  - `hiring-platform` → `https://github.com/DizzyMii/HiringPlatform`

### 6. MODULE: SYSTEM METRICS

Pure text metrics — no stats cards, no streak images, no activity graph images.

```
◆ MODULE: SYSTEM METRICS ───────────────────────────────────
contributions   │ ████████░░  see profile
primary lang    │ Java / Kotlin
streak          │ active
visibility      │ public + classified
```

- Progress bar built from Unicode block characters (`█` / `░`) — static/decorative, not pulled from live data
- "classified" in `#d29922`

### 7. MODULE: WORKSTATION (collapsible)

Remains as a `<details>/<summary>` block, content reformatted as blueprint table.

```
◆ MODULE: WORKSTATION [collapsed] ──────────────────────────
  ▸ CPU: AMD Ryzen 7 9800X3D · GPU: AMD Radeon RX 9070 XT · 1080p 240Hz · Windsurf
```

Full expanded content:

```
component  │ spec
CPU        │ AMD Ryzen 7 9800X3D
GPU        │ AMD Radeon RX 9070 XT
display    │ 1080p · 240Hz
ide        │ Windsurf
design     │ Aseprite · Blockbench
```

### 8. MODULE: INTERFACES

```
◆ MODULE: INTERFACES ───────────────────────────────────────
github   │ github.com/DizzyMii
discord  │ DizzyMii

open to discussing anything — reach out.
```

- `github.com/DizzyMii` links to profile via `<a>` tag, displayed as text
- "reach out." in `#8b949e`

### 9. Closing Rule + Quote

```
────────────────────────────────────────────────────────────
Evolution is not an update. It is the result of a mind that refuses to stall.
█
```

- Divider in amber
- Quote in `#8b949e`, italic
- Trailing cursor `█` in `#d29922`

---

## Implementation Approach

GitHub README constraints:
- Markdown + HTML only — no JavaScript executes
- Inline styles work; CSS classes do not
- `<pre>` blocks preserve monospace but GitHub strips color — must use `<div>`/`<span>` with inline styles for colored text
- All colored sections implemented as `<div align="left">` with `<span style="...">` for color
- Divider lines built from `─`, `═`, `◆`, `▶`, `│`, `█`, `░`, `●`, `○` Unicode characters
- Fonts: GitHub's sanitizer strips `font-family` from inline styles — monospace look is achieved by using `<code>` backtick spans for uncolored content; colored spans will render in GitHub's default sans-serif but alignment via `&nbsp;` padding still holds
- No `background-color` set on container `<div>`s — let GitHub's native dark/light theme handle the background; colors are text-only

**Removed entirely:**
- `capsule-render` header/footer banners
- Typing SVG animation
- GitHub trophy badges
- Stats cards (github-readme-stats)
- Streak counter (streak-stats.demolab.com)
- Activity graph (github-readme-activity-graph)
- Snake contribution animation
- Skill icon images (skillicons.dev)
- All `<img>` tags — no images in the final README

---

## What's Preserved

- `.github/workflows/snake.yml` — untouched (workflow still runs even if SVG not displayed)
- Closing quote text
- All four projects and their descriptions
- Workstation specs
- GitHub + Discord contact links

---

## Out of Scope

- Dynamic/auto-updating content (requires external services)
- Custom domain or JS interactivity
- Light/dark mode variants (profile is designed for GitHub dark theme; degrades gracefully on light)
