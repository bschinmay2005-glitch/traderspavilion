import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- 1. THE MASTER MAPPING ---
# 'Display Name': ['Yahoo Ticker', 'TradingView ID']
# This ensures the price works AND the button never 404s.
MARKET_MAP = {
    "Nifty 50": ["^NSEI", "NSE:NIFTY"],
    "Bank Nifty": ["^NSEBANK", "NSE:BANKNIFTY"],
    "Nifty IT": ["^CNXIT", "NSE:CNXIT"],
    "Nifty Pharma": ["^CNXPHARMA", "NSE:CNXPHARMA"],
    "Nifty Auto": ["^CNXAUTO", "NSE:CNXAUTO"],
    "Nifty Metal": ["^CNXMETAL", "NSE:CNXMETAL"],
    "Nifty FMCG": ["^CNXFMCG", "NSE:CNXFMCG"],
    "Nifty Realty": ["^CNXREALTY", "NSE:CNXREALTY"],
    "Nifty Energy": ["^CNXENERGY", "NSE:CNXENERGY"],
    "Nifty Infra": ["^CNXINFRA", "NSE:CNXINFRA"],
    "Nifty PSU Bank": ["^CNXPSUBANK", "NSE:CNXPSUBANK"],
    "Nifty Pvt Bank": ["PVTBANK.NS", "NSE:NIFTY_PVT_BANK"],
    "Nifty Media": ["MEDIA.NS", "NSE:CNXMEDIA"],
    "Nifty PSE": ["^CPSE", "NSE:CPSE"],
    "Nifty Fin Service": ["^CNXFINANCE", "NSE:CNXFINANCE"],
    "Nifty Service": ["SERVICES.NS", "NSE:CNXSERVICE"],
    "Nifty Commodities": ["COMMODITIES.NS", "NSE:CNXCOMMODITIES"],
    "Nifty Consumption": ["CONSUME.NS", "NSE:CNXCONSUMPTION"],
    "Nifty Healthcare": ["^CNXHEALTHCARE", "NSE:CNXHEALTHCARE"],
    "Nifty Oil & Gas": ["^CNXOILGAS", "NSE:CNXOILGAS"],
    "Nifty Mfg": ["MAKEINDIA.NS", "NSE:CNXMANUFACTURING"],
    "Nifty Defence": ["DEFENCE.NS", "NSE:DEFENCE"]
}

# --- 2. DATA ENGINE ---
@st.cache_data(ttl=15)
def fetch_market_data():
    results = []
    # Fetching all tickers in one go is faster (The "Best" way to use Yahoo)
    all_yahoo_tickers = [v[0] for v in MARKET_MAP.values()]
    data = yf.download(all_yahoo_tickers, period="5d", interval="1d", group_by='ticker', progress=False)
    
    for name, tickers in MARKET_MAP.items():
        y_ticker = tickers[0]
        tv_id = tickers[1]
        try:
            df = data[y_ticker]
            if not df.empty:
                curr = df['Close'].iloc[-1]
                prev = df['Close'].iloc[-2]
                pct = ((curr - prev) / prev) * 100
                results.append({"name": name, "price": curr, "pct": pct, "tv_id": tv_id})
        except: continue
    return results

# --- 3. UI LAYOUT ---
st.set_page_config(layout="wide", page_title="TradersPavilion Pro")
st.markdown("""
    <style>
    .stApp { background: #0e1117; }
    .market-card {
        background: #1e222d;
        border: 1px solid #363c4e;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
        margin-bottom: 15px;
    }
    .market-card:hover { border-color: #2962ff; background: #2a2e39; }
    .price { font-size: 1.4rem; font-weight: bold; color: white; margin: 5px 0; }
    .pos { color: #089981; font-weight: bold; }
    .neg { color: #f23645; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🇮🇳 Live Sector Velocity")
data = fetch_market_data()

cols = st.columns(4)
for i, item in enumerate(data):
    with cols[i % 4]:
        color = "pos" if item['pct'] >= 0 else "neg"
        arrow = "▲" if item['pct'] >= 0 else "▼"
        # THE FIX: We use the TV ID specifically for the URL
        url = f"https://www.tradingview.com/symbols/{item['tv_id']}"
        
        st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration:none">
                <div class="market-card">
                    <div style="color:#d1d4dc; font-size:0.9rem;">{item['name']}</div>
                    <div class="price">{item['price']:,.2f}</div>
                    <div class="{color}">{arrow} {abs(item['pct']):.2f}%</div>
                </div>
            </a>
        """, unsafe_allow_html=True)

st.caption(f"Refreshed at: {datetime.now().strftime('%H:%M:%S')} | Data: Yahoo | Links: TradingView")
