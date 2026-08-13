# Installing skills

Each subfolder in `claude-skills/` is one self-contained skill — a folder with
a `SKILL.md` inside, plus optional reference files and scripts. Installing a
skill simply means putting that folder where Claude can find it.

Claude runs in two places: the Claude app/website (**claude.ai**) and
**Claude Code**. They have separate skill stores, so pick the one you use —
or install in both. The examples below use `<skill-name>` as a placeholder
for the subfolder you want to install.

## Option A: Claude.ai (website / desktop / mobile app)

Claude.ai expects a skill as a single zip file.

1. Create the zip — the skill folder itself must be inside the archive:

   ```bash
   cd claude-skills
   zip -r <skill-name>.skill <skill-name>
   ```

   (On a Mac you can also right-click the folder → *Compress*, then rename
   the resulting `.zip` to `.skill`. Both extensions work.)

2. In Claude.ai, open **Settings → Skills** and upload the file.

3. **Start a new chat.** Skills are loaded when a conversation begins — an
   already-open chat will not see a newly installed or updated skill.

## Option B: Claude Code

Claude Code reads skills from a folder on your disk. Copy the skill into your
personal skills directory:

```bash
mkdir -p ~/.claude/skills
cp -r claude-skills/<skill-name> ~/.claude/skills/
```

Check: `~/.claude/skills/<skill-name>/SKILL.md` must exist — if it ended up
one level deeper, move it up.

Then **start a new Claude Code session** and type `/skills` to confirm the
skill is listed.

Alternative for a single project: put the folder into
`<project>/.claude/skills/` instead — then it applies only to that project
and can be committed to the repository for your whole team.

## Updating a skill

When a skill here changes (or ships its own update script — see the skill's
README), repeat the steps above:

- **Claude Code:** replace the folder in `~/.claude/skills/` (or run the
  skill's update script right there).
- **Claude.ai:** re-zip, remove the old version under **Settings → Skills**,
  upload the new zip.

In both cases: **start a new chat/session** afterwards, otherwise you keep
talking to the old version.
