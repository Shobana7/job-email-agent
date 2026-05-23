CATEGORIES = ["work", "personal", "spam", "newsletter", "other"]


def classify_email(email: dict) -> str:
    subject = email.get("subject", "").lower()
    sender = email.get("from", "").lower()
    snippet = email.get("snippet", "").lower()

    if any(word in subject for word in ["invoice", "meeting", "project", "deadline"]):
        return "work"
    if any(word in sender for word in ["noreply", "no-reply", "newsletter", "digest"]):
        return "newsletter"
    if any(word in snippet for word in ["unsubscribe", "click here", "limited offer"]):
        return "spam"
    if any(word in subject for word in ["hi", "hey", "dinner", "catch up"]):
        return "personal"
    return "other"
