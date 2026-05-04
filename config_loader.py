# config_loader.py

"""
Loads validation rules and column config from a JSON file.
"""

import json
import logging

logger = logging.getLogger(__name__)


def load_config(path="config.json"):
    """
    Read and return config from a JSON file.

    Args:
        path: Path to config JSON file

    Returns:
        dict with config data
    """

    with open(path, "r") as f:
        config = json.load(f)

    logger.info(f"Config loaded from {path}")
    return config
