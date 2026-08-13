# claris-fm-reference

A [skill](https://agentskills.io) that gives Claude fast, reliable access to the official Claris FileMaker documentation — with a focus on the two things you look up most: **calculation functions** and **script steps**, including a complete **German/English name mapping**.

Instead of answering FileMaker questions from (possibly outdated or hallucinated) model knowledge, Claude resolves the function or script step name to its documentation slug and fetches the current page live from help.claris.com.

## Why

- Claris publishes every help page as Markdown under a stable URL scheme
  (`https://help.claris.com/markdown/{locale}/pro-help/<slug>.md`) — ideal for AI agents.
- LLMs routinely invent FileMaker parameter names and signatures. Fetching the
  real page eliminates that.
- German FileMaker solutions use localized names (`SetzeVar`, `Gehe zu Layout`,
  `Hole(LetzterFehler)`). The bundled mapping resolves them to their English
  counterparts and slugs — the slugs are language-neutral, so both locales of
  the docs are one fetch away.

## Contents

```
claris-fm-reference/
├── SKILL.md                     # instructions for the agent
├── references/
│   ├── functions.md             # all functions: EN name | slug, by category
│   ├── script-steps.md          # all script steps: EN name | slug, by category
│   └── mapping-de-en.md         # German | English | slug (generated)
└── scripts/
    └── update.py                # regenerates all three reference files
```

## How the agent uses it

1. Resolve the name (German → `mapping-de-en.md`, English → the index files) to a slug.
2. Fetch `https://help.claris.com/markdown/en/pro-help/<slug>.md` (or `de/`) —
   signature, parameters, compatibility, examples.
3. Answer with signatures quoted verbatim from the docs.

For complete or current lists (e.g. "all text functions"), the skill instructs
the agent to fetch the live category page rather than quote the bundled snapshot.

## Installation

**Claude Code** (recommended):

```bash
git clone https://github.com/<you>/claris-fm-reference ~/.claude/skills/claris-fm-reference
cd ~/.claude/skills/claris-fm-reference && python3 scripts/update.py
```

**Claude.ai:** zip the folder, then upload it under *Settings → Skills*.
Run `update.py` locally first — the claude.ai sandbox cannot reach
help.claris.com, so the generated files must ship inside the package.

## Updating after a FileMaker release

```bash
python3 scripts/update.py
```

Requires only Python 3 (stdlib) and internet access. It makes ~9 small
requests and rewrites all three reference files; each carries its generation
date in a header comment.

## How update.py works

The bodies of the Claris help pages are rendered client-side, so the Markdown
mirrors of the overview pages are empty. The navigation tree, however, is
served as static JavaScript by the underlying MadCap Flare help system:

```
https://help.claris.com/{locale}/pro-help/Data/Tocs/main_toc.js        # tree
https://help.claris.com/{locale}/pro-help/Data/Tocs/main_toc_ChunkN.js # titles
```

`update.py` parses the English TOC to extract the "Functions reference" and
"Script steps reference" subtrees (categories → entries), then loads the German
TOC and joins both locales over the language-neutral slug to produce the
mapping.

## Notes

- Data source is Claris' official help; this project stores no documentation
  content, only names, slugs, and URLs.
- Verified with the FileMaker 2026 (v26) documentation: 368 functions,
  216 script steps, 584/584 names mapped de/en.
- Not affiliated with Claris International Inc. FileMaker and Claris are
  trademarks of Claris International Inc.
