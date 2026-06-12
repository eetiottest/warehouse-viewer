import streamlit as st
import pandas as pd

# 1. Data Loading
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# 2. Logic to handle the "click"
# We store the selected location in the session state
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = None

st.subheader("Inventory Data")

# 3. Manual Table Builder (This is 100% clean, no checkboxes)
# We loop through the dataframe and create a button for each location
for index, row in df.iterrows():
    # We display the Location as a button. When pressed, it updates the session state
    if st.button(f"{row['Location']}", key=f"btn_{index}"):
        st.session_state.selected_location = index

# 4. Show details if a location was pressed
if st.session_state.selected_location is not None:
    idx = st.session_state.selected_location
    row = df.iloc[idx]
    
    # Filter out columns we don't want
    details = row.drop(labels=['Image', 'Image Link'], errors='ignore')
    
    st.divider()
    with st.expander(f"Details for: {row['Location']}", expanded=True):
        st.write(details)
