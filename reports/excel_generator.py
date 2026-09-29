import os
import pandas as pd


def generate_excel(
    df,
    output_path,
    emi_transactions=None,
    gst_transactions=None
):
    """
    Generate an Excel report containing:
    - Transactions
    - Summary
    - Spending Analysis
    - Monthly Analysis
    - EMI Analysis
    - GST Analysis
    """

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True
    )

    # --------------------------------------------------
    # PREPARE BASIC DATA
    # --------------------------------------------------

    debit_df = df[
        df["type"] == "Debit"
    ].copy()

    credit_df = df[
        df["type"] == "Credit"
    ].copy()

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    emi_count = 0
    gst_count = 0

    if emi_transactions is not None:
        emi_count = sum(
            transaction.get("is_emi", False)
            for transaction in emi_transactions
        )

    if gst_transactions is not None:
        gst_count = sum(
            transaction.get("has_gst", False)
            for transaction in gst_transactions
        )

    summary = pd.DataFrame({
        "Metric": [
            "Total Transactions",
            "Total Debit",
            "Total Credit",
            "Largest Transaction",
            "EMI Transactions",
            "GST Transactions"
        ],
        "Value": [
            len(df),
            debit_df["amount"].sum(),
            credit_df["amount"].sum(),
            df["amount"].max()
            if not df.empty
            else 0,
            emi_count,
            gst_count
        ]
    })

    # --------------------------------------------------
    # EXCEL WRITER
    # --------------------------------------------------

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl"
    ) as writer:

        # --------------------------------------------------
        # TRANSACTIONS SHEET
        # --------------------------------------------------

        df.to_excel(
            writer,
            sheet_name="Transactions",
            index=False
        )

        # --------------------------------------------------
        # SUMMARY SHEET
        # --------------------------------------------------

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        # --------------------------------------------------
        # SPENDING ANALYSIS
        # --------------------------------------------------

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

        # --------------------------------------------------
        # MONTHLY ANALYSIS
        # --------------------------------------------------

        monthly_df = debit_df.copy()

        if not monthly_df.empty:

            monthly_df["month"] = (
                pd.to_datetime(
                    monthly_df["date"],
                    errors="coerce"
                )
                .dt.strftime("%B %Y")
            )

            monthly = (
                monthly_df
                .dropna(subset=["month"])
                .groupby("month")["amount"]
                .sum()
                .reset_index()
            )

            monthly.to_excel(
                writer,
                sheet_name="Monthly Analysis",
                index=False
            )

        # --------------------------------------------------
        # EMI ANALYSIS
        # --------------------------------------------------

        if emi_transactions is not None:

            emi_df = pd.DataFrame(
                emi_transactions
            )

            if not emi_df.empty:

                emi_df = emi_df[
                    emi_df["is_emi"] == True
                ].copy()

                if not emi_df.empty:

                    emi_display = emi_df[
                        [
                            "date",
                            "description",
                            "amount",
                            "emi_tenure",
                            "emi_installment",
                            "emi_principal",
                            "emi_interest",
                            "emi_gst"
                        ]
                    ].copy()

                    emi_display = emi_display.rename(
                        columns={
                            "date": "Date",
                            "description": "Description",
                            "amount": "EMI Amount",
                            "emi_tenure": "Tenure",
                            "emi_installment": "Installment",
                            "emi_principal": "Principal",
                            "emi_interest": "Interest",
                            "emi_gst": "GST on Interest"
                        }
                    )

                    emi_display.to_excel(
                        writer,
                        sheet_name="EMI Analysis",
                        index=False
                    )

        # --------------------------------------------------
        # GST ANALYSIS
        # --------------------------------------------------

        if gst_transactions is not None:

            gst_df = pd.DataFrame(
                gst_transactions
            )

            if not gst_df.empty:

                gst_df = gst_df[
                    gst_df["has_gst"] == True
                ].copy()

                if not gst_df.empty:

                    gst_display = gst_df[
                        [
                            "date",
                            "description",
                            "amount",
                            "gst_type",
                            "gst_rate",
                            "gst_base_amount",
                            "gst_cgst",
                            "gst_sgst",
                            "gst_igst"
                        ]
                    ].copy()

                    gst_display = gst_display.rename(
                        columns={
                            "date": "Date",
                            "description": "Description",
                            "amount": "Transaction Amount",
                            "gst_type": "GST Type",
                            "gst_rate": "GST Rate",
                            "gst_base_amount": "Taxable Base",
                            "gst_cgst": "CGST",
                            "gst_sgst": "SGST",
                            "gst_igst": "IGST"
                        }
                    )

                    gst_display.to_excel(
                        writer,
                        sheet_name="GST Analysis",
                        index=False
                    )

    return output_path