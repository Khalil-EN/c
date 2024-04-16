from googleapiclient.discovery import build
from google.oauth2 import service_account
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

SCOPES=['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "service_account.json"
PARENT_FOLDER_ID = "1oXdZjS4cC1FXtH_3wRcHxZvhqz7B31Ly"

def authentificate():
    creds=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def authenticate():
    # Load service account credentials from JSON file
    creds = service_account.Credentials.from_service_account_file('service_account.json')
    # Create a service object for interacting with the Google Drive API
    service = build('drive', 'v3', credentials=creds)
    return service

def authenticate2():
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_photo(file_path):
    creds=authentificate()
    service=build('drive', 'v3', credentials=creds)
    file_metadata={
        'name' : "Hello",
        'parents' : [PARENT_FOLDER_ID]
    }
    file=service.files().create(body=file_metadata, media_body=file_path).execute()

def download_photo(file_id, dest_path):
    creds = authentificate()
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(dest_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


def get_file_id(file_name, parent_folder_id):
    creds = authentificate()
    service = build('drive', 'v3', credentials=creds)
    query = f"name='{file_name}' and '{parent_folder_id}' in parents"
    response = service.files().list(q=query, fields='files(id)').execute()
    files = response.get('files', [])
    if files:
        return files[0]['id']
    else:
        print(f"File '{file_name}' not found in folder with ID '{parent_folder_id}'")
        return None



def update_photo(file_id, new_photo_path):
    service = authenticate2()
    media = MediaFileUpload(new_photo_path)
    service.files().update(fileId=file_id, media_body=media).execute()
    print(f"Photo with ID {file_id} updated successfully.")



# Example usage
file_id = get_file_id('lamp.png', PARENT_FOLDER_ID)


download_photo(file_id, 'downloaded_file.png')

update_photo(file_id,"C:\TPs\Ateliers\ATELIER_DEV_WEB\Images\lightv1.png")

#upload_photo("C:\TPs\Ateliers\ATELIER_DEV_WEB\Images\lightv1.png")