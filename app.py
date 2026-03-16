import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import re
import os

# Page setup
st.set_page_config(
    page_title="Warehouse Image Viewer",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Warehouse Location Image Viewer")
st.markdown("---")

# Your Google Drive folder ID
FOLDER_ID = "1yUNa4AkLtY3JMIZbTSajNKGx-aWQdDiK"

# Your Excel file
excel_path = "data.xlsx"

# Load Excel data
try:
    df = pd.read_excel(excel_path)
    df.columns = df.columns.str.strip()
    data_loaded = True
except Exception as e:
    df = pd.DataFrame()
    data_loaded = False

# HARDCODED subfolders - YOU JUST LIST THEM ONCE
subfolders = ["SHA", "SHB", "SHC"]  # <-- Add ALL your folder names here

# For each folder, we need image file IDs (get these once from Drive)
# Format: folder_name -> list of (filename, file_id)
image_data = {
    "SHA": [
        # ("SHA_001_10.jpg", "FILE_ID_HERE"),
        # ("SHA_001_20.jpg", "FILE_ID_HERE"),
    ],
    "SHB": [
        # ("SHB_001_10.jpg", "FILE_ID_HERE"),
    ],
    "SHC": [
        # ("SHC_001_10.jpg", "FILE_ID_HERE"),
    ]
}

# Sidebar
with st.sidebar:
    st.header("📍 Select Location")
    selected_folder = st.selectbox(
        "Choose location:",
        options=[''] + sorted(subfolders)
    )
    
    if selected_folder and data_loaded:
        location_records = df[df['location'].str.startswith(selected_folder, na=False)]
        st.info(f"📊 {len(location_records)} records in Excel")

# Main content
if selected_folder:
    st.subheader(f"📍 Location: **{selected_folder}**")
    
    # Filter Excel data
    if data_loaded:
        location_data = df[df['location'].str.startswith(selected_folder, na=False)]
        
        if not location_data.empty:
            # Search bar
            search_term = st.text_input("🔍 Search:", placeholder="Type location code...")
            
            # Filter based on search
            if search_term:
                filtered_data = location_data[location_data['location'].str.contains(search_term, case=False)]
            else:
                filtered_data = location_data
            
            # Display records
            st.dataframe(filtered_data[['no', 'location', 'pallet_qr', 'is_pallet_present']])
            
            # Show images if we have them
            if selected_folder in image_data and image_data[selected_folder]:
                st.markdown("### 📸 Images")
                cols = st.columns(3)
                
                folder_images = image_data[selected_folder]
                for idx, (filename, file_id) in enumerate(folder_images):
                    if search_term and search_term.lower() not in filename.lower():
                        continue
                        
                    with cols[idx % 3]:
                        try:
                            img_url = f"https://drive.google.com/uc?export=view&id={file_id}"
                            response = requests.get(img_url)
                            img = Image.open(BytesIO(response.content))
                            st.image(img, use_container_width=True)
                            st.caption(filename)
                        except:
                            st.error(f"Failed to load {filename}")
            else:
                # Just show folder link
                st.info(f"📸 Add images or [open folder in Drive](https://drive.google.com/drive/folders/{FOLDER_ID}/{selected_folder})")
        else:
            st.warning("No records found")
else:
    st.info("👈 Select a location from the sidebar")
    
    # Show data overview
    if data_loaded and not df.empty:
        st.markdown("### 📊 Data Overview")
        st.dataframe(df.head(10))
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            if 'is_pallet_present' in df.columns:
                yes_count = len(df[df['is_pallet_present'] == 'YES'])
                st.metric("Pallets Present", yes_count)
        with col3:
            if 'is_pallet_present' in df.columns:
                no_count = len(df[df['is_pallet_present'] == 'NO'])
                st.metric("Empty Spots", no_count)

st.markdown("---")
st.caption("🏭 Warehouse Viewer")
