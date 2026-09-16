Azure Data Migration -- Pytest

A Python-based QA project for validating customer data migration into
Azure Blob Storage.

This project demonstrates automated data quality validation,
source-to-target reconciliation, transformation validation, and
migration defect detection using pytest, pandas, and Azure Blob
Storage.

Project Overview

The test scenario simulates a data migration where customer records are:

Read from a source CSV file.

Transformed into the expected target structure.

Uploaded to Azure Blob Storage.

Downloaded from Azure for validation.

Compared using automated reconciliation tests.

The project also includes deliberate defect injection to demonstrate
that automated tests can detect data integrity issues.

Key QA Coverage

Source and target record-count validation

Customer ID preservation

Duplicate customer ID detection

Mandatory-field / NULL validation

Column transformation validation

Country-to-region transformation validation

Financial amount reconciliation

Customer-name reconciliation

Source-to-target record matching

Azure Blob Storage integration

Record-level migration defect detection

Technology Stack

Python 3.9+

pytest

pandas

Azure Blob Storage

Azure Identity

Azure CLI authentication

Git / GitHub

PyCharm

Project Structure

data_migration_pytest/
│
├── data/
│   ├── source/
│   │   └── customers_source.csv
│   └── target/
│       └── customers_target.csv
│
├── src/
│   ├── azure_storage.py
│   └── etl.py
│
├── tests/
│   ├── test_etl.py
│   ├── test_azure_storage.py
│   ├── test_azure_reconciliation.py
│   └── test_defect_detection.py
│
├── .gitignore
└── README.md

Azure Architecture

The current learning environment uses Azure Blob Storage as the cloud
data store.

Local Source CSV
      │
      ▼
Azure Blob Storage
  ┌─────────────┐
  │   source    │
  │ customers_  │
  │ source.csv  │
  └─────────────┘
      │
      │ validation / transformation
      ▼
  ┌─────────────┐
  │   target    │
  │ customers_  │
  │ target.csv  │
  └─────────────┘
      │
      ▼
Automated Pytest
Reconciliation & QA Validation

Azure Authentication

The project uses Azure CLI authentication through AzureCliCredential.

Authenticate before running Azure tests:

az login

Verify the active subscription:

az account show

Installation

Clone the repository:

git clone git@github.com:Amby-git/data_migration_pytest.git
cd data_migration_pytest

Create a virtual environment:

python3 -m venv .venv

Activate it on macOS/Linux:

source .venv/bin/activate

Install dependencies:

pip install pytest pandas azure-storage-blob azure-identity

Running the Tests

Run the complete test suite:

.venv/bin/python -m pytest -v

Run local ETL tests:

.venv/bin/python -m pytest tests/test_etl.py -v

Run Azure Storage validation:

.venv/bin/python -m pytest tests/test_azure_storage.py -v

Run source-to-target reconciliation:

.venv/bin/python -m pytest tests/test_azure_reconciliation.py -v

Run migration defect detection:

.venv/bin/python -m pytest tests/test_defect_detection.py -v

Example Defect Detection

The project deliberately demonstrates a financial data migration defect.

For customer 1004, the source contains:

2100

while the target is deliberately changed to:

9999

The reconciliation test detects the mismatch and reports:

customer_id  amount  amount_eur
1004         2100    9999

This demonstrates that the automated QA suite can identify a specific
record-level data integrity defect rather than simply reporting that a
migration failed.

Current Validation

The project has demonstrated:

Local ETL validation

Azure source validation

Azure source-to-target reconciliation

Intentional financial-data defect detection

The intentionally injected defect is expected to make the relevant
reconciliation test fail. After investigation, the target data can be
restored and the complete suite should return to green.

QA Approach

The validation is layered:

Layer 1 – Local transformation tests
        ↓
Layer 2 – Azure source data validation
        ↓
Layer 3 – Source-to-target reconciliation
        ↓
Layer 4 – Record-level defect detection
        ↓
Future: End-to-end Azure Data Factory validation

This structure is designed to reflect the responsibilities of a Data
Migration QA / ETL Test Engineer.

Future Enhancements

Azure Data Factory pipeline integration

Automated source-to-target migration execution

Missing-record detection

Duplicate-record migration scenarios

Incorrect transformation scenarios

SQL-based reconciliation

CI/CD with GitHub Actions

Automated test reporting

Performance and load testing

Environment-based Azure configuration

Secure Azure authentication and secret management

Author

Ambrose Hastings

Licence

This project is intended as a technical learning and portfolio project.