import base64
from bs4 import BeautifulSoup
from gmail_service import mark_as_read, get_message_detail
from sheets_service import append_row_to_sheet, get_existing_message_ids

def _get_header(headers, name):
    """Return the value of a header from the headers list."""
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""

def _get_body(payload):
   
    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            body = part.get("body", {})

            if mime_type == "text/plain" and "data" in body:
                return body["data"]

            if mime_type == "text/html" and "data" in body:
                return body["data"]

            if "parts" in part:
                result = _get_body(part)
                if result:
                    return result
    else:
        body = payload.get("body", {})
        if "data" in body:
            return body["data"]

    return None

def parse_email(message):
   
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    sender = _get_header(headers, "From")
    subject = _get_header(headers, "Subject")
    date = _get_header(headers, "Date")

    body_data = _get_body(payload)
    body_text = ""

    if body_data:
        try:
            decoded_bytes = base64.urlsafe_b64decode(body_data)
            decoded_text = decoded_bytes.decode("utf-8", errors="ignore")
        except:
            decoded_text = body_data

        # Convert HTML to plain text
        soup = BeautifulSoup(decoded_text, "html.parser")
        body_text = soup.get_text(separator="\n").strip()

    return {
        "from": sender,
        "subject": subject,
        "date": date,
        "body": body_text
    }

def process_emails(service, messages):
  
    existing_ids = get_existing_message_ids()

    for msg in messages:
        msg_id = msg["id"]

        if msg_id in existing_ids:
            continue  # Skip duplicates

        # Fetch full message
        message = get_message_detail(service, msg_id)
        parsed = parse_email(message)

        # Append to sheet
        row = [msg_id, parsed["from"], parsed["subject"], parsed["date"], parsed["body"]]
        append_row_to_sheet(row)

        # Mark as read
        mark_as_read(service, msg_id)

        print(f"Added email: {parsed['subject']}")
