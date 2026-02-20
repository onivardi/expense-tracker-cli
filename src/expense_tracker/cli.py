import sys
import argparse
import pandas as pd
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage expenses.")
    subparsers = parser.add_subparsers(
        help="Available commands", dest="command", required=True
    )

    # List subcommand
    subparsers.add_parser("list", help="List a table of expensses")

    args = parser.parse_args()

    if args.command == "list":
        display_expenses()


def display_expenses():
    file_path = Path(__file__).parent / "my-expenses.csv"

    data = pd.read_csv(file_path)
    print(data.to_string(index=False))


if __name__ == "__main__":
    sys.exit(main())
