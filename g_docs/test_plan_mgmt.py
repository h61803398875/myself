# -*- encoding:utf8 -*-

from __future__ import print_function

import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_http():
    return httplib2.Http(
        proxy_info=httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP, 'dev-proxy.oa.com', 8080,
                                      proxy_user="chazzhuang",
                                      proxy_pass="Tencent201611"))


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.test_plan_mgmt.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        if flags:
            http = get_http()
            credentials = tools.run_flow(flow, store, flags, http)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """

    credentials = get_credentials()

    http = credentials.authorize(http=get_http())

    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1C9lUHC3kEZmb7OmePYdarEMJEcIF7_ipHBuLwvqUoNw'
    rangeName = '每日工作!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))


# from oauth2client.client import OAuth2WebServerFlow
# from oauth2client.client import flow_from_clientsecrets
#
# home_dir = os.path.expanduser('~')
# credential_dir = os.path.join(home_dir, '.credentials')
# if not os.path.exists(credential_dir):
#     os.makedirs(credential_dir)
# credential_path = os.path.join(credential_dir,
#                                'sheets.googleapis.com-python-quickstart.json')
# flow = flow_from_clientsecrets(credential_path,
#                                scope='https://spreadsheets.google.com/feeds')

if __name__ == '__main__':
    main()
