import os
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate_gmail():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


def get_latest_emails(max_results=10):
    service = authenticate_gmail()

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=max_results,
            q="job OR application OR interview OR recruiter",
        )
        .execute()
    )

    messages = results.get("messages", [])

    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()

        payload = msg_data["payload"]
        headers = payload.get("headers", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), None)
        sender = next((h["value"] for h in headers if h["name"] == "From"), None)

        emails.append({"subject": subject, "from": sender})

    return emails
