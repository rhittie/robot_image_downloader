# Claude Code Custom Commands

This folder contains custom slash commands for Claude Code. Use these to trigger specific workflows.

## Available Commands

| Command | Purpose |
|---------|---------|
| `/init` | **First time setup** - Configure project, set up GitHub, generate CLAUDE.md |
| `/planner` | Save all planning work to roadmap files and update CLAUDE.md |
| `/review` | Orient to project state and decide what to work on |
| `/builder` | Start building a feature from the roadmap |
| `/debug` | Troubleshoot and fix issues |
| `/cleanup` | Improve code quality without changing features |

## Usage

Just type the command in Claude Code:

```
/planner
```

Claude will follow the instructions in the corresponding .md file.

## When to Use Each Command

**First time setup (new project):**
```
/init
```
Run this once when you first set up the project. It will:
- Ask about your project and preferences
- Optionally set up GitHub (new or existing repo)
- Generate a customized CLAUDE.md
- **Important:** Restart your terminal after /init for commands to work!

**Starting a session:**
```
/review
```
Get oriented, see what's in progress, decide what to do.

**After brainstorming features:**
```
/planner
```
Save all plans before clearing the session.

**Ready to build:**
```
/builder
```
Pick a feature from planned/ and start implementing.

**Something broke:**
```
/debug
```
Systematic troubleshooting approach.

**Code getting messy:**
```
/cleanup
```
Refactor and improve without breaking things.

## Customizing Commands

Edit any .md file to adjust the workflow. Common customizations:
- Add project-specific checklists
- Change priorities or rules
- Add new steps to existing commands

## Creating New Commands

1. Create a new .md file in this folder
2. Write instructions for Claude to follow
3. Use it with `/your-command-name`

Example ideas:
- `/deploy` - Deployment checklist
- `/test` - Run through testing procedures
- `/document` - Generate/update documentation
