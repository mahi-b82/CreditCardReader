import re
from datetime import datetime


def normalize_date(date_text):
    """
    Convert common statement date formats into DD-MMM-YYYY.
    """

    date_text = date_text.strip()

    date_formats = [
        "%d-%b-%Y",
        "%d-%B-%Y",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%d %b %Y",
        "%d %B %Y",
    ]

    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(
                date_text,
                date_format
            )

            return parsed_date.strftime(
                "%d-%b-%Y"
            )

        except ValueError:
            continue

    return date_text


def clean_amount(amount_text):
    """
    Convert statement amounts into float values.
    """

    amount_text = str(amount_text).strip()

    amount_text = (
        amount_text
        .replace(",", "")
        .replace(" ", "")
    )

    amount_text = re.sub(
        r"[₹$€£]",
        "",
        amount_text
    )

    return float(amount_text)


def clean_description(description):
    """
    Clean extra spaces and unwanted characters.
    """

    description = str(description).strip()

    description = re.sub(
        r"\s+",
        " ",
        description
    )

    return description


def parse_transactions(text):

    transactions = []

    lines = text.splitlines()

    # --------------------------------------------------
    # STEP 1: JOIN SPLIT YEAR LINES
    # --------------------------------------------------

    processed_lines = []

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # HDFC-style statements may place the year
        # on the following line.
        #
        # Example:
        #
        # 01-SEP- SWIGGY ... Debit 450.00 18,900.00
        # 2026 Base: ₹428.57 | CGST...
        #
        # We only need the year for the transaction.
        # The GST/EMI information is left untouched
        # for future GST/EMI analysis.

        date_match = re.match(
            r"^(\d{2}-[A-Za-z]{3})-\s+",
            line
        )

        if (
            date_match
            and i + 1 < len(lines)
        ):

            next_line = lines[i + 1].strip()

            year_match = re.match(
                r"^(\d{4})\b",
                next_line
            )

            if year_match:

                year = year_match.group(1)

                line = re.sub(
                    r"^(\d{2}-[A-Za-z]{3})-\s+",
                    r"\1-" + year + " ",
                    line,
                    count=1
                )

                i += 1

        processed_lines.append(line)

        i += 1

    # --------------------------------------------------
    # STEP 2: TRANSACTION DATE PATTERN
    # --------------------------------------------------

    date_pattern = (
        r"(?:"
        r"\d{2}-[A-Za-z]{3}-\d{4}"
        r"|"
        r"\d{2}-[A-Za-z]+-\d{4}"
        r"|"
        r"\d{2}/\d{2}/\d{4}"
        r"|"
        r"\d{2}-\d{2}-\d{4}"
        r"|"
        r"\d{2}\.\d{2}\.\d{4}"
        r"|"
        r"\d{2} [A-Za-z]{3} \d{4}"
        r"|"
        r"\d{2} [A-Za-z]+ \d{4}"
        r")"
    )

    amount_pattern = (
        r"[\d,]+(?:\.\d{1,2})?"
    )

    # --------------------------------------------------
    # STEP 3: TRANSACTION PATTERN
    # --------------------------------------------------

    pattern = re.compile(
        r"^\s*"
        r"(?P<date>"
        + date_pattern
        + r")"
        r"\s+"
        r"(?P<description>.+?)"
        r"\s+"
        r"(?P<type>Debit|Credit)"
        r"\s+"
        r"(?P<amount>"
        + amount_pattern
        + r")"
        r"\s+"
        r"(?P<balance>"
        + amount_pattern
        + r")"
        r"\s*$",
        re.IGNORECASE
    )

    # --------------------------------------------------
    # STEP 4: PARSE TRANSACTIONS
    # --------------------------------------------------

    for line in processed_lines:

        match = pattern.match(line)

        if not match:
            continue

        date = match.group("date")
        description = match.group(
            "description"
        )
        txn_type = match.group("type")
        amount = match.group("amount")
        balance = match.group("balance")

        date = normalize_date(date)

        description = clean_description(
            description
        )

        txn_type = txn_type.capitalize()

        amount = clean_amount(amount)

        balance = clean_amount(balance)

        transactions.append(
            {
                "date": date,
                "description": description,
                "type": txn_type,
                "amount": amount,
                "balance": balance
            }
        )

    return transactions