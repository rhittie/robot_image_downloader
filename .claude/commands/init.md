# Init Agent - Project Setup Wizard

You are now in **Init mode**. Help the user set up or update their Claude Code project configuration.

---

## Step 1: Detect Current State

First, check the project:
1. Does `CLAUDE.md` exist in the project root?
2. Does it have real content or just placeholders?
3. Is there existing code in the project?

**If CLAUDE.md exists with real content:**
Ask the user:
> "I found an existing CLAUDE.md configuration. Would you like to:
> A) Update specific sections
> B) Start fresh with a new configuration
> C) Cancel"

**If CLAUDE.md is missing or has only placeholders:**
Proceed with full initialization.

---

## Step 2: Gather Project Information

Ask these questions conversationally (not all at once). Wait for answers before continuing.

### Project Basics

**Ask:**
> "Let's set up your project! First, some basics:
> 1. What's your project name?
> 2. In 1-2 sentences, what does it do?
> 3. What type of project is this? (web app, frontend only, backend/API, CLI tool, library, or other)"

### Tech Stack

**Ask based on project type:**
> "Now for your tech stack:
> - What's your primary language? (TypeScript, JavaScript, Python, Go, etc.)
> - [If applicable] What frontend framework? (React, Vue, Svelte, None, etc.)
> - [If applicable] What backend framework? (Express, Fastify, Django, Flask, None, etc.)
> - [If applicable] What database? (PostgreSQL, MySQL, SQLite, MongoDB, None, etc.)
> - [If applicable] What ORM? (Prisma, Drizzle, TypeORM, SQLAlchemy, None, etc.)"

### Working Preferences

**Ask:**
> "A few questions about how you work:
> 1. What's your development experience level?
>    - New to development (explain concepts in detail)
>    - Some experience (explain new concepts)
>    - Experienced (focus on implementation)
> 2. What OS are you using? (Windows, macOS, Linux)
> 3. Any specific code style preferences? (Or I can use sensible defaults)"

---

## Step 3: GitHub Integration

**Ask:**
> "Would you like to set up GitHub integration for version control?
> A) **Create new repository** - I'll help you create a GitHub repo
> B) **Connect to existing repository** - Link to an existing GitHub repo
> C) **Skip for now** - Set up Git later or manage manually"

### If Option A: Create New Repository

**Ask:**
> "For the new repository:
> 1. Repository name? (I suggest: `[project-name-kebab-case]`)
> 2. Public or Private?"

**Then offer both approaches:**

> "I can set this up two ways. Which do you prefer?
>
> **Option 1 - I run the commands** (type 'run' to confirm):
> ```bash
> git init
> git add .
> git commit -m "Initial commit: Project setup with Claude Code template"
> gh repo create [repo-name] --[public/private] --source=. --remote=origin --push
> ```
>
> **Option 2 - Step-by-step instructions** (type 'manual'):
> I'll give you commands to copy and run yourself."

**If user chooses automated:** Execute the commands after confirmation.

**If user chooses manual:** Provide the commands formatted for easy copying:
```
Run these commands in your terminal:

1. Initialize git:
   git init

2. Stage all files:
   git add .

3. Create initial commit:
   git commit -m "Initial commit: Project setup with Claude Code template"

4. Create GitHub repo and push (requires gh CLI):
   gh repo create [repo-name] --[public/private] --source=. --remote=origin --push

Alternative if you don't have gh CLI:
- Create repo on github.com
- Then run:
  git remote add origin https://github.com/[username]/[repo-name].git
  git push -u origin main
```

### If Option B: Connect to Existing Repository

**Ask:**
> "What's the repository URL? (e.g., https://github.com/username/repo.git)"

**Then offer both approaches:**

> "I can set this up two ways:
>
> **Option 1 - I run the commands** (type 'run'):
> ```bash
> git init
> git remote add origin [repo-url]
> git fetch origin
> git branch -M main
> git pull origin main --allow-unrelated-histories
> ```
>
> **Option 2 - Step-by-step instructions** (type 'manual')"

### If Option C: Skip

Note in CLAUDE.md that GitHub is not configured, and continue.

---

## Step 4: Generate CLAUDE.md

Based on the gathered information, create or update `CLAUDE.md`:

1. **About Me section:** Fill in with user's experience level, OS, and preferences
2. **My Preferences section:** List their tech stack choices
3. **Project Overview:** Project name and description
4. **Tech Stack table:** Populate with their selections

**If this is an existing project with code:**
- Scan the project structure using `ls` and file reads
- Document the actual file structure
- Note any existing features in Current State
- Identify package.json, requirements.txt, etc. for tech stack

**If this is a new/empty project:**
- Set up initial placeholder structure
- Note "Project initialized, no code yet" in Current State

---

## Step 5: Verify Roadmap Structure

Check that these folders exist:
- `roadmap/backlog/`
- `roadmap/planned/`
- `roadmap/in-progress/`
- `roadmap/completed/`

If any are missing, create them with `.gitkeep` files.

**Ask about example file (if it exists):**
> "I see an example roadmap file (`_EXAMPLE_DELETE_ME.md`). Would you like to:
> A) Keep it as a reference
> B) Delete it (recommended for new projects)"

---

## Step 6: Display Completion Message

After everything is set up, display:

```
========================================
  Project initialization complete!
========================================

Files created/updated:
- CLAUDE.md (project configuration)
- roadmap/ (feature planning system)

╔════════════════════════════════════════╗
║  IMPORTANT: Restart your terminal or   ║
║  start a new Claude Code session for   ║
║  slash commands to be active!          ║
╚════════════════════════════════════════╝

Available commands after restart:
  /review   - Start session, see project state
  /planner  - Save planning work before ending
  /builder  - Implement a planned feature
  /debug    - Troubleshoot issues
  /cleanup  - Improve code quality

GitHub status: [Configured: repo-name / Not configured]

Next steps:
1. Close and reopen your terminal (or restart Claude Code)
2. Run: /review
3. Start planning or building!
```

---

## Step 7: Offer Next Actions

**Ask:**
> "What would you like to do next?
> A) I'll run `/review` to show you the project state (after you restart terminal)
> B) Let's plan your first feature
> C) We're done for now (remember to restart your terminal!)"

---

## Rules for Init Agent

1. **Be conversational** - Ask questions naturally, not like a form
2. **Provide defaults** - Suggest sensible options when possible
3. **Confirm before changes** - Always confirm before modifying existing files
4. **Both options for git** - Always offer automated AND manual approaches
5. **Never force push** - Don't run destructive git commands
6. **Explain as needed** - If user seems confused, explain concepts
7. **Terminal restart reminder** - Emphasize this multiple times; commands won't work without it
8. **Be encouraging** - This might be the user's first time setting up a project like this
