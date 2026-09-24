from predict import predict_email


email = """
Subject: Urgent Account Verification

URGENT ACTION REQUIRED!

Your account will be suspended within 24 hours.

Please login to your account immediately and confirm your password.

You must also provide your credit card information
to complete the verification process.

Verify your account here:

https://bit.ly/account-verification
"""


analysis = predict_email(email)


print()
print("===================================")
print("       MAILGUARD SECURITY REPORT")
print("===================================")

print()

print(
    f"Classification : {analysis['result']}"
)

print(
    f"ML Confidence  : "
    f"{analysis['confidence']:.2%}"
)

print()

print(
    f"URLs Found     : "
    f"{len(analysis['urls'])}"
)

print(
    f"Suspicious URLs: "
    f"{len(analysis['suspicious_urls'])}"
)

print(
    f"Phishing Signals: "
    f"{len(analysis['phishing_indicators'])}"
)

print()

print("-----------------------------------")
print("RISK ASSESSMENT")
print("-----------------------------------")

print(
    f"Risk Score     : "
    f"{analysis['risk']['score']}/100"
)

print(
    f"Risk Level     : "
    f"{analysis['risk']['level']}"
)

print()

print("-----------------------------------")
print("SECURITY FINDINGS")
print("-----------------------------------")

for reason in analysis["risk"]["reasons"]:

    print(f"- {reason}")

print()

print("-----------------------------------")
print("URL FINDINGS")
print("-----------------------------------")

for item in analysis["urls"]:

    print()
    print(f"URL: {item['url']}")

    if item["suspicious"]:

        print("Status: SUSPICIOUS")

        for finding in item["findings"]:
            print(f"  - {finding}")

    else:

        print("Status: CLEAN")


print()

print("-----------------------------------")
print("PHISHING INDICATORS")
print("-----------------------------------")

for indicator in analysis["phishing_indicators"]:

    print(
        f"\nCategory: {indicator['category']}"
    )

    for match in indicator["matches"]:

        print(
            f"  - {match}"
        )

print()