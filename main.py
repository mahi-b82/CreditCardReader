import os
import pandas as pd

from parser.pdf_reader import read_pdf
from processing.transaction_parser import parse_transactions
from processing.ai_classifier import ai_categorize_transaction
from reports.excel_generator import generate_excel


PDF_PATH = "sample_statements/fresh_sample_statement.pdf"
OUTPUT_PATH = "output/statement.xlsx"


def main():
    if not os.path.exists(PDF_PATH):
        print(f"PDF not found: {PDF_PATH}")
        return

    text = read_pdf(PDF_PATH)
    transactions = parse_transactions(text)

    if not transactions:
        print("No transactions detected.")
        return

    for transaction in transactions:
        result = ai_categorize_transaction(
            transaction["description"]
        )

        transaction["merchant"] = result["merchant"]
        transaction["category"] = result["category"]
        transaction["classification_method"] = (
            result["method"]
        )

    df = pd.DataFrame(transactions)

    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%b-%Y"
    )

    os.makedirs("output", exist_ok=True)

    generate_excel(df, OUTPUT_PATH)

    print(f"Transactions Found: {len(df)}")
    print(f"Excel report created: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()