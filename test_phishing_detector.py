from analysis.phishing_detector import detect_phishing_indicators


email = """
URGENT ACTION REQUIRED!

Your account will be suspended within 24 hours.

Please login to your account immediately and confirm your password.

You must also provide your credit card information
to complete the verification process.
"""


findings = detect_phishing_indicators(email)


print()
print("MailGuard Phishing Analysis")
print("---------------------------")

print(
    f"Indicators Found: {len(findings)}"
)

print()


for finding in findings:

    print(
        f"Category: {finding['category']}"
    )

    print(
        "Matches:"
    )

    for match in finding["matches"]:
        print(f"  - {match}")

    print()