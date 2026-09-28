import re


def parse_transactions(text):
    transactions = []

    # Process the PDF line by line
    lines = text.splitlines()

    pattern = re.compile(
        r"^\s*"
        r"(\d{2}-[A-Za-z]{3}-\d{4})\s+"
        r"(.+?)\s+"
        r"(Debit|Credit)\s+"
        r"([\d,]+(?:\.\d{1,2})?)\s+"
        r"([\d,]+(?:\.\d{1,2})?)"
        r"\s*$",
        re.IGNORECASE
    )

    for line in lines:
        line = line.strip()

        match = pattern.match(line)

        if not match:
            continue

        date, description, txn_type, amount, balance = match.groups()

        transactions.append({
            "date": date,
            "description": description.strip(),
            "type": txn_type.capitalize(),
            "amount": float(amount.replace(",", "")),
            "balance": float(balance.replace(",", ""))
        })

    return transactions