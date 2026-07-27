import streamlit as st
import pandas as pd
from config.settings import inject_global_css
from database.database import get_connection

st.set_page_config(page_title="Sources | TruthGuard AI", page_icon="📰", layout="wide")
inject_global_css()

st.markdown('<div class="tg-title">📰 Source Intelligence</div>', unsafe_allow_html=True)
conn = get_connection()
df = pd.read_sql_query("SELECT source_name, COUNT(*) uses, AVG(credibility) avg_credibility FROM evidence GROUP BY source_name ORDER BY uses DESC", conn)
conn.close()

if df.empty:
    st.info("No source evidence collected yet.")
else:
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index("source_name")["avg_credibility"])