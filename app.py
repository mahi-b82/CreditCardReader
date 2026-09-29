import os
import tempfile
import pandas as pd
import streamlit as st

from parser.pdf_reader import read_pdf
from processing.transaction_parser import parse_transactions
from processing.ai_classifier import ai_categorize_transaction
from processing.anomaly_detector import detect_unusual_transactions
from processing.spending_patterns import analyze_spending_patterns
from processing.financial_insights import generate_financial_insights
from reports.excel_generator import generate_excel
from processing.emi_detector import detect_emi_transactions
from processing.gst_detector import detect_gst_transactions


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Credit Card Statement Analyzer",
    page_icon="💳",
    layout="wide"
)


# ==================================================
# HEADER
# ==================================================

st.title("💳 Credit Card Statement Analyzer")
st.caption(
    "Intelligent analysis of bank and credit card statements"
)

st.divider()


# ==================================================
# PDF UPLOAD
# ==================================================

st.header("📤 Upload Statement")

uploaded_file = st.file_uploader(
    "Choose your credit card statement",
    type=["pdf"]
)

if uploaded_file is None:
    st.info("Upload a PDF statement to begin analysis.")
    st.stop()


# ==================================================
# PDF EXTRACTION
# ==================================================

temp_pdf_path = None

try:
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_pdf_path = temp_file.name

    text = read_pdf(temp_pdf_path)

finally:
    if temp_pdf_path and os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)


# ==================================================
# TRANSACTION PARSING
# ==================================================

transactions = parse_transactions(text)

emi_transactions = detect_emi_transactions(
    transactions,
    text
)

gst_transactions = detect_gst_transactions(
    transactions,
    text
)

if not transactions:
    st.error(
        "No transactions were detected. "
        "Please check the PDF format."
    )
    st.stop()


# ==================================================
# TRANSACTION CLASSIFICATION
# ==================================================

for transaction in transactions:
    result = ai_categorize_transaction(
        transaction["description"]
    )

    transaction["merchant"] = result["merchant"]
    transaction["category"] = result["category"]
    transaction["classification_method"] = (
        result["method"]
    )


# ==================================================
# DATAFRAME
# ==================================================

df = pd.DataFrame(transactions)

df["date"] = pd.to_datetime(
    df["date"],
    format="%d-%b-%Y",
    errors="coerce"
)

debit_df = df[
    df["type"] == "Debit"
].copy()

credit_df = df[
    df["type"] == "Credit"
].copy()


# ==================================================
# EMI DATAFRAME
# ==================================================

emi_df = pd.DataFrame(emi_transactions)

if not emi_df.empty:
    emi_df["date"] = pd.to_datetime(
        emi_df["date"],
        format="%d-%b-%Y",
        errors="coerce"
    )

    emi_df = emi_df[
        emi_df["is_emi"] == True
    ].copy()


# ==================================================
# GST DATAFRAME
# ==================================================

gst_df = pd.DataFrame(gst_transactions)

if not gst_df.empty:
    gst_df["date"] = pd.to_datetime(
        gst_df["date"],
        format="%d-%b-%Y",
        errors="coerce"
    )

    gst_df = gst_df[
        gst_df["has_gst"] == True
    ].copy()


# ==================================================
# FINANCIAL OVERVIEW
# ==================================================

total_transactions = len(df)
total_debit = debit_df["amount"].sum()
total_credit = credit_df["amount"].sum()

largest_transaction = (
    df["amount"].max()
    if not df.empty
    else 0
)

st.success(
    f"Successfully processed {total_transactions} transactions."
)

st.header("📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Transactions",
    total_transactions
)

col2.metric(
    "Total Spending",
    f"₹{total_debit:,.2f}"
)

col3.metric(
    "Total Credits",
    f"₹{total_credit:,.2f}"
)

col4.metric(
    "Largest Transaction",
    f"₹{largest_transaction:,.2f}"
)


# ==================================================
# DASHBOARD TABS
# ==================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Transactions",
    "📊 Spending Analysis",
    "⚠️ Unusual Spending",
    "💡 Financial Insights",
    "🤖 AI Classification"
])


# ==================================================
# TAB 1: TRANSACTIONS
# ==================================================

with tab1:

    # --------------------------------------------------
    # ALL TRANSACTIONS
    # --------------------------------------------------

    st.subheader("All Transactions")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Transactions CSV",
        data=csv_data,
        file_name="transactions.csv",
        mime="text/csv"
    )

    st.divider()

    # --------------------------------------------------
    # EMI DETAILS
    # --------------------------------------------------

    st.subheader("💳 EMI Details")

    emi_count = len(emi_df)

    st.metric(
        "EMI Transactions Detected",
        emi_count
    )

    if emi_df.empty:

        st.info(
            "No EMI transactions were detected in this statement."
        )

    else:

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

        st.dataframe(
            emi_display,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # --------------------------------------------------
    # GST DETAILS
    # --------------------------------------------------

    st.subheader("🧾 GST Details")

    gst_count = len(gst_df)

    st.metric(
        "GST Transactions Detected",
        gst_count
    )

    if gst_df.empty:

        st.info(
            "No GST-related transactions were detected in this statement."
        )

    else:

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

        st.dataframe(
            gst_display,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# TAB 2: SPENDING ANALYSIS
# ==================================================

with tab2:

    # --------------------------------------------------
    # CREDIT & DEBIT SUMMARY
    # --------------------------------------------------

    st.subheader("💳 Transaction Summary")

    debit_count = len(debit_df)
    credit_count = len(credit_df)

    net_amount = total_debit - total_credit

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Debit",
        f"₹{total_debit:,.2f}"
    )

    col2.metric(
        "Total Credit",
        f"₹{total_credit:,.2f}"
    )

    col3.metric(
        "Debit Transactions",
        debit_count
    )

    col4.metric(
        "Credit Transactions",
        credit_count
    )

    col5.metric(
        "Net Amount",
        f"₹{net_amount:,.2f}"
    )

    st.divider()

    # --------------------------------------------------
    # CREDIT TRANSACTIONS
    # --------------------------------------------------

    st.subheader("💰 Credits / Adjustments")

    if credit_df.empty:

        st.info("No credit transactions found.")

    else:

        credit_display = credit_df[
            [
                "date",
                "description",
                "amount",
                "balance"
            ]
        ].copy()

        credit_display = credit_display.rename(
            columns={
                "date": "Date",
                "description": "Description",
                "amount": "Amount",
                "balance": "Balance"
            }
        )

        st.dataframe(
            credit_display,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # --------------------------------------------------
    # CATEGORY-WISE SPENDING
    # --------------------------------------------------

    st.subheader("Category-wise Spending")

    if debit_df.empty:

        st.info("No debit transactions found.")

    else:

        category_analysis = (
            debit_df
            .groupby("category")
            .agg(
                total_spending=("amount", "sum"),
                transaction_count=("amount", "count"),
                average_transaction=("amount", "mean")
            )
            .sort_values(
                "total_spending",
                ascending=False
            )
        )

        category_analysis["percentage"] = (
            category_analysis["total_spending"]
            / category_analysis["total_spending"].sum()
            * 100
        )

        st.dataframe(
            category_analysis,
            use_container_width=True
        )

        st.subheader("Spending by Category")

        st.bar_chart(
            category_analysis["total_spending"]
        )

        st.divider()

        # --------------------------------------------------
        # MONTHLY SPENDING
        # --------------------------------------------------

        st.subheader("Monthly Spending")

        monthly_df = debit_df.dropna(
            subset=["date"]
        ).copy()

        monthly_df["month"] = (
            monthly_df["date"].dt.strftime("%B %Y")
        )

        monthly_analysis = (
            monthly_df
            .groupby("month")
            .agg(
                total_spending=("amount", "sum"),
                transaction_count=("amount", "count"),
                average_transaction=("amount", "mean")
            )
        )

        st.dataframe(
            monthly_analysis,
            use_container_width=True
        )


# ==================================================
# TAB 3: UNUSUAL SPENDING
# ==================================================

with tab3:

    st.subheader("Unusual Transaction Detection")

    unusual_transactions = (
        detect_unusual_transactions(df)
    )

    if unusual_transactions.empty:

        st.success(
            "No unusually large debit transactions detected."
        )

    else:

        st.warning(
            f"{len(unusual_transactions)} unusual "
            "transaction(s) detected."
        )

        st.dataframe(
            unusual_transactions,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("Spending Patterns")

    patterns = analyze_spending_patterns(df)

    if patterns:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average Debit",
            f"₹{patterns['average_debit']:,.2f}"
        )

        col2.metric(
            "Largest Debit",
            f"₹{patterns['largest_debit']:,.2f}"
        )

        col3.metric(
            "Categories Used",
            patterns["number_of_categories"]
        )

        st.write(
            f"**Highest Spending Category:** "
            f"{patterns['highest_category']} "
            f"(₹{patterns['highest_category_amount']:,.2f})"
        )

        st.write(
            f"**Most Frequent Category:** "
            f"{patterns['most_frequent_category']} "
            f"({patterns['most_frequent_count']} transactions)"
        )

    else:

        st.info(
            "Not enough debit data to calculate spending patterns."
        )


# ==================================================
# TAB 4: FINANCIAL INSIGHTS
# ==================================================

with tab4:

    st.subheader("Automatic Financial Insights")

    patterns = analyze_spending_patterns(df)

    unusual_transactions = (
        detect_unusual_transactions(df)
    )

    insights = generate_financial_insights(
        df,
        patterns,
        unusual_transactions
    )

    if insights:

        for insight in insights:
            st.info(f"💡 {insight}")

    else:

        st.info(
            "No financial insights are available."
        )


# ==================================================
# TAB 5: AI CLASSIFICATION
# ==================================================

with tab5:

    st.subheader("Intelligent Transaction Classification")

    st.write(
        "Transactions are categorized using merchant "
        "recognition and contextual keyword recognition."
    )

    st.dataframe(
        df[
            [
                "description",
                "merchant",
                "category",
                "classification_method"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# EXCEL REPORT
# ==================================================

st.divider()

st.header("📥 Export Report")

if st.button("Generate Excel Report"):

    output_path = os.path.join(
        "output",
        "statement.xlsx"
    )

    try:

        generate_excel(
            df,
            output_path,
            emi_transactions,
            gst_transactions
        )

        with open(output_path, "rb") as excel_file:

            st.download_button(
                label="Download Excel Report",
                data=excel_file,
                file_name="statement.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )

        st.success(
            "Excel report generated successfully."
        )

    except Exception as error:

        st.error(
            f"Could not generate Excel report: {error}"
        )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Credit Card Statement Analyzer | "
    "Automated Financial Analysis"
)