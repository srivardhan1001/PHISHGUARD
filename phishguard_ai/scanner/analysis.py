import json
import os
import re
from urllib.parse import urlparse
import requests
from django.conf import settings

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "bank", "free", "account", "secure",
    "confirm", "password", "unlock", "gift", "prize", "bonus", "apple",
    "paypal", "microsoft", "amazon", "wallet"
]

IP_PATTERN = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")


def rule_based_score(target_url: str):
    issues = []
    score = 0
    parsed = urlparse(target_url)
    host = parsed.hostname or ""
    path_q = (parsed.path or "") + (("?" + parsed.query) if parsed.query else "")

    if not parsed.scheme or parsed.scheme != "https":
        score += 10
        issues.append("HTTPS is missing")

    if IP_PATTERN.match(host):
        score += 15
        issues.append("URL uses raw IP address")

    if len(target_url) > 75:
        score += 8
        issues.append("URL length is unusually long")

    if host.count(".") >= 3:
        score += 8
        issues.append("URL has multiple subdomains")

    hits = [k for k in SUSPICIOUS_KEYWORDS if k in host.lower() or k in path_q.lower()]
    if hits:
        score += min(15, 3 * len(hits))
        issues.append(f"Suspicious keywords detected: {', '.join(sorted(set(hits)))}")

    score = max(0, min(50, score))
    return score, issues


def api_based_score(target_url: str):
    if not getattr(settings, "ENABLE_EXTERNAL_API", True):
        return 0, "API disabled", "unavailable"

    api_key = getattr(settings, "GOOGLE_SAFEBROWSING_API_KEY", None) or os.getenv("GOOGLE_SAFEBROWSING_API_KEY")
    if not api_key:
        return 0, "No API key configured", "unavailable"

    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {"clientId": "phishguard-ai", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION",
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": target_url}],
        },
    }
    try:
        resp = requests.post(endpoint, json=payload, timeout=8)
        status = "success" if resp.ok else "error"
        if not resp.ok:
            return 0, f"API error {resp.status_code}", "error"
        data = resp.json() if resp.text else {}
        matches = data.get("matches", [])
        if not matches:
            return 0, "No threats found", "success"
        types = sorted({m.get("threatType", "UNKNOWN") for m in matches})
        verdict = f"Threats: {', '.join(types)}"
        high_types = {"MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION"}
        high = any(t in high_types for t in types)
        score = 50 if high else 35
        return score, verdict, "success"
    except requests.RequestException as e:
        return 0, "API request failed", "error"


def classify(final_score: int) -> str:
    if final_score < 30:
        return "Safe"
    if final_score < 60:
        return "Suspicious"
    return "Highly Dangerous"


def analyze_url(target_url: str):
    rule_score, issues = rule_based_score(target_url)
    api_score, verdict, api_status = api_based_score(target_url)
    final_score = min(100, rule_score + api_score)
    label = classify(final_score)
    return {
        "rule_score": rule_score,
        "api_score": api_score,
        "final_score": final_score,
        "risk_label": label,
        "issues": issues,
        "api_verdict": verdict,
        "api_status": api_status,
    }

