import streamlit as st
import pandas as pd
import os
import requests
from PIL import Image
from io import BytesIO
import re

# Page setup
st.set_page_config(
    page_title="Warehouse Image Viewer",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Warehouse Location Image Viewer")
st.markdown("---")

# Google Drive folder ID (REPLACE WITH YOURS)
FOLDER_ID = "PASTE_YOUR_FOLDER_ID_HERE"  # <-- Paste your folder ID here

# Your Excel file is still in GitHub
excel_path = "data.xlsx"

# Load Excel data
try:
    df = pd.read_excel(excel_path)
    df.columns = df.columns.str.strip()
    data_loaded = True
    st.sidebar.success(f"✅ Loaded {len(df)} records from Excel")
    
    with st.sidebar.expander("📊 Data Preview"):
        st.dataframe(df.head(10))
        
except Exception as e:
    df = pd.DataFrame()
    data_loaded = False
    st.sidebar.error(f"❌ Error loading Excel: {e}")

# Function to get images from Google Drive folder
@st.cache_data
def get_images_from_drive():
    """Get list of images from public Google Drive folder"""
    # For now, we'll use a simplified approach
    # You'll need to add your image file IDs here
    
    # This is a placeholder structure - you need to add your actual file IDs
    folder_contents = {
        "SHA": [
            # Format: {"id": "FILE_ID", "name": "SHA_001_10.jpg"},
        ],
        "SHB": [
            # Add your SHB files here
        ],
        "SHC": [
            # Add your SHC files here
        ]
    }
    return folder_contents

# Get folder contents
folder_contents = get_images_from_drive()

# Sidebar
with st.sidebar:
    st.header("📍 Select Location")
    selected_folder = st.selectbox(
        "Choose location:",
        options=[''] + list(folder_contents.keys())
    )
    
    if selected_folder:
        images = folder_contents[selected_folder]
        st.info(f"📸 Found **{len(images)}** images in {selected_folder}")

# Main content
if selected_folder:
    st.subheader(f"📍 Location: **{selected_folder}**")
    
    images = folder_contents[selected_folder]
    
    if images:
        # Search bar
        search_term = st.text_input("🔍 Search images:", placeholder="Type location code...")
        
        # Filter images
        if search_term:
            filtered_images = []
            for img in images:
                if search_term.lower() in img['name'].lower():
                    filtered_images.append(img)
            display_images = filtered_images
            st.write(f"📋 Found **{len(display_images)}** images matching '{search_term}'")
        else:
            display_images = images
            st.write(f"📋 Showing all **{len(display_images)}** images")
        
        # Display in 3 columns
        cols = st.columns(3)
        
        for idx, img_data in enumerate(display_images):
            with cols[idx % 3]:
                try:
                    # Load image from Google Drive
                    img_url = f"https://drive.google.com/drive/folders/1yUNa4AkLtY3JMIZbTSajNKGx-aWQdDiK?usp=sharing={img_data['id']}"
                    response = requests.get(img_url)
                    img = Image.open(BytesIO(response.content))
                    
                    st.image(img, use_container_width=True)
                    
                    filename = img_data['name']
                    
                    # Extract location code
                    location_code = None
                    for ext in ['.jpg', '.jpeg', '.png', '.gif']:
                        if filename.lower().endswith(ext):
                            location_code = filename[:-len(ext)]
                            break
                    
                    # Show data if available
                    if data_loaded and location_code:
                        match = df[df['location'] == location_code]
                        if not match.empty:
                            row = match.iloc[0]
                            with st.expander(f"📄 Details"):
                                st.write(f"**Record:** {row.get('no', 'N/A')}")
                                st.write(f"**QR:** {row.get('pallet_qr', 'None')}")
                                status = row.get('is_pallet_present', '')
                                if status == 'YES':
                                    st.write("**Status:** ✅ Present")
                                else:
                                    st.write("**Status:** ❌ Empty")
                except Exception as e:
                    st.error(f"Error loading image: {e}")
    else:
        st.warning("No images found")
else:
    st.info("👈 Select a location from the sidebar")

st.markdown("---")
st.caption("🏭 Warehouse Viewer")
