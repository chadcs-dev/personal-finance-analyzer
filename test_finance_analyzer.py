from finance_analyzer import Transaction, analyze_transactions


def test_analyze_transactions_calculates_savings_rate():
    transactions = [
        Transaction("2026-05-01", "Income", "Paycheck", 1000),
        Transaction("2026-05-02", "Food", "Groceries", -200),
        Transaction("2026-05-03", "Rent", "Rent", -500),
    ]
    summary = analyze_transactions(transactions)
    assert summary["income"] == 1000
    assert summary["expenses"] == 700
    assert summary["net_cash_flow"] == 300
    assert summary["savings_rate"] == 30
    assert summary["category_spending"]["Rent"] == 500
