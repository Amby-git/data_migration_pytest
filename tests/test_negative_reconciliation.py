import logging
from pathlib import Path

import pandas as pd
import pytest

from src.reconciliation import validate_customer_migration


PROJECT_ROOT = Path(__file__).resolve().parent.parent
NEGATIVE_FIXTURES = PROJECT_ROOT / "data" / "fixtures" / "negative"
SOURCE_FILE = NEGATIVE_FIXTURES / "customers_source.csv"


@pytest.mark.parametrize(
    ("target_filename", "expected_codes"),
    [
        ("target_amount_mismatch.csv", {"AMOUNT_MISMATCH"}),
        (
            "target_missing_customer.csv",
            {"MISSING_TARGET_CUSTOMER", "RECORD_COUNT_MISMATCH"},
        ),
        ("target_duplicate_customer.csv", {"DUPLICATE_TARGET_ID"}),
        ("target_invalid_region.csv", {"INVALID_COUNTRY_REGION"}),
        ("target_null_required_field.csv", {"NULL_REQUIRED_FIELD"}),
        (
            "target_unexpected_customer.csv",
            {"MISSING_TARGET_CUSTOMER", "UNEXPECTED_TARGET_CUSTOMER"},
        ),
    ],
)
def test_negative_fixture_is_detected_and_logged(
    target_filename, expected_codes, caplog
):
    source = pd.read_csv(SOURCE_FILE)
    target = pd.read_csv(NEGATIVE_FIXTURES / target_filename)

    caplog.set_level(logging.ERROR, logger="src.reconciliation")
    issues = validate_customer_migration(source, target)

    detected_codes = {issue.code for issue in issues}
    assert expected_codes.issubset(detected_codes)
    for code in expected_codes:
        assert code in caplog.text


def test_clean_local_migration_logs_no_reconciliation_issues(caplog):
    source = pd.read_csv(PROJECT_ROOT / "data" / "source" / "customers_source.csv")
    target = pd.read_csv(PROJECT_ROOT / "data" / "target" / "customers_target.csv")

    caplog.set_level(logging.ERROR, logger="src.reconciliation")
    issues = validate_customer_migration(source, target)

    assert issues == []
    assert caplog.records == []
