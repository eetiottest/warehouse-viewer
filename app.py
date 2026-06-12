import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Load data - explicitly keep 'NA' as string
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url, dtype=str, keep_default_na=False)
    df.columns = df.columns.str.strip()
    return df

df = load_data()
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

# Search and Filter Section
col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("🔍 Search", placeholder="Type to filter...")
with col2:
    # Status filter dropdown
    status_options = ["All", "Match", "Mismatch", "NA"]
    status_filter = st.selectbox("Status", options=status_options)

# Apply filters
filtered_df = display_df.copy()

# Apply search filter (case-insensitive)
if search:
    filtered_df = filtered_df[filtered_df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)]

# Apply status filter
if status_filter != "All":
    if 'Status' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Status'].str.upper() == status_filter.upper()]

# Display table
event = st.dataframe(
    filtered_df,
    use_container_width=True,
    selection_mode="single-row",
    on_select="rerun",
    hide_index=True
)

# Show details when row selected
if event.selection.get("rows"):
    selected_index = event.selection["rows"][0]
    row = df.iloc[selected_index]
    
    with st.expander("📋 Item Details", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            # Get the Google Drive image link
            image_url = row.get('Image Link', '')
            if image_url and image_url.strip():
                # Extract file ID from Google Drive URL
                if 'id=' in image_url:
                    file_id = image_url.split('id=')[1].split('&')[0]
                elif '/d/' in image_url:
                    file_id = image_url.split('/d/')[1].split('/')[0]
                else:
                    file_id = None
                
                if file_id:
                    # Use Google's direct image serving URL
                    direct_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"
                    st.image(direct_url, width=500)
                else:
                    st.image(image_url, width=500)
            else:
                st.info("No image available")
        
        with col2:
            for col in display_df.columns:
                value = row[col] if pd.notna(row[col]) and row[col] != '' else ""
                # Highlight status field
                if col == 'Status' and value:
                    if value.upper() == 'MATCH':
                        st.markdown(f"**{col}:** ✅ Match")
                    elif value.upper() == 'MISMATCH':
                        st.markdown(f"**{col}:** ❌ Mismatch")
                    elif value.upper() == 'NA':
                        st.markdown(f"**{col}:** NA")
                    else:
                        st.markdown(f"**{col}:** {value}")
                else:
                    st.markdown(f"**{col}:** {value}")
