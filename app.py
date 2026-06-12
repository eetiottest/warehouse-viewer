import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# CSS to hide the selection checkbox column
hide_checkbox_css = """
    <style>
    div[data-testid="stDataFrame"] table thead tr th:first-child,
    div[data-testid="stDataFrame"] table tbody tr td:first-child {
        display: none;
    }
    </style>
"""
st.markdown(hide_checkbox_css, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Drop the columns
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

st.subheader("Inventory Data")

# Display the table
# hide_index=True removes the row numbers
event = st.dataframe(
    display_df, 
    use_container_width=True, 
    selection_mode="single-row", 
    on_select="rerun",
    hide_index=True 
)

# Interaction: Clicking a row shows details
if event.selection.get("rows"):
    selected_index = event.selection["rows"][0]
    selected_row = df.iloc[selected_index]
    
    details = selected_row.drop(labels=['Image', 'Image Link'], errors='ignore')
    
    with st.expander(f"Details for: {selected_row.get('Location')}", expanded=True):
        st.write(details)
