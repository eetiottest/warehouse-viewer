import streamlit as st
import pandas as pd

st.title("Bare Metal Test")

# No external files, no external connections
data = {
    "Location": ["AB-001-B", "AB-001-C"],
    "SKU": [3114159, 3114816],
    "Status": ["MATCH", "MATCH"]
}

df = pd.DataFrame(data)

st.write("If you see this table, your deployment pipeline is working:")
st.table(df)

st.success("Deployment successful without external dependencies.")
