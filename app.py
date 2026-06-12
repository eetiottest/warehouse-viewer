import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS290SM6SoFt8t3UJ2CcH18VKuLv8FldT8a8UO7Zp52Ov56Hf-I6ChIzjczsYCGVShran2PZSdlAQd5/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

st.subheader("Inventory Data")

event = st.dataframe(
    display_df, 
    use_container_width=True, 
    selection_mode="single-row", 
    on_select="rerun"
)

if event.selection.get("rows"):
    selected_index = event.selection["rows"][0]
    selected_row = df.iloc[selected_index]
    
    details = selected_row.drop(labels=['Image', 'Image Link'], errors='ignore')
    
    # Converting to DataFrame and transposing to display vertically without index/row numbers
    details_df = pd.DataFrame(details).transpose()
    details_df = details_df.reset_index(drop=True)
    
    with st.expander(f"Details for: {selected_row.get('Location')}", expanded=True):
        st.table(details_df.T.rename(columns={0: "Value"}))
