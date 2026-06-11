import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Warehouse Inventory Dashboard")

# 2. Data Loading with Caching
@st.cache_data(ttl=600)
def load_data():
    # Replace with your actual Published CSV link
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url, dtype=str).fillna("")
    return df

# Load the data
df = load_data()

# 3. Dashboard UI
st.title("📂 Warehouse Inventory System")

# Search/Filter
search_term = st.text_input("Search by Filename or Barcode:")

if search_term:
    # Filter the dataframe based on search input
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
else:
    filtered_df = df

# 4. Display Logic
if not filtered_df.empty:
    st.write(f"Showing {len(filtered_df)} matches")
    
    # Layout with columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Data Table")
        # Displaying the filtered results as an interactive table
        st.dataframe(filtered_df, use_container_width=True)
        
    with col2:
        st.subheader("Image Preview")
        # Select the first item from the filtered list to show its image
        selected_row = filtered_df.iloc[0]
        img_link = selected_row.get("Direct_Link", "")
        
        if img_link and img_link.startswith("http"):
            st.image(img_link, caption=selected_row.get("Filename", "Image"), use_container_width=True)
        else:
            st.warning("No image available for this item.")
else:
    st.info("No items found. Please try a different search term.")
