import pandas as pd

from src.azure_storage import (
    download_source_as_dataframe,
    download_target_as_dataframe
)


def test_amount_mismatch_is_detected():
    source = download_source_as_dataframe()
    target = download_target_as_dataframe()

    merged = source[["customer_id", "amount"]].merge(
        target[["customer_id", "amount_eur"]],
        on="customer_id",
        how="inner"
    )

    mismatches = merged[
        merged["amount"] != merged["amount_eur"]
    ]

    assert mismatches.empty, (
        f"Amount mismatches detected:\n{mismatches}"
    )