# CSV Data Cleaner CLI

A command-line tool to clean messy CSV data by detecting and removing:

- Null values
- Invalid data types
- Duplicate rows

---

## Features

- Built using Python standard library (no pandas)
- OOP-based design
- Custom exception handling
- CLI interface using argparse

---

## Usage

```bash
python main.py input.csv output.csv
```

### Example
```bash
python main.py data/sample.csv data/cleaned_output.csv
```

---

## Output

- Cleaned CSV file
- Summary report printed in terminal

### Example Output

```python
📊 Data Cleaning Report
------------------------------
Total rows: 25
Invalid rows: 8
Duplicate rows: 3
Clean rows: 14

✅ Cleaned file saved at: data/cleaned_output.csv
```