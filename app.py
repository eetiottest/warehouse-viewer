import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Warehouse Inventory")

@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url, dtype=str).fillna("")
    # Strip whitespace from headers so names like "Image " become "Image"
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title("📂 Warehouse Inventory System")

# Search logic
search_term = st.text_input("Search by Filename or Barcode:")
filtered_df = df
if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

# 1. DROP the columns you don't want to see in the table
# Make sure these names exactly match the header names in your sheet
cols_to_hide = ['Image', 'Image Link']
display_df = filtered_df.drop(columns=cols_to_hide, errors='ignore')

# 2. Display Table
image_placeholder = st.empty()

event = st.dataframe(
    display_df, 
    use_container_width=True, 
    selection_mode="single-row", 
    on_select="rerun"
)

# 3. Image Logic
if event.selection["rows"]:
    selected_index = event.selection["rows"][0]
    # We pull the actual row from 'filtered_df' (which still has the image links)
    selected_row = filtered_df.iloc[selected_index]
    
    # Try to find the link in either 'Image' or 'Image Link' column
    img_link = selected_row.get("Image Link") or selected_row.get("Image")
    
    with image_placeholder.container():
        if img_link and img_link.startswith("http"):
            st.image(img_link, width=400)
        else:
            st.warning("No valid image link found in the selected row.")
