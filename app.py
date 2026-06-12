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

# 1. Prepare display dataframe
display_df = df.drop(columns=['Image', 'Image Link'], errors='ignore')

# 2. Add the trigger column
display_df.insert(0, "Details", "▶")

st.subheader("Inventory Data")

# 3. Use data_editor to avoid automatic checkboxes
edited_df = st.data_editor(
    display_df,
    use_container_width=True,
    hide_index=True,
    disabled=df.columns, # This makes the table read-only
    column_config={
        "Details": st.column_config.TextColumn("View", width="small")
    }
)

# 4. Logic for the arrow
# We look for which cell in the 'Details' column was clicked
for i, row in edited_df.iterrows():
    if row["Details"] == "▼":  # If user changed ▶ to ▼
        # Trigger your expansion here
        with st.expander(f"Details for {row['Location']}", expanded=True):
            st.write(df.iloc[i].drop(labels=['Image', 'Image Link'], errors='ignore'))
        
        # Reset the arrow back to ▶ for next time
        edited_df.at[i, "Details"] = "▶"
