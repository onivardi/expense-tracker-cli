"""Expense Tracker CLI"""

import sys
import argparse
import pandas as pd
from pathlib import Path
from datetime import date
import calendar


def main() -> None:
    """Main function to handle CLI commands."""

    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Manage expenses.")
    subparsers = parser.add_subparsers(
        help="Available commands", dest="command", required=True
    )

    # List subcommand
    subparsers.add_parser("list", help="Display a table of expensses")

    # Summary the entire expenses
    parse_summary = subparsers.add_parser("summary", help="Summary the expenses")
    parse_summary.add_argument(
        "--month",
        type=int,
        choices=range(1, 12),
        help="Summary the expenses on given month",
    )

    # Add a expense to the tracker
    parse_add = subparsers.add_parser("add", help="Add a expense")
    parse_add.add_argument(
        "--description", help="Description of your expense", required=True
    )
    parse_add.add_argument(
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
    elif args.command == "summary":
        res = summary_expenses(args.month)
        print(res)


def summary_expenses(month: int) -> str:
    """Summary the expenses for a given month or all expenses if month is not provided.
    Args:
        month (int): _Month number (1-12) to filter expenses. If not provided, summary for all expenses._
        Returns: str: _Summary of expenses for the specified month or all expenses._""" 
    data = load_data()

    # Convert them to the right type
    data["Date"] = pd.to_datetime(data["Date"])
    data["Amount"] = data["Amount"].str.replace("$", "").astype("int")

    # Data with month selected or all expenses
    total = (
        data[data["Date"].dt.month == month]["Amount"].sum()
        if month
        else data["Amount"].sum()
    )

    if month:
        return f"Total expenses for {calendar.month_name[month]}: ${total}"

    return f"Total expenses: ${total}"


def display_expenses() -> str:
    """Display the list of expenses in a tabular format.
    Returns:
        str: A string representation of the expenses table."""
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
    """Delete an expense from the tracker.

    Args:
        id (int): The ID of the expense to delete.

    Returns:
        str: A success message indicating the expense was deleted.
    """
    if not isinstance(id, int) or id < 0:
        raise ValueError("Invalid ID. Use a positive integer value.")
    
    data = load_data()

    new_data = data.drop(data[data["ID"] == id].index)

    save_data(new_data, ops="w", header=True)

    return "Expense deleted successfully"


def load_data() -> pd.DataFrame:
    """Load the expenses data from the CSV file.
    Returns:
        pd.DataFrame: A DataFrame containing the expenses data."""
    file_path = Path(__file__).parent / "my-expenses.csv"

    return pd.read_csv(file_path)


def save_data(new_data: pd.DataFrame, ops="a", header=False) -> None:
    """Save a new expense to the tracker.
    Args:
        new_data (pd.DataFrame): The new expense data to save.
        ops (str, optional): The file mode to use when saving the data. Defaults to "a" (append).
        header (bool, optional): Whether to include the header in the CSV file. Defaults to False.
        
        Returns: None: This function does not return anything."""
    file_path = Path(__file__).parent / "my-expenses.csv"

    new_data.to_csv(file_path, mode=ops, header=header, index=False)


if __name__ == "__main__":
    sys.exit(main())
