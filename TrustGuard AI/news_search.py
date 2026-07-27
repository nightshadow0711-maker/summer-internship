import requests
from urllib.parse import quote_plus
from verification.source_analyzer import credibility_score
from config.settings import NEWS_API_KEY, GNEWS_API_KEY

def _keywords(text):
    words = [w.strip(".,!?;:()[]{}\"'").lower() for w in text.split()]
    stop = {"the","and","that","this","with","from","have","will","for","are","was","were","has","not","but","about","into","their","they","you","said"}
    return " ".join([w for w in words if len(w)>3 and w not in stop][:14])

def search_news(text, url=""):
    q = _keywords(text)
    results = []
    seen_urls = set()

    # 1. Check NewsAPI (if configured)
    if NEWS_API_KEY:
        try:
            r = requests.get("https://newsapi.org/v2/everything", params={
                "q": q, "apiKey": NEWS_API_KEY, "language": "en", "sortBy": "relevancy", "pageSize": 8
            }, timeout=12)
            if r.ok:
                for a in r.json().get("articles", []):
                    article_url = a.get("url", "").strip()
                    if article_url and article_url not in seen_urls:
                        seen_urls.add(article_url)
                        results.append({
                            "source_name": (a.get("source") or {}).get("name", "Unknown"),
                            "title": a.get("title", ""), 
                            "url": article_url,
                            "published_at": a.get("publishedAt", ""),
                            "evidence_type": "supporting", 
                            "relevance": 70,
                            "credibility": credibility_score(article_url)
                        })
        except Exception:
            pass

    # 2. Check GNews API (if configured) - Now runs IN ADDITION to NewsAPI
    if GNEWS_API_KEY:
        try:
            r = requests.get("https://gnews.io/api/v4/search", params={
                "q": q, "token": GNEWS_API_KEY, "lang": "en", "max": 8
            }, timeout=12)
            if r.ok:
                for a in r.json().get("articles", []):
                    article_url = a.get("url", "").strip()
                    if article_url and article_url not in seen_urls:
                        seen_urls.add(article_url)
                        results.append({
                            "source_name": (a.get("source") or {}).get("name", "Unknown"),
                            "title": a.get("title", ""), 
                            "url": article_url,
                            "published_at": a.get("publishedAt", ""),
                            "evidence_type": "supporting", 
                            "relevance": 70,
                            "credibility": credibility_score(article_url)
                        })
        except Exception:
            pass

    # 3. Fallback discovery link if no API returned results
    if not results and q:
        results.append({
            "source_name": "Google News Search",
            "title": f"Search related reporting for: {q}",
            "url": "https://news.google.com/search?q=" + quote_plus(q),
            "published_at": "",
            "evidence_type": "neutral", 
            "relevance": 30, 
            "credibility": 50
        })

    return results