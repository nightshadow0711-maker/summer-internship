import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

# Import the safely loaded and synchronized keys directly from settings
from config.settings import NEWS_API_KEY, GNEWS_API_KEY, FACT_CHECK_API_KEY

from ml.predictor import predict_news
from verification.verification_engine import run_verification_pipeline
from database.database import save_analysis

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="TruthGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================

st.title("🛡️ TruthGuard AI")
st.subheader("AI-Powered Fake News Detection & Verification")
st.write(
    "Analyze news using Machine Learning, "
    "online news verification, fact-checking, "
    "and source credibility."
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("⚙️ Primary Verification Status")

    if NEWS_API_KEY:
        st.success("NewsAPI: Connected")
    else:
        st.warning("NewsAPI: Missing / Not Configured")

    if GNEWS_API_KEY:
        st.success("GNews API: Connected")
    else:
        st.warning("GNews API: Missing / Not Configured")

    if FACT_CHECK_API_KEY:
        st.success("Fact Check API: Connected")
    else:
        st.warning("Fact Check API: Missing / Not Configured")

    st.caption(
        "All configured APIs (including Google News RSS) "
        "operate collectively as primary verification sources."
    )

# ============================================================
# SOURCE
# ============================================================

source_name = st.text_input(
    "📰 News Source (Optional)",
    placeholder="Example: Reuters"
)

# ============================================================
# SAMPLE ARTICLES
# ============================================================

samples = {
    "Select sample": "",
    "NASA Satellite Launch": (
        "NASA successfully launched a communications "
        "satellite into orbit following a scheduled mission. "
        "The spacecraft reached its intended orbit and "
        "engineers began checking the satellite systems."
    ),
    "Miracle Disease Cure": (
        "Scientists have discovered a secret drink that "
        "makes humans completely immune to every known "
        "disease. Viral social media posts claim that "
        "drinking it removes the need for vaccines and "
        "medical treatment."
    ),
    "AI Technology Announcement": (
        "The technology company announced a new software "
        "platform designed to help developers build "
        "applications using artificial intelligence. "
        "The company said the platform will initially "
        "be available to selected users."
    )
}

selected = st.selectbox(
    "🧪 Sample News",
    list(samples.keys())
)

# ============================================================
# ARTICLE
# ============================================================

article = st.text_area(
    "📝 Enter News Article",
    value=samples[selected],
    height=300,
    placeholder="Paste the complete news article here..."
)

# ============================================================
# STATISTICS
# ============================================================

words = article.split()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Words", len(words))

with c2:
    st.metric("Characters", len(article))

with c3:
    st.metric(
        "Reading Time",
        f"{max(1, len(words) // 200)} min" if words else "0 min"
    )

# ============================================================
# BUTTON
# ============================================================

analyse = st.button(
    "🔍 Analyse News",
    type="primary",
    use_container_width=True
)

# ============================================================
# ANALYSIS
# ============================================================

if analyse:
    if not article.strip():
        st.error("Please enter a news article.")
        st.stop()

    # --------------------------------------------------------
    # ML
    # --------------------------------------------------------

    with st.spinner("Running Machine Learning model..."):
        ml_result = predict_news(article)

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    with st.spinner("Checking all primary online sources and fact-checks..."):
        result = run_verification_pipeline(
            article_text=article,
            ml_result=ml_result,
            news_api_key=NEWS_API_KEY,
            gnews_api_key=GNEWS_API_KEY,
            fact_check_api_key=FACT_CHECK_API_KEY,
            source_name=source_name
        )

    # Automatically save to database for History & Analytics
    try:
        save_analysis(result, article_text=article, source_name=source_name)
    except Exception:
        pass

    # ========================================================
    # FINAL
    # ========================================================

    final = result["final"]
    verdict = final["verdict"]
    score = final["score"]
    confidence = final["confidence"]

    st.divider()
    st.header("🎯 Final Assessment")

    if verdict == "LIKELY REAL":
        st.success("🟢 LIKELY REAL")
    elif verdict == "LIKELY FAKE":
        st.error("🔴 LIKELY FAKE")
    else:
        st.warning("🟡 UNCERTAIN")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Final Verdict", verdict)

    with m2:
        st.metric("Credibility Score", f"{score:.1f}/100")

    with m3:
        st.metric("Confidence", f"{confidence:.1f}%")

    # ========================================================
    # ML
    # ========================================================

    st.divider()
    st.header("🤖 Machine Learning")

    ml = result["ml"]
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Prediction", ml.get("prediction", "UNKNOWN"))

    with m2:
        st.metric("Real Probability", f"{ml.get('real_probability', 0):.2f}%")

    with m3:
        st.metric("Fake Probability", f"{ml.get('fake_probability', 0):.2f}%")

    with m4:
        st.metric("ML Confidence", f"{ml.get('confidence', 0):.2f}%")

    if ml.get("model_ready", False):
        st.success("ML model loaded successfully.")
    else:
        st.error(ml.get("message", "ML model failed."))

    # ========================================================
    # ONLINE
    # ========================================================

    st.divider()
    st.header("🌐 Online Verification")

    online = result["online"]

    if online.get("status") == "SUPPORTING":
        st.success(
            f"Found {online.get('articles_found', 0)} "
            "related online articles across primary sources."
        )
    else:
        st.info(
            "No matching online coverage found. "
            "This does not automatically mean the news is fake."
        )

    st.write(online.get("message", ""))

    for source in online.get("sources", []):
        title = source.get("title", "Article")
        url = source.get("url", "")
        publisher = source.get("source", "Unknown")

        if url:
            st.markdown(f"- [{title}]({url}) — {publisher}")

    # ========================================================
    # FACT CHECK
    # ========================================================

    st.divider()
    st.header("🔎 Fact Check")

    fact = result["fact_check"]
    fact_status = fact.get("status", "NOT_FOUND")

    if fact_status == "TRUE":
        st.success("Fact-check sources support the claim.")
    elif fact_status == "FALSE":
        st.error("Fact-check sources identify false or misleading information.")
    else:
        st.info("No matching fact-check was found.")

    st.write(fact.get("message", ""))

    for claim in fact.get("claims", []):
        with st.expander(claim.get("claim", "Fact Check Result")):
            st.write("Rating:", claim.get("rating", "Unknown"))
            st.write("Publisher:", claim.get("publisher", "Unknown"))

    # ========================================================
    # SOURCE
    # ========================================================

    st.divider()
    st.header("📰 Source Credibility")

    source = result["source"]
    s1, s2, s3 = st.columns(3)

    with s1:
        st.metric("Source", source_name if source_name else "Not Provided")

    with s2:
        st.metric("Score", f"{source.get('score', 50)}/100")

    with s3:
        st.metric("Level", source.get("level", "UNKNOWN"))

    st.write(source.get("message", ""))

    # ========================================================
    # DEBUG
    # ========================================================

    st.divider()
    with st.expander("🔧 Technical Debug Information"):
        st.write("ML Result")
        st.json(ml)

        st.write("Online Result")
        st.json(online)

        st.write("Fact Check Result")
        st.json(fact)

        st.write("Final Result")
        st.json(final)

    st.caption(
        "TruthGuard AI provides an AI-assisted assessment. "
        "Always verify important information with multiple "
        "reliable sources."
    )