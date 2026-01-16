# Planner Agent

You are now in Planner mode. Your job is to save all planning work before this session ends.

## Do the following steps in order:

### 1. Review the Conversation
Look through our conversation for any features, ideas, or plans we discussed that haven't been saved to files yet.

### 2. Create/Update Roadmap Files
For each feature discussed:
- If it's a new idea -> Create file in `roadmap/backlog/` using the `_TEMPLATE.md` format
- If we planned it in detail -> Create/move file to `roadmap/planned/` with full technical approach
- If work has started -> Update the file in `roadmap/in-progress/`
- If it's complete -> Move to `roadmap/completed/`

Each roadmap file MUST have these sections filled in (not placeholder text):
- **Description**: What this feature does
- **Requirements**: Specific checkboxes of what's needed
- **Technical Approach**: How it will be built
- **Subtasks**: Numbered steps to complete the work
- **Files to Create/Modify**: Specific file paths affected
- **Notes**: Any decisions or context from our discussion

Use numbered prefixes for files: `001-feature-name.md`, `002-feature-name.md`, etc.

### 3. Update CLAUDE.md

**Current State section:**
- What features are working now
- What's partially complete
- What's broken or blocked

**Completed Features section:**
- Add any features we finished this session

**Next Steps section:**
- Prioritized list based on roadmap/planned/
- Consider dependencies (what must be built first)
- Note any blockers

**Decisions Made section:**
- Add any architectural or technical decisions from this session

**Session Handoff Notes section:**
- Date of this session
- What we discussed and planned
- Where we left off
- Specific next actions for the next session
- Any context the next session needs to know

### 4. Verify Completeness
For each roadmap file created/updated, confirm:
- [ ] Technical approach is specific, not generic
- [ ] Subtasks are small enough to complete in one step
- [ ] A fresh session could build this without extra context

### 5. Report Summary
List all files created or updated:
```
Created:
- roadmap/backlog/xxx.md
- roadmap/planned/xxx.md

Updated:
- CLAUDE.md
- roadmap/in-progress/xxx.md
```

Ask me to verify the files before I clear the session.

## Rules
- Do NOT write any application code
- ONLY create/update planning and documentation files
- Ask clarifying questions if any plans are unclear before saving
- If unsure about priority or complexity, ask me
