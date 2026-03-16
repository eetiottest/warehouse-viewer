import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os

# Page setup
st.set_page_config(
    page_title="Warehouse Image Viewer",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Warehouse Location Image Viewer")
st.markdown("---")

# ACTUAL FOLDER IDs (now we have them!)
FOLDERS = {
    "renamed": "1pUuGrP1PEhTg03npxykOpaft29t_A79W",
    "errors": "FOLDER_ID_FOR_ERRORS"  # You'll need to get this one too
}

# Function to get images from a folder using its ID
def get_images_from_folder(folder_id):
    """Get all images from a public Drive folder"""
    images = []
    try:
        # Use the public Drive API endpoint
        url = "https://www.googleapis.com/drive/v3/files"
        params = {
            'q': f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
            'fields': 'files(id, name)',
            'key': 'AIzaSyB5BzrCpL9JxByQPLSjvQ-JFREjClLkYrs'  # Public test key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            files = response.json().get('files', [])
            for f in files:
                images.append({
                    'name': f['name'],
                    'id': f['id'],
                    'location': f['name'].rsplit('.', 1)[0]  # Remove extension
                })
    except Exception as e:
        st.error(f"Error loading images: {e}")
    
    return images

# Load Excel data (from GitHub)
excel_path = "data.xlsx"
try:
    df = pd.read_excel(excel_path)
    df.columns = df.columns.str.strip()
    if 'pallet_qr' in df.columns:
        df['pallet_qr'] = df['pallet_qr'].astype(str)
    data_loaded = True
    st.sidebar.success(f"✅ Loaded {len(df)} Excel records")
except Exception as e:
    df = pd.DataFrame()
    data_loaded = False
    st.sidebar.error(f"❌ Excel error: {e}")

# Sidebar
with st.sidebar:
    st.header("📍 Select Folder")
    selected = st.selectbox("Choose:", options=[''] + list(FOLDERS.keys()))
    
    if selected:
        folder_id = FOLDERS[selected]
        images = get_images_from_folder(folder_id)
        st.info(f"📸 Found {len(images)} images in {selected}")
        
        # Store in session state
        st.session_state['current_images'] = images
        st.session_state['current_folder'] = selected

# Main content
if selected and 'current_images' in st.session_state:
    st.subheader(f"📍 Folder: **{selected}**")
    
    images = st.session_state['current_images']
    
    if images:
        # Search bar
        search = st.text_input("🔍 Search:", placeholder="Type filename or location...")
        
        # Filter images
        if search:
            filtered = [img for img in images if search.lower() in img['name'].lower()]
        else:
            filtered = images
        
        st.write(f"📋 Found {len(filtered)} images")
        
        # Display in grid
        cols = st.columns(3)
        
        for idx, img in enumerate(filtered):
            with cols[idx % 3]:
                try:
                    # Load image
                    img_url = f"https://drive.google.com/uc?export=view&id={img['id']}"
                    response = requests.get(img_url)
                    picture = Image.open(BytesIO(response.content))
                    st.image(picture, use_container_width=True)
                    
                    # Show filename
                    st.caption(f"📄 {img['name']}")
                    
                    # Check Excel for matching data
                    if data_loaded:
                        match = df[df['location'] == img['location']]
                        if not match.empty:
                            row = match.iloc[0]
                            with st.expander("📊 Details"):
                                st.write(f"**Record No:** {row.get('no', 'N/A')}")
                                st.write(f"**QR:** {row.get('pallet_qr', 'None')}")
                                if row.get('is_pallet_present') == 'YES':
                                    st.write("**Status:** ✅ Present")
                                else:
                                    st.write("**Status:** ❌ Empty")
                except Exception as e:
                    st.error(f"Error loading image")
    else:
        st.warning("No images in this folder")
else:
    st.info("👈 Select a folder from the sidebar")
    
    if data_loaded:
        st.markdown("### 📊 Excel Data Preview")
        st.dataframe(df.head(10))

st.markdown("---")
st.caption("🏭 Warehouse Viewer")
