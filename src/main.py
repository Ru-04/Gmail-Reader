from gmail_service import get_gmail_service, fetch_unread_messages
from email_parser import process_emails

def main():
    # Step 1: Authenticate Gmail API
    service = get_gmail_service()

    # Step 2: Fetch unread emails
    messages = fetch_unread_messages(service)

    if not messages:
        print("No unread emails found.")
        return

    print(f"Found {len(messages)} unread email(s).")

    # Step 3: Process emails 
    process_emails(service, messages)

    print("Sheets working.")

if __name__ == "__main__":
    main()

