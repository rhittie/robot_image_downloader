# Builder Agent

You are now in Builder mode. Time to implement a feature from the roadmap.

## Before Starting

### 1. Confirm the Target
Check `roadmap/in-progress/` first:
- If a file exists there, confirm I want to continue that work
- If empty, ask which item from `roadmap/planned/` to build

### 2. Move to In-Progress
- Move the roadmap file from `planned/` to `in-progress/`
- Update the Status section with today's date for "Started"

### 3. Review the Plan
Read the roadmap file and confirm:
- Technical approach is clear
- Subtasks are defined
- Files to modify are listed

If anything is unclear, ask before proceeding.

## During Building

### 4. Work Through Subtasks
- Follow the subtasks in order
- Check off each subtask as you complete it (change `[ ]` to `[x]`)
- Update the Session Log after completing each major subtask
- Run linter/tests after changes

### 5. Test as You Go
- Verify each piece works before moving to the next
- Note any issues in the roadmap file's Notes section

### 6. Handle Problems
If you hit a blocker:
- Document it in the roadmap file
- Ask me how to proceed
- Don't guess or work around it silently

## After Completing

### 7. Finalize
When all subtasks are done:
- Move roadmap file to `completed/`
- Update Status with completion date
- Update `CLAUDE.md`:
  - Add to Completed Features
  - Update Current State
  - Update Next Steps
- Run full test suite
- Confirm everything works

### 8. Report Completion
Summarize:
- What was built
- Files created/modified
- Any notes or follow-up items

Ask if I want to:
- Start the next planned feature
- Take a break
- Review what was built

## Rules
- Follow the roadmap plan closely
- Update the roadmap file as you work
- Ask before deviating from the plan
- Don't skip testing steps
- Keep CLAUDE.md in sync with actual state
