from gmail_reader import get_latest_emails
from classifier import classify_email
from db import init_db, upsert_application, show_all

init_db()

print("Fetching emails...\n")

emails = get_latest_emails()

for email in emails:
    result = classify_email(email["subject"], email["from"])

    print("\nEMAIL:")
    print(email)

    print("\nCLASSIFIED:")
    print(result)

    upsert_application(
        result["company"],
        result["role"],
        result["status"],
        result["confidence"]
    )

print("\n--- DATABASE STATE ---")
show_all()
