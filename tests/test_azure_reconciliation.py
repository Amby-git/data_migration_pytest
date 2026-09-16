import pandas as pd

from src.azure_storage import (
    download_source_as_dataframe,
    download_target_as_dataframe
)


def test_source_and_target_record_counts_match():
    """
    Validate that no records were lost or unexpectedly added.
    """
    source = download_source_as_dataframe()
    target = download_target_as_dataframe()

    assert len(source) == len(target)


def test_all_source_customer_ids_exist_in_target():
    """
    Validate that every source customer exists in the target.
    """
    source = download_source_as_dataframe()
    target = download_target_as_dataframe()

    source_ids = set(source["customer_id"])
    target_ids = set(target["customer_id"])

    missing_ids = source_ids - target_ids

    assert not missing_ids, (
        f"Customers missing from target: {missing_ids}"
    )


def test_target_customer_ids_are_unique():
    """
    Validate target primary-key uniqueness.
    """
    target = download_target_as_dataframe()

    assert target["customer_id"].is_unique


def test_target_mandatory_fields_are_not_null():
    """
    Validate mandatory target fields.
    """
    target = download_target_as_dataframe()

    required_columns = [
        "customer_id",
        "customer_name",
        "country",
        "amount_eur",
        "country_region"
    ]

    for column in required_columns:
        assert target[column].notna().all(), (
            f"NULL value found in mandatory column: {column}"
        )


def test_amount_values_are_preserved():
    """
    Validate that the financial amount was not changed
    during the migration.
    """
    source = download_source_as_dataframe()
    target = download_target_as_dataframe()

    source_amounts = (
        source[["customer_id", "amount"]]
        .rename(columns={"amount": "amount_eur"})
        .sort_values("customer_id")
        .reset_index(drop=True)
    )

    target_amounts = (
        target[["customer_id", "amount_eur"]]
        .sort_values("customer_id")
        .reset_index(drop=True)
    )

    pd.testing.assert_frame_equal(
        source_amounts,
        target_amounts
    )


def test_country_region_transformation_is_correct():
    """
    Validate the business transformation rule:

    IE, DE, FR -> EU
    UK          -> UK
    """
    target = download_target_as_dataframe()

    eu_countries = ["IE", "DE", "FR"]

    for country in eu_countries:
        actual_regions = target.loc[
            target["country"] == country,
            "country_region"
        ]

        assert actual_regions.eq("EU").all(), (
            f"Incorrect region mapping for {country}"
        )

    uk_regions = target.loc[
        target["country"] == "UK",
        "country_region"
    ]

    assert uk_regions.eq("UK").all()


def test_source_and_target_customer_names_match():
    """
    Validate that customer names were not changed.
    """
    source = download_source_as_dataframe()
    target = download_target_as_dataframe()

    source_names = (
        source[["customer_id", "customer_name"]]
        .sort_values("customer_id")
        .reset_index(drop=True)
    )

    target_names = (
        target[["customer_id", "customer_name"]]
        .sort_values("customer_id")
        .reset_index(drop=True)
    )

    pd.testing.assert_frame_equal(
        source_names,
        target_names
    )
