"""Google Cloud Storage tools for artifact management."""

import os
from typing import Optional

from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
from langchain_core.tools import tool

from src.config import get_settings


def _get_storage_client():
    """Get Google Cloud Storage client."""
    settings = get_settings()

    # Set credentials if provided
    if settings.google_application_credentials:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials

    return storage.Client(project=settings.gcs_project_id)


@tool
def upload_to_gcs(file_name: str, file_content: str, destination_path: str) -> str:
    """Upload a file to Google Cloud Storage.

    Args:
        file_name: Name of the file
        file_content: Content of the file as string
        destination_path: Destination path in the bucket (folder/filename)

    Returns:
        Upload status and public URL
    """
    try:
        settings = get_settings()
        client = _get_storage_client()
        bucket = client.bucket(settings.gcs_bucket_name)
        blob = bucket.blob(destination_path)

        # Upload the file
        blob.upload_from_string(file_content)

        # Make the blob publicly accessible (optional)
        # blob.make_public()

        public_url = f"gs://{settings.gcs_bucket_name}/{destination_path}"
        return f"Successfully uploaded {file_name} to GCS. URL: {public_url}"
    except GoogleCloudError as e:
        return f"Error uploading to GCS: {str(e)}"
    except Exception as e:
        return f"Error uploading to GCS: {str(e)}"


@tool
def download_from_gcs(source_path: str) -> str:
    """Download a file from Google Cloud Storage.

    Args:
        source_path: Source path in the bucket (folder/filename)

    Returns:
        File content or error message
    """
    try:
        settings = get_settings()
        client = _get_storage_client()
        bucket = client.bucket(settings.gcs_bucket_name)
        blob = bucket.blob(source_path)

        # Download the file content
        content = blob.download_as_text()

        return f"Successfully downloaded {source_path}. Content:\n{content[:500]}..."
    except GoogleCloudError as e:
        return f"Error downloading from GCS: {str(e)}"
    except Exception as e:
        return f"Error downloading from GCS: {str(e)}"


@tool
def list_gcs_files(prefix: Optional[str] = None, max_results: int = 10) -> str:
    """List files in Google Cloud Storage bucket.

    Args:
        prefix: Filter files by prefix (folder path)
        max_results: Maximum number of results to return

    Returns:
        List of files in the bucket
    """
    try:
        settings = get_settings()
        client = _get_storage_client()
        bucket = client.bucket(settings.gcs_bucket_name)

        blobs = bucket.list_blobs(prefix=prefix, max_results=max_results)

        file_list = []
        for blob in blobs:
            file_list.append(f"- {blob.name} (Size: {blob.size} bytes, Updated: {blob.updated})")

        if not file_list:
            return "No files found in the bucket."

        return f"Files in gs://{settings.gcs_bucket_name}:\n" + "\n".join(file_list)
    except GoogleCloudError as e:
        return f"Error listing GCS files: {str(e)}"
    except Exception as e:
        return f"Error listing GCS files: {str(e)}"


@tool
def delete_from_gcs(file_path: str) -> str:
    """Delete a file from Google Cloud Storage.

    Args:
        file_path: Path to the file in the bucket

    Returns:
        Deletion status
    """
    try:
        settings = get_settings()
        client = _get_storage_client()
        bucket = client.bucket(settings.gcs_bucket_name)
        blob = bucket.blob(file_path)

        blob.delete()

        return f"Successfully deleted {file_path} from GCS."
    except GoogleCloudError as e:
        return f"Error deleting from GCS: {str(e)}"
    except Exception as e:
        return f"Error deleting from GCS: {str(e)}"


# Export tools list
gcs_tools = [
    upload_to_gcs,
    download_from_gcs,
    list_gcs_files,
    delete_from_gcs,
]
