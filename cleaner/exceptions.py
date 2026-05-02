# cleaner/exceptions.py

"""
Custom exceptions for CSV Data Cleaner
These help us handle specific errors in a clean way
"""

class EmptyFileError(Exception):
    """Raised when the CSV file is empty"""
    pass


class SchemaError(Exception):
    """Raised when required columns are missing"""
    pass