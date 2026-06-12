import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Load data
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url, dtype=str).fillna('')
    df.columns = df.columns.str.strip()
    return df

df = load_data()
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

# Pagination
ROWS_PER_PAGE = 50
total_pages = max(1, (len(display_df) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE)

if 'page' not in st.session_state:
    st.session_state.page = 1

# Search
search = st.text_input("🔍 Search", placeholder="Type to filter...")
filtered_df = display_df[display_df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)] if search else display_df

# Page controls
col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("◀ Previous", disabled=st.session_state.page==1):
        st.session_state.page -= 1
        st.rerun()
with col2:
    total_pages_filtered = max(1, (len(filtered_df) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE)
    st.write(f"Page {st.session_state.page} of {total_pages_filtered}")
with col3:
    if st.button("Next ▶", disabled=st.session_state.page==total_pages_filtered):
        st.session_state.page += 1
        st.rerun()

# Display table
start = (st.session_state.page - 1) * ROWS_PER_PAGE
page_df = filtered_df.iloc[start:start + ROWS_PER_PAGE]

event = st.dataframe(
    page_df,
    use_container_width=True,
    selection_mode="single-row",
    on_select="rerun",
    hide_index=True
)

# Show details when row selected
if event.selection.get("rows"):
    selected_index = event.selection["rows"][0]
    actual_index = filtered_df.index[start + selected_index]
    row = df.iloc[actual_index]
    
    with st.expander("📋 Item Details", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            # Get the Google Drive image link
            image_url = row.get('Image Link', '')
            if image_url:
                # Fix Google Drive URL to work with Streamlit
                if 'export=view' in image_url:
                    # Change export=view to export=download
                    image_url = image_url.replace('export=view', 'export=download')
                st.image(image_url, width=300)
            else:
                st.info("No image available")
        
        with col2:
            for col in display_df.columns:
                value = row[col] if row[col] else "—"
                st.markdown(f"**{col}:** {value}")
