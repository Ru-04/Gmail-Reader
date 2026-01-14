from googleapiclient.discovery import build
from gmail_service import get_gmail_service
from config import SHEET_ID, SHEET_NAME


def get_sheets_service():
    
    creds = get_gmail_service()._http.credentials
    service = build("sheets", "v4", credentials=creds)
    return service


def append_row_to_sheet(row):
    
    service = get_sheets_service()

    range_name = f"'{SHEET_NAME}'!A1:D"

    body = {
        "values": [row]
    }

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=range_name,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

def get_existing_message_ids():
    
    service = get_sheets_service()
    range_name = f"{SHEET_NAME}!A:A"
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=range_name
    ).execute()
    values = result.get("values", [])
    existing_ids = [row[0] for row in values if row]
    return set(existing_ids)