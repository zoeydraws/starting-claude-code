# Anonymize Research Data

Removes personally identifiable information (PII) from research files (`.md`, `.txt`, `.csv`, `.xlsx`, `.json`) using Microsoft Presidio. It detects names, emails, phone numbers, locations, company names, and more – and replaces them with labels like `<PERSON_1>`, `<LOCATION>`, `<EMAIL_ADDRESS>`.

People get **numbered labels** so you can still track who said what without exposing real names (e.g. "Jane Doe" becomes `<PERSON_1>` everywhere, including when just "Jane" is mentioned).

The script uses a **multilingual transformer model** that recognizes diverse names (Malay, Chinese, Indian, Arabic, etc.), plus a **two-pass system** – if a name is detected on any line, a cleanup pass catches any remaining occurrences the model missed (including possessives like "Jane's").

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
   - Navigate to wherever you saved this `anonymize-research` folder and open it
3. **Open the terminal** in VS Code with `Cmd + J`
4. **Do NOT start Claude Code** in this terminal – this is intentional. You want a plain terminal here
5. **Install all dependencies** – copy-paste this into the terminal and press Enter (it's one long command):

   ```bash
   pip3 install 'presidio-analyzer[transformers]' openpyxl protobuf sentencepiece 'transformers<4.57' && python3 -m spacy download en_core_web_sm
   ```

   This installs everything the script needs in one go. It may take a few minutes.

6. **Choose a language model** – this is what detects names in your files. Pick the one that fits your needs:

   | Model                          | Best for                                            | Download size | Speed   |
   | ------------------------------ | ---------------------------------------------------- | ------------- | ------- |
   | **xlm-roberta-large** (default) | Diverse names – Malay, Chinese, Indian, Arabic, etc. | ~1.2 GB       | Slower  |
   | **xlm-roberta-base**           | Diverse names, lighter alternative                   | ~1.1 GB       | Medium  |
   | **en_core_web_lg** (original)  | Western/English names only                           | ~500 MB       | Fastest |

   **Option A – Best for diverse names (default):**
   No changes needed. The transformer model downloads automatically on first run (~1.2 GB).

   **Option B – Lighter multilingual model:**
   If Option A is too slow or too large, open `anonymize.py`, find the line that says `"transformers": "Davlan/xlm-roberta-large-ner-hrl"` and change it to:

   ```python
   "transformers": "Davlan/xlm-roberta-base-ner-hrl"
   ```

   **Option C – Western/English names only (original):**
   If your participants all have Western names, you can use the faster original model. Open `anonymize.py` and:

   1. Find the import line (near the top) that says `from presidio_analyzer.nlp_engine import TransformersNlpEngine, NerModelConfiguration` and delete it
   2. Find the engine setup section (lines starting with `ner_config = ...` through `analyzer = AnalyzerEngine(nlp_engine=nlp_engine)`) and replace it all with just:

      ```python
      analyzer = AnalyzerEngine()
      ```

   3. Then run this in the terminal:

      ```bash
      python3 -m spacy download en_core_web_lg
      ```

7. You'll know it worked if all commands finish without errors. If you see a "Successfully installed" message, you're good

---

## How to Use

Every time you need to anonymize research files:

1. **Open the `anonymize-research` folder in VS Code** (same as setup – a fresh window, not your Claude project)
2. **Open the terminal** with `Cmd + J`. Again, do NOT start Claude Code here
3. **Drop your files** (`.md`, `.txt`, `.csv`, `.xlsx`, `.json`) into the `input/` folder. You can do this in Finder or drag them into the VS Code sidebar
4. **Run the script** – type this in the terminal and press Enter:

   ```bash
   # Process all files in input/
   python3 anonymize.py

   # Or process specific file(s) only
   python3 anonymize.py filename.md
   python3 anonymize.py file1.md file2.csv
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

**Sensitivity threshold** – controls how aggressively it flags PII:

```python
SCORE_THRESHOLD = 0.4
```

- `0.4` (default) catches more, but may flag some non-PII words
- Change it to `0.7` if you're getting too many false positives
- Just change the number and save the file (`Cmd + S`)

**What types of PII to detect** – controls which categories it looks for. Here are all the available types you can add or remove:

```python
ENTITIES_TO_DETECT = [
    "PERSON",           # People's names
    "EMAIL_ADDRESS",    # Email addresses
    "PHONE_NUMBER",     # Phone numbers
    "LOCATION",         # Places, addresses, countries
    "URL",              # Web links
    "IP_ADDRESS",       # IP addresses
    "CREDIT_CARD",      # Credit card numbers
    "DATE_TIME",        # Dates and times
    "NRP",              # Nationalities, religious, political groups
    "MEDICAL_LICENSE",  # Medical license numbers
    "US_SSN",           # US Social Security numbers
    "US_PASSPORT",      # US passport numbers
    "US_DRIVER_LICENSE", # US driver's license numbers
    "US_BANK_NUMBER",   # US bank account numbers
    "US_ITIN",          # US Individual Taxpayer ID
    "UK_NHS",           # UK National Health Service numbers
    "SG_NRIC_FIN",      # Singapore NRIC/FIN numbers
    "AU_ABN",           # Australian Business Numbers
    "AU_ACN",           # Australian Company Numbers
    "AU_TFN",           # Australian Tax File Numbers
    "AU_MEDICARE",      # Australian Medicare numbers
]
```

- To stop detecting a category, delete that line from the list (e.g. remove `"DATE_TIME",` if you want dates to stay visible)
- To add a category, copy the line from the list above and paste it in
- Save the file (`Cmd + S`) and run the script again
- Full list of supported entities: [Presidio docs](https://microsoft.github.io/presidio/supported_entities/)
