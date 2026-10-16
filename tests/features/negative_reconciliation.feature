Feature: Negative customer migration reconciliation
  Data-quality defects must be detected and logged without changing Azure data.

  Background:
    Given the negative source fixture "customers_source.csv"

  @test
  Scenario Outline: Detect and log a known migration defect
    Given the negative target fixture "<target_fixture>"
    When I validate the customer migration
    Then validation finds issue "<issue_code>"
    And validation logs issue "<issue_code>"
    Examples:
      | target_fixture                 | issue_code                 |
      | target_amount_mismatch.csv     | AMOUNT_MISMATCH            |
      | target_missing_customer.csv    | MISSING_TARGET_CUSTOMER    |
      | target_duplicate_customer.csv  | DUPLICATE_TARGET_ID        |
      | target_invalid_region.csv      | INVALID_COUNTRY_REGION     |
      | target_null_required_field.csv | NULL_REQUIRED_FIELD        |
      | target_unexpected_customer.csv | UNEXPECTED_TARGET_CUSTOMER |
