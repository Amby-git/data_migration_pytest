Feature: Mandatory customer fields
  Required source and target fields must always contain a value.

  @test
  Scenario Outline: Validate a required source field
    Given the local customer source data
    Then the source dataset has no null values in "<column_name>"
    Examples:
      | column_name   |
      | customer_id   |
      | customer_name |
      | country       |
      | amount        |

  @test
  Scenario Outline: Validate a required target field
    Given the local customer target data
    Then the target dataset has no null values in "<column_name>"
    Examples:
      | column_name    |
      | customer_id    |
      | customer_name  |
      | country        |
      | amount_eur     |
      | country_region |
