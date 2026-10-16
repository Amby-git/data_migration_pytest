# Azure Data Migration – Pytest

A Python-based QA project for validating customer data migration into Azure Blob Storage.

This project demonstrates automated data quality validation, source-to-target reconciliation, transformation validation, and migration defect detection using **pytest**, **pandas**, and **Azure Blob Storage**.

---

## Project Overview

The test scenario simulates a data migration where customer records are:

1. Read from a source CSV file.
2. Transformed into the expected target structure.
3. Uploaded to Azure Blob Storage.
4. Downloaded from Azure for validation.
5. Compared using automated reconciliation tests.

The project also includes deliberate defect injection to demonstrate that automated tests can detect data integrity issues.

---

## Key QA Coverage

- Source and target record-count validation
- Customer ID preservation
- Duplicate customer ID detection
- Mandatory-field / NULL validation
- Column transformation validation
- Country-to-region transformation validation
- Financial amount reconciliation
- Customer-name reconciliation
- Source-to-target record matching
- Azure Blob Storage integration
- Record-level migration defect detection

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.9+ | Test automation and data processing |
| pytest | Automated testing framework |
| pandas | Data manipulation and reconciliation |
| Azure Blob Storage | Cloud source and target data storage |
| Azure Identity | Azure authentication |
| Azure CLI | Local Azure authentication |
| Git / GitHub | Source control |
| PyCharm | Development environment |

---

## Project Structure

```text
data_migration_pytest/
│
├── data/
│   ├── fixtures/
│   │   └── negative/              # Isolated negative-scenario CSV fixtures
│   ├── source/
│   │   └── customers_source.csv
│   │
│   └── target/
│       └── customers_target.csv
│
├── src/
│   ├── azure_storage.py
│   ├── etl.py
│   └── reconciliation.py          # Reusable logged reconciliation checks
│
├── tests/
│   ├── test_etl.py
│   ├── test_azure_storage.py
│   ├── test_azure_reconciliation.py
│   ├── test_defect_detection.py
│   ├── test_negative_reconciliation.py
│   ├── bdd/
│       └── test_reconciliation_steps.py
│   └── features/
│       ├── clean_migration.feature
│       ├── customer_attribute_reconciliation.feature
│       ├── customer_reconciliation.feature
│       ├── financial_data_quality.feature
│       ├── mandatory_fields.feature
│       ├── negative_reconciliation.feature
│       ├── source_data_quality.feature
│       └── target_transformation.feature
│
├── .gitignore
└── README.md
````

---

## Azure Architecture

The current learning environment uses Azure Blob Storage as the cloud data store.

```text
┌──────────────────────────┐
│     Local Source CSV     │
│ customers_source.csv     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Azure Blob Storage     │
│                          │
│  ┌────────────────────┐  │
│  │      source        │  │
│  │ customers_source   │  │
│  │       .csv         │  │
│  └─────────┬──────────┘  │
│            │             │
│            │ validation  │
│            │ / transform │
│            ▼             │
│  ┌────────────────────┐  │
│  │      target        │  │
│  │ customers_target   │  │
│  │       .csv         │  │
│  └─────────┬──────────┘  │
└────────────┼─────────────┘
             │
             ▼
┌──────────────────────────┐
│      Automated Pytest    │
│                          │
│  Data Quality Validation │
│  Reconciliation          │
│  Defect Detection        │
└──────────────────────────┘
```

---

## Azure Authentication

The project uses Azure CLI authentication through `AzureCliCredential`.

Authenticate with Azure:

```bash
az login
```

Verify the active subscription:

```bash
az account show
```

The Azure CLI must be available in the Python execution environment.

---

## Installation

### Clone the repository

```bash
git clone git@github.com:Amby-git/data_migration_pytest.git
cd data_migration_pytest
```

### Create a virtual environment

```bash
python3 -m venv .venv
```

### Activate the virtual environment

macOS / Linux:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install pytest pandas azure-storage-blob azure-identity
```

---

## Running the Tests

### Run the complete test suite

```bash
.venv/bin/python -m pytest -v
```

### Run local ETL tests

```bash
.venv/bin/python -m pytest tests/test_etl.py -v
```

### Run Azure Storage validation

```bash
.venv/bin/python -m pytest tests/test_azure_storage.py -v
```

### Run source-to-target reconciliation

```bash
.venv/bin/python -m pytest tests/test_azure_reconciliation.py -v
```

### Run migration defect detection

```bash
.venv/bin/python -m pytest tests/test_defect_detection.py -v
```

---

## Data Reconciliation

The reconciliation tests validate that migrated records preserve critical business data.

The current validation includes:

* Record count
* Customer IDs
* Customer names
* Financial amounts
* Country values
* Country-to-region transformation
* Mandatory fields
* Duplicate records

For example:

```text
Source                         Target

customer_id: 1004             customer_id: 1004
amount:       2100             amount_eur: 2100
country:      DE               country:      DE
```

The test suite compares these values automatically.

---

## Negative Scenario Fixtures and Logging

The main Azure source and target blobs contain valid migration data. Deliberately
invalid CSV fixtures live under data/fixtures/negative so defect tests remain
repeatable and never corrupt Azure test data.

The logged validator detects:

* Amount mismatches
* Missing or unexpected target customers
* Duplicate target customer IDs
* Invalid country-to-region mappings
* Null mandatory target fields

Every detected defect is logged with a stable code, for example:

    ERROR src.reconciliation AMOUNT_MISMATCH: Amount differs for customer IDs: [2002]

Run the negative tests with log output enabled:

    .venv/bin/python -m pytest tests/test_negative_reconciliation.py -v --log-cli-level=ERROR

Each negative test passes only when it detects and logs its expected defect.

---

## BDD with Cucumber-Style Gherkin

The project uses pytest-bdd, which runs Gherkin feature files through pytest.
Feature files in tests/features describe business-readable scenarios; reusable Python
steps in tests/bdd/test_reconciliation_steps.py load CSV data, call the shared
validator, and assert the detected log events.

The reusable steps cover data population, key uniqueness, null checks, schema
renaming, amount reconciliation, name reconciliation, source-to-target
presence, and country-to-region mappings.

Run all BDD scenarios:

    .venv/bin/python -m pytest tests/bdd -v --log-cli-level=ERROR

The feature scenarios use only local fixtures and local CSVs. They do not
modify Azure Blob Storage.

---

## QA Approach

The validation is implemented in multiple layers:

```text
Layer 1
Local transformation validation
        │
        ▼
Layer 2
Azure source data validation
        │
        ▼
Layer 3
Source-to-target reconciliation
        │
        ▼
Layer 4
Record-level defect detection
        │
        ▼
Future
End-to-end Azure Data Factory validation
```

This layered approach is designed to reflect the responsibilities of a **Data Migration QA / ETL Test Engineer**.

---

## Test Scenarios

The project currently covers the following scenarios:

| Test Area        | Validation                                             |
| ---------------- | ------------------------------------------------------ |
| Record count     | Source and target record counts match                  |
| Customer IDs     | IDs are preserved                                      |
| Uniqueness       | Duplicate IDs are detected                             |
| Mandatory fields | NULL values are detected                               |
| Amounts          | Financial values are reconciled                        |
| Customer names   | Names are preserved                                    |
| Transformation   | Country-to-region mapping is validated                 |
| Azure            | Source and target data are retrieved from Blob Storage |
| Defects          | Record-level migration defects are detected            |

---

## Current Validation

The project has successfully demonstrated:

* Local ETL validation
* Azure Blob Storage integration
* Azure source data validation
* Source-to-target reconciliation
* Financial data reconciliation
* Record-level defect detection
* Isolated negative-fixture validation with structured log output

---

## Future Enhancements

The next stages of the project include:

* Azure Data Factory pipeline integration
* Automated source-to-target migration execution
* Missing-record detection
* Duplicate-record migration scenarios
* Incorrect transformation scenarios
* SQL-based reconciliation
* CI/CD with GitHub Actions
* Automated test reporting
* Performance and load testing
* Environment-based Azure configuration
* Secure Azure authentication and secret management

---

## Portfolio Objective

This project is designed as a practical demonstration of skills relevant to:

* Data Migration QA
* ETL Testing
* Data Validation
* Data Reconciliation
* API and cloud-based testing
* Azure testing
* Python test automation
* SQL validation
* CI/CD
* Defect detection

The project will progressively evolve towards an end-to-end Azure Data Factory migration testing framework.

---

## Author

**Ambrose Hastings**

---

## Licence

This project is intended as a technical learning and portfolio project.
