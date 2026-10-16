Feature: Financial migration data quality
  Financial values must be present, positive, and preserved by the migration.

  @test
  Scenario Outline: Validate positive financial values
    Given the local "<dataset_name>" customer data
    Then the <dataset_name> "<column_name>" values are positive

    Examples:
      | dataset_name | column_name |
      | source       | amount      |
      | target       | amount_eur  |

  @test
  Scenario: Reconcile migrated financial amounts
    Given the local customer source data
    And the local customer target data
    Then source and target amounts match by customer ID
