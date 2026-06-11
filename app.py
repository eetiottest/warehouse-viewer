import streamlit as st
import pandas as pd

# Set wide layout
st.set_page_config(layout="wide", page_title="Warehouse Full v1")

# CSS Styling
st.html("""<style>
    .appsheet-table-wrapper { width: 100%; background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; overflow-x: auto; margin-top: 15px; }
    .appsheet-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    .appsheet-table th { background-color: #F1F5F9; color: #475569; padding: 12px; font-size: 0.75rem; text-transform: uppercase; }
    .appsheet-table td { padding: 12px; border-bottom: 1px solid #E2E8F0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
</style>""")

@st.cache_data(ttl=600)
def load_data():
    # Public CSV URL
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQkarZ8ud6N-YO8aFTgIMidqO5uCbyKoqiIZaukL6Ql8K99XRX_-3cjmuGfaNWdOh8QHZWLP4-ePYuN/pub?output=csv"
    
    # dtype=str prevents the 2^53 integer overflow error
    df = pd.read_csv(url, dtype=str).fillna("")
    df.columns = df.columns.astype(str).str.strip()
    return df

df = load_data()

st.title("📂 Warehouse Full v1")

# Display the table
st.markdown('<div class="appsheet-table-wrapper">', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Image Handling Logic
st.subheader("Item Detail Preview")
selected_row_idx = st.number_input("Enter Row Number to view image", min_value=0, max_value=len(df)-1, value=0)
row = df.iloc[selected_row_idx]

st.write(f"**Description:** {row.get('Description', 'N/A')}")

# For images to show in the cloud, they MUST be public URLs. 
# If your 'Image' column contains a public link (like an Imgur or Google Drive share link), it will render.
image_url = row.get("Image", "")
if image_url and image_url.startswith("http"):
    st.image(image_url, caption="Item Image", width=300)
else:
    st.warning("No valid public image URL found for this row.")
