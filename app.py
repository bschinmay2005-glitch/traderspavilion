import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import ccxt

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Global Market Dashboard", layout="wide")

FINNHUB_API_KEY = "YOUR_FINNHUB_API_KEY"
TWELVE_API_KEY = "YOUR_TWELVE_DATA_API_KEY"

# =========================
# AUTO REFRESH (Every 5 sec)
# =========================
st_autorefresh(interval=5000, key="market_refresh")

# =========================
# DARK GLASS UI
# =========================
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 12px;
    margin: 8px 0;
    border-radius: 10px;
    backdrop-filter: blur(10px);
}
.green { color: #00ff9f; font-weight: bold; }
.red { color: #ff4d4d; font-weight: bold; }
a { text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# =========================
# MULTI SOURCE FETCHERS
# =========================

def fetch_finnhub(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    try:
        data = requests.get(url).json()
        return {
            "price": data.get("c"),
            "change": data.get("dp")
        }
    except:
        return None

def fetch_twelve(symbol):
    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={TWELVE_API_KEY}"
    try:
        data = requests.get(url).json()
        return {
            "price": float(data.get("price")),
            "change": float(data.get("percent_change"))
        }
    except:
        return None

def fetch_crypto(symbol):
    exchange = ccxt.binance()
    try:
        ticker = exchange.fetch_ticker(symbol)
        return {
            "price": ticker["last"],
            "change": ticker["percentage"]
        }
    except:
        return None

def get_data(symbol, market_type="stock"):
    if market_type == "crypto":
        return fetch_crypto(symbol)
    data = fetch_finnhub(symbol)
    if data and data["price"]:
        return data
    return fetch_twelve(symbol)

# =========================
# GLOBAL DATA STRUCTURE
# =========================

markets = {
    "USA": {
        "Tech": ["AAPL", "MSFT", "NVDA"],
        "Finance": ["JPM", "GS"],
        "Energy": ["XOM", "CVX"]
    },
    "India": {
        "Tech": ["TCS.NS", "INFY.NS"],
        "Finance": ["HDFCBANK.NS", "ICICIBANK.NS"],
        "Energy": ["RELIANCE.NS"]
    },
    "Europe": {
        "Tech": ["SAP.DE"],
        "Finance": ["HSBA.L"]
    }
}

crypto_list = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

global_indices = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "NIFTY 50": "^NSEI",
    "DAX": "^GDAXI",
    "NIKKEI": "^N225"
}

# =========================
# SIDEBAR
# =========================

st.sidebar.title("Market Navigation")

mode = st.sidebar.selectbox(
    "Select Market",
    ["Stock Markets", "Commodity Markets", "Crypto Markets"]
)

timeframe = st.sidebar.selectbox(
    "Timeframe",
    ["1D", "1W", "1M", "1Y"]
)

# =========================
# STOCK MARKET LOGIC
# =========================

if mode == "Stock Markets":

    country = st.sidebar.selectbox("Select Country", list(markets.keys()))
    sector = st.sidebar.selectbox("Select Sector", list(markets[country].keys()))

    st.title(f"{country} - {sector} Stocks")

    for symbol in markets[country][sector]:
        data = get_data(symbol)

        if not data:
            continue

        price = data["price"]
        change = data["change"]

        color_class = "green" if change >= 0 else "red"

        tradingview_url = f"https://www.tradingview.com/chart/?symbol={symbol}"

        st.markdown(f"""
        <div class="card">
            <a href="{tradingview_url}" target="_blank">
                <span>{symbol}</span> |
                <span>{price:.2f}</span> |
                <span class="{color_class}">{change:.2f}%</span>
            </a>
        </div>
        """, unsafe_allow_html=True)

# =========================
# CRYPTO MARKET
# =========================

elif mode == "Crypto Markets":

    st.title("Crypto Market")

    for symbol in crypto_list:
        data = get_data(symbol, market_type="crypto")

        if not data:
            continue

        price = data["price"]
        change = data["change"]

        color_class = "green" if change >= 0 else "red"

        tv_symbol = symbol.replace("/", "")
        tradingview_url = f"https://www.tradingview.com/chart/?symbol=BINANCE:{tv_symbol}"

        st.markdown(f"""
        <div class="card">
            <a href="{tradingview_url}" target="_blank">
                <span>{symbol}</span> |
                <span>{price:.2f}</span> |
                <span class="{color_class}">{change:.2f}%</span>
            </a>
        </div>
        """, unsafe_allow_html=True)

# =========================
# GLOBAL INDICES
# =========================

elif mode == "Commodity Markets":

    st.title("Global Indices")

    for name, symbol in global_indices.items():
        data = get_data(symbol)

        if not data:
            continue

        price = data["price"]
        change = data["change"]

        color_class = "green" if change >= 0 else "red"

        tradingview_url = f"https://www.tradingview.com/chart/?symbol={symbol}"

        st.markdown(f"""
        <div class="card">
            <a href="{tradingview_url}" target="_blank">
                <span>{name}</span> |
                <span>{price:.2f}</span> |
                <span class="{color_class}">{change:.2f}%</span>
            </a>
        </div>
        """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================

st.markdown("---")
st.caption(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")
