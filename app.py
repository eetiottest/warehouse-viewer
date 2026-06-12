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

# 4. Add a "Details" button column to the dataframe
# This will render as an arrow button in the table
display_df.insert(0, "View", "▶") 

# 5. Display the Table
st.subheader("Inventory Data")

event = st.dataframe(
    display_df,
    use_container_width=True,
    column_config={
        "View": st.column_config.Column(
            "Details", 
            help="Click to open", 
            width="small"
        ),
    },
    hide_index=True
)

# 6. Interaction Logic
# When the user clicks the "View" column, we show the details below the table
# Note: Since Streamlit tables are read-only for clicks, we check for a selection
# or use the last clicked row index.
if event.selection["rows"]:
    selected_index = event.selection["rows"][0]
    selected_row = df.iloc[selected_index]
    
    # Exclude the image columns from the display details
    details = selected_row.drop(labels=['Image', 'Image Link'], errors='ignore')
    
    with st.expander("Details for: " + str(selected_row.get("Location", "Selected Item")), expanded=True):
        st.table(details)
