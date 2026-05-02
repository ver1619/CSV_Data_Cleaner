# cleaner/data_cleaner.py

from utils.file_utils import read_csv
from utils.validators import is_null, is_valid_salary, find_duplicates


class DataCleaner:
    """
    Main class responsible for:
    - loading data
    - validating data
    - cleaning data
    - storing results
    """

    def __init__(self, file_path):
        # Input file path
        self.file_path = file_path

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
        self.raw_data = read_csv(self.file_path)

    # ---------------------------
    # Step 2: Validate Data
    # ---------------------------
    def validate(self):
        """
        Detect invalid rows and duplicates
        """

        for row in self.raw_data:

            # Check null values
            if is_null(row["name"]):
                self.invalid_rows.append(row)
                continue

            # Check salary
            if not is_valid_salary(row["salary"]):
                self.invalid_rows.append(row)
                continue

        # Detect duplicates (separate step)
        self.duplicate_rows = find_duplicates(self.raw_data)

    # ---------------------------
    # Step 3: Clean Data
    # ---------------------------
    def clean(self):
        """
        Remove invalid rows and duplicates
        """

        seen = set()

        for row in self.raw_data:

            # Skip invalid rows
            if row in self.invalid_rows:
                continue

            # Convert row to tuple for duplicate detection
            row_tuple = tuple(row.items())

            if row_tuple in seen:
                continue  # skip duplicate

            seen.add(row_tuple)

            # Convert salary to int (clean transformation)
            row["salary"] = int(row["salary"])

            self.cleaned_data.append(row)

    # ---------------------------
    # Step 4: Report
    # ---------------------------
    def report(self):
        """
        Print summary report
        """

        print("\n📊 Data Cleaning Report")
        print("-" * 30)
        print("Total rows:", len(self.raw_data))
        print("Invalid rows:", len(self.invalid_rows))
        print("Duplicate rows:", len(self.duplicate_rows))
        print("Clean rows:", len(self.cleaned_data))

     # ---------------------------
    # Step 5: Write Output
    # ---------------------------
    def write(self, output_path):
        """
        Save cleaned data to CSV
        """

        from utils.file_utils import write_csv

        write_csv(output_path, self.cleaned_data)