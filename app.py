import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Warehouse Inventory")

# 2. Data Loading
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url, dtype=str).fillna("")
    df.columns = df.columns.str.strip() # Clean header names
    return df

df = load_data()

st.title("📂 Warehouse Inventory System")

# 3. Search logic
search_term = st.text_input("Search by Filename or Barcode:")
filtered_df = df
if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

# 4. Filter Table Display: Remove the columns containing the links
# We hide both 'Image' and 'Image Link' from the view
cols_to_hide = ['Image', 'Image Link']
display_df = filtered_df.drop(columns=cols_to_hide, errors='ignore')

# 5. Display Table with selection
event = st.dataframe(
    display_df, 
    use_container_width=True, 
    selection_mode="single-row", 
    on_select="rerun"
)

# 6. Image Logic: Using an expander to act like a "button"
if event.selection["rows"]:
    selected_index = event.selection["rows"][0]
    selected_row = filtered_df.iloc[selected_index]
    
    # Try to find the link in either 'Image' or 'Image Link' column
    raw_link = selected_row.get("Image Link") or selected_row.get("Image", "")
    
    # "Triangle" expander effect
    with st.expander("▶ Click to view item image", expanded=True):
        if "drive.google.com" in raw_link and "/d/" in raw_link:
            # Convert Drive View link to Direct Link
            file_id = raw_link.split("/d/")[1].split("/")[0]
            direct_link = f"https://drive.google.com/uc?export=view&id={file_id}"
            st.image(direct_link, width=400)
        elif raw_link.startswith("http"):
            st.image(raw_link, width=400)
        else:
            st.warning("No image available for this item.")
