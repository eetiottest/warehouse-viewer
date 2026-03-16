import streamlit as st
import pandas as pd
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

# Your public Drive main folder ID
MAIN_FOLDER_ID = "1yUNa4AkLtY3JMIZbTSajNKGx-aWQdDiK"

# Your Excel file
excel_path = "data.xlsx"

# Load Excel data
try:
    df = pd.read_excel(excel_path)
    df.columns = df.columns.str.strip()
    # Convert pallet_qr to string to avoid issues
    if 'pallet_qr' in df.columns:
        df['pallet_qr'] = df['pallet_qr'].astype(str)
    data_loaded = True
    st.sidebar.success(f"✅ Excel loaded: {len(df)} records")
except Exception as e:
    st.error(f"❌ Error loading Excel: {e}")
    st.stop()

# Function to get all subfolders in main folder
def get_subfolders(folder_id):
    """Get all subfolder names and IDs"""
    folders = {}
    try:
        url = "https://www.googleapis.com/drive/v3/files"
        params = {
            'q': f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
            'fields': 'files(id, name)',
            'key': 'AIzaSyB5BzrCpL9JxByQPLSjvQ-JFREjClLkYrs'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            for folder in response.json().get('files', []):
                folders[folder['name']] = folder['id']
    except Exception as e:
        st.error(f"Error getting folders: {e}")
    return folders

# Function to get all images from a specific folder
def get_images_from_folder(folder_id):
    """Get all images from a folder, return dict of filename -> file_id"""
    images = {}
    try:
        url = "https://www.googleapis.com/drive/v3/files"
        params = {
            'q': f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
            'fields': 'files(id, name)',
            'key': 'AIzaSyB5BzrCpL9JxByQPLSjvQ-JFREjClLkYrs'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            for img in response.json().get('files', []):
                # Store by full filename
                images[img['name']] = img['id']
    except Exception as e:
        st.error(f"Error getting images: {e}")
    return images

# Get all subfolders
with st.spinner("Scanning for subfolders..."):
    subfolders = get_subfolders(MAIN_FOLDER_ID)

if not subfolders:
    st.error("❌ No subfolders found! Make sure main folder is public.")
    st.stop()

st.sidebar.success(f"📁 Found subfolders: {', '.join(subfolders.keys())}")

# Sidebar
with st.sidebar:
    st.header("📍 Select Subfolder")
    selected_subfolder = st.selectbox(
        "Choose folder:",
        options=[''] + sorted(subfolders.keys())
    )
    
    if selected_subfolder:
        # Get images from this subfolder
        folder_id = subfolders[selected_subfolder]
        folder_images = get_images_from_folder(folder_id)
        st.info(f"📸 {len(folder_images)} images in this folder")
        
        # Store in session state
        st.session_state['current_folder'] = selected_subfolder
        st.session_state['current_images'] = folder_images

# Main content
if selected_subfolder and 'current_images' in st.session_state:
    st.subheader(f"📍 Folder: **{selected_subfolder}**")
    
    images = st.session_state['current_images']
    
    if images:
        # Search
        search = st.text_input("🔍 Search images:", placeholder="Type filename...")
        
        # Filter images
        if search:
            filtered = {name: id for name, id in images.items() 
                       if search.lower() in name.lower()}
        else:
            filtered = images
        
        st.write(f"📋 Found {len(filtered)} images")
        
        # Display in grid
        if filtered:
            cols = st.columns(3)
            for idx, (filename, file_id) in enumerate(filtered.items()):
                with cols[idx % 3]:
                    try:
                        # Load image
                        img_url = f"https://drive.google.com/uc?export=view&id={file_id}"
                        response = requests.get(img_url)
                        img = Image.open(BytesIO(response.content))
                        st.image(img, use_container_width=True)
                        
                        # Show filename
                        st.caption(f"📄 {filename}")
                        
                        # Check Excel for matching location
                        # Remove extension for matching
                        location_match = filename.rsplit('.', 1)[0]
                        excel_row = df[df['location'] == location_match]
                        
                        if not excel_row.empty:
                            row = excel_row.iloc[0]
                            with st.expander("📊 Excel Data"):
                                st.write(f"**Record No:** {row.get('no', 'N/A')}")
                                st.write(f"**QR:** {row.get('pallet_qr', 'None')}")
                                if row.get('is_pallet_present') == 'YES':
                                    st.write("**Status:** ✅ Present")
                                else:
                                    st.write("**Status:** ❌ Empty")
                    except Exception as e:
                        st.error(f"Error loading {filename}")
        else:
            st.warning("No images match search")
    else:
        st.warning("No images in this folder")
else:
    st.info("👈 Select a subfolder from the sidebar")
    
    # Show Excel preview
    if data_loaded:
        st.markdown("### 📊 Excel Data Preview")
        st.dataframe(df.head(10))

st.markdown("---")
st.caption("🏭 Warehouse Viewer - Browse subfolders, images match Excel by filename")
