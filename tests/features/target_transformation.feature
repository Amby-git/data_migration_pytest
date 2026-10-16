Feature: Customer target transformation
  Source customers must be transformed into the expected target schema.

  @test
  Scenario: Validate target schema and country-region business rules
    Given the local customer source data
    And the local customer target data
    Then the target uses "amount_eur" instead of "amount"
    And the target maps countries "IE, DE, FR" to region "EU"
    And the target maps countries "UK" to region "UK"
    And source and target amounts match by customer ID
