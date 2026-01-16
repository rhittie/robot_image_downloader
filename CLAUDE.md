# CLAUDE.md - Project Intelligence File

## About Me
- New to development, please explain concepts as you code
- Using Windows with VS Code and Git Bash
- Work at Brasfield & Gorrie on innovation projects
- Prefer step-by-step explanations for new concepts

## My Preferences
- Python for scripting and automation
- Keep code simple and readable
- Prefer standard library when possible
- Clear error messages and user feedback

## Code Quality Standards
- Run linter/tests before completing any task
- Keep files under 200 lines - split if larger
- Keep functions focused on single responsibility
- Use meaningful variable names, not single letters
- Add docstrings to public functions
- Add comments only for complex logic

---

## Project Overview
Robot Image Downloader is a Python CLI tool that batch downloads images of robots from manufacturers using Google's Custom Search API. It prioritizes official images from manufacturer websites before falling back to general web search.

## Tech Stack
| Layer | Technology | Purpose |
|-------|------------|---------|
| Language | Python 3.x | Core application |
| HTTP Client | requests | API calls and image downloads |
| CLI | argparse | Command-line interface |
| Data | CSV (stdlib) | Input data parsing |
| Output | JSON (stdlib) | Download manifest |

## File Structure
```
robot_image_downloader/
├── robot_image_downloader.py  # Main application script
├── requirements.txt           # Python dependencies
├── sample_robots.csv          # Example input data
├── README.md                  # User documentation
├── GOOGLE_API_SETUP.md        # API setup instructions
├── CLAUDE.md                  # This file
├── .gitignore                 # Git ignore rules
├── .claude/
│   ├── commands/              # Custom slash commands
│   │   ├── README.md
│   │   ├── init.md            # Project initialization wizard
│   │   ├── planner.md         # Save planning work
│   │   ├── review.md          # Session orientation
│   │   ├── builder.md         # Feature implementation
│   │   ├── debug.md           # Troubleshooting
│   │   └── cleanup.md         # Code quality
│   ├── tools/                 # External tools
│   │   └── README.md          # Tools documentation
│   └── settings.local.json    # Local Claude settings
└── roadmap/                   # Feature planning
    ├── README.md
    ├── backlog/
    ├── planned/
    ├── in-progress/
    └── completed/
```

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/init` | **First time setup** - Configure project, set up GitHub, generate CLAUDE.md |
| `/review` | Orient to project state and decide what to work on |
| `/planner` | Save all planning work to roadmap files and update CLAUDE.md |
| `/builder` | Start building a feature from the roadmap |
| `/debug` | Troubleshoot and fix issues |
| `/cleanup` | Improve code quality without changing features |

---

## Current State
**Last Updated:** 2026-01-13

**What's Working:**
- [x] CSV parsing with auto-detection of columns
- [x] Google Custom Search API integration
- [x] Image downloading with proper extension handling
- [x] Manufacturer site-first search strategy
- [x] Fallback to general web search
- [x] Rate limiting between requests
- [x] Download manifest (JSON) generation
- [x] CLI with argparse (all options documented)
- [x] Environment variable support for credentials

**What's In Progress:**
- [ ] Nothing currently in progress

**What's Broken:**
- [ ] No known issues

## Completed Features
1. Core image downloader - Initial release - Full functionality

## Next Steps
1. [ ] Add progress bar for large CSV files
2. [ ] Add retry logic for failed downloads
3. [ ] Add image validation (check dimensions, file integrity)
4. [ ] Add logging instead of print statements
5. [ ] Add GUI wrapper (optional)

## Decisions Made
| Decision | Reasoning | Date |
|----------|-----------|------|
| Use requests library | Simple, well-maintained, handles edge cases | Initial |
| Manufacturer site search first | Higher quality official images | Initial |
| Suffix images with _official/_web | Easy to identify image source | Initial |
| JSON manifest for tracking | Machine-readable, easy to parse | Initial |

## Known Issues & Bugs
| Issue | Severity | Status | Notes |
|-------|----------|--------|-------|
| None currently | - | - | - |

## Session Handoff Notes
**Last Session:** 2026-01-16

**What We Were Working On:**
Updating project with new Claude Code template framework

**Where We Left Off:**
- Added `/init` command for project setup wizard
- Added `.claude/tools/` folder with README
- Updated `.claude/settings.local.json` with more permissions
- Updated `.gitignore` with comprehensive ignore rules
- Updated file structure documentation

**What Needs to Happen Next:**
- Run `/review` to start working on features
- Add planned features to roadmap if desired
- Consider setting up Notion sync (optional)

**Important Context:**
This is a working Python CLI tool. Google API credentials required for use.

---

## Troubleshooting Log

### API Key Invalid
**Symptoms:** Error message about invalid API key
**Cause:** Key not set or incorrect
**Solution:** Check GOOGLE_API_KEY env var or --api-key argument

### No Images Found
**Symptoms:** Robot downloads zero images
**Cause:** Robot name not recognized or no indexed images
**Solution:** Try --skip-site-search to search web only

### Rate Limit Exceeded
**Symptoms:** API returns quota error
**Cause:** Exceeded 100 free queries/day
**Solution:** Wait for reset or enable billing

---

## Commands Reference

### Running the Script
```bash
# Basic usage
python robot_image_downloader.py robots.csv ./robot_images --api-key KEY --cx CX

# With more images per robot
python robot_image_downloader.py robots.csv ./images --api-key KEY --cx CX --num 5

# Skip manufacturer site search
python robot_image_downloader.py robots.csv ./images --api-key KEY --cx CX --skip-site-search

# Generate sample CSV
python robot_image_downloader.py --create-sample sample_robots.csv
```

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set credentials (Windows PowerShell)
$env:GOOGLE_API_KEY="your_api_key"
$env:GOOGLE_CX="your_search_engine_id"

# Set credentials (Git Bash)
export GOOGLE_API_KEY="your_api_key"
export GOOGLE_CX="your_search_engine_id"
```

---

## Instructions for Claude

### After EVERY Task (Do This Automatically)
1. Update "Current State" with what's working now
2. Move completed items from "Next Steps" to "Completed Features"
3. Add any new decisions to "Decisions Made"
4. Note any bugs discovered in "Known Issues"
5. Update "File Structure" if new files were created

### When I Request a New Feature
1. Add it to "Next Steps" before starting work
2. Break complex features into smaller subtasks
3. Update "Current State" as you make progress

### Before Context Gets Full or Session Ends
1. Write detailed "Session Handoff Notes"
2. Ensure "Current State" is accurate
3. List specific next actions in "Next Steps"

### When Starting a New Session
1. Read this entire file first
2. Check "Session Handoff Notes" for context
3. Confirm "Current State" matches actual project
4. Ask me if anything is unclear before proceeding

### Code Changes
1. Test script after making changes
2. Verify the app still works
3. Update this file to reflect changes

### If You Get Confused
1. Stop and re-read this file
2. Check git history for recent changes
3. Ask me for clarification
4. Don't guess - verify by reading actual files

---

## Roadmap System

Feature planning lives in the `/roadmap` folder:
- `backlog/` - Ideas and requests not yet planned
- `planned/` - Detailed plans ready to build
- `in-progress/` - Currently being worked on (1-2 max)
- `completed/` - Finished features for reference

### When I Request a New Feature
1. Create a new .md file in `roadmap/backlog/` using the template
2. Ask clarifying questions about requirements
3. When I say "plan this feature", move to `planned/` and fill in:
   - Technical approach
   - Subtasks broken into small steps
   - Files to create/modify
4. Show me the plan and wait for approval
5. Move to `in-progress/` only when I say to start building
6. Move to `completed/` when done

### When I Say "Plan Mode" or "/plan"
1. Do not write any code
2. Only discuss approach, create plans, and organize work
3. Wait for explicit approval before implementing anything

### Organizing Work Priority
Before starting a new task, consider:
1. **Dependencies** - What must be built first?
2. **Continuity** - What shares code with recent work?
3. **Quick wins** - Any small tasks to knock out?
4. **Blockers** - What's blocking other features?

Review `roadmap/planned/` and suggest the most logical next item.

### After Completing Any Feature
1. Move roadmap file to `completed/`
2. Update CLAUDE.md "Current State" section
3. Add to "Completed Features" list
4. Review `planned/` and suggest what's next
5. Ask if I want to start the next item or take a break

### Starting a New Session
1. Check `roadmap/in-progress/` - is something unfinished?
2. Read the Session Log in that file
3. Confirm where we left off before continuing
4. If nothing in progress, review `planned/` and suggest next steps

### Session Handoff
Before ending a long session:
1. Update the Session Log in the current roadmap file
2. List exactly where you stopped
3. Note any blockers or decisions needed
4. Update CLAUDE.md handoff notes

---

## Documenting Features in README.md

When adding or updating features in README.md, use this format:
```
- **Feature Topic** - Description (configurable via `ENV_VARIABLE` or `function_name()`)
```

Each feature entry must include:
1. **Topic** (bold) - Short name for the feature
2. **Description** - What it does and default behavior
3. **Function/Config** - The env variable, config setting, or function that controls it

Examples:
- **Manufacturer site search** - Searches official sites first for better quality (configurable via `--skip-site-search`)
- **Rate limiting** - Adds delay between API calls (configurable via `--delay` argument)

---

## Notion Sync (Optional)

The template includes optional Notion sync for roadmap features. To set up:

1. Clone the sync tool into `.claude/tools/`:
   ```bash
   cd .claude/tools
   git clone https://github.com/rhittie/notion_claude_sync.git
   ```

2. Configure credentials:
   ```bash
   cd notion_claude_sync
   cp .env.example .env
   # Edit .env with your Notion token and database IDs
   ```

3. Install and test:
   ```bash
   npm install
   npm run sync
   ```

See `.claude/tools/README.md` for detailed setup instructions.

---

## Notes
This is a utility tool for the robotics/construction innovation team. Primary use case is gathering reference images for presentations and documentation.
