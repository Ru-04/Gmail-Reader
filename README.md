PROJECT OVERVIEW

This project is a Python-based automation tool that reads unread emails from my Gmail inbox and stores important details into a Google Sheet automatically.

The goal of this project is to demonstrate:

    Practical use of Google APIs

    OAuth 2.0 authentication

    Real-world automation

    Clean, modular backend code

TECK STACK USED:

    Python 3

    Google Gmail API

    Google Sheets API

    OAuth 2.0

    google-api-python-client

    google-auth

    BeautifulSoup (for email body parsing)

FEATURES:

    Reads unread Gmail emails

    Extracts:

        Sender

        Subject

        Date

        Email body

    Stores data into Google Sheets

    Prevents duplicate entries using Gmail Message IDs

    Marks emails as read after processing

    Uses a single OAuth login for both Gmail & Sheets

OAuth AUTHENTICATION

    This project uses OAuth 2.0 to securely access Gmail and Google Sheets.

    How it works:

        When the script is run for the first time, a browser window opens.

        The user logs in with their Google account.

        Google asks for permission to:

            Read Gmail emails

            Modify email status (mark as read)

            Access Google Sheets

            After approval, Google generates a token file.

        This token is reused for future runs — no repeated login required.

    This ensures:

        No passwords are stored

        Secure access

        Google-approved authentication flow

OAuth consent screen used during login

GOOGLE SHEET STRUCTURE

| Column | Description      |
| ------ | ---------------- |
|        |                  |
| A      | Sender           |
| B      | Subject          |
| C      | Date             |
| D      | Content          |

DUPLICATE HANDLING LOGIC

To avoid duplicate entries:

    The Gmail Message ID is stored in the sheet.

    Before adding a new email, the script checks if the Message ID already exists.

    If found, the email is skipped.

This ensures:

    No repeated emails

    Safe re-running of the script

MARKING EMAIL AS READ

After an email is successfully added to Google Sheets:

    The UNREAD label is removed from the email

    This prevents the same email from being processed again

This makes the automation clean and efficient.

HOW TO RUN THE PROJECT

1. Clone the Repository
    git clone https://github.com/YOUR_USERNAME/gmail-to-sheets.git
    cd gmail-to-sheets

2. Create Virtual Environment
    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate

3. Install Dependencies
    pip install -r requirements.txt

4. Add Google Credentials

    Create OAuth credentials from Google Cloud Console

        Download credentials.json

    Place it in the project root directory

5. Run the Script
    python src/main.py