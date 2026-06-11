import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Warehouse Inventory Dashboard")

@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    return pd.read_csv(url, dtype=str).fillna("")

df = load_data()

st.title("📂 Warehouse Inventory System")

# Search input
search_term = st.text_input("Search by Filename or Barcode:")
if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
else:
    filtered_df = df

# Create a container for the image that only shows when needed
image_placeholder = st.empty()

# Display the table (Always shown)
event = st.dataframe(
    filtered_df, 
    use_container_width=True, 
    selection_mode="single-row", 
    on_select="rerun"
)

# Logic to show image only when selected
if event.selection["rows"]:
    selected_index = event.selection["rows"][0]
    selected_row = filtered_df.iloc[selected_index]
    img_link = selected_row.get("Direct_Link", "")
    
    with image_placeholder.container():
        if img_link and img_link.startswith("http"):
            st.image(img_link, width=400)
        else:
            st.error("No image available for this item.")
