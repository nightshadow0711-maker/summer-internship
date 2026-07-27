from urllib.parse import urlparse

KNOWN_SOURCES = {
    "reuters.com": 95, "apnews.com": 94, "bbc.com": 92, "bbc.co.uk": 92,
    "theguardian.com": 88, "nytimes.com": 90, "washingtonpost.com": 88,
    "npr.org": 88, "aljazeera.com": 82, "ndtv.com": 78, "thehindu.com": 86,
    "timesofindia.indiatimes.com": 76, "snopes.com": 90, "politifact.com": 90,
    "factcheck.org": 91
}

def domain_from_url(url):
    try:
        return urlparse(url).netloc.lower().replace("www.","")
    except Exception:
        return ""

def credibility_score(url):
    domain = domain_from_url(url)
    if domain in KNOWN_SOURCES:
        return KNOWN_SOURCES[domain]
    if domain.endswith(".gov") or ".gov." in domain:
        return 88
    if domain.endswith(".edu") or ".edu." in domain:
        return 85
    if domain.endswith(".org") or ".org." in domain:
        return 70
    return 55