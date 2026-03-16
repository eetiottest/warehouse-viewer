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

# Your public Drive folder ID (where images are stored)
FOLDER_ID = "1yUNa4AkLtY3JMIZbTSajNKGx-aWQdDiK"

# Your Excel file
excel_path = "data.xlsx"

# Load Excel data
try:
    df = pd.read_excel(excel_path)
    df.columns = df.columns.str.strip()
    
    # Get ALL locations from Excel
    excel_locations = set(df['location'].unique())
    st.sidebar.success(f"✅ Excel loaded: {len(excel_locations)} locations")
    
except Exception as e:
    st.error(f"❌ Error loading Excel: {e}")
    st.stop()

# Function to get all images from Drive folder
def get_all_images(folder_id):
    """Returns dict of {filename: file_id} from Drive folder"""
    images = {}
    try:
        # Using the public Drive endpoint
        url = "https://www.googleapis.com/drive/v3/files"
        params = {
            'q': f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
            'fields': 'files(id, name)',
            'key': 'AIzaSyB5BzrCpL9JxByQPLSjvQ-JFREjClLkYrs'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            files = response.json().get('files', [])
            for f in files:
                # Remove extension to get location code
                name = f['name']
                location = name.rsplit('.', 1)[0]  # Removes .jpg, .png etc.
                images[location] = {
                    'file_id': f['id'],
                    'filename': name
                }
    except Exception as e:
        st.error(f"Error fetching images: {e}")
    
    return images

# Get all images
with st.spinner("Scanning Drive for images..."):
    drive_images = get_all_images(FOLDER_ID)

st.sidebar.success(f"📸 Found {len(drive_images)} images in Drive")

# Find which locations have images
locations_with_images = set(drive_images.keys())
all_locations = sorted(excel_locations.union(locations_with_images))

# Sidebar
with st.sidebar:
    st.header("📍 Select Location")
    selected = st.selectbox(
        "Choose location:",
        options=[''] + all_locations
    )
    
    if selected:
        in_excel = selected in excel_locations
        in_drive = selected in drive_images
        
        if in_excel:
            excel_data = df[df['location'] == selected].iloc[0]
            st.info(f"📊 Excel: {excel_data.get('no', 'N/A')}")
            st.caption(f"QR: {excel_data.get('pallet_qr', 'None')}")
            if excel_data.get('is_pallet_present') == 'YES':
                st.caption("✅ Pallet present")
            else:
                st.caption("❌ No pallet")
        
        if in_drive:
            st.success(f"📸 Image available")
        elif selected:
            st.warning("📸 No image in Drive")

# Main content
if selected:
    st.subheader(f"📍 Location: **{selected}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Excel Data")
        if selected in excel_locations:
            row = df[df['location'] == selected].iloc[0]
            data = {
                "Record No": row.get('no', 'N/A'),
                "Location": row['location'],
                "Pallet QR": row.get('pallet_qr', 'None'),
                "Pallet Present": row.get('is_pallet_present', 'N/A')
            }
            st.json(data)
        else:
            st.warning("No Excel data for this location")
    
    with col2:
        st.markdown("### 📸 Image")
        if selected in drive_images:
            img_data = drive_images[selected]
            img_url = f"https://drive.google.com/uc?export=view&id={img_data['file_id']}"
            try:
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                st.image(img, use_container_width=True)
                st.caption(f"Filename: {img_data['filename']}")
            except:
                st.error("Could not load image")
        else:
            st.warning("No image in Drive")
    
    # Show both datasets
    st.markdown("---")
    st.markdown("### 🔍 Raw Data")
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Excel Row**")
        if selected in excel_locations:
            st.dataframe(df[df['location'] == selected])
    
    with col4:
        st.markdown("**Drive File**")
        if selected in drive_images:
            st.write(drive_images[selected])

else:
    st.info("👈 Select a location from the sidebar")
    
    # Statistics
    st.markdown("### 📊 Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Excel Locations", len(excel_locations))
    with col2:
        st.metric("Drive Images", len(drive_images))
    with col3:
        both = len(excel_locations.intersection(locations_with_images))
        st.metric("Have Both", both)
    
    # Show samples
    if excel_locations:
        st.markdown("### 📋 Sample Excel Locations")
        st.write(list(excel_locations)[:10])
    
    if locations_with_images:
        st.markdown("### 📋 Sample Drive Images")
        st.write(list(locations_with_images)[:10])

st.markdown("---")
st.caption("🏭 Warehouse Viewer - Matches by filename = location")
