import pandas as pd


def detect_unusual_transactions(df):
    """
    Detect unusually large debit transactions.

    A transaction is considered unusual when:
    1. It is greater than 2x the average debit amount, OR
    2. It is among the largest transactions in the statement.

    Returns a DataFrame containing unusual transactions
    and the reason for detection.
    """

    # --------------------------------------------------
    # KEEP ONLY DEBIT TRANSACTIONS
    # --------------------------------------------------

    if df.empty:
        return pd.DataFrame(
            columns=list(df.columns) + ["reason"]
        )

    debit_df = df[
        df["type"].astype(str).str.lower() == "debit"
    ].copy()

    if debit_df.empty:
        debit_df["reason"] = pd.Series(
            dtype="object"
        )
        return debit_df

    # --------------------------------------------------
    # CLEAN AMOUNTS
    # --------------------------------------------------

    debit_df["amount"] = pd.to_numeric(
        debit_df["amount"],
        errors="coerce"
    )

    debit_df = debit_df.dropna(
        subset=["amount"]
    )

    if debit_df.empty:
        debit_df["reason"] = pd.Series(
            dtype="object"
        )
        return debit_df

    # --------------------------------------------------
    # CALCULATE SPENDING THRESHOLD
    # --------------------------------------------------

    average_amount = debit_df["amount"].mean()

    threshold = average_amount * 2

    # --------------------------------------------------
    # FIND UNUSUAL TRANSACTIONS
    # --------------------------------------------------

    unusual = debit_df[
        debit_df["amount"] > threshold
    ].copy()

    # --------------------------------------------------
    # ADD REASONS
    # --------------------------------------------------

    reasons = []

    for _, transaction in unusual.iterrows():

        amount = transaction["amount"]

        if amount > average_amount * 3:

            reasons.append(
                "Transaction amount is more than "
                "3x the average debit"
            )

        else:

            reasons.append(
                "Transaction amount is more than "
                "2x the average debit"
            )

    unusual["reason"] = reasons

    # --------------------------------------------------
    # SORT BY AMOUNT
    # --------------------------------------------------

    unusual = unusual.sort_values(
        by="amount",
        ascending=False
    )

    return unusual
