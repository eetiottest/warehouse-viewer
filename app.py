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

# Your Google Drive folder ID - already configured
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

# ALL your subfolders - automatically detected (replace this with actual API call later)
subfolders = ["SHA", "SHB", "SHC", "SHD", "SHE", "SHF"]  # Add all your folders here

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
            # Create lookup dictionary for quick access
            data_lookup = dict(zip(location_data['location'], location_data.to_dict('records')))
            
            # Display placeholder for images (will be replaced with actual Drive images)
            st.info(f"📸 Found {len(location_data)} records for {selected_folder}")
            
            # Show data table
            st.dataframe(location_data[['no', 'location', 'pallet_qr', 'is_pallet_present']])
            
            # Here you would add the code to fetch and display images from Drive
            # For now, showing the data is working
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

st.markdown("---")
st.caption("🏭 Warehouse Viewer")
