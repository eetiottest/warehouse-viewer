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

# 3. Drop columns for table view
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

# 4. Display the table
st.subheader("Inventory Data")
st.dataframe(display_df, use_container_width=True)

# 5. "Triangle" Button Logic
# This button acts as a trigger to view details for a specific index
# We use a text input to pick the row by ID/Index
row_to_view = st.number_input("Enter Row Number to view details:", min_value=0, max_value=len(df)-1, step=1)

if st.button("▶ Open Details"):
    selected_row = df.iloc[row_to_view]
    
    # We clean the data for display by dropping the columns here too
    details = selected_row.drop(labels=['Image', 'Image Link'], errors='ignore')
    
    with st.expander("Details", expanded=True):
        st.write(details)
