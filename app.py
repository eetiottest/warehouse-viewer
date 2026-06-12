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

# 3. Drop columns for display
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

# 4. Add a column for the Arrow
display_df.insert(0, "Select", "▶") 

# 5. Display the Table
st.subheader("Inventory Data")

event = st.dataframe(
    display_df,
    use_container_width=True,
    selection_mode="single-row",
    on_select="rerun",
    hide_index=True
)

# 6. FIXED Interaction Logic
# We check if event.selection exists, if 'rows' exists in it, and if it is not empty
if event and "selection" in event and event.selection.get("rows"):
    selected_index = event.selection["rows"][0]
    selected_row = df.iloc[selected_index]
    
    # Exclude the image columns from the display details
    details = selected_row.drop(labels=['Image', 'Image Link'], errors='ignore')
    
    with st.expander(f"Details for: {selected_row.get('Location', 'Selected Item')}", expanded=True):
        st.table(details)
