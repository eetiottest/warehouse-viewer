import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Warehouse Full v1", initial_sidebar_state="collapsed")

# 2. Styling (CSS)
st.html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    .appsheet-title { font-size: 1.5rem; font-weight: 700; color: #0F172A; margin-bottom: 2px; }
    .appsheet-subtitle { font-size: 0.9rem; color: #64748B; margin-bottom: 20px; font-weight: 500; }
    .appsheet-table-wrapper { width: 100%; background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; overflow-x: auto; box-shadow: 0 1px 3px rgba(0,0,0,0.02); margin-top: 15px; }
    .appsheet-table { width: 100%; border-collapse: collapse; text-align: left; table-layout: fixed; }
    .appsheet-table th { background-color: #F1F5F9; color: #475569; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; padding: 12px 16px; border-bottom: 2px solid #E2E8F0; white-space: nowrap; }
    .appsheet-table td { padding: 10px 16px; color: #0F172A; font-size: 0.85rem; border-bottom: 1px solid #E2E8F0; vertical-align: middle; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .badge { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 700; }
    .badge-match { background-color: #E6F4EA; color: #137333; }
    .badge-mismatch { background-color: #FCE8E6; color: #C5221F; }
    .badge-na { background-color: #F1F3F4; color: #3C4043; }
    .table-action-btn { background-color: #1E40AF; color: #FFFFFF !important; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; text-decoration: none; }
    </style>
""")

# 3. Data Loading via Google Sheets
@st.cache_data(ttl=600)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    url = "https://docs.google.com/spreadsheets/d/14GQoIfWuN2FG0huZ9H96xJyiDLXmNle1vRBxvl_3PX4/edit"
    df = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11]) # Adjust index if needed
    df.columns = df.columns.astype(str).str.strip()
    # Rename columns to match logic
    return df.rename(columns={"Status": "Inventory Sts", "Count": "On Hand Qty", "Layer Check": "Layer Count"})

df = load_data()

# 4. View Logic
query_params = st.query_params
selected_location = query_params.get("loc", None)

if "current_page" not in st.session_state: st.session_state.current_page = 0

if selected_location:
    matched = df[df["Location"] == selected_location]
    if not matched.empty:
        if st.button("⬅️ Back to Table"):
            st.query_params.clear(); st.rerun()
        st.write(matched.iloc[0].to_dict()) 
    else:
        st.query_params.clear(); st.rerun()
else:
    st.markdown('<div class="appsheet-title">📂 Warehouse Full v1</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1: search = st.text_input("Search", placeholder="Type here...")
    with c2: status_filt = st.selectbox("Status", ["All Statuses"] + list(df["Inventory Sts"].unique()))
    
    # Simple Filtering
    if status_filt != "All Statuses": df = df[df["Inventory Sts"] == status_filt]
    
    items_per_page = 25
    total_pages = max(1, (len(df) + items_per_page - 1) // items_per_page)
    
    # Render Table
    table_html = """
    <div class="appsheet-table-wrapper"><table class="appsheet-table">
        <thead><tr>
            <th style="width: 10%;">Location</th><th style="width: 10%;">SKU</th>
            <th style="width: 25%;">Description</th><th style="width: 20%;">SSCC</th>
            <th style="width: 10%;">Status</th><th style="width: 8%;">Qty</th>
            <th style="width: 10%;">Badge</th><th style="width: 7%; text-align:right;">Action</th>
        </tr></thead><tbody>
    """
    chunk = df.iloc[st.session_state.current_page*items_per_page : (st.session_state.current_page+1)*items_per_page]
    for idx, row in chunk.iterrows():
        status = str(row.get("Inventory Sts", "")).upper()
        badge = f'<span class="badge badge-match">🟢 MATCH</span>' if "MATCH" in status else (f'<span class="badge badge-mismatch">🔴 MISMATCH</span>' if "MISMATCH" in status else f'<span class="badge badge-na">⚪ NA</span>')
        table_html += f"""<tr>
            <td><b>{row.get('Location')}</b></td><td>{row.get('SKU')}</td><td>{row.get('Description')}</td>
            <td><code>{row.get('SSCC')}</code></td><td>{status}</td><td>{row.get('On Hand Qty')}</td>
            <td>{badge}</td><td style="text-align:right;"><a class="table-action-btn" href="?loc={row.get('Location')}" target="_self">View ➡️</a></td>
        </tr>"""
    table_html += "</tbody></table></div>"
    st.html(table_html)
    
    cols = st.columns([1, 2, 1])
    if cols[0].button("◀️ Prev"): st.session_state.current_page -= 1; st.rerun()
    cols[1].markdown(f"<div style='text-align:center;'>Page {st.session_state.current_page + 1} of {total_pages}</div>", unsafe_allow_html=True)
    if cols[2].button("Next ▶️"): st.session_state.current_page += 1; st.rerun()
