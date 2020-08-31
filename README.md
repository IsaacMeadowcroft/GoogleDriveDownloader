# GoogleDriveDownloader
This is a Python script that uses the Google Drive V3 API to download all Google Drive files that are in folders. To run this script, first enable the Drive API at https://developers.google.com/drive/api/v3/quickstart/python. This will create a credentials.json file. Then replace the credentials.json file in your local repo with the credentials file you created and delete the token.pickle file since a new one will be generated after you run the driveDownloader.py script for the first time. Finally, replace the oldPath variable with the folder path to your local GoogleDriveDownloader folder and the newPath variable with the folder path where you want the python files downloaded to. 

For more information regarding the Google Drive V3 API check out: https://developers.google.com/drive/api/v3/about-sdk
