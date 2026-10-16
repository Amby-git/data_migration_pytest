"""Reusable pytest-bdd steps for customer migration reconciliation features."""

import logging
from pathlib import Path

import pandas as pd
from pytest_bdd import given, parsers, scenario, then, when

from src.reconciliation import validate_customer_migration


PROJECT_ROOT = Path(__file__).resolve().parents[2]
NEGATIVE_FIXTURES_DIR = PROJECT_ROOT / "data" / "fixtures" / "negative"
LOCAL_DATA_FILES = {
    "source": PROJECT_ROOT / "data" / "source" / "customers_source.csv",
    "target": PROJECT_ROOT / "data" / "target" / "customers_target.csv",
}

@scenario("../features/clean_migration.feature", "Validate the clean local customer migration")
def test_clean_migration_feature():
    pass


@scenario("../features/customer_attribute_reconciliation.feature", "Reconcile names and countries")
def test_customer_attribute_reconciliation_feature():
    pass


@scenario("../features/customer_reconciliation.feature", "Reconcile customer population and names")
def test_customer_reconciliation_feature():
    pass


@scenario("../features/financial_data_quality.feature", "Validate positive financial values")
def test_positive_financial_values_feature():
    pass


@scenario("../features/financial_data_quality.feature", "Reconcile migrated financial amounts")
def test_financial_amount_reconciliation_feature():
    pass


@scenario("../features/mandatory_fields.feature", "Validate a required source field")
def test_source_mandatory_fields_feature():
    pass


@scenario("../features/mandatory_fields.feature", "Validate a required target field")
def test_target_mandatory_fields_feature():
    pass


@scenario("../features/negative_reconciliation.feature", "Detect and log a known migration defect")
def test_negative_reconciliation_feature():
    pass


@scenario("../features/source_data_quality.feature", "Validate source population, keys, and mandatory fields")
def test_source_data_quality_feature():
    pass


@scenario("../features/target_transformation.feature", "Validate target schema and country-region business rules")
def test_target_transformation_feature():
    pass


@given(
    parsers.parse('the negative source fixture "{filename}"'),
    target_fixture="source_data",
)
def negative_source_fixture(filename):
    return pd.read_csv(NEGATIVE_FIXTURES_DIR / filename)


@given(
    parsers.parse('the negative target fixture "{filename}"'),
    target_fixture="target_data",
)
def negative_target_fixture(filename):
    return pd.read_csv(NEGATIVE_FIXTURES_DIR / filename)


@given("the local customer source data", target_fixture="source_data")
def local_source_data():
    return pd.read_csv(LOCAL_DATA_FILES["source"])


@given("the local customer target data", target_fixture="target_data")
def local_target_data():
    return pd.read_csv(LOCAL_DATA_FILES["target"])


@when("I validate the customer migration", target_fixture="validation_issues")
def validate_migration(source_data, target_data, caplog):
    caplog.set_level(logging.ERROR, logger="src.reconciliation")
    return validate_customer_migration(source_data, target_data)


@then(parsers.parse('validation finds issue "{issue_code}"'))
def validation_finds_issue(validation_issues, issue_code):
    assert issue_code in {issue.code for issue in validation_issues}


@then(parsers.parse('validation logs issue "{issue_code}"'))
def validation_logs_issue(caplog, issue_code):
    assert issue_code in caplog.text


@then("validation finds no issues")
def validation_finds_no_issues(validation_issues):
    assert validation_issues == []


@then("validation logs no errors")
def validation_logs_no_errors(caplog):
    assert caplog.records == []


def _dataset_for_name(dataset_name, request):
    return request.getfixturevalue(f"{dataset_name}_data")


@then(
    parsers.parse(
        'the {dataset_name} dataset contains {expected_count:d} customer records'
    )
)
def dataset_contains_expected_customer_records(
    dataset_name, expected_count, request
):
    dataset = _dataset_for_name(dataset_name, request)
    assert len(dataset) == expected_count


@then(parsers.parse('the {dataset_name} customer IDs are unique'))
def customer_ids_are_unique(dataset_name, request):
    dataset = _dataset_for_name(dataset_name, request)
    assert dataset["customer_id"].is_unique


@then(
    parsers.parse(
        'the {dataset_name} dataset has no null values in "{column_names}"'
    )
)
def dataset_has_no_null_values(
    dataset_name, column_names, request
):
    dataset = _dataset_for_name(dataset_name, request)
    columns = [column.strip() for column in column_names.split(",")]
    assert dataset[columns].notna().all().all()


@given(
    parsers.parse('the local "{dataset_name}" customer data'),
    target_fixture="selected_dataset_data",
)
def local_customer_dataset(dataset_name):
    return pd.read_csv(LOCAL_DATA_FILES[dataset_name])


@then(
    parsers.parse('the {dataset_name} "{column_name}" values are positive')
)
def dataset_column_values_are_positive(
    dataset_name, column_name, selected_dataset_data
):
    assert (selected_dataset_data[column_name] > 0).all()


@then(parsers.parse('the target uses "{new_column}" instead of "{old_column}"'))
def target_uses_renamed_amount_column(target_data, new_column, old_column):
    assert new_column in target_data.columns
    assert old_column not in target_data.columns


@then(
    parsers.parse(
        'the target maps countries "{country_names}" to region "{expected_region}"'
    )
)
def target_maps_countries_to_region(target_data, country_names, expected_region):
    countries = [country.strip() for country in country_names.split(",")]
    regions = target_data.loc[
        target_data["country"].isin(countries), "country_region"
    ]
    assert not regions.empty
    assert regions.eq(expected_region).all()


def _merged_source_and_target(source_data, target_data):
    return source_data.merge(
        target_data,
        on="customer_id",
        how="inner",
        suffixes=("_source", "_target"),
    )


@then("source and target amounts match by customer ID")
def source_and_target_amounts_match(source_data, target_data):
    merged = _merged_source_and_target(source_data, target_data)
    assert merged["amount"].eq(merged["amount_eur"]).all()


@then("every source customer exists in the target")
def every_source_customer_exists_in_target(source_data, target_data):
    assert set(source_data["customer_id"]).issubset(target_data["customer_id"])


@then("source and target customer names match by customer ID")
def source_and_target_customer_names_match(source_data, target_data):
    merged = _merged_source_and_target(source_data, target_data)
    assert merged["customer_name_source"].eq(merged["customer_name_target"]).all()


@then("source and target countries match by customer ID")
def source_and_target_countries_match(source_data, target_data):
    merged = _merged_source_and_target(source_data, target_data)
    assert merged["country_source"].eq(merged["country_target"]).all()
