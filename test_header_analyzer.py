from analysis.header_analyzer import analyze_headers


headers = """\
From: Security Team <security@example.com>
Reply-To: attacker@evil-example.com
Return-Path: bounce@evil-example.com
Message-ID: <123456@example.com>
Received: from mail.example.com
Authentication-Results: example.com; spf=fail; dkim=pass; dmarc=fail
"""


result = analyze_headers(headers)


print()
print("===================================")
print("       EMAIL HEADER ANALYSIS")
print("===================================")

print()

print("From:")
print(result["from"])

print()

print("Reply-To:")
print(result["reply_to"])

print()

print("Return-Path:")
print(result["return_path"])

print()

print("Message-ID:")
print(result["message_id"])

print()

print("Received Headers:")
print(result["received_count"])

print()

print("-----------------------------------")
print("AUTHENTICATION")
print("-----------------------------------")

for item in result["authentication"]:

    print(
        f"{item['type']}: "
        f"{item['status']} - "
        f"{item['message']}"
    )

print()

print("-----------------------------------")
print("HEADER FINDINGS")
print("-----------------------------------")

for finding in result["findings"]:

    print(
        f"- {finding['message']}"
    )

print()