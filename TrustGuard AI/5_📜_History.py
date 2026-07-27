import streamlit as st
import pandas as pd
from config.settings import inject_global_css
from database.database import list_analyses, get_analysis, delete_analysis
from reports.pdf_report import build_pdf
from reports.email_report import send_report

st.set_page_config(page_title="History | TruthGuard AI", page_icon="📜", layout="wide")
inject_global_css()

st.markdown('<div class="tg-title">📜 Analysis History</div>', unsafe_allow_html=True)
rows = list_analyses()
df = pd.DataFrame(rows)

if df.empty:
    st.info("No history available.")
else:
    q = st.text_input("Search")
    statuses = st.multiselect("Filter Assessment", sorted(df.final_assessment.dropna().unique()))
    filtered = df.copy()

    if q:
        filtered = filtered[filtered.article_title.str.contains(q, case=False, na=False)]
    if statuses:
        filtered = filtered[filtered.final_assessment.isin(statuses)]

    st.dataframe(
        filtered[["analysis_id", "article_title", "ml_prediction", "online_status", "fact_check_status", "final_assessment", "final_score", "created_at"]],
        use_container_width=True
    )

    selected = st.selectbox("Open Analysis", filtered.analysis_id.tolist())
    r = get_analysis(int(selected))

    st.subheader(r["article_title"])
    st.write(r["article_text"][:4000])

    c1, c2, c3 = st.columns(3)
    c1.download_button("📄 PDF", build_pdf(r), file_name=f"truthguard_{selected}.pdf", mime="application/pdf", key=f"pdf_{selected}")

    if c2.button("🗑️ Delete", key=f"delete_{selected}"):
        delete_analysis(int(selected))
        st.rerun()

    with c3:
        recipient = st.text_input("Recipient Gmail", key=f"email_{selected}")
        if st.button("📧 Send Report", key=f"send_{selected}"):
            try:
                send_report(recipient, "TruthGuard AI Verification Report", f'Final Assessment: {r["final_assessment"]}\nScore: {r["final_score"]}%', build_pdf(r))
                st.success("Report sent.")
            except Exception as e:
                st.error(str(e))