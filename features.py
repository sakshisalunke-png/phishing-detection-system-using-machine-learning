import ipaddress
import re
from urllib.parse import urlparse

import pandas as pd

FEATURE_NAMES = [
    "url_length", "hostname_length", "path_length", "query_length",
    "count_dots", "count_hyphens", "count_underscores", "count_slashes",
    "count_at", "count_question", "count_equal", "count_percent",
    "count_digits", "count_letters", "count_subdomains",
    "has_ip_address", "has_https_scheme", "has_suspicious_word",
    "has_shortener_domain", "has_port", "has_punycode"
]

SUSPICIOUS_WORDS = {
    "login", "verify", "update", "secure", "account", "banking",
    "password", "signin", "confirm", "wallet", "payment", "support"
}
SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
    "buff.ly", "cutt.ly", "rebrand.ly"
}

def normalize_url(value: str) -> str:
    value = str(value).strip()
    if not value:
        return ""
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value):
        value = "http://" + value
    return value

def extract_url_features(value: str) -> dict:
    normalized = normalize_url(value)
    parsed = urlparse(normalized)
    host = (parsed.hostname or "").lower()
    path = parsed.path or ""
    query = parsed.query or ""
    raw = str(value).strip().lower()

    try:
        ipaddress.ip_address(host)
        has_ip = 1
    except ValueError:
        has_ip = 0

    try:
        port = 1 if parsed.port is not None else 0
    except ValueError:
        port = 1

    host_parts = [part for part in host.split(".") if part]
    words = set(re.findall(r"[a-z]+", raw))
    return {
        "url_length": len(raw),
        "hostname_length": len(host),
        "path_length": len(path),
        "query_length": len(query),
        "count_dots": raw.count("."),
        "count_hyphens": raw.count("-"),
        "count_underscores": raw.count("_"),
        "count_slashes": raw.count("/"),
        "count_at": raw.count("@"),
        "count_question": raw.count("?"),
        "count_equal": raw.count("="),
        "count_percent": raw.count("%"),
        "count_digits": sum(ch.isdigit() for ch in raw),
        "count_letters": sum(ch.isalpha() for ch in raw),
        "count_subdomains": max(0, len(host_parts) - 2),
        "has_ip_address": has_ip,
        "has_https_scheme": int(parsed.scheme.lower() == "https"),
        "has_suspicious_word": int(bool(words & SUSPICIOUS_WORDS)),
        "has_shortener_domain": int(host in SHORTENER_DOMAINS),
        "has_port": port,
        "has_punycode": int("xn--" in host),
    }

def make_feature_frame(urls) -> pd.DataFrame:
    return pd.DataFrame([extract_url_features(url) for url in urls], columns=FEATURE_NAMES)
