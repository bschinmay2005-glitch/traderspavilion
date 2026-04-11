import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="TradersPavilion | Sectoral Velocity", layout="wide")

# Custom CSS for Branding
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stApp { color: #f1f5f9; }
    h1 { font-weight: 800; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# Branding Header
st.markdown("# Traders<span style='color:#22c55e'>Pavilion</span>", unsafe_allow_html=True)
st.write("### Sectoral Analysis • Previous Close vs Real-time")
st.divider()

@st.cache_data(ttl=60)  # Refresh data every 60 seconds
def fetch_nse_data():
    url = "https://www.nseindia.com/api/allIndices"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)
        response = session.get(url, headers=headers)
        data = response.json()['data']
        
        # Filter for key sectoral indices
        target_sectors = [
            "NIFTY BANK", "NIFTY IT", "NIFTY AUTO", "NIFTY FMCG", 
            "NIFTY METAL", "NIFTY PHARMA", "NIFTY REALTY", "NIFTY MEDIA"
        ]
        
        processed_data = []
        for item in data:
            if item['index'] in target_sectors:
                processed_data.append({
                    "Sector": item['index'].replace("NIFTY ", ""),
                    "Change %": item['percentChange'],
                    "LTP": item['last'],
                    "Color": "green" if item['percentChange'] >= 0 else "red"
                })
        
        return pd.DataFrame(processed_data).sort_values("Change %", ascending=True)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Execution
df = fetch_nse_data()

if not df.empty:
    # Summary Metrics
    col1, col2 = st.columns(2)
    top_gainer = df.iloc[-1]
    top_loser = df.iloc[0]
    
    col1.metric("Top Outperformer", top_gainer['Sector'], f"{top_gainer['Change %']}%")
    col2.metric("Top Underperformer", top_loser['Sector'], f"{top_loser['Change %']}%", delta_color="inverse")

    # The Chart
    # Streamlit's st.bar_chart is simple, but for conditional colors, we use st.column_config
    st.write("#### Nifty Sectoral Heatmap (%)")
    
    st.bar_chart(
        data=df,
        x="Sector",
        y="Change %",
        color="Color",  # This highlights the Green/Red logic
        horizontal=True,
        height=500
    )

    # Raw Data Tableimport streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

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
        /* Main Background */
        .stApp {
            background: radial-gradient(circle at top left, #1a1c2c, #4a192c);
        }
        
        /* Glassmorphism Card Style */
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
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .symbol-name { font-size: 0.9rem; color: #888ea8; font-weight: 600; margin-bottom: 5px; }
        .price { font-size: 1.4rem; font-weight: 700; color: white; }
        .change-pos { color: #00ff88; font-size: 0.85rem; }
        .change-neg { color: #ff3b3b; font-size: 0.85rem; }
        
        /* Remove Streamlit default padding */
        .main .block-container { padding-top: 2rem; }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=60) # Cache for 1 minute for "Real-time" feel without hitting rate limits
def fetch_market_data(symbols, period="1d"):
    data_list = []
    for name, sym in symbols.items():
        try:
            ticker = yf.Ticker(sym)
            # Fetch history based on user timeframe
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
        except Exception as e:
            continue
    return data_list

# --- 4. CONFIGURATION ---
MARKETS = {
    "Global Indices": {
        "Nifty 50": "^NSEI",
        "S&P 500": "^GSPC",
        "Nasdaq 100": "^IXIC",
        "FTSE 100": "^FTSE",
        "Nikkei 225": "^N225"
    },
    "Commodities": {
        "Gold": "GC=F",
        "Silver": "SI=F",
        "Crude Oil": "CL=F",
        "Natural Gas": "NG=F"
    },
    "Forex": {
        "USD/INR": "USDINR=X",
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "JPY=X"
    }
}

# --- 5. UI LAYOUT ---
st.title("traderspavilion")

# Timeframe Selector
timeframe = st.select_slider(
    "Select Performance Timeframe",
    options=["1d", "5d", "1mo", "1y"],
    value="1d",
    help="Calculates percentage change from the start of the selected period."
)

# Categories Tabs
tabs = st.tabs(list(MARKETS.keys()))

for i, category in enumerate(MARKETS.keys()):
    with tabs[i]:
        market_data = fetch_market_data(MARKETS[category], period=timeframe)
        
        # Create a 4-column grid
        cols = st.columns(4)
        
        for idx, item in enumerate(market_data):
            col_idx = idx % 4
            
            color_class = "change-pos" if item['change'] >= 0 else "change-neg"
            arrow = "▲" if item['change'] >= 0 else "▼"
            
            # TradingView URL Logic
            # Note: Tickers like ^NSEI need to be converted to NSE:NIFTY for TradingView
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

# Footer Auto-Refresh Info
st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')} | Data provided by Yahoo Finance")
    with st.expander("View Detailed Prices"):
        st.dataframe(df[["Sector", "LTP", "Change %"]], use_container_width=True)
else:
    st.warning("Waiting for Market Data... Ensure you are running this during market hours.")

st.caption("Data source: NSE India. Analysis starts from previous day closing.")
