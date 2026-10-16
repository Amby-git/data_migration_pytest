Feature: Source customer data quality
  The local migration source must meet its baseline data-quality contract.

  @test
  Scenario: Validate source population, keys, and mandatory fields
    Given the local customer source data
    Then the source dataset contains 100 customer records
    And the source customer IDs are unique
    And the source dataset has no null values in "customer_id, customer_name, country, amount"
