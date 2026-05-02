# utils/file_utils.py

import csv
from cleaner.exceptions import EmptyFileError, SchemaError


def read_csv(file_path):
    """
    Reads a CSV file and returns list of rows (as dictionaries)
    """

    data = []

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        # Check if file is empty
        if reader.fieldnames is None:
            raise EmptyFileError("CSV file is empty")

        # Check required columns
        required_columns = ["id", "name", "salary"]

        for col in required_columns:
            if col not in reader.fieldnames:
                raise SchemaError(f"Missing column: {col}")

        for row in reader:
            data.append(row)

    return data

# Add this function below read_csv()

def write_csv(file_path, data):
    """
    Writes cleaned data to CSV file
    """

    if not data:
        print("No data to write")
        return

    import csv

    # Get headers from first row
    headers = data[0].keys()

    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()
        writer.writerows(data)