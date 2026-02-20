"""Expense Tracker CLI"""

import sys
import argparse
import pandas as pd
from pathlib import Path
from datetime import date


def main() -> None:
    """Main function to handle CLI commands."""

    # Set up the argument parser
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
        "-a",
        "--amount",
        help="The amount that you have spended(Use only positive value)",
        type=int,
        required=True,
    )

    # Delete a expense from the tracker
    parse_add = subparsers.add_parser("delete", help="delete a expense")
    parse_add.add_argument(
        "--id",
        help="id of a expense",
        type=int,
        required=True,
    )

    # Parse the arguments
    args = parser.parse_args()

    # Handle the commands
    if args.command == "list":
        display = display_expenses()
        print(display)
    elif args.command == "add":
        res = add_expense(args.description, args.amount)
        print(res)
    elif args.command == "delete":
        res = delete_expense(args.id)
        print(res)


def display_expenses() -> str:
    """Display the list of expenses in a tabular format."""
    data = load_data()

    return data.to_string(index=False)


def add_expense(description: str, amount: int) -> str:
    """Add a new expense to the tracker.

    Args:
        description (str): _Description of the expense_
        amount (str): _Amount spent on the expense_

    Returns:
        str: A success message with the ID of the added expense.
    """
    if not description:
        raise ValueError("Invalid description. Cannot be empty, Try to use more words.")
    if amount < 0:
        raise ValueError("Invalid amount. Use positive value")

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


def delete_expense(id: int) -> str:
    data = load_data()

    new_data = data.drop(data[data["ID"] == id].index)

    save_data(new_data, ops="w", header=True)
    return "Expense deleted successfully"


def load_data() -> pd.DataFrame:
    """Load the expenses data from the CSV file."""
    file_path = Path(__file__).parent / "my-expenses.csv"

    return pd.read_csv(file_path)


def save_data(new_data: pd.DataFrame, ops="a", header=False) -> None:
    """Save a new expense to the tracker."""
    file_path = Path(__file__).parent / "my-expenses.csv"

    new_data.to_csv(file_path, mode=ops, header=header, index=False)


if __name__ == "__main__":
    sys.exit(main())
