import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- MASTER TRADINGVIEW MAPPING ---
TV_MAP = {
    "^NSEI": "NSE:NIFTY",
    "^NSEBANK": "NSE:BANKNIFTY",
    "^CNXPSUBANK": "NSE:CNXPSUBANK",
    "^PVTBANK": "NSE:NIFTY_PVT_BANK",
    "^CNXFINANCE": "NSE:CNXFINANCE",
    "^CNXIT": "NSE:CNXIT",
    "^CNXAUTO": "NSE:CNXAUTO",
    "^CNXFMCG": "NSE:CNXFMCG",
    "^CNXMETAL": "NSE:CNXMETAL",
    "^CNXPHARMA": "NSE:CNXPHARMA",
    "^CNXREALTY": "NSE:CNXREALTY",
    "^CNXMEDIA": "NSE:CNXMEDIA",
    "^CNXENERGY": "NSE:CNXENERGY",
    "^CNXINFRA": "NSE:CNXINFRA",
    "^CPSE": "NSE:CPSE",
    "^CNXCOMMODITIES": "NSE:CNXCOMMODITIES",
    "^CNXCONSUMPTION": "NSE:CNXCONSUMPTION",
    "^CNXSERVICE": "NSE:CNXSERVICE",
    "NIFTY_CONSR_DURBL.NS": "NSE:CNXCONSDURABLE",
    "^CNXHEALTHCARE": "NSE:CNXHEALTHCARE",
    "^CNXOILGAS": "NSE:CNXOILGAS",
    "NIFTY_INDIA_MFG.NS": "NSE:CNXMANUFACTURING",
    "DEFENCE.NS": "NSE:DEFENCE",
    "^GSPC": "INDEX:SPX",
    "^IXIC": "NASDAQ:IXIC",
    "^GDAXI": "XETR:DAX",
    "^FTSE": "INDEX:UKX",
    "^N225": "TSE:NI225",
    "GC=F": "COMEX:GC1!",
    "SI=F": "COMEX:SI1!",
    "HG=F": "COMEX:HG1!",
    "CL=F": "NYMEX:CL1!",
    "NG=F": "NYMEX:NG1!",
    "HRC=F": "NYMEX:HRC1!",
    "LIT": "AMEX:LIT",
    "USDINR=X": "FX_IDC:USDINR",
    "EURUSD=X": "FX:EURUSD",
    "GBPUSD=X": "FX:GBPUSD"
}

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
    .symbol-name { font-size: 0.85rem; color: #888ea8; font-weight: 600; margin-bottom: 5px; }
    .price { font-size: 1.2rem; font-weight: 700; color: white; }
    .change-pos { color: #00ff88; font-size: 0.8rem; }
    .change-neg { color: #ff3b3b; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=60)
def fetch_data(symbols_dict, period):
    data_list = []
    for name, sym in symbols_dict.items():
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="5d" if period == "1d" else period)
            if not hist.empty:
                curr = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[0]
                chg = ((curr - prev) / prev) * 100
                data_list.append({"name": name, "symbol": sym, "price": curr, "change": chg})
        except: continue
    return data_list

# --- 4. CONFIGURATIONS ---
GLOBAL_MARKETS = {
    "Global Indices": {"Nifty 50": "^NSEI", "S&P 500": "^GSPC", "Nasdaq 100": "^IXIC", "DAX 40": "^GDAXI", "FTSE 100": "^FTSE"},
    "Commodities": {"Gold": "GC=F", "Silver": "SI=F", "Copper": "HG=F", "Steel": "HRC=F", "Lithium": "LIT", "Crude Oil": "CL=F"},
    "Forex": {"USD/INR": "USDINR=X", "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X"}
}

INDIA_SECTORS = {
    "Bank Nifty": "^NSEBANK",
    "Nifty PSU Bank": "^CNXPSUBANK",
    "Nifty Pvt Bank": "^PVTBANK",
    "Nifty IT": "^CNXIT",
    "Nifty Auto": "^CNXAUTO",
    "Nifty FMCG": "^CNXFMCG",
    "Nifty Metal": "^CNXMETAL",
    "Nifty Pharma": "^CNXPHARMA",
    "Nifty Realty": "^CNXREALTY",
    "Nifty Media": "^CNXMEDIA",
    "Nifty Energy": "^CNXENERGY",
    "Nifty Infra": "^CNXINFRA",
    "Nifty Fin Service": "^CNXFINANCE",
    "Nifty Commodities": "^CNXCOMMODITIES",
    "Nifty Consumption": "^CNXCONSUMPTION",
    "Nifty Services": "^CNXSERVICE",
    "Nifty Healthcare": "^CNXHEALTHCARE",
    "Nifty Oil & Gas": "^CNXOILGAS",
    "Nifty PSE": "^CPSE",
    "Nifty Microcap 250": "^NIFTY_MICROCAP250", # Added
    "Nifty Midcap 100": "^MZNifty",           # Added
    "Nifty Smallcap 100": "^CNXSC",          # Added
    "Nifty India Defence": "DEFENCE.NS"
}

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("# traders<span style='color:#22c55e'>pavilion</span>", unsafe_allow_html=True)
    st.divider()
    market_choice = st.selectbox("Market Type", ["India", "Global Markets"])
    timeframe = st.select_slider("Timeframe", options=["1d", "5d", "1mo", "1y"], value="1d")
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

# --- 6. MAIN DISPLAY ---
st.title(f"📊 {market_choice} Velocity")

if market_choice == "India":
    data = fetch_data(INDIA_SECTORS, timeframe)
    cols = st.columns(4)
    for idx, item in enumerate(data):
        with cols[idx % 4]:
            color = "change-pos" if item['change'] >= 0 else "change-neg"
            icon = "▲" if item['change'] >= 0 else "▼"
            tv_id = TV_MAP.get(item['symbol'], item['symbol'].replace('^', ''))
            url = f"https://www.tradingview.com/symbols/{tv_id}"
            st.markdown(f"""
                <a href="{url}" target="_blank" style="text-decoration:none">
                    <div class="market-card">
                        <div class="symbol-name">{item['name']}</div>
                        <div class="price">{item['price']:,.2f}</div>
                        <div class="{color}">{icon} {abs(item['change']):.2f}%</div>
                    </div>
                </a>""", unsafe_allow_html=True)
else:
    tabs = st.tabs(list(GLOBAL_MARKETS.keys()))
    for i, cat in enumerate(GLOBAL_MARKETS.keys()):
        with tabs[i]:
            data = fetch_data(GLOBAL_MARKETS[cat], timeframe)
            cols = st.columns(4)
            for idx, item in enumerate(data):
                with cols[idx % 4]:
                    color = "change-pos" if item['change'] >= 0 else "change-neg"
                    icon = "▲" if item['change'] >= 0 else "▼"
                    tv_id = TV_MAP.get(item['symbol'], item['symbol'].replace('^', '').replace('=F', '').replace('=X', ''))
                    url = f"https://www.tradingview.com/symbols/{tv_id}"
                    st.markdown(f"""
                        <a href="{url}" target="_blank" style="text-decoration:none">
                            <div class="market-card">
                                <div class="symbol-name">{item['name']}</div>
                                <div class="price">{item['price']:,.2f}</div>
                                <div class="{color}">{icon} {abs(item['change']):.2f}%</div>
                            </div>
                        </a>""", unsafe_allow_html=True)

st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
