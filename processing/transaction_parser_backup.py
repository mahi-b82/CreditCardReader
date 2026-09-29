import re
from datetime import datetime


def normalize_date(date_text):
    """
    Convert common statement date formats into DD-MMM-YYYY.
    """

    date_text = date_text.strip()

    date_formats = [
        "%d-%b-%Y",   # 29-Sep-2026
        "%d-%B-%Y",   # 29-September-2026
        "%d/%m/%Y",   # 29/09/2026
        "%d-%m-%Y",   # 29-09-2026
        "%d.%m.%Y",   # 29.09.2026
        "%d %b %Y",   # 29 Sep 2026
        "%d %B %Y",   # 29 September 2026
    ]

    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(date_text, date_format)
            return parsed_date.strftime("%d-%b-%Y")
        except ValueError:
            continue

    # If the format is unknown, keep the original value
    return date_text


def clean_amount(amount_text):
    """
    Convert amounts such as:
    1,250
    1,250.50
    1250
    1250.50
    into float values.
    """

    amount_text = amount_text.strip()

    # Remove commas and other unnecessary spaces
    amount_text = amount_text.replace(",", "")
    amount_text = amount_text.replace(" ", "")

    # Remove common currency symbols
    amount_text = re.sub(r"[₹$€£]", "", amount_text)

    return float(amount_text)


def clean_description(description):
    """
    Clean extra spaces from transaction descriptions.
    """

    description = description.strip()

    # Replace multiple spaces/tabs with a single space
    description = re.sub(r"\s+", " ", description)

    return description


def parse_transactions(text):

    transactions = []

    # --------------------------------------------------
    # PROCESS PDF TEXT
    # --------------------------------------------------

    lines = text.splitlines()

    # --------------------------------------------------
    # DATE PATTERN
    # --------------------------------------------------

    date_pattern = (
        r"(?:"
        r"\d{2}-[A-Za-z]{3}-\d{4}"       # 29-Sep-2026
        r"|"
        r"\d{2}-[A-Za-z]+-\d{4}"         # 29-September-2026
        r"|"
        r"\d{2}/\d{2}/\d{4}"             # 29/09/2026
        r"|"
        r"\d{2}-\d{2}-\d{4}"             # 29-09-2026
        r"|"
        r"\d{2}\.\d{2}\.\d{4}"           # 29.09.2026
        r"|"
        r"\d{2} [A-Za-z]{3} \d{4}"       # 29 Sep 2026
        r"|"
        r"\d{2} [A-Za-z]+ \d{4}"         # 29 September 2026
        r")"
    )

    # --------------------------------------------------
    # AMOUNT PATTERN
    # --------------------------------------------------

    amount_pattern = r"[\d,]+(?:\.\d{1,2})?"

    # --------------------------------------------------
    # TRANSACTION PATTERN
    # --------------------------------------------------

    pattern = re.compile(
        r"^\s*"
        r"(?P<date>" + date_pattern + r")"
        r"\s+"
        r"(?P<description>.+?)"
        r"\s+"
        r"(?P<type>Debit|Credit)"
        r"\s+"
        r"(?P<amount>" + amount_pattern + r")"
        r"\s+"
        r"(?P<balance>" + amount_pattern + r")"
        r"\s*$",
        re.IGNORECASE
    )

    # --------------------------------------------------
    # READ EACH LINE
    # --------------------------------------------------

    for line in lines:

        line = line.strip()

        if not line:
            continue

        match = pattern.match(line)

        if not match:
            continue

        date = match.group("date")
        description = match.group("description")
        txn_type = match.group("type")
        amount = match.group("amount")
        balance = match.group("balance")

        # --------------------------------------------------
        # CLEAN DATA
        # --------------------------------------------------

        date = normalize_date(date)

        description = clean_description(description)

        txn_type = txn_type.capitalize()

        amount = clean_amount(amount)

        balance = clean_amount(balance)

        # --------------------------------------------------
        # STORE TRANSACTION
        # --------------------------------------------------

        transactions.append({
            "date": date,
            "description": description,
            "type": txn_type,
            "amount": amount,
            "balance": balance
        })

    return transactions
