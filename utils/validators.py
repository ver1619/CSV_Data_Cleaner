# utils/validators.py

"""
Contains functions to validate data
"""


def is_null(value):
    """
    Check if value is empty or missing
    """
    return value is None or value.strip() == ""


def is_valid_salary(value):
    """
    Check if salary is a valid positive integer
    """
    try:
        value = int(value)

        if value < 0:
            return False

        return True

    except:
        return False


def find_duplicates(data):
    """
    Detect duplicate rows based on full row match
    """
    seen = set()
    duplicates = []

    for row in data:
        # Convert row to tuple (so it can be stored in set)
        row_tuple = tuple(row.items())

        if row_tuple in seen:
            duplicates.append(row)
        else:
            seen.add(row_tuple)

    return duplicates