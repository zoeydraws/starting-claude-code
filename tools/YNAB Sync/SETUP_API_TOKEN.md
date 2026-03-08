# Setting Up YNAB API Token (Securely)

This guide stores your YNAB API token in macOS Keychain so it never appears in any project file.

---

## Step 1: Get Your YNAB API Token

1. Open your web browser
2. Go to https://app.ynab.com/settings/developer
3. Log in if needed
4. Click **"New Token"**
5. Enter your YNAB password when asked
6. You'll see a long string of random letters and numbers — that's your token
7. **Copy it now** (highlight it, then Cmd+C) — you won't be able to see it again!

---

## Step 2: Store the Token in macOS Keychain

> **What is Keychain?** It's the built-in password manager on your Mac — the same thing that saves your Wi-Fi passwords. We're putting your token there so it stays safe.

1. In **VSCode**, look at the bottom of the screen — you should see a panel called **Terminal**
   - If you don't see it: click the menu **Terminal → New Terminal** (at the top of VSCode)
2. Click inside the Terminal panel so your cursor is there
3. Copy-paste this command and press **Enter**:

```bash
security add-generic-password -a "$USER" -s "ynab-api-token" -w
```

4. It will ask: `password data for new item:` — **paste your API token** here (Cmd+V) and press **Enter**
   - NOTE: You won't see anything appear when you paste — that's normal! It hides it for security. Just paste and hit Enter.

5. To check it saved correctly, copy-paste this command and press **Enter**:

```bash
security find-generic-password -a "$USER" -s "ynab-api-token" -w
```

6. You should see your token printed back. If you do, it worked!

---

## Step 3: Make Your Terminal Load the Token Automatically

> **What does this step do?** Every time you open a new terminal, your Mac needs to know where to find the token. This step tells it: "go grab the token from Keychain every time I open a terminal."

1. In the **same VSCode Terminal**, copy-paste this command and press **Enter**:

```bash
echo '' >> ~/.zshrc && echo 'export YNAB_API_TOKEN=$(security find-generic-password -a "$USER" -s "ynab-api-token" -w 2>/dev/null)' >> ~/.zshrc
```

> **What just happened?** You added a line to a hidden settings file called `.zshrc`. This file runs automatically every time you open a terminal. The line you added tells the terminal to fetch your token from Keychain.

2. Now tell your current terminal to reload that settings file. Copy-paste this and press **Enter**:

```bash
source ~/.zshrc
```

3. Check that it worked. Copy-paste this and press **Enter**:

```bash
echo $YNAB_API_TOKEN
```

4. You should see your token printed. If you do, this step is done!

---

## Step 4: Create Your config.yaml

1. In the **same VSCode Terminal**, copy-paste this and press **Enter**:

```bash
cp config.example.yaml config.yaml
```

2. That's it! The config file is already set up to read from the token you just stored.

> **Important:** If you open `config.yaml` and see `"${YNAB_API_TOKEN}"` — **leave it as-is**. Do NOT replace it with your actual token. It's supposed to look like that — it's a reference that says "go get the token from the environment."

---

## Step 5: Test That Everything Works

1. In the **VSCode Terminal**, copy-paste this and press **Enter**:

```bash
ynab-sync ynab-accounts
```

2. If you see a list of your YNAB budgets and accounts, **you're all set!**

---

## Troubleshooting

**"command not found: ynab-sync"** — The CLI tool isn't installed yet. Ask for help installing it.

**The `echo $YNAB_API_TOKEN` command shows nothing** — Try closing your terminal completely and opening a new one (Terminal → New Terminal in VSCode), then try `echo $YNAB_API_TOKEN` again.

**"security: SecKeychainSearchCopyNext: The specified item could not be found"** — The token wasn't saved to Keychain. Go back to Step 2 and try again.

---

## If Your Token Stops Working (401 Unauthorized Error)

This means your token has expired or is no longer valid. You need to get a new one from YNAB and replace the old one. Follow these steps:

### 1. Get a new token from YNAB

1. Open your web browser
2. Go to https://app.ynab.com/settings/developer
3. Log in if needed
4. Click **"New Token"**
5. Enter your YNAB password when asked
6. You'll see a long string of random letters and numbers — that's your new token
7. **Copy it now** (highlight it, then Cmd+C) — you won't be able to see it again!

### 2. Delete the old token from Keychain

1. Open **Terminal** in VSCode (if you don't see it: click the menu **Terminal → New Terminal** at the top)
2. Copy-paste this command and press **Enter**:

```bash
security delete-generic-password -a "$USER" -s "ynab-api-token"
```

3. You should see a message like `password has been deleted`. That's good!

### 3. Save the new token to Keychain

1. Copy-paste this command and press **Enter**:

```bash
security add-generic-password -a "$USER" -s "ynab-api-token" -w
```

2. It will ask: `password data for new item:` — **paste your new API token** (Cmd+V) and press **Enter**
   - NOTE: You won't see anything appear when you paste — that's normal! It hides it for security. Just paste and hit Enter.

### 4. Reload your terminal

1. Copy-paste this command and press **Enter**:

```bash
source ~/.zshrc
```

### 5. Test that it works

1. Copy-paste this command and press **Enter**:

```bash
ynab-sync ynab-accounts
```

2. If you see your YNAB budgets and accounts listed, you're good to go!
3. If you still get an error, try closing the terminal completely (**Terminal → Kill Terminal** in VSCode) and opening a new one (**Terminal → New Terminal**), then try the test command again.

---

## If You Need to Delete the Token Entirely

```bash
security delete-generic-password -a "$USER" -s "ynab-api-token"
```

Then remove the `export YNAB_API_TOKEN=...` line from `~/.zshrc` (ask for help if you're unsure how).
