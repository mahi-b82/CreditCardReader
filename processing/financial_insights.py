def generate_financial_insights(
    df,
    patterns,
    unusual_transactions
):
    """
    Generate automatic financial insights
    from transaction and spending analysis.
    """

    insights = []

    # ==================================================
    # BASIC SPENDING INSIGHTS
    # ==================================================

    if patterns:

        total_spending = patterns.get(
            "total_spending",
            0
        )

        average_transaction = patterns.get(
            "average_transaction",
            0
        )

        largest_transaction = patterns.get(
            "largest_transaction",
            0
        )

        smallest_transaction = patterns.get(
            "smallest_transaction",
            0
        )

        most_frequent_category = patterns.get(
            "most_frequent_category",
            "None"
        )

        most_expensive_category = patterns.get(
            "most_expensive_category",
            "None"
        )

        spending_by_category = patterns.get(
            "spending_by_category",
            {}
        )

        # --------------------------------------------------
        # TOTAL SPENDING
        # --------------------------------------------------

        if total_spending > 0:

            insights.append(
                f"Total debit spending was "
                f"₹{total_spending:,.2f}."
            )

        # --------------------------------------------------
        # AVERAGE TRANSACTION
        # --------------------------------------------------

        if average_transaction > 0:

            insights.append(
                f"Your average debit transaction "
                f"amount was ₹{average_transaction:,.2f}."
            )

        # --------------------------------------------------
        # LARGEST TRANSACTION
        # --------------------------------------------------

        if largest_transaction > 0:

            insights.append(
                f"Your largest debit transaction was "
                f"₹{largest_transaction:,.2f}."
            )

        # --------------------------------------------------
        # SMALLEST TRANSACTION
        # --------------------------------------------------

        if smallest_transaction > 0:

            insights.append(
                f"Your smallest debit transaction was "
                f"₹{smallest_transaction:,.2f}."
            )

        # --------------------------------------------------
        # MOST FREQUENT CATEGORY
        # --------------------------------------------------

        if most_frequent_category != "None":

            insights.append(
                f"Your most frequent spending category "
                f"was {most_frequent_category}."
            )

        # --------------------------------------------------
        # HIGHEST SPENDING CATEGORY
        # --------------------------------------------------

        if spending_by_category:

            highest_category = max(
                spending_by_category,
                key=spending_by_category.get
            )

            highest_amount = spending_by_category[
                highest_category
            ]

            if total_spending > 0:

                percentage = (
                    highest_amount
                    / total_spending
                    * 100
                )

            else:

                percentage = 0

            insights.append(
                f"{highest_category} was your highest "
                f"spending category, accounting for "
                f"{percentage:.2f}% of total spending "
                f"(₹{highest_amount:,.2f})."
            )

        # --------------------------------------------------
        # CATEGORY CONCENTRATION
        # --------------------------------------------------

        if len(spending_by_category) >= 2:

            sorted_categories = sorted(
                spending_by_category.items(),
                key=lambda x: x[1],
                reverse=True
            )

            first_category = sorted_categories[0]
            second_category = sorted_categories[1]

            insights.append(
                f"Your top two spending categories were "
                f"{first_category[0]} and "
                f"{second_category[0]}."
            )

    # ==================================================
    # UNUSUAL TRANSACTION INSIGHT
    # ==================================================

    if unusual_transactions is None:

        pass

    elif unusual_transactions.empty:

        insights.append(
            "No unusually large debit transactions "
            "were detected."
        )

    else:

        unusual_count = len(
            unusual_transactions
        )

        largest_unusual = (
            unusual_transactions["amount"].max()
        )

        insights.append(
            f"{unusual_count} unusually large "
            f"transaction(s) were detected."
        )

        insights.append(
            f"The largest unusual transaction was "
            f"₹{largest_unusual:,.2f}."
        )

    # ==================================================
    # CREDIT INSIGHT
    # ==================================================

    if df is not None and not df.empty:

        credit_df = df[
            df["type"].astype(str).str.lower()
            == "credit"
        ]

        if not credit_df.empty:

            total_credit = credit_df[
                "amount"
            ].sum()

            insights.append(
                f"The statement contains "
                f"₹{total_credit:,.2f} in credits, "
                f"such as refunds, payments or "
                f"adjustments."
            )

    # ==================================================
    # FALLBACK
    # ==================================================

    if not insights:

        insights.append(
            "Not enough transaction data was available "
            "to generate financial insights."
        )

    return insights