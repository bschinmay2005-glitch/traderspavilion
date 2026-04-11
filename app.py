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

# --- 3. MASTER MAPPING (TV) ---
TV_MAP = {
    "^NSEI": "NSE:NIFTY", "^NSEBANK": "NSE:BANKNIFTY", "^CNXIT": "NSE:CNXIT",
    "^CNXPHARMA": "NSE:CNXPHARMA", "^CNXAUTO": "NSE:CNXAUTO", "^CNXMETAL": "NSE:CNXMETAL",
    "^CNXFMCG": "NSE:CNXFMCG", "^CNXREALTY": "NSE:CNXREALTY", "^CNXENERGY": "NSE:CNXENERGY",
    "^CNXINFRA": "NSE:CNXINFRA", "^CNXPSUBANK": "NSE:CNXPSUBANK", "^PVTBANK": "NSE:NIFTY_PVT_BANK",
    "MEDIA.NS": "NSE:CNXMEDIA", "^CPSE": "NSE:CPSE", "^CNXFINANCE": "NSE:CNXFINANCE",
    "SERVICES.NS": "NSE:CNXSERVICE", "COMMODITIES.NS": "NSE:CNXCOMMODITIES",
    "CONSUME.NS": "NSE:CNXCONSUMPTION", "HEALTHY.NS": "NSE:CNXHEALTHCARE",
    "OIL.NS": "NSE:CNXOILGAS", "MAKEINDIA.NS": "NSE:CNXMANUFACTURING", 
    "DEFENCE.NS": "NSE:DEFENCE"
}

# --- 4. DATA ENGINE (The Fix) ---
@st.cache_data(ttl=30) # Reduced TTL for faster updates
def fetch_data(symbols_dict, timeframe):
    data_list = []
    # Fetching 7 days to ensure we always have data even over weekends
    for name, sym in symbols_dict.items():
        try:
            t = yf.Ticker(sym)
            df = t.history(period="7d")
            if not df.empty:
                current_price = df['Close'].iloc[-1]
                # Dynamic change calculation based on timeframe slider
                if timeframe == "1d":
                    prev_price = df['Close'].iloc[-2]
                elif timeframe == "5d":
                    prev_price = df['Close'].iloc[0]
                else: # Fallback for 1mo/1y (requires more data)
                    df_long = t.history(period=timeframe)
                    prev_price = df_long['Close'].iloc[0]
                    current_price = df_long['Close'].iloc[-1]
                
                change = ((current_price - prev_price) / prev_price) * 100
                data_list.append({"name": name, "symbol": sym, "price": current_price, "change": change})
        except: continue
    return data_list

# --- 5. CONFIGURATIONS (The 22 Verified Tickers) ---
INDIA_SECTORS = {
    "Nifty 50": "^NSEI", "Bank Nifty": "^NSEBANK", "Nifty IT": "^CNXIT",
    "Nifty Pharma": "^CNXPHARMA", "Nifty Auto": "^CNXAUTO", "Nifty Metal": "^CNXMETAL",
    "Nifty FMCG": "^CNXFMCG", "Nifty Realty": "^CNXREALTY", "Nifty Energy": "^CNXENERGY",
    "Nifty Infra": "^CNXINFRA", "Nifty PSU Bank": "^CNXPSUBANK", "Nifty Pvt Bank": "^PVTBANK",
    "Nifty Media": "MEDIA.NS", "Nifty PSE": "^CPSE", "Nifty Fin Service": "^CNXFINANCE",
    "Nifty Service": "SERVICES.NS", "Nifty Commodities": "COMMODITIES.NS", 
    "Nifty Consumption": "CONSUME.NS", "Nifty Healthcare": "HEALTHY.NS", 
    "Nifty Oil & Gas": "OIL.NS", "Nifty Mfg": "MAKEINDIA.NS", "Nifty Defence": "DEFENCE.NS"
}

GLOBAL_MARKETS = {
    "Indices": {"S&P 500": "^GSPC", "Nasdaq 100": "^IXIC", "DAX": "^GDAXI"},
    "Commodities": {"Gold": "GC=F", "Silver": "SI=F", "Crude Oil": "CL=F"},
    "Forex": {"USD/INR": "USDINR=X", "EUR/USD": "EURUSD=X"}
}

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown("# traders<span style='color:#22c55e'>pavilion</span>", unsafe_allow_html=True)
    st.divider()
    market_view = st.selectbox("Select Market", ["India", "Global Markets"])
    time_slider = st.select_slider("Timeframe", options=["1d", "5d", "1mo", "1y"], value="1d")
    if st.button("🔄 Force Refresh"):
        st.cache_data.clear()
        st.rerun()

# --- 7. MAIN UI ---
st.title(f"{market_view} Sectoral Watch")
target_dict = INDIA_SECTORS if market_view == "India" else {}

if market_view == "Global Markets":
    for sub in GLOBAL_MARKETS.values(): target_dict.update(sub)

market_data = fetch_data(target_dict, time_slider)

# GRID SYSTEM
cols = st.columns(4)
for i, item in enumerate(market_data):
    with cols[i % 4]:
        pos = item['change'] >= 0
        color = "change-pos" if pos else "change-neg"
        arrow = "▲" if pos else "▼"
        
        # Link Logic
        tv_id = TV_MAP.get(item['symbol'], item['symbol'].replace('^', '').replace('.NS', ''))
        url = f"https://www.tradingview.com/symbols/{tv_id}"
        
        st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration:none">
                <div class="market-card">
                    <div class="symbol-name">{item['name']}</div>
                    <div class="price">{item['price']:,.2f}</div>
                    <div class="{color}">{arrow} {abs(item['change']):.2f}%</div>
                </div>
            </a>""", unsafe_allow_html=True)

st.caption(f"Update time: {datetime.now().strftime('%H:%M:%S')} | Total Sectors Loaded: {len(market_data)}")
