import re


PHISHING_PATTERNS = {
    "urgent_language": [
        "urgent",
        "immediately",
        "act now",
        "action required",
        "expires today",
        "within 24 hours",
        "account will be suspended",
        "account has been suspended"
    ],

    "credential_request": [
        "enter your password",
        "provide your password",
        "confirm your password",
        "verify your password",
        "login to your account",
        "log in to your account",
        "confirm your account",
        "verify your account"
    ],

    "financial_request": [
        "bank account",
        "credit card",
        "debit card",
        "payment required",
        "make a payment",
        "transfer money",
        "billing information"
    ],

    "sensitive_information": [
        "social security",
        "personal information",
        "identity verification",
        "security code",
        "verification code",
        "otp"
    ]
}


def detect_phishing_indicators(email_text):
    """
    Detect common phishing-related patterns
    in email content.
    """

    text = email_text.lower()

    findings = []

    for category, patterns in PHISHING_PATTERNS.items():

        matched = []

        for pattern in patterns:

            if re.search(
                r"\b" + re.escape(pattern) + r"\b",
                text
            ):
                matched.append(pattern)

        if matched:

            findings.append({
                "category": category,
                "matches": matched
            })

    return findings