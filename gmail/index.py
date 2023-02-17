import os.path
import datetime
import re
import functools
import pickle

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    "https://mail.google.com/"
]

# この日以前のメールが削除対象
# BEFORE_DATE = 'YYYY-mm-dd'
BEFORE_DATE = '2022-01-01'

def main():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refrech_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build("gmail", "v1", credentials=creds)
    users = service.users()

    """
    -is:important で重要メールを外す
    -is:starred でスター付きメールを外す
    それ以外のフラグは https://support.google.com/mail/answer/7190?hl=ja を参照
    """
    meta_data = users.messages().list(userId='me', q='before:{} -is:important -is:starred'.format(BEFORE_DATE)).execute()

    while len(meta_data["message"]) > 0:
        remove_list = []
        for m in meta_data["message"]:
            print(m["id"])
            remove_list.append(m["id"])

        users.messages().batchDelete(userId="me", body={"ids": remove_list}).execute()
        meta_data = users.messages().list(userId="me", pageToken=meta_data["nextPageToken"]).execute()

if __name__ == "__main__":
    main()
