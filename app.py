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
    .market-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.1); border-color: #2962ff; }
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
    # Extract just the Yahoo tickers for the batch download
    yahoo_tickers = [v[0] for v in symbols_dict.values()]
    try:
        raw_data = yf.download(yahoo_tickers, period="1mo", interval="1d", group_by='ticker', progress=False)
        for name, ids in symbols_dict.items():
            y_sym = ids[0]
            tv_id = ids[1]
            try:
                # Handle single vs multi-ticker dataframe return from yf
                df = raw_data[y_sym] if len(yahoo_tickers) > 1 else raw_data
                if not df.empty:
                    current_price = df['Close'].iloc[-1].item()
                    prev_price = df['Close'].iloc[-2].item() if timeframe == "1d" else df['Close'].iloc[0].item()
                    change = ((current_price - prev_price) / prev_price) * 100
                    data_list.append({"name": name, "tv_id": tv_id, "price": current_price, "change": change})
            except: continue
    except: pass
    return data_list

# --- 4. CONFIGURATIONS ---
# [Yahoo Ticker, TradingView Link ID]
INDIA_SECTORS = {
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
GLOBAL_MARKETS = {
    "Indices": {
        "S&P 500": ["^GSPC", "INDEX:SPX"],
        "Nasdaq 100": ["^IXIC", "INDEX:IUXX"],
        "DAX 40": ["^GDAXI", "XETR:DAX"],
        "FTSE 100": ["^FTSE", "INDEX:UKX"]
    },
    "Commodities": {
        "Gold": ["GC=F", "COMEX:GC1!"],
        "Silver": ["SI=F", "COMEX:SI1!"],
        "Crude Oil": ["CL=F", "NYMEX:CL1!"],
        "Natural Gas": ["NG=F", "NYMEX:NG1!"]
    },
    "Forex": {
        "USD/INR": ["USDINR=X", "FX_IDC:USDINR"],
        "EUR/USD": ["EURUSD=X", "FX_IDC:EURUSD"],
        "GBP/USD": ["GBPUSD=X", "FX_IDC:GBPUSD"]
    }
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
            url = f"https://www.tradingview.com/symbols/{item['tv_id']}"
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
                    url = f"https://www.tradingview.com/symbols/{item['tv_id']}"
                    st.markdown(f"""<a href="{url}" target="_blank" style="text-decoration:none"><div class="market-card">
                        <div class="symbol-name">{item['name']}</div><div class="price">{item['price']:,.2f}</div>
                        <div class="{color}">{arrow} {abs(item['change']):.2f}%</div></div></a>""", unsafe_allow_html=True)

st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
