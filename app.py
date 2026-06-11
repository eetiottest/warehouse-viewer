import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data(ttl=600)
def load_data():
    # Replace this URL with the one you just generated from "Publish to web"
    url = "https://docs.google.com/spreadsheets/d/14GQoIfWuN2FG0huZ9H96xJyiDLXmNle1vRBxvl_3PX4/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.astype(str).str.strip()
    return df

try:
    df = load_data()
    st.title("Warehouse Inventory Viewer")
    st.table(df.head(10)) # Displays first 10 rows to verify
    st.success("Successfully loaded data from Google Sheets!")
except Exception as e:
    st.error(f"Error loading data: {e}")
