import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- 1. THE LIVE DATA FETCH ENGINE ---
def get_nse_live_data():
    # NSE blocks basic scrapers, so we use 'Headers' to look like a Chrome browser
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'accept-language': 'en-US,en;q=0.9',
        'accept-encoding': 'gzip, deflate, br'
    }
    
    # We first visit the home page to get "Cookies" (NSE requirement)
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    
    # Now we hit the live API endpoint for all sector indices
    url = "https://www.nseindia.com/api/allIndices"
    response = session.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['data']
    return []

# --- 2. THE UI & MAPPING ---
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .stApp { background: #0e1117; }
    .market-card {
        background: #1e222d;
        border: 1px solid #363c4e;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    .price { font-size: 1.3rem; font-weight: bold; color: white; }
    .pos { color: #089981; } .neg { color: #f23645; }
    </style>
""", unsafe_allow_html=True)

# Map NSE Names to TradingView IDs (To avoid 404s)
TV_MAP = {
    "NIFTY 50": "NSE:NIFTY", "NIFTY BANK": "NSE:BANKNIFTY", "NIFTY IT": "NSE:CNXIT",
    "NIFTY AUTO": "NSE:CNXAUTO", "NIFTY PHARMA": "NSE:CNXPHARMA", "NIFTY FMCG": "NSE:CNXFMCG",
    "NIFTY REALTY": "NSE:CNXREALTY", "NIFTY METAL": "NSE:CNXMETAL", "NIFTY ENERGY": "NSE:CNXENERGY"
}

st.title("⚡ NSE Real-Time Dashboard")

try:
    raw_data = get_nse_live_data()
    cols = st.columns(4)
    
    # Filter only the sectors we want
    for i, item in enumerate(raw_data):
        name = item['index']
        if name in TV_MAP:
            with cols[len(TV_MAP) % 4]: # Simplified column logic
                color = "pos" if item['percentChange'] >= 0 else "neg"
                url = f"https://www.tradingview.com/symbols/{TV_MAP[name]}"
                
                st.markdown(f"""
                <a href="{url}" target="_blank" style="text-decoration:none">
                    <div class="market-card">
                        <div style="color:gray; font-size:0.8rem;">{name}</div>
                        <div class="price">{item['last']:,.2f}</div>
                        <div class="{color}">{item['percentChange']:.2f}%</div>
                    </div>
                </a>
                """, unsafe_allow_html=True)
except Exception as e:
    st.error("NSE Server Busy. Refresh in 5 seconds.")

st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')} (Direct from NSE)")
