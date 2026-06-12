import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide")

# 2. Data Loading
# We use st.cache_data so it doesn't reload every time you click something
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    return pd.read_csv(url)

df = load_data()

# 3. Display the Table
st.title("Warehouse Inventory Table")
st.dataframe(df, use_container_width=True)
