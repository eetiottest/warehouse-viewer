import streamlit as st
import pandas as pd

# Set up the page
st.set_page_config(layout="wide", page_title="Warehouse System")

@st.cache_data(ttl=600)
def load_data():
    # Your live CSV link
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url, dtype=str).fillna("")
    return df

df = load_data()

st.title("📂 Warehouse Inventory")

# Search feature
search_term = st.text_input("Enter filename or search term:")
if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
else:
    filtered_df = df

if not filtered_df.empty:
    selected_row = filtered_df.iloc[0]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Item Details")
        st.table(selected_row)
        
    with col2:
        st.subheader("Image Preview")
        # Ensure 'Direct_Link' matches your spreadsheet column header
        img_link = selected_row.get("Direct_Link", "")
        
        if img_link.startswith("http"):
            st.image(img_link, width=500)
        else:
            st.warning("No image found for this item.")
else:
    st.info("No items found.")
