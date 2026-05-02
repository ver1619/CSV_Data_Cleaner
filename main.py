# main.py

import argparse
from cleaner.data_cleaner import DataCleaner


def main():

    parser = argparse.ArgumentParser(
        description="CSV Data Cleaner CLI"
    )

    parser.add_argument(
        "input_file",
        help="Path to input CSV file"
    )

    parser.add_argument(
        "output_file",
        help="Path to output cleaned CSV file"
    )

    args = parser.parse_args()

    cleaner = DataCleaner(args.input_file)

    try:
        cleaner.read()
        cleaner.validate()
        cleaner.clean()
        cleaner.write(args.output_file)
        cleaner.report()

        print(f"\n✅ Cleaned file saved at: {args.output_file}")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()