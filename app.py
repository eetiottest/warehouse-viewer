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
    
    /* Header styling - minimal */
    .main-header {
        margin-bottom: 1.5rem;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 24px;
        font-weight: 600;
        color: #2c3e50;
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
        font-size: 18px;
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
    
    /* Image styling */
    .detail-image {
        max-width: 100%;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Clear button styling */
    .clear-btn {
        background: white;
        border: 1px solid #dee2e6;
        padding: 6px 12px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 13px;
        transition: all 0.2s;
    }
    
    .clear-btn:hover {
        background: #f8f9fc;
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

# 5. Header Section - Minimal
st.markdown("""
    <div class="main-header">
        <h1>📦 Inventory Data</h1>
    </div>
""", unsafe_allow_html=True)

# 6. Search Section
search = st.text_input("🔍 Search inventory...", key="search_input", placeholder="Search by any field...")
if search:
    st.session_state.search_term = search
    mask = display_df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
    filtered_df = display_df[mask].copy()
    st.session_state.current_page = 1
else:
    st.session_state.search_term = ""
    filtered_df = display_df.copy()

# 7. Pagination Settings
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

# 8. Display Table
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
        # Truncate long text for better display
        cell_value = str(row[col])
        if len(cell_value) > 50:
            cell_value = cell_value[:47] + "..."
        html_table += f'<td>{cell_value}</td>'
    html_table += '</tr>'

html_table += '</tbody></table>'
st.markdown(html_table, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 9. Pagination Controls
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if total_rows > 0:
        st.markdown(f'<div class="page-info">Showing {start_idx + 1} to {min(end_idx, total_rows)} of {total_rows} items</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="page-info">No items found</div>', unsafe_allow_html=True)

with col2:
    if total_pages > 1:
        # Pagination buttons
        button_cols = st.columns([1, 1, 2, 1, 1])
        with button_cols[0]:
            if st.button("◀◀", disabled=(st.session_state.current_page == 1), key="first_page", help="First page"):
                st.session_state.current_page = 1
                st.rerun()
        with button_cols[1]:
            if st.button("◀", disabled=(st.session_state.current_page == 1), key="prev_page", help="Previous page"):
                st.session_state.current_page -= 1
                st.rerun()
        
        with button_cols[2]:
            # Page selector
            page_options = list(range(1, min(total_pages + 1, 11)))
            selected_page = st.selectbox(
                "Page",
                options=page_options,
                index=min(st.session_state.current_page - 1, len(page_options) - 1),
                key="page_select",
                label_visibility="collapsed"
            )
            if selected_page != st.session_state.current_page:
                st.session_state.current_page = selected_page
                st.rerun()
        
        with button_cols[3]:
            if st.button("▶", disabled=(st.session_state.current_page == total_pages), key="next_page", help="Next page"):
                st.session_state.current_page += 1
                st.rerun()
        with button_cols[4]:
            if st.button("▶▶", disabled=(st.session_state.current_page == total_pages), key="last_page", help="Last page"):
                st.session_state.current_page = total_pages
                st.rerun()

with col3:
    if st.session_state.selected_row_id is not None:
        if st.button("✕ Clear Selection", key="clear_selection"):
            st.session_state.selected_row_id = None
            st.rerun()

# 10. Detail View Panel
if st.session_state.selected_row_id is not None and st.session_state.selected_row_id < len(df):
    row = df.iloc[st.session_state.selected_row_id]
    
    st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="detail-header">📋 Item Details</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if 'Image Link' in row and pd.notna(row['Image Link']) and row['Image Link']:
            st.image(row['Image Link'], use_column_width=True)
        elif 'Image' in row and pd.notna(row['Image']) and row['Image']:
            st.image(row['Image'], use_column_width=True)
        else:
            st.info("No image available")
    
    with col2:
        # Create a grid for details
        detail_html = '<div class="detail-grid">'
        for col in display_df.columns:
            value = row[col] if pd.notna(row[col]) else "—"
            detail_html += f'''
                <div class="detail-item">
                    <div class="detail-label">{col}</div>
                    <div class="detail-value">{value}</div>
                </div>
            '''
        detail_html += '</div>'
        st.markdown(detail_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 11. JavaScript for row selection
st.markdown("""
    <script>
    function selectRow(rowId) {
        const url = new URL(window.location.href);
        url.searchParams.set('selected_row', rowId);
        window.location.href = url;
    }
    </script>
""", unsafe_allow_html=True)

# Handle row selection from URL parameters
query_params = st.query_params
if 'selected_row' in query_params:
    try:
        selected = int(query_params['selected_row'])
        if 0 <= selected < len(df):
            st.session_state.selected_row_id = selected
        # Clear the parameter
        st.query_params.clear()
        st.rerun()
    except:
        pass
