import streamlit as st

def status_badge(label):
    cls="tg-uncertain"
    if "REAL" in label: cls="tg-real"
    if "FAKE" in label: cls="tg-fake"
    st.markdown(f'<div class="tg-card"><span class="{cls}">{label}</span></div>',unsafe_allow_html=True)
