import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Warehouse Inventory")

# 2. Data Loading
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url, dtype=str).fillna("")
    df.columns = df.columns.str.strip()  # Clean header names
    return df

df = load_data()

st.title("📂 Warehouse Inventory System")

# 3. Filter Columns: Remove the ones you don't want in the table
# We keep them in the dataframe 'df' so we can still use the links for images
cols_to_hide = ['Image', 'Image Link']
display_df = df.drop(columns=cols_to_hide, errors='ignore')

# 4. Display Table
# use_container_width=False ensures the horizontal scrollbar stays active
# column_config keeps your text columns wide and readable
st.subheader("Inventory Data")
event = st.dataframe(
    display_df, 
    use_container_width=False,
    selection_mode="single-row", 
    on_select="rerun",
    column_config={
        "Description": st.column_config.TextColumn("Description", width=300),
        "Description Master": st.column_config.TextColumn("Description Master", width=300)
    }
)

# 5. Image Logic: Using an expander as the "triangle button"
if event.selection["rows"]:
    selected_index = event.selection["rows"][0]
    selected_row = df.iloc[selected_index]
    
    # Retrieve the link from the original dataframe (which has the columns)
    raw_link = selected_row.get("Image Link") or selected_row.get("Image", "")
    
    with st.expander("▶ Click here to view the item image", expanded=True):
        if "drive.google.com" in raw_link and "/d/" in raw_link:
            # Conversion logic: View link -> Direct download link
            file_id = raw_link.split("/d/")[1].split("/")[0]
            direct_link = f"https://drive.google.com/uc?export=view&id={file_id}"
            st.image(direct_link, width=400)
        elif raw_link.startswith("http"):
            st.image(raw_link, width=400)
        else:
            st.warning("No image link found for this item.")
