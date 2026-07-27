import streamlit as st
import pandas as pd
import plotly.express as px
from config.settings import inject_global_css
from database.database import list_analyses
from ml.model_utils import load_artifacts

st.set_page_config(page_title="Analytics | TruthGuard AI", page_icon="📈", layout="wide")
inject_global_css()

st.markdown('<div class="tg-title">📈 Analytics</div>', unsafe_allow_html=True)
df = pd.DataFrame(list_analyses())

if df.empty:
    st.info("Analyse some articles to populate analytics.")
else:
    df["date"] = pd.to_datetime(df.created_at, errors="coerce").dt.date
    daily = df.groupby("date").size().reset_index(name="analyses")
    st.plotly_chart(px.line(daily, x="date", y="analyses", markers=True, title="Analysis Trend"), use_container_width=True)

    a, b = st.columns(2)
    with a:
        st.plotly_chart(px.bar(df, x="final_assessment", title="Assessment Distribution"), use_container_width=True)
    with b:
        st.plotly_chart(px.box(df, y="final_score", x="ml_prediction", title="Final Score by ML Prediction"), use_container_width=True)

    st.subheader("Model Metrics")
    model, vec, meta = load_artifacts()
    if meta:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Accuracy", f'{meta.get("accuracy", 0) * 100:.2f}%')
        m2.metric("Precision", f'{meta.get("precision", 0) * 100:.2f}%')
        m3.metric("Recall", f'{meta.get("recall", 0) * 100:.2f}%')
        m4.metric("F1", f'{meta.get("f1", 0) * 100:.2f}%')
    else:
        st.warning("Train the ML model to show model metrics.")