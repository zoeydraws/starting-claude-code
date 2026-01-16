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

## Step 3: Open the Terminal in VS Code

**What is the Terminal?**
The Terminal is where you type commands instead of clicking buttons. VS Code has one built in, so you don't need to open a separate app.

**How to open it:**
- Press `Cmd + J`
- Or go to `View` → `Terminal`

**What you'll see:**
A panel appears at the bottom of VS Code with text like:
```
yourname@MacBook project-folder %
```

This is called the "command line" or "prompt". It's waiting for you to type something.

**Important:** The terminal automatically starts in your project folder (the one you opened in Step 2). This saves you from navigating manually.

---

## Step 4: Install Claude Code

**What we're doing:**
Running a command that downloads and installs Claude Code automatically.

**Type this command in the Terminal and press Enter:**
```
npm install -g @anthropic-ai/claude-code
```

**Wait, what's npm?**
npm is a tool that installs programs. If you see an error like `command not found: npm`, you need to install Node.js first. See the Troubleshooting section below.

**What you'll see during installation:**
- Several lines of text scrolling by
- It might take 1-2 minutes
- When done, you'll see your prompt again (`yourname@MacBook project-folder %`)

---

## Step 5: Start Claude Code

**Type this and press Enter:**
```
claude
```

**What you'll see:**
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

**You're ready to use Claude Code!** The remaining steps are optional but useful. Head to [2_FIRST_SESSION.md](2_FIRST_SESSION.md) when you're ready.

---

## Step 6: Keep Personal Files Out of Git

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

## Step 7: Set Up GitHub + Vercel for Auto-Deploy

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

See [5_SLASH_COMMANDS.md](5_SLASH_COMMANDS.md) for more on the `/commit` shortcut.

---

## Troubleshooting

### "command not found: npm"

You need to install Node.js first:

1. Go to https://nodejs.org
2. Download the "LTS" version (the one that says "Recommended")
3. Open the downloaded file and follow the installer
4. **Important:** Close VS Code completely and reopen it (the terminal needs to refresh)
5. Open your project folder again, open the Terminal, and try the `npm install` command again

### "permission denied" or "EACCES" errors

This usually means Node.js wasn't installed correctly. The easiest fix:

1. Uninstall Node.js (find it in Applications and drag to Trash)
2. Install Node using Homebrew instead:
   - First install Homebrew by pasting this in Terminal:
     ```
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Then install Node:
     ```
     brew install node
     ```
3. Close VS Code completely and reopen it
4. Try the `npm install -g @anthropic-ai/claude-code` command again

**What is Homebrew?** It's a popular tool for installing software on macOS. It sets up permissions correctly so you won't hit these errors.

### Claude Code won't start

Make sure you're connected to the internet. Claude Code needs to connect to Anthropic's servers.

### Terminal shows wrong folder

If your terminal prompt doesn't show your project folder name, the terminal might have opened before you selected a folder. Close the terminal panel (click the X) and reopen it with `Cmd + J`.

### "I don't know what folder to use"

Start with any folder that has documents you're working on. You can always close Claude Code (`Ctrl + C`) and open VS Code with a different folder.

---

## Working with Multiple Projects

Each VS Code window can only be in one folder at a time. To switch projects:

1. `File` → `Open Folder...`
2. Choose a different folder
3. The terminal will automatically switch to that folder
4. Type `claude` to start Claude Code in the new project

Or open a second VS Code window (`File` → `New Window`) to work on multiple projects at once.
