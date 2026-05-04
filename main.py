# main.py

import argparse
import logging
from logging_config import setup_logging
from config_loader import load_config
from cleaner.data_cleaner import DataCleaner

logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(
        description="CSV Data Cleaner CLI"
    )

    # Positional arguments
    parser.add_argument(
        "input_file",
        help="Path to input CSV file"
    )

    parser.add_argument(
        "output_file",
        help="Path to output cleaned CSV file"
    )

    # Optional flags
    parser.add_argument(
        "--drop-null",
        action="store_true",
        help="Drop rows with null values"
    )

    parser.add_argument(
        "--dedupe",
        action="store_true",
        help="Remove duplicate rows"
    )

    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to config file (default: config.json)"
    )

    parser.add_argument(
        "--errors-file",
        default=None,
        help="Path to save invalid/duplicate rows CSV"
    )

    args = parser.parse_args()

    # Initialize logging
    setup_logging()

    # Load config
    config = load_config(args.config)

    # If no flags passed, enable all cleaning (backwards compatible)
    drop_null = args.drop_null or (not args.drop_null and not args.dedupe)
    dedupe = args.dedupe or (not args.drop_null and not args.dedupe)

    # Initialize cleaner with config and flags
    cleaner = DataCleaner(
        args.input_file,
        config=config,
        drop_null=drop_null,
        dedupe=dedupe
    )

    try:
        cleaner.read()
        cleaner.validate()
        cleaner.clean()
        cleaner.write(args.output_file)
        cleaner.report()

        # Save error rows if requested
        if args.errors_file:
            cleaner.write_errors(args.errors_file)

        logger.info(f"✅ Cleaned file saved at: {args.output_file}")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()