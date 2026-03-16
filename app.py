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

# Your public Drive folder URL
FOLDER_URL = "https://drive.google.com/drive/folders/1yUNa4AkLtY3JMIZbTSajNKGx-aWQdDiK"

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

# SCRAPE folder names directly from the public Drive page
def get_folder_names_from_drive(url):
    """Extract folder names from public Google Drive HTML"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Look for folder names in the HTML
            # This pattern matches the folder links in Drive
            pattern = r'data-target="folder"[^>]*aria-label="([^"]+)"'
            folders = re.findall(pattern, response.text)
            
            # Also try alternative pattern
            if not folders:
                pattern = r'folder-title">([^<]+)<'
                folders = re.findall(pattern, response.text)
            
            # Clean up and return unique folder names
            unique_folders = []
            for f in folders:
                if f and f not in unique_folders and not f.startswith('.'):
                    unique_folders.append(f.strip())
            
            return unique_folders
    except:
        pass
    return []

# Get folders automatically
with st.spinner("Scanning Google Drive for folders..."):
    subfolders = get_folder_names_from_drive(FOLDER_URL)

if not subfolders:
    st.error("""
    ❌ Could not detect folders automatically.
    
    But your Drive URL is: """ + FOLDER_URL + """
    
    Please make sure the folder is public (Anyone with link can view)
    """)
    st.stop()

st.sidebar.success(f"✅ Automatically found {len(subfolders)} folders: {', '.join(subfolders)}")

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
    
    if data_loaded:
        location_data = df[df['location'].str.startswith(selected_folder, na=False)]
        
        if not location_data.empty:
            search_term = st.text_input("🔍 Search:", placeholder="Type location code...")
            
            if search_term:
                filtered_data = location_data[location_data['location'].str.contains(search_term, case=False)]
            else:
                filtered_data = location_data
            
            st.dataframe(filtered_data[['no', 'location', 'pallet_qr', 'is_pallet_present']])
            
            # Link to open folder
            st.markdown(f"🔗 [Open folder in Drive]({FOLDER_URL}/{selected_folder})")
        else:
            st.warning("No records found in Excel for this location")
else:
    st.info("👈 Select a location from the sidebar")
    
    if data_loaded and not df.empty:
        st.markdown("### 📊 Data Overview")
        st.dataframe(df.head(10))
        
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
st.caption("🏭 Warehouse Viewer - Automatically detects folders from Drive")
