# Markdown to Notion

Syncs markdown files to Notion pages with **smart diffing** – only changed blocks get updated, and comments on unchanged blocks are preserved. Write in markdown, run one command, and your Notion page updates surgically instead of being wiped and rebuilt.

If a block you edited had comments, they're automatically migrated to a gray marker paragraph (e.g. `📄 "original text"`) so nothing is lost.

> **Note:** This tool is macOS-only because it uses macOS Keychain for credential storage.

---

## Before You Start

You need to do a few things in Notion's website first. Claude can't do these for you because they require logging into your Notion account in a browser.

### 1. Create a Notion integration

This gives the script permission to read and write to your Notion workspace.

1. Go to [notion.so/profile/integrations](https://www.notion.so/profile/integrations)
2. Click **New integration**
3. Give it a name (e.g. "Markdown Uploader")
4. Select the workspace you want to use
5. Click **Submit**
6. You'll see an **Internal Integration Secret** – it starts with `ntn_`. Copy it somewhere safe for now

### 2. Create a database in Notion (or use an existing one)

The script uploads each markdown file as a page inside a Notion database.

- If you already have a database, skip to step 3
- To create one: open Notion, create a new page, type `/database` and select **Database – Full page**. Give it any name you like

### 3. Connect your integration to the database

Your integration can only access pages you explicitly share with it.

1. Open the database in Notion
2. Click the **`···`** menu in the top-right corner
3. Scroll down to **Connections**
4. Click **Connect to** and search for the integration name you created in step 1
5. Click **Confirm**

### 4. Find your Database ID

The Database ID is the long string of characters in the URL when you open your database.

1. Open the database in Notion (in your browser, not the desktop app)
2. Look at the URL – it looks like:
   ```
   https://www.notion.so/your-workspace/abc123def456...?v=...
   ```
3. The Database ID is the part between the last `/` and the `?` – it's 32 characters long (letters and numbers)
4. Copy it

### 5. Store your credentials in Keychain

This stores your API key and database ID in **macOS Keychain** – the same secure system that stores your Wi-Fi passwords. Your credentials never appear in project files and never enter Claude Code's context (Keychain fetches happen at runtime).

Give Claude Code this prompt:

```
Store my Notion credentials in macOS Keychain. Run these two commands, replacing the placeholder values with the real ones I provide:

security add-generic-password -a "notion" -s "notion-api-key" -w "MY_API_KEY"
security add-generic-password -a "notion" -s "notion-database-id" -w "MY_DATABASE_ID"

My API key is: [paste your ntn_ key here]
My database ID is: [paste your 32-character ID here]

Then verify both stored correctly by running:

security find-generic-password -a "notion" -s "notion-api-key" -w
security find-generic-password -a "notion" -s "notion-database-id" -w
```

You should see both values printed back. If so, you're all set.

---

## Setup

Once your credentials are in Keychain, give Claude Code this prompt to install dependencies:

```
Install the dependencies for the Markdown to Notion tool. Navigate to the tool folder and run npm install:

cd "path/to/Markdown to Notion"
npm install
```

Replace `path/to/` with wherever you saved this folder. It installs two packages (`@notionhq/client` and `@tryfabric/martian`) – takes a few seconds.

---

## How to Use

Tell Claude Code to sync a file. Here are the three modes:

**Smart sync (recommended):**

```
Sync my-document.md to Notion using the Markdown to Notion tool:

cd "path/to/Markdown to Notion" && node upload.mjs path/to/my-document.md
```

- If the page doesn't exist in your database yet, creates it
- If the page already exists, compares block-by-block and only updates what changed
- Comments on unchanged blocks are preserved
- Comments on changed or deleted blocks are migrated to marker paragraphs

**Preview changes (dry run):**

```
Preview what would change without actually updating Notion:

cd "path/to/Markdown to Notion" && node upload.mjs --dry-run path/to/my-document.md
```

Shows what would change without modifying anything. Useful for checking before you commit.

**Full refresh:**

```
Wipe and re-upload my-document.md to Notion from scratch:

cd "path/to/Markdown to Notion" && node upload.mjs --refresh path/to/my-document.md
```

Replaces everything on the page. **This destroys all comments** – use only when you want a clean slate.

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
| `security: SecKeychainSearchCopyNext: The specified item could not be found in the keychain.` | API key or Database ID not stored in Keychain | Re-run the `security add-generic-password` commands from step 5 |
| `Could not find database` or `401 Unauthorized` | Integration doesn't have access to the database | Open the database in Notion > `···` > Connections > add your integration (step 3) |
| `API token is invalid` | Wrong API key stored | Delete and re-add: `security delete-generic-password -a "notion" -s "notion-api-key"` then re-run step 5 |
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
