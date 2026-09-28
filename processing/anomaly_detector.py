def detect_unusual_transactions(df):
    debit_df = df[
        df["type"] == "Debit"
    ].copy()

    if debit_df.empty:
        debit_df["reason"] = []
        return debit_df

    average_amount = debit_df["amount"].mean()
    threshold = average_amount * 2

    unusual = debit_df[
        debit_df["amount"] > threshold
    ].copy()

    unusual["reason"] = (
        "Transaction amount is more than "
        "2x the average debit"
    )

    return unusual