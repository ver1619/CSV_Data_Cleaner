# cleaner/data_cleaner.py

import logging
from utils.file_utils import read_csv, write_csv
from utils.validators import is_null, validate_field, find_duplicates

logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Main class responsible for:
    - loading data
    - validating data
    - cleaning data
    - storing results
    """

    def __init__(self, file_path, config=None, drop_null=True, dedupe=True):
        """
        Initialize DataCleaner with config and behavior flags.

        Args:
            file_path: Path to input CSV file
            config: Dict loaded from config.json (column rules, validation)
            drop_null: If True, remove rows with null values
            dedupe: If True, remove duplicate rows
        """

        # Input file path
        self.file_path = file_path

        # Config (rules + columns)
        self.config = config or {}

        # Behavior flags
        self.drop_null = drop_null
        self.dedupe = dedupe

        # Raw data (loaded from CSV)
        self.raw_data = []

        # Cleaned data
        self.cleaned_data = []

        # Tracking issues
        self.invalid_rows = []
        self.duplicate_rows = []

    # ---------------------------
    # Step 1: Read Data
    # ---------------------------
    def read(self):
        """
        Load CSV data into memory
        """

        required_columns = self.config.get("required_columns")
        self.raw_data = read_csv(self.file_path, required_columns)
        logger.info(f"Loaded {len(self.raw_data)} rows from {self.file_path}")

    # ---------------------------
    # Step 2: Validate Data
    # ---------------------------
    def validate(self):
        """
        Detect invalid rows and duplicates based on config rules.
        """

        logger.info("Starting validation...")

        null_columns = self.config.get("null_check_columns", [])
        rules = self.config.get("validation_rules", {})

        for row in self.raw_data:

            invalid = False

            # Check null values (dynamic columns from config)
            for col in null_columns:
                if is_null(row.get(col, "")):
                    logger.warning(f"Null value in '{col}': {row}")
                    self.invalid_rows.append(row)
                    invalid = True
                    break

            if invalid:
                continue

            # Check validation rules (dynamic from config)
            for col, col_rules in rules.items():
                if not validate_field(row.get(col, ""), col_rules):
                    logger.warning(f"Invalid '{col}' value: {row}")
                    self.invalid_rows.append(row)
                    invalid = True
                    break

        # Detect duplicates (separate step)
        self.duplicate_rows = find_duplicates(self.raw_data)

        logger.info(
            f"Validation complete: {len(self.invalid_rows)} invalid, "
            f"{len(self.duplicate_rows)} duplicates"
        )

    # ---------------------------
    # Step 3: Clean Data
    # ---------------------------
    def clean(self):
        """
        Orchestrate cleaning based on flags (drop_null, dedupe).
        Each sub-step is handled by a focused private method.
        """

        logger.info(
            f"Cleaning with flags: drop_null={self.drop_null}, dedupe={self.dedupe}"
        )

        data = self.raw_data[:]

        if self.drop_null:
            data = self._remove_invalid(data)

        if self.dedupe:
            data = self._remove_duplicates(data)

        data = self._cast_types(data)
        self.cleaned_data = data

        logger.info(f"Cleaning complete: {len(self.cleaned_data)} clean rows")

    def _remove_invalid(self, data):
        """Remove rows that were flagged invalid during validation"""
        return [row for row in data if row not in self.invalid_rows]

    def _remove_duplicates(self, data):
        """Remove duplicate rows (full row match)"""
        seen = set()
        result = []

        for row in data:
            key = tuple(row.items())
            if key not in seen:
                seen.add(key)
                result.append(row)

        return result

    def _cast_types(self, data):
        """Cast fields based on config validation_rules type"""
        rules = self.config.get("validation_rules", {})

        for row in data:
            for col, rule in rules.items():
                if rule.get("type") == "int" and col in row:
                    try:
                        row[col] = int(row[col])
                    except (ValueError, TypeError):
                        pass  # already handled in validate()

        return data

    # ---------------------------
    # Step 4: Report
    # ---------------------------
    def report(self):
        """
        Log summary report
        """

        logger.info("📊 Data Cleaning Report")
        logger.info("-" * 30)
        logger.info(f"  Total rows:     {len(self.raw_data)}")
        logger.info(f"  Invalid rows:   {len(self.invalid_rows)}")
        logger.info(f"  Duplicate rows: {len(self.duplicate_rows)}")
        logger.info(f"  Clean rows:     {len(self.cleaned_data)}")

    # ---------------------------
    # Step 5: Write Output
    # ---------------------------
    def write(self, output_path):
        """
        Save cleaned data to CSV
        """

        write_csv(output_path, self.cleaned_data)
        logger.info(f"Cleaned data written to {output_path}")

    # ---------------------------
    # Step 6: Write Errors
    # ---------------------------
    def write_errors(self, error_path):
        """
        Save invalid + duplicate rows to a separate CSV
        """

        error_rows = self.invalid_rows + self.duplicate_rows

        if error_rows:
            write_csv(error_path, error_rows)
            logger.info(f"Error rows saved to {error_path}")
        else:
            logger.info("No error rows to write")