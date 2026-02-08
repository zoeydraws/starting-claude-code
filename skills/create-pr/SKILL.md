---
name: create-pr
description: Rebase onto main, resolve conflicts, force push, and create a pull request
---

Prepare and create a pull request with a clean commit history.

## Steps

1. **Check status**: Run `git status` - warn if uncommitted changes
2. **Fetch latest**: Run `git fetch origin`
3. **Identify main branch**: Check if `develop` exists, otherwise use `main`
4. **Rebase**: Run `git rebase origin/<main-branch>`
5. **Handle conflicts**: If conflicts occur:
   - List conflicting files
   - Walk user through each conflict manually
   - After user resolves, run `git add <file>` then `git rebase --continue`
   - Repeat until rebase completes
6. **Force push**: Run `git push --force` (required after rebase)
7. **Create PR**: Run `gh pr create` with title and description

## Conflict Resolution

- Show the conflicting files clearly
- Do NOT auto-resolve - let user decide
- After user says "done" or "continue", stage resolved files and continue rebase
- If user wants to abort, run `git rebase --abort`

## Important

- Always rebase before creating PR to ensure clean history
- Force push is expected and safe on feature branches after rebase
- Use `gh pr create` with clear title and description summarizing changes
