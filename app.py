import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

st.subheader("Inventory Data")

# 1. Display the table (Selection triggers interaction)
event = st.dataframe(
    display_df, 
    use_container_width=True, 
    selection_mode="single-row", 
    on_select="rerun",
    hide_index=True
)

# 2. Custom layout for details (No headers, no index, no value column)
if event.selection.get("rows"):
    selected_index = event.selection["rows"][0]
    row = df.iloc[selected_index]
    
    with st.expander(f"Details for: {row.get('Location')}", expanded=True):
        # We loop through columns and print them side by side
        for col in display_df.columns:
            c1, c2 = st.columns([1, 2])
            c1.markdown(f"**{col}**")
            c2.write(str(row[col]))
