import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- 1. THE DATA ENGINE (GOOGLE REAL-TIME) ---
def fetch_google_finance(ticker):
    # This hits the Google Finance search endpoint which returns live data
    url = f"https://www.google.com/finance/quote/{ticker}:NSE"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        # We search the HTML for the price data-value
        # This is a 'light' scrape that Google usually allows
        content = response.text
        price_search = content.split('data-last-price="')[1].split('"')[0]
        change_search = content.split('data-price-percentage-change="')[1].split('"')[0]
        
        return float(price_search), float(change_search)
    except:
        return None, None

# --- 2. THE UI STYLING ---
st.set_page_config(page_title="traderspavilion", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #0e1117; }
    .market-card {
        background: #1e222d;
        border: 1px solid #363c4e;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .price { font-size: 1.5rem; font-weight: bold; color: white; }
    .pos { color: #00ff88; } .neg { color: #ff3b3b; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SECTOR MAPPING (Google Ticker vs TradingView ID) ---
# Format: "Display Name": ["Google Ticker", "TradingView ID"]
SECTORS = {
    "Nifty 50": ["NIFTY_50", "NSE:NIFTY"],
    "Bank Nifty": ["NIFTY_BANK", "NSE:BANKNIFTY"],
    "Nifty IT": ["NIFTY_IT", "NSE:CNXIT"],
    "Nifty Auto": ["NIFTY_AUTO", "NSE:CNXAUTO"],
    "Nifty Pharma": ["NIFTY_PHARMA", "NSE:CNXPHARMA"],
    "Nifty Metal": ["NIFTY_METAL", "NSE:CNXMETAL"],
    "Nifty FMCG": ["NIFTY_FMCG", "NSE:CNXFMCG"],
    "Nifty Realty": ["NIFTY_REALTY", "NSE:CNXREALTY"]
}

# --- 4. DISPLAY LOOP ---
st.sidebar.markdown("# traders<span style='color:#22c55e'>pavilion</span> ⚡", unsafe_allow_html=True)
st.title("⚡ Live Market Velocity")

cols = st.columns(4)
idx = 0

for name, ids in SECTORS.items():
    price, change = fetch_google_finance(ids[0])
    
    if price:
        with cols[idx % 4]:
            color = "pos" if change >= 0 else "neg"
            url = f"https://www.tradingview.com/symbols/{ids[1]}"
            
            st.markdown(f"""
                <a href="{url}" target="_blank" style="text-decoration:none">
                    <div class="market-card">
                        <div style="color:#848e9c; font-size:0.8rem;">{name}</div>
                        <div class="price">{price:,.2f}</div>
                        <div class="{color}">{"▲" if change >= 0 else "▼"} {abs(change):.2f}%</div>
                    </div>
                </a>
            """, unsafe_allow_html=True)
            idx += 1
    else:
        # If Google blocks a specific ticker, it won't break the whole app
        continue

st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')} | Source: Google Finance")
