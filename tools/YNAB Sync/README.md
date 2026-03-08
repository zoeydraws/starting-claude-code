# YNAB Sync

Automatically upload your bank transactions to YNAB.

---

## What This Does

Instead of manually entering transactions in YNAB, you can:
1. Download your bank statement
2. Put it in a folder
3. Run one command
4. Your transactions appear in YNAB

---

## One-Time Setup (Do This Once)

### Step 1: Get permission from YNAB

You need to tell YNAB it's okay for this tool to add transactions.

1. Open YNAB in your browser: https://app.ynab.com
2. Click your name in the top-left corner
3. Click **Account Settings**
4. Scroll down and find **Developer Settings**
5. Click **New Token**
6. Type your YNAB password
7. Click **Generate**
8. You'll see a long code - **copy it and save it somewhere safe**
   (You won't be able to see it again!)

### Step 2: Install the tool

Open Terminal and type:

```
git clone https://github.com/YOUR_USERNAME/ynab-sync.git
cd ynab-sync
pip install -e .
```

### Step 3: Create your config file

```
cp config.example.yaml config.yaml
```

### Step 4: Add your YNAB token

1. Open `config.yaml` in any text editor (TextEdit, VS Code, etc.)

2. Find this line:
   ```
   api_token: "PASTE_YOUR_TOKEN_HERE"
   ```

3. Replace `PASTE_YOUR_TOKEN_HERE` with the code you copied in Step 1:
   ```
   api_token: "your-actual-code-here"
   ```

4. Save the file

### Step 5: Test it works

```
ynab-sync ynab-accounts
```

If it shows your YNAB accounts, you're all set!

---

## How to Use (Every Time)

### Step 1: Download your bank statements

Go to each bank's website and download your transactions:

| Bank | What to download |
|------|------------------|
| DBS | CSV file |
| Citibank | CSV file |
| UOB | Excel file (.xls) |
| Wise | CSV file |

### Step 2: Put files in the inbox folder

Move all the downloaded files into the `inbox/` folder in this project.

### Step 3: Run the upload

Open Terminal, go to the project folder, and run:

```
ynab-sync run
```

The tool will:
- Figure out which bank each file is from
- Send the transactions to the right YNAB account
- Skip any transactions that are already in YNAB

### Want to preview first?

If you want to see what will be uploaded (without actually uploading):

```
ynab-sync run --dry-run
```

### Need to re-import transactions?

If you see "0 new, X duplicates" but want to force the transactions through (e.g. you deleted them from YNAB and need to re-import):

```
ynab-sync run --force
```

This skips duplicate detection so YNAB will accept all transactions, even if they were previously imported. **Use with care** — it will create duplicates if the transactions already exist in YNAB.

---

## Setting Up Your Accounts

Your `config.yaml` file tells the tool which bank accounts match which YNAB accounts.

Here's what each bank is called in the config:

| Your Bank Account | Put this in config |
|-------------------|-------------------|
| DBS savings/checking | `dbs` |
| UOB savings (One Account) | `uob-bank` |
| UOB ONE credit card | `uob-one-cc` |
| UOB Preferred Platinum Visa | `uob-ppv-cc` |
| UOB Lady's Solitaire card | `uob-ladies-cc` |
| Citibank Premier card | `citi-premier-cc` |
| Citibank Shared card | `citi-shared-cc` |
| Wise | `wise` |

---

## Citibank: Card Number Setup

Citibank CSVs include the full card number in the file. The tool uses the **last 4 digits** to figure out which Citibank account each file belongs to.

You need to update the card map in `ynab_sync/parsers/citibank.py` with your own card numbers:

```python
CITIBANK_CARD_MAP = {
    "0000": "citi-premier-cc",    # Replace 0000 with your card's last 4 digits
    "1111": "citi-shared-cc",     # Replace 1111 with your card's last 4 digits
    "2222": "citi-shared-cc",     # Remove or add entries as needed
}
```

The values (`citi-premier-cc`, `citi-shared-cc`) must match the `bank` field in your `config.yaml`.

> **Why is this needed?** Other banks (UOB, DBS, Wise) include the account type in their export files, so the tool can auto-detect them. Citibank doesn't — it only includes the card number, so you need to tell the tool which card belongs to which account.

---

## Common Problems

**"No config file found"**
> Make sure you created `config.yaml` (Step 3 in setup)

**"YNAB API error: 401"**
> Your YNAB code is wrong. Go back to Step 1 and get a new one.

**"Could not detect bank type"**
> You downloaded the wrong file type. Check the table above - UOB needs Excel, others need CSV.

**"No account configured"**
> You need to add this account to your `config.yaml` file.
