from email import policy
from email.parser import Parser
from email.utils import parseaddr


def get_domain(address):
    """Extract the domain from an email address."""

    _, email_address = parseaddr(address)

    if "@" not in email_address:
        return None

    return email_address.split("@", 1)[1].lower()


def analyze_authentication_results(headers):
    """Analyze SPF, DKIM and DMARC results when present."""

    findings = []

    authentication_results = headers.get(
        "Authentication-Results",
        ""
    ).lower()

    if not authentication_results:
        return findings

    checks = {
        "SPF": "spf",
        "DKIM": "dkim",
        "DMARC": "dmarc"
    }

    for name, keyword in checks.items():

        if keyword not in authentication_results:
            continue

        if f"{keyword}=pass" in authentication_results:

            findings.append({
                "type": name,
                "status": "PASS",
                "message": f"{name} authentication passed"
            })

        elif f"{keyword}=fail" in authentication_results:

            findings.append({
                "type": name,
                "status": "FAIL",
                "message": f"{name} authentication failed"
            })

        elif f"{keyword}=softfail" in authentication_results:

            findings.append({
                "type": name,
                "status": "SOFTFAIL",
                "message": f"{name} authentication returned softfail"
            })

        elif f"{keyword}=none" in authentication_results:

            findings.append({
                "type": name,
                "status": "NONE",
                "message": f"{name} authentication result was none"
            })

    return findings


def analyze_headers(header_text):
    """
    Analyze raw email headers for observable characteristics.
    """

    if not header_text or not header_text.strip():

        return {
            "from": "",
            "reply_to": "",
            "return_path": "",
            "message_id": "",
            "received_count": 0,
            "authentication": [],
            "findings": []
        }

    try:

        message = Parser(
            policy=policy.default
        ).parsestr(header_text)

    except Exception:

        return {
            "from": "",
            "reply_to": "",
            "return_path": "",
            "message_id": "",
            "received_count": 0,
            "authentication": [],
            "findings": [
                "Unable to parse email headers"
            ]
        }

    from_header = message.get("From", "")
    reply_to = message.get("Reply-To", "")
    return_path = message.get("Return-Path", "")
    message_id = message.get("Message-ID", "")

    received_headers = message.get_all(
        "Received",
        []
    )

    authentication = analyze_authentication_results(
        message
    )

    findings = []

    # -----------------------------------
    # FROM / REPLY-TO MISMATCH
    # -----------------------------------

    from_domain = get_domain(
        from_header
    )

    reply_domain = get_domain(
        reply_to
    )

    if (
        from_domain
        and reply_domain
        and from_domain != reply_domain
    ):

        findings.append({
            "type": "reply_to_mismatch",
            "message": (
                "Reply-To domain differs from "
                "the From domain"
            )
        })

    # -----------------------------------
    # MISSING REPLY-TO
    # -----------------------------------

    if not reply_to:

        findings.append({
            "type": "reply_to_missing",
            "message": "No Reply-To header present"
        })

    # -----------------------------------
    # RETURN-PATH MISMATCH
    # -----------------------------------

    return_domain = get_domain(
        return_path
    )

    if (
        from_domain
        and return_domain
        and from_domain != return_domain
    ):

        findings.append({
            "type": "return_path_mismatch",
            "message": (
                "Return-Path domain differs from "
                "the From domain"
            )
        })

    # -----------------------------------
    # MESSAGE-ID
    # -----------------------------------

    if not message_id:

        findings.append({
            "type": "message_id_missing",
            "message": "No Message-ID header present"
        })

    # -----------------------------------
    # RECEIVED HEADERS
    # -----------------------------------

    if not received_headers:

        findings.append({
            "type": "received_missing",
            "message": "No Received headers present"
        })

    # -----------------------------------
    # AUTHENTICATION FAILURES
    # -----------------------------------

    for auth in authentication:

        if auth["status"] in [
            "FAIL",
            "SOFTFAIL"
        ]:

            findings.append({
                "type": "authentication_failure",
                "message": auth["message"]
            })

    return {
        "from": from_header,
        "reply_to": reply_to,
        "return_path": return_path,
        "message_id": message_id,
        "received_count": len(received_headers),
        "authentication": authentication,
        "findings": findings
    }