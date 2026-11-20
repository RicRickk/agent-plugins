---
name: release
description: Release the klicktipp plugin — run the eval suite, bump both manifests, write the CHANGELOG entry, commit, tag and push. Use when the user asks to cut, prepare or ship a release, to bump the version, to tag a version, or to write the changelog entry for one. Also use to run the eval suite on its own before deciding whether to release.
tools: Bash, Read, Edit, Write, Grep, Glob
model: sonnet
---

# Release the klicktipp plugin

A pushed tag publishes the release. `.github/workflows/release.yml` checks the tag against
both manifests, revalidates the plugin, takes the release notes from that version's
`CHANGELOG.md` section and attaches `klicktipp-<tag>.zip`. A tag without a changelog
section, or one that disagrees with the manifests, fails the run and publishes nothing.

So everything below happens **before** the tag is pushed. The push is the point of no
return: a tag that reaches the remote has published.

## What the user must decide, and you must not

- **The version number.** Ask for it, or propose one from the change and have them confirm.
  Never pick it silently.
- **Pushing.** Commit and tag locally, show what you did, and push only on an explicit yes.
  If the eval run came back worse than the last recorded one, say so in the same breath and
  let them decide with that in hand.
- **Releasing with a failing eval case.** Three cases are known-bad (see
  `plugins/klicktipp/evals/README.md`). A *new* failure is theirs to accept, not yours.

## Steps

### 1. Establish the current state

```bash
git status --short && git log --oneline -3 && git tag --sort=-creatordate | head -3
```

Read `plugins/klicktipp/.claude-plugin/plugin.json` and
`plugins/klicktipp/.codex-plugin/plugin.json`. Both carry the same `version` — if they
already disagree, stop and report it: that is a broken state, not something to fix in
passing.

A dirty tree is normal (that is the change being released). Uncommitted work unrelated to
the release is not — name it and ask.

### 2. Run the eval suite

From inside a Claude Code session the parent injects a token the child cannot use
(`401 Invalid bearer token`), so strip it. Run in the background; it takes minutes.

```bash
cd plugins/klicktipp && env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL \
  -u CLAUDE_CODE_CHILD_SESSION claude plugin eval . --tag core \
  --ablation with-without --judge-model haiku --no-publish
```

`--tag core` is the twelve guard cases. Drop it for all 33 before a release that touches a
skill the core set does not reach — which is most feature releases. Decide from the diff
which it is, and say which you ran.

Mocks are regenerated from `tools/build-mocks.py`; if `--check` reports stale files, run it
without `--check` and include the regenerated mocks in the release commit.

```bash
python3 tools/build-mocks.py --check
```

Read the result from `plugins/klicktipp/evals/results/<timestamp>/aggregate-result.json`:
`aggregates.meanDelta`, `casesPassed`, and any case whose `score` dropped against the
figures in `evals/README.md`. Report the mean Δ, the pass count and every failing case by
name. At `runs: 1` a single case's score is not evidence on its own — re-run a surprising
failure with `--runs 3` before calling it a regression.

### 3. Bump both manifests

Same version in both, nowhere else — the version appears only in these two files and in the
changelog heading.

```bash
grep -rn '"version"' plugins/klicktipp/.claude-plugin/plugin.json plugins/klicktipp/.codex-plugin/plugin.json
```

### 4. Write the CHANGELOG entry

Newest first, directly under the intro paragraph. The heading is `## X.Y.Z — YYYY-MM-DD`
with an em dash and today's real date (check it; do not carry over a date from an older
entry).

Match the voice of the entries already there: a bolded sentence naming what the release
does, then indented sub-bullets with the specifics — which skill changed, which reference
file, which tool, and the staging MR or ticket where there is one. Write what a reader of
the plugin needs to know, not a list of touched files. These become the published release
notes, so no internal-only shorthand that means nothing outside the team.

### 5. Commit

```bash
git add -A && git commit
```

Message: `Release X.Y.Z: <the same summary as the changelog's lead sentence, lowercased>`,
then a blank line and a short body of two to four lines covering the substance. Look at
`git log` for the established shape before writing it.

End the message with:

```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

### 6. Tag and push — only on an explicit yes

Tags here are lightweight and carry no `v` prefix: the bare version, on the release commit.

```bash
git tag X.Y.Z
```

Show the user the commit, the tag and the eval result, and ask before pushing. On their yes:

```bash
git push origin main && git push origin X.Y.Z
```

Push the branch before the tag. A tag whose commit is not on the remote publishes a release
pointing at a commit nobody can fetch.

### 7. Report

Name the version, what the eval run gave, what was committed and whether it was pushed. If
you did not push, say the tag exists locally and how to undo it (`git tag -d X.Y.Z`).

## Anything that does not fit

Stop and say so rather than improvise: the two manifests disagreeing, a tag that already
exists, a release workflow that fails after the push, a version the user wants that goes
backwards. None of those are recoverable by guessing.
