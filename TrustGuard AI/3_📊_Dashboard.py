import streamlit as st
import pandas as pd
import plotly.express as px
from config.settings import inject_global_css
from database.database import list_analyses

st.set_page_config(page_title="Dashboard | TruthGuard AI", page_icon="📊", layout="wide")
inject_global_css()

st.markdown('<div class="tg-title">📊 Intelligence Dashboard</div>', unsafe_allow_html=True)
df = pd.DataFrame(list_analyses())

if df.empty:
    st.info("No analysis data yet.")
else:
    total = len(df)
    real = int(df.final_assessment.str.contains("REAL", na=False).sum())
    fake = int(df.final_assessment.str.contains("FAKE", na=False).sum())
    uncertain = total - real - fake

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Articles Analysed", total)
    c2.metric("Real / Likely Real", real)
    c3.metric("Fake / Likely Fake", fake)
    c4.metric("Uncertain", uncertain)

    c5, c6 = st.columns(2)
    with c5:
        fig = px.pie(df, names="final_assessment", title="Final Assessments", hole=.5)
        st.plotly_chart(fig, use_container_width=True)
    with c6:
        fig = px.histogram(df, x="final_score", nbins=10, title="Final Score Distribution")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recent Activity")
    st.dataframe(
        df[["analysis_id", "article_title", "ml_prediction", "online_status", "fact_check_status", "final_assessment", "final_score", "created_at"]].head(20),
        use_container_width=True
    )