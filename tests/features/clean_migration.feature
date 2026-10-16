Feature: Clean customer migration reconciliation
  A valid local migration must produce no reconciliation errors.

  @test_1
  Scenario: Validate the clean local customer migration
    Given the local customer source data
    And the local customer target data
    When I validate the customer migration
    Then validation finds no issues
    And validation logs no errors
