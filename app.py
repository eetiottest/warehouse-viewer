import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide")

# 2. Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 20px;
        color: #1f1f1f;
    }
    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    .data-table th {
        background-color: #f0f2f6;
        padding: 12px;
        text-align: left;
        font-weight: 600;
        border: 1px solid #e0e0e0;
        cursor: pointer;
    }
    .data-table td {
        padding: 10px;
        border: 1px solid #e0e0e0;
        cursor: pointer;
    }
    .data-table tr:hover {
        background-color: #f5f5f5;
    }
    .selected-row {
        background-color: #e3f2fd !important;
    }
    .detail-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
    }
    .detail-label {
        font-weight: 600;
        color: #495057;
        margin-bottom: 5px;
    }
    .detail-value {
        color: #212529;
        margin-bottom: 15px;
        word-wrap: break-word;
    }
    .divider {
        border-top: 2px solid #e0e0e0;
        margin: 20px 0;
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

# 4. Filter display columns for the main table
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')
columns = display_df.columns.tolist()

st.markdown('<div class="main-header">📦 Inventory Data</div>', unsafe_allow_html=True)

# 5. Initialize session state for selected row
if 'selected_row_id' not in st.session_state:
    st.session_state.selected_row_id = None

# 6. Build HTML Table with clickable rows
def build_html_table(df, columns, selected_id):
    html = '<table class="data-table">'
    
    # Header
    html += '<thead><tr>'
    for col in columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    
    # Rows
    for idx, row in df.iterrows():
        row_class = 'selected-row' if idx == selected_id else ''
        html += f'<tr class="{row_class}" onclick="selectRow({idx})">'
        for col in columns:
            html += f'<td>{row[col]}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    return html

# JavaScript for row selection
st.markdown("""
    <script>
    function selectRow(rowId) {
        const event = new CustomEvent('row_selected', {detail: {rowId: rowId}});
        window.dispatchEvent(event);
    }
    </script>
""", unsafe_allow_html=True)

# Display HTML table
html_table = build_html_table(display_df, columns, st.session_state.selected_row_id)
st.markdown(html_table, unsafe_allow_html=True)

# 7. Handle row selection via custom component
if st.button("Load Selected Row (Demo)", key="load_btn"):
    # In a real implementation, you'd want to use st.components.v1.html with callbacks
    # For simplicity, let's use a selectbox alternative
    pass

# Alternative: Use selectbox for row selection (more reliable with Streamlit)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Create a selectbox for row selection
row_options = {i: f"Row {i+1} - {display_df.iloc[i]['Location'] if 'Location' in display_df.columns else 'Item'}" 
               for i in range(len(display_df))}
selected_idx = st.selectbox(
    "Select an item to view details:",
    options=list(row_options.keys()),
    format_func=lambda x: row_options[x],
    key="row_selector"
)

# 8. Detail View Layout
if selected_idx is not None:
    row = df.iloc[selected_idx]
    
    st.markdown('<div class="detail-card">', unsafe_allow_html=True)
    
    # Title
    if 'Location' in row:
        st.markdown(f'### 📍 {row["Location"]}')
    else:
        st.markdown('### Item Details')
    
    # Two column layout for details
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display image if available
        if 'Image Link' in row and pd.notna(row['Image Link']):
            st.image(row['Image Link'], use_column_width=True)
        else:
            st.info("No image available")
    
    with col2:
        # Display fields in an organized grid
        for col in display_df.columns:
            if col != 'Location':  # Location already shown in title
                st.markdown(f'**{col}:** {row[col]}')
    
    st.markdown('</div>', unsafe_allow_html=True)

# Optional: Add download button for data
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
if st.button("📥 Export to CSV"):
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="inventory_data.csv",
        mime="text/csv",
    )
