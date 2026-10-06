## Kade Heglin

I build tooling for AI agents and Minecraft mods, mostly in Python, TypeScript and Java. Self-taught. Most of what's here started as something I wanted for myself and got out of hand (the AI engineering vault was supposed to be a few notes, it's 660 now).

### Agents

**[fable-skills](https://github.com/DizzyMii/fable-skills)** ![stars](https://img.shields.io/github/stars/DizzyMii/fable-skills?style=flat&label=%E2%98%85&color=555)<br>
Six Claude Code skills that push Opus 4.8 toward Fable 5 behavior on the stuff instructions can actually fix: what it claims, when it stops, what it touches, how it reports. Every skill was pressure-tested on real Opus subagents until the failure flipped, and the transcripts are in the repo.

**[landlord](https://github.com/DizzyMii/landlord)**<br>
MCP server that splits one task into parallel Claude Agent SDK sessions, each bound to a contract (objective, checkpoints, JSON Schema outputs). Tenants that break contract get evicted and retried with fresh context. Runs on a Pro/Max subscription with no API credits, ~1,200 lines and 52 tests.

**[Flint](https://github.com/DizzyMii/Flint)** · [docs](https://dizzymii.github.io/Flint/)<br>
TypeScript agent runtime. Six primitives, one agent loop, one runtime dependency, errors come back as values.

**[ai-engineering-brain](https://github.com/DizzyMii/ai-engineering-brain)** ![stars](https://img.shields.io/github/stars/DizzyMii/ai-engineering-brain?style=flat&label=%E2%98%85&color=555)<br>
~660 linked Obsidian notes on AI engineering, from floating point up to inference economics. Every empirical claim in the applied half carries an evidence tier, a named source and a date.

### Minecraft

**[bracken-reforged](https://github.com/DizzyMii/bracken-reforged)**<br>
Ports The Bracken Pack (11 dimensions, 74 biomes, 9 bosses, roughly 1,100 `mcfunction` files on scoreboard clocks) from a data pack to a NeoForge 1.21.1 mod. Same content and numbers, with the command runtime swapped for event listeners and a single tick scheduler.

### Smaller stuff

- [Git-Kitchen](https://github.com/DizzyMii/Git-Kitchen): Overcooked-themed multiplayer game for teaching testers git and PR hygiene
- [TestWeave](https://github.com/DizzyMii/TestWeave): drag-and-drop blocks in, Playwright / Selenium / Cypress / Puppeteer tests out
- [Resilient-Locator-Extractor](https://github.com/DizzyMii/Resilient-Locator-Extractor): CLI + Chrome extension that ranks selectors by how likely they are to survive DOM changes

---

Python, TypeScript, Java, Kotlin · NeoForge 1.21.1 · MCP and the Claude Agent SDK · pixel art in Aseprite, models in Blockbench

Discord: **DizzyMii**
