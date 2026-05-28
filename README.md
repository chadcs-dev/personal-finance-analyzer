# Personal Finance Analyzer

Python command-line tool that reads a CSV of transactions and summarizes
income, expenses, category spending, savings rate, and monthly cash flow.

This project is intentionally read-only and local. It does not connect to bank
accounts or use real credentials.

## What it demonstrates

- CSV parsing
- Financial summary calculations
- Category aggregation
- Monthly cash-flow analysis
- Defensive input validation
- Clean command-line output

## Run

```bash
python3 finance_analyzer.py sample_transactions.csv
```

## Example Output

```text
Personal Finance Summary
Total income: $3,200.00
Total expenses: $2,095.25
Net cash flow: $1,104.75
Savings rate: 34.52%

Top spending categories:
- Rent: $1,200.00
- Food: $315.25
- Savings: $240.00
- Transportation: $180.00
```
