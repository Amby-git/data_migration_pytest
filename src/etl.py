import pandas as pd
from pathlib import Path


SOURCE_FILE = Path(__file__).parent.parent / "data" / "source" / "customers_source.csv"
TARGET_FILE = Path(__file__).parent.parent / "data" / "target" / "customers_target.csv"


def transform_customers():
    df = pd.read_csv(SOURCE_FILE)

    # Rename the amount column to make the target schema explicit
    df = df.rename(columns={"amount": "amount_eur"})

    # Add a derived field based on the customer's country
    df["country_region"] = df["country"].apply(
        lambda country: "EU" if country in ["IE", "DE", "FR"] else "UK"
    )

    df.to_csv(TARGET_FILE, index=False)

    return df


if __name__ == "__main__":
    result = transform_customers()
    print(result)