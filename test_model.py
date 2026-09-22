from predict import predict_email


email = """
Congratulations! You have won a $1,000,000 prize.
Click the link below immediately to claim your reward.
You must provide your account information to receive the money.
"""


result, confidence = predict_email(email)

print()
print("MailGuard Result")
print("----------------")
print(f"Classification : {result}")
print(f"Confidence    : {confidence:.2%}")