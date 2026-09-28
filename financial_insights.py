def generate_financial_insights(
    df,
    patterns,
    unusual_transactions
):
    insights = []

    if patterns:
        highest_category = patterns["highest_category"]
        highest_amount = patterns["highest_category_amount"]
        percentage = patterns["top_category_percentage"]

        insights.append(
            f"Your highest spending category is "
            f"{highest_category}, accounting for "
            f"{percentage:.2f}% of total spending "
            f"(₹{highest_amount:,.2f})."
        )

        insights.append(
            f"Your average debit transaction amount is "
            f"₹{patterns['average_debit']:,.2f}."
        )

        insights.append(
            f"Your largest debit transaction was "
            f"₹{patterns['largest_debit']:,.2f}."
        )

        insights.append(
            f"Your most frequent spending category is "
            f"{patterns['most_frequent_category']} "
            f"with {patterns['most_frequent_count']} "
            f"transactions."
        )

    if unusual_transactions.empty:
        insights.append(
            "No unusually large debit transactions "
            "were detected."
        )
    else:
        insights.append(
            f"{len(unusual_transactions)} unusual "
            f"transaction(s) were detected based "
            f"on the spending threshold."
        )

    return insights