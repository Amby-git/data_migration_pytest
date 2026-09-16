import os
from pathlib import Path
from io import BytesIO

# Make Azure CLI available to the Python process started by PyCharm
os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("PATH", "")

from azure.identity import AzureCliCredential
from azure.storage.blob import BlobServiceClient

import pandas as pd


# ============================================================
# Azure Storage configuration
# ============================================================

STORAGE_ACCOUNT_NAME = "ambroseetldata01"
ACCOUNT_URL = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"

SOURCE_CONTAINER = "source"
TARGET_CONTAINER = "target"


# ============================================================
# Local project files
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

LOCAL_SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "source"
    / "customers_source.csv"
)

LOCAL_TARGET_FILE = (
    PROJECT_ROOT
    / "data"
    / "target"
    / "customers_target.csv"
)


SOURCE_BLOB_NAME = "customers_source.csv"
TARGET_BLOB_NAME = "customers_target.csv"


# ============================================================
# Azure client
# ============================================================

def get_blob_service_client():
    """
    Create an authenticated Azure Blob Storage client.
    Authentication is provided through the Azure CLI login.
    """
    credential = AzureCliCredential()

    return BlobServiceClient(
        account_url=ACCOUNT_URL,
        credential=credential
    )


# ============================================================
# Upload source
# ============================================================

def upload_source_file():
    """
    Upload the local source CSV to the Azure source container.
    """
    client = get_blob_service_client()

    container_client = client.get_container_client(
        SOURCE_CONTAINER
    )

    with open(LOCAL_SOURCE_FILE, "rb") as data:
        container_client.upload_blob(
            name=SOURCE_BLOB_NAME,
            data=data,
            overwrite=True
        )

    print(
        f"Uploaded source: "
        f"{SOURCE_CONTAINER}/{SOURCE_BLOB_NAME}"
    )


# ============================================================
# Upload target
# ============================================================

def upload_target_file():
    """
    Upload the target target CSV to the Azure target container.
    """
    client = get_blob_service_client()

    container_client = client.get_container_client(
        TARGET_CONTAINER
    )

    with open(LOCAL_TARGET_FILE, "rb") as data:
        container_client.upload_blob(
            name=TARGET_BLOB_NAME,
            data=data,
            overwrite=True
        )

    print(
        f"Uploaded target: "
        f"{TARGET_CONTAINER}/{TARGET_BLOB_NAME}"
    )


# ============================================================
# Download source
# ============================================================

def download_source_as_dataframe():
    """
    Download the source CSV from Azure
    and return it as a pandas DataFrame.
    """
    client = get_blob_service_client()

    blob_client = client.get_blob_client(
        container=SOURCE_CONTAINER,
        blob=SOURCE_BLOB_NAME
    )

    blob_data = blob_client.download_blob().readall()

    return pd.read_csv(BytesIO(blob_data))


# ============================================================
# Download target
# ============================================================

def download_target_as_dataframe():
    """
    Download the target CSV from Azure
    and return it as a pandas DataFrame.
    """
    client = get_blob_service_client()

    blob_client = client.get_blob_client(
        container=TARGET_CONTAINER,
        blob=TARGET_BLOB_NAME
    )

    blob_data = blob_client.download_blob().readall()

    return pd.read_csv(BytesIO(blob_data))


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    upload_source_file()
    upload_target_file()

    source_df = download_source_as_dataframe()
    target_df = download_target_as_dataframe()

    print("\nAzure source:")
    print(source_df)

    print("\nAzure target:")
    print(target_df)

    print("\nSource record count:", len(source_df))
    print("Target record count:", len(target_df))