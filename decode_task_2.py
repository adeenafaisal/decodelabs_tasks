from decimal import Decimal, InvalidOperation


def parse_expense(raw_text):
    """Gatekeeper: turn raw text into a valid, positive Decimal.

    Raises ValueError if the text is not a usable expense amount.
    Decimal is used instead of float so money math stays exact
    (e.g. 0.10 + 0.20 == 0.30).
    """
    try:
        amount = Decimal(raw_text.strip())
    except InvalidOperation:
        raise ValueError("not a number")

    if not amount.is_finite():
        raise ValueError("not a finite number")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")
    return amount


def format_total(total):
    """View: how the total is presented to the user."""
    return f"FINAL TOTAL: ${total:,.2f}"


def main():
    total = Decimal("0")  
    count = 0

    print("=== Expense Tracker ===")
    print("Enter an expense amount (e.g. 100, 50, 20.50).")
    print("Type 'quit' to finish.\n")

    while True:
        raw = input("Expense: ")
        if raw.strip().lower() == "quit":
            break
        try:
            new_expense = parse_expense(raw)
        except ValueError as error:
            print(f"  Invalid data ({error}). Try again.")
            continue
        total += new_expense
        count += 1
        print(f"  Added {new_expense:,.2f} | Running total: {total:,.2f}")

    print(f"\nTransactions recorded: {count}")
    print(format_total(total))


if __name__ == "__main__":
    main()