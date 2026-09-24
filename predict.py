import joblib

from analysis.url_analyzer import analyze_email_urls
from analysis.phishing_detector import detect_phishing_indicators
from analysis.risk_engine import calculate_risk
from analysis.header_analyzer import analyze_headers


MODEL_PATH = "models/spam_classifier.pkl"

model = joblib.load(MODEL_PATH)


def predict_email(email_text, header_text=""):

    # -----------------------------
    # ML CLASSIFICATION
    # -----------------------------

    prediction = model.predict(
        [email_text]
    )[0]

    probabilities = model.predict_proba(
        [email_text]
    )[0]

    classes = model.classes_

    probability_map = dict(
        zip(classes, probabilities)
    )

    confidence = probability_map[
        prediction
    ]

    if prediction == "spam":
        result = "SPAM"
    else:
        result = "LEGITIMATE"

    # -----------------------------
    # URL ANALYSIS
    # -----------------------------

    url_results = analyze_email_urls(
        email_text
    )

    suspicious_urls = [
        url
        for url in url_results
        if url["suspicious"]
    ]

    # -----------------------------
    # PHISHING ANALYSIS
    # -----------------------------

    phishing_indicators = detect_phishing_indicators(
        email_text
    )

    # -----------------------------
    # HEADER ANALYSIS
    # -----------------------------

    header_analysis = analyze_headers(
        header_text
    )

    # -----------------------------
    # SPAM CONFIDENCE
    # -----------------------------

    if result == "SPAM":

        spam_confidence = confidence

    else:

        spam_confidence = 0

    # -----------------------------
    # RISK ANALYSIS
    # -----------------------------

    risk = calculate_risk(
        spam_confidence,
        suspicious_urls,
        phishing_indicators,
        header_analysis
    )

    return {
        "result": result,
        "confidence": confidence,
        "urls": url_results,
        "suspicious_urls": suspicious_urls,
        "phishing_indicators": phishing_indicators,
        "headers": header_analysis,
        "risk": risk
    }