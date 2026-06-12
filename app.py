import streamlit as st
import pandas as pd
import math

# 1. Page Configuration
st.set_page_config(
    layout="wide",
    page_title="Inventory Management System",
    page_icon="📊"
)

# 2. Professional AppSheet-like CSS
st.markdown("""
    <style>
    /* Main container styling */
    .stApp {
        background-color: #f5f7fa;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 600;
    }
    
    .main-header p {
        margin: 8px 0 0 0;
        opacity: 0.9;
        font-size: 14px;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        transition: transform 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stat-label {
        font-size: 12px;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    .stat-value {
        font-size: 28px;
        font-weight: 700;
        color: #2c3e50;
        margin-top: 8px;
    }
    
    /* Table styling */
    .data-table-wrapper {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
    }
    
    .data-table th {
        background: #f8f9fc;
        color: #2c3e50;
        padding: 14px 12px;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid #e9ecef;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .data-table td {
        padding: 12px;
        border-bottom: 1px solid #e9ecef;
        color: #495057;
    }
    
    .data-table tbody tr:hover {
        background-color: #f8f9fc;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .data-table tbody tr.selected-row {
        background-color: #e7f1ff;
        border-left: 3px solid #667eea;
    }
    
    /* Pagination styling */
    .pagination-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        background: white;
        border-radius: 8px;
        margin-top: 1rem;
    }
    
    .pagination-buttons {
        display: flex;
        gap: 8px;
        align-items: center;
    }
    
    .page-btn {
        background: white;
        border: 1px solid #dee2e6;
        padding: 6px 12px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 13px;
        transition: all 0.2s;
        color: #495057;
    }
    
    .page-btn:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    
    .page-btn.active {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    
    .page-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    .page-info {
        color: #6c757d;
        font-size: 13px;
    }
    
    /* Detail panel styling */
    .detail-panel {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #667eea;
    }
    
    .detail-header {
        font-size: 20px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e9ecef;
    }
    
    .detail-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1rem;
    }
    
    .detail-item {
        padding: 0.75rem;
        background: #f8f9fc;
        border-radius: 8px;
    }
    
    .detail-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        color: #6c757d;
        margin-bottom: 0.5rem;
    }
    
    .detail-value {
        font-size: 14px;
        color: #2c3e50;
        font-weight: 500;
        word-wrap: break-word;
    }
    
    /* Search box styling */
    .search-box {
        margin-bottom: 1rem;
    }
    
    .search-box input {
        width: 100%;
        padding: 10px 12px;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        font-size: 14px;
        transition: all 0.2s;
    }
    
    .search-box input:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .badge-success {
        background: #d4edda;
        color: #155724;
    }
    
    .badge-warning {
        background: #fff3cd;
        color: #856404;
    }
    
    /* Image styling */
    .detail-image {
        max-width: 100%;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url, dtype=str)
    df.columns = df.columns.str.strip()
    return df

df = load_data()
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

# 4. Initialize session state
if 'selected_row_id' not in st.session_state:
    st.session_state.selected_row_id = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""

# 5. Header Section
st.markdown("""
    <div class="main-header">
        <h1>📦 Inventory Management System</h1>
        <p>Real-time inventory tracking and management</p>
    </div>
""", unsafe_allow_html=True)

# 6. Stats Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Total Items</div>
            <div class="stat-value">{len(df)}</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Categories</div>
            <div class="stat-value">{df['Category'].nunique() if 'Category' in df.columns else 'N/A'}</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Locations</div>
            <div class="stat-value">{df['Location'].nunique() if 'Location' in df.columns else 'N/A'}</div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Last Updated</div>
            <div class="stat-value" style="font-size: 14px;">Just Now</div>
        </div>
    """, unsafe_allow_html=True)

# 7. Search and Filter Section
col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("🔍 Search inventory...", key="search_input", placeholder="Search by any field...")
    if search:
        st.session_state.search_term = search
        # Apply search filter
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
        filtered_df = display_df[mask].copy()
        st.session_state.current_page = 1  # Reset to first page on search
    else:
        st.session_state.search_term = ""
        filtered_df = display_df.copy()

# 8. Pagination Settings
ROWS_PER_PAGE = 50
total_rows = len(filtered_df)
total_pages = max(1, math.ceil(total_rows / ROWS_PER_PAGE))

# Ensure current page is valid
if st.session_state.current_page > total_pages:
    st.session_state.current_page = total_pages

# Calculate slice
start_idx = (st.session_state.current_page - 1) * ROWS_PER_PAGE
end_idx = min(start_idx + ROWS_PER_PAGE, total_rows)
page_df = filtered_df.iloc[start_idx:end_idx]

# 9. Display Table
st.markdown('<div class="data-table-wrapper">', unsafe_allow_html=True)

# Build HTML table
html_table = '<table class="data-table">'
html_table += '<thead><tr>'
for col in page_df.columns:
    html_table += f'<th>{col}</th>'
html_table += '</tr></thead><tbody>'

for idx, (orig_idx, row) in enumerate(page_df.iterrows()):
    row_class = 'selected-row' if orig_idx == st.session_state.selected_row_id else ''
    html_table += f'<tr class="{row_class}" onclick="selectRow({orig_idx})" style="cursor: pointer;">'
    for col in page_df.columns:
        html_table += f'<td>{row[col]}</td>'
    html_table += '</tr>'

html_table += '</tbody></table>'
st.markdown(html_table, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 10. Pagination Controls
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown(f'<div class="page-info">Showing {start_idx + 1} to {min(end_idx, total_rows)} of {total_rows} items</div>', unsafe_allow_html=True)

with col2:
    # Pagination buttons
    cols = st.columns([1, 1, 2, 1, 1])
    with cols[0]:
        if st.button("◀◀ First", disabled=(st.session_state.current_page == 1), key="first_page"):
            st.session_state.current_page = 1
            st.rerun()
    with cols[1]:
        if st.button("◀ Previous", disabled=(st.session_state.current_page == 1), key="prev_page"):
            st.session_state.current_page -= 1
            st.rerun()
    
    with cols[2]:
        # Page selector
        page_options = list(range(1, min(total_pages + 1, 11)))  # Show up to 10 pages
        selected_page = st.selectbox(
            "Page",
            options=page_options,
            index=st.session_state.current_page - 1 if st.session_state.current_page <= len(page_options) else 0,
            key="page_select",
            label_visibility="collapsed"
        )
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()
    
    with cols[3]:
        if st.button("Next ▶", disabled=(st.session_state.current_page == total_pages), key="next_page"):
            st.session_state.current_page += 1
            st.rerun()
    with cols[4]:
        if st.button("Last ▶▶", disabled=(st.session_state.current_page == total_pages), key="last_page"):
            st.session_state.current_page = total_pages
            st.rerun()

# 11. Detail View Panel
if st.session_state.selected_row_id is not None:
    row = df.iloc[st.session_state.selected_row_id]
    
    st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="detail-header">📋 Item Details</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if 'Image Link' in row and pd.notna(row['Image Link']):
            st.image(row['Image Link'], use_column_width=True)
        else:
            st.info("No image available")
    
    with col2:
        # Create a grid for details
        detail_html = '<div class="detail-grid">'
        for col in display_df.columns:
            detail_html += f'''
                <div class="detail-item">
                    <div class="detail-label">{col}</div>
                    <div class="detail-value">{row[col]}</div>
                </div>
            '''
        detail_html += '</div>'
        st.markdown(detail_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 12. JavaScript for row selection
st.markdown("""
    <script>
    function selectRow(rowId) {
        // Store selected row in Streamlit session state via rerun
        const input = document.createElement('input');
        input.type = 'hidden';
        input.id = 'selected_row_' + rowId;
        document.body.appendChild(input);
        
        // Trigger Streamlit rerun with query parameter
        const url = new URL(window.location.href);
        url.searchParams.set('selected_row', rowId);
        window.location.href = url;
    }
    
    // Check URL for selected row on load
    const urlParams = new URLSearchParams(window.location.search);
    const selectedRow = urlParams.get('selected_row');
    if (selectedRow) {
        // Remove from URL without reloading
        const newUrl = window.location.href.split('?')[0];
        window.history.pushState({}, '', newUrl);
    }
    </script>
""", unsafe_allow_html=True)

# Handle row selection from URL parameters (simpler approach)
import streamlit as st
query_params = st.query_params
if 'selected_row' in query_params:
    try:
        selected = int(query_params['selected_row'])
        if 0 <= selected < len(df):
            st.session_state.selected_row_id = selected
        # Clear the parameter
        st.query_params.clear()
    except:
        pass

# Alternative row selection using buttons (more reliable)
# Add a clear selection button
if st.session_state.selected_row_id is not None:
    if st.button("Clear Selection", key="clear_selection"):
        st.session_state.selected_row_id = None
        st.rerun()
