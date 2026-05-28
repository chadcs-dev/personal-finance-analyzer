from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Transaction:
    date: str
    category: str
    description: str
    amount: float


def load_transactions(path: str) -> list[Transaction]:
    transactions: list[Transaction] = []
    with Path(path).open(newline="") as file:
        reader = csv.DictReader(file)
        required = {"date", "category", "description", "amount"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")

        for row in reader:
            transactions.append(
                Transaction(
                    date=row["date"],
                    category=row["category"].strip(),
                    description=row["description"].strip(),
                    amount=float(row["amount"]),
                )
            )
    return transactions


def analyze_transactions(transactions: list[Transaction]) -> dict:
    income = sum(t.amount for t in transactions if t.amount > 0)
    expenses = abs(sum(t.amount for t in transactions if t.amount < 0))
    net_cash_flow = income - expenses
    savings_rate = (net_cash_flow / income * 100) if income else 0.0

    category_spending: dict[str, float] = defaultdict(float)
    monthly_cash_flow: dict[str, float] = defaultdict(float)
    for transaction in transactions:
        month = transaction.date[:7]
        monthly_cash_flow[month] += transaction.amount
        if transaction.amount < 0:
            category_spending[transaction.category] += abs(transaction.amount)

    return {
        "income": income,
        "expenses": expenses,
        "net_cash_flow": net_cash_flow,
        "savings_rate": savings_rate,
        "category_spending": dict(category_spending),
        "monthly_cash_flow": dict(monthly_cash_flow),
    }


def dollars(value: float) -> str:
    return f"${value:,.2f}"


def format_summary(summary: dict) -> str:
    lines = [
        "Personal Finance Summary",
        f"Total income: {dollars(summary['income'])}",
        f"Total expenses: {dollars(summary['expenses'])}",
        f"Net cash flow: {dollars(summary['net_cash_flow'])}",
        f"Savings rate: {summary['savings_rate']:.2f}%",
        "",
        "Top spending categories:",
    ]
    categories = sorted(
        summary["category_spending"].items(),
        key=lambda item: item[1],
        reverse=True,
    )
    if categories:
        for category, total in categories[:5]:
            lines.append(f"- {category}: {dollars(total)}")
    else:
        lines.append("- None")

    lines.extend(["", "Monthly cash flow:"])
    for month, total in sorted(summary["monthly_cash_flow"].items()):
        lines.append(f"- {month}: {dollars(total)}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze personal finance transactions.")
    parser.add_argument("csv_path", help="CSV file with date, category, description, amount columns.")
    args = parser.parse_args()

    transactions = load_transactions(args.csv_path)
    summary = analyze_transactions(transactions)
    print(format_summary(summary))


if __name__ == "__main__":
    main()
