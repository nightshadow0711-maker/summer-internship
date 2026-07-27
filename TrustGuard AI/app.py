import streamlit as st
from config.settings import APP_NAME, APP_ICON, inject_global_css
from database.database import init_db

st.set_page_config(page_title=APP_NAME, page_icon=APP_ICON, layout="wide", initial_sidebar_state="expanded")
inject_global_css()
init_db()

st.sidebar.markdown(f"## {APP_ICON} {APP_NAME}")
st.sidebar.caption("AI-Powered News Intelligence & Verification Platform")
st.sidebar.success("● SYSTEM ONLINE")

st.title("🛡️ TRUTHGUARD AI")
st.subheader("AI-Powered News Intelligence & Verification Platform")
st.markdown("### Detect • Verify • Understand")
st.info("Use the **Analyse News** page from the sidebar to submit article text, a URL, or a file. The complete pipeline combines ML prediction, online evidence, fact-checking, source credibility, and a final assessment.")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("ML Analysis", "Ready", "TF-IDF + Logistic Regression")
with c2:
    st.metric("Online Verification", "Ready", "News + Web Evidence")
with c3:
    st.metric("Fact Checking", "Ready", "Fact-check API + Search")

st.markdown("---")
st.markdown("### Verification Pipeline")
p1, p2, p3, p4, p5 = st.columns(5)
for col, title, desc in [
    (p1, "🧠 ML", "Fake / Real prediction"),
    (p2, "🌐 Search", "Related reporting"),
    (p3, "🔎 Fact Check", "Claim verification"),
    (p4, "📰 Sources", "Credibility analysis"),
    (p5, "🛡️ Final", "Evidence-based assessment"),
]:
    with col:
        st.markdown(f"**{title}**")
        st.caption(desc)

st.markdown("---")
st.caption("TruthGuard AI is an educational decision-support system. A model prediction is not proof of truth or falsehood.")