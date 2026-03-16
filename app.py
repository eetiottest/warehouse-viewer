import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import xml.etree.ElementTree as ET

# Page setup
st.set_page_config(page_title="Warehouse Viewer", layout="wide")
st.title("🏭 Warehouse Location Viewer")
st.markdown("---")

# Your public Drive folder ID
FOLDER_ID = "1yUNa4AkLtY3JMIZbTSajNKGx-aWQdDiK"
FEED_URL = f"https://drive.google.com/embeddedfolderview?id={FOLDER_ID}#list"

# Load Excel data
df = pd.read_excel("data.xlsx")
df.columns = df.columns.str.strip()

# --- AUTOMATIC FOLDER DETECTION (USING THE SAME FEED THAT SHOWS IMAGES) ---
@st.cache_data
def get_folders_from_drive_feed(url):
    """Parses the public Drive XML feed to get folder names."""
    folders = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # The feed is XML, parse it
            root = ET.fromstring(response.text)
            # Find all entries that are folders (mime type)
            for entry in root.findall('.//entry'):
                mime_type_elem = entry.find('.//mimeType')
                if mime_type_elem is not None and 'folder' in mime_type_elem.text:
                    title_elem = entry.find('.//title')
                    if title_elem is not None and title_elem.text:
                        folders.append(title_elem.text)
    except Exception as e:
        st.error(f"Error reading feed: {e}")
    return folders

with st.spinner("Detecting folders from Drive..."):
    subfolders = get_folders_from_drive_feed(FEED_URL)

if not subfolders:
    st.error(f"❌ Could not detect folders. Please ensure the folder is public: [Open Drive Folder](https://drive.google.com/drive/folders/{FOLDER_ID})")
    st.stop()
else:
    st.sidebar.success(f"✅ Auto-detected folders: {', '.join(subfolders)}")

# --- SIDEBAR (USING AUTO-DETECTED FOLDERS) ---
with st.sidebar:
    st.header("📍 Select Location")
    selected_folder = st.selectbox("Choose location:", options=[''] + sorted(subfolders))

    if selected_folder:
        folder_records = df[df['location'].str.startswith(selected_folder, na=False)]
        st.info(f"📊 {len(folder_records)} Excel records")

# --- MAIN CONTENT ---
if selected_folder:
    st.subheader(f"📍 **{selected_folder}**")
    folder_data = df[df['location'].str.startswith(selected_folder, na=False)]
    st.dataframe(folder_data[['no', 'location', 'pallet_qr', 'is_pallet_present']])
    st.markdown(f"🔗 [Open Folder in Drive](https://drive.google.com/drive/folders/{FOLDER_ID}/{selected_folder})")
else:
    st.info("👈 Select a location from the sidebar")
    st.markdown("### 📊 Data Overview")
    st.dataframe(df.head(10))

st.markdown("---")
st.caption("✅ Folders detected automatically from the public Drive feed.")
