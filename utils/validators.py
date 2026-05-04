# utils/validators.py

"""
Contains functions to validate data
"""


def is_null(value):
    """
    Check if value is empty or missing
    """
    return value is None or value.strip() == ""


def validate_field(value, rules):
    """
    Validate a field value against rules from config.

    Args:
        value: The field value to check
        rules: Dict with validation rules, e.g. {"type": "int", "min": 0}

    Returns:
        True if valid, False otherwise
    """

    expected_type = rules.get("type")

    if expected_type == "int":
        try:
            num = int(value)
        except (ValueError, TypeError):
            return False

        if "min" in rules and num < rules["min"]:
            return False

        if "max" in rules and num > rules["max"]:
            return False

    return True


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