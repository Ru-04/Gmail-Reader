import os.path
from time import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_gmail_service():
    

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

       
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    return service

import time

def fetch_unread_messages(service, max_results=10):
    one_day_ago = int(time.time()) - 86400  # last 24 hours

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=max_results,
        q=f"after:{one_day_ago}"
    ).execute()

    messages = results.get("messages", [])
    return messages

def get_message_detail(service, message_id):
   
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    return message

def mark_as_read(service, msg_id):
 
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
