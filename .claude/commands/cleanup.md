# Cleanup Agent

You are now in Cleanup mode. Improve code quality without changing functionality.

## Before Starting

### 1. Confirm Scope
Ask me:
- Full project cleanup or specific file?
- Any areas I'm concerned about?
- Anything to leave alone?

### 2. Check Current State
- Make sure the script works before cleanup
- Note any existing issues

## Analysis Phase

### 3. Scan for Issues
Look for:

**Code Quality**
- [ ] Files over 200 lines (should be split)
- [ ] Functions over 50 lines (should be broken down)
- [ ] Duplicate code (should be extracted)
- [ ] Unused imports or variables
- [ ] Print statements that should be logging
- [ ] Commented-out code blocks

**Organization**
- [ ] Functions in wrong order
- [ ] Inconsistent naming conventions
- [ ] Related code spread across functions
- [ ] Missing docstrings on public functions

**Python Best Practices**
- [ ] Type hints missing
- [ ] Magic numbers that should be constants
- [ ] Error handling too broad (bare except)
- [ ] Resource cleanup (context managers)

**Documentation**
- [ ] Complex functions without comments
- [ ] Missing README sections
- [ ] Outdated comments

### 4. Report Findings
List what you found organized by priority:

**High Priority** (causes problems)
- List issues...

**Medium Priority** (improves maintainability)
- List issues...

**Low Priority** (nice to have)
- List issues...

Ask which priorities I want to address.

## Cleanup Phase

### 5. Fix Issues
For each issue:
- Make the change
- Verify the script still works
- Test the fix

### 6. Don't Break Things
Rules:
- No feature changes, only refactoring
- Test the script after major refactors
- Keep changes focused and reviewable

## After Cleanup

### 7. Final Verification
- Run the script with sample data
- Verify all features work exactly as before

### 8. Report Changes
Summarize:
- Files modified
- What was cleaned up
- Any issues you chose not to fix (and why)

### 9. Update Documentation
- Update CLAUDE.md if structure changed
- Update roadmap files if relevant

## Rules
- Don't change how features work
- Small, incremental changes
- Test after each change
- Ask before major refactors
- Leave code better than you found it
