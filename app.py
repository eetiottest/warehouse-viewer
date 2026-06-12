import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide")

# 2. CSS to hide the selection checkbox column
hide_checkbox_css = """
    <style>
    div[data-testid="stDataFrame"] table thead tr th:first-child,
    div[data-testid="stDataFrame"] table tbody tr td:first-child {
        display: none;
    }
    </style>
"""
st.markdown(hide_checkbox_css, unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    # dtype=str forces all data to be read as text, preventing scientific notation
    df = pd.read_csv(url, dtype=str) 
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# 4. Filter display columns
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

st.subheader("Inventory Data")

# 5. Main Table Display
event = st.dataframe(
    display_df, 
    use_container_width=True, 
    selection_mode="single-row", 
    on_select="rerun",
    hide_index=True
)

# 6. Detail View Layout
if event.selection.get("rows"):
    selected_index = event.selection["rows"][0]
    row = df.iloc[selected_index]
    
    with st.expander(f"Details for: {row.get('Location')}", expanded=True):
        # Loop through columns and print as clean text
        for col in display_df.columns:
            c1, c2 = st.columns([1, 2])
            c1.markdown(f"**{col}**")
            # row[col] is already a string due to dtype=str
            c2.write(row[col])
