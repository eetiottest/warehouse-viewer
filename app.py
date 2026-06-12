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

# 3. Drop the columns for the table view
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

# 4. Display the table
st.subheader("Inventory Data")
event = st.dataframe(
    display_df, 
    use_container_width=True, 
    selection_mode="single-row", 
    on_select="rerun"
)

# 5. Mini-tab triggered by row selection
if event.selection["rows"]:
    selected_index = event.selection["rows"][0]
    selected_row = df.iloc[selected_index]
    
    with st.expander("▶ Details for Location: " + str(selected_row.get("Location", "N/A")), expanded=True):
        st.write(selected_row)
