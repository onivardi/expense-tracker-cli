import sys
import argparse
import pandas as pd
from pathlib import Path
from datetime import date


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage expenses.")
    subparsers = parser.add_subparsers(
        help="Available commands", dest="command", required=True
    )

    # List subcommand
    subparsers.add_parser("list", help="List a table of expensses")

    # Add a expense to the tracker
    parse_add = subparsers.add_parser("add", help="Add a expense")
    parse_add.add_argument(
        "-d", "--description", help="Description of your expense", required=True
    )
    parse_add.add_argument(
        "-a", "--amount", help="How much have you spended", type=int, required=True
    )

    args = parser.parse_args()

    if args.command == "list":
        display_expenses()
    elif args.command == "add":
        res = add_expense(args.description, args.amount)
        print(res)


def display_expenses():
    file_path = Path(__file__).parent / "my-expenses.csv"

    data = pd.read_csv(file_path)
    print(data.to_string(index=False))


def add_expense(description: str, amount: str) -> str:
    file_path = Path(__file__).parent / "my-expenses.csv"

    data = pd.read_csv(file_path)
    id = data["ID"].iloc[-1] + 1

    new_entry = pd.DataFrame(
        [
            {
                "ID": id,
                "Date": date.today(),
                "Description": description,
                "Amount": f"${amount}",
            }
        ]
    )
    new_entry.to_csv(file_path, mode="a", header=False, index=False)

    return f"Expense added successfully (ID: {id})"


if __name__ == "__main__":
    sys.exit(main())
