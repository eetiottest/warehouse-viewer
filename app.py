import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Warehouse Inventory")

# 2. Data Loading
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    # Read CSV and strip spaces from headers to prevent matching errors
    df = pd.read_csv(url, dtype=str).fillna("")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title("📂 Warehouse Inventory System")

# 3. Search logic
search_term = st.text_input("Search by Filename or Barcode:")
filtered_df = df
if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

# 4. EXPLICITLY separate display data from logic data
# This creates a copy that excludes the link column for the table
columns_to_drop = ['Image Link']
display_df = filtered_df.drop(columns=columns_to_drop, errors='ignore')

# 5. Display Table
image_placeholder = st.empty()

# We pass display_df (the one WITHOUT the link column)
event = st.dataframe(
    display_df, 
    use_container_width=True, 
    selection_mode="single-row", 
    on_select="rerun"
)

# 6. Image logic
if event.selection["rows"]:
    selected_index = event.selection["rows"][0]
    # We pull from filtered_df (the original one) to get the link
    selected_row = filtered_df.iloc[selected_index]
    img_link = selected_row.get("Image Link", "")
    
    with image_placeholder.container():
        if isinstance(img_link, str) and img_link.startswith("http"):
            st.image(img_link, width=400)
        else:
            st.info("No image found for this selection.")

# DEBUG: Use this to confirm the column is gone
with st.sidebar:
    st.write("Columns in Table:", display_df.columns.tolist())
