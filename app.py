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
MAIN_FOLDER_ID = "1yUNa4AkLtY3JMIZbTSajNKGx-aWQdDiK"

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

# Function to get contents of a Google Drive folder (works for ANY folder)
def get_folder_contents(folder_id):
    """Returns list of (name, id, type) for all items in a folder"""
    items = []
    try:
        # This is the SAME logic that works for images
        page_token = None
        while True:
            url = "https://www.googleapis.com/drive/v3/files"
            params = {
                'q': f"'{folder_id}' in parents and trashed=false",
                'fields': 'nextPageToken, files(id, name, mimeType)',
                'pageSize': 100,
                'key': 'AIzaSyB5BzrCpL9JxByQPLSjvQ-JFREjClLkYrs'
            }
            if page_token:
                params['pageToken'] = page_token
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                for file in data.get('files', []):
                    if 'application/vnd.google-apps.folder' in file['mimeType']:
                        items.append((file['name'], file['id'], 'folder'))
                    elif 'image/' in file['mimeType']:
                        items.append((file['name'], file['id'], 'image'))
                
                page_token = data.get('nextPageToken')
                if not page_token:
                    break
            else:
                break
    except:
        pass
    return items

# Get ALL contents of main folder
all_items = get_folder_contents(MAIN_FOLDER_ID)

# Separate folders and images
subfolders = [(name, id) for name, id, type in all_items if type == 'folder']
images_in_main = [(name, id) for name, id, type in all_items if type == 'image']

# Show what we found
st.sidebar.success(f"✅ Found {len(subfolders)} subfolders and {len(images_in_main)} images in main folder")

# Sidebar - folder selection
with st.sidebar:
    st.header("📍 Select Location")
    
    folder_names = [name for name, _ in subfolders]
    selected_folder = st.selectbox(
        "Choose location:",
        options=[''] + sorted(folder_names)
    )
    
    if selected_folder:
        # Get the folder ID for selected folder
        folder_id = dict(subfolders)[selected_folder]
        
        # Get images in this subfolder
        subfolder_items = get_folder_contents(folder_id)
        folder_images = [(name, id) for name, id, type in subfolder_items if type == 'image']
        st.info(f"📸 {len(folder_images)} images in this folder")

# Main content
if selected_folder:
    st.subheader(f"📍 Location: **{selected_folder}**")
    
    # Get folder ID and images
    folder_id = dict(subfolders)[selected_folder]
    subfolder_items = get_folder_contents(folder_id)
    folder_images = [(name, id) for name, id, type in subfolder_items if type == 'image']
    
    # Filter Excel data
    if data_loaded:
        location_data = df[df['location'].str.startswith(selected_folder, na=False)]
        
        if not location_data.empty:
            # Search bar
            search_term = st.text_input("🔍 Search:", placeholder="Type location code...")
            
            # Filter Excel data
            if search_term:
                filtered_data = location_data[location_data['location'].str.contains(search_term, case=False)]
            else:
                filtered_data = location_data
            
            # Display records
            st.dataframe(filtered_data[['no', 'location', 'pallet_qr', 'is_pallet_present']])
            
            # Display images
            if folder_images:
                st.markdown("### 📸 Images")
                cols = st.columns(3)
                
                for idx, (img_name, img_id) in enumerate(folder_images):
                    if search_term and search_term.lower() not in img_name.lower():
                        continue
                        
                    with cols[idx % 3]:
                        try:
                            img_url = f"https://drive.google.com/uc?export=view&id={img_id}"
                            response = requests.get(img_url)
                            img = Image.open(BytesIO(response.content))
                            st.image(img, use_container_width=True)
                            
                            # Extract location code
                            location_code = img_name.split('.')[0]
                            
                            # Show matching Excel data
                            match = df[df['location'] == location_code]
                            if not match.empty:
                                row = match.iloc[0]
                                qr = row.get('pallet_qr', '')
                                if pd.notna(qr) and qr != '':
                                    st.caption(f"QR: {qr[:15]}...")
                                if row.get('is_pallet_present') == 'YES':
                                    st.caption("✅ Present")
                                else:
                                    st.caption("❌ Empty")
                            else:
                                st.caption(img_name[:20])
                        except Exception as e:
                            st.error(f"Error")
            else:
                st.info("No images in this folder")
        else:
            st.warning("No Excel records for this location")
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
st.caption("🏭 Warehouse Viewer - Same logic for folders AND images")
