Feature: Customer migration reconciliation
  A complete migration preserves the intended customer population and key attributes.

  @test
  Scenario: Reconcile customer population and names
    Given the local customer source data
    And the local customer target data
    Then the target dataset contains 100 customer records
    And the target customer IDs are unique
    And every source customer exists in the target
    And source and target customer names match by customer ID
