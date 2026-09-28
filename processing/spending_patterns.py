def analyze_spending_patterns(df):
    debit_df = df[
        df["type"] == "Debit"
    ].copy()

    if debit_df.empty:
        return {}

    total_spending = debit_df["amount"].sum()

    if total_spending <= 0:
        return {}

    category_totals = (
        debit_df
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    category_counts = (
        debit_df
        .groupby("category")["amount"]
        .count()
        .sort_values(ascending=False)
    )

    highest_category = category_totals.index[0]
    highest_category_amount = category_totals.iloc[0]

    most_frequent_category = category_counts.index[0]
    most_frequent_count = category_counts.iloc[0]

    average_debit = debit_df["amount"].mean()
    largest_debit = debit_df["amount"].max()

    top_category_percentage = (
        highest_category_amount / total_spending
    ) * 100

    return {
        "total_spending": total_spending,
        "average_debit": average_debit,
        "largest_debit": largest_debit,
        "number_of_categories": len(category_totals),
        "highest_category": highest_category,
        "highest_category_amount": highest_category_amount,
        "top_category_percentage": top_category_percentage,
        "most_frequent_category": most_frequent_category,
        "most_frequent_count": int(most_frequent_count)
    }