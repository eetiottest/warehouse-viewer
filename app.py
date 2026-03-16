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

# FIRST: Get ALL subfolders automatically using the same logic
# We'll store folder info here
folder_info = {}  # folder_name -> folder_id

try:
    # Use the public Drive API to list folders
    api_url = "https://www.googleapis.com/drive/v3/files"
    params = {
        'q': f"'{FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        'fields': 'files(id, name)',
        'key': 'AIzaSyB5BzrCpL9JxByQPLSjvQ-JFREjClLkYrs'  # Public test key
    }
    
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        folders = response.json().get('files', [])
        for folder in folders:
            folder_info[folder['name']] = folder['id']
        st.sidebar.success(f"✅ Automatically found {len(folder_info)} folders")
    else:
        st.error("Could not fetch folders. Make sure your main folder is public.")
        st.stop()
        
except Exception as e:
    st.error(f"Error scanning folders: {e}")
    st.stop()

# Get folder names automatically
subfolders = list(folder_info.keys())

# Sidebar
with st.sidebar:
    st.header("📍 Select Location")
    selected_folder = st.selectbox(
        "Choose location:",
        options=[''] + sorted(subfolders)
    )
    
    if selected_folder:
        folder_id = folder_info[selected_folder]
        
        # Now get images in this folder
        try:
            img_params = {
                'q': f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
                'fields': 'files(id, name)',
                'key': 'AIzaSyB5BzrCpL9JxByQPLSjvQ-JFREjClLkYrs'
            }
            
            img_response = requests.get(api_url, params=img_params)
            if img_response.status_code == 200:
                images = img_response.json().get('files', [])
                st.info(f"📸 {len(images)} images found")
            else:
                st.warning("Could not load images")
        except:
            st.warning("Error loading images")

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
            
            # Get and display images for this folder
            folder_id = folder_info[selected_folder]
            try:
                img_params = {
                    'q': f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
                    'fields': 'files(id, name)',
                    'key': 'AIzaSyB5BzrCpL9JxByQPLSjvQ-JFREjClLkYrs'
                }
                
                img_response = requests.get(api_url, params=img_params)
                if img_response.status_code == 200:
                    images = img_response.json().get('files', [])
                    
                    if images:
                        st.markdown("### 📸 Images")
                        cols = st.columns(3)
                        
                        for idx, img in enumerate(images):
                            if search_term and search_term.lower() not in img['name'].lower():
                                continue
                                
                            with cols[idx % 3]:
                                try:
                                    img_url = f"https://drive.google.com/uc?export=view&id={img['id']}"
                                    response = requests.get(img_url)
                                    picture = Image.open(BytesIO(response.content))
                                    st.image(picture, use_container_width=True)
                                    st.caption(img['name'])
                                except:
                                    st.error(f"Failed to load")
                    else:
                        st.info("No images in this folder")
            except Exception as e:
                st.error(f"Error loading images: {e}")
        else:
            st.warning("No records found in Excel for this location")
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
st.caption("🏭 Warehouse Viewer - Automatically detects all folders")
