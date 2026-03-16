import streamlit as st
import os
from PIL import Image
import glob
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Warehouse Image Viewer",
    page_icon="🏭",
    layout="wide"
)

# Title
st.title("🏭 Warehouse Location Image Viewer")
st.markdown("---")

# For Streamlit Cloud, files are in the same directory
base_path = ""  # Current directory
excel_path = "data.xlsx"  # Your Excel file

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

# Get all location folders (SHA, SHB, SHC, etc.)
if os.path.exists(base_path):
    location_folders = [f for f in os.listdir(base_path) 
                       if os.path.isdir(os.path.join(base_path, f))]
    location_folders = [f for f in location_folders if f not in ['.git', '.streamlit']]
    location_folders.sort()
else:
    location_folders = []
    st.error(f"❌ Folder not found")

# Sidebar for selection
with st.sidebar:
    st.header("📍 Select Location")
    selected_folder = st.selectbox(
        "Choose location:",
        options=[''] + location_folders
    )
    
    if selected_folder:
        folder_path = os.path.join(base_path, selected_folder)
        
        # Find all images in this folder
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.JPG']:
            image_files.extend(glob.glob(os.path.join(folder_path, ext)))
        
        image_files.sort()
        st.info(f"📸 Found **{len(image_files)}** images in {selected_folder}")

# Main content
if selected_folder:
    st.subheader(f"📍 Location: **{selected_folder}**")
    
    folder_path = os.path.join(base_path, selected_folder)
    
    # Find all images again
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.JPG']:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))
    image_files.sort()
    
    if image_files:
        # Search bar
        search_term = st.text_input("🔍 Search images:", placeholder="Type location code...")
        
        # Filter images
        if search_term:
            filtered_images = []
            for img_path in image_files:
                if search_term.lower() in os.path.basename(img_path).lower():
                    filtered_images.append(img_path)
            display_images = filtered_images
            st.write(f"📋 Found **{len(display_images)}** images matching '{search_term}'")
        else:
            display_images = image_files
            st.write(f"📋 Showing all **{len(display_images)}** images")
        
        # Display in 3 columns
        cols = st.columns(3)
        
        for idx, img_path in enumerate(display_images):
            with cols[idx % 3]:
                try:
                    img = Image.open(img_path)
                    st.image(img, use_container_width=True)
                    
                    filename = os.path.basename(img_path)
                    
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
                    st.error(f"Error: {e}")
    else:
        st.warning("No images found")
else:
    st.info("👈 Select a location from the sidebar")
    
    if data_loaded:
        st.markdown("### 📊 Data Preview:")
        st.dataframe(df.head(10))

st.markdown("---")
st.caption("🏭 Warehouse Viewer")
