import argparse
import logging
import pandas as pd
import re

# defining available data
sample_files = {
    "small": "sample_data/raw_customers_small.csv",
    "large": "sample_data/raw_customers_large.csv"
}

# set up argparse
parser = argparse.ArgumentParser(description = "Data Cleanup and Validation Automation")

# choose between two sample filesets...
parser.add_argument(
    "--data",
    choices=sample_files.keys(),
    default="small",
    help="Select which sample data to process (default: small)"
)

# ... or provide a custom dataset
parser.add_argument(
    "--file",
    type=str,
    help="Path to a custom CSV file to clean."
)

# parse argument, if applicable
args = parser.parse_args()
if args.file:
    input_data = args.file
else:
    input_data = sample_files[args.data]
    print(f"Processing data: {args.data} ({input_data})")

# set up logging
logging.basicConfig(
    filename="process.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# set up email validation
EMAIL_REGEX = r"^[^@]+@[^@]+\.[^@]+$"
def is_valid_email(email):
    return bool(re.match(EMAIL_REGEX, str(email)))

def main():
    df = pd.read_csv(input_data)
    original_count = len(df)

    # Drop exact duplicates
    df = df.drop_duplicates()
    count_after_dupes = len(df)
    dupe_count = original_count - count_after_dupes

    # Required fields
    df = df.dropna(subset=["customer_id", "email", "signup_date"])
    count_after_required = len(df)
    required_count = count_after_dupes - count_after_required

    # Email validation
    df = df[df["email"].apply(is_valid_email)]
    count_after_email = len(df)
    email_count = count_after_required - count_after_email


    # Normalize dates
    df["signup_date"] = pd.to_datetime(
        df["signup_date"], errors="coerce"
    )
    df = df.dropna(subset=["signup_date"])
    count_after_date = len(df)
    date_count = count_after_email - count_after_date

    cleaned_count = len(df)
    df.to_csv("output/clean_customers.csv", index=False)

    # Write summary log
    with open("output/summary_report.txt", "w") as f:
        f.write(f"Dataset cleaned: {input_data}\n")
        f.write(f"Original rows: {original_count}\n")
        f.write(f"Cleaned rows: {cleaned_count}\n")
        f.write(f"Rows removed: {original_count - cleaned_count}\n")
        f.write(f"- Duplicate rows: {dupe_count}\n")
        f.write(f"- Missing required fields: {required_count}\n")
        f.write(f"- Invalid email: {email_count}\n")
        f.write(f"- Invalid date: {date_count}\n")


    logging.info("Data cleanup completed successfully.")

if __name__ == "__main__":
    main()