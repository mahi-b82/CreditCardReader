import re


def clean_amount(amount_text):
    """
    Convert an amount such as ₹22,118.64 into a float.
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


def find_transaction_line(lines, transaction):
    """
    Find the exact transaction line using date and description.
    """

    date = transaction.get("date", "")
    description = transaction.get("description", "")

    if not date or not description:
        return None

    date_match = re.match(
        r"(\d{2})-([A-Za-z]{3})-(\d{4})",
        date
    )

    if not date_match:
        return None

    day = date_match.group(1)
    month = date_match.group(2).upper()

    date_prefix = f"{day}-{month}-"

    for index, line in enumerate(lines):

        upper_line = line.upper()

        if (
            date_prefix in upper_line
            and description.upper() in upper_line
        ):
            return index

    return None


def extract_gst_details(lines, transaction_index):
    """
    Extract GST details appearing immediately after
    a transaction.
    """

    details = {
        "has_gst": False,
        "gst_rate": None,
        "gst_base_amount": None,
        "gst_cgst": None,
        "gst_sgst": None,
        "gst_igst": None,
        "gst_type": None
    }

    following_text = " ".join(
        line.strip()
        for line in lines[
            transaction_index + 1:
            transaction_index + 3
        ]
        if line.strip()
    )

    # --------------------------------------------------
    # BASE AMOUNT
    # --------------------------------------------------

    base_match = re.search(
        r"Base:\s*₹?\s*([\d,]+(?:\.\d{1,2})?)",
        following_text,
        re.IGNORECASE
    )

    if base_match:

        details["gst_base_amount"] = clean_amount(
            base_match.group(1)
        )

        details["has_gst"] = True
        details["gst_type"] = "Embedded GST"

    # --------------------------------------------------
    # CGST
    # --------------------------------------------------

    cgst_match = re.search(
        r"CGST\s*\(([\d.]+)%\)\s*:\s*₹?\s*([\d,]+(?:\.\d{1,2})?)",
        following_text,
        re.IGNORECASE
    )

    if cgst_match:

        details["gst_rate"] = float(
            cgst_match.group(1)
        )

        details["gst_cgst"] = clean_amount(
            cgst_match.group(2)
        )

        details["has_gst"] = True
        details["gst_type"] = "Embedded GST"

    # --------------------------------------------------
    # SGST
    # --------------------------------------------------

    sgst_match = re.search(
        r"SGST\s*\(([\d.]+)%\)\s*:\s*₹?\s*([\d,]+(?:\.\d{1,2})?)",
        following_text,
        re.IGNORECASE
    )

    if sgst_match:

        if details["gst_rate"] is None:
            details["gst_rate"] = float(
                sgst_match.group(1)
            )

        details["gst_sgst"] = clean_amount(
            sgst_match.group(2)
        )

        details["has_gst"] = True
        details["gst_type"] = "Embedded GST"

    # --------------------------------------------------
    # IGST
    # --------------------------------------------------

    igst_match = re.search(
        r"IGST\s*\(([\d.]+)%\)\s*:\s*₹?\s*([\d,]+(?:\.\d{1,2})?)",
        following_text,
        re.IGNORECASE
    )

    if igst_match:

        details["gst_rate"] = float(
            igst_match.group(1)
        )

        details["gst_igst"] = clean_amount(
            igst_match.group(2)
        )

        details["has_gst"] = True
        details["gst_type"] = "Embedded GST"

    return details


def detect_standalone_gst(transaction):
    """
    Detect transactions where GST itself is charged
    as a separate transaction.
    """

    description = transaction.get(
        "description",
        ""
    ).upper()

    gst_info = {
        "has_gst": False,
        "gst_rate": None,
        "gst_base_amount": None,
        "gst_cgst": None,
        "gst_sgst": None,
        "gst_igst": None,
        "gst_type": None
    }

    if "GST" not in description:
        return gst_info

    gst_info["has_gst"] = True
    gst_info["gst_type"] = "Standalone GST"

    rate_match = re.search(
        r"\((\d+(?:\.\d+)?)%\)",
        description
    )

    if rate_match:

        gst_info["gst_rate"] = float(
            rate_match.group(1)
        )

    return gst_info


def detect_gst_transactions(transactions, text=None):
    """
    Detect both embedded and standalone GST.

    Embedded GST:
    GST details attached to a purchase/service transaction.

    Standalone GST:
    GST charged as a separate transaction.
    """

    gst_transactions = []

    lines = []

    if text:
        lines = text.splitlines()

    for transaction in transactions:

        # --------------------------------------------------
        # START WITH DEFAULT GST INFORMATION
        # --------------------------------------------------

        gst_info = {
            "has_gst": False,
            "gst_rate": None,
            "gst_base_amount": None,
            "gst_cgst": None,
            "gst_sgst": None,
            "gst_igst": None,
            "gst_type": None
        }

        # --------------------------------------------------
        # STANDALONE GST
        # --------------------------------------------------

        standalone_info = detect_standalone_gst(
            transaction
        )

        if standalone_info["has_gst"]:

            gst_info.update(
                standalone_info
            )

            # IMPORTANT:
            # Standalone GST rows are already complete.
            # Do not search the following PDF lines because
            # those lines belong to other transactions.

            enriched_transaction = transaction.copy()

            enriched_transaction.update(
                gst_info
            )

            gst_transactions.append(
                enriched_transaction
            )

            continue

        # --------------------------------------------------
        # EMBEDDED GST
        # --------------------------------------------------

        if lines:

            transaction_index = find_transaction_line(
                lines,
                transaction
            )

            if transaction_index is not None:

                embedded_info = extract_gst_details(
                    lines,
                    transaction_index
                )

                if embedded_info["has_gst"]:

                    gst_info.update(
                        embedded_info
                    )

        # --------------------------------------------------
        # SAVE RESULT
        # --------------------------------------------------

        enriched_transaction = transaction.copy()

        enriched_transaction.update(
            gst_info
        )

        gst_transactions.append(
            enriched_transaction
        )

    return gst_transactions