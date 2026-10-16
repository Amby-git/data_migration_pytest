import pandas as pd
from pathlib import Path

from src.etl import transform_customers


SOURCE_FILE = Path(__file__).resolve().parent.parent / "data" / "source" / "customers_source.csv"

def test_source_and_target_record_count_match():
    source = pd.read_csv(SOURCE_FILE)
    target = transform_customers()

    assert len(source) == len(target)


def test_customer_ids_are_preserved():
    source = pd.read_csv(SOURCE_FILE)
    target = transform_customers()

    assert source["customer_id"].tolist() == target["customer_id"].tolist()


def test_customer_ids_are_unique():
    target = transform_customers()

    assert target["customer_id"].is_unique


def test_mandatory_fields_are_not_null():
    target = transform_customers()

    assert target["customer_id"].notna().all()
    assert target["customer_name"].notna().all()
    assert target["country"].notna().all()
    assert target["amount_eur"].notna().all()


def test_amount_column_was_renamed_correctly():
    target = transform_customers()

    assert "amount_eur" in target.columns
    assert "amount" not in target.columns


def test_country_region_transformation():
    target = transform_customers()

    assert target.loc[target["country"] == "IE", "country_region"].eq("EU").all()
    assert target.loc[target["country"] == "DE", "country_region"].eq("EU").all()
    assert target.loc[target["country"] == "FR", "country_region"].eq("EU").all()
    assert target.loc[target["country"] == "UK", "country_region"].eq("UK").all()