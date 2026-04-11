import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(
    page_title="traderspavilion",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GLASSMORPHISM CSS ---
def local_css():
    st.markdown("""
        <style>
        .stApp {
            background: radial-gradient(circle at top left, #1a1c2c, #4a192c);
        }
        .market-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            transition: transform 0.3s ease;
            cursor: pointer;
            text-decoration: none !important;
            display: block;
            margin-bottom: 20px;
        }
        .market-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.1);
        }
        .symbol-name { font-size: 0.9rem; color: #888ea8; font-weight: 600; margin-bottom: 5px; }
        .price { font-size: 1.4rem; font-weight: 700; color: white; }
        .change-pos { color: #00ff88; font-size: 0.85rem; }
        .change-neg { color: #ff3b3b; font-size: 0.85rem; }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=60)
def fetch_market_data(symbols, period="1d"):
    data_list = []
    for name, sym in symbols.items():
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period=period)
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[0]
                pct_change = ((current_price - prev_price) / prev_price) * 100
                data_list.append({
                    "name": name,
                    "symbol": sym,
                    "price": current_price,
                    "change": pct_change
                })
        except:
            continue
    return data_list

# --- 4. CONFIGURATION ---
MARKETS = {
    "Global Indices": {
        "Nifty 50": "^NSEI",
        "S&P 500": "^GSPC",
        "Nasdaq 100": "^IXIC",
        "DAX 40": "^GDAXI",
        "Nikkei 225": "^N225"
    },
    "Commodities": {
        "Gold": "GC=F",
        "Silver": "SI=F",
        "Crude Oil": "CL=F",
        "Copper": "HG=F",       # Added Copper
        "Steel": "HRC=F",       # Added US Midwest Domestic Hot-Rolled Coil Steel
        "Lithium (LIT)": "LIT",  # Added Lithium Proxy (ETF)
        "Natural Gas": "NG=F"
    },
    "Forex": {
        "USD/INR": "USDINR=X",
        "EUR/USD": "EURUSD=X"
    }
}

# --- 5. UI LAYOUT ---
st.markdown("# traders<span style='color:#22c55e'>pavilion</span>", unsafe_allow_html=True)

timeframe = st.select_slider(
    "Select Performance Timeframe",
    options=["1d", "5d", "1mo", "1y"],
    value="1d"
)

tabs = st.tabs(list(MARKETS.keys()))

for i, category in enumerate(MARKETS.keys()):
    with tabs[i]:
        market_data = fetch_market_data(MARKETS[category], period=timeframe)
        cols = st.columns(4)
        
        for idx, item in enumerate(market_data):
            col_idx = idx % 4
            color_class = "change-pos" if item['change'] >= 0 else "change-neg"
            arrow = "▲" if item['change'] >= 0 else "▼"
            
            tv_symbol = item['symbol'].replace('^', '').replace('=F', '').replace('=X', '')
            url = f"https://www.tradingview.com/symbols/{tv_symbol}"
            
            card_html = f"""
                <a href="{url}" target="_blank" style="text-decoration: none;">
                    <div class="market-card">
                        <div class="symbol-name">{item['name']}</div>
                        <div class="price">${item['price']:,.2f}</div>
                        <div class="{color_class}">
                            {arrow} {abs(item['change']):.2f}% ({timeframe})
                        </div>
                    </div>
                </a>
            """
            cols[col_idx].markdown(card_html, unsafe_allow_html=True)

# --- 6. FOOTER & DATA TABLE ---
st.divider()
with st.expander("View Detailed Raw Data"):
    # Combine all data for the table
    all_data = []
    for cat in MARKETS:
        all_data.extend(fetch_market_data(MARKETS[cat], period=timeframe))
    df = pd.DataFrame(all_data)
    if not df.empty:
        st.dataframe(df[["name", "price", "change"]], use_container_width=True)

st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')} | Data: Yahoo Finance")
