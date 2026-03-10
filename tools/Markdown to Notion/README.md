# Markdown to Notion

Syncs markdown files to Notion pages with **smart diffing** – only changed blocks get updated, and comments on unchanged blocks are preserved. Write in markdown, run one command, and your Notion page updates surgically instead of being wiped and rebuilt.

If a block you edited had comments, they're automatically migrated to a gray marker paragraph (e.g. `📄 "original text"`) so nothing is lost.

## Why Keychain?

This tool stores your Notion API key and database ID in **macOS Keychain** – the same secure system that stores your Wi-Fi passwords and website logins.

This means your credentials:

- **Never appear in project files** – no `.env` files, no config files, nothing to accidentally commit to GitHub
- **Never enter Claude Code's context** – even if you run this tool from a Claude Code terminal, the API key is fetched directly from Keychain at runtime, so Claude never sees it
- **Are encrypted at rest** – Keychain encrypts everything and requires your Mac login to access

We intentionally avoid `.env` files. Even with `.gitignore`, it's too easy to accidentally expose credentials. Keychain is the safer default.

> **Note:** This tool is macOS-only because it uses macOS Keychain for credential storage.

---

## Before You Start

Make sure you have:

- [ ] A **Notion account** (free tier works)
- [ ] **Node.js** installed on your Mac – check by running `node --version` in Terminal. If you don't have it, download from [nodejs.org](https://nodejs.org)
- [ ] A **Notion database** you want to upload pages into (you'll create one during setup if you don't have one)

---

## One-time Setup

You only need to do this once. It creates a Notion integration, stores credentials securely, and installs dependencies.

### Step 1: Create a Notion integration

This gives the script permission to read and write to your Notion workspace.

1. Go to [notion.so/profile/integrations](https://www.notion.so/profile/integrations)
2. Click **New integration**
3. Give it a name (e.g. "Markdown Uploader")
4. Select the workspace you want to use
5. Click **Submit**
6. You'll see an **Internal Integration Secret** – it starts with `ntn_`. Copy it somewhere safe for now (you'll store it in Keychain in a moment)

### Step 2: Create a database in Notion (or use an existing one)

The script uploads each markdown file as a page inside a Notion database.

- If you already have a database, skip to Step 3
- To create one: open Notion, create a new page, type `/database` and select **Database – Full page**. Give it any name you like

### Step 3: Connect your integration to the database

Your integration can only access pages you explicitly share with it.

1. Open the database in Notion
2. Click the **`···`** menu in the top-right corner
3. Scroll down to **Connections**
4. Click **Connect to** and search for the integration name you created in Step 1
5. Click **Confirm**

### Step 4: Find your Database ID

The Database ID is the long string of characters in the URL when you open your database.

1. Open the database in Notion (in your browser, not the desktop app)
2. Look at the URL – it looks like:
   ```
   https://www.notion.so/your-workspace/abc123def456...?v=...
   ```
3. The Database ID is the part between the last `/` and the `?` – it's 32 characters long (letters and numbers)
4. Copy it

### Step 5: Store your API key in Keychain

Open **Terminal** (search "Terminal" in Spotlight, or find it in Applications > Utilities) and run:

```bash
security add-generic-password -a "notion" -s "notion-api-key" -w "YOUR_API_KEY_HERE"
```

Replace `YOUR_API_KEY_HERE` with the integration secret from Step 1 (the one starting with `ntn_`). Keep the quotes.

You should see no output – that means it worked.

### Step 6: Store your Database ID in Keychain

In the same Terminal, run:

```bash
security add-generic-password -a "notion" -s "notion-database-id" -w "YOUR_DATABASE_ID_HERE"
```

Replace `YOUR_DATABASE_ID_HERE` with the Database ID from Step 4. Keep the quotes.

Again, no output means success.

### Step 7: Verify both stored correctly

Run these two commands to confirm:

```bash
security find-generic-password -a "notion" -s "notion-api-key" -w
security find-generic-password -a "notion" -s "notion-database-id" -w
```

Each should print back the value you stored. If you see the correct API key and Database ID, you're all set.

### Step 8: Download this folder

Copy this entire `Markdown to Notion` folder to somewhere on your computer (e.g. your Documents folder).

### Step 9: Install dependencies

In Terminal, navigate to the folder and install:

```bash
cd "path/to/Markdown to Notion"
npm install
```

You'll see it install two packages (`@notionhq/client` and `@tryfabric/martian`). This takes a few seconds.

---

## How to Use

Navigate to this folder in Terminal, then run one of three modes:

### Smart sync (recommended)

```bash
node upload.mjs my-document.md
```

- If the page doesn't exist in your database yet, creates it
- If the page already exists, compares block-by-block and only updates what changed
- Comments on unchanged blocks are preserved
- Comments on changed or deleted blocks are migrated to marker paragraphs

### Preview changes (dry run)

```bash
node upload.mjs --dry-run my-document.md
```

Shows you what would change without actually modifying anything in Notion. Useful for checking before you commit to an update.

### Full refresh

```bash
node upload.mjs --refresh my-document.md
```

Wipes the existing page and re-uploads everything from scratch. **This destroys all comments** – use only when you want a clean slate.

---

## How It Works

Here's what happens when you run the script:

1. **Parses your markdown** into Notion block objects (using the [martian](https://github.com/tryfabric/martian) library)
2. **Fetches the existing page** from your Notion database (matched by filename = page title)
3. **Diffs old vs new blocks** using a longest common subsequence (LCS) algorithm – this detects insertions, deletions, and edits without misaligning surrounding content
4. **Fetches comments** only on blocks that are about to be deleted or changed (not the whole page – this keeps API calls low)
5. **Migrates comments** from affected blocks to gray italic marker paragraphs, preserving reply threads
6. **Applies changes**: deletes removed blocks, updates changed blocks in place, appends new blocks at the correct positions

The result: most of your page stays untouched, comments survive, and only the parts you actually changed get updated.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `security: SecKeychainSearchCopyNext: The specified item could not be found in the keychain.` | API key or Database ID not stored in Keychain | Re-run the `security add-generic-password` commands from Steps 5–6 |
| `Could not find database` or `401 Unauthorized` | Integration doesn't have access to the database | Open the database in Notion > `···` > Connections > add your integration (Step 3) |
| `API token is invalid` | Wrong API key stored | Delete and re-add: `security delete-generic-password -a "notion" -s "notion-api-key"` then re-run Step 5 |
| `Rate limited` / `429` errors | Too many requests to Notion API | Wait a minute and try again – the script already uses conservative concurrency, but large pages can hit limits |
| `Could not find page` on update | Page title doesn't match filename | The script matches by filename (without `.md`). Rename your file or the Notion page so they match exactly |
| `npm install` fails | Node.js not installed or outdated | Install Node.js from [nodejs.org](https://nodejs.org) (LTS version recommended) |

---

## Limitations

- **macOS only** – uses macOS Keychain for credential storage. Won't work on Windows or Linux without modification
- **No toggle blocks** – markdown doesn't have a standard toggle/collapsible syntax, so `<details>` tags won't convert
- **Nested blocks replaced wholesale** – if a parent block changes, its children are replaced entirely rather than diffed individually
- **One file at a time** – upload a single markdown file per command (batch upload not yet supported)
- **Rate limits** – Notion's API allows ~3 requests/second. The script uses concurrency pools (5 for reads, 3 for writes) to stay within limits, but very large pages may still hit throttling
- **Some markdown features don't convert** – anything that martian doesn't support (e.g. footnotes, definition lists) will be dropped or simplified
