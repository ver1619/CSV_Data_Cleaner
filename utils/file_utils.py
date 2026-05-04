# utils/file_utils.py

import csv
import logging
from cleaner.exceptions import EmptyFileError, SchemaError

logger = logging.getLogger(__name__)


def read_csv(file_path, required_columns=None):
    """
    Reads a CSV file and returns list of rows (as dictionaries)

    Args:
        file_path: Path to the CSV file
        required_columns: List of column names that must be present
    """

    data = []

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        # Check if file is empty
        if reader.fieldnames is None:
            raise EmptyFileError("CSV file is empty")

        # Check required columns
        if required_columns:
            for col in required_columns:
                if col not in reader.fieldnames:
                    raise SchemaError(f"Missing column: {col}")

        for row in reader:
            data.append(row)

    return data




def write_csv(file_path, data):
    """
    Writes cleaned data to CSV file
    """

    if not data:
        logger.warning("No data to write")
        return

    # Get headers from first row
    headers = data[0].keys()

    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()
        writer.writerows(data)