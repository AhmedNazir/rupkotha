from __future__ import print_function
import httplib2
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

from Split import split
from Finish import finish,clear

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'private/client_secrets.json'
APPLICATION_NAME = 'Project Rupkotha'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_path = os.path.join("private/", 'credentials.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def ocr(imgfile = 'sample.png',imgfolder ='',project =''):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    imgfilepath =imgfolder + imgfile  # Image with texts (png, jpg, bmp, gif, pdf)
    txtfile =project + '//'+ project +'.txt'  # Text file outputted by OCR

    mime = 'application/vnd.google-apps.document'
    res = service.files().create(
        body={
            'name': imgfile,
            'mimeType': mime
        },
        media_body=MediaFileUpload(imgfilepath, mimetype=mime, resumable=True)
    ).execute()

    downloader = MediaIoBaseDownload(
        io.FileIO(txtfile, 'a'),
        service.files().export_media(fileId=res['id'], mimeType="text/plain")
    )

    done = False
    while done is False:
        status, done = downloader.next_chunk()

    service.files().delete(fileId=res['id']).execute()
    print(imgfile)


# if __name__ == '__main__':

#     # clear()

#     file= 'project1'
#     project_number = 1

#     pdfname= 'project' + str(project_number).zfill(3)
#     total_page = split(path =file,name=pdfname)

#     start = 10
#     stop = total_page

#     folder = pdfname+'\\'
#     for i in range(start,stop):
#         name =pdfname+str(i).zfill(3)+'.pdf'
#         ocr(name,folder)

#     finish()