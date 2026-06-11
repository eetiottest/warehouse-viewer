import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Warehouse Inventory Dashboard")

# 2. Data Loading
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    return pd.read_csv(url, dtype=str).fillna("")

df = load_data()

st.title("📂 Warehouse Inventory System")

# 3. Search logic
search_term = st.text_input("Search by Filename or Barcode:")
if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
else:
    filtered_df = df

# 4. CRITICAL: Explicitly create the display dataframe by dropping the column
# We are creating a brand new variable 'display_df' that 100% excludes that column
display_df = filtered_df.drop(columns=['Image Link'], errors='ignore')

# 5. Display Table
image_placeholder = st.empty()

# We pass 'display_df' (the cleaned version) to the table
event = st.dataframe(
    display_df, 
    use_container_width=True, 
    selection_mode="single-row", 
    on_select="rerun"
)

# 6. Display Image
if event.selection["rows"]:
    selected_index = event.selection["rows"][0]
    # We pull the actual data from 'filtered_df' (which HAS the link)
    selected_row = filtered_df.iloc[selected_index]
    
    img_link = selected_row.get("Image Link", "")
    
    with image_placeholder.container():
        if isinstance(img_link, str) and img_link.startswith("http"):
            st.image(img_link, width=400)
