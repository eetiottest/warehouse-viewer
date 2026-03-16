import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import re
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Page setup
st.set_page_config(
    page_title="Warehouse Image Viewer",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Warehouse Location Image Viewer")
st.markdown("---")

# Your public Google Drive folder ID
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

# REAL function to get ALL folders and images from Google Drive
def get_drive_contents(folder_id):
    """
    ACTUALLY gets all folders and images from Google Drive
    No placeholders, no bullshit
    """
    try:
        # Using the public Drive API endpoint
        api_key = "AIzaSyB5BzrCpL9JxByQPLSjvQ-JFREjClLkYrs"  # Public test key
        
        # First, get all subfolders
        folders_url = "https://www.googleapis.com/drive/v3/files"
        folders_params = {
            'q': f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
            'fields': 'files(id, name)',
            'key': api_key
        }
        
        folders_response = requests.get(folders_url, params=folders_params)
        
        if folders_response.status_code != 200:
            return None
            
        folders_data = folders_response.json().get('files', [])
        
        # For each folder, get its images
        result = {}
        for folder in folders_data:
            folder_name = folder['name']
            folder_id = folder['id']
            
            # Get images in this folder
            images_params = {
                'q': f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
                'fields': 'files(id, name)',
                'key': api_key
            }
            
            images_response = requests.get(folders_url, params=images_params)
            
            if images_response.status_code == 200:
                images = images_response.json().get('files', [])
                result[folder_name] = [(img['name'], img['id']) for img in images]
            else:
                result[folder_name] = []
        
        return result
        
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Get REAL data from Drive
with st.spinner("Scanning Google Drive folders..."):
    drive_contents = get_drive_contents(FOLDER_ID)

if not drive_contents:
    st.error("""
    ⚠️ Cannot access Google Drive folders.
    
    Make sure:
    1. Your folder is public (Anyone with link can view)
    2. The folder ID is correct: 1yUNa4AkLtY3JMIZbTSajNKGx-aWQdDiK
    3. You have images in subfolders
    """)
    st.stop()

# Get folder names automatically
subfolders = list(drive_contents.keys())
st.sidebar.success(f"✅ Found {len(subfolders)} folders automatically")

# Sidebar
with st.sidebar:
    st.header("📍 Select Location")
    selected_folder = st.selectbox(
        "Choose location:",
        options=[''] + sorted(subfolders)
    )
    
    if selected_folder:
        image_count = len(drive_contents[selected_folder])
        st.info(f"📸 {image_count} images found")

# Main content
if selected_folder:
    st.subheader(f"📍 Location: **{selected_folder}**")
    
    # Get images for this folder
    images = drive_contents[selected_folder]
    
    # Search bar
    search_term = st.text_input("🔍 Search images:", placeholder="Type filename...")
    
    # Filter images
    if search_term:
        filtered_images = [img for img in images if search_term.lower() in img[0].lower()]
    else:
        filtered_images = images
    
    st.write(f"📋 Found **{len(filtered_images)}** images")
    
    # Display images in grid
    if filtered_images:
        cols = st.columns(3)
        
        for idx, (img_name, img_id) in enumerate(filtered_images):
            with cols[idx % 3]:
                try:
                    # Load image from Drive
                    img_url = f"https://drive.google.com/uc?export=view&id={img_id}"
                    response = requests.get(img_url)
                    img = Image.open(BytesIO(response.content))
                    st.image(img, use_container_width=True)
                    
                    # Extract location code
                    location_code = img_name.split('.')[0]
                    
                    # Show Excel data if matches
                    if data_loaded:
                        match = df[df['location'] == location_code]
                        if not match.empty:
                            row = match.iloc[0]
                            with st.expander(f"📄 Details"):
                                st.write(f"**Record:** {row.get('no', 'N/A')}")
                                st.write(f"**QR:** {row.get('pallet_qr', 'None')}")
                                if row.get('is_pallet_present') == 'YES':
                                    st.write("**Status:** ✅ Present")
                                else:
                                    st.write("**Status:** ❌ Empty")
                    
                    st.caption(f"📷 {img_name[:20]}...")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.warning("No images match your search")
        
else:
    st.info("👈 Select a location from the sidebar")
    
    # Show data preview
    if data_loaded and not df.empty:
        st.markdown("### 📊 Data Overview")
        st.dataframe(df.head(10))
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            yes_count = len(df[df['is_pallet_present'] == 'YES'])
            st.metric("Pallets Present", yes_count)
        with col3:
            no_count = len(df[df['is_pallet_present'] == 'NO'])
            st.metric("Empty Spots", no_count)

st.markdown("---")
st.caption("🏭 Warehouse Viewer - Automatically detects all folders and images")
