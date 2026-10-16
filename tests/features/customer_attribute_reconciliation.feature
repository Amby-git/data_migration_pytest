Feature: Customer attribute reconciliation
  Customer identity attributes must remain unchanged during migration.

  @test
  Scenario: Reconcile names and countries
    Given the local customer source data
    And the local customer target data
    Then source and target customer names match by customer ID
    And source and target countries match by customer ID
