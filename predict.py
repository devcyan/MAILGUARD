import joblib


MODEL_PATH = "models/spam_classifier.pkl"

model = joblib.load(MODEL_PATH)


def predict_email(email_text):
    prediction = model.predict([email_text])[0]

    probabilities = model.predict_proba([email_text])[0]

    classes = model.classes_

    probability_map = dict(zip(classes, probabilities))

    confidence = probability_map[prediction]

    if prediction == "spam":
        result = "SPAM"
    else:
        result = "LEGITIMATE"

    return result, confidence