import streamlit as st
from config.settings import inject_global_css
from database.database import list_analyses, get_analysis

st.set_page_config(page_title="Verification Engine | TruthGuard AI", page_icon="🧠", layout="wide")
inject_global_css()

st.markdown('<div class="tg-title">🧠 Verification Engine</div>', unsafe_allow_html=True)
rows = list_analyses()

if not rows:
    st.info("No analyses yet. Start from Analyse News.")
else:
    ids = [r["analysis_id"] for r in rows]
    selected = st.selectbox("Select Analysis", ids)
    r = get_analysis(selected)
    st.subheader("Pipeline Status")
    cols = st.columns(5)
    steps = [
        ("🧠 ML", r["ml_prediction"]),
        ("🌐 Online", r["online_status"]),
        ("🔎 Fact Check", r["fact_check_status"]),
        ("📰 Source", f'{r["source_credibility"]:.1f}/100'),
        ("🛡️ Final", r["final_assessment"])
    ]
    for c, (a, b) in zip(cols, steps):
        c.metric(a, b)
    st.markdown("---")
    st.subheader("Evidence")
    for s in r["sources"]:
        st.markdown(f'**{s["source_name"]}** — {s["title"]}')
        st.caption(f'{s["evidence_type"]} | relevance {s["relevance"]} | credibility {s["credibility"]}')
        st.write(s["url"])
    st.subheader("Verification Note")
    st.info(r["verification_note"])