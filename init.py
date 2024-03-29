from __future__ import print_function
import httplib2
import os
import io

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def get_credentials(ID=1):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    # If modifying these scopes, delete your previously saved credentials
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = f'private/client_secrets-{ID}.json'
    APPLICATION_NAME = 'Project Rupkotha'

    credential_path = os.path.join("private/", f'credentials-{ID}.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def getService(ID=1):
    credentials = get_credentials(ID)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    return service


def clear(bookName=''):
    path = 'book' + '//' + bookName + '//'

    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path+'output'):
        os.makedirs(path+'output')
    if not os.path.exists(path+'input'):
        os.makedirs(path+'input')
    if not os.path.exists(path+'images'):
        os.makedirs(path+'images')

    try:
        open(path+bookName+'_raw.txt', 'w', encoding='utf-8').close()
    except:
        pass

    try:
        open(path+bookName+'.txt', 'w', encoding='utf-8').close()
    except:
        pass

    try:
        open(path+bookName+'.html', 'w', encoding='utf-8').close()
    except:
        pass

