---
description: Fetch from remote and merge the main branch into current branch
---

Sync current branch with the main branch.

## Steps

1. Check for uncommitted changes with `git status`
2. If there are uncommitted changes, warn the user and stop
3. Run `git fetch origin`
4. Identify the main branch (usually `main` or `develop`)
5. Run `git merge origin/<main-branch>`
6. Report the result

## Important

- If there are uncommitted changes, warn and stop — don't proceed
- If there are merge conflicts, list the conflicting files and stop
- Do not auto-resolve conflicts — let the user decide
