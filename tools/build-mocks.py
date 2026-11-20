#!/usr/bin/env python3
"""Generate each case's MCP mock from a shared world and the full tool set.

Every case mocks every tool the suite knows: the union of mocks/klicktipp/_tools.json
(when tools/refresh-tools.py has written it) and every <group>/tools.txt. A mocked tool
is visible to Claude during the run and its schema goes into the run's context, so this
costs roughly 110k tokens of tool definitions per run — the groups used to mock only
their own tools, 1 to 61 of them, which was cheaper but let a skill reach for a tool the
mock did not serve. The fictional account is shared, so the groups agree about ids, tags
and counts.

<group>/tools.txt is no longer what a group serves. It stays as the record of which
tools that skill names, and it feeds the union above.

Layout it reads, below plugins/klicktipp/evals/:
    mocks/world.md              the fictional account, shared by every group
    mocks/klicktipp/_tools.json the production tools/list, when tools/refresh-tools.py
                                has written it (it is not committed)
    <group>/tools.txt           one tool name per line: the tools that skill names
    <group>/abort_when.md       the conditions that end a run, one per '- ' line

and writes <group>/<case>/mocks/klicktipp/_server.md for every case in the group.

    python3 tools/build-mocks.py [--check]

This script lives outside the plugin folder on purpose: the plugin directory accepts
Markdown, text, JSON, YAML and a few image formats there, and no executable scripts.

--check exits 1 when a file on disk differs from what would be written, for CI.
"""
import json, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "plugins" / "klicktipp" / "evals"
check = "--check" in sys.argv[1:]
catalogue = root / "mocks" / "klicktipp" / "_tools.json"
known = (
    {t["name"] for t in json.loads(catalogue.read_text())["tools"]}
    if catalogue.exists()
    else None
)
world = (root / "mocks" / "world.md").read_text().strip()

# Every case serves the same full set: the catalogue plus every tool a group names.
# A name only a group names is kept — the published catalogue the refresh script reads
# lags the server, and dropping such a tool would leave the skill that calls it unmocked.
named = {
    t.strip(): f
    for f in sorted(root.glob("*/tools.txt"))
    for t in f.read_text().split()
    if t.strip()
}
all_tools = sorted(set(named) | (known or set()))
if known is not None:
    for t in sorted(set(named) - known):
        print(f"{named[t].relative_to(root)}: {t} is not in the catalogue, mocked anyway",
              file=sys.stderr)

stale, written, groups = [], 0, 0
for tools_file in sorted(root.glob("*/tools.txt")):
    group = tools_file.parent
    tools = all_tools
    abort = (group / "abort_when.md").read_text().strip()
    header = "---\ntype: agent\ntools:\n" + "".join(f"  - {t}\n" for t in tools)
    header += "abort_when: |\n" + "".join(f"  {l}\n" for l in abort.splitlines()) + "---\n\n"
    body = header + world + "\n"
    groups += 1
    for case in sorted(p.parent for p in group.glob("*/prompt.md")):
        out = case / "mocks" / "klicktipp" / "_server.md"
        if out.exists() and out.read_text() == body:
            continue
        if check:
            stale.append(str(out.relative_to(root)))
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(body)
        written += 1

if check and stale:
    sys.exit("out of date, re-run tools/build-mocks.py:\n  " + "\n  ".join(stale))
note = "" if known is not None else " (tool names unchecked: run tools/refresh-tools.py first)"
print(f"{groups} group(s), {written} mock(s) written{note}", file=sys.stderr)
