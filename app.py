import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Mapping Yahoo Tickers to exact TradingView IDs
# --- MASTER TRADINGVIEW MAPPING ---
TV_MAP = {
    # 🇮🇳 Indian Indices & Sectors
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
    "^CNXCONSDURABL": "NSE:CNXCONSDURABLE",
    "^CNXHEALTHCARE": "NSE:CNXHEALTHCARE",
    "^CNXOILGAS": "NSE:CNXOILGAS",
    "^CNXMFG": "NSE:CNXMANUFACTURING",
    "DEFENCE.NS": "NSE:DEFENCE",

    # 🌍 Global Indices
    "^GSPC": "INDEX:SPX",        # S&P 500
    "^IXIC": "NASDAQ:IXIC",      # Nasdaq
    "^GDAXI": "XETR:DAX",        # DAX 40
    "^FTSE": "INDEX:UKX",        # FTSE 100
    "^N225": "TSE:NI225",        # Nikkei 225

    # 💎 Commodities (Yahoo Tickers usually work directly, but these are safer)
    "GC=F": "COMEX:GC1!",        # Gold Futures
    "SI=F": "COMEX:SI1!",        # Silver Futures
    "HG=F": "COMEX:HG1!",        # Copper Futures
    "CL=F": "NYMEX:CL1!",        # Crude Oil
    "NG=F": "NYMEX:NG1!",        # Natural Gas
    "HRC=F": "NYMEX:HRC1!",      # Steel
    "LIT": "AMEX:LIT",           # Lithium ETF

    # 💱 Forex
    "USDINR=X": "FX_IDC:USDINR",
    "EURUSD=X": "FX:EURUSD",
    "GBPUSD=X": "FX:GBPUSD",
    "JPY=X": "FX:USDJPY"
}

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="traderspavilion",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GLASSMORPHISM CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top left, #1a1c2c, #4a192c); }
    .market-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
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
    .symbol-name { font-size: 0.9rem; color: #888ea8; font-weight: 600; margin-bottom: 5px; }
    .price { font-size: 1.4rem; font-weight: 700; color: white; }
    .change-pos { color: #00ff88; font-size: 0.85rem; }
    .change-neg { color: #ff3b3b; font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=60)
def fetch_data(symbols_dict, period):
    data_list = []
    for name, sym in symbols_dict.items():
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period=period)
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
    "Commodities": {"Gold": "GC=F", "Silver": "SI=F", "Copper": "HG=F", "Steel": "HRC=F", "Lithium (LIT)": "LIT", "Crude Oil": "CL=F"},
    "Forex": {"USD/INR": "USDINR=X", "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X"}
}

# --- 4. CONFIGURATIONS (Updated with PSU, PSE, Energy, and Defence) ---
# --- 4. CONFIGURATIONS (Full 22 Sectors) ---
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
    "Nifty Cons Durbl": "^CNXCONSDURABL",
    "Nifty Healthcare": "^CNXHEALTHCARE",
    "Nifty Oil & Gas": "^CNXOILGAS",
    "NIFTY India Mfg": "^CNXMFG",
    "Nifty PSE": "^CPSE",
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
if market_choice == "India":
    st.title("🇮🇳 Indian Sectoral Velocity")
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
    st.title("🌍 Global Market Monitor")
    tabs = st.tabs(list(GLOBAL_MARKETS.keys()))
    for i, cat in enumerate(GLOBAL_MARKETS.keys()):
        with tabs[i]:
            data = fetch_data(GLOBAL_MARKETS[cat], timeframe)
            cols = st.columns(4)
            for idx, item in enumerate(data):
                with cols[idx % 4]:
                    color = "change-pos" if item['change'] >= 0 else "change-neg"
                    icon = "▲" if item['change'] >= 0 else "▼"
                    clean_sym = item['symbol'].replace('^', '').replace('=F', '').replace('=X', '')
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

st.caption(f"Last Refreshed: {datetime.now().strftime('%H:%M:%S')}")
