# Setup Guide

This guide walks you through installing Claude Code on macOS (the operating system on Mac computers) using VS Code. Every step includes what you'll see on screen so you know you're on track.

## Step 1: Install VS Code (if you don't have it)

**What is VS Code?**
VS Code (Visual Studio Code) is a free text editor made by Microsoft. It's popular for writing code, but it's also great for editing markdown files, documentation, and research notes. Most importantly, it has a built-in Terminal — which is where we'll run Claude Code.

**How to install:**
1. Go to https://code.visualstudio.com
2. Click the big "Download for macOS" button (it may say "Download for Mac")
3. Open the downloaded file
4. Drag VS Code to your Applications folder
5. Open VS Code from Applications

**Already have VS Code?** Skip to Step 2.

---

## Step 2: Open Your Project Folder in VS Code

**What is a "project folder"?**
Any folder with files you want to work on. This could be a research project, a folder of transcripts, documentation — anything.

**How to open a folder:**
1. In VS Code, go to `File` → `Open Folder...` (or press `Cmd + O`)
2. Navigate to the folder you want to work in
3. Click `Open`

**What you'll see:**
Your folder's files appear in the left sidebar. You can click any file to view or edit it.

**Don't have a project yet?** Create a new folder on your Desktop and open that. You can always switch later.

---

## Step 3: Install Claude Code

There are two ways to install Claude Code. Pick whichever feels easier for you.

### Option 1: Install via Terminal (Recommended)

This is the official recommended method. It auto-updates in the background, so you always have the latest version.

**First, open the Terminal:** Press `Cmd + J` or go to `View` → `Terminal`

**Type this command and press Enter:**
```
curl -fsSL https://claude.ai/install.sh | bash
```

**What's happening?**
This downloads and runs the official Claude Code installer from Anthropic.

**What you'll see during installation:**
- Several lines of text scrolling by
- It might take 1-2 minutes
- When done, you'll see your prompt again (`yourname@MacBook project-folder %`)

**Verify it worked:**
```
claude --version
```

### Option 2: Install via VS Code Extension

If the terminal method doesn't work for you, you can install Claude Code as a VS Code extension.

**How to install:**
1. In VS Code, click the **Extensions** icon in the left sidebar (it looks like four squares)
2. Search for "Claude Code"
3. Click **Install** on the official Anthropic extension
4. Wait for the installation to complete

---

## Step 4: Start Claude Code

How you start Claude Code depends on how you installed it.

### Option 1: Click the Claude Icon (Extension Install)

If you installed via the VS Code extension, look for the **Claude icon** in the sidebar (left or right side, depending on your VS Code layout). Click it to open Claude Code.

### Option 2: Type `claude` in Terminal (Terminal Install)

If you installed via terminal, open the Terminal (`Cmd + J` or `View` → `Terminal`) and type:
```
claude
```

---

**What you'll see (both options):**

Claude Code will start and ask you to log in. It will show something like:
```
Welcome to Claude Code!
Please authenticate to continue...
```

Follow the prompts to:
1. Open a browser link (it may open automatically)
2. Log into your Anthropic account (or create one)
3. Authorize Claude Code

Once authenticated, you'll see Claude's prompt ready for input.

**You're ready to use Claude Code!** Head to [2_FIRST_SESSION.md](2_FIRST_SESSION.md) when you're ready. The bonus sections below are optional but useful.

---

## Bonus 1: Keep Personal Files Out of Git

**What is .gitignore?**
A file that tells Git "don't track these files." Useful for personal notes, local config, or anything you don't want shared when you push to GitHub.

**How to create one:**
1. In your project folder, create a file called `.gitignore` (note the dot at the start)
2. Add filenames or patterns, one per line

**Example .gitignore:**
```
SESSION_LOG.md
CLAUDE.md
.env
notes/
```

**Common files to ignore:**
- `SESSION_LOG.md` / `CLAUDE.md` — personal project notes
- `.env` — files with passwords or API keys
- `node_modules/` — installed packages (can be reinstalled)
- `.DS_Store` — macOS system files

**Already tracking a file you want to ignore?**
Adding it to .gitignore won't stop tracking it. Ask Claude:
```
Remove SESSION_LOG.md from git tracking but keep the file
```

---

## Bonus 2: Set Up GitHub + Vercel for Auto-Deploy

**What is this?**
If you're building a website or app, you can connect your project to GitHub and Vercel so that every time you commit, your site automatically updates.

**Note:** This works well for simple projects — static sites, portfolios, documentation, basic web apps. Projects with complicated backends or external services may need a different setup.

**What you need:**
- A GitHub account (free at github.com)
- A Vercel account (free at vercel.com)

**How to set it up:**
Ask Claude to help you. Try:
```
Help me set up this project with GitHub and connect it to Vercel for auto-deploy
```

Claude will walk you through each step and run the commands for you.

**Once it's set up:**
```
You: commit

Claude: [pushes to GitHub]

Vercel: [auto-deploys your site]
```

See [5_SPEED_UP_WORKFLOW.md](5_SPEED_UP_WORKFLOW.md) for more on shortcuts and skills.

---

## Troubleshooting

### "command not found: curl"

This is rare on macOS, but if you see this error:

1. Open **Terminal** (find it in Applications → Utilities)
2. Install Xcode Command Line Tools:
   ```
   xcode-select --install
   ```
3. Follow the prompts to install
4. Try the installation command again

### Installation seems stuck

The installer might be waiting for input. Try:
1. Press Enter a few times
2. If still stuck, press `Ctrl + C` to cancel and try again

### "permission denied" errors

Try running the installer with sudo (you'll need to enter your Mac password):
```
curl -fsSL https://claude.ai/install.sh | sudo bash
```

### Claude Code won't start

Make sure you're connected to the internet. Claude Code needs to connect to Anthropic's servers.

### "command not found: claude" after installation

The terminal might not have refreshed. Try:
1. Close VS Code completely and reopen it
2. Or type `source ~/.zshrc` (or `source ~/.bashrc`) to refresh your terminal
3. Try `claude` again

### Terminal shows wrong folder

If your terminal prompt doesn't show your project folder name, the terminal might have opened before you selected a folder. Close the terminal panel (click the X) and reopen it with `Cmd + J`.

### "I don't know what folder to use"

Start with any folder that has documents you're working on. You can always close Claude Code (`Ctrl + C`) and open VS Code with a different folder.

### Check your installation

Run this command to verify Claude Code is installed correctly:
```
claude doctor
```

This shows your installation type, version, and checks for common issues.

---

## Working with Multiple Projects

Each VS Code window can only be in one folder at a time. To switch projects:

1. `File` → `Open Folder...`
2. Choose a different folder
3. The terminal will automatically switch to that folder
4. Type `claude` to start Claude Code in the new project

Or open a second VS Code window (`File` → `New Window`) to work on multiple projects at once.
