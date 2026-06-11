import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Warehouse Full v1")

# Custom UI styling to match your AppSheet look
st.html("""<style>
    .appsheet-table-wrapper { width: 100%; background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; overflow-x: auto; margin-top: 15px; }
    .appsheet-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    .appsheet-table th { background-color: #F1F5F9; color: #475569; padding: 12px 16px; border-bottom: 2px solid #E2E8F0; text-transform: uppercase; font-size: 0.8rem; }
    .appsheet-table td { padding: 12px 16px; border-bottom: 1px solid #E2E8F0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.9rem; }
</style>""")

@st.cache_data(ttl=600)
def load_data():
    # This is the direct CSV link for your sheet
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQkarZ8ud6N-YO8aFTgIMidqO5uCbyKoqiIZaukL6Ql8K99XRX_-3cjmuGfaNWdOh8QHZWLP4-ePYuN/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.astype(str).str.strip()
    return df

# Main logic
try:
    df = load_data()
    st.markdown("### 📂 Warehouse Full v1")
    # Using your CSS wrapper for the dataframe
    st.markdown('<div class="appsheet-table-wrapper">', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Could not load data: {e}")
