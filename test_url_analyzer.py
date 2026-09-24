from analysis.url_analyzer import analyze_email_urls


email = """
Hello,

Your account needs verification immediately.

Please login here:
https://example.com/login

You can also verify your account here:
https://bit.ly/account-verification

Thanks.
"""


results = analyze_email_urls(email)

print()
print("MailGuard URL Analysis")
print("----------------------")

print(f"URLs Found: {len(results)}")
print()

for result in results:

    print(f"URL: {result['url']}")

    if result["suspicious"]:
        print("Status: SUSPICIOUS")

        for finding in result["findings"]:
            print(f"  - {finding}")

    else:
        print("Status: CLEAN")

    print()