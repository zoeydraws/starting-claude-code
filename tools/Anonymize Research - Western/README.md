# Anonymize Research Data

Removes personally identifiable information (PII) from research files (`.md`, `.txt`, `.csv`, `.xlsx`, `.json`) using Microsoft Presidio. It detects names, emails, phone numbers, locations, company names, and more – and replaces them with labels like `<PERSON_1>`, `<LOCATION>`, `<EMAIL_ADDRESS>`.

People get **numbered labels** so you can still track who said what without exposing real names (e.g. "Jane Doe" becomes `<PERSON_1>` everywhere, including when just "Jane" is mentioned).

## Why a Separate Terminal?

This script should run **outside** of Claude Code. Here's why:

- Claude Code can see everything in the terminal it's running in – including file contents and command output
- If you run this script inside a Claude Code session, Claude would see the raw participant names before they get anonymized
- By running it in a separate terminal, the original data never touches Claude's context

Think of it as a clean room: you process the data in one place, and only bring the cleaned version to Claude.

---

## One-time Setup

You only need to do this once. It installs the libraries the script needs.

1. **Download this folder** to somewhere on your computer (e.g. your Documents folder). Make sure it's **not inside a project folder where Claude Code is running**
2. **Open VS Code** – but don't open it from an existing Claude project. Instead:
   - Open VS Code fresh (`Cmd + Shift + N` for a new window)
   - Go to **File > Open Folder**
   - Navigate to wherever you saved this `Anonymize Research - Western` folder and open it
3. **Open the terminal** in VS Code with `Cmd + J`
4. **Do NOT start Claude Code** in this terminal – this is intentional. You want a plain terminal here
5. **Run these two commands** one at a time (copy-paste each line, press Enter, wait for it to finish before running the next):

   ```bash
   pip3 install presidio-analyzer openpyxl
   ```

   ```bash
   python3 -m spacy download en_core_web_lg
   ```

   The second command downloads a ~500 MB language model – it may take a few minutes depending on your internet.

6. You'll know it worked if both commands finish without errors. If you see a "Successfully installed" message for each, you're good

---

## How to Use

Every time you need to anonymize research files:

1. **Open the `Anonymize Research - Western` folder in VS Code** (same as setup – a fresh window, not your Claude project)
2. **Open the terminal** with `Cmd + J`. Again, do NOT start Claude Code here
3. **Drop your files** (`.md`, `.txt`, `.csv`, `.xlsx`, `.json`) into the `input/` folder. You can do this in Finder or drag them into the VS Code sidebar
4. **Run the script** – type this in the terminal and press Enter:

   ```bash
   python3 anonymize.py
   ```

   You'll see it process each file one by one. This may take a minute depending on file size.

5. **Find your anonymized files** in the `output/` folder. The script also creates an `entity_map.txt` there so you can look up who each `<PERSON_1>`, `<PERSON_2>`, etc. refers to
6. **Copy the anonymized files** from `output/` to wherever your Claude project lives – now they're safe to use with Claude

Your original files in `input/` are never modified.

---

## Tweaking (Optional)

If the script is catching too many false positives (flagging normal words as PII) or missing things, you can adjust two settings.

1. Open `anonymize.py` in VS Code by clicking on it in the sidebar
2. Near the top of the file, you'll see these two sections:

**Sensitivity threshold** (line 69) – controls how aggressively it flags PII:

```python
SCORE_THRESHOLD = 0.4
```

- `0.4` (default) catches more, but may flag some non-PII words
- Change it to `0.7` if you're getting too many false positives
- Just change the number and save the file (`Cmd + S`)

**What types of PII to detect** (lines 52–65) – controls which categories it looks for:

```python
ENTITIES_TO_DETECT = [
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "LOCATION",
    ...
]
```

- To stop detecting a category, delete that line from the list (e.g. remove `"DATE_TIME",` if you want dates to stay visible)
- Save the file (`Cmd + S`) and run the script again
