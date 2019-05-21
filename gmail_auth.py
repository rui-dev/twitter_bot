from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def create_Gmail_credential():
    # define app name whatever you want
    APPLICATION_NAME = "myGmailApi"
    SCOPES = 'https://www.googleapis.com/auth/gmail.send'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        flow.user_agent = APPLICATION_NAME
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service

if __name__ == "__main__":
    # create credentials
    create_Gmail_credential()