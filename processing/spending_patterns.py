import pandas as pd


def analyze_spending_patterns(transactions):
    """
    Analyze spending behaviour from transaction data.

    Returns:
        Dictionary containing:
        - total_spending
        - average_transaction
        - largest_transaction
        - smallest_transaction
        - spending_by_category
        - spending_by_month
        - most_frequent_category
        - most_expensive_category
    """

    # --------------------------------------------------
    # CONVERT DATA TO DATAFRAME
    # --------------------------------------------------

    if not transactions:
        return {
            "total_spending": 0,
            "average_transaction": 0,
            "largest_transaction": 0,
            "smallest_transaction": 0,
            "spending_by_category": {},
            "spending_by_month": {},
            "most_frequent_category": "None",
            "most_expensive_category": "None"
        }

    df = pd.DataFrame(transactions)

    # --------------------------------------------------
    # KEEP ONLY DEBIT TRANSACTIONS
    # --------------------------------------------------

    if "type" in df.columns:

        df = df[
            df["type"].astype(str).str.lower() == "debit"
        ].copy()

    if df.empty:
        return {
            "total_spending": 0,
            "average_transaction": 0,
            "largest_transaction": 0,
            "smallest_transaction": 0,
            "spending_by_category": {},
            "spending_by_month": {},
            "most_frequent_category": "None",
            "most_expensive_category": "None"
        }

    # --------------------------------------------------
    # CLEAN AMOUNTS
    # --------------------------------------------------

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(subset=["amount"])

    if df.empty:
        return {
            "total_spending": 0,
            "average_transaction": 0,
            "largest_transaction": 0,
            "smallest_transaction": 0,
            "spending_by_category": {},
            "spending_by_month": {},
            "most_frequent_category": "None",
            "most_expensive_category": "None"
        }

    # --------------------------------------------------
    # BASIC SPENDING STATISTICS
    # --------------------------------------------------

    total_spending = df["amount"].sum()

    average_transaction = df["amount"].mean()

    largest_transaction = df["amount"].max()

    smallest_transaction = df["amount"].min()

    # --------------------------------------------------
    # CATEGORY ANALYSIS
    # --------------------------------------------------

    if "category" in df.columns:

        spending_by_category = (
            df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
            .to_dict()
        )

        category_frequency = (
            df["category"]
            .value_counts()
        )

        most_frequent_category = (
            category_frequency.index[0]
            if not category_frequency.empty
            else "None"
        )

        most_expensive_category = (
            max(
                spending_by_category,
                key=spending_by_category.get
            )
            if spending_by_category
            else "None"
        )

    else:

        spending_by_category = {}
        most_frequent_category = "None"
        most_expensive_category = "None"

    # --------------------------------------------------
    # MONTHLY SPENDING
    # --------------------------------------------------

    spending_by_month = {}

    if "date" in df.columns:

        dates = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        monthly_df = df.copy()

        monthly_df["date"] = dates

        monthly_df = monthly_df.dropna(
            subset=["date"]
        )

        if not monthly_df.empty:

            monthly_df["month"] = (
                monthly_df["date"]
                .dt.strftime("%B %Y")
            )

            spending_by_month = (
                monthly_df
                .groupby("month")["amount"]
                .sum()
                .to_dict()
            )

    # --------------------------------------------------
    # RETURN ANALYSIS
    # --------------------------------------------------

    return {
        "total_spending": float(total_spending),
        "average_transaction": float(average_transaction),
        "largest_transaction": float(largest_transaction),
        "smallest_transaction": float(smallest_transaction),
        "spending_by_category": spending_by_category,
        "spending_by_month": spending_by_month,
        "most_frequent_category": most_frequent_category,
        "most_expensive_category": most_expensive_category
    }