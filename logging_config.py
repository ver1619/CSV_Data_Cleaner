# logging_config.py

"""
Centralized logging configuration.
Sets up file + terminal logging with timestamps and levels.
"""

import logging
import os


def setup_logging(log_dir="logs", log_file="app.log"):
    """
    Configure logging to write to both a file and the terminal.

    Args:
        log_dir: Directory for log files (created if missing)
        log_file: Log file name
    """

    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
