# Claude Code Tools

This directory contains external tools integrated into this project.

## notion_claude_sync

Syncs project roadmap features to Notion Kanban boards.

### Quick Setup

1. **Configure Notion credentials:**
   ```bash
   cd .claude/tools/notion_claude_sync
   cp .env.example .env
   # Edit .env with your Notion token and database IDs
   ```

2. **Install dependencies:**
   ```bash
   cd .claude/tools/notion_claude_sync
   npm install
   ```

3. **Create roadmap structure** in your project root:
   ```
   roadmap/
   ├── backlog/
   ├── planned/
   ├── in-progress/
   └── completed/
   ```

4. **Test the sync manually:**
   ```bash
   cd .claude/tools/notion_claude_sync
   npm run sync
   ```

### Auto-Sync on Push

A Git hook has been installed at `.git/hooks/pre-push` that automatically runs the Notion sync whenever you `git push`.

The hook will:
- Check if the tool is configured (has `.env`)
- Install dependencies if needed
- Run the sync before pushing
- Log results to `notion-sync.log`

**Note:** The hook won't block your push if the sync fails - it will just log the error.

### Getting Notion Credentials

1. Go to https://www.notion.so/my-integrations
2. Create a new integration (or use existing)
3. Copy the Integration Token
4. Create two databases in Notion (Projects and Features) - see full README
5. Share both databases with your integration
6. Copy the database IDs from the URLs

For detailed setup instructions, see `.claude/tools/notion_claude_sync/README.md`
