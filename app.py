import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Custom CSS with !important to override Streamlit defaults
st.markdown("""
<style>
    /* Force background colors */
    .stApp {
        background-color: #f3f4f6 !important;
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 8px !important;
        overflow: hidden !important;
        border: 1px solid #d1d5db !important;
    }
    
    /* Detail panel styling */
    .detail-container {
        background: #ffffff !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-top: 20px !important;
        border: 1px solid #d1d5db !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    .detail-title {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #1f2937 !important;
        margin-bottom: 20px !important;
        padding-bottom: 12px !important;
        border-bottom: 2px solid #e5e7eb !important;
    }
    
    .detail-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)) !important;
        gap: 12px !important;
        margin-top: 16px !important;
    }
    
    .detail-card {
        background: #fefce8 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        border: 1px solid #fde047 !important;
        transition: all 0.2s ease !important;
    }
    
    .detail-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        background: #fef08a !important;
    }
    
    .detail-label {
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #854d0e !important;
        margin-bottom: 6px !important;
    }
    
    .detail-value {
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #1f2937 !important;
        word-wrap: break-word !important;
    }
    
    .status-match {
        color: #16a34a !important;
        font-weight: 700 !important;
        background: #dcfce7 !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        display: inline-block !important;
    }
    
    .status-mismatch {
        color: #dc2626 !important;
        font-weight: 700 !important;
        background: #fee2e2 !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        display: inline-block !important;
    }
    
    .status-na {
        color: #6b7280 !important;
        font-weight: 600 !important;
        background: #f3f4f6 !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        display: inline-block !important;
    }
    
    .image-container {
        background: #fefce8 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        text-align: center !important;
        border: 1px solid #fde047 !important;
    }
    
    /* Search and filter styling */
    .stTextInput > div > div > input {
        border-radius: 6px !important;
        border: 1px solid #eab308 !important;
        background: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ca8a04 !important;
        box-shadow: 0 0 0 2px rgba(234,179,8,0.1) !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 6px !important;
        border-color: #eab308 !important;
    }
    
    /* Table header styling */
    thead th {
        background: #fefce8 !important;
        color: #854d0e !important;
        font-weight: 600 !important;
    }
    
    /* Row hover effect */
    tbody tr:hover {
        background: #fef08a !important;
        cursor: pointer !important;
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
st.markdown("### 📦 Inventory Management System")

col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("🔍 Search", placeholder="Type to filter by any field...")
with col2:
    status_options = ["All", "Match", "Mismatch", "NA"]
    status_filter = st.selectbox("🏷️ Status Filter", options=status_options)

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
            st.info("📷 No image available")
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
