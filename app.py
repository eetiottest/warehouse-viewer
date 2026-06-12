import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide")

# 2. Data Loading
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# 3. Drop unwanted columns for display
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

st.subheader("Inventory Data")

# 4. Display the table
# Selecting a row now acts as your "click"
event = st.dataframe(
    display_df,
    use_container_width=True,
    selection_mode="single-row",
    on_select="rerun",
    hide_index=True
)

# 5. When a row is clicked, show details
if event and event.selection.get("rows"):
    selected_index = event.selection["rows"][0]
    selected_row = df.iloc[selected_index]
    
    # Filter out columns we don't want in the details
    details = selected_row.drop(labels=['Image', 'Image Link'], errors='ignore')
    
    # This acts as your "mini-tab"
    with st.expander(f"Details for: {selected_row.get('Location', 'Selected Item')}", expanded=True):
        st.write(details)
