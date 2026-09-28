
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


# ==================================================
# TAB 2: SPENDING ANALYSIS
# ==================================================

with tab2:
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
            output_path
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

        st.success("Excel report generated successfully.")

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