import streamlit as st
import pandas as pd

st.set_page_config(page_title="Connection Test")

st.title("🧪 System Connection Test")

# Test 1: Library Check
try:
    st.write("✅ Pandas version:", pd.__version__)
    st.success("Environment is stable.")
except Exception as e:
    st.error(f"Error: {e}")

# Test 2: Dataframe Display
data = {"Test Col": ["Success", "Test passed"], "Value": [1, 2]}
df = pd.DataFrame(data)
st.table(df)

# Test 3: Google Sheet Connectivity (Published CSV method)
# Using the "Publish to Web" CSV method avoids all authentication errors
st.subheader("Testing Google Sheet CSV Link")
try:
    # IMPORTANT: Use the CSV link from File > Share > Publish to web
    url = "https://docs.google.com/spreadsheets/d/14GQoIfWuN2FG0huZ9H96xJyiDLXmNle1vRBxvl_3PX4/pub?output=csv"
    df_sheet = pd.read_csv(url)
    st.write("Successfully read", len(df_sheet), "rows from the Sheet.")
    st.dataframe(df_sheet.head())
except Exception as e:
    st.error(f"Could not read Google Sheet: {e}")
