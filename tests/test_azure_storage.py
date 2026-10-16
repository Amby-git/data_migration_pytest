import pandas as pd
from pathlib import Path

from src.azure_storage import download_source_as_dataframe


SOURCE_FILE = Path(__file__).resolve().parent.parent / "data" / "source" / "customers_source.csv"
EXPECTED_CUSTOMER_IDS = set(range(1001, 1101))


def test_azure_source_record_count():
    df = download_source_as_dataframe()

    assert len(df) == len(EXPECTED_CUSTOMER_IDS)


def test_azure_source_customer_ids_are_unique():
    df = download_source_as_dataframe()

    assert df["customer_id"].is_unique


def test_azure_source_has_required_columns():
    df = download_source_as_dataframe()

    required_columns = {
        "customer_id",
        "customer_name",
        "country",
        "amount"
    }

    assert required_columns.issubset(df.columns)


def test_azure_source_mandatory_fields_are_not_null():
    df = download_source_as_dataframe()

    assert df["customer_id"].notna().all()
    assert df["customer_name"].notna().all()
    assert df["country"].notna().all()
    assert df["amount"].notna().all()


def test_azure_source_customer_ids_are_valid():
    df = download_source_as_dataframe()

    assert set(df["customer_id"]) == EXPECTED_CUSTOMER_IDS


def test_azure_source_matches_local_source():
    azure_df = download_source_as_dataframe()

    local_df = pd.read_csv(SOURCE_FILE)

    pd.testing.assert_frame_equal(
        azure_df.reset_index(drop=True),
        local_df.reset_index(drop=True)
    )
