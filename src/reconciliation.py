"""Reusable, logged checks for source-to-target customer migrations."""

from dataclasses import dataclass
import logging

import pandas as pd


logger = logging.getLogger(__name__)

EU_COUNTRIES = {"IE", "DE", "FR"}
REQUIRED_TARGET_COLUMNS = [
    "customer_id",
    "customer_name",
    "country",
    "amount_eur",
    "country_region",
]


@dataclass(frozen=True)
class ValidationIssue:
    """A data-quality problem found during reconciliation."""

    code: str
    message: str


def _report(issues, code, message):
    issue = ValidationIssue(code=code, message=message)
    issues.append(issue)
    logger.error("%s: %s", issue.code, issue.message)


def validate_customer_migration(source, target):
    """Return and log every detected source-to-target data-quality issue."""
    issues = []

    missing_columns = set(REQUIRED_TARGET_COLUMNS) - set(target.columns)
    if missing_columns:
        _report(
            issues,
            "MISSING_TARGET_COLUMNS",
            f"Target is missing required columns: {sorted(missing_columns)}",
        )
        return issues

    duplicate_ids = sorted(
        target.loc[target["customer_id"].duplicated(), "customer_id"].unique().tolist()
    )
    if duplicate_ids:
        _report(
            issues,
            "DUPLICATE_TARGET_ID",
            f"Duplicate target customer IDs: {duplicate_ids}",
        )

    null_columns = [
        column for column in REQUIRED_TARGET_COLUMNS if target[column].isna().any()
    ]
    if null_columns:
        _report(
            issues,
            "NULL_REQUIRED_FIELD",
            f"Target contains null values in: {null_columns}",
        )

    source_ids = set(source["customer_id"])
    target_ids = set(target["customer_id"])
    missing_ids = sorted(source_ids - target_ids)
    unexpected_ids = sorted(target_ids - source_ids)

    if missing_ids:
        _report(
            issues,
            "MISSING_TARGET_CUSTOMER",
            f"Source customer IDs missing from target: {missing_ids}",
        )
    if unexpected_ids:
        _report(
            issues,
            "UNEXPECTED_TARGET_CUSTOMER",
            f"Target has customer IDs not present in source: {unexpected_ids}",
        )
    if len(source) != len(target):
        _report(
            issues,
            "RECORD_COUNT_MISMATCH",
            f"Source has {len(source)} records; target has {len(target)} records",
        )

    merged = source.merge(
        target,
        on="customer_id",
        how="inner",
        suffixes=("_source", "_target"),
    )

    amount_mismatches = merged.loc[
        merged["amount"] != merged["amount_eur"], "customer_id"
    ].tolist()
    if amount_mismatches:
        _report(
            issues,
            "AMOUNT_MISMATCH",
            f"Amount differs for customer IDs: {amount_mismatches}",
        )

    name_mismatches = merged.loc[
        merged["customer_name_source"] != merged["customer_name_target"],
        "customer_id",
    ].tolist()
    if name_mismatches:
        _report(
            issues,
            "CUSTOMER_NAME_MISMATCH",
            f"Customer name differs for customer IDs: {name_mismatches}",
        )

    country_mismatches = merged.loc[
        merged["country_source"] != merged["country_target"], "customer_id"
    ].tolist()
    if country_mismatches:
        _report(
            issues,
            "COUNTRY_MISMATCH",
            f"Country differs for customer IDs: {country_mismatches}",
        )

    expected_regions = merged["country_target"].map(
        lambda country: "EU" if country in EU_COUNTRIES else "UK"
    )
    invalid_region_ids = merged.loc[
        merged["country_region"] != expected_regions, "customer_id"
    ].tolist()
    if invalid_region_ids:
        _report(
            issues,
            "INVALID_COUNTRY_REGION",
            f"Country region is invalid for customer IDs: {invalid_region_ids}",
        )

    return issues
