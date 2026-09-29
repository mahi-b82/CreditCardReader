import re


def clean_amount(amount_text):
    """
    Convert an amount such as ₹3,950.00 into a float.
    """

    amount_text = str(amount_text)

    amount_text = (
        amount_text
        .replace(",", "")
        .replace("₹", "")
        .replace(" ", "")
        .strip()
    )

    try:
        return float(amount_text)
    except ValueError:
        return None


def extract_emi_details(lines, transaction_index):
    """
    Extract Principal, Interest and GST details
    from the lines following an EMI transaction.
    """

    details = {
        "emi_principal": None,
        "emi_interest": None,
        "emi_gst": None
    }

    # Look at the next few lines because PDF extraction
    # may split EMI details across multiple lines.

    following_text = " ".join(
        line.strip()
        for line in lines[
            transaction_index + 1:
            transaction_index + 4
        ]
        if line.strip()
    )

    # --------------------------------------------------
    # PRINCIPAL
    # --------------------------------------------------

    principal_match = re.search(
        r"Principal:\s*₹?\s*([\d,]+(?:\.\d{1,2})?)",
        following_text,
        re.IGNORECASE
    )

    if principal_match:

        details["emi_principal"] = clean_amount(
            principal_match.group(1)
        )

    # --------------------------------------------------
    # INTEREST
    # --------------------------------------------------

    interest_match = re.search(
        r"Interest:\s*₹?\s*([\d,]+(?:\.\d{1,2})?)",
        following_text,
        re.IGNORECASE
    )

    if interest_match:

        details["emi_interest"] = clean_amount(
            interest_match.group(1)
        )

    # --------------------------------------------------
    # GST ON INTEREST
    # --------------------------------------------------

    gst_match = re.search(
        r"GST\s+on\s+Interest\s*\(18%\)\s*:\s*₹?\s*([\d,]+(?:\.\d{1,2})?)",
        following_text,
        re.IGNORECASE
    )

    if gst_match:

        details["emi_gst"] = clean_amount(
            gst_match.group(1)
        )

    return details


def detect_emi_transactions(transactions, text=None):
    """
    Detect actual EMI installment transactions.

    Also extracts:
    - EMI installment number
    - EMI tenure
    - Principal
    - Interest
    - GST on interest

    EMI processing fees and GST charges are excluded.
    """

    emi_transactions = []

    lines = []

    if text:
        lines = text.splitlines()

    for transaction in transactions:

        description = transaction.get(
            "description",
            ""
        ).upper()

        emi_info = {
            "is_emi": False,
            "emi_tenure": None,
            "emi_installment": None,
            "emi_principal": None,
            "emi_interest": None,
            "emi_gst": None
        }

        # --------------------------------------------------
        # ACTUAL EMI DETECTION
        # --------------------------------------------------

        tenure_match = re.search(
            r"\b(\d{1,2})\s*/\s*(\d{1,2})\b",
            description
        )

        if (
            "EMI" in description
            and tenure_match
        ):

            emi_info["is_emi"] = True

            emi_info["emi_installment"] = int(
                tenure_match.group(1)
            )

            emi_info["emi_tenure"] = int(
                tenure_match.group(2)
            )

            # --------------------------------------------------
            # FIND ORIGINAL TRANSACTION LINE
            # --------------------------------------------------

            if lines:

                for index, line in enumerate(lines):

                    if description in line.upper():

                        details = extract_emi_details(
                            lines,
                            index
                        )

                        emi_info.update(
                            details
                        )

                        break

        enriched_transaction = transaction.copy()

        enriched_transaction.update(
            emi_info
        )

        emi_transactions.append(
            enriched_transaction
        )

    return emi_transactions