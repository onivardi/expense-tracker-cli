# Expense Tracker

A small command-line expense tracker that stores expenses in a CSV file and
provides simple commands to list, add, delete and summarize expenses.

**Highlights**
- **Simple CLI:** list, add, delete, summary.
- **CSV storage:** data saved in a plain CSV at [src/expense_tracker/my-expenses.csv](src/expense_tracker/my-expenses.csv).
- **Single-file implementation:** CLI and data helpers in [src/expense_tracker/cli.py](src/expense_tracker/cli.py).

**Requirements**
- **Python:** 3.10 or newer.
- **Dependencies:** `pandas` (used for CSV handling and tabular display).

**Quick Install**
- Clone the repo and create a virtual environment:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

- Install the package in editable mode (this will pick up `pyproject.toml`):

```bash
pip install -e .
pip install pandas
```

**Usage (CLI)**
Run the CLI module or the script directly. Examples below use the module form.

- List all expenses:

```bash
python -m expense_tracker.cli list
```

- Add an expense (description required, amount must be a positive integer):

```bash
python -m expense_tracker.cli add --description "Coffee" --amount 5
```

- Delete an expense by ID:

```bash
python -m expense_tracker.cli delete --id 3
```

- Summary of expenses (optionally for a specific month):

```bash
python -m expense_tracker.cli summary
python -m expense_tracker.cli summary --month 5
```

**CSV storage**
- File location: [src/expense_tracker/my-expenses.csv](src/expense_tracker/my-expenses.csv)
- Expected columns / example header:

```
ID,Date,Description,Amount
1,2026-02-20,Coffee,$5
```

Notes:
- `Amount` values are stored with a leading dollar sign (e.g. `$12`).
- The CSV is appended to when adding an expense; deleting rewrites the file.

**Development**
- To inspect and edit the CLI, see [src/expense_tracker/cli.py](src/expense_tracker/cli.py).
- If you add new dependencies, update `pyproject.toml` or install them into your virtual environment.


