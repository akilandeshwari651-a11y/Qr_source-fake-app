from urllib.parse import urlparse
import re

BAD_ENDINGS = ["xyz", "tk", "top", "click"]
RISKY_WORDS = ["login", "verify", "secure", "update", "pay", "bank", "otp", "free", "gift"]
BRANDS = {"paytm": "paytm.com", "google": "google.com", "amazon": "amazon.in", "sbi": "sbi.co.in"}


def analyze(link, reported=False):
    link = link.strip()
    if "://" not in link:
        link = "http://" + link
    host = urlparse(link).hostname or ""
    score = 0
    reasons = []

    if not link.startswith("https"):
        score += 20
        reasons.append("Not using HTTPS (not encrypted)")
    if re.fullmatch(r"[\d.]+", host):
        score += 35
        reasons.append("Uses an IP address instead of a domain name")
    if host.split(".")[-1] in BAD_ENDINGS:
        score += 15
        reasons.append("Suspicious domain ending")
    if host.count("-") >= 2:
        score += 10
        reasons.append("Many hyphens in the domain name")
    found = [w for w in RISKY_WORDS if w in link.lower()]
    if found:
        score += min(20, 7 * len(found))
        reasons.append("Risky words in link: " + ", ".join(found))
    for brand, official in BRANDS.items():
        if brand in host and host != official and not host.endswith("." + official):
            score += 30
            reasons.append("Pretends to be " + brand + " but is not the official site")
    if reported:
        score += 30
        reasons.append("Reported by other users")

    score = min(score, 100)
    if score < 25:
        verdict = "safe"
    elif score < 60:
        verdict = "suspicious"
    else:
        verdict = "dangerous"
    if not reasons:
        reasons = ["No warning signs found"]
    return {"url": link, "score": score, "verdict": verdict, "reasons": reasons}
