import streamlit as st
from nsepythonserver import nse_get_index_quotes
import pandas as pd
from datetime import datetime

# --- 1. DATA ENGINE (NSE DIRECT) ---
@st.cache_data(ttl=30)
def get_nse_data():
    try:
        # This function fetches all sectoral indices in one shot
        data = nse_get_index_quotes()
        return data
    except Exception as e:
        st.error(f"NSE Connection Blocked: {e}")
        return []

# --- 2. CONFIG & UI ---
st.set_page_config(layout="wide")

# Mapping NSE index names to TradingView IDs
TV_MAP = {
    "NIFTY 50": "NSE:NIFTY", "NIFTY BANK": "NSE:BANKNIFTY", 
    "NIFTY IT": "NSE:CNXIT", "NIFTY AUTO": "NSE:CNXAUTO",
    "NIFTY PHARMA": "NSE:CNXPHARMA", "NIFTY FMCG": "NSE:CNXFMCG",
    "NIFTY METAL": "NSE:CNXMETAL", "NIFTY REALTY": "NSE:CNXREALTY"
}

st.title("⚡ Direct NSE Live Watch")

raw_indices = get_nse_data()

if raw_indices:
    cols = st.columns(4)
    # We filter for the specific sectors we want to display
    valid_data = [i for i in raw_indices if i['indexName'] in TV_MAP]
    
    for idx, item in enumerate(valid_data):
        with cols[idx % 4]:
            name = item['indexName']
            price = item['last']
            change = float(item['percentChange'])
            color = "#00ff88" if change >= 0 else "#ff3b3b"
            url = f"https://www.tradingview.com/symbols/{TV_MAP[name]}"
            
            st.markdown(f"""
                <a href="{url}" target="_blank" style="text-decoration:none">
                    <div style="background:#1e222d; border:1px solid #363c4e; border-radius:10px; padding:20px; text-align:center; margin-bottom:15px;">
                        <div style="color:gray; font-size:0.8rem; font-weight:bold;">{name}</div>
                        <div style="color:white; font-size:1.5rem; font-weight:bold; margin:10px 0;">{price}</div>
                        <div style="color:{color}; font-weight:bold;">{"▲" if change >= 0 else "▼"} {abs(change):.2f}%</div>
                    </div>
                </a>
            """, unsafe_allow_html=True)
else:
    st.warning("NSE is currently blocking the connection. Try refreshing in 10 seconds.")

st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')} (Source: NSE India)")
