import requests
from config.settings import GOOGLE_FACT_CHECK_API_KEY

def _extract_claim_keywords(text):
    """
    Cleans the raw article text and extracts the top keywords 
    so the Google API can actually understand the search query.
    """
    words = [w.strip(".,!?;:()[]{}\"'").lower() for w in text.split()]
    stop_words = {"the","and","that","this","with","from","have","will","for",
                  "are","was","were","has","not","but","about","into","their",
                  "they","you","said","which","when","where"}
    
    # Filter out stop words and short words, keeping the top 10 keywords
    keywords = [w for w in words if len(w) > 3 and w not in stop_words]
    return " ".join(keywords[:10])

def search_fact_checks(text):
    if not GOOGLE_FACT_CHECK_API_KEY:
        return [], "NOT_CONFIGURED"
        
    try:
        # Use optimized keywords instead of a 500-character paragraph
        query = _extract_claim_keywords(text)
        if not query:
            return [], "NO_MATCH"
            
        r = requests.get("https://factchecktools.googleapis.com/v1alpha1/claims:search", params={
            "query": query, 
            "key": GOOGLE_FACT_CHECK_API_KEY, 
            "pageSize": 10
        }, timeout=12)
        
        if not r.ok:
            return [], "UNAVAILABLE"
            
        items = []
        false_count = 0
        true_count = 0
        
        for claim in r.json().get("claims", []):
            for review in claim.get("claimReview", []):
                rating = review.get("textualRating", "Unknown")
                rating_lower = rating.lower()
                
                # Tally up the ratings properly
                if any(x in rating_lower for x in ["false", "pants on fire", "incorrect", "fake", "misleading"]):
                    false_count += 1
                elif any(x in rating_lower for x in ["true", "correct", "accurate"]):
                    true_count += 1
                    
                items.append({
                    "publisher": (review.get("publisher") or {}).get("name", "Unknown"),
                    "claim": claim.get("text", ""),
                    "rating": rating,
                    "url": review.get("url", "")
                })
                
        if not items:
            return [], "NO_MATCH"
            
        # Determine status based on the majority of evidence
        if false_count > true_count:
            status = "FALSE"
        elif true_count > false_count:
            status = "SUPPORTED"
        else:
            status = "DISPUTED"
            
        return items, status
        
    except Exception:
        return [], "UNAVAILABLE"