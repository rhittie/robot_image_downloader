# Debug Agent

You are now in Debug mode. Help troubleshoot and fix issues.

## Gather Information

### 1. Identify the Problem
Ask me:
- What's the error message? (exact text)
- What were you trying to do?
- When did it start happening?
- Did it work before?

### 2. Check the Basics
Before diving deep:
- Is Python running correctly? Check terminal for errors
- Are all dependencies installed? (`pip install -r requirements.txt`)
- Are environment variables set? (GOOGLE_API_KEY, GOOGLE_CX)
- Is the CSV file formatted correctly?

### 3. Common Issues Checklist
Run through these:
- [ ] Dependencies installed? (`pip install -r requirements.txt`)
- [ ] API key valid and has quota?
- [ ] Search engine ID (cx) correct?
- [ ] CSV columns detected correctly?
- [ ] Output directory writable?
- [ ] Network connectivity working?

## Investigate

### 4. Read Relevant Files
Based on the error, read:
- The file mentioned in the error
- Related files that might be affected
- Recent changes (check git status/diff if available)

### 5. Trace the Problem
- Follow the error from where it appears back to the source
- Check data flow: CSV -> API -> Download -> Save
- Look for typos, missing imports, wrong paths

## Fix

### 6. Propose a Solution
Before changing anything:
- Explain what's causing the issue
- Describe the fix
- Ask for approval if it's a significant change

### 7. Apply the Fix
- Make the minimal change needed
- Test that the fix works
- Verify no regressions

### 8. Document
If this was a tricky issue:
- Add it to CLAUDE.md Troubleshooting section
- Note: Symptoms, Cause, Solution

## Rules
- Don't make changes without understanding the problem first
- Explain what you find in plain language
- Ask for more information if the error isn't clear
- Document solutions so we don't solve the same problem twice
