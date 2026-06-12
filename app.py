import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }
    
    /* Detail panel styling */
    .detail-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .detail-title {
        font-size: 20px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .detail-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 12px;
        margin-top: 16px;
    }
    
    .detail-card {
        background: #f9fafb;
        border-radius: 8px;
        padding: 12px 16px;
        border: 1px solid #e5e7eb;
    }
    
    .detail-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #6b7280;
        margin-bottom: 6px;
    }
    
    .detail-value {
        font-size: 14px;
        font-weight: 500;
        color: #111827;
        word-wrap: break-word;
    }
    
    .status-match {
        color: #059669;
        font-weight: 600;
    }
    
    .status-mismatch {
        color: #dc2626;
        font-weight: 600;
    }
    
    .status-na {
        color: #6b7280;
        font-weight: 500;
    }
    
    .image-container {
        background: #f9fafb;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    
    /* Search and filter styling */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #d1d5db;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59,130,246,0.1);
    }
    
    .stSelectbox > div > div {
        border-radius: 6px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 6px;
        background: #ffffff;
        border: 1px solid #d1d5db;
        color: #374151;
    }
    
    .stButton > button:hover {
        background: #f9fafb;
        border-color: #9ca3af;
    }
</style>
""", unsafe_allow_html=True)

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
st.markdown("### Inventory Management System")

col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("Search", placeholder="Type to filter by any field...")
with col2:
    status_options = ["All", "Match", "Mismatch", "NA"]
    status_filter = st.selectbox("Status Filter", options=status_options)

# Apply filters
filtered_df = display_df.copy()

if search:
    filtered_df = filtered_df[filtered_df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)]

if status_filter != "All":
    if 'Status' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Status'].str.upper() == status_filter.upper()]

# Display count
st.caption(f"Showing {len(filtered_df)} items")

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
    
    # HTML Detail View
    st.markdown('<div class="detail-container">', unsafe_allow_html=True)
    
    # Title with location
    location = row.get('Location', 'Item')
    st.markdown(f'<div class="detail-title">📦 {location}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        image_url = row.get('Image Link', '')
        if image_url and image_url.strip():
            if 'id=' in image_url:
                file_id = image_url.split('id=')[1].split('&')[0]
            elif '/d/' in image_url:
                file_id = image_url.split('/d/')[1].split('/')[0]
            else:
                file_id = None
            
            if file_id:
                direct_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"
                st.image(direct_url, use_container_width=True)
            else:
                st.image(image_url, use_container_width=True)
        else:
            st.info("No image available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Create grid of details
        detail_html = '<div class="detail-grid">'
        for col in display_df.columns:
            value = row[col] if pd.notna(row[col]) and row[col] != '' else ""
            
            # Add special styling for status
            if col == 'Status' and value:
                if value.upper() == 'MATCH':
                    value_display = f'<span class="status-match">✅ {value}</span>'
                elif value.upper() == 'MISMATCH':
                    value_display = f'<span class="status-mismatch">❌ {value}</span>'
                elif value.upper() == 'NA':
                    value_display = f'<span class="status-na">⚠️ {value}</span>'
                else:
                    value_display = value
            else:
                value_display = value if value else "—"
            
            detail_html += f'''
                <div class="detail-card">
                    <div class="detail-label">{col}</div>
                    <div class="detail-value">{value_display}</div>
                </div>
            '''
        detail_html += '</div>'
        st.markdown(detail_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
