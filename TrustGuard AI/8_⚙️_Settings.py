import streamlit as st

from config.settings import (
    APP_NAME,
    APP_ICON,
    APP_VERSION,
    APP_DESCRIPTION,
    BASE_DIR,
    ENV_FILE,
    NEWS_API_KEY,
    GNEWS_API_KEY,
    GOOGLE_FACT_CHECK_API_KEY,
    SMTP_USERNAME,
    SMTP_SERVER,
    SMTP_PORT,
    GOOGLE_NEWS_ENABLED,
    NEWS_API_ENABLED,
    GNEWS_API_ENABLED,
    FACT_CHECK_ENABLED,
    SMTP_ENABLED,
    inject_global_css,
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title=f"{APP_NAME} - Settings",
    page_icon=APP_ICON,
    layout="wide",
)

inject_global_css()

# ============================================================
# HEADER
# ============================================================

st.title(f"{APP_ICON} {APP_NAME} Settings")
st.markdown(
    """
    Configure and monitor the services used by TruthGuard AI.

    **All enabled APIs (Google News RSS, NewsAPI, GNews, Google Fact Check) 
    operate collectively as the Primary online verification sources.**
    """
)
st.divider()

# ============================================================
# APPLICATION INFORMATION
# ============================================================

st.subheader("📱 Application Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Application", APP_NAME)

with col2:
    st.metric("Version", APP_VERSION)

with col3:
    st.metric("Verification Mode", "Multi-Source Primary")

st.info(
    "TruthGuard AI uses a multi-source primary verification architecture. "
    "All enabled APIs are queried simultaneously to gather the most comprehensive evidence."
)

# ============================================================
# ONLINE VERIFICATION
# ============================================================

st.subheader("🌐 Primary Verification Services")

# Google News RSS
st.markdown("### 🟢 Google News RSS")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("Primary online verification source")
    st.caption("Searches Google News RSS for matching news coverage without requiring an API key.")
with col2:
    if GOOGLE_NEWS_ENABLED:
        st.success("Configured")
    else:
        st.error("Disabled")

# NewsAPI
st.markdown("### 🟢 NewsAPI")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("Primary online verification source")
    st.caption("Provides core news articles when a NewsAPI key is configured.")
with col2:
    if NEWS_API_ENABLED:
        st.success("Configured")
    else:
        st.warning("Not Configured")

# GNews API
st.markdown("### 🟢 GNews API")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("Primary online verification source")
    st.caption("Provides core news articles when a GNews API key is configured.")
with col2:
    if GNEWS_API_ENABLED:
        st.success("Configured")
    else:
        st.warning("Not Configured")

# Google Fact Check API
st.markdown("### 🟢 Google Fact Check API")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("Primary online verification source")
    st.caption("Provides core fact-check claims when a Google Fact Check API key is configured.")
with col2:
    if FACT_CHECK_ENABLED:
        st.success("Configured")
    else:
        st.warning("Not Configured")

st.divider()

# ============================================================
# VERIFICATION ARCHITECTURE
# ============================================================

st.subheader("🔍 TruthGuard AI Verification Architecture")
st.markdown(
    """
    <div style="
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 20px;
    ">
    <h4>📰 News Article</h4>
    <p>↓</p>
    <h4>🤖 Machine Learning Prediction</h4>
    <p>Fake / Real Probability</p>
    <p>↓</p>
    <h4>🌐 Multi-Primary Online Verification</h4>
    <p>Google News RSS &nbsp; + &nbsp; NewsAPI &nbsp; + &nbsp; GNews API &nbsp; + &nbsp; Google Fact Check API</p>
    <p>↓</p>
    <h4>🔎 Evidence Matching</h4>
    <p>Compare article claims with all aggregated primary sources</p>
    <p>↓</p>
    <h4>🧠 Final Assessment</h4>
    <p>Likely Real &nbsp; | &nbsp; Uncertain &nbsp; | &nbsp; Likely Fake</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# API CONFIGURATION STATUS
# ============================================================

st.subheader("🔐 API Configuration Status")

status_data = [
    ("Google News RSS", "🟢 Available", "No API key required"),
    ("NewsAPI", "🟢 Configured" if NEWS_API_ENABLED else "🟡 Missing Key", "API key detected" if NEWS_API_ENABLED else "No API key configured"),
    ("GNews API", "🟢 Configured" if GNEWS_API_ENABLED else "🟡 Missing Key", "API key detected" if GNEWS_API_ENABLED else "No API key configured"),
    ("Google Fact Check API", "🟢 Configured" if FACT_CHECK_ENABLED else "🟡 Missing Key", "API key detected" if FACT_CHECK_ENABLED else "No API key configured"),
    ("SMTP Email", "🟢 Configured" if SMTP_ENABLED else "🟡 Optional", "Email service ready" if SMTP_ENABLED else "Email service not configured")
]

for service, status, description in status_data:
    col1, col2, col3 = st.columns([2, 1, 3])
    with col1:
        st.write(f"**{service}**")
    with col2:
        st.write(status)
    with col3:
        st.caption(description)

st.divider()

# ============================================================
# API INFORMATION
# ============================================================

st.subheader("ℹ️ Primary API Configuration")
st.markdown(
    """
    To enable all primary verification sources, ensure your `.env` file contains the required keys.

    Example:
    ```text
    NEWS_API_KEY=your_newsapi_key
    GNEWS_API_KEY=your_gnews_key
    GOOGLE_FACT_CHECK_API_KEY=your_google_fact_check_key
    ```
    If any key is missing, TruthGuard AI will seamlessly continue using the remaining configured primary sources.
    """
)

st.divider()
st.subheader("📁 Project Configuration")

col1, col2 = st.columns(2)
with col1:
    st.write("**Project Directory**")
    st.code(str(BASE_DIR))
with col2:
    st.write("**Environment File**")
    st.code(str(ENV_FILE))

st.divider()
st.subheader("📧 Email Service")

if SMTP_ENABLED:
    st.success("SMTP email service is configured.")
    st.write(f"SMTP Server: `{SMTP_SERVER}`")
    st.write(f"SMTP Port: `{SMTP_PORT}`")
    if SMTP_USERNAME:
        st.write(f"SMTP Username: `{SMTP_USERNAME}`")
else:
    st.info("SMTP email is optional and is currently not configured.")

st.divider()
st.subheader("🛡️ TruthGuard AI System Status")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.success("🤖 ML Model\n\nAvailable")
with col2:
    if GOOGLE_NEWS_ENABLED or NEWS_API_ENABLED or GNEWS_API_ENABLED:
        st.success("🌐 Online Search\n\nAvailable")
    else:
        st.error("🌐 Online Search\n\nUnavailable")
with col3:
    if FACT_CHECK_ENABLED:
        st.success("🔎 Fact Check\n\nConfigured")
    else:
        st.warning("🔎 Fact Check\n\nMissing Key")
with col4:
    if SMTP_ENABLED:
        st.success("📧 Email\n\nConfigured")
    else:
        st.info("📧 Email\n\nOptional")

st.divider()
st.caption(f"{APP_ICON} {APP_NAME} v{APP_VERSION} • AI-Powered News Detection & Verification")