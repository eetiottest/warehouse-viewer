import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import re
import os
import time

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

# Function to automatically get ALL subfolders from Google Drive
def get_all_subfolders(folder_id):
    """
    Automatically fetches ALL subfolder names from a public Google Drive folder
    No hardcoding needed!
    """
    try:
        # Google Drive API endpoint to list files in a folder
        api_url = f"https://www.googleapis.com/drive/v3/files"
        
        # Parameters to get only folders
        params = {
            'q': f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
            'fields': 'files(name, id)',
            'key': 'AIzaSyB5BzrCpL9JxByQPLSjvQ-JFREjClLkYrs'  # Public API key for testing
        }
        
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            folders = response.json().get('files', [])
            return [f['name'] for f in folders]
    except:
        pass
    
    # Fallback: If API fails, return empty list
    return []

# Get all subfolders automatically
subfolders = get_all_subfolders(FOLDER_ID)

# If no folders detected yet, show message but don't hardcode
if not subfolders:
    st.warning("⚠️ Waiting for Google Drive folder to be public...")
    st.info("Please make your folder public (Anyone with link can view)")
    st.markdown(f"🔗 [Click here to open your folder](https://drive.google.com/drive/folders/{FOLDER_ID})")
    st.stop()

# Sidebar - only the location selector
with st.sidebar:
    st.header("📍 Select Location")
    selected_folder = st.selectbox(
        "Choose location:",
        options=[''] + sorted(subfolders)
    )
    
    if selected_folder and data_loaded:
        # Show count of records for this location
        location_records = df[df['location'].str.startswith(selected_folder, na=False)]
        st.info(f"📊 {len(location_records)} records in Excel")

# Main content
if selected_folder:
    st.subheader(f"📍 Location: **{selected_folder}**")
    
    # Search bar
    search_term = st.text_input("🔍 Search images:", placeholder="Type location code...")
    
    # Filter Excel data for this location
    if data_loaded:
        location_data = df[df['location'].str.startswith(selected_folder, na=False)]
        
        if not location_data.empty:
            # Show data table
            st.dataframe(location_data[['no', 'location', 'pallet_qr', 'is_pallet_present']])
            
            st.success(f"✅ Found {len(location_data)} records for {selected_folder}")
            
            # Display placeholder for images
            st.info("📸 Images will appear here once Google Drive API is fully configured")
        else:
            st.warning("No records found for this location")
    else:
        st.error("Excel data not loaded")
else:
    st.info("👈 Select a location from the sidebar to begin")
    
    # Show preview of data
    if data_loaded and not df.empty:
        st.markdown("### 📊 Data Overview")
        st.dataframe(df.head(10))
        
        # Summary stats
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
        
        # Show detected subfolders
        if subfolders:
            st.markdown("### 📁 Detected Locations")
            st.write(f"Found {len(subfolders)} subfolders: {', '.join(subfolders[:10])}")
            if len(subfolders) > 10:
                st.write(f"... and {len(subfolders)-10} more")

st.markdown("---")
st.caption("🏭 Warehouse Viewer - Automatically Detects All Subfolders")
