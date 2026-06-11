import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Warehouse Inventory Dashboard")

# 2. Data Loading
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url, dtype=str).fillna("")
    return df

df = load_data()

st.title("📂 Warehouse Inventory System")

# 3. Search/Filter
search_term = st.text_input("Search by Filename or Barcode:")

if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
else:
    filtered_df = pd.DataFrame() # Keep empty until search

# 4. Display Logic
if not filtered_df.empty:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Table displayed without the extra header
        st.dataframe(filtered_df, use_container_width=True)
        
    with col2:
        # Only show image if exactly one result is found OR if specific logic is met
        if len(filtered_df) == 1:
            selected_row = filtered_df.iloc[0]
            img_link = selected_row.get("Direct_Link", "")
            
            if img_link and img_link.startswith("http"):
                st.image(img_link, use_container_width=True)
            else:
                st.warning("No image available for this item.")
        else:
            st.info("Select or narrow search to one item to view the image.")
else:
    st.info("Enter a search term to find items.")
