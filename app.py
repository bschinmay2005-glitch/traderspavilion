import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="traderspavilion", page_icon="📈", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top left, #1a1c2c, #4a192c); }
    .market-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        transition: transform 0.3s ease;
        text-decoration: none !important;
        display: block;
        margin-bottom: 20px;
    }
    .market-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.1); }
    .symbol-name { font-size: 0.8rem; color: #888ea8; font-weight: 600; text-transform: uppercase; }
    .price { font-size: 1.2rem; font-weight: 700; color: white; margin: 5px 0; }
    .change-pos { color: #00ff88; font-size: 0.85rem; font-weight: bold; }
    .change-neg { color: #ff3b3b; font-size: 0.85rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=30)
def fetch_data(symbols_dict, timeframe):
    data_list = []
    for name, sym in symbols_dict.items():
        try:
            t = yf.Ticker(sym)
            df = t.history(period="7d" if timeframe in ["1d", "5d"] else timeframe)
            if not df.empty:
                current_price = df['Close'].iloc[-1]
                prev_price = df['Close'].iloc[-2] if timeframe == "1d" else df['Close'].iloc[0]
                change = ((current_price - prev_price) / prev_price) * 100
                data_list.append({"name": name, "symbol": sym, "price": current_price, "change": change})
        except: continue
    return data_list

# --- 4. CONFIGURATIONS ---
INDIA_SECTORS = {
    "Nifty IT": "^CNXIT", "Nifty Pharma": "^CNXPHARMA", 
    "Nifty Auto": "^CNXAUTO", "Nifty Metal": "^CNXMETAL", "Nifty FMCG": "^CNXFMCG", 
    "Nifty Realty": "^CNXREALTY", "Nifty Energy": "^CNXENERGY", "Nifty Infra": "^CNXINFRA", 
    "Nifty PSU Bank": "^CNXPSUBANK", "Nifty Pvt Bank": "^PVTBANK", "Nifty Media": "^CNXMEDIA", 
    "Nifty PSE": "^CPSE", "Nifty Fin Service": "^CNXFINANCE", "Nifty Service": "^CNXSERVICE", 
    "Nifty Commodities": "^CNXCOMMODITIES", "Nifty Consumption": "^CNXCONSUMPTION", 
    "Nifty Healthcare": "HEALTHY.NS", "Nifty Oil & Gas": "OIL.NS", 
    "Nifty Mfg": "MAKEINDIA.NS", "Nifty India Defence": "NIFTY_INDIA_DEFENCE", "Nifty MNC": "MNC.NS"
}

GLOBAL_MARKETS = {
    "Indices": {"Nifty 50": "^NSEI", "S&P 500": "^GSPC", "Nasdaq 100": "^IXIC", "DAX": "^GDAXI", "FTSE 100": "^FTSE"},
    "Commodities": {"Gold": "GC=F", "Silver": "SI=F", "Crude Oil": "CL=F", "Natural Gas": "NG=F"},
    "Forex": {"USD/INR": "USDINR=X", "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X"}
}

TV_MAP = {
    "^NSEI": "NSE:NIFTY", "^NSEBANK": "NSE:BANKNIFTY", "^CNXIT": "NSE:CNXIT",
    "^CNXPHARMA": "NSE:CNXPHARMA", "^CNXAUTO": "NSE:CNXAUTO", "^CNXMETAL": "NSE:CNXMETAL",
    "HEALTHY.NS": "NSE:CNXHEALTHCARE", "OIL.NS": "NSE:CNXOILGAS", "MAKEINDIA.NS": "NSE:CNXMANUFACTURING",
    "DEFENCE.NS": "NSE:DEFENCE", "USDINR=X": "FX_IDC:USDINR", "GC=F": "COMEX:GC1!"
}

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("# traders<span style='color:#22c55e'>pavilion</span>", unsafe_allow_html=True)
    st.divider()
    market_view = st.selectbox("Select Market", ["India Sectors", "Global Markets"])
    time_slider = st.select_slider("Timeframe", options=["1d", "5d", "1mo", "1y"], value="1d")
    if st.button("🔄 Force Refresh"):
        st.cache_data.clear()
        st.rerun()

# --- 6. MAIN UI ---
if market_view == "India Sectors":
    st.title("🇮🇳 Sectoral Velocity")
    data = fetch_data(INDIA_SECTORS, time_slider)
    cols = st.columns(4)
    for i, item in enumerate(data):
        with cols[i % 4]:
            color = "change-pos" if item['change'] >= 0 else "change-neg"
            arrow = "▲" if item['change'] >= 0 else "▼"
            tv_id = TV_MAP.get(item['symbol'], item['symbol'].replace('^', '').replace('.NS', '').replace('=F', ''))
            url = f"https://www.tradingview.com/symbols/{tv_id}"
            st.markdown(f"""<a href="{url}" target="_blank" style="text-decoration:none"><div class="market-card">
                <div class="symbol-name">{item['name']}</div><div class="price">{item['price']:,.2f}</div>
                <div class="{color}">{arrow} {abs(item['change']):.2f}%</div></div></a>""", unsafe_allow_html=True)

else:
    st.title("🌍 Global Market Watch")
    tabs = st.tabs(["Indices", "Commodities", "Forex"])
    for idx, (category, symbols) in enumerate(GLOBAL_MARKETS.items()):
        with tabs[idx]:
            data = fetch_data(symbols, time_slider)
            cols = st.columns(4)
            for i, item in enumerate(data):
                with cols[i % 4]:
                    color = "change-pos" if item['change'] >= 0 else "change-neg"
                    arrow = "▲" if item['change'] >= 0 else "▼"
                    tv_id = TV_MAP.get(item['symbol'], item['symbol'].replace('^', '').replace('=F', '').replace('=X', ''))
                    url = f"https://www.tradingview.com/symbols/{tv_id}"
                    st.markdown(f"""<a href="{url}" target="_blank" style="text-decoration:none"><div class="market-card">
                        <div class="symbol-name">{item['name']}</div><div class="price">{item['price']:,.2f}</div>
                        <div class="{color}">{arrow} {abs(item['change']):.2f}%</div></div></a>""", unsafe_allow_html=True)

st.caption(f"Last Refreshed: {datetime.now().strftime('%H:%M:%S')}")
