import re
from urllib.parse import urlparse


URL_PATTERN = r'https?://[^\s<>"\']+'


SHORTENED_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "cutt.ly",
    "shorturl.at"
}


def extract_urls(text):
    """Extract HTTP/HTTPS URLs from email text."""
    return re.findall(URL_PATTERN, text)


def analyze_url(url):
    """Analyze a single URL for suspicious characteristics."""

    findings = []

    try:
        parsed = urlparse(url)

        hostname = parsed.hostname

        if not hostname:
            return {
                "url": url,
                "suspicious": True,
                "findings": ["Invalid URL"]
            }

        hostname = hostname.lower()

        # IP address instead of domain
        ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

        if re.match(ip_pattern, hostname):
            findings.append(
                "IP address used instead of a domain name"
            )

        # URL shortener
        if hostname in SHORTENED_DOMAINS:
            findings.append(
                "URL shortening service detected"
            )

        # Excessive subdomains
        parts = hostname.split(".")

        if len(parts) >= 5:
            findings.append(
                "Unusually large number of subdomains"
            )

        # Suspicious characters
        if "@" in url:
            findings.append(
                "URL contains '@' character"
            )

        # Very long URL
        if len(url) > 150:
            findings.append(
                "Unusually long URL"
            )

        # Suspicious keywords in URL
        suspicious_words = [
            "login",
            "verify",
            "verification",
            "account",
            "secure",
            "password",
            "update",
            "confirm"
        ]

        matched_words = [
            word for word in suspicious_words
            if word in url.lower()
        ]

        if matched_words:
            findings.append(
                "Security-related keywords found: "
                + ", ".join(matched_words)
            )

        return {
            "url": url,
            "suspicious": len(findings) > 0,
            "findings": findings
        }

    except Exception:
        return {
            "url": url,
            "suspicious": True,
            "findings": ["Unable to analyze URL"]
        }


def analyze_email_urls(email_text):
    """Extract and analyze all URLs found in an email."""

    urls = extract_urls(email_text)

    results = []

    for url in urls:
        result = analyze_url(url)
        results.append(result)

    return results