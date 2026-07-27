# ============================================================
# TRUTHGUARD AI
# verification/verification_engine.py
# ============================================================

import re
import requests
from urllib.parse import quote
import xml.etree.ElementTree as ET

REQUEST_TIMEOUT = 15
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)

# ============================================================
# STOP WORDS
# ============================================================

STOP_WORDS = {
    "about", "after", "again", "against", "also", "because", "before", "being", 
    "between", "could", "every", "from", "have", "having", "into", "more", 
    "most", "other", "over", "same", "should", "some", "such", "than", "that", 
    "their", "there", "these", "they", "this", "those", "through", "under", 
    "very", "were", "what", "when", "where", "which", "while", "with", "would", 
    "your", "the", "and", "for", "are", "was", "has", "had", "not", "but", 
    "you", "can", "will", "its", "his", "her", "our", "out", "who", "how", 
    "why", "all", "any", "one", "two", "new"
}

# ============================================================
# CLEAN & KEYWORDS
# ============================================================

def clean_text(text):
    if not text:
        return ""
    text = str(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_keywords(text, max_words=10):
    text = clean_text(text).lower()
    words = re.findall(r"[a-zA-Z0-9]+", text)
    keywords = []

    for word in words:
        if len(word) < 4 or word in STOP_WORDS:
            continue
        if word not in keywords:
            keywords.append(word)

    return keywords[:max_words]

def create_search_query(article_text):
    keywords = extract_keywords(article_text, 10)
    return " ".join(keywords)

# ============================================================
# GOOGLE NEWS RSS
# ============================================================

def search_google_news(article_text):
    query = create_search_query(article_text)
    if not query:
        return []

    try:
        rss_url = (
            "https://news.google.com/rss/search?q="
            + quote(query)
            + "&hl=en-US&gl=US&ceid=US:en"
        )
        response = requests.get(rss_url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT)

        if response.status_code != 200:
            return []

        root = ET.fromstring(response.content)
        items = root.findall(".//item")
        sources = []

        for item in items[:10]:
            title_element = item.find("title")
            link_element = item.find("link")
            source_element = item.find("source")
            date_element = item.find("pubDate")

            sources.append({
                "title": title_element.text if title_element is not None else "",
                "url": link_element.text if link_element is not None else "",
                "source": source_element.text if source_element is not None else "Google News",
                "published": date_element.text if date_element is not None else ""
            })
        return sources

    except Exception:
        return []

# ============================================================
# NEWS API
# ============================================================

def search_news_api(article_text, api_key):
    if not api_key:
        return []

    query = create_search_query(article_text)

    try:
        url = (
            "https://newsapi.org/v2/everything?q="
            + quote(query)
            + "&language=en&sortBy=relevancy&pageSize=10&apiKey="
            + api_key
        )
        response = requests.get(url, timeout=REQUEST_TIMEOUT)

        if response.status_code != 200:
            return []

        data = response.json()
        articles = data.get("articles", [])
        sources = []

        for article in articles[:10]:
            sources.append({
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("name", "NewsAPI"),
                "published": article.get("publishedAt", "")
            })

        return sources

    except Exception:
        return []

# ============================================================
# GNEWS API
# ============================================================

def search_gnews_api(article_text, api_key):
    if not api_key:
        return []

    query = create_search_query(article_text)

    try:
        url = (
            "https://gnews.io/api/v4/search?q="
            + quote(query)
            + "&lang=en&max=10&token="
            + api_key
        )
        response = requests.get(url, timeout=REQUEST_TIMEOUT)

        if response.status_code != 200:
            return []

        data = response.json()
        articles = data.get("articles", [])
        sources = []

        for article in articles[:10]:
            sources.append({
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("name", "GNews"),
                "published": article.get("publishedAt", "")
            })

        return sources

    except Exception:
        return []

# ============================================================
# MULTI-API ONLINE VERIFICATION
# ============================================================

def verify_online_news(article_text, news_api_key=None, gnews_api_key=None):
    all_sources = []
    seen_urls = set()

    # 1. Query Google News RSS
    google_sources = search_google_news(article_text)
    for src in google_sources:
        url = src.get("url", "").strip()
        if url and url not in seen_urls:
            seen_urls.add(url)
            all_sources.append(src)

    # 2. Query NewsAPI (if key provided)
    if news_api_key:
        news_api_sources = search_news_api(article_text, news_api_key)
        for src in news_api_sources:
            url = src.get("url", "").strip()
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_sources.append(src)

    # 3. Query GNews API (if key provided)
    if gnews_api_key:
        gnews_sources = search_gnews_api(article_text, gnews_api_key)
        for src in gnews_sources:
            url = src.get("url", "").strip()
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_sources.append(src)

    if all_sources:
        return {
            "status": "SUPPORTING",
            "confidence": min(95, 50 + len(all_sources) * 5),
            "articles_found": len(all_sources),
            "sources": all_sources,
            "message": f"Found {len(all_sources)} related news articles across available services."
        }

    return {
        "status": "NOT_FOUND",
        "confidence": 0,
        "articles_found": 0,
        "sources": [],
        "message": "No matching online coverage was found across any configured news sources."
    }

# ============================================================
# FACT CHECK
# ============================================================

def verify_fact_check(article_text, fact_check_api_key=None):
    if not fact_check_api_key:
        return {
            "status": "NOT_FOUND",
            "confidence": 0,
            "claims_found": 0,
            "claims": [],
            "message": "Fact Check API is not configured."
        }

    query = create_search_query(article_text)

    try:
        url = (
            "https://factchecktools.googleapis.com/v1alpha1/claims:search?query="
            + quote(query)
            + "&pageSize=10&key="
            + fact_check_api_key
        )
        response = requests.get(url, timeout=REQUEST_TIMEOUT)

        if response.status_code != 200:
            return {
                "status": "NOT_FOUND",
                "confidence": 0,
                "claims_found": 0,
                "claims": [],
                "message": "Fact Check API request failed."
            }

        data = response.json()
        claims = data.get("claims", [])
        formatted = []
        has_false = False
        has_true = False

        for claim in claims:
            reviews = claim.get("claimReview", [])
            rating = ""
            publisher = ""

            if reviews:
                rating = reviews[0].get("textualRating", "")
                publisher = reviews[0].get("publisher", {}).get("name", "Unknown")

            rating_lower = rating.lower()

            if any(word in rating_lower for word in ["false", "fake", "incorrect", "misleading"]):
                has_false = True

            if any(word in rating_lower for word in ["true", "correct", "accurate"]):
                has_true = True

            formatted.append({
                "claim": claim.get("text", ""),
                "rating": rating,
                "publisher": publisher
            })

        if has_false:
            status = "FALSE"
        elif has_true:
            status = "TRUE"
        else:
            status = "REVIEWED"

        return {
            "status": status,
            "confidence": 90,
            "claims_found": len(formatted),
            "claims": formatted,
            "message": "Related fact-check information found."
        }

    except Exception as e:
        return {
            "status": "NOT_FOUND",
            "confidence": 0,
            "claims_found": 0,
            "claims": [],
            "message": f"Fact Check error: {str(e)}"
        }

# ============================================================
# SOURCE CREDIBILITY
# ============================================================

def calculate_source_credibility(source_name=None):
    if not source_name:
        return {
            "score": 50,
            "level": "UNKNOWN",
            "message": "No source was provided."
        }

    source = source_name.lower()
    high = ["reuters", "associated press", "ap news", "bbc", "npr", "pbs", "nasa", "who", "world health organization", "united nations"]
    good = ["cnn", "nbc", "abc news", "cbs news", "ndtv", "the hindu", "times of india", "indian express"]

    for item in high:
        if item in source:
            return {"score": 90, "level": "HIGH", "message": "Established and generally reliable source."}

    for item in good:
        if item in source:
            return {"score": 75, "level": "GOOD", "message": "Established news source."}

    return {"score": 50, "level": "UNKNOWN", "message": "Source credibility could not be established."}

# ============================================================
# FINAL ASSESSMENT (UPDATED LOGIC)
# ============================================================

def calculate_final_assessment(ml_prediction="UNCERTAIN", ml_confidence=0, real_probability=50, fake_probability=50, online_status="NOT_FOUND", fact_check_status="NOT_FOUND", source_score=50, online_articles_found=0):
    prediction = str(ml_prediction).upper().strip()
    
    try: real_probability = float(real_probability)
    except: real_probability = 50
        
    try: source_score = float(source_score)
    except: source_score = 50

    # Start with the ML model's baseline probability
    score = real_probability

    # 1. HEAVY ADJUSTMENTS FOR FACT CHECKS (Overrides ML mistakes)
    if fact_check_status == "TRUE": 
        score = max(score + 25, 85) # Floor it at 85 if proven true
    elif fact_check_status == "FALSE": 
        score = min(score - 40, 20) # Cap it at 20 if proven false
        
    # 2. ADJUSTMENTS FOR ONLINE NEWS EVIDENCE
    if online_status == "SUPPORTING" and online_articles_found > 0:
        # If multiple news sites are reporting this, boost the score heavily
        score += min(35, online_articles_found * 6)
    elif online_status == "NOT_FOUND":
        # If zero news outlets are reporting a major claim, penalize it
        score -= 20

    # 3. SOURCE CREDIBILITY BONUS
    score += (source_score - 50) * 0.20

    # 4. NORMALIZE FINAL SCORE
    score = max(0, min(100, score))

    # 5. DETERMINE VERDICT
    if fact_check_status == "FALSE": verdict = "LIKELY FAKE"
    elif fact_check_status == "TRUE": verdict = "LIKELY REAL"
    elif score >= 60: verdict = "LIKELY REAL"
    elif score <= 40: verdict = "LIKELY FAKE"
    else: verdict = "UNCERTAIN"

    if verdict == "LIKELY REAL": confidence = score
    elif verdict == "LIKELY FAKE": confidence = 100 - score
    else: confidence = 50

    return {
        "verdict": verdict,
        "score": round(score, 2),
        "confidence": round(confidence, 2)
    }

# ============================================================
# COMPLETE PIPELINE
# ============================================================

def run_verification_pipeline(article_text, ml_result, news_api_key=None, gnews_api_key=None, fact_check_api_key=None, source_name=None):
    online_result = verify_online_news(article_text, news_api_key, gnews_api_key)
    fact_result = verify_fact_check(article_text, fact_check_api_key)
    source_result = calculate_source_credibility(source_name)
    
    final_result = calculate_final_assessment(
        ml_prediction=ml_result.get("prediction", "UNCERTAIN"),
        ml_confidence=ml_result.get("confidence", 0),
        real_probability=ml_result.get("real_probability", 50),
        fake_probability=ml_result.get("fake_probability", 50),
        online_status=online_result.get("status", "NOT_FOUND"),
        fact_check_status=fact_result.get("status", "NOT_FOUND"),
        source_score=source_result.get("score", 50),
        online_articles_found=online_result.get("articles_found", 0) # Now dynamically passes the article count
    )

    return {
        "ml": ml_result,
        "online": online_result,
        "fact_check": fact_result,
        "source": source_result,
        "final": final_result
    }