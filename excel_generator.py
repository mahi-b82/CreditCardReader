import os
import pandas as pd


def generate_excel(df, output_path):
    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True
    )

    debit_df = df[
        df["type"] == "Debit"
    ].copy()

    credit_df = df[
        df["type"] == "Credit"
    ].copy()

    summary = pd.DataFrame({
        "Metric": [
            "Total Transactions",
            "Total Debit",
            "Total Credit",
            "Largest Transaction"
        ],
        "Value": [
            len(df),
            debit_df["amount"].sum(),
            credit_df["amount"].sum(),
            df["amount"].max() if not df.empty else 0
        ]
    })

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Transactions",
            index=False
        )

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        if not debit_df.empty:
            category = (
                debit_df
                .groupby("category")["amount"]
                .sum()
                .reset_index()
                .sort_values(
                    "amount",
                    ascending=False
                )
            )

            category.to_excel(
                writer,
                sheet_name="Spending Analysis",
                index=False
            )

        monthly_df = debit_df.copy()

        if not monthly_df.empty:
            monthly_df["month"] = (
                pd.to_datetime(monthly_df["date"])
                .dt.strftime("%B %Y")
            )

            monthly = (
                monthly_df
                .groupby("month")["amount"]
                .sum()
                .reset_index()
            )

            monthly.to_excel(
                writer,
                sheet_name="Monthly Analysis",
                index=False
            )

    return output_path
