def calculate_risk(
    spam_confidence,
    suspicious_urls,
    phishing_indicators,
    header_analysis
):
    """
    Calculate an explainable email risk score.

    The score combines:
    - ML spam confidence
    - Suspicious URL findings
    - Phishing indicators
    - Email header findings
    """

    score = 0
    reasons = []

    # -----------------------------
    # ML SPAM CLASSIFICATION
    # -----------------------------

    if spam_confidence >= 0.80:
        score += 35
        reasons.append(
            "Machine-learning model strongly classified the email as spam"
        )

    elif spam_confidence >= 0.60:
        score += 20
        reasons.append(
            "Machine-learning model showed elevated spam probability"
        )

    elif spam_confidence >= 0.40:
        score += 10

    # -----------------------------
    # SUSPICIOUS URLS
    # -----------------------------

    url_count = len(suspicious_urls)

    if url_count >= 3:
        score += 30
        reasons.append(
            f"{url_count} suspicious URLs detected"
        )

    elif url_count >= 1:
        score += 20
        reasons.append(
            f"{url_count} suspicious URL detected"
        )

    # -----------------------------
    # PHISHING INDICATORS
    # -----------------------------

    phishing_count = len(phishing_indicators)

    if phishing_count >= 3:
        score += 30
        reasons.append(
            "Multiple phishing-related indicators detected"
        )

    elif phishing_count >= 2:
        score += 20
        reasons.append(
            "Several phishing-related indicators detected"
        )

    elif phishing_count >= 1:
        score += 10
        reasons.append(
            "Phishing-related language detected"
        )

    # -----------------------------
    # EMAIL HEADER ANALYSIS
    # -----------------------------

    header_findings = header_analysis.get(
        "findings",
        []
    )

    header_score = 0

    for finding in header_findings:

        finding_type = finding.get(
            "type",
            ""
        )

        if finding_type == "authentication_failure":

            header_score += 10

        elif finding_type in [
            "reply_to_mismatch",
            "return_path_mismatch"
        ]:

            header_score += 10

    if header_score > 0:

        header_score = min(
            header_score,
            30
        )

        score += header_score

        reasons.append(
            f"{len(header_findings)} suspicious email header condition(s) detected"
        )

    # -----------------------------
    # LIMIT SCORE
    # -----------------------------

    score = min(
        score,
        100
    )

    # -----------------------------
    # RISK LEVEL
    # -----------------------------

    if score >= 80:
        risk_level = "CRITICAL"

    elif score >= 60:
        risk_level = "HIGH"

    elif score >= 30:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "score": score,
        "level": risk_level,
        "reasons": reasons
    }