import pandas as pd


def analyze_spending_patterns(transactions):
    """
    Analyze spending behaviour from transaction data.

    Accepts either:
    - A list of transaction dictionaries
    - A pandas DataFrame

    Returns a dictionary containing spending statistics
    used by the Streamlit dashboard.
    """

    # --------------------------------------------------
    # HANDLE EMPTY / INVALID INPUT
    # --------------------------------------------------

    if transactions is None:
        return {
            "total_spending": 0,
            "average_transaction": 0,
            "largest_transaction": 0,
            "smallest_transaction": 0,
            "spending_by_category": {},
            "spending_by_month": {},
            "most_frequent_category": "None",
            "most_expensive_category": "None",
            "average_debit": 0,
            "largest_debit": 0,
            "number_of_categories": 0,
            "highest_category": "None",
            "highest_category_amount": 0,
            "most_frequent_count": 0
        }

    # --------------------------------------------------
    # CONVERT DATA TO DATAFRAME
    # --------------------------------------------------

    if isinstance(transactions, pd.DataFrame):

        df = transactions.copy()

    else:

        if not transactions:
            return {
                "total_spending": 0,
                "average_transaction": 0,
                "largest_transaction": 0,
                "smallest_transaction": 0,
                "spending_by_category": {},
                "spending_by_month": {},
                "most_frequent_category": "None",
                "most_expensive_category": "None",
                "average_debit": 0,
                "largest_debit": 0,
                "number_of_categories": 0,
                "highest_category": "None",
                "highest_category_amount": 0,
                "most_frequent_count": 0
            }

        df = pd.DataFrame(transactions)

    # --------------------------------------------------
    # EMPTY DATAFRAME CHECK
    # --------------------------------------------------

    if df.empty:
        return {
            "total_spending": 0,
            "average_transaction": 0,
            "largest_transaction": 0,
            "smallest_transaction": 0,
            "spending_by_category": {},
            "spending_by_month": {},
            "most_frequent_category": "None",
            "most_expensive_category": "None",
            "average_debit": 0,
            "largest_debit": 0,
            "number_of_categories": 0,
            "highest_category": "None",
            "highest_category_amount": 0,
            "most_frequent_count": 0
        }

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
            "most_expensive_category": "None",
            "average_debit": 0,
            "largest_debit": 0,
            "number_of_categories": 0,
            "highest_category": "None",
            "highest_category_amount": 0,
            "most_frequent_count": 0
        }

    # --------------------------------------------------
    # CLEAN AMOUNTS
    # --------------------------------------------------

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["amount"]
    )

    if df.empty:
        return {
            "total_spending": 0,
            "average_transaction": 0,
            "largest_transaction": 0,
            "smallest_transaction": 0,
            "spending_by_category": {},
            "spending_by_month": {},
            "most_frequent_category": "None",
            "most_expensive_category": "None",
            "average_debit": 0,
            "largest_debit": 0,
            "number_of_categories": 0,
            "highest_category": "None",
            "highest_category_amount": 0,
            "most_frequent_count": 0
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

    spending_by_category = {}

    most_frequent_category = "None"

    most_expensive_category = "None"

    most_frequent_count = 0

    highest_category = "None"

    highest_category_amount = 0

    number_of_categories = 0

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

        if not category_frequency.empty:

            most_frequent_category = (
                category_frequency.index[0]
            )

            most_frequent_count = int(
                category_frequency.iloc[0]
            )

        if spending_by_category:

            most_expensive_category = max(
                spending_by_category,
                key=spending_by_category.get
            )

            highest_category = (
                most_expensive_category
            )

            highest_category_amount = float(
                spending_by_category[
                    most_expensive_category
                ]
            )

        number_of_categories = len(
            spending_by_category
        )

    # --------------------------------------------------
    # MONTHLY SPENDING
    # --------------------------------------------------

    spending_by_month = {}

    if "date" in df.columns:

        monthly_df = df.copy()

        monthly_df["date"] = pd.to_datetime(
            monthly_df["date"],
            errors="coerce"
        )

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
        "total_spending": float(
            total_spending
        ),
        "average_transaction": float(
            average_transaction
        ),
        "largest_transaction": float(
            largest_transaction
        ),
        "smallest_transaction": float(
            smallest_transaction
        ),
        "spending_by_category": spending_by_category,
        "spending_by_month": spending_by_month,
        "most_frequent_category": (
            most_frequent_category
        ),
        "most_expensive_category": (
            most_expensive_category
        ),

        # Keys used by Streamlit Tab 3
        "average_debit": float(
            average_transaction
        ),
        "largest_debit": float(
            largest_transaction
        ),
        "number_of_categories": (
            number_of_categories
        ),
        "highest_category": (
            highest_category
        ),
        "highest_category_amount": float(
            highest_category_amount
        ),
        "most_frequent_count": (
            most_frequent_count
        )
    }