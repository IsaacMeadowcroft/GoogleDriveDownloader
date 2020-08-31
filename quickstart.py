from __future__ import print_function
import pickle
import os
import io
import shutil
import time
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API to get Drive folders
    results = service.files().list(
        q="mimeType='application/vnd.google-apps.folder'", pageSize=1000, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # Initialize empty dictionary to store folder name to folder ID correspondence
    folderDict = dict()

    if not items:
        print('No folders found.')
    else:
        print('Folders:')
        for item in items:
            folderDict.update({item['id']:item['name']})
            print("Creating folder ", str(item['name']), " from Google Drive")
            dir = os.path.join("/","Users","Keith",'Desktop','FALL 2020',item['name'])
            if not os.path.exists(dir):
                os.mkdir(dir)


    # Call the Drive v3 API to get drive files
    results = service.files().list(
        fields="*").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        currentTime = time.strftime('%Y-%m-%dT%H:%M:%SZ')
        for item in items:
            try:
                if (item['parents'][0] in folderDict and (str(currentTime)[0:10]==str(item['modifiedTime'][0:10]))):
                    print(item['modifiedTime'])
                    print("Downloading file ", str(item['name']), " from Google Drive")
                    file_id = item['id']
                    request = service.files().get_media(fileId=file_id)
                    fh = io.FileIO(item['name'], 'wb')
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        try:
                            status, done = downloader.next_chunk()
                            print('Download %d%%.' % int(status.progress() * 100))
                            oldPath='/Users/Keith/Desktop/GoogleDriveDownloader/'+item['name']
                            newPath='/Users/Keith/Desktop/Fall 2020/'+folderDict.get(item['parents'][0])+'/'
                            os.remove(newPath+item['name'])
                            shutil.move(oldPath,newPath)
                        except:
                            continue
            except:
                continue
                

if __name__ == '__main__':
    main()
