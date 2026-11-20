# Working in this repository

This repository publishes the **production** KlickTipp plugin. Relevant changes from
KlickTipp's internal staging plugin are adapted here for the production endpoint; this
repository has its own version tags.

[`README.md`](README.md) is the layout and the public picture. This file is the rules an
agent needs before changing anything.

## The three manifests move together

Under `plugins/klicktipp/`, `.claude-plugin/plugin.json` (Claude),
`.codex-plugin/plugin.json` (Codex/ChatGPT) and `.cursor-plugin/plugin.json` (Cursor) are
three manifests for one plugin. They **must carry the same `version`**, and all three read
the same `plugins/klicktipp/.mcp.json` and the same `skills/`.
`.github/scripts/check_manifests.py` fails the build when they drift, and the version
appears nowhere else but the `CHANGELOG.md` heading.

Claude and Cursor carry the listing fields flat (`displayName`, `documentationUrl`,
`privacyPolicyUrl` and so on); Codex carries them inside its `interface` block. The
checker compares both shapes against the Claude manifest.

The published plugin points at production only — `https://mcp.klicktipp.com/mcp`. Never
commit a staging or local endpoint into a manifest or `.mcp.json`.

## The plugin directory ships no executable code

`plugins/klicktipp/` accepts Markdown, text, JSON, YAML and a few image formats. A script
there is rejected. That is why the eval suite's generators live in
[`tools/`](tools/) at the repository root while everything they *write* stays inside the
plugin. Keep that split: if you need a new generator, it goes in `tools/`.

## Skills

`plugins/klicktipp/skills/<name>/SKILL.md`, seventeen of them, each with its own
`references/`. A skill's frontmatter `description` is what makes it fire, so changing it
changes behaviour — check the eval suite afterwards, not just the prose.

Skill sources are written in English — frontmatter, body and references alike — even
though the plugin talks to its users in German at runtime. Keep new text English and
match the voice of the file you are editing.

## The eval suite

[`plugins/klicktipp/evals/`](plugins/klicktipp/evals/) — behaviour cases run with
`claude plugin eval`. Read [`evals/README.md`](plugins/klicktipp/evals/README.md) before
touching it; the essentials:

- Every case runs twice, with the plugin and without, so the number that matters is **Δ**.
- **From inside a Claude Code session**, strip the injected token or the child fails with
  `401 Invalid bearer token`:
  ```bash
  cd plugins/klicktipp && env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL \
    -u CLAUDE_CODE_CHILD_SESSION claude plugin eval . --tag core \
    --ablation with-without --judge-model haiku --no-publish
  ```
- `--tag core` is the twelve guard cases, the everyday run. Drop it for all 33 before a
  release or after touching a skill the core set does not reach.
- The judge must not be the model under test — a model prefers its own output.
- Mocks are generated, never hand-edited: `python3 tools/build-mocks.py` from the root,
  `--check` in CI. Every case serves the full tool set.
- No real account is touched. Cases run against an agent mock of one fictional account.
- `evals/results/`, `.replay/` and `mocks/klicktipp/_tools.json` are git-ignored. The tool
  catalogue stays out of the repository on purpose — it mirrors the server's tool list
  word for word, and 133 of its parameter descriptions read to a scanner as credential
  handling.
- At `runs: 1` a single case's score is not evidence. Re-run a surprising result with
  `--runs 3` and read the judge's verdict text before calling it a regression.

Three cases are known-bad and documented as such in `evals/README.md`. Do not "fix" them
by loosening a grader.

## Changelog and releases

One entry per released version, newest first, heading `## X.Y.Z — YYYY-MM-DD` with an em
dash. The entry becomes the published release notes, so write for someone outside the
team: what the release does, then the specifics per skill and reference file, with the
staging MR or ticket where there is one.

A pushed tag publishes. Tags are lightweight, named for the bare version with no `v`
prefix, on the release commit:

```bash
git tag 0.36.0 && git push origin 0.36.0
```

`.github/workflows/release.yml` checks the tag against both manifests, revalidates, takes
the notes from that version's changelog section and attaches the zip. A tag without a
changelog section, or one that disagrees with the manifests, publishes nothing.

The `release` agent in [`.claude/agents/release.md`](.claude/agents/release.md) walks the
whole sequence. **The version number and the push are always the user's call.**

## Commits

Release commits are `Release X.Y.Z: <summary>` with a short body. Other commits describe
the change in the same plain voice. Commit only when asked.
