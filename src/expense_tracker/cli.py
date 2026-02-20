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
        display = display_expenses()
        print(display)
    elif args.command == "add":
        res = add_expense(args.description, args.amount)
        print(res)


def display_expenses() -> str:
    data = load_data()
    return data.to_string(index=False)


def add_expense(description: str, amount: str) -> str:
    data = load_data()
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
    save_data(new_entry)
    return f"Expense added successfully (ID: {id})"


def load_data() -> pd.DataFrame:
    file_path = Path(__file__).parent / "my-expenses.csv"

    return pd.read_csv(file_path)


def save_data(new_data: pd.DataFrame) -> None:
    file_path = Path(__file__).parent / "my-expenses.csv"
    new_data.to_csv(file_path, mode="a", header=False, index=False)


if __name__ == "__main__":
    sys.exit(main())
