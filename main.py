from gmail_reader import get_latest_emails
from classifier import classify_email
from db import save_email


def main():
    print("Fetching emails...\n")

    emails = get_latest_emails()

    for e in emails:
        print(e)


if __name__ == "__main__":
    main()
