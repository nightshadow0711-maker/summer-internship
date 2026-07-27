import streamlit as st
import pandas as pd
from config.settings import inject_global_css
from database.database import list_analyses
from reports.csv_export import analyses_to_csv

st.set_page_config(page_title="Reports | TruthGuard AI", page_icon="📄", layout="wide")
inject_global_css()

st.markdown('<div class="tg-title">📄 Reports & Exports</div>', unsafe_allow_html=True)
rows = list_analyses()

if not rows:
    st.info("No analyses available.")
else:
    st.metric("Available Reports", len(rows))
    st.download_button("📊 Export All History as CSV", analyses_to_csv(rows), file_name="truthguard_history.csv", mime="text/csv", key="export_all_csv")
    st.dataframe(pd.DataFrame(rows), use_container_width=True)