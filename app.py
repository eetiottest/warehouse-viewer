import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide")

# 2. Data Loading
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url)
    # Clean up column names (removes extra spaces)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# 3. Remove unwanted columns
# We use errors='ignore' so it won't crash if it can't find a column
cols_to_drop = ['Image', 'Image Link'] 
display_df = df.drop(columns=cols_to_drop, errors='ignore')

# 4. Display the Cleaned Table
st.title("Warehouse Inventory Table")
st.dataframe(display_df, use_container_width=False)
