from googleapiclient.http import MediaIoBaseUpload
import io
# =========================================================
# Uploader Utility
# - Handles uploading files to Google Drive
# - Automatically sets the uploaded file to public access
# =========================================================

import mimetypes
from googleapiclient.http import MediaFileUpload

def upload_file_to_drive(service, file_path, folder_id, file_name):
    """
    Upload a file to a specific folder in Google Drive and make it publicly accessible.

    Args:
        service: Authorized Google Drive API service instance.
        file_path (str): Local path of the file to upload.
        folder_id (str): ID of the destination folder in Google Drive.
        file_name (str): Name for the uploaded file in Google Drive.

    Returns:
        str: The file ID of the uploaded file in Google Drive.

    Raises:
        ValueError: If the provided Google Drive service instance is None.
    """

    # Validate that the Google Drive service instance is provided
    if service is None:
        raise ValueError("Google Drive service is not initialized.")

    # Automatically detect the MIME type of the file based on its filename
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        # Fallback to a default MIME type if detection fails
        mime_type = 'application/octet-stream'

    # Set up the file metadata for Google Drive upload
    file_metadata = {
        'name': file_name,         # Desired name of the file in Drive
        'parents': [folder_id],    # Destination folder ID in Drive
        'mimeType': mime_type      # MIME type of the file
    }

    # Create a MediaFileUpload object to handle the file upload (supports resumable uploads)
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

    # Upload the file to Google Drive using the API and retrieve the file ID
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'  # Only retrieve the file ID in the response
    ).execute()
    file_id = file.get('id')

    # Define the permission to make the uploaded file publicly accessible (anyone with the link can view)
    permission = {
        'role': 'reader',  # Read-only access
        'type': 'anyone'   # Anyone on the internet
    }

    # Apply the public permission to the uploaded file
    service.permissions().create(
        fileId=file_id,
        body=permission
    ).execute()

    # Return the file ID of the uploaded file
    return file_id


# =========================================================
# Upload file-like object to a specific folder in Google Drive
# =========================================================
def upload_file_to_folder(drive_service, folder_id, file, filename):
    """
    Uploads a file-like object to a specified Google Drive folder and returns its metadata.

    Args:
        drive_service: Authorized Google Drive API service instance.
        folder_id (str): ID of the destination folder in Google Drive.
        file: File-like object (e.g., from Streamlit's file_uploader).
        filename (str): Desired name for the uploaded file in Drive.

    Returns:
        dict: Dictionary containing uploaded file metadata like id and webViewLink.

    Raises:
        ValueError: If the provided Drive service instance is None.
    """

    if drive_service is None:
        raise ValueError("Google Drive service is not initialized.")

    # Create file metadata
    file_metadata = {
        "name": filename,
        "parents": [folder_id]
    }

    # Create a MediaIoBaseUpload for the file
    media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.type)

    # Upload the file to Google Drive
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink"
    ).execute()

    # Set permissions to make the file public
    permission = {
        'role': 'reader',
        'type': 'anyone'
    }
    drive_service.permissions().create(
        fileId=uploaded_file['id'],
        body=permission
    ).execute()

    return uploaded_file
