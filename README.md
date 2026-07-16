![Status](https://img.shields.io/badge/status-retired-red)

# *CSV Data Cleaner CLI*

A command-line tool to clean messy CSV file, finds problems in it, fixes them, and gives you back a clean version.

---

## What Does It Actually Do?    

Real-world data is messy. You might get a CSV file from a database export, a form submission, or a coworker — and it often has problems like:

| Problem | Example |
|---|---|
| **Empty/null values** | Row 3: name is missing (blank) |
| **Wrong data types** | Row 5: salary is `abc` instead of a number |
| **Negative values** | Row 4: salary is `-5000` |
| **Duplicate rows** | Row 12: exact copy of row 2 |

This tool catches all of those, removes (or separates) the bad rows, and saves the clean data.

---

## Features

- **No external dependencies** — uses only Python's standard library
- **Config-driven validation** — rules live in `config.json`, not hardcoded
- **CLI flags** — control what cleaning to apply (`--drop-null`, `--dedupe`)
- **Error row export** — save bad rows to a separate file instead of losing them
- **Structured logging** — every step is logged with timestamps to `logs/app.log`
- **OOP design** — clean `DataCleaner` class with focused methods
- **Custom exceptions** — `EmptyFileError` and `SchemaError` for clear error messages

---

## Requirements

- **Python 3.6+** (any recent version works)
- No external packages needed — built entirely on Python's standard library (`csv`, `argparse`, `logging`, `json`)

---

## Setup

```bash
# 1. Clone or download the project
git clone https://github.com/ver1619/CSV_Data_Cleaner.git
cd CSV_Data_Cleaner

# 2. (Optional) Create a virtual environment
python3 -m venv myvenv
source myvenv/bin/activate
```

---

## Project Structure

```
├── 📁 cleaner
│   ├── data_cleaner.py
│   └── exceptions.py
├── 📁 data
│   ├── sample.csv           ← Sample messy data
│   └── cleaned_output.csv   ← Cleaned CSV file
├── 📁 utils
│   ├── file_utils.py
│   └── validators.py
├── ⚙️ .gitignore
├── 📝 README.md
├── ⚙️ config.json
├── config_loader.py
├── logging_config.py
├── main.py
└── logs/
    └── app.log              ← Auto-generated log file with timestamps
```

---

## Usage

### Basic (clean everything)

```bash
python3 main.py data/sample.csv data/cleaned_output.csv
```

This runs **all** cleaning — removes nulls, invalid rows, and duplicates.


### With specific flags

```bash
# Only drop rows with null/empty values (keep duplicates)
python3 main.py data/sample.csv output.csv --drop-null

# Only remove duplicate rows (keep invalid rows)
python3 main.py data/sample.csv output.csv --dedupe

# Both flags explicitly
python3 main.py data/sample.csv output.csv --drop-null --dedupe
```

### Save error rows to a file

```bash
python3 main.py data/sample.csv data/output.csv --errors-file data/errors.csv
```

This saves all invalid and duplicate rows into `errors.csv` so you can review them later.

### Use a custom config file

```bash
python3 main.py data/sample.csv output.csv --config my_custom_rules.json
```

### See all available options

```bash
python3 main.py --help
```

---

## What if I have a different dataset?

The tool is **not hardcoded** to work with only name/salary columns. You can use it with **any CSV file** by editing `config.json`.

### Step 1 — Update `required_columns`

List the columns your CSV must have:

```json
{
  "required_columns": ["product_id", "product_name", "price", "stock"]
}
```

### Step 2 — Update `null_check_columns`

List which columns should not be empty:

```json
{
  "null_check_columns": ["product_name"]
}
```

### Step 3 — Update `validation_rules`

Define what type each column should be and any bounds:

```json
{
  "validation_rules": {
    "price": {
      "type": "int",
      "min": 1
    },
    "stock": {
      "type": "int",
      "min": 0,
      "max": 10000
    }
  }
}
```

### Full example for a product inventory CSV

```json
{
  "required_columns": ["product_id", "product_name", "price", "stock"],
  "null_check_columns": ["product_name"],
  "validation_rules": {
    "price": {
      "type": "int",
      "min": 1
    },
    "stock": {
      "type": "int",
      "min": 0
    }
  }
}
```

Then run:

```bash
python3 main.py <input_file.csv> <output_file.csv> --config config.json
```

That's it — no code changes needed, just update the JSON.

---


## Pipeline Flow

Here's how data moves through the tool from start to finish:

```
User runs:  python3 main.py input.csv output.csv --drop-null --dedupe --errors-file errors.csv
                │
                ▼
        CLI parses flags (argparse)
                │
                ▼
        Config loaded from config.json
                │
                ▼
        DataCleaner initialized with config + flags
                │
                ▼
        read()      → loads CSV rows into memory
                │
                ▼
        validate()  → checks each row against config rules
                │        (null columns, type checks, min/max)
                ▼
        clean()     → removes invalid rows (if --drop-null)
                │        removes duplicates (if --dedupe)
                │        casts types (salary string → int)
                ▼
        write()     → saves clean rows to output CSV
                │
                ▼
        write_errors() → saves bad rows to errors.csv
                │
                ▼
        report()    → logs summary (total, invalid, duplicate, clean)
                │
                ▼
        logs/app.log ← everything is recorded with timestamps
```

---

## Example

**Sample Data** : `data/sample.csv`

```csv
id,name,department,salary,joining_year
1,Rahul,Engineering,70000,2020
2,Anita,HR,60000,2019
3,,Finance,80000,2021
4,Vikram,Engineering,-5000,2018
5,Raj,Sales,abc,2022
6,Kiran,Engineering,75000,2020
7,Sneha,HR,62000,2017
8,,Marketing,50000,2021
9,Amit,Engineering,0,2023
10,Pooja,Finance,82000,2019
2,Anita,HR,60000,2019
11,Neha,Sales,67000,2020
12,Arjun,Engineering,not_available,2021
13,Meera,Finance,88000,2018
14,John,Engineering,92000,2017
15,,HR,55000,2022
16,Ravi,Engineering,-2000,2016
17,Sara,Marketing,78000,2020
18,Ali,Sales,abc,2023
19,Kabir,Engineering,91000,2019
20,Nina,Finance,94000,2021
21,Rahul,Engineering,70000,2020
22,Anita,HR,60000,2019
23,Dev,Sales,0,2022
24,,Finance,null,2020
25,Sam,Engineering,72000,2021
```

---

Run : 
```bash
python3 main.py data/sample.csv data/output.csv --errors-file data/errors.csv
```

---

**Output Data** : `data/output.csv`

```csv
id,name,department,salary,joining_year
1,Rahul,Engineering,70000,2020
2,Anita,HR,60000,2019
6,Kiran,Engineering,75000,2020
7,Sneha,HR,62000,2017
9,Amit,Engineering,0,2023
10,Pooja,Finance,82000,2019
11,Neha,Sales,67000,2020
13,Meera,Finance,88000,2018
14,John,Engineering,92000,2017
17,Sara,Marketing,78000,2020
19,Kabir,Engineering,91000,2019
20,Nina,Finance,94000,2021
21,Rahul,Engineering,70000,2020
22,Anita,HR,60000,2019
23,Dev,Sales,0,2022
25,Sam,Engineering,72000,2021
```


---

**Errors** : `data/errors.csv`

```csv
id,name,department,salary,joining_year
3,,Finance,80000,2021
4,Vikram,Engineering,-5000,2018
5,Raj,Sales,abc,2022
8,,Marketing,50000,2021
12,Arjun,Engineering,not_available,2021
15,,HR,55000,2022
16,Ravi,Engineering,-2000,2016
18,Ali,Sales,abc,2023
24,,Finance,null,2020
2,Anita,HR,60000,2019
```

---


### Log entries are generated and saved with timestamps to `logs/app.log`

```
2026-05-04 09:36:55,649 [INFO] Config loaded from config.json
2026-05-04 09:36:55,650 [INFO] Loaded 26 rows from data/sample.csv
2026-05-04 09:36:55,650 [INFO] Starting validation...
2026-05-04 09:36:55,650 [WARNING] Null value in 'name': {'id': '3', 'name': '', 'department': 'Finance', 'salary': '80000', 'joining_year': '2021'}
2026-05-04 09:36:55,650 [WARNING] Invalid 'salary' value: {'id': '4', 'name': 'Vikram', 'department': 'Engineering', 'salary': '-5000', 'joining_year': '2018'}
2026-05-04 09:36:55,651 [WARNING] Invalid 'salary' value: {'id': '5', 'name': 'Raj', 'department': 'Sales', 'salary': 'abc', 'joining_year': '2022'}
2026-05-04 09:36:55,651 [WARNING] Null value in 'name': {'id': '8', 'name': '', 'department': 'Marketing', 'salary': '50000', 'joining_year': '2021'}
2026-05-04 09:36:55,651 [WARNING] Invalid 'salary' value: {'id': '12', 'name': 'Arjun', 'department': 'Engineering', 'salary': 'not_available', 'joining_year': '2021'}
2026-05-04 09:36:55,651 [WARNING] Null value in 'name': {'id': '15', 'name': '', 'department': 'HR', 'salary': '55000', 'joining_year': '2022'}
2026-05-04 09:36:55,651 [WARNING] Invalid 'salary' value: {'id': '16', 'name': 'Ravi', 'department': 'Engineering', 'salary': '-2000', 'joining_year': '2016'}
2026-05-04 09:36:55,651 [WARNING] Invalid 'salary' value: {'id': '18', 'name': 'Ali', 'department': 'Sales', 'salary': 'abc', 'joining_year': '2023'}
2026-05-04 09:36:55,651 [WARNING] Null value in 'name': {'id': '24', 'name': '', 'department': 'Finance', 'salary': 'null', 'joining_year': '2020'}
2026-05-04 09:36:55,652 [INFO] Validation complete: 9 invalid, 1 duplicates
2026-05-04 09:36:55,652 [INFO] Cleaning with flags: drop_null=True, dedupe=True
2026-05-04 09:36:55,652 [INFO] Cleaning complete: 16 clean rows
2026-05-04 09:36:55,653 [INFO] Cleaned data written to output.csv
2026-05-04 09:36:55,653 [INFO] 📊 Data Cleaning Report
2026-05-04 09:36:55,653 [INFO] ------------------------------
2026-05-04 09:36:55,653 [INFO]   Total rows:     26
2026-05-04 09:36:55,653 [INFO]   Invalid rows:   9
2026-05-04 09:36:55,653 [INFO]   Duplicate rows: 1
2026-05-04 09:36:55,653 [INFO]   Clean rows:     16
2026-05-04 09:36:55,653 [INFO] Error rows saved to data/errors.csv
2026-05-04 09:36:55,654 [INFO] ✅ Cleaned file saved at: output.csv
```

