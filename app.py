import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. DATA ENGINE (The Fix) ---
@st.cache_data(ttl=60) # Updates every 60 seconds
def get_stable_data():
    # We use ETFs (Ending in .NS) because Index tickers (^NSEI) are glitching
    # NIFTYBEES tracks Nifty 50, BANKBEES tracks Bank Nifty, etc.
    mapping = {
        "Nifty 50": "NIFTYBEES.NS",
        "Bank Nifty": "BANKBEES.NS",
        "Nifty IT": "ITBEES.NS",
        "Nifty Pharma": "PHARMABEES.NS",
        "Nifty Junior": "JUNIORBEES.NS",
        "Nifty Gold": "GOLDBEES.NS"
    }
    
    data = []
    tickers = list(mapping.values())
    raw = yf.download(tickers, period="5d", interval="1d", group_by='ticker')
    
    for name, ticker in mapping.items():
        try:
            df = raw[ticker].dropna()
            price = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            change = ((price - prev) / prev) * 100
            data.append({"name": name, "price": price, "change": change})
        except: continue
    return data

# --- 2. THE UI ---
st.set_page_config(page_title="traderspavilion", layout="wide")
st.markdown("<style>.stApp { background: #0e1117; color: white; }</style>", unsafe_allow_html=True)
st.title("⚡ Stable Market Watch")

# Use your existing card-styling CSS here...
sectors = get_stable_data()
cols = st.columns(3)

for i, sector in enumerate(sectors):
    with cols[i % 3]:
        color = "green" if sector['change'] >= 0 else "red"
        st.metric(label=sector['name'], value=f"{sector['price']:,.2f}", delta=f"{sector['change']:.2f}%")
