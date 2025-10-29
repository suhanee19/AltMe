def classify_email(content):
    """
    Simple rule-based classification — can be upgraded with ML later.
    """
    content_lower = content.lower()
    if "offer" in content_lower or "discount" in content_lower:
        return "Promotional"
    elif "reminder" in content_lower or "deadline" in content_lower:
        return "Important"
    else:
        return "General"
